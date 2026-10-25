# 2026-10-25 — R01 真实证据复核与 RV08 代码整改进展

> **证据完整性已复核，正式隔离 Review 仍 PENDING。** 此报告不是新 RequirementAnalysisAgent 签署，也不是 PM 本人授权证明。没有改动新旧原生事件账本。

## 当前 GitHub Review

[独立仓库预审](P0-SKILL-AB-R01-INDEPENDENT-REVIEW-20261025.md) 对 `9d4dc013` 结论 `NEEDS_CHANGES_BEFORE_NATIVE_POSITIVE`，指出 RV08-01～06：旧单来源 Gate 任务 ID 硬编码、v2 Consumer 未接线、新 R01 尚未独立签署、Provider 源洁净性检查不充分、正向测试不足、PM 治理未完成。

## 本轮直接读取用户原始 ZIP 及原生命令结果

- 文件：`p0-skill-ab-r01-owner-and-dual-source-handoff-20261025.zip`；ZIP SHA-256 **33903e7638cd5400dbe866c18404177f738d2d33b1565c23e6cff06510f32653**，CRC 正常，`SHA256SUMS.txt` **39/39 校验通过**。
- R01 canonical `requirement.md` 当前 SHA-256 **615aa67b147be0093cf52159e61b883bc8c72defeeb6c998bc7ed84a2812f3eb**。
- 原生 Task `FEATURE-DESC-2AD10B7DBDCA`；事件 JSONL **8 条**（1×ATTEMPT_STARTED、1×ATTEMPT_FINISHED、1×STAGE_OUTCOME_PUBLISHED、0×STAGE_OUTCOME_FINALIZED）；六条当前 `AC-01..06` Manual Review Assertion 均 **PENDING**。
- `PM_SCOPE_DECISION.md` 字节包含 **PROJECT_SCOPE_ACCEPTED_BY_USER / NATIVE_PM_AUTHORIZATION_PENDING**，并明确两个 `businessLogic/dataModel` Impact 仍 UNKNOWN，旧 R06 历史任务原样保留。
- 从 ZIP 中解压的**固定原版 Skill** `scripts/long_task.py validate -g ProjectManagerAgent --task-dir {CURRENT_R01_TASK} --json` 实际返回 **PASSED**（结构）；`scripts/wk.py next -g ProjectManagerAgent --task-dir {CURRENT_R01_TASK} --json` 实际返回 **READY / REVIEW_REQUIRED / RequirementAnalysisAgent / ISOLATED_REVIEW_SESSION_REQUIRED**。该 `READY` 指下一步 Reviewer 可执行，不表示 Review 已通过。
- 独立 Review Forms ZIP SHA-256：**bb76c300104e4417e8f5c556cc32d0d12e9b5ebe2b9ac6ac81f7749174230c91**；表单均为空白，不是 Reviewer 意见。

这消除了此前 RV08-03 对 R01 ZIP 原始字节不可访问的**证据限制**，但绝不把“Owner Evidence 自洽”提升为“被真正隔离 Reviewer 批准”。

## RV08 代码整改状态

| Finding | 本轮实现 | 剩余门禁 |
|---|---|---|
| RV08-01 HIGH | 原 `native_gate.py` 仅凭某固定 Task ID 拒绝单来源已替换：**任意 Task** 的 v1 DEC Gate 必须由该原生 Design StageOutcome 的真实 Evidence ID 指向不可变 DEC YAML Scope Snapshot，其内容/任务/DEC SHA 匹配；Skill-design Scope 一律拒绝。不同任务号的测试已增加 | 尚无真实 v1 设计审批材料以正向验证 |
| RV08-02 HIGH | `p0_integration.py` 已新增双来源 Runner CLI，消费两份独立 native Design StageOutcome 与 Review Scope，Provider 执行**前后**重验，并将两来源绑定到本轮 Manifest/报告 | 两份获批真实 Design 来源不存在；尚无真正 native-positive 成功 |
| RV08-03 HIGH | 对 R01 ZIP 39/39、当前 Revision、Evidence、8 Events、六条 PENDING 及原生 CLI 进行独立的字节与结构复验 | 真正隔离的 `RequirementAnalysisAgent` 正式提交与 finalize-phase 未完成 |
| RV08-04 MEDIUM | 双源预检从只检查 YAML 改为启动前 Git 全仓库洁净检查；新增固定 Provider 可执行跟踪源码 SHA，运行完成后重算，防止 Generator/Adapter 中途改变 | 后续应由真实完整 CI 验证该运行时路径 |
| RV08-05 MEDIUM | 增加测试专用双原生 Finalized Design + Scope SNAPSHOT 正向解析样例、Source SHA/Task 偷换/重开/Generator 源变动反例 | 测试用 Fixture 不代表原生 Review；真正完整双来源运行待实施 |
| RV08-06 MEDIUM | PM_SCOPE_DECISION 已证实 Pending，产品范围与历史 Standard 阶段边界未被覆盖 | **授权 PM 签署仍阻断** |

## 下一步硬门禁

1. 授权 PM 对新 R01 与旧 R06 的职责/Standard 模式/两项 UNKNOWN Impact 正式签署，记录原生受支持的 Evidence 或 Issue Resolution；不能凭 `-g ProjectManagerAgent` 冒认权限。
2. 在**全新隔离 Reviewer 执行环境**读取此 39/39 原生任务包和六份空白表单，逐条审核 R01 AC-01～06，若不通过返修；通过后由原生工具正式执行 `manual_review.py submit` 和合法 `finalize-phase`。
3. 需求分析合法 `sync-traceability`、Skill Design / DEC YAML Design 分开正式审核与 StageOutcome、必要的测试/代码阶段，再用新 Runner 正向验证。
4. 固定 Provider/JUnit、Manifest lineage、负向异常及 Skill 本体后续 Standard 阶段完整验收；C 可选业务软件 E2E/D 产品发布保持独立。

**总体 P0：BLOCKED / PARTIALLY IMPLEMENTED，Issue #1 OPEN。**
