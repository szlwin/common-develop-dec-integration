# P0 RV07 四步执行与新 Skill A+B Owner R01 交接报告（2026-10-25）

> 执行结论：**已形成项目级范围决定、原生 Skill A+B 任务 R01 Owner/PUBLISHED、双设计源机械预检与 fail-closed、历史文档修正和 GitHub 提交；真正授权的 PM 签署、隔离 RequirementAnalysisAgent Review、两个 Design/PASSED、v2 正向消费仍未完成。P0 BLOCKED。**
> 这是 Owner 执行记录，不是独立原生 Reviewer 文档，不得拿它替代 manual_review submit 或 finalize-phase。

## 第一步：PM 目标、影响及新旧 Task

- 用户明确产品范围：**A Skill 规范/路由/原生 Gate；B 三固定 Provider Demo/Java/JUnit/Binding/负向回归**均为 Skill P0 必做；**C 完整订单支付软件 Standard E2E 可选 Issue #2**；**D 产品发布独立**。
- 旧原生任务 FEATURE-DESC-DAE4FAB5F9F4：历史 R06 Requirement Artifact PUBLISHED，六项 REVIEW PENDING，无 finalized event。原 R06 ZIP 哈希为 695a4dc306b0cf0bd694264b32fc8f1ed558f6157735a64b3913bd2c86f737ae，本轮没有覆盖原历史事实。
- 新独立 DocRoot Skill Task FEATURE-DESC-2AD10B7DBDCA：初始 Intake 为 NEW_REQUIREMENT / STANDARD_FEATURE_FLOW，保留十阶段；受影响 apiContract/permission/workflow/persistence/dependency 为 CHANGED，businessLogic/dataModel 为 UNKNOWN，externalSideEffect/migration 为 NONE。
- 新 Task 的 PM 范围/工作模式意见记录在原生 DocRoot 的 PM_SCOPE_DECISION.md 中，作为只读不可变 EVD-000002 登记。**该文件明确标注 NATIVE_PM_AUTHORIZATION_PENDING**：-g ProjectManagerAgent 只是 CLI 的公开角色选择，不能证明真正身份认证，也不能擅自写成 PM 已正式签署或所有影响字段 CLOSED。
- 新 Task 当前 Standard 适用于 Skill 本体的开发、代码、测试和 Review；没有通过改成 -min、-ws 或改写旧 request_intake.json 绕开实际强制阶段。

**第一步状态：产品范围决议已落实、Task 数据已隔离；授权 PM 对历史任务归属和新 Intake 未决分类的正式签署仍 PENDING。RV07-01 仅部分关闭。**

## 第二步：RV07-03 双设计来源

原来的正向 Gate v1 假定 native design.output_revision = sha256(DEC YAML tree)。新 Skill Task 的设计对象是 Skill 架构/路由，不等于订单支付 YAML。现在：

1. 新建 [双来源契约](../dual-source-design-binding.md)：A 为 Skill 设计字节/独立原生 Skill design StageOutcome；B 为固定 DEC 十 YAML 内容字节/另一个独立原生 DEC design StageOutcome。
2. 新增 scripts/check_dual_source_binding.py：两个不同 Task、两份 Source SHA/Revision、两组 native validate + task-events、真实最新 finalized design/PASSED、Scope Evidence ID/SNAPSHOT、当前 Requirement Trace。调用命令的 DEC checkout 必须为固定提交 4fb21242498746365c201fdf2a7fd8052f3a122a 且 canonical YAML 干净。
3. 新增 tests/test_dual_source_binding.py：双源缺失/Task 身份偷换/相同 Task/变更 YAML/变更 Skill/Revision 未内容绑定/缺原生 finalization/Scope Snapshot 非不可变或摘要错误，都必须拒绝。
4. 现有 scripts/native_gate.py 显式拒绝使用 **新 Skill A+B Task** 通过 DEC-only 单来源 v1 Gate；不放宽任何已存在的旧审核要求。真正 v2→DEC 正向消费尚未完成，需独立设计 Review 后另行验收。

**第二步状态：契约和机械 fail-closed 可测；两份真正设计原生审查和 v2 正向执行未完成，不可声称双设计已批准。**

## 第三步：修正历史文档

- docs/P0-native-design-review.md 与 docs/P0-native-task-handoff.md 开头明确标明「旧完整业务软件 E2E 合同已被当前 Skill A+B 范围覆盖」，指向 Issue #2；原历史正文和审计信息保留。
- docs/gate-contract.md 增补 v1 DEC-only 的合法适用边界与双来源要求，严禁 Skill 架构审核偷换 DEC YAML 审核。
- GitHub Issue #1 继续作为必做 A+B 跟踪，Issue #2 独立保留可选 C，四个 PLANNED Design ID 仍阻断产品发布 D。

