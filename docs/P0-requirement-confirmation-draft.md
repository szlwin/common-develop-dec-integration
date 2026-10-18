# P0 订单支付双 Skill 集成 — 需求确认工作稿

> **状态：DRAFT / NOT APPROVED**。本稿是 RequirementConfirmationAgent 阶段的输入，不是该 Agent 已通过的正式 Attempt，不是独立 RequirementAnalysisAgent Review 结论，也不允许直接用于解锁 DEC 的原生 Gate。

## 1. 背景、目标与事实基线

开发目标是在 **固定 Provider** 范围内证明 `common-develop-opt` 的真实需求、设计、审查及后续研发阶段能够与 `dec-design`、`dec-java-lite` 和 `dec-implementation` 协同。当前目标不是设计动态 Provider SPI。

- 固定 DEC 上游提交：`4fb21242498746365c201fdf2a7fd8052f3a122a`；订单支付 canonical YAML 位于 `demo/order-payment-yaml/`，共 10 份设计文件。
- 已验证的源目录 SHA-256：`a6961def87860d3cc1a7ecd1c67595b857b664b7077dc527207d9556610e1660`。该值描述固定 DEC 基线，不意味着有人已经批准这些字节。
- 固定 `common-develop-opt` Gitee 提交：`b26715f6779b373b4f840b519ba9725fed5d789a`。
- 正式原生任务：`FEATURE-DESC-DAE4FAB5F9F4`，版本 `V_P0`，原生 `wk start` 返回 CREATED。可审计事件账本在 [真实启动 CI](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39150138291)。
- 已通过的独立回归：[360 项 native、80 项 dec-design、24 项 dec-implementation 和 Java Maven](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39146485409)。
- 已通过的集成器负向校验及固定 DEC Demo CI **不能替代**真实获批 StageOutcome。
- Demo 已登记的 111 个 Design ID 中 107 VERIFIED、4 PLANNED。四项 PLANNED 是产品 Release 阻断项，而非可以任意改成 VERIFIED 的 P0 验收捷径。

## 2. 需求范围

**R-01 原生需求确认与来源**：在固定 Gitee Skill 的官方 Standard 工作流中，使用正式 RequirementConfirmationAgent Task/Attempt 形成需求事实、范围、验收条件、输入修订号和 Evidence。需要的阶段 Task ID 必须由原生正式规划机制创建；不得编辑 task_events.jsonl 伪造。

**R-02 独立 Review**：每一个需要 Review 的阶段必须由合约要求的独立 Reviewer 基于准确的当前 Artifact 内容与 Revision 给出结论，Evidence ID、问题关闭记录和 Review 关联必须能通过原生验证。仅设置 `review=PASSED` 的 Handoff JSON 不算独立 Review。

**R-03 内容绑定**：由 Design 阶段 PASSED Attempt 正式发布的 `output_revision` 必须绑定审核时实际展示的 canonical YAML 源目录字节。建议采用 `sha256:<DEC-YAML-tree-digest>`，但须先经 Gitee 原生 Attempt/Artifact 发布机制实际验证该格式合法。事后重写 JSON/账本无效。

**R-04 三 Provider 正向执行**：获批且未 reopen/invalidate 的原生 Design Gate 被 Integration 读取，经 Gitee 的 `validate` 和 `task-events` 双重核验后实际运行 DEC 设计校验/转换/HTML、Java 生成及 JUnit、Binding 与测试证据校验，全部留存可重复审核的原始日志、产物摘要与父级 lineage。

**R-05 下游双向交接**：把 DEC 生成的代码、Design ID/Binding 映射和 JUnit Evidence 作为真实下游输入提交至 `common-develop-opt` 的 `test_design`、`implementation_plan`、`development`、`code_review`、`testing`、`completion_verification` 正式阶段，完成上游规则要求的 Reviewer Gate。最终通过官方归档/收尾，确保从 Requirement→Review→Design→Code→Test 的链路可重放。

**R-06 独立性及失败关闭**：独立使用两套上游 Skill 不因 Integration 安装而改变；任意缺失 Evidence、历史已失效 Revision、产物内容不一致、未经授权 Agent、缺少独立 Review 均 fail closed。

**R-07 产品发布与 P0 验收分离**：产品 `release-readiness --require-ready` 的失败可以是演示场景已知、正确的阻断结果。即便 P0 fixed-provider 协同通过，Demo 的 4 个 PLANNED Design IDs、真实外部支付/数据库/短信替身风险仍需独立处理，不得自动宣称生产发布可用。

## 3. 可测试的验收条件

| ID | 验收条件 | 应有证据 |
|---|---|---|
| AC-01 | 原生需求确认正式 PASSED，且能证明独立 Review 覆盖当前修订 | 原生 `STAGE_OUTCOME_FINALIZED`、Review/Evidence、需求版本 |
| AC-02 | 原生 Design PASSED 且设计版号绑定当前 canonical YAML | 最新 Design StageOutcome、真实发布 Attempt、目录 SHA |
| AC-03 | DEC 三 Provider 与 JUnit 实际通过，代码/Binding 与已审批设计一致 | CLI 日志、JUnit XML、Artifact Manifest、SHA-256 |
| AC-04 | 真实下游阶段成功消费同一批 DEC 产物并经 Review | 各阶段原生 Artifact / StageOutcome、Evidence 输入引用 |
| AC-05 | 全部原生阶段及归档完整结束，独立 Skill 回归仍通过 | 原生最终状态与归档回执、独立 CI |
| AC-06 | 任意审批不存在或设计文件变动时被拒绝 | 原生及 Integration 负向拒绝日志 |
| AC-07 | P0 总结与 Product Release 状态分别报告 | `p0AcceptanceStatus` 和 `productReleaseReady` 独立字段 |

## 4. 已确认风险 / 待解决问题

**BLK-01（当前阻断）**：原生 `wk start` 建立的任务在 `wk begin` 阶段显示 `requirement_confirmation` 缺 Artifact；其机器上下文的 `stableIdIndex.taskIds=[]`。原生 `long_task.py task-context` 需要 `--task-id`，但不存在可供引用的阶段 Task ID。必须找到并使用受支持的阶段 Task 规划/创建途径，不能直接生成任意 ID。详见 [Requirement Context CI](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39177419367)。

**BLK-02（独立 Reviewer）**：目前没有独立的 RequirementAnalysisAgent、DesignReviewAgent 等角色完成真实内容检查的记录。此草稿不能冒充 Review。

**BLK-03（正向链）**：目前无获批的设计修订可供 `p0-native-positive.yml` 执行。

**DEC-01（范围决策）**：明确本轮固定 Demo 的完整生命周期是集成验收的一部分，但真实线上支付、MongoDB/SMS 外部平台、商业发布不是本次 P0 承诺范围；这些需要单独生产级验收。

## 5. 下一次原生执行

恢复 CI 中产生的完整 `native-doc`，只通过原生 CLI 查询当前 Task Plan、任务上下文和合约；完成实际需求确认文件后创建正式阶段 Task，再执行原生 `start-attempt`、收集 Evidence、执行原生 `finish-attempt`、`publish-artifact` 和独立 Review，直至 `finalize-phase` 真正通过。**每一操作都必须记录原生输出和对象 ID。**

**本文件是未审工作稿，不在验收表中标记任何原生阶段 PASSED。**
