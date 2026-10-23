# P0 Requirement Confirmation R04 — 正式 Owner 返修执行记录（2026-10-23）

> **原生结果：Owner Attempt PASSED / Requirement Artifact PUBLISHED / independent RequirementAnalysisAgent Review PENDING。P0 BLOCKED。** 本文不是独立 Reviewer 签字文件，不得用于执行 `finalize-phase`。

## 来源与正式新修订

根据 [2026-10-23 R02 内容 Review](P0-R02-REQUIREMENT-ANALYSIS-CONTENT-PRE-REVIEW-20261023.md) 的 CR-01～CR-07，恢复真实 R02 Task ZIP，使用固定 Gitee `common-develop-opt` 原生脚本执行并验证，不触及其他持久项目目录。

- Task：`FEATURE-DESC-DAE4FAB5F9F4`，阶段 `requirement_confirmation`。
- 正式 `reopen-phase` 曾创建 Iteration 003，在发布后发现章节顺序与发布前措辞问题，于是再次通过官方 `reopen-phase` 创建 **Iteration 004**；R01、R02、R03 事件和 Evidence 均保留，以 `STAGE_OUTCOME_SUPERSEDED` 等原生事件失效旧版本。
- 当前文件：`native-doc/version/V_P0/requirement/FEATURE-DESC-DAE4FAB5F9F4/requirement.md`（官方 canonical 14 节模板）。
- 当前 Revision：`REQCONF-P0-R04@sha256-73beddea3e0ec60120c12c027877bb5aebd1ec35af64159e2e6b0b45dae5a28d`；内容 SHA-256：`73beddea3e0ec60120c12c027877bb5aebd1ec35af64159e2e6b0b45dae5a28d`。
- Owner Attempt：`ATTEMPT-TASK-REQCONF-P0-001-I004-A001`，原生 `finish-attempt=PASSED`。
- Evidence `EVD-000007`（上述 canonical 原文不可变 SNAPSHOT）和 `EVD-000008`（真实原生验证命令日志）。
- StageOutcome `SO-FEATURE-DESC-DAE4FAB5F9F4-REQUIREMENT_CONFIRMATION-I004` 由原生 `publish-artifact` 返回 **PUBLISHED**，并非 FINALIZED/PASSED。
- 官方 `requirement_doc.py validate --stage confirmation`：`valid=true, errors=[]`；`--stage analysis`：`valid=true, errors=[]`，1 Feature、2 BR、1 CR、6 AC、1 Trace、1 Exception，0 未解决占位符。
- 官方 `long_task.py validate`：PASSED（仅结构与事件事实）；`wk.py next`：`REVIEW_REQUIRED`、`requiredAgent=RequirementAnalysisAgent`、`executionContext=ISOLATED_REVIEW_SESSION_REQUIRED`、`ownerContextReuseAllowed=false`。
- 六条 R04 当前 AC-01～AC-06 的 `MANUAL_REVIEW` Assertions 均 **PENDING**。整个事件账本当前 **没有任何 `STAGE_OUTCOME_FINALIZED`**；官方 R02 事件账本的原始 bytes 是当前账本完整前缀，旧 R02 需求原文同样没有被修改。

## Review 返修逐项处理

| Review 项目 | 原生实际动作 | 当前判定 |
|---|---|---|
| **CR-01** 规范需求 | 将原版 R02 非标准 `requirement_confirmation.md` 转换为正式 canonical `requirement.md`，并通过新 Owner Attempt + SNAPSHOT + Publish 形成正式 R04 Revision | **已修复，待独立 Reviewer 确认** |
| **CR-02** Task Plan | 原生 reopen 产生当前运行时 Iteration 004；静态 `task_plan.json` 的 `allowed_files` 增加 `requirement.md`，修订校验命令的交付布局并记录历史 Evidence 约束 | **部分修复**；静态计划的初始 `iteration_id=001` 不等于 Runtime 实际 Iteration 004，不能将静态初始身份硬改以冒充运行时状态；对任意工作区使用绝对 `--task-dir` |
| **CR-03** 代码/TDD 时序 | 正式 11.4 节明确 TestDesign Case、Implementation Plan、`TddAgent` RED、`TDDReviewAgent` PRE_IMPLEMENTATION、正式 Java/Binding 受控生成、GREEN/REFACTOR、Code Review/Testing 证据先后序；区分参考预览与真实实现 | **文档已修复，后续实际执行仍需验证** |
| **CR-04** Intake/风险 | 正式 11.5 节逐项明确 9 类影响；使用固定 Skill `request_intake.py classify` + `validate` 生成同 Task ID 的合法**候选** | **部分修复**：已有原生 `request_intake.json` 仍九项 UNKNOWN；固定 `reclassify` 仅支持 SIMPLE_OPTIMIZATION 升级，不支持既有 NEW_REQUIREMENT 同级写回；不得手工覆写有状态绑定的 Intake |
| **CR-05** 章节与状态 | R03 发布后因 11.4/11.5 错排到 13 后，依法重开 R04 并修正为 11→11.4→11.5→12→13→14，取消“尚须 publish”的过期表述；正式新修订真实发布 | **已修复** |
| **CR-06** 旧 Trace | 官方 `sync-traceability --dry-run` 已对 canonical 文档返回成功，并计划创建 `TR-REQ-P0-001-001`；历史 `TR-P0-REQCONF-001` 不被自动删除 | **待后续 `requirement_analysis` 正式同步与旧 Trace 处置**；不能在需求确认阶段伪造审批 |
| **CR-07** 独立 Review | 原生生成六条针对 R04 的新 Assertions 和未填写表单 | **阻断**：必须由隔离的 RequirementAnalysisAgent 审查提交，不能当前 Owner 代签 |

## 安全与剩余工作

- `risk.json.status=NOT_SCANNED`；原生 `risk_detect.py scan` 实际报错 `risk scan requires current development revision`。后续合法开发阶段扫描和正式风险审查仍是硬边界，不能将 R04 影响分类候选当作 Risk PASSED。
- 正式 RequirementAnalysisAgent Review 之前不得 `finalize-phase` 或 `advance-phase`。后续需正式需求分析、Trace 同步、业务模型/Design 独立 Review、真实 native-positive Gate、TDD/开发/代码 Review/系统测试、Completion Verification 与原生归档。
- R04 原生任务与官方 Evidence、Reviewer 表单、60 项 SHA256SUMS 和原始 R02/固定 Skill ZIP 以 **`p0-requirement-r04-owner-remediation-20261023.zip`** 交付于用户对话。公开 GitHub 本报告不是原生 Event/Review 账本，也不自动拥有这些数据。 Reviewer 应先验清单，再从当前 R04 字节独立执行审核。

**总状态：P0 BLOCKED / PARTIALLY IMPLEMENTED；Issue #1 必须 OPEN。**
