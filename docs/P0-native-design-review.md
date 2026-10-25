> **现行验收范围说明（2026-10-25）**：本文原先按照完整订单支付软件 Standard E2E 作为 P0 必做条件编写；该产品层范围已被用户明确澄清并由 [Skill P0 A+B 验收矩阵](P0-skill-scope-governance-20261025.md) 取代。完整业务软件 Standard E2E 已独立列为 [可选 Issue #2](https://github.com/szlwin/common-develop-dec-integration/issues/2)。**此注记不免除任何已经在真实原生 Standard 任务中生效的 Gate/Review/TDD/测试要求**；历史文字和审批记录保留审计。Skill Design 与 DEC Demo Design 不能互用一个 Reviewer/Revision，详见 [双来源绑定契约](dual-source-design-binding.md)。**P0 仍 BLOCKED。**

# P0 Native Design Review — unapproved candidate

**Status: AWAITING INDEPENDENT NATIVE REVIEW.** This is an acceptance work item, not proof that P0 is done.

## Exact design to review

DEC repository: [doc-eq-code-Dgremlin-skills](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/tree/4fb21242498746365c201fdf2a7fd8052f3a122a/demo/order-payment-yaml)

Pinned source commit: `4fb21242498746365c201fdf2a7fd8052f3a122a`

Canonical design: 10 YAML sources; five API definitions, 19 Information nodes and complete order/payment Directory. The upstream DEC Demo contains 111 Design IDs (107 VERIFIED, 4 PLANNED). The 4 PLANNED nodes do not block P0 integration but **must block Product Release**.

The Demo uses local substitutes for external payment provider, MongoDB and SMS; it is **not** a production payment integration. The native design Reviewer should explicitly acknowledge these scope boundaries and review the actual canonical YAML, API requests/responses, data effects, payment success/failure/back transitions, idempotency and transaction limits described in [upstream Demo README](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/blob/4fb21242498746365c201fdf2a7fd8052f3a122a/demo/order-payment-app/README.md).

[Review candidate CI](../.github/workflows/p0-review-candidate.yml) creates a machine-readable digest manifest from the exact pinned upstream YAML. The artifact is deliberately marked **unapproved** and has no StageOutcome ID.

## Required original common-develop-opt execution

Use pinned Gitee `common-develop-opt` source commit `b26715f6779b373b4f840b519ba9725fed5d789a`. Run its actual task stages (`requirement_confirmation` → `requirement_analysis` → `business_model` → `design`) with real user decisions and independently reviewed design. Do not bypass or manufacture phases. The design artifact's native PASSED Attempt must publish `output_revision = sha256:<digest from the candidate>` using its official `publish-artifact` command, followed by genuine Review and `finalize-phase`. The content digest must describe what reviewers actually read **before** approving it.

Independent Review must supply real issue closure, output revision binding, evidence IDs and upstream requirement input revisions, not just reviewer names in custom JSON.

Only then use [native-positive-runbook](native-positive-runbook.md) to export the actual task directory, write its read-only Handoff Gate index, run [native-positive CI](../.github/workflows/p0-native-positive.yml), and check the resulting native CLI/DEC/JUnit logs and Artifact trace manifest.

## Full lifecycle closure

After the design handoff succeeds, continue native TDD, Development, Code Review, Testing, Completion Verification and archive using original official commands and meaningful DEC outputs. Record corresponding native Artifact / StageOutcome references and test IDs. The integration itself does not currently auto-drive these stages.

**Current P0 Gate: BLOCKED.** Preparation of a Review candidate does *not* imply genuine approval, and must never change the P0 acceptance ledger to PASSED.
