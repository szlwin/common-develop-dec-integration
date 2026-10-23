# P0 R04 — RequirementAnalysisAgent 审核标准下的内容预审（未签署）

> **内容建议：NEEDS_CHANGES；正式原生审核：PENDING。** 评估者所在的 ChatGPT 会话曾执行同一任务的 Owner 返修，不满足原生 `ISOLATED_REVIEW_SESSION_REQUIRED`。本文件不得作为 `manual_review.py submit`、`STAGE_OUTCOME_FINALIZED` 或独立 Reviewer PASSED 的替代证据。

## 已复现事实

- Task `FEATURE-DESC-DAE4FAB5F9F4`；R04 当前 `requirement_confirmation`、Iteration 004；正式 Revision `REQCONF-P0-R04@sha256-73beddea3e0ec60120c12c027877bb5aebd1ec35af64159e2e6b0b45dae5a28d`。
- 当前 `requirement.md` 与 `EVD-000007` 快照 **bytes identical**，SHA-256 为 `73beddea3e0ec60120c12c027877bb5aebd1ec35af64159e2e6b0b45dae5a28d`；`EVD-000008` 为 Owner 命令证据。
- 原始 ZIP SHA-256 `85e348547574be8b7b9cd92bfa6c2e6749d5cb901d7c5bcc3a72c4502310b370`。ZIP 文件 60/60、固定原生 Skill `FILE_MANIFEST.sha256` 532/532 一致。
- 固定原生 `requirement_doc validate --stage confirmation` 和 `--stage analysis` 都是 `valid=true, errors=[]`；`long_task validate` 是 `PASSED`（结构），`wk next` 要求 `RequirementAnalysisAgent` 在隔离 Reviewer Session 继续。
- 事件共 38 条，4 次 `STAGE_OUTCOME_PUBLISHED`、3 次 `SUPERSEDED`、3 次 `PHASE_STALE`、**0 次 `STAGE_OUTCOME_FINALIZED`**；六项当前 R04 `MANUAL_REVIEW` 断言仍全部 `PENDING`。原生 Task/Event/Review/Intake/Risk 文件没有修改。

## 原生 Review Criterion 对照

| Criterion | 内容建议 | 原因 |
|---|---|---|
| RC-REQ-001 目标与对象 | **需修改** | R04 正文 §1 当前 I004，§2.1 却仍写「现已正式 reopen 到 Iteration 003」 |
| RC-REQ-002 范围边界 | 基本明确 | 三固定 Provider 定义清楚，但 §9 第一条「两个 Provider 版本」不一致 |
| RC-REQ-003 验收可观察 | **需修改** | 原生 Assertions 编号 `AC-01..06`，正文/§13 是 `AC-REQ-P0-001-001..006`，缺正式映射；生成代码与 RED 时序要明确 |
| RC-REQ-004 失败/禁止副作用 | 满足（范围） | stale/reopen/缺 Review 与外部支付、敏感凭据禁止条件明确 |
| RC-REQ-005 关键决策闭合 | **需修改** | §12.1 声明无待决，但 Intake 九项 UNKNOWN；§11.4 对生成代码是否必须在 RED 前产生仅给条件性分段方案，未封闭实施决策 |

## 六条 AC 内容建议（**不是**正式表单结果）

| Native Assertion | 候选 canonical 对应 | 建议 | 说明 |
|---|---|---|---|
| AC-01 | AC-REQ-P0-001-001 | **NO** | 当前状态不准和正式映射缺失 |
| AC-02 | AC-REQ-P0-001-002 | YES（仅范围） | 设计 SHA/Revision/失效约束明确，未代表原始 YAML 已审 |
| AC-03 | AC-REQ-P0-001-003 | YES（仅范围） | Provider/Binding/JUnit/父子 SHA/日志验收明确 |
| AC-04 | AC-REQ-P0-001-004 | **NO** | §6.1.4 Design 通过后执行三 Provider 与 §11.4 RED 审查后再纳入生成代码，缺确定的两段式执行边界 |
| AC-05 | AC-REQ-P0-001-005 | YES（仅范围） | Fail-closed、异常与恢复边界明确 |
| AC-06 | AC-REQ-P0-001-006 | YES（仅范围） | P0 与产品发布隔离、4 个 PLANNED、外部替身界限明确 |

## 发现与 Owner 返修建议

1. **RV04-01 High，错误的当前 Iteration 与 Provider 数量。** 正文 §2.1 需同步现有发布状态，§9 第一条「两个」改为三固定 Provider；必须通过原生修订产生新快照，不能直接覆盖已发布 R04。
2. **RV04-02 High，缺 AC 同一性映射。** 形式化定义 `AC-01..06` ↔ `AC-REQ-P0-001-001..006`，列明逐项审查证据和阶段责任；真正更新 canonical Trace 要在合法的 `requirement_analysis` 阶段执行。
3. **RV04-03 High，TDD/Provider 时序仍存在实现歧义。** 固定两阶段：独立设计预览与真正 RED 后的正式生成/实现，明确哪些 Provider 命令何时运行，哪个 Artifact 可以先存在，禁止预览作为正式 Development/RED 通过证据；如固定脚本无法分段，应阻断实施计划而非假定可行。
4. **RV04-04 Medium，影响分类治理未闭合。** 原生 Intake 九项 UNKNOWN、Risk NOT_SCANNED，§11.5 仅有 Owner 候选；把已决范围与尚待 PM 正式登记的治理事项分别写清，并给出角色/最晚 Gate。**原生 Risk Scan 需要开发 Revision，不能单独将 NOT_SCANNED 作为确认阶段否决理由。**
5. **RV04-05 Medium，Task Plan 中验证命令不便于跨工作区运行。** `validation_commands` 使用 `../taskcopy/native-doc`；建议通过正式 Task/Amendment 采用当前绝对 `--task-dir`。静态初始 iteration=001 与当前运行时=004 数字不等，但原生验证 PASSED，不能据此未经原生规则直接篡改计划。
6. **RV04-06 Deferred，旧 R01 Trace 与风险扫描。** `sync-traceability --dry-run` 提示新增 `TR-REQ-P0-001-001`，不会自动删旧 Trace；正式同步是后续 `requirement_analysis` 职责，Design→DEC 必须拒绝陈旧 SHA；Risk Scan 在合法开发阶段处理。
7. **RV04-07 Gate，独立性约束仍未满足。** 当前 Owner 会话不可代替 `RequirementAnalysisAgent`；R04 的六份 Review 表单仍为空白，既无 `submit` 也无 Finalized Outcome。

## 下一步

建议 Owner 依原生 Reopen/Amendment 正式返修 RV04-01～04、整理 RV04-05 的官方计划问题，发布全新内容绑定 Revision/Evidence；随后在真正隔离的 Reviewer 会话重新审查并决定，不能沿用这里的 YES/NO。RV04-06 的后续阶段责任保持显式硬 Gate。

**结论：内容预审 NEEDS_CHANGES；正式原生独立 Review 未提交；P0 继续 BLOCKED。**
