#!/usr/bin/env python3
"""Check the public tree's publication boundary and normalized file fingerprints."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_public_release import digest, normalized
from public_release_policy import forbidden, selected
from prepare_public_snapshot import check as check_source_prose


PUBLIC_TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".svg", ".toml", ".txt", ".tex", ".lean"}
PERSONAL_HOME_PATH = re.compile(
    r"(?:\b[A-Za-z]:[\\/]+Users[\\/]+|(?<![\w:])/(?:home|Users)/)"
    r"(?P<user>[^\\/\s\"'`<>]+)",
    re.IGNORECASE,
)
OWNER_WORKSPACE_PATH = re.compile(
    r"\b[A-Za-z]:[\\/]+Grad_Study[\\/]+Practimum[\\/]+Formalization\b",
    re.IGNORECASE,
)
EXAMPLE_USER_NAMES = {"user", "username", "your-user", "your_username", "example", "example-user", "$user", "${user}"}

# Optional public companions are pinned Git links, not exported runtime files.
# Keep this list exact: adding a submodule must not allow arbitrary local trees.
PUBLIC_SUBMODULES = {
    "evaluations/review-history": {
        "name": "review-history-evaluation",
        "url": "https://github.com/Kind-NK-Hill/review-history-evaluation.git",
    }
}


def check_public_submodules(root: Path, declared: object) -> tuple[set[str], list[str]]:
    if not isinstance(declared, dict):
        return set(), ["publication git_submodules must be an object"]
    if not declared:
        return set(), []
    allowed, errors, expected_config = set(), [], {}
    for path, binding in declared.items():
        policy = PUBLIC_SUBMODULES.get(path)
        if policy is None or not isinstance(binding, dict):
            errors.append(f"unapproved public submodule: {path}")
            continue
        allowed.add(path)
        commit = binding.get("commit", "")
        if binding.get("url") != policy["url"]:
            errors.append(f"public submodule URL mismatch: {path}")
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            errors.append(f"public submodule commit must be a full Git object: {path}")
        # Read the superproject index, so CI also works with uninitialized modules.
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--stage", "--", path],
            capture_output=True, text=True,
        )
        expected_entry = f"160000 {commit} 0\t{path}"
        if result.returncode or result.stdout.strip() != expected_entry:
            errors.append(f"public submodule Git link mismatch: {path}")
        prefix = f"submodule.{policy['name']}."
        expected_config[prefix + "path"] = path
        expected_config[prefix + "url"] = policy["url"]
    config = subprocess.run(
        ["git", "config", "--file", str(root / ".gitmodules"), "--list"],
        capture_output=True, text=True,
    )
    lines = [line for line in config.stdout.splitlines() if line]
    actual_config = dict(line.split("=", 1) for line in lines if "=" in line)
    if config.returncode or actual_config != expected_config or len(lines) != len(expected_config):
        errors.append("public .gitmodules configuration differs from approved companions")
    return allowed, errors


def machine_path_findings(relative_path: str, text: str) -> list[str]:
    """Check published prose/data, excluding code and deliberate test fixtures.

    Generic setup paths such as C:/work, /absolute/path and placeholder users
    remain valid examples. Personal home roots and the owner's known workspace
    root must not leak through documentation, rules, examples or JSON exports.
    """
    path = relative_path.replace("\\", "/")
    if path.startswith(("src/", "tools/", "tests/")) or Path(path).suffix not in PUBLIC_TEXT_SUFFIXES:
        return []
    errors = []
    for number, line in enumerate(text.splitlines(), 1):
        personal_home = any(
            match.group("user").casefold() not in EXAMPLE_USER_NAMES
            for match in PERSONAL_HOME_PATH.finditer(line)
        )
        if personal_home or OWNER_WORKSPACE_PATH.search(line):
            errors.append(f"machine-specific path: {path}:{number}")
    return errors


def check(root: Path, paths: list[str]) -> list[str]:
    manifest = json.loads((root / "data/publication/release_manifest.json").read_text(encoding="utf-8"))
    submodules, errors = check_public_submodules(root, manifest.get("git_submodules", {}))
    companion_paths = submodules | ({".gitmodules"} if submodules else set())
    for path in paths:
        if forbidden(path) or not (selected(path) or path in companion_paths or path in {
            "data/publication/corpus_map.json", "data/publication/release_manifest.json"
        }):
            errors.append(f"private path: {path}")
            continue
        if path.startswith(("ToyApollo/", "src/toy_apollo/")) or path in {"run_chapter.py", "ToyApollo.lean"}:
            errors.append(f"retired public runtime path: {path}")
        target = root / path
        if target.is_file() and target.suffix in PUBLIC_TEXT_SUFFIXES:
            errors.extend(machine_path_findings(path, target.read_text(encoding="utf-8")))
    if manifest.get("schema") != "formalization-engine.public-release.v1":
        errors.append("unsupported publication manifest schema")
    if not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("source_commit", ""))):
        errors.append("source_commit must identify a full Git commit")
    if manifest.get("authority") != "publication_integrity_only_not_semantic_review":
        errors.append("publication manifest cannot assert semantic review authority")
    if manifest.get("normalization") != "UTF-8 LF":
        errors.append("unsupported publication normalization")
    expected = {entry["path"]: entry["sha256"] for entry in manifest["files"]}
    if len(expected) != len(manifest["files"]):
        errors.append("duplicate publication manifest paths")
    execution_tools = manifest.get("execution_tools", {})
    required_tools = {f"tools/{name}" for name in (
        "export_public_release.py", "public_release_policy.py", "prepare_public_snapshot.py"
    )}
    if not isinstance(execution_tools, dict) or set(execution_tools) != required_tools:
        errors.append("publication execution tools are not fully identified")
    elif any(expected.get(p) != sha for p, sha in execution_tools.items()):
        errors.append("publication execution tool fingerprints differ from published tools")
    required = {"manifest_by_chapter.csv", "COORDINATION_PROVENANCE.md", "data/publication/corpus_map.json"}
    if not required.issubset(expected):
        errors.append("publication manifest is missing required corpus provenance files")
    corpus_path = root / "data/publication/corpus_map.json"
    if corpus_path.is_file():
        corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
        if corpus.get("schema") != "formalization-engine.public-corpus-map.v1":
            errors.append("unsupported public corpus mapping schema")
        if corpus.get("source_commit") != manifest.get("source_commit"):
            errors.append("corpus and release source commits differ")
        if corpus.get("authority") != manifest.get("authority"):
            errors.append("corpus and release authority declarations differ")
    else:
        errors.append("public corpus mapping is missing")
    actual = set(paths) - {"data/publication/release_manifest.json"} - submodules
    if actual != set(expected):
        errors.append(f"manifest inventory differs: missing={sorted(set(expected)-actual)}, extra={sorted(actual-set(expected))}")
    for p, sha in expected.items():
        if forbidden(p) or not (selected(p) or p == "data/publication/corpus_map.json" or (p == ".gitmodules" and submodules)):
            errors.append(f"private manifest path: {p}")
            continue
        target = root / p
        if not target.is_file() or digest(normalized(target.read_bytes())) != sha:
            errors.append(f"content fingerprint mismatch: {p}")
    errors.extend(f"source prose remains: {p.relative_to(root)}" for p in check_source_prose(root / "ProbabilityTheory"))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--export-directory", action="store_true", help="Check an export before it is added to Git")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.export_directory:
        paths = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    else:
        result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True)
        paths = [p for p in result.stdout.decode().split("\0") if p]
    try:
        errors = check(root, paths)
    except (OSError, ValueError, KeyError) as exc:
        errors = [str(exc)]
    for error in errors:
        print(f"[FAIL] {error}")
    if errors:
        return 1
    print(f"[PASS] public release boundary and {len(paths)} tracked entries; not semantic review authority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
