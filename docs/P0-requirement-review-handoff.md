# P0 Requirement Confirmation 原生审核交接

**真实执行进度：Owner Attempt PASSED / Artifact PUBLISHED / Independent Review PENDING。**

这份说明记录了从固定 Gitee `common-develop-opt` 源码 `b26715f6779b373b4f840b519ba9725fed5d789a` 执行的真实结果。与只在 CI 中生成“Review 候选包”不同，本次已从原始任务账本恢复并实际执行正式 Task/Attempt/Evidence/Artifact 命令。

## 真实对象及校验

| 对象 | 实际值 |
|---|---|
| Native task | `FEATURE-DESC-DAE4FAB5F9F4` |
| Plan task | `TASK-REQCONF-P0-001` |
| Attempt | `ATTEMPT-TASK-REQCONF-P0-001-I001-A001`，Owner PASSED |
| Requirement revision | `REQCONF-P0-R01@sha256-130eb2a1a3d5b74f175755101737fe5b74a25e8fdee33665158af514a16a7db4` |
| Immutable owner evidence | `EVD-000001`（文档快照），`EVD-000002`（实际验证命令） |
| StageOutcome ID | `SO-FEATURE-DESC-DAE4FAB5F9F4-REQUIREMENT_CONFIRMATION-I001` |
| StageOutcome status | **RUNNING / PUBLISHED**；不是 FINALIZED / PASSED |
| Manual Review | 6 个 PENDING assertions，AC-01～AC-06 |
| Required independent Reviewer | `RequirementAnalysisAgent` |
| Official next gate | `REVIEW_REQUIRED`、`ISOLATED_REVIEW_SESSION_REQUIRED` |
| Runtime validator | PASSED，证明结构有效，不代表独立审批 |
| P0 overall | BLOCKED |

## Review 执行边界

用户对话中的 Owner 和另一个名字相同的 Reviewer **不能算独立上下文**。原生路由明确要求 `ownerContextReuseAllowed=false`，所以 Review 必须在真正隔离的 Reviewer 会话里完成，而非由当前工作会话修改 `acceptance.json` 或伪造 `STAGE_OUTCOME_FINALIZED`。

本次交付的原生任务 ZIP 包含原始 `native-doc/`、官方创建的 Evidence Registry、Review Assertions、`task_events.jsonl`、未填写的 `review-forms/AC-01.md` 至 `AC-06.md` 及 SHA-256 清单。

用一致的 Gitee Skill 版本解压并校验：

```bash
TASK_DIR=/path/to/native-doc/version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4
cd /path/to/common-develop-opt

python scripts/long_task.py validate -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
python scripts/wk.py next -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
```

随后将需求确认稿、当前 Revision、真实 Evidence 与 6 个 **未填写的** Review 表单交给独立的 `RequirementAnalysisAgent`。Reviewer 应先核验内容和证据、提出需要的 Issue，再按自己的真实独立判断提交；不能预选 PASSED。需要填写和提交表单时以本版本原生命令帮助为准：

```bash
python scripts/manual_review.py submit -g RequirementAnalysisAgent --task-dir "$TASK_DIR" --review-file /path/to/review-forms/AC-01.md
```

通过所有原生 Review 后才允许按真正原生流程 `finalize-phase` 并 `advance-phase`。然后依次完成需求分析、业务建模、设计及后续全部 Standard 阶段，再检验固定 DEC 三 Provider 正向消费并回传 Evidence。勿修改历史 events 或把 Owner PASSED 改写为 Review PASSED。

## 当前剩余问题

- 六项独立 Manual Review 尚未执行；
- 正式 `STAGE_OUTCOME_FINALIZED requirement_confirmation/PASSED` 不存在；
- 尚未推进 `requirement_analysis` 和 `design`；
- 正向 Native Gate→DEC 和开发/代码审查/测试/归档证据仍缺失。

详见 [Issue #1](https://github.com/szlwin/common-develop-dec-integration/issues/1)。本进展不改变 `docs/P0-acceptance.md` 的 P0 总体 BLOCKED 状态。
