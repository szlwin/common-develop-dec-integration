# P0 Requirement Confirmation — 原 Owner 返修执行记录（R02）

> **Status: OWNER REWORK COMPLETE / ARTIFACT PUBLISHED / INDEPENDENT REVIEW PENDING / P0 BLOCKED**  
> 原始独立内容审查：[2026-10-19 NEEDS_CHANGES](P0-REQUIREMENT-CONFIRMATION-INDEPENDENT-REVIEW-20261019.md)。这份返修报告是 Owner 对审查意见的回应，**不是** Reviewer 的通过结论，更不是 `manual_review.py submit` 或 `STAGE_OUTCOME_FINALIZED`。

## 返修依据与不可变追溯

- Native Task：`FEATURE-DESC-DAE4FAB5F9F4`，原生 Skill 为固定 Gitee 提交 `b26715f6779b373b4f840b519ba9725fed5d789a`。
- 通过官方 `long_task reopen-phase` 从 `requirement_confirmation` 开启 **Iteration 002**；原生返回 `invalidatedPhases` 覆盖后续全部正式阶段，旧 `SO-...-I001` 通过 `STAGE_OUTCOME_SUPERSEDED` 保留历史。
- R01 Revision：`REQCONF-P0-R01@sha256-130eb2a1a3d5b74f175755101737fe5b74a25e8fdee33665158af514a16a7db4`，仍可通过原来 `EVD-000001` 不可变快照追溯。
- R02 Revision：`REQCONF-P0-R02@sha256-b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2`，由真实新需求正文的 SHA-256 标识。
- Owner Attempt：`ATTEMPT-TASK-REQCONF-P0-001-I002-A001`，通过正式 `start-attempt`、`finish-attempt --auto-evidence` 并返回 **PASSED**。
- 新 Evidence：`EVD-000003` 为新需求正文 Snapshot，`EVD-000004` 为真实原生 `validate` 命令执行 Evidence。
- 官方 `publish-artifact` 返回 **PUBLISHED**，新 Outcome ID `SO-FEATURE-DESC-DAE4FAB5F9F4-REQUIREMENT_CONFIRMATION-I002`；`long_task validate` 返回 **PASSED**，但这**不等于阶段 finalized**。
- `wk next` 返回 `REVIEW_REQUIRED`；`requiredAgent=RequirementAnalysisAgent`；`executionContext=ISOLATED_REVIEW_SESSION_REQUIRED`；`ownerContextReuseAllowed=false`。六项针对 **R02** 的 Review Assertions 均为 PENDING。

## 审核意见逐项回应

| 原问题 | 已实施的 Owner 改动 | 复验结论 / 仍缺的条件 |
|---|---|---|
| **R-01** — 设计 SHA 与 Revision 绑定不明确 | R02 正式需求明确路径过滤、POSIX 相对路径的升序、UTF-8 名称加 NUL、每文件 SHA-256 **二进制**摘要拼接；固定 DEC commit、10 个 canonical YAML、拟定 `sha256:<tree digest>`、变化失效与原生拒绝时的正式替代审批规则 | **Owner 文档修复**。实际 Design Gate 按该格式完成原生 publish/Review 尚未证明，仍需后续实测 |
| **R-02** — Artifact→原生阶段的交接不完整 | 在 R02 正文建立十阶段（及归档）的输入 Revision、责任 Agent、DEC 五类 Artifact、Evidence、Case、Review、失败阻断表 | **Owner 文档修复**；下游阶段实际消费与归档仍需执行 |
| **R-03** — TDD 子门禁未明确 | 明确在 `test_design` 编排 Case，`TddAgent` 进行先 RED、`TDDReviewAgent` 在 `PRE_IMPLEMENTATION` 核对，`development` 执行 GREEN/REFACTOR，保留命令日志与 SHA | **Owner 文档修复**；实际子门禁和时间顺序需在正式研发中验证，不造 `tdd` canonical StageOutcome |
| **R-04** — 六项 AC 使用相同模板 | 在 R02 正式需求为 AC-01..AC-06 分别定义范围、后续证据、负向阻断；不批量 YES、不把 R01 PENDING 断言沿用 | **Owner 文档修复**；R02 新建的六份官方 Reviewer 表单仍均未作答 |
| **R-05** — Crosswalk 缺失、验证命令路径不可移植 | R02 将 AC/Artifact/Evidence crosswalk **纳入正式需求正文**；说明 R01 相对路径命令的历史 cwd，以及绝对 `--task-dir` 的独立验证方法。新 Owner 阶段实际重新产生 `EVD-000004` | **部分修复**：原始 Task Plan 中的相对路径验证命令仍作为历史保留，不能冒称已被原生版本化替换； Reviewer 可在隔离目录按绝对路径复验 |
| **R-06** — 风险尚未识别 | R02 增列业务/API/跨模块/授权与角色隔离、凭据泄露、Event/Evidence 持久化、外部替身及 reopen 风险和处理规则 | **部分修复**：`risk.json=NOT_SCANNED`；固定版本的 `risk_detect.py scan` 在 requirement 阶段因为无 development revision 而拒绝。此 Gate 不能假报 PASSED，应由后续合法 Risk 流程或 Reviewer 决定 |
| **R-07** — 真正独立 Reviewer 缺失 | 正式重开 R02 并新增六项 **PENDING** 断言；保留 Reviewer 角色/执行隔离约束 | **仍为阻断**：必须由隔离的 `RequirementAnalysisAgent` 根据新正文和真实 Evidence 审查并提交；未经审核不得 `finalize-phase` |

## 正式需求附件、审查材料与来源边界

当前具权威性的 R02 需求文件位于新交付的 **原生任务 ZIP**：

`native-doc/version/V_P0/requirement/FEATURE-DESC-DAE4FAB5F9F4/requirement_confirmation.md`

ZIP 同时包含本轮完整 `native-doc`、Append-only `task_events.jsonl`、Evidence Registry、34 个文件的 SHA 清单及六份新的空白 `review-forms/AC-01.md`～`AC-06.md`。该包由当前任务交付，不在公开 GitHub 存放敏感运行数据；应核验 SHA 和源码来源。固定原生源码版本沿用 [先前 pin 的 CI](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39177612656)。

关于 R-01 的**实际 10 个 YAML 字节**，应从固定 [DEC 源码提交](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/tree/4fb21242498746365c201fdf2a7fd8052f3a122a/demo/order-payment-yaml) 单独获取、逐文件比对，再进行 Design Review。只有 Digest 不足以完成真实设计语义审查。

## 必须保留的验收边界

**Owner Attempt PASSED ≠ Independent Review PASSED；Artifact PUBLISHED ≠ STAGE_OUTCOME_FINALIZED/PASSED；P0 Integration ≠ Product Release。**

Reviewer 必须在隔离且被授权的 `RequirementAnalysisAgent` 上下文，对 R02 当前字节、EVD-000003/000004 与 AC-01..AC-06 分别判断。Reviewer 如发现 R-05、R-06 剩余问题仍阻断，应执行正式 Issue/再次修订而不是通过。直到原生 `wk next` 合法进入 `finalize-phase` 且验证通过前，**P0 总体仍为 BLOCKED，Issue #1 仍 OPEN**。