**第三步状态：GitHub 文档修改已提交。**

## 第四步：新的原生 Skill A+B 需求 Owner Attempt / Artifact / Review 交接

在隔离 DocRoot 中使用固定版本 common-develop-opt 原生命令：

| 对象 | 实际值与状态 |
|---|---|
| Native Task | FEATURE-DESC-2AD10B7DBDCA / Standard |
| 正式文档 | version/V_P0/requirement/FEATURE-DESC-2AD10B7DBDCA/requirement.md |
| 需求 Revision | REQCONF-SKILL-AB-R01@sha256-615aa67b147be0093cf52159e61b883bc8c72defeeb6c998bc7ed84a2812f3eb |
| 当前 Owner Attempt | ATTEMPT-TASK-REQCONF-AB-001-I001-A001 / PASSED |
| 不可变 Evidence | EVD-000001 需求 Snapshot；EVD-000002 PM 待决范围说明 Snapshot；EVD-000003 真实命令校验结果 |
| StageOutcome | SO-FEATURE-DESC-2AD10B7DBDCA-REQUIREMENT_CONFIRMATION-I001 / **PUBLISHED，尚未 FINALIZED** |
| 官方 confirmation / analysis 文档校验 | 两级均 valid=true、errors=[]，6 AC、1 Trace、零占位符 |
| 原生 long_task validate | PASSED（结构） |
| 原生 wk next | REVIEW_REQUIRED，ISOLATED_REVIEW_SESSION_REQUIRED，ownerContextReuseAllowed=false |
| 当前六项 Review Assertion | AC-01～AC-06 均 PENDING |
| STAGE_OUTCOME_FINALIZED | 0 条 |

由于确认阶段要创建原生手工 Review Assertion，而正式 canonical Trace 同步属于后续 requirement_analysis，本次在新任务的初始 Task Plan 中建立了**显式 PENDING 的六项确认审核映射** TR-REQCONF-SKILL-AB-001。此记录是新的规划事实，不是已通过的 requirement_analysis Trace 或外部 Reviewer 验证；正式分析后必须用原生 sync-traceability 完整同步。

本会话曾承担 Owner，因此不符合独立 Reviewer 会话要求：**没有执行 manual_review submit、没有把任何 Assertion 改为 VERIFIED、没有执行 finalize-phase**。

## 完整任务交接与完整性

受信任独立交接 ZIP：p0-skill-ab-r01-owner-and-dual-source-handoff-20261025.zip，SHA-256 为 **33903e7638cd5400dbe866c18404177f738d2d33b1565c23e6cff06510f32653**。包含当前新 Task/DocRoot、PM 待决文件、原生 Evidence Registry/Objects、8 条 Task Event、10 份官方 CLI 结果、原 R06 ZIP 不可变来源、固定 common-develop-opt 原版 ZIP，以及原生 Owner 复现脚本。**39/39 Manifest SHA-256 匹配，ZIP CRC 通过**。重新解压并重跑官方 long_task validate = PASSED、wk next = REVIEW_REQUIRED。

这个二进制交接包在当前对话下载，**没有将原生任务历史、用户附件和可能含本机路径的 ZIP 公开上传到 GitHub**。GitHub 提交的是代码、规范、验收/审核索引与核验事实。独立 Reviewer 必须先获取真实任务原件，不能仅凭本报告表格签署。

## 下一步剩余门禁

1. 真正获授权的 ProjectManagerAgent 对新 Task、历史 R06、影响 UNKNOWN、工作模式/归属作合法正式决议。
2. 真正隔离的 RequirementAnalysisAgent 独立审核本次新 Task R01 的六项 AC；不通过则官方返修、通过后才能合法 finalize-phase。
3. 在 requirement_analysis 正式同步 Trace；各设计来源完成互相独立的 Design Review/StageOutcome 和绑定 Snapshot。
4. 由受审的 v2 消费实现运行真实 native-positive → 三 Provider、Java/JUnit/Binding、独立系统测试；新 Skill Standard Task 仍按真实需要完成其代码/测试/归档阶段。
5. C 可选软件 E2E 不作为 A+B 默认通过项，D 产品发布与四个 PLANNED 状态独立。

**P0：BLOCKED / PARTIALLY IMPLEMENTED。**
