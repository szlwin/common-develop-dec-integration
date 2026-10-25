# P0 双来源 Design 绑定契约（RV07-03）

> **当前：契约与只读机械校验已经实现，两个真实独立 Design/PASSED 尚不存在。P0 BLOCKED。**
> 本文不生成审批，不更改 common-develop-opt 的原生 Event，不表示产品发布。现有单来源 Gate v1 只适用于真正审查 DEC YAML 的原生任务，不能拿审核 Skill 架构的 Task 冒充 DEC 业务设计批准。

## 1. 两种不同的设计对象

| 来源 | 审核对象 | 正式内容摘要 | 原生审批与证据 |
|---|---|---|---|
| A：Skill Design | Skill 规范、路由、权限、原生 Gate、Artifact 血缘、异常/恢复及 Adapter 设计源 | 真实 Skill 设计文件或目录 SHA-256 | Skill 独立 Native Task、Design/PASSED StageOutcome、真实独立 Reviewer、不可变 Scope Evidence |
| B：DEC YAML Design | 固定 DEC commit 4fb21242498746365c201fdf2a7fd8052f3a122a 的 demo/order-payment-yaml 十个文件 | 当前十文件树的确定性 SHA-256 | **另外一个** DEC Design Native Task、Design/PASSED StageOutcome、真实独立 Reviewer、不可变 Scope Evidence |

A 的设计 Revision 不得改名为 B 的 tree SHA。两者设计源不同、Native Task 不同、独立 Review Scope 不同。新 Skill A+B 需求的 Revision 不是 Design Review，也不是 B 的设计审批。

## 2. 双来源候选绑定格式（不是审批）

Schema：common-develop-dec/dual-source-design-binding/v1。以下只展示字段和占位符，绝非真实批准：

~~~json
{
  "schema": "common-develop-dec/dual-source-design-binding/v1",
  "skill": {
    "taskId": "<SKILL_AB_NATIVE_TASK_ID>",
    "designRevision": "sha256:<SKILL_DESIGN_SHA256>",
    "stageOutcomeId": "<REAL_SKILL_STAGE_OUTCOME_ID>",
    "finalizationEventId": "<REAL_SKILL_FINALIZED_EVENT_ID>",
    "sourceSha256": "<SKILL_DESIGN_SHA256>",
    "reviewScopeEvidenceId": "<IMMUTABLE_SKILL_SCOPE_EVIDENCE_ID>",
    "designSourceKind": "skill-design"
  },
  "dec": {
    "taskId": "<SEPARATE_DEC_NATIVE_TASK_ID>",
    "designRevision": "sha256:<DEC_YAML_TREE_SHA256>",
    "stageOutcomeId": "<REAL_DEC_STAGE_OUTCOME_ID>",
    "finalizationEventId": "<REAL_DEC_FINALIZED_EVENT_ID>",
    "sourceSha256": "<DEC_YAML_TREE_SHA256>",
    "reviewScopeEvidenceId": "<IMMUTABLE_DEC_SCOPE_EVIDENCE_ID>",
    "designSourceKind": "dec-yaml-design"
  }
}
~~~

每个 reviewScopeEvidenceId 必须存在于本来源真实 Native StageOutcome 的 Evidence ID 列表中，并是原生 Evidence registry 记录的设计来源 design_ref / SNAPSHOT。该不可变快照必须包含下面这样的 JSON Scope Manifest，且字节哈希应与 registry 的 digest 一致：

~~~json
{
  "schema": "common-develop-dec/review-scope/v1",
  "taskId": "<SAME_NATIVE_TASK_ID>",
  "designSourceKind": "skill-design",
  "sourceSha256": "<EXACT_CONTENT_DIGEST_REVIEWED>"
}
~~~

DEC 来源使用 designSourceKind=dec-yaml-design。Reviewer 必须真实审查相应完整设计源，而不是只检查该 JSON Manifest；正式任务必须保存来源 commit、十文件清单、设计源路径、快照和 Reviewer 记录。

## 3. 只读预检与现有 Gate 的 fail-closed 边界

仓库新增脚本 scripts/check_dual_source_binding.py，用于在可信的固定版本源与原生任务副本上做**双来源机械证据预检**，不会执行 Review 或写入原生账本。

~~~sh
python scripts/check_dual_source_binding.py \
  --binding /trusted/dual-binding.json \
  --opt-root /trusted/pinned-common-develop-opt \
  --skill-task-dir /trusted/skill-doc/version/V_P0/task/SKILL_TASK \
  --dec-task-dir /trusted/dec-doc/version/V_P0/task/DEC_TASK \
  --skill-design-source /trusted/skill-design.md \
  --dec-root /trusted/fixed-dec-source
~~~

校验器核对两个不同原生 Task ID、各自真实来源字节摘要和 Revision；分别调用官方 long_task validate 与 task-events；验证各自最新 finalized design/PASSED 及后续 stale/superseded/reopen；验证 Event/Outcome ID、Scope Evidence ID、不可变 Snapshot 字节；验证两来源的合法 canonical requirement Trace。

只有两份完整真实证据全部满足时才返回 TWO_SOURCE_NATIVE_EVIDENCE_MATCHED；即便此预检通过，**它也不证明授权 Reviewer 真正独立执行，更不是 P0 已完整验收或产品 READY**。隔离 Reviewer/权限由原生 Host 负责。

**当前集成消费能力边界**：旧 p0_integration.py 的单来源正向链路还不能直接消费 v2 两来源。为了避免误用，native_gate.validate_native_with_runner 对新 Skill A+B Task FEATURE-DESC-2AD10B7DBDCA 现有单来源 Gate 明确阻断；待真正独立 Review、双来源关联和受审的 v2 消费路径实施后再启用正向运行。不能用现有 v1 Gate、Fixture、人工 JSON 或 Skill-only Design/PASSED 代替 DEC 已批准来源。

## 4. 失效与重审

| 变化 | 所需处置 |
|---|---|
| Skill 设计文本、路由、权限或适配器变更 | A 的 SHA 失效，A 的 Design Reviewer 重新审查 |
| DEC YAML 任意文件变更、源 commit 改变 | B Tree SHA 失效，B 重新正式 Review，不能复用旧设计 |
| 任一 Task Reopen、Superseded、Phase Stale 或新发布替代 | 对应来源拒绝；旧 Event 不再可消费 |
| Scope Evidence 不存在、不在 Outcome 中或 Snapshot hash 不匹配 | 双来源 Gate BLOCKED |
| 任一来源单独通过，另一来源仍 PENDING | 整体阻断，不运行正式 Native-positive |
| A+B 后续测试成功而可选软件 C 或产品 D 未完成 | 分层验收，不声明完整业务产品发布 |

## 5. 独立 Reviewer 正式审核前需准备

分别给出：设计源文件/目录、源 Git commit、实际文件 SHA 或 tree digest、Native Task ID、原生最新 PASSED Design StageOutcome、Finalization Event、当前 input_revisions、全部 Evidence、审核 Scope Snapshot 和真正独立 Reviewer 的提交记录。被审核的实际输入必须在审核之前固定，不能在审核后替换 Binding 值。

相关源：原始 docs/gate-contract.md 的 v1 合约与 docs/P0-native-design-review.md 历史 DEC-only 候选仍保留，不用于新的 Skill A+B 双来源正向授权。Issue #1 保持 BLOCKED。
