# P0 Skill 范围与原生任务分离记录 — 2026-10-25

> **决议分层：用户已明确 Skill P0 的产品范围（A+B 必做、C 可选、D 独立）；原生 PM 工作模式/既有任务重分类及独立 Reviewer 签署**仍未完成，不得把此文件当成已签字的原生 `ProjectManagerAgent` 决议。**P0 整体 BLOCKED。**

## 一、来源及原有冲突（RV06-01）

用户提交的《R05 独立 Review（修订版）——Skill 编写与集成项目》和其后 GitHub [R06 独立预审](reviews/R06-INDEPENDENT-REVIEW-20261024.md) 均明确：此仓库交付的是**Skill 自身的规则、集成代码及验证能力**，不是一套生产订单支付软件。原 [Issue #1](https://github.com/szlwin/common-develop-dec-integration/issues/1) 早期合同要求把业务 Java/TDD/开发/测试/归档全链条完成作为 P0，R06 Owner 文档又把完整业务 E2E 改为可选，两者需要明确修订边界。

原始 Native Task `FEATURE-DESC-DAE4FAB5F9F4` 的 `request_intake.json` 仍是 `NEW_REQUIREMENT/STANDARD_FEATURE_FLOW`，十阶段、`skippedPhases=[]`、九项影响 `UNKNOWN`。原任务 R06 `requirement_confirmation` Artifact **PUBLISHED**，六项 Reviewer Assertions **PENDING**，无 Finalized Outcome。**原任务原始 ZIP 与历史事件必须保持原样，不删、不覆盖、不将默认 Stage Gate 降级。**

## 二、产品 P0 目标与可追溯矩阵

| 等级 | 项目 | 对 P0 的要求 | 可接受证据 | 当前状态 |
|---|---|---|---|---|
| **A 必做** | Skill 内容、`SKILL.md`、Agent/固定 Provider 路由、版本来源、权限、原生真实 StageOutcome/Review/Evidence Gate、Artifact lineage、失败阻断及文档 | 必须有通过适用原生规则的证据，禁止用自制 JSON 替代 Reviewer | Skill 规范审查、原生 `validate`/`task-events`、经独立 Reviewer 批准的当前 design/PASSED 正向 Gate、反例回归 | 部分已实现；**独立正向 Gate 未验证** |
| **B 必做** | 固定 `dec-design`、`dec-java-lite`、`dec-implementation`；10 个 canonical YAML 的 SHA；Demo XML/HTML/Java、Binding/JUnit、Python 单元、Maven、负向注入/恢复 | 真实运行、可复算源码与产物、测试失败 fail-closed；Demo Java 是 Skill 能力夹具 | 固定源码 CI、34 Python tests、独立上游 native/DEC tests、实际 Java Maven/JUnit、Artifact Manifest/日志，明确 Fixture 属性 | 固定 Fixture 与上游回归已成功；不代表 A 原生正向审批 |
| **C 可选** | 用 Skill 交付一轮完整订单支付业务软件 Standard E2E，包括 RED/TDDReview/Development/Code Review/Testing/Completion Verification/Archive | 只有激活 C 时才单独验收；**该 Standard 任务一旦开始不能跳过实际原生 Gate** | [独立 Issue #2](https://github.com/szlwin/common-develop-dec-integration/issues/2)、正式 StageOutcome/Case/TDD/Review/Evidence/Archive | **不再作为 Skill P0 的默认必做项**，历史 R06 不自动完成 |
| **D 独立** | Demo Product Release | 与 Skill P0 通过无自动关系 | Product Release 真实外部支付/DB/SMS、所有 Design ID READY | NOT READY（4/111 PLANNED，使用替身） |

**原生工作流与项目产品验收是两个维度**：本次分离不降低任何实际选择 `STANDARD_FEATURE_FLOW` 的 Task 的强制阶段。如果新 Skill A+B 任务采用 Standard，阶段用于开发、Review 和测试 **Skill/适配器本身**，而非要求人为编造一套订单支付业务 RED。若某真实 Task 原生契约对其适用 TDD 子门禁，必须真实满足或由授权 PM 使用官方机制变更，不能在 Artifact 中写“可选 C”就伪造 PASS。

## 三、原生任务分离的真实动作

- **历史任务（保持原样）**：`FEATURE-DESC-DAE4FAB5F9F4`，R06/PUBLISHED/PENDING。R06 原始 ZIP SHA-256 为 `695a4dc306b0cf0bd694264b32fc8f1ed558f6157735a64b3913bd2c86f737ae`。
- **新 Skill A+B 任务（隔离新 DocRoot）**：`FEATURE-DESC-2AD10B7DBDCA`，由固定 Gitee `common-develop-opt` 的真实 `wk.py start -g ProjectManagerAgent --apply` 创建，`NEW_REQUIREMENT/STANDARD_FEATURE_FLOW`，入口 `requirement_confirmation`；**十个原生阶段未删除**。`long_task validate` 返回 `PASSED`（结构），`wk begin --apply` 返回 `BLOCKED / EXECUTION_REQUIRED / ARTIFACT_NOT_PUBLISHED`，需要 `RequirementConfirmationAgent` 真实开始执行。
- 新 Intake 已明确 `apiContract/permission/workflow/persistence/dependency=CHANGED`、`externalSideEffect/migration=NONE`（隔离 Demo 边界），`businessLogic/dataModel=UNKNOWN`；不是九项都已审批或通过 Risk Scan。
- 新任务使用**独立 DocRoot**，未采用对既有 R06 状态做 `work_mode apply` 或 `request_intake reclassify` 的捷径。逐字节比较原始 R06 ZIP 的所有历史 Task 文件，均保持相同；没有删除、覆盖、reset 原本的历史事件。
- CLI 的 `-g ProjectManagerAgent` 是工具公开的 Agent 参数，**不是外部身份认证或独立 PM 签字**。新建任务的事实已经发生，但后续 PM 必须确认新任务范围/影响、原 Standard 历史任务如何处置及 Review 责任，才可判定 RV06-01 **正式 Closed**。

交接：`p0-skill-ab-pm-task-split-20261025.zip`（用户会话提供），19/19 包内 SHA-256 通过；包含新 DocRoot 的原生任务/Intake/账本、CLI 结果、工作模式与**未经更改的原始 R06 ZIP**。该包是原生 Task 创建证据，**不是需求 Attempt PASSED/Review/StageOutcome**。

## 四、目前的治理决议与后续硬门禁

| 责任 | 最晚时点 | 未满足则阻断 |
|---|---|---|
| 项目验收 Owner | 已执行产品层范围澄清；本矩阵覆盖当前 P0 新目标，Issue #1 同步 | 不得拿旧完整业务 E2E 清单错误地验收 Skill P0 |
| 授权 ProjectManagerAgent | 新 Skill 任务需求确认正式发布/签署前 | 审查新 Skill A+B Task/Intake 和现有 Standard R06 的关系，决定历史任务仅用于可选 C 或保留原职责；需要的变更必须走原生官方命令 |
| 独立 RequirementAnalysisAgent | 新 Skill A+B Task requirement_confirmation `finalize-phase` 前 | 必须对该 Task 当前已发布 Revision 和 AC 单独 Review；目前没有发布 Artifact，不可审假对象 |
| RequirementAnalysisAgent / PM | `requirement_analysis`→Design 之前 | canonical `requirement.md` Trace 真正同步并处置历史 R01 Trace，不能使用旧 SHA 放行 |
| Design Reviewer / Integration | A 正向 Gate 消费前 | 真正 Design/PASSED、原生 Event/Evidence、固定 DEC tree digest、未失效事件链，`--demo-fixture-gate` 不足 |
| Develop/Test/Risk Owner | 对各真实 Task 触发对应阶段时 | 原生适用 TDD、单元、Maven/JUnit、负向回归、Risk Scan 必须真实执行，不得跳过或伪造 |
| Product Release Owner | 任何宣称业务产品 READY 之前 | 四个 PLANNED/替身外部系统仍导致 NOT READY |

**未解除的事实**：正式 Reviewer 尚未签署、旧 R06 Intake 九项 UNKNOWN、Risk NOT_SCANNED、真实 native-positive Gate 未完成。不能将上述项目范围澄清和新任务初始化等同于独立原生审批。**Issue #1 与 Issue #2 按各自职责开放，P0 BLOCKED。**
