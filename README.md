# ProbabilityTheoryFormalization

**AI Agent Workflows & Verification**

A research project that uses a probability textbook to develop AI-assisted code
generation, checking, review, and repair. The goal is to make generated Lean
code match the intended mathematics and remain usable by the modules that depend
on it.

**中文概述**：以概率论教材为场景，研究和开发 AI 辅助代码生成、自动检查、独立审查与迭代修复流程，保留可追溯的失败和修复记录。[阅读中文版](README.zh-CN.md)

**Shuo Deng:** requirements, agent coordination, operation and review of the
AI-assisted workflow; first author of the linked preprint.
**System technologies:** Python · Lean 4 · SQLite · automated verification.

[Paper](https://arxiv.org/abs/2607.27298) ·
[Run the complete workflow](docs/workflow_demo.md) ·
[Agent evaluation study](https://github.com/Kind-NK-Hill/review-history-evaluation) ·
[Two representative cases](#two-representative-cases) ·
[Merged collaboration](https://github.com/wkshum/ProbabilityTheory/pull/8) ·
[Contact](mailto:kdsdengshuo2823@gmail.com)

## My role and contributions

I am **Shuo Deng**, a contributor to this workflow and the textbook
formalization. My work, with AI assistance, covers:

- **Requirements and agent coordination:** direct task requirements, coordinate
  code generation, builds and review, inspect failures, and request corrections. [Workflow and architecture](docs/phase2/workflow.md)
- **Workflow operation and review:** operate and inspect the mechanisms that
  bind reviews to checked code and dependencies, retain repair records and
  reject outdated approvals. SQLite is part of the system implementation.
  [State and evidence model](docs/workspace_state.md)
- **Failure analysis and research:** investigate missing assumptions, changed
  theorem interfaces, and broken downstream use; contribute reviewed fixes
  and coauthor the probability-formalization preprint.
  [Cases](examples/case-studies/) · [Merged fixes](https://github.com/wkshum/ProbabilityTheory/pull/7)

**Collaboration and AI assistance.** Kenneth W. Shum is the textbook author and
paper coauthor, and maintains the [collaborating textbook repository](https://github.com/wkshum/ProbabilityTheory).
My role centers on requirements, execution coordination and result review; source corrections
are discussed with the textbook author. AI tools assist with code generation,
proof search, repairs, review, and documentation. These artifacts are not a claim
of wholly handwritten work; mathematical interpretation still requires human judgment.

## Outputs you can inspect

| Output | Evidence |
| --- | --- |
| **First-author preprint** | [*From Lecture Notes to Lean: Formalizing a Textbook on Probability Theory*](https://arxiv.org/abs/2607.27298) — **Shuo Deng**, Kenneth W. Shum. **arXiv preprint**, July 2026. |
| **Runnable workflow** | [Complete production-API demonstration](docs/workflow_demo.md): real Lean builds, isolated SQLite state, caller repair and stale-review rejection. Default opinions are recorded teaching reviews. |
| **Public system and cases** | [Workflow implementation](src/formalization_engine/) and [eight selected cases](examples/case-studies/), with code comparisons and review timelines. |
| **Agent evaluation study** | [*How probability proofs are completed*](https://github.com/Kind-NK-Hill/review-history-evaluation): 66 primary runs across 11 task groups, three configurations and two batches, with completion reassessment and proof-handoff analysis. Technical report, revision 30 / public v0.7.0. |
| **Merged collaboration** | [Chapter 2: align assumptions and interfaces](https://github.com/wkshum/ProbabilityTheory/pull/7) and [Chapter 3: refactor measure extension](https://github.com/wkshum/ProbabilityTheory/pull/8), both merged into Kenneth's repository. |

The evaluation study now examines delivered mathematics, matched-task time
comparisons, historical proof composition and whether collaborators' results
reached their intended recipients. Its H1, L6 and M2 cases distinguish missing
work, ambiguous task scope and failed delivery. The configurations bundle
several differences; these observations do not isolate a causal review benefit
or provide independent human validation of every judgment.
[Current report and evidence](https://github.com/Kind-NK-Hill/review-history-evaluation/tree/main/report-v30)
· [Research history and limits](docs/project_notes.md#paper-and-ongoing-evaluation)

The [evaluation repository](https://github.com/Kind-NK-Hill/review-history-evaluation)
contains the report, selected evidence, analysis scripts and saved results.
It is linked here as the optional
[`evaluations/review-history`](evaluations/review-history) Git submodule; running
the formalization workflow does not require initializing it. The pinned submodule
is an earlier snapshot; use the repository link above for the latest study.

## Two representative cases

### Catch code that compiles but omits a required condition

**Problem:** a definition intended for probability measures accepted arbitrary
measures, allowing misleading values outside the intended domain.
**Action:** review identified the missing conditions; repair added explicit
probability-measure requirements and updated affected callers.
**Result:** the corrected definition and its downstream use received a fresh
passing review. Both the initial and final code compile.

[Code and review history](examples/case-studies/def_8_5/) ·
[Before](examples/case-studies/def_8_5/initial.lean) ·
[After](examples/case-studies/def_8_5/final.lean)

### Repair a module, then check and repair its downstream callers

**Problem:** a theorem compiled by taking its missing proof as an input.
Replacing that input with an internal proof still left a caller using the old interface.
**Action:** implement the proof, add the interface needed by the caller, and
migrate the caller through another review cycle.
**Result:** a fresh review accepted the repaired theorem and downstream migration.

[Case and timeline](examples/case-studies/thm_14_8/) ·
[Full proof](ProbabilityTheory/chapter_14/thm_14_8.lean)

The second case's short before/after files are **reduced interface demonstrations**;
the full mathematical proof is linked separately. All eight cases are selected
examples, **not an accuracy, cost, or productivity benchmark**.

![A real review sequence: compiling code, missing conditions, caller migration, and a fresh passing review](docs/images/def85-review.svg)

*Based on the [first case's retained review timeline](examples/case-studies/def_8_5/review-timeline.json);
the code lines are excerpts from its public snapshots.*

## Technical reading

The system checks compilation, reviews the intended meaning independently, then
accepts changes only while the reviewed code and dependencies remain current.
Model-assisted review is evidence, not a guarantee of mathematical correctness.

- [Architecture](docs/architecture.md) and [workflow](docs/phase2/workflow.md)
- [Run the complete workflow](docs/workflow_demo.md)
- [Review-basis identity experiment](docs/review_basis_pilot.md) and [prospective comparison protocol](docs/review_comparison_pilot.md)
- [Installation and verification commands](docs/development.md)
- [All eight cases and reproduction commands](examples/case-studies/)
- [Review criteria](docs/phase2/review_criteria.md) and [status contract](docs/phase2/status_contract.md)
- [Research context, related work, and limits](docs/project_notes.md)
- [Repository scope and publication history](docs/repository_scope.md)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [MIT License](LICENSE)

The project was formerly called **ToyApollo**; historical schemas and case evidence
retain that name. The active command is `formalize`, the package is
`src/formalization_engine/`, and the corpus is `ProbabilityTheory/`. Use **ProbabilityTheoryFormalization** when citing
the project.
