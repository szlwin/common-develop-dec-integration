# P0 R02 — RequirementAnalysisAgent 内容预审（2026-10-23）

> **内容判断：NEEDS_CHANGES；正式原生 Review：NOT SUBMITTED / PENDING。**
>
> 当前 ChatGPT 会话曾执行 RequirementConfirmationAgent Owner 工作，与原生 `ISOLATED_REVIEW_SESSION_REQUIRED` / `ownerContextReuseAllowed=false` 不兼容。本报告是根据真实文件和原生只读 CLI 的**内容复核**，不伪称已经以隔离的 RequirementAnalysisAgent 身份调用 `manual_review.py submit`，也没有更新任何 `acceptance.json`、`task_events.jsonl` 或 StageOutcome。

## 输入与可核验事实

- Task `FEATURE-DESC-DAE4FAB5F9F4`，阶段 `requirement_confirmation`，Iteration 002；发布修订 `REQCONF-P0-R02@sha256-b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2`。
- 当前已发布需求 `native-doc/version/V_P0/requirement/FEATURE-DESC-DAE4FAB5F9F4/requirement_confirmation.md`，SHA-256 `b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2`，与 `EVD-000003` 不可变快照一致。`EVD-000004` 是 Owner 验证命令 Evidence，不是 Reviewer 签署。
- 原生 ZIP SHA256SUMS 与固定 Gitee Skill ZIP 的 `FILE_MANIFEST.sha256` 完整校验。ZIP 缺少 Git object，文件级校验本身不能证明固定 commit 的 Git 身份。
- 官方 `long_task.py validate`：`PASSED`（原生结构）；`wk.py next`：`REVIEW_REQUIRED`、`RequirementAnalysisAgent`、`ISOLATED_REVIEW_SESSION_REQUIRED`；当前六条 Manual Review Assertions 均 `PENDING`。
- **新增真实复现**：对**已发布 R02 原文**运行官方 `requirement_doc.py validate --stage confirmation` 返回 `valid=false`，缺 `## 1/2/3/4/12/14` 标准章节、`### 1.1 阅读摘要` 和九项基础元数据。
- 另一个候选 `candidate/requirement.md`（SHA-256 `1c733bc8a94758e3e0f5d00128ab50e9b00f3251553d71004dddeb040b4e1240`）在官方 confirmation 和 analysis 格式校验中均 `valid=true, errors=[]`，但**未通过原生 Task/Attempt/Evidence/发布/独立 Review 正式纳入当前任务**。

## 原生 Review profile（语义标准）判断

依据固定 Skill `assets/review/review-contract.json` 的 `requirement_confirmation:RequirementAnalysisAgent`，Review 需覆盖 RC-REQ-001～005：

| 标准 | 内容判断 | 说明 |
|---|---|---|
| RC-REQ-001 目标与对象明确 | 满足 | 现状、目标、固定三 Provider 均有描述 |
| RC-REQ-002 范围边界明确 | 基本满足 | 禁止动态 SPI 与生产副作用；但 Intake 九项影响全是 UNKNOWN |
| RC-REQ-003 验收可观察 | 部分满足 | 六项 AC 有可观察目标，Artifact 消费时序/TDD 边界还不够确定 |
| RC-REQ-004 失败与禁止副作用 | 满足 | stale/reopen、缺审批和生产凭据等有 fail-closed |
| RC-REQ-005 关键决策已闭合 | **未满足** | 当前规范文档未正式发布；候选仍保留阻塞决策，影响分类未进入原生 Intake |

## 六项 AC 的逐项参考判断（不是已提交审核结果）

