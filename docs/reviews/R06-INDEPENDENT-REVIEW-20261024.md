# P0 R06 Skill 范围修订——独立审查报告（证据边界版）

- 审查日期：2026-10-24
- 审查基线：`szlwin/common-develop-dec-integration` main `c983bafd856152b67689a0ef3486cde500f363ee`
- 目标任务：`FEATURE-DESC-DAE4FAB5F9F4`，`requirement_confirmation` Iteration 006
- Owner 声明的目标 Revision：`REQCONF-P0-R06@sha256-8d7ad856379aeeb320bd0d6edeb482bab996e2552cdcb5ea6653918a23bf9046`
- 审查性质：**独立仓库与验收契约预审**，不属于原生 `RequirementAnalysisAgent` 已授权独立会话签署
- 综合建议：**NEEDS_CHANGES_FOR_APPROVAL / EVIDENCE_NOT_FULLY_VERIFIED**；原生正式 Review 继续 `PENDING`，P0 为 `BLOCKED`

## 1. 审查范围及证据等级

本次独立读取 GitHub 最新 HEAD 的 R06 Owner 文档、完整验收台账、Issue #1、CI 配置以及 GitHub Actions jobs/logs；并直接对可读取的 R05 源 ZIP 进行基线字节检查：R05 canonical `requirement.md` SHA-256 为 `10aed9de57fbc090ae67eb354fa613c55bd6d05c4906ab1ddf0e3524a7b4418d`，事件账本 48 条，旧 Intake 为 `NEW_REQUIREMENT` / `STANDARD_FEATURE_FLOW` 且 9 个影响字段全部 UNKNOWN，Risk 为 NOT_SCANNED。

R06 Owner 报告位于：
https://github.com/szlwin/common-develop-dec-integration/blob/main/docs/reviews/P0-R06-SKILL-SCOPE-OWNER-REMEDIATION-20261024.md

**重要证据限制**：文件库中发现 `p0-requirement-r06-skill-scope-20261024.zip`，但原始二进制的授权物化失败；文本读取也没有得到 ZIP 内容。R06 ZIP 并未提交公共仓库。因此本次**没有独立重新计算** R06 需求 SHA、51/51 清单、EVD-000011/012、58 条新事件前缀、六项 R06 Assertions 或重放原生 `wk next`。这些事实目前仅有 Owner 报告陈述，不能标为“已由本次独立验证通过”。

## 2. 修订方向审查

R06 报告描述将 P0 分为：
- **A 必须**：Skill 规范、路由、权限、原生 Gate 接口与版本约束；
- **B 必须**：三个固定 Provider 的真实集成、Java 编译/JUnit、Binding、Artifact lineage、负向注入、回归；
- **C 可选**：完整业务软件 Standard E2E，若选择执行不得绕开正式原生 TDD/Review 门禁；
- **D 独立判断**：订单支付 Demo 的产品发布准备度。

这项区分**在需求方向上正确**：编写或集成 Skill 不需要把业务软件 TDD RED 和 `TDDReviewAgent` 作为一切 Provider 测试的强制前置条件；但不得取消适用的脚本单测、真实集成、Java/JUnit 及证据链验证。对真正选择了 Standard 软件开发的任务，也不能口头豁免已有原生 Gate。

## 3. 独立 Findings

### RV06-01 / HIGH：工作模式与 P0 范围合同尚未统一（审批阻断）

R06 文档承认既有 `request_intake.json` 为 `STANDARD_FEATURE_FLOW`，`requiredPhases` 包含十个原生阶段、`skippedPhases=[]`，九类影响 UNKNOWN。**原 R05 源 ZIP 可独立证明这一历史 Intake 状态**；R06 版本称未合法更改。与此同时 R06 把完整软件 E2E 降为 C 可选。现有 `docs/P0-acceptance.md` 历史合同、Issue #1 的原始验收任务以及 `docs/native-positive-runbook.md` 仍写有将 TDD、Development、Code Review、Testing、Completion Verification、Archive 证据正式回流 common-develop-opt 的强制完整 P0 目标。

必须由有权 PM/验收 Owner 采用原生支持的路径明确：① 当前 Standard Task 继续完成其强制阶段；或 ② 依法重定模式/拆分成 Skill A+B 任务与可选软件 E2E 任务，并同步 Task Plan、Intake、验收基线和 Issue。不能只在 requirement.md 新文字中说 C 可选，而让有效执行合同保持原样。

### RV06-02 / HIGH：R06 原生证据未能独立核验（完整审查阻断）

Owner 陈述 51/51 文件哈希、58 个事件、R05 原始前缀、R06 Rev SHA、EVD-000011/012、Attempt PASSED 和六项 PENDING；由于完整 ZIP 字节不可访问，本轮不能确认这些声明与原生对象实际一致。必须取得可读取的原始 R06 ZIP 才能给 R06 当前 Revision 做逐句/逐 AC 的最终内容审查。

### RV06-03 / MEDIUM：Skill 验收规范与现有 CI 证明范围不同

GitHub latest CI `p0.yml` 仍以 `--demo-fixture-gate` 运行固定 Provider 链，报 `VERIFIED_WITH_FIXTURE`、`nativeP0Approval=BLOCKED`、`productReleaseReady=false`；负向原生 Gate 通过，尚无真实 R06 Reviewer/PASSED Design Gate 正向联调。应把 A 的路由/原生身份审批、B 的 Provider/JUnit/血缘、C 的软件 E2E 分开出具独立验收矩阵，避免把 B Fixture 绿色写作 A 原生正式通过。

