# P0 Skill A+B 范围拆分——最新提交独立 Review（2026-10-25）

- 仓库：`szlwin/common-develop-dec-integration`
- 被审提交：`99274d7197c2248bcd39fd7d5c9a32d31802dd5b`（相对已审查的 `6717a1547c0a84afd3535445748647001c633cfa`）
- 提交说明：`docs(p0): split Skill A+B acceptance from optional software E2E, preserve Standard gate obligations`
- Review 性质：GitHub 变更/治理契约独立审查；**并非**固定 `common-develop-opt` 的授权、隔离 `RequirementAnalysisAgent` 原生签署。
- **增量文档整改结论：ACCEPTABLE_WITH_OPEN_NATIVE_GATES**；**P0 整体验收：BLOCKED / PARTIALLY IMPLEMENTED**。

## 1. 核查范围与证据等级

GitHub compare API 核实 `6717a154..99274d7` **1 个提交、4 个变动文件**：

1. `docs/P0-skill-scope-governance-20261025.md`（新增，44 行）；
2. `docs/P0-acceptance.md`（新增 7 行）；
3. `docs/native-positive-runbook.md`（新增 5 行）；
4. `README.md`（新增 2 行）。

直接读取了上述 GitHub 文件、Issue #1 和新 Issue #2、`docs/gate-contract.md`、`scripts/native_gate.py`、`docs/P0-native-design-review.md`，并读取最新两条 GitHub Actions 的 job/log。**本次没有代码改动，没有原生 Task ZIP 随本次 Git commit 提交。**

新文档称，原生 Skill A+B task 交接包为 `p0-skill-ab-pm-task-split-20261025.zip`，内含 19/19 SHA 校验、真实新 DocRoot、原 R06 ZIP 与 CLI 输出。这些为 **Owner 声明**；未从 GitHub 独立读取、验证 ZIP 或执行原生命令，不能标注成“本次独立已验证”。同理，既有 R06 ZIP 的 Revision/EVD-000011/012/58 事件尚未在本次独立复验。

## 2. 对上一轮 Findings 的整改判定

| 上轮问题 | 本次证据与结论 | 状态 |
|---|---|---|
| RV06-01：Skill P0 与完整软件 E2E、Standard 合同混淆 | Issue #1、Issue #2、README、验收矩阵明确 A+B 必做/C 可选/D 独立；历史 Standard 原生任务未被宣称豁免。**产品验收范围层面已修复**；授权 PM 对新老 Task 的工作模式及任务归属决定仍未完成 | **PRODUCT_SCOPE_RESOLVED / NATIVE_PM_OPEN** |
| RV06-02：R06 原生字节证据不足 | 新提交只有范围文档，无 R06 ZIP/EVD 或新任务 ZIP | **OPEN** |
| RV06-03：Fixture CI 不等于原生批准 | 新文档明确区分，并保持正向 Gate 必做；真实 `design/PASSED` 仍未出现 | **DISCLAIMERS_FIXED / POSITIVE_GATE_OPEN** |
| RV06-04：Trace/Risk 后续治理 | 责任人、期限和 fail-closed 边界明确，实质执行未发生 | **DEFERRED_WITH_GATE** |
| RV06-05：Gitee Commit 固定来源 | 之前提交已加固，本次 CI 未更改源选择 | **RETAINS_PRIOR_VERIFICATION** |

## 3. 本次新增/延续独立 Findings

### RV07-01 / HIGH / NATIVE_PM_OPEN：产品范围澄清不等于原生工作模式决议

现有 `FEATURE-DESC-DAE4FAB5F9F4` 仍为 R06 `PUBLISHED`、六项独立 Review `PENDING`；新 `FEATURE-DESC-2AD10B7DBDCA` 按 Owner 文档同样是 `NEW_REQUIREMENT/STANDARD_FEATURE_FLOW`，保留标准十阶段。`-g ProjectManagerAgent` 是 CLI Agent 参数，不是外部 PM 授权/签署凭证。

**行动**：由受权 PM 正式批准新 A+B Task 的目标、模式、Impact Assessment（新 Intake 的 `businessLogic/dataModel=UNKNOWN`）、与历史 R06 的关系及后者转为可选 C 的正式处置；按原生官方机制保留历史事件。现阶段不得将 RV06-01 的**原生治理部分**标为 CLOSED。

### RV07-02 / HIGH / EVIDENCE_NOT_IN_REPO：新任务与旧 R06 的交接证据尚不可独立验真

公开 GitHub 只有范围文档和说明，新 DocRoot 的 `request_intake.json`、`task_events.jsonl`、`wk start/begin` 命令 JSON、19 项清单并未随提交公开。Owner 文档声明原始 R06 完整保留，但本轮没有独立的两份 Task 字节比较。对新 Task 不能复用旧 R06 的 Revision、六项 AC 或 Reviewer 表单。

**行动**：在可信独立 Reviewer 环境提供含 SHA 清单的脱敏原生任务原件（不宜放公开仓库的资料使用私有渠道）；核验真正 task id、DocRoot、CLI 退出码、任务路由、Intake 状态和旧事件的字节不变性。新 Task `requirement_confirmation` Artifact 尚未发布，因此不具备原生内容 Review 的当前 Revision。

### RV07-03 / HIGH / DESIGN_BINDING_DECISION_REQUIRED：Skill 设计审核对象与 DEC Demo 设计摘要的绑定必须明确

`docs/gate-contract.md` 与 `scripts/native_gate.py:verify_content_bound_revision` 规定 **native `design.output_revision = sha256:<exact order-payment DEC YAML tree digest>`**，而新独立 A+B Task 的设计对象是 Skill 规则/路由/适配器本身。两者不是天然同一个制品。真实独立 `Design Review` 必须确实覆盖这一版 canonical DEC YAML，而不能只审核 Skill 架构就把其 StageOutcome 绑定为 Demo YAML 已审批。