| AC | 内容参考判断 | 原因 |
|---|---|---|
| AC-01 | **NO** | 当前 R02 缺正式 canonical `requirement.md`，Task Plan 只允许旧文档 |
| AC-02 | YES（仅范围） | Tree SHA、来源绑定、失效规则明确；Design YAML 原文/审批仍待后续核验 |
| AC-03 | YES（仅范围） | 三 Provider、Java、Binding、JUnit 和可核验日志要求明确 |
| AC-04 | **NO** | Stage Owner/Reviewer、Java 生成/RED/Development 真实前后序与每类 Artifact 的精确归属尚不充分 |
| AC-05 | YES（仅范围） | 未审批/过期/重开/回归失败的拒绝条件明确 |
| AC-06 | YES（仅范围） | 4 个 PLANNED/111 和支付、MongoDB、SMS 替身及生产边界明确 |

表中 YES 仅针对原生 `MRQ-SCOPE` 的职责/范围/边界；**不表示功能已实现、AC 已 VERIFIED、Design StageOutcome PASSED 或可生产发布**。

## 返修发现与必要动作

**CR-01（阻断）— 已发布 R02 非标准需求文档。** 正式文档仍是 `requirement_confirmation.md`，官方确认阶段格式验证失败。合法 Owner 应通过原生 Task Plan/Amendment/Reopen 正式纳入 canonical `requirement.md`、重新产生内容绑定的 Evidence/Revision；绝不可事后将未发布候选当作 R02 已审批字节。

**CR-02（高）— Task Plan 版本与路径。** `TASK-REQCONF-P0-001.iteration_id` 仍为 Iteration 001，`allowed_files` 指向旧文件，`validation_commands` 使用只能在原 cwd 下成立的 `../native-doc`。必须经原生机制确认/修改计划，实际重跑可移植验证命令，保留旧事件。

**CR-03（高）— Artifact 与 TDD 时序。** 第 3 节有 `原生 owner` 模糊责任定义，并把“生成的 Java”列为 development 输入，同时要求 TDD RED 在实现前；需要明确代码生成时点、参考生成产物 vs. 正式实现、PRE_IMPLEMENTATION 审核、Case/Revision/Evidence 的确切顺序和失败关闭。

**CR-04（中）— Intake/风险不一致。** `request_intake.json.impactAssessment` 九项均为 UNKNOWN，而 R02 已承认跨模块、授权、持久化及供应链影响。依法适用原生风险/分类更新流程；`risk.json=NOT_SCANNED` 应在原生支持阶段真实扫描或留存正式不适用理由，不能伪报通过。

**CR-05（中）— 文本状态/阻断决策。** 已发布 R02 第 8 节仍写“需要新 Attempt/Evidence/publish”，而 Iteration 002 的 Owner Attempt/EVD-000003/004/PUBLISHED 已发生；候选第 12 节仍有“是否阻塞=是”的待决事项。后续正式新版本应准确记录已完成事实，关闭决定或保持显式 BLOCKED。

**CR-06（后续 Design Gate 阻断，不单独否决确认内容）— 旧 Trace。** `TR-P0-REQCONF-001.requirement_source_digest` 仍指 R01，真实 R02 是新摘要。固定 Skill 将 `requirement_doc.py sync-traceability` 安排在 `requirement_analysis`；必须在合法阶段同步 canonical Trace 并处置旧记录，Design→DEC 之前 fail-closed，不允许手工重写历史。

**CR-07（原生审批阻断）— 真正隔离 Reviewer 未执行。** 六项 Assertion 仍 PENDING。后续必须在**另一个真正隔离且获授权的 Reviewer 上下文**独立决定、提交真实 Review，再由有权 Agent `finalize-phase`。本报告不能代替上述操作。

## 返修后允许的路径

正式返修 canonical 需求/Task Plan → 创建真实新 Owner Attempt/Evidence/发布 → 独立 RequirementAnalysisAgent 内容 Review → 原生 finalize → requirement_analysis 正式业务流程/Trace 同步与旧项处置 → business_model/design 完整审批 → DEC 正向消费 → TDD、开发、代码审查、测试、Completion Verification/Archive。

**P0 总体：BLOCKED / PARTIALLY IMPLEMENTED，Issue #1 保持 OPEN。**
