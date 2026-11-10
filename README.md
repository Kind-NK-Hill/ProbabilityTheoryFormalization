# ProbabilityTheoryFormalization

**AI Agent Workflows & Verification**

A research project that uses a probability textbook to develop AI-assisted code
generation, checking, review, and repair. The goal is to make generated Lean
code match the intended mathematics and remain usable by the modules that depend
on it.

**中文概述**：以概率论教材为场景，研究和开发 AI 辅助代码生成、自动检查、独立审查与迭代修复流程，保留可追溯的失败和修复记录。[阅读中文版](README.zh-CN.md)

**Shuo Deng:** project creator. Defined the problem and requirements, made the design decisions, organized AI-assisted development, ran the workflow and delivered the results; first author of the linked preprint. Research period: March to early September 2026. This page describes the current public snapshot.
**Technology stack:** Python · Lean 4 · SQLite · automated verification.

[Paper](https://arxiv.org/abs/2607.27298) ·
[Run the complete workflow](docs/workflow_demo.md) ·
[Project scope and outputs](docs/project_overview.md) ·
[Two representative cases](#two-representative-cases) ·
[Merged collaboration](https://github.com/wkshum/ProbabilityTheory/pull/8) ·
[Contact](mailto:kdsdengshuo2823@gmail.com)

## My role and contributions

I am **Shuo Deng**, the creator of this project, working with textbook author Kenneth W. Shum on textbook formalization and its workflow.

- **Workflow design and directed implementation:** specify the task, generation, checking, semantic-review and repair workflow, decide its trade-offs, and direct its AI-assisted implementation.
  [Workflow and architecture](docs/phase2/workflow.md)
- **Verification and state management:** bind reviews to checked code and
  dependencies, retain repair records and reject outdated approvals.
  [State and evidence model](docs/workspace_state.md)
- **Failure analysis and research:** investigate missing assumptions, changed theorem interfaces and broken downstream use; submit fixes merged by the textbook author; coauthor the probability-formalization preprint.
  [Cases](examples/case-studies/) · [Merged fixes](https://github.com/wkshum/ProbabilityTheory/pull/7)

**Collaboration and tools.** Kenneth W. Shum is the textbook author and paper
coauthor, and maintains the [collaborating textbook repository](https://github.com/wkshum/ProbabilityTheory).
Development uses AI tools for coding, proof search, analysis and writing.

## Outputs you can inspect

| Output | Evidence |
| --- | --- |
| **First-author preprint** | [*From Lecture Notes to Lean*](https://arxiv.org/abs/2607.27298) — **Shuo Deng**, Kenneth W. Shum. arXiv preprint, July 2026. It covers the textbook formalization and its Mathlib interfaces; Section 4 describes the agent workflow used at the time. |
| **Catalog and corpus size** | 452 formal tasks and 584 Lean modules (452 primary, 108 task-owned support, 24 shared support). These are sizes, not a completion rate. [Definitions](docs/workspace_state.md#current-catalog-and-corpus) |
| **Runnable workflow** | [Complete production-API demonstration](docs/workflow_demo.md): real Lean builds, isolated SQLite state, caller repair and stale-review rejection. Default opinions are recorded teaching reviews. |
| **Public system and cases** | [Workflow implementation](src/formalization_engine/) and [eight selected cases](examples/case-studies/), with code comparisons and review timelines. |
| **Merged collaboration** | [Chapter 2: align assumptions and interfaces](https://github.com/wkshum/ProbabilityTheory/pull/7) and [Chapter 3: refactor measure extension](https://github.com/wkshum/ProbabilityTheory/pull/8), both merged into Kenneth's repository. |

## Later independent studies

Two studies share this project's background but have their own questions, data and conclusions. Their runs and items are not experiments of this project.

| Study | Content | Relation to this repository |
| --- | --- | --- |
| [Agent workflow evaluation](https://github.com/Kind-NK-Hill/review-history-evaluation) | 66 primary runs across 11 task groups, three configurations and two batches. Technical report, Shuo Deng and Kenneth W. Shum, September 2026. | Studies one fixed revision of this engine. |
| [Semantic reviewer evaluation](https://github.com/Kind-NK-Hill/semantic-reviewer-evaluation) | 858 items, two model routes, calibrated against externally published labels. Evaluation report, Shuo Deng, November 2026. | Tests an adapted prompt, not a replay of this engine's full reviewer. |

The optional [`evaluations/review-history`](evaluations/review-history) submodule pins an earlier study snapshot; it is not required to run the engine. See [project scope](docs/project_overview.md).

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

The system checks compilation, then a read-only semantic-review role checks the intended meaning; changes are accepted only while the reviewed code and dependencies remain current. Under the current [review contract](docs/phase2/agent_review_contract.md), review in the repair loop is performed by an independent subagent that did not author that change, or by a configured review runner, and `reviewer_independence` is recorded. "Independent" means workflow role separation; it does not mean human review or necessarily a different model, and the contract does not describe every historical record. Model-assisted review is evidence, not a guarantee of mathematical correctness.

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

