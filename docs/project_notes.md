# Research context and limits

## Project identity and roles

**ProbabilityTheoryFormalization** is the public project name. It studies AI
agent workflows and verification using textbook probability formalization.
Older identifiers retain the historical project name.

Shuo Deng directs requirements, coordinates AI-assisted execution, and operates
and reviews the workflow and formalization results. Kenneth W. Shum is the source textbook author, a coauthor of the
preprint, and maintainer of the collaborating textbook repository.

Public provenance:

- The [collaborating repository's contributor statement](https://github.com/wkshum/ProbabilityTheory#contributors)
  credits Shuo Deng and explicitly acknowledges AI assistance.
- [Chapter 2 interface alignment](https://github.com/wkshum/ProbabilityTheory/pull/7)
  and [Chapter 3 measure extension](https://github.com/wkshum/ProbabilityTheory/pull/8)
  were authored by Shuo Deng's account and merged on 15 July 2026.
- [The preprint](https://arxiv.org/abs/2607.27298) lists Shuo Deng first and
  Kenneth W. Shum second. Section 4 describes the workflow; the acknowledgements
  disclose AI assistance.

These sources establish roles, collaboration, and inspectable outputs. Git
authorship does not establish that every line was handwritten or that every
review was performed by a human.

## Paper and ongoing evaluation

[*From Lecture Notes to Lean: Formalizing a Textbook on Probability Theory*](https://arxiv.org/abs/2607.27298)
is an **arXiv preprint**, submitted on 29 July 2026, by Shuo Deng and Kenneth W.
Shum. Its scope is the textbook formalization and its interfaces with Mathlib.

**Current study (15 September 2026):** [*How probability proofs are completed*](https://github.com/Kind-NK-Hill/review-history-evaluation)
is a separate technical report by Shuo Deng and Kenneth W. Shum, now at report
revision 30 / public v0.7.0. It examines 66 primary runs (11 task groups, three
configurations, two batches), completion judgments, elapsed time, historical
proof composition and proof handoffs. The H1 caller changes the interpretation
of missing work; L6 exposes task-scope ambiguity; M2 separates a completed proof
from its delivery and subsequent use. Selected evidence and arithmetic
reproduction are public. The study does not establish independent human ground
truth for all judgments or isolate a causal benefit of a single mechanism.

**Earlier historical analysis:** the review-history study first reconstructed
historical records and described candidate repair. The fixed
analysis population contains 3,231 distinct review-evidence signatures, not
independent executions. Later stages distinguish candidate repair from official
re-review, external review and duplicate representations of the same review.

The first-round repair analysis uses 230 fail-origin episodes and separates the
first recorded PASS from later revisions. Its changing risk sets show task
composition and selection effects; it does not identify a stable within-task
effect of attempt count. Same-condition independent repeat reviews are absent
from this historical sample. Automated finding alignment has not become an
independently adjudicated resolution label.

Those early results describe retained historical research data. They are not
independent mathematical truth labels, reviewer accuracy, a repair success rate,
or causal evidence that the review process improves outcomes. The study is maintained in the separate evaluation repository; this runtime
repository is the engineering entry point.

Three separately inspectable additions support engineering and future evaluation:

- The [complete workflow demonstration](workflow_demo.md) runs production APIs,
  real Lean builds and isolated state using recorded teaching opinions by default.
- The [review-basis pilot](review_basis_pilot.md) explains invalidation dimensions
  and tests explicit target/proof/evidence/state identities; it does not relax
  acceptance or measure historical invalidation rates.
- The [paired review pilot](review_comparison_pilot.md) prepares ordinary and
  blind-translation-assisted review under matched total budgets. Prospective
  model runs and independent human adjudication remain pending; synthetic QA is
  not evidence of quality gain.

## Related work

- [APOLLO](https://arxiv.org/abs/2505.05758) is acknowledged in the preprint as
  an inspiration for agent-assisted Lean proof repair.
- [M2F](https://github.com/optsuite/M2F) addresses project-scale translation of
  mathematical literature into Lean, including planning and proof generation.
- [Prove2Me](https://prove2.me/about) provides a collaborative platform where
  missions are decomposed into formal statements and submitted proofs are
  checked by Lean.

M2F and Prove2Me provide related context, not evidence of an integration or a
measured comparison in this repository. This project focuses on a probability
textbook and inspectable source review, version binding, and repair histories.
Claims of research novelty or comparative performance require evidence beyond
the homepage examples.

## What the public evidence supports

The [eight public cases](../examples/case-studies/) are selected mechanism
demonstrations. Each connects a failure or explicit exception to an inspectable
repair record. They are not an unbiased sample and do not establish accuracy,
cost savings, productivity, or fully autonomous mathematical correctness.

A Lean build checks the formal declarations in a particular environment.
Whether those declarations express the intended textbook mathematics requires
a separate interpretation and review. Model-assisted review can also be wrong.

The short snapshots for the triangular-array theorem demonstrate its interface
change using reduced predicates. They do not reproduce its complete proof;
the case page links the full implementation.

The complete textbook-derived input corpus and mutable review packs are
retained outside the public source tree. See
[repository scope](repository_scope.md) for evidence boundaries and publication
history, and [development](development.md) for verified setup and platform limits.
