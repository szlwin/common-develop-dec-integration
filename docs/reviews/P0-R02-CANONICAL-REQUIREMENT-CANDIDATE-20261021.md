# P0 R02 — 原生结构化需求可执行候选稿及受控交接（2026-10-21）

> **状态：候选文件校验通过；当前原生 Reviewer 仍 PENDING；没有新 Owner Artifact、StageOutcome 或审批。P0 BLOCKED。**
>
> 本文是已发布 R02 需求的**后续结构化转换候选**和正式执行步骤，不是 R02 原始 Artifact，不是新批准 Revision，也不修改 2026-10-19 的独立 NEEDS_CHANGES 审查结论。

## 来源与重要边界

- 原始 Native Task：`FEATURE-DESC-DAE4FAB5F9F4`，阶段 `requirement_confirmation`，已发布 R02：`REQCONF-P0-R02@sha256-b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2`。
- 原生固定 Skill 源：Gitee `b26715f6779b373b4f840b519ba9725fed5d789a`。本轮实际执行的文件级 `FILE_MANIFEST.sha256` 原始校验通过；这不替代独立 Git object 身份检查。
- GitHub 在旧复查快照 `116156cb` 后另有 `56ef90a69003056fa739cd884541e549a1d89435`（修正独立需求内容 Review 与需求分析追踪同步的阶段边界），`66d24b4cbafe33e0df051a3a6239ac2b2623fa92`（更新正式验收声明）。
- 原生 `requirement_doc.py` 支持 `init` 生成 `version/V_P0/requirement/{TASK}/requirement.md`；此文件应在需求确认形成、在 `requirement_analysis` 补全。后续 `sync-traceability` **首先验证 analysis 阶段的正式文档结构**，与 R02 当前非规范命名的 `requirement_confirmation.md` 不同。

## 真实可重复验证（隔离候选任务，零审批写入）

此次在**原始 R02 ZIP 的独立恢复副本**中使用 `requirement_doc.py init -g RequirementConfirmationAgent` 生成候选 `requirement.md`，把固定 Provider 的权限/范围/失效规则、六项差异化验收 AC、十个原生阶段责任和风险约束整合到官方 14 节模板。

候选文档文件 SHA-256：`1c733bc8a94758e3e0f5d00128ab50e9b00f3251553d71004dddeb040b4e1240`。这不是已发布 R02 的输出 Revision（两者字节不同）。

| 官方校验 | 原始结果 | 审查含义 |
|---|---|---|
| `requirement_doc.py init --json` | 成功 | 模板路径由原生命令创建 |
| `validate --stage confirmation` | `valid=true, errors=[]` | 格式和确认阶段内容规则通过 |
| `validate --stage analysis` | `valid=true, errors=[]` | 结构规则通过；包含 6 AC、1 Trace、2 BR、1 CR、0 未解决占位符 |
| `sync-traceability --dry-run` | `changed=true, created=[TR-REQ-P0-001-001], resultTraceCount=2` | 同步命令在结构上可执行，**未修改实际 Trace** |
| `long_task.py validate` | `PASSED`，阶段仍为 `requirement_confirmation`，任务状态 `PARTIAL` | 原任务结构通过，**不是 Review PASSED** |
| R02 原文、原始事件/Trace/Acceptance | 恢复副本与 ZIP **逐字节一致** | 未篡改旧账本/审核状态 |

完整候选 Markdown、5 个原生命令 JSON 输出、历史 R02 交接 ZIP 和 SHA256SUMS 已作为独立文件包交付用户会话；**该包不会被视作最新原生任务输入或新官方 Evidence**。

## 审核所需的实际工作

1. 先由**真正隔离**的 `RequirementAnalysisAgent` 对当前已发布 R02、`EVD-000003/000004` 和六项仍 PENDING 的 Review Assertion 审核范围与关键风险；如认为文档规范化是确认阶段的阻断问题，应按原生正式 Issue/Reopen 或 Amendment 退回 Owner，而不是当前会话直接把候选文件覆盖成已批准来源。
2. 旧 Task Plan 的 `allowed_files` 仍限定 `requirement_confirmation.md`、`validation_commands` 仍引用旧工作目录；未经原生修订不能直接把新 `requirement.md` 塞入旧 Attempt 并宣称 R02 已通过。需将候选文档合法纳入后续阶段的 Task/Artifact 和 Evidence，保留当前审批引用及原文哈希。
3. 进入 `requirement_analysis` 后，必须核实业务流程 `FLOW-REQ-P0-001-001` 的**实际结构化业务流程内容**和跨模块依赖影响，并在相关审批范围内补齐，不应把“文档 `validate` 通过”当作全部流程事实已验证。
4. `sync-traceability --dry-run` 创建新标准 Trace 而**不会自动删掉**旧 `TR-P0-REQCONF-001`。由合法 Agent 使用当前真实 DocRoot 正式同步，然后审核旧追踪的处置/版本失效与关系映射，不得直接手工改旧 JSON 或追加虚假 `TRACEABILITY_REVALIDATED` 事件。
5. 在真的 `requirement_analysis`、`business_model` 和 `design` 完成独立 Review/PASSED 前，不得执行 native-positive DEC 正向 Gate。Risk Scan 仍 `NOT_SCANNED`，需在原生规定阶段真实完成或合法记录其不适用理由。

**状态**：R-01..R-04 已有文档整改；R-05/R-06 仍需原生对象级处置；R-07 依然是独立 Review 阻断；R-08 的正式同步需要在需求分析阶段完成并在 Design→DEC Gate 严格验证。**P0 BLOCKED / PARTIALLY IMPLEMENTED，Issue #1 保持 OPEN。**
