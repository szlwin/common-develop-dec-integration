# P0 Skill A+B R01 / 双来源 Gate —— 最新提交独立 Review（2026-10-25）

> **内容及代码审查建议：NEEDS_CHANGES_BEFORE_NATIVE_POSITIVE；原生正式 Reviewer：PENDING；P0：BLOCKED / PARTIALLY IMPLEMENTED。** 本文件是仓库代码、契约、CI 及 Owner 交接声明的独立复查，不是 common-develop-opt 授权的隔离 `RequirementAnalysisAgent` 签署，不调用 `manual_review.py submit`，不生成 `STAGE_OUTCOME_FINALIZED`，不替代实际设计批准。

## 1. 审查对象、来源与证据等级

- 仓库：`szlwin/common-develop-dec-integration`，本次 HEAD `9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd`（2026-10-25 04:36:17 UTC）。
- 对比上次已审查并提交的 `6717a1547c0a84afd3535445748647001c633cfa`：**10 个新增提交，14 个变动文件**。
- 审查范围：`docs/P0-skill-scope-governance-20261025.md`、`docs/dual-source-design-binding.md`、`docs/reviews/P0-SKILL-AB-R01-FOUR-STEP-EXECUTION-20261025.md`、`scripts/check_dual_source_binding.py`、`scripts/native_gate.py`、`scripts/p0_integration.py`、`tests/test_dual_source_binding.py`、`tests/test_native_gate.py`、CI、Issue #1/#2、验收台账。
- 代码/文档来自 GitHub 已提交的当前版本，属于**直接读取验证**。最新 CI job 日志为**实际可核验的自动化结果**。
- Owner 所称新 Skill Task `FEATURE-DESC-2AD10B7DBDCA` 的 `p0-skill-ab-r01-owner-and-dual-source-handoff-20261025.zip` **未公开进入本仓库**。Owner 陈述 ZIP SHA `33903e7638cd5400dbe866c18404177f738d2d33b1565c23e6cff06510f32653`、39/39 SHA、8 条原生 Event、`EVD-000001/002/003`、Owner Attempt PASSED 和 R01 PUBLISHED；**本次未取得该 ZIP 原始字节独立复算或重放 CLI**。本轮文件库的另一份 R01 Review Forms ZIP 同样未能授权物化原始字节。上述 Owner 数字不可当作本次直接验真结论。
- 此次没有在本地运行原生 Skill / DEC 端到端正向流。审查证据为源码、代码契约、GitHub CI 日志和 Owner 记录；没有改动上游 Task/Evidence。

## 2. 增量整改的有效进展

