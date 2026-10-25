> **现行验收范围说明（2026-10-25）**：本文原先按照完整订单支付软件 Standard E2E 作为 P0 必做条件编写；该产品层范围已被用户明确澄清并由 [Skill P0 A+B 验收矩阵](P0-skill-scope-governance-20261025.md) 取代。完整业务软件 Standard E2E 已独立列为 [可选 Issue #2](https://github.com/szlwin/common-develop-dec-integration/issues/2)。**此注记不免除任何已经在真实原生 Standard 任务中生效的 Gate/Review/TDD/测试要求**；历史文字和审批记录保留审计。Skill Design 与 DEC Demo Design 不能互用一个 Reviewer/Revision，详见 [双来源绑定契约](dual-source-design-binding.md)。**P0 仍 BLOCKED。**

# P0 原生任务交接 — 实际 `wk start` / `wk begin` 结果

## 可复现的原生事实

固定原生 Skill：Gitee `common-develop-opt` 提交 `b26715f6779b373b4f840b519ba9725fed5d789a`。

真实工作流调用：`scripts/wk.py start -g ProjectManagerAgent --doc-root <DOC_ROOT> --version V_P0 -f <FEATURE> --classification new-requirement --no-auto --apply --json`。

真实返回：`status=CREATED`、退出码 `0`，生成了 append-only `task_events.jsonl`。任务：`version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4`。证据：[Actions #39150138291](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39150138291)，产物 `p0-real-native-unreviewed-task`。

随后执行正式 `wk begin --apply --json`。原生返回 `BLOCKED / EXECUTION_REQUIRED`，原因 `ARTIFACT_NOT_PUBLISHED`。这不是测试故障，而是 **requirement_confirmation 阶段尚未产生 PASSED Attempt / 正式 Artifact**。

- 当前阶段：`requirement_confirmation`
- 必需执行 Agent：`RequirementConfirmationAgent`
- 该阶段需要的独立 Reviewer：`RequirementAnalysisAgent`（来自原生 `contractQueries.phase.requiredReviewerAgents`）
- 允许下一步：`long_task.task-context`、`long_task.start-attempt`
- `requiresUserDecision=false` 只是说明当前可以由 Agent 开始阶段执行，**不是**表示用户已批准需求或 Reviewer 已审核。

## 实际下一条命令

将 Actions 产物 ZIP 解压到可信任的独立工作目录，取得其中的 `native-doc`。使用匹配的原生 Skill 源码：

```bash
TASK_DIR=/path/to/native-doc/version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4
cd /path/to/common-develop/skills/common-develop-opt

python3 scripts/long_task.py task-context \
  -g RequirementConfirmationAgent --task-dir "$TASK_DIR" --json
```

然后以返回的真实 `task-id`、当前 Revision 和 `actionPlan` 为依据，由 **RequirementConfirmationAgent** 使用 `start-attempt` 开始产物制作，引用固定 DEC 源码 `4fb21242498746365c201fdf2a7fd8052f3a122a` 及其目录摘要 `a6961def87860d3cc1a7ecd1c67595b857b664b7077dc527207d9556610e1660`。必须完成必要的真实需求澄清、风险与测试范围，不能用已有 DEMO 的 CI 结果替代需求确认。

由原生授权角色在独立上下文执行正式 Review、解决问题、发布 Artifact，再经官方 `finalize-phase` 形成可核验的 StageOutcome。**不得手工修改 `task_events.jsonl`、StageOutcome、Review 状态或用另一个名字假扮独立 Reviewer**。

完整 Standard 原生正式阶段（从固定 Gitee `runtime-contract.json` 核对）：

```text
requirement_confirmation → requirement_analysis → business_model → design
→ test_design → implementation_plan → development → code_review
→ testing → completion_verification → 原生归档/收尾
```

完成 `design/PASSED` 后还需验证输出 Revision 与经过审核的 DEC 内容摘要精确一致，执行 [正向 Gate → DEC CI](../.github/workflows/p0-native-positive.yml)。随后将 DEC 代码、Binding、JUnit 证据按原生任务的阶段规则回流至测试和验收，最终才可考虑关闭 Issue #1。

## 当前结论

`REAL_NATIVE_TASK_UNREVIEWED`。目前已真实创建任务、完成 `wk begin` 的阶段分派，并验证原生阻断正常；**未完成 Requirement Review、Design Review、DEC 正向联调或完整生命周期验收**。不能改变 `P0 BLOCKED`。

注意：CI Artifacts 有保留期限。只有在没有密码、Token 或业务敏感数据时，才可将脱敏任务移交给公开仓库；否则使用私有工作空间保留完整 doc-root。