### RV06-04 / MEDIUM：Trace/Risk 等后续事项必须落地、不能提前伪通过

根据 R06 Owner 声明，历史 R01 Trace 尚未合法同步，需在 `requirement_analysis` 使用 canonical `requirement.md` 按官方规则同步和处置旧引用；Risk 为 NOT_SCANNED，固定原生 Skill 需有相应开发 Revision 才能扫描。确认阶段可记录延期，但必须形成清晰的责任 Agent、期限、下游硬 Gate 和 Review 判据。

### RV06-05 / LOW：固定 Gitee Commit 的 CI pin 加固——正面发现

`1d7ec072` / `c983bafd` 将四条以上关键 CI 工作流从浅克隆后直接要求 main HEAD=旧 SHA，调整为 main 已前进时拉取并 checkout **原审计 SHA** `b26715f6779b373b4f840b519ba9725fed5d789a`，且校验实际 Git commit。GitHub Jobs 已成功执行该流程。这解决了旧 Gitee main 移动造成的非确定性失败，但**不能代替 R06 task ZIP 的独立字节核验**。

## 4. 六项 AC 当前审查矩阵（不等于原生官方 Reviewer 判定）

| AC | R06 Owner 描述的修订重点 | 本次独立状态 |
|---|---|---|
| AC-01 | Skill 研发集成目标、范围和工作流角色 | 方向正确；工作模式合同未决；原文未复核 |
| AC-02 | 设计 SHA/Revision、审批及失效 | 旧规则存在；R06 是否逐字保留未核实 |
| AC-03 | 三 Provider 真实集成、Java/JUnit/Binding/Evidence | 最新 Fixture CI 支持部分验证；不证明 R06 Revision 已获批准 |
| AC-04 | Skill 集成测试不用强制业务 RED/TDD；软件 Standard E2E 单列可选 | 纠偏方向合理；需先合法处理 Standard 当前任务的 Gate 冲突 |
| AC-05 | Fail-closed、审计、失效和恢复 | 原生负向 CI 通过；R06 当前原文未核实 |
| AC-06 | Skill P0 / 软件 E2E / 产品发布三层边界 | 方向正确；应同步正式验收合同 |

**六项 R06 MANUAL_REVIEW 据 Owner 报告仍全部 PENDING；本次没有提交、修改或标记任何官方 Assertion。**

## 5. GitHub CI 核验

- HEAD：`c983bafd856152b67689a0ef3486cde500f363ee`；GitHub Issue #1 仍 OPEN。
- 固定 Provider CI：https://github.com/szlwin/common-develop-dec-integration/actions/runs/40104814758 （通过；34 项集成器单测；Fixture Integration PASSED，原生批准 BLOCKED）。
- Native 负向 Gate：https://github.com/szlwin/common-develop-dec-integration/actions/runs/40104814788 （通过；未批准设计正确拒绝）。
- 独立上游回归：https://github.com/szlwin/common-develop-dec-integration/actions/runs/40104814719 （360 native、80 dec-design、24 dec-implementation 测试通过，Maven Reactor BUILD SUCCESS）。
- 真实 kickoff：https://github.com/szlwin/common-develop-dec-integration/actions/runs/40104814891 （成功创建**未审批**的新原生任务；并非 R06 独立 Review）。

这些 CI 只证明它们实际运行的任务，不等于 R06 的原生 Owner Evidence 和 Reviewer 签署均已重验。

## 6. 正式结论与下一步

**内容方向判断**：R06 解决“Skill 项目必须先业务 RED/TDDReview”的概念性问题，技术方向合理。

**独立 R06 完整内容 Review**：因 R06 真实原文和 Evidence 未能访问，结论只能是 `EVIDENCE_NOT_FULLY_VERIFIED`，不能对 6 个 AC 签 PASS。

**验收/治理结论**：`NEEDS_CHANGES_FOR_APPROVAL`，核心是 P0 目标与原生 Standard Intake、正式验收台账/Issue 的边界尚未通过授权的修订流程统一；不能在原生规则没变时自行删减必需阶段。

**原生审批结论**：`PENDING`；按 Owner 报告，StageOutcome 仅 PUBLISHED、无 FINALIZED 事件，六个 MANUAL_REVIEW 全部 PENDING。P0 `BLOCKED / PARTIALLY IMPLEMENTED`。

推荐顺序：
1. PM 先签署当前 Standard Task 与 Skill-only A+B 验收关系、正式拆分/模式决定及 Issue/验收条款修订，不覆盖历史事件。
2. 将原始 R06 ZIP 以本次会话可读取的附件交付，验证 51 条清单、原文 SHA、EVD-000011/012、事件账本前缀和六项断言。
3. 在与 Owner 真正隔离且有权限的 `RequirementAnalysisAgent` 会话逐项提交原生 Review；通过后方可正式 `finalize-phase`。
4. 在后续合法阶段完成 canonical Trace 同步、Risk/Intake 治理、Design Gate 和 A+B 正向 Evidence；C 项软件 Standard E2E 由批准范围另行决定，D 项产品发布保持独立。

**任何内容预审意见都不是 `manual_review.py submit`、StageOutcome FINALIZED 或设计批准。**