1. **Skill 产品 P0 范围正确**：A（Skill 规范、路由、权限、原生审批接口）和 B（三固定 Provider、真实 Java/JUnit、Binding、负向回归）必做；完整业务软件 Standard E2E C 在 [Issue #2](https://github.com/szlwin/common-develop-dec-integration/issues/2) 独立可选；D 产品发布独立。该分层**不豁免任何现存 Standard Task 自身真实强制 Gate**。
2. **两个设计审核对象被正式区分**：Skill 架构/Adapter 设计的 SHA，与固定 DEC 十 YAML 的内容树 SHA 并非同一对象。新双来源契约要求不同 Native Task、独立 Design StageOutcome、不可变 Scope Evidence、各自原生 Requirement Trace。
3. **只读 Fail-closed 预检实际实现**：`check_dual_source_binding.py` 验证来源 hash、Revision、原生最新 finalized design Event、stale/reopen、Snapshot digest 和 Scope manifest；单来源旧 Gate 对**指定新任务 ID**被明确阻断。不得解释成双设计已审批。
4. **历史合同保留且显式标为已被覆盖**，Issue #1 仍 OPEN；旧 R06 账本不因新任务创建而声称已完成/已删除。

## 3. 独立 Findings

### RV08-01 / HIGH / LEGACY_SCOPE_GUARD_NOT_GENERALIZED：单来源 Gate 仍仅靠硬编码 Task ID 防错

**证据**：`scripts/native_gate.py:validate_native_with_runner` 仅当 `task_dir.name == "FEATURE-DESC-2AD10B7DBDCA"` 时拒绝单来源 Gate，随后对所有其他任务继续进入旧的单一 `design/PASSED` 核验。新增 `tests/test_native_gate.py:test_skill_ab_task_rejects_dec_only_legacy_native_gate` 同样只覆盖固定 ID。

**风险**：如果 Skill A+B Task 重新创建、迁移、更名、产生其他 Task ID，旧入口不会基于真实设计**来源类型和 Review Scope**阻断。虽然此问题本身不伪造上游审批，但仍可能把“已审批 Skill 设计”和“已审批 DEC YAML”错误绑定到同一单来源合同。

**必须整改**：将 Gate v1 的适用性基于**可独立验证的来源类型/Scope Evidence/Native Task 所审设计对象**判定，而不是固定 Task 名；拒绝任何 Skill-only 设计经 v1 充当 DEC YAML 批准。加入不同 Task ID、迁移和多任务的回归测试。

### RV08-02 / HIGH / V2_CONSUMER_NOT_IMPLEMENTED：双来源校验还不是正式集成消费

**证据**：`scripts/check_dual_source_binding.py` 提供独立 CLI 只读预检；`scripts/p0_integration.py` 仍仅接受 `--gate` / `--demo-fixture-gate`，没有双来源 binding、Skill Task 与 DEC Task 的正式消费路径；`.github/workflows/p0-native-positive.yml` 仍为原 v1 单来源入口。仓库 Owner 文档也明确承认“v2 正向消费尚未完成”。

**风险**：即使未来双来源预检成功，也不能推断集成 Runner 真正将**同一批已审来源/Revision/Evidence**原子绑定到三 Provider 执行及最终 Manifest。

**必须整改**：实现受审 v2 正向消费契约（两 Native Task + 两份批准 Design + 两来源 SHA + 同一运行的 Artifact lineage），运行前后重新校验来源 hash、最新非失效 Event，并建立真实 positive CI 和失败注入测试。禁止把“预检绿灯”升级为 P0 PASSED。

### RV08-03 / HIGH / INDEPENDENT_NATIVE_REVIEW_PENDING：新 Skill R01 仅有 Owner 发布声明

**证据**：`docs/reviews/P0-SKILL-AB-R01-FOUR-STEP-EXECUTION-20261025.md` 报告新 Task `FEATURE-DESC-2AD10B7DBDCA`，Revision `REQCONF-SKILL-AB-R01@sha256-615aa67b147be0093cf52159e61b883bc8c72defeeb6c998bc7ed84a2812f3eb`，Attempt PASSED、Artifact PUBLISHED；六项 Manual Review `AC-01..06` **PENDING**、`wk next=REVIEW_REQUIRED/ISOLATED_REVIEW_SESSION_REQUIRED`、零 `STAGE_OUTCOME_FINALIZED`。这些目前是 Owner 文档事实声明，非本轮对 ZIP 的独立证据重放。

**必须整改**：在真正隔离、获授权的 Reviewer 环境读取 R01 完整 canonical `requirement.md`、Evidence registry/object、Task Plan、Intake、Event ledger 与六项表单，核对内容 SHA 和每条 AC，依法提交原生 Review；由原生阶段后续合法 finalize。该报告或 Git Commit **不能**替代签署。

### RV08-04 / MEDIUM / DEC_PROVIDER_SOURCE_CLEANLINESS：当前 Git 干净检查只覆盖 YAML

**证据**：`scripts/check_dual_source_binding.py:_assert_pinned_dec_checkout` 核对 Git HEAD 为固定 commit，但 `git status --porcelain -- demo/order-payment-yaml` **仅检查该 YAML 目录**。如果其他 Provider 脚本、Java 生成器或 Binding 工具存在未提交改动，此检查本身仍可能通过。验证器将源身份限定于设计 SHA 属合理最小目标，但不得把它描述成“整个固定三 Provider checkout 均未修改”。

**建议整改**：若该预检结果将用于真实 A+B Provider 执行的受信任源声明，补充全仓库干净性或至少精确校验三个 Provider 的真实执行源码及依赖；构造“YAML 未变但 `skills/dec-design`、`skills/dec-implementation` 或 `dec-java-lite` 已改”负向回归。必要时区分 *design-source integrity* 与 *executable-provider integrity* 两种证据。

### RV08-05 / MEDIUM / POSITIVE_TEST_COVERAGE_GAP：没有成功双原生 Design 的消费测试

**证据**：`tests/test_dual_source_binding.py` 目前重点覆盖缺第二来源、身份替换、Task 相同、SHA 过期、Revision 错误、缺 finalized Event、Snapshot 非不可变和 Scope 内容不匹配；未有构造两份一致且真实原生结构合格的正向闭环 fixture，亦未运行经实际隔离 Review 的真正双来源正向 CI。最新 GitHub Actions 仍运行 `--demo-fixture-gate`。

**建议整改**：增加**不伪造审批的测试专用**双来源正向解析 fixture、stale-after-finalize 负向、两个来源部分成功/部分失败以及变更 Provider 可执行源码的用例；真实 P0 通过必须另用正式原生数据。

### RV08-06 / MEDIUM / PM_GOVERNANCE_AND_SCOPE_PENDING：授权 PM 与工作模式治理没有结束

**证据**：`docs/P0-skill-scope-governance-20261025.md` 和 R01 Owner 执行报告明确新 Task 仍为 `STANDARD_FEATURE_FLOW`（十阶段），Impact 中 `businessLogic/dataModel=UNKNOWN`，`PM_SCOPE_DECISION.md` 标为 `NATIVE_PM_AUTHORIZATION_PENDING`；历史 R06 同样未独立结束。使用 `-g ProjectManagerAgent` 执行 CLI **不是**真正授权 PM 签署。

**必须整改**：受权 PM 决定新/旧任务关系、实际 Standard Gate 和影响分类，再由真正隔离 Reviewer 继续。Skill P0 不强制业务 RED/TDDReview，但不能通过文字豁免**已实际绑定**的 Standard 子门禁。

## 4. Latest GitHub CI：当前可独立验证的事实

针对 **同一被审 HEAD** `9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd`：

| Workflow / Run | 直接核查结果 | 允许推断 |
| --- | --- | --- |
| [P0 fixed-provider DEC integration #40162495121](https://github.com/szlwin/common-develop-dec-integration/actions/runs/40162495121) | SUCCESS；unit `44 tests`；固定三 Provider Fixture PASS；`nativeP0Approval=BLOCKED`，`productReleaseReady=false` | 适配器及 Fixture 兼容、负向/单元回归 |
| [P0 real native negative Gate #40162495128](https://github.com/szlwin/common-develop-dec-integration/actions/runs/40162495128) | SUCCESS；`liveNativeCli=PASSED`、`fakeDesignGate=BLOCKED`、`nativeFinalizationPresent=false` | 未批准的原生 Design 必须被阻断 |
| 新 Skill R01 实际独立 Review / 双 Native Design positive | **没有被以上两次 CI 验证** | 不得推断 APPROVED |
| v2 两来源绑定实际 Native→DEC 三 Provider 正向运行 | **尚未接入/执行** | 不得推断 VERIFIED |

源码、文档与 CI 的“新增硬门禁/当前失败关闭”是有效改善，**但所有原生当前 Approval 仍不可从绿灯推断**。

## 5. Skill A+B 需求审查范围（六项 AC）

由于新原生 R01 ZIP 当前不在本轮可读取的原件证据中，`AC-01..06` **不能逐条打正式 YES/VERIFIED**。仓库 Owner 报告中六项仍为 PENDING。建议 Reviewer 逐项核查：

1. **AC-01**：Skill 自身规则/角色/模式/上下游职责，不把完整业务软件 E2E 当作 P0 必做。
2. **AC-02**：独立 Skill Design SHA、明确可审来源、Native Revision/Evidence 与失效规则。
3. **AC-03**：DEC 十文件 YAML 与三个 Provider、Java/JUnit、Binding、lineage 真实一致。
4. **AC-04**：两来源分别独立设计审批；Skill 集成不得拿一个设计 StageOutcome 替代另一个。
5. **AC-05**：未批、篡改、过期、Reopen、缺 Evidence 时失败关闭且不产生误报批准。
6. **AC-06**：A+B Skill P0 与 C 可选软件 E2E / D 产品发布范围分离；保留真正 Standard 模式已生效的门禁。

以上是**独立建议的复核主题**，非对 Owner 原件六份 AC 文本的逐字转录；不得用作正式表单签署。

## 6. 最终审查结论与建议执行顺序

- **产品验收范围及任务分层：ACCEPTABLE**；旧 R05/R06 的业务 TDD 强制范围错误已合理修正。
- **双设计源契约及只读反例校验：PARTIALLY ACCEPTABLE**；识别来源混淆、能阻断已知错配，但 Task-ID 硬编码与正向未接线仍是高优先级问题。
- **Skill A+B 新 R01 Owner 的原生内容与 Event/Evidence 完整复核：INSUFFICIENT_DIRECT_EVIDENCE**。
- **原生隔离 Reviewer、PM 签署、两 Design/PASSED、v2 正向 Skill→DEC、完整 A+B 验收：NOT COMPLETED**。
- **P0 总体：BLOCKED / PARTIALLY IMPLEMENTED**。

建议顺序：① 独立取得 R01 原生交接 ZIP 验真，授权 PM 关闭模式治理；② 隔离 RequirementAnalysisAgent 审查当前 R01、合法 finalize/analysis Trace；③ 修复 Gate 适用性硬编码并为 v2 增加正向/负向自动化；④ 两来源各自独立 Native Design Review 后，正式 v2→DEC positive 回归；⑤ A+B 本体 Skill 开发/测试/Review/归档验收。**C 可选业务软件 E2E 与 D Product Release 不作为 Skill P0 默认硬门禁。**

## 7. 证据与引用

- [最新 R01 Owner 执行报告](https://github.com/szlwin/common-develop-dec-integration/blob/9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd/docs/reviews/P0-SKILL-AB-R01-FOUR-STEP-EXECUTION-20261025.md)
- [双来源 Gate 规范](https://github.com/szlwin/common-develop-dec-integration/blob/9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd/docs/dual-source-design-binding.md)
- [双来源预检代码](https://github.com/szlwin/common-develop-dec-integration/blob/9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd/scripts/check_dual_source_binding.py)
- [旧 Native Gate 代码](https://github.com/szlwin/common-develop-dec-integration/blob/9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd/scripts/native_gate.py)
- [最新验收矩阵](https://github.com/szlwin/common-develop-dec-integration/blob/9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd/docs/P0-skill-scope-governance-20261025.md)
- [GitHub compare：上次 Review→本次 HEAD](https://github.com/szlwin/common-develop-dec-integration/compare/6717a1547c0a84afd3535445748647001c633cfa...9d4dc013a092cda9747d81d98bfdf81c4ae4b1cd)
- [Issue #1：Skill P0](https://github.com/szlwin/common-develop-dec-integration/issues/1)；[Issue #2：可选软件 E2E](https://github.com/szlwin/common-develop-dec-integration/issues/2)

**审查报告提交本身不代表原生审批，且不会更改 Task Event、Review Assertions、Risk、Trace 或 StageOutcome。**
