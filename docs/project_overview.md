# Project scope and public outputs

ProbabilityTheoryFormalization uses Kenneth W. Shum's measure-theoretic probability textbook to study how AI-generated Lean code can compile, match the source statement, and stay usable by dependent modules. Shuo Deng created the project; the research period is March to early September 2026.

**Mechanism.** Each task is bound to its source passage. Candidates go through a real Lean build, then a read-only semantic review. Verdicts are bound to the reviewed code and dependency versions and are rechecked when either changes; validated mechanical rebinding may preserve compatible evidence. Failures and repairs are retained.

**Outputs.** The engine and the `ProbabilityTheory/` corpus, a runnable demonstration, eight selected cases, two merged pull requests in the collaborating repository, and an arXiv preprint.

**Numbers.** The catalog has 452 formal tasks from 445 printed-number families (5 families split into 12 tasks), in 584 modules: 452 primary, 108 task-owned support, 24 shared support. The preprint counts 449 textbook items. The two counts use different units and dates; neither is a completion rate.

**Related work.** The preprint covers the formalization and its Mathlib interfaces; its Section 4 relates to this engine but is not an empirical evaluation of the current one. The 66-run agent workflow evaluation and the 858-item semantic reviewer evaluation are separate studies with their own data.