**行动**：在新 Task 需求及 Design Artifact 中明确 DEC YAML 只是 A+B 集成的**固定、待审核输入**，提供十文件/树哈希、内容 Review scope 与原生 Task/Revision/Evidence 映射。若 Skill 设计 Revision 和 DEC 设计 Revision 不同，应由合法独立设计来源/双来源绑定契约处理；不要用单一字符串偷换审查对象。此为设计正向 Gate 前置风险，目前尚无证据证明发生伪通过。

### RV07-04 / MEDIUM / CI_SCOPE_ONLY：当前 CI 与 A+B 全体验收有边界

最新 HEAD：

- 固定 Provider/Fixture Action `40154238102` **success**，Python `34/34`，`integrationStatus=VERIFIED_WITH_FIXTURE`、`decFixtureIntegration=PASSED`、`nativeP0Approval=BLOCKED`、`productReleaseReady=false`；
- 原生负向 Gate Action `40154238069` **success**，日志 `fakeDesignGate=BLOCKED`、`nativeFinalizationPresent=false`。

成功证明现有适配器和 fail-closed 负向行为，不证明新 A+B 原生 Reviewer、Design Gate、Native→DEC 正向运行或历史 R06 已完成。后续需真实、受审的任务与固定输入执行正向联调，保留日志和 Artifacts。

### RV07-05 / LOW / DOC_HISTORICAL_DRIFT：部分旧文档仍保留已被取代的 Skill P0 强制完整软件 E2E 文案

`docs/P0-native-design-review.md` 的“Full lifecycle closure” 和 `docs/P0-native-task-handoff.md` 末尾仍出现完整业务 E2E 后才能完成 Issue #1 的旧叙述。新 `README.md`、`docs/P0-acceptance.md`、Issue #1 和 Runbook 的最新前言/附注虽已声明覆盖旧合同，但单独进入旧文档的读者仍可能误解。

**行动**：在这两份旧文档开头添加“历史合同，不再控制 2026-10-25 Skill P0 A+B”的显式标记，指向统一验收矩阵和 Issue #2；保留历史审计事实。

## 4. 最新验收矩阵判定

| 验收对象 | 内容/实现判断 | 是否已经正式通过 |
|---|---|---|
| A：Skill 路由、规范、原生身份/Review/Evidence、设计正向 Gate | 范围正确；正向 native Gate 未完成；新 Skill Task 的实际 Reviewer 尚不存在 | **NO** |
| B：三固定 Provider Demo、Java/JUnit、Binding/lineage 与负向回归 | Fixture 和独立回归有成功 CI，正向来源绑定与 A 仍待完成 | **PARTIAL** |
| C：完整业务软件 Standard E2E | 已按用户目标转为独立可选 Issue #2；不作为 P0 必做 | **NOT REQUIRED FOR A+B** |
| D：产品发布 | 四个上游 Design ID 仍 PLANNED、使用外部替身，保持独立 | **NOT READY** |
| 历史 R06 原生需求内容 Review | Owner 报告 `PUBLISHED`，六条 PENDING；无独立再次校验、签署或 `finalize-phase` 证据 | **PENDING** |
| 新 A+B Task 需求确认 Review | Owner 报告 `wk begin=ARTIFACT_NOT_PUBLISHED`；当前无已发布 Revision、无法审核不存在的 AC | **NOT READY FOR REVIEW** |

## 5. 最终独立结论

**本次 Commit 作为“产品 P0 范围纠偏 + Task 职责拆分”的增量文档变更是可接受的（`ACCEPTABLE_WITH_OPEN_NATIVE_GATES`）**。上一轮 **RV06-01 的“产品验收范围”子问题可关闭**，但不能由此宣布原生 PM、R06 原文/Evidence、独立 Review 或 Design Gate 完成。真正的原生运行时权限和 StageOutcome 没有被本次提交改变。

**P0 总体：BLOCKED / PARTIALLY IMPLEMENTED。** 目前应按顺序：正式 PM 任务范围/模式决议 → 新 A+B Owner Requirement Artifact 发布 → 隔离 RequirementAnalysisAgent Review → 合法的 requirement_analysis Trace/Design Review → 原生正向 Design Gate 与三 Provider Evidence → Skill A+B 完整验收。C 软件 E2E 独立可选，D 产品发布独立。

本报告为独立内容/代码契约审查，不调用 `manual_review.py submit`、不伪造 Reviewer、不给任何原生 AC 设置 VERIFIED、不产生 `STAGE_OUTCOME_FINALIZED`。

## 6. 来源

- GitHub 变更：https://github.com/szlwin/common-develop-dec-integration/compare/6717a1547c0a84afd3535445748647001c633cfa...99274d7197c2248bcd39fd7d5c9a32d31802dd5b
- 新范围治理：https://github.com/szlwin/common-develop-dec-integration/blob/main/docs/P0-skill-scope-governance-20261025.md
- 原生 Gate 契约：https://github.com/szlwin/common-develop-dec-integration/blob/main/docs/gate-contract.md
- 原生 Gate 实现：https://github.com/szlwin/common-develop-dec-integration/blob/main/scripts/native_gate.py
- Issue #1：https://github.com/szlwin/common-develop-dec-integration/issues/1
- Issue #2：https://github.com/szlwin/common-develop-dec-integration/issues/2
- Fixture CI：https://github.com/szlwin/common-develop-dec-integration/actions/runs/40154238102
- Native Negative Gate CI：https://github.com/szlwin/common-develop-dec-integration/actions/runs/40154238069
