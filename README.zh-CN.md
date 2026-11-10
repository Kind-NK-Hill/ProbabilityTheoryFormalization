# ProbabilityTheoryFormalization

**智能体工作流与验证**

以概率论教材为场景，研究和开发 AI 辅助代码生成、自动检查、独立审查与迭代修复流程。目标是让生成的 Lean 代码符合原文含义，并能被其他模块正确调用，同时保留可追溯的失败和修复记录。

**项目发起人**：Shuo Deng。提出问题与需求、决定方案取舍、组织 AI 辅助开发、运行流程并根据反馈完成交付；下方预印本第一作者。研究时间 2026.03—2026.09 上旬，本页介绍当前公开快照。

**技术栈**：Python、Lean 4、SQLite、自动化验证。

[English](README.md) · [论文](https://arxiv.org/abs/2607.27298) · [项目内容与公开成果](docs/project_overview.zh-CN.md) · [运行完整流程](docs/workflow_demo.md) · [两个代表案例](#两个代表案例) · [已合并的协作贡献](https://github.com/wkshum/ProbabilityTheory/pull/8) · [联系邮箱](mailto:kdsdengshuo2823@gmail.com)

## 我的职责与贡献

我是 **Shuo Deng**，本项目的发起人，与教材作者 Kenneth W. Shum 合作开展教材形式化及其工作流研究。

- **工作流设计与组织实现**：提出任务组织、代码生成、自动检查、语义审查与反馈修复的流程需求，决定方案取舍，并组织 AI 辅助实现。[流程与架构](docs/phase2/workflow.md)
- **验证与状态管理**：将审查结论绑定到实际代码和依赖版本，保留修复记录，拒绝使用过期判断批准新交付。[状态与证据管理](docs/workspace_state.md)
- **失败分析与研究**：分析遗漏条件、定理接口变化和下游调用问题，提交修订并由教材作者合并至协作仓库，共同撰写概率论形式化预印本。[完整案例](examples/case-studies/) · [已合并修订](https://github.com/wkshum/ProbabilityTheory/pull/7)

**合作与工具**：Kenneth W. Shum 是教材作者、论文合作者，并维护[协作教材仓库](https://github.com/wkshum/ProbabilityTheory)。项目开发使用人工智能工具辅助编码、证明搜索、分析和写作。

## 可查看的成果

| 成果 | 证据入口 |
| --- | --- |
| **第一作者预印本** | [*From Lecture Notes to Lean: Formalizing a Textbook on Probability Theory*](https://arxiv.org/abs/2607.27298)，作者：**Shuo Deng**、Kenneth W. Shum。arXiv 预印本，2026 年 7 月。主题是教材形式化及其与 Mathlib 的接口，第 4 节描述当时使用的智能体工作流。 |
| **目录与正文规模** | 452 个正式任务、584 个 Lean 模块（452 个主模块、108 个任务所属支持模块、24 个共享支持模块）。这是规模，不是完成率。[口径说明](docs/workspace_state.md#current-catalog-and-corpus) |
| **可运行的完整流程** | [正式接口演示](docs/workflow_demo.md)：真实 Lean 编译、隔离数据库、调用方修复和旧审查拒绝。默认使用已登记的教学审查。 |
| **公开系统与案例** | [工作流实现](src/formalization_engine/)与[八个精选案例](examples/case-studies/)，包含代码对照和审查时间线。 |
| **已合并的协作贡献** | [第二章：对齐假设与接口](https://github.com/wkshum/ProbabilityTheory/pull/7)、[第三章：重构测度扩张](https://github.com/wkshum/ProbabilityTheory/pull/8)，均已合并至 Kenneth 的仓库。 |

## 后续独立研究

以下两项研究与本项目背景相同，但各有自己的问题、数据和结论，其运行和题目不计入本项目的实验。

| 研究 | 内容 | 与本工程的关系 |
| --- | --- | --- |
| [智能体工作流评估](https://github.com/Kind-NK-Hill/review-history-evaluation) | 11 组任务、三种配置、两批共 66 次主运行，考察完成判断、历史证明组合与证明交接。技术报告，Shuo Deng、Kenneth W. Shum，2026 年 9 月。 | 引用本工程的一个固定版本作为研究对象。 |
| [语义审核模型评估](https://github.com/Kind-NK-Hill/semantic-reviewer-evaluation) | 858 道题、两条模型路线，用外部已发布标签校准语义审查组件。评估报告，Shuo Deng，2026 年 11 月。 | 测试的是改编提示词，不是本工程完整审查器的重放。 |

可选的 [`evaluations/review-history`](evaluations/review-history) 子模块固定在第一项研究的较早快照，运行形式化流程无需初始化它。三者的联系见[项目内容与公开成果](docs/project_overview.zh-CN.md)。

## 两个代表案例

### 发现自动检查通过、但遗漏适用条件的代码

**问题**：一个原本针对概率测度的定义接受了任意测度，可能在适用范围外产生误导性结果。

**处理**：审查定位缺失条件，修复显式补上概率测度约束，并更新受影响的调用方。

**结果**：修正后的定义及下游用法通过了新的审查。初始版本和最终版本都能编译，区别在于是否表达了预期的数学含义。

[代码与完整记录](examples/case-studies/def_8_5/) · [修复前](examples/case-studies/def_8_5/initial.lean) · [修复后](examples/case-studies/def_8_5/final.lean)

### 修复当前模块后，继续检查并修复下游调用

**问题**：一个定理通过把缺失的证明当作输入而获得编译通过。补上内部证明后，调用方仍依赖旧接口。

**处理**：实现证明，补充调用方所需的接口，再更新调用方并重新审查。

**结果**：新的审查接受了修复后的定理和下游迁移。

[案例与审查时间线](examples/case-studies/thm_14_8/) · [完整证明](ProbabilityTheory/chapter_14/thm_14_8.lean)

第二例的简短前后文件是**简化的接口演示**，完整数学证明见单独链接。八个案例均经过选择，**不代表准确率、成本或生产率评测结果**。

![真实案例对照：代码可编译，补齐条件后仍需迁移调用方，最终通过新审查](docs/images/def85-review.svg)

*图据[第一例的审查时间线](examples/case-studies/def_8_5/review-timeline.json)整理，代码行摘自其公开快照。*

## 技术材料与进一步阅读

流程先检查能否编译，再由只读的语义审查角色核对是否符合原文含义；只有审查对应的代码和依赖仍然有效，才接受修改。按当前[审查契约](docs/phase2/agent_review_contract.md)，修复循环中的审查由未参与该次编写的独立子代理或已配置的审查运行器执行，并记录 `reviewer_independence`。这里的"独立"指工作流角色隔离，不等于人工审查，也不必然是不同模型；契约是当前规则，不追溯说明每条历史记录。模型辅助审查提供证据，不能保证数学判断绝对正确。

- [系统架构](docs/architecture.md)与[工作流](docs/phase2/workflow.md)
- [运行完整流程](docs/workflow_demo.md)
- [审查身份试验](docs/review_basis_pilot.md)与[前瞻比较方案](docs/review_comparison_pilot.md)
- [安装与验证命令](docs/getting_started.zh-CN.md)
- [八个案例及复现命令](examples/case-studies/)
- [审查标准](docs/phase2/review_criteria.md)与[状态规则](docs/phase2/status_contract.md)
- [研究背景、相关工作与限制](docs/project_notes.md)
- [仓库范围与公开历史说明](docs/repository_scope.md)
- [贡献指南](CONTRIBUTING.md) · [安全策略](SECURITY.md) · [MIT 许可证](LICENSE)

项目旧名为 **ToyApollo**，历史证据与格式标识保留旧名。当前命令为 `formalize`，
程序位于 `src/formalization_engine/`，正文位于 `ProbabilityTheory/`。
简历和引用请统一使用 **ProbabilityTheoryFormalization**。

