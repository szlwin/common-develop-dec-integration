# P0 Requirement R02 技术复查及剩余整改（2026-10-20）

> **结论：NEEDS_CHANGES / BLOCKED_INTEGRITY。** 本文件是对现有 GitHub 独立内容 Review 及其 R02 Owner 返修的进一步核查，不是新的独立原生 Review，也不是 PASSED 或 \`STAGE_OUTCOME_FINALIZED\`。原独立 Review 报告仍保留历史，不改写。

## 1. GitHub 当前事实

截至本次复查，GitHub main 上的独立审查仍为 [2026-10-19 NEEDS_CHANGES](P0-REQUIREMENT-CONFIRMATION-INDEPENDENT-REVIEW-20261019.md)，之后为 [2026-10-20 Owner R02 返修说明](P0-REQUIREMENT-CONFIRMATION-OWNER-REMEDIATION-20261020.md)。未发现单独签署的 R02 原生 Review、Review PASSED 或任何 \`requirement_confirmation\` finalized/PASSED StageOutcome。Issue #1 必须保持 OPEN。

## 2. 复查 R02 真实原生 ZIP 发现的额外缺陷

对会话上传的 \`p0-requirement-r02-native-review-handoff.zip\` **只读**解压并以固定 Gitee \`common-develop-opt\` CLI 重新验证：

| 检查项 | 实际结果 |
|---|---|
| \`long_task.py validate\` | PASSED（结构规则，并未验证以下跨文件等价） |
| \`wk.py next\` | REVIEW_REQUIRED / ISOLATED_REVIEW_SESSION_REQUIRED |
| 正式新需求 MD SHA-256 | \`b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2\` |
| R02 发布 Revision | \`REQCONF-P0-R02@sha256-b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2\` |
| \`traceability.json\` 中 \`TR-P0-REQCONF-001.requirement_source_digest\` | **仍为 R01**：\`130eb2a1a3d5b74f175755101737fe5b74a25e8fdee33665158af514a16a7db4\` |
| \`task_plan.json\` 中 \`TASK-REQCONF-P0-001.iteration_id\` | **仍为 001**，而当前 Attempt/StageOutcome 是 002；暂视为需原生确认的任务迭代归属疑点，不能直接以此自行改写计划 |
| \`risk.json.status\` | **NOT_SCANNED** |
| R02 的 AC-01..AC-06 | **全部 PENDING** |
| R02 \`STAGE_OUTCOME_FINALIZED\` | **0** |

**新增发现 R-08（高，阻断独立 Review 前置核对）：** 需求实际字节与原生 Trace 中被引用的需求 SHA 不一致。当前的 \`long_task validate\` 返回 PASSED 并不能证明此跨文件追溯一致。不能把 R01 Trace/Evidence 错误地作为 R02 有效链接，也不能填写六项 AC 为 VERIFIED。

**R-05/R-06 尚有遗留**：原 Task Plan 以历史工作目录相对路径验证，新工作目录必须使用绝对 \`--task-dir\`；risk scan 在此固定版本中要求开发阶段 Revision，现时不能伪称扫过。独立 Reviewer 应判断是否可在后续阶段处理并设定阻断条件。

## 3. 本次已实施的代码修复

- 新增 [\`scripts/check_requirement_review_handoff.py\`](../../scripts/check_requirement_review_handoff.py)：只读查验 **当前正文原始 bytes / 原生发布 Revision / Evidence 快照 / Owner Attempt / 六条当前 Review Assertion / Trace SHA / 风险扫描状态**。遇到本次 R02 数据返回 \`BLOCKED_INTEGRITY\` 并列出 \`STALE_REQUIREMENT_TRACE_DIGEST\`，不会创建审批、修改 Task Plan 或写入事件账本。
- 新增 [\`tests/test_requirement_review_handoff.py\`](../../tests/test_requirement_review_handoff.py) 的正向待审边界与负向回归：旧 Trace、文档篡改、旧修订 Assertion、Outcome supersede 均不能绕过检查。
- 加固 [\`scripts/native_gate.py\`](../../scripts/native_gate.py)：正式 Design/PASSED 之后如出现 \`STAGE_OUTCOME_SUPERSEDED\`、包含 design 的 \`PHASE_STALE\`、或新的未批准 Design \`STAGE_OUTCOME_PUBLISHED\`，拒绝继续使用旧 StageOutcome。
- 加固 [\`scripts/build_native_review_packet.py\`](../../scripts/build_native_review_packet.py)：检查固定 DEC checkout 中 canonical YAML 有无本地修改、未追踪文件及超出审核范围的额外文件；不再仅依据 \`git rev-parse HEAD\` 推断工作目录纯净。

## 4. 如何复现与正式修复

在只读、可信任的解压目录中执行：

\`\`\`bash
SKILL_ROOT=/trusted/common-develop-opt
DOC_ROOT=/trusted/native-doc
TASK_DIR="$DOC_ROOT/version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4"
REQ_FILE="$DOC_ROOT/version/V_P0/requirement/FEATURE-DESC-DAE4FAB5F9F4/requirement_confirmation.md"

python scripts/check_requirement_review_handoff.py \
  --task-dir "$TASK_DIR" --requirement "$REQ_FILE" --skill-root "$SKILL_ROOT"

python "$SKILL_ROOT/scripts/long_task.py" validate \
  -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
python "$SKILL_ROOT/scripts/wk.py" next \
  -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
\`\`\`

**必须真实更正的原生任务状态**：由合法 Owner/ProjectManager 按官方 Reopen/Amendment、当前 Task Plan 与 Trace 同步流程处理 R-08，并产生内容与 Trace 共同一致的新、可审核 Revision 及 Evidence，再提交新隔离 Reviewer。不得直接编辑已经发布的 R02 记录/旧 Event，并说仍旧通过。当前固定 Skill 的 \`requirement_doc.py sync-traceability --dry-run\` 对 R02 的非标准 \`requirement_confirmation.md\` 返回格式校验错误（缺正式规范的章节/元数据等）；因此此流程尚未能合法完成，若要使用它，需要先将当前文档转换为满足官方 \`requirement.md\` 规范的新修订，**不能**把重命名或单纯改 JSON 当作原生 Review。

完成后独立 \`RequirementAnalysisAgent\` 检查并按正式原生命令提交，最后按真实 Gate \`finalize-phase\`。所有阶段仍须来源、Revision、Review 和 Evidence 一致。当前 **P0 BLOCKED**；不进入 P1，也不宣称生产发布就绪。
