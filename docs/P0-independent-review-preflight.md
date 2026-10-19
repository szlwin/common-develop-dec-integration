# P0 Requirement Confirmation — independent Review preflight (unapproved)

> **Status: PRE-REVIEW ONLY / INDEPENDENT REVIEW REQUIRED.** This analysis was made in the existing Owner conversation, so it **must not** be treated as a genuine `RequirementAnalysisAgent` approval or submitted as PASSED. It cannot unblock native `finalize-phase`.

## Verified state (2026-10-19)

From the previously exported, SHA-verified native task `FEATURE-DESC-DAE4FAB5F9F4` and the exact upstream Gitee common-develop-opt source commit `b26715f6779b373b4f840b519ba9725fed5d789a`:

- Original ZIP manifest matches. Native `long_task.py validate` returns `PASSED` (ledger/schema consistency only).
- Native `wk.py next`: `status=READY`, `classification=REVIEW_REQUIRED`, `requiredAgent=RequirementAnalysisAgent`, `executionContext=ISOLATED_REVIEW_SESSION_REQUIRED`.
- Events: `ATTEMPT_STARTED` (1), `ATTEMPT_FINISHED` (1), `STAGE_OUTCOME_PUBLISHED` (1), **`STAGE_OUTCOME_FINALIZED` (0)**. Other events are `TASK_STATE_PATCHED`.
- Six native `AC-01` through `AC-06` Review forms remain unanswered (`无法判断`). Their single profile question is the same `MRQ-SCOPE` prompt, even though the Acceptance IDs cover six different P0 capabilities.
- Owner Attempt **PASSED** and requirement artifact **PUBLISHED** are not independent Review **PASSED**. The native phase must stay pending.

## Findings requiring independent Reviewer judgment

| ID | Priority | Finding and requested validation |
|---|---|---|
| PF-01 | Blocking | There is no genuinely isolated RequirementAnalysisAgent review session/provenance yet. The originating Owner context cannot self-submit six Review forms as independent Reviewer. |
| PF-02 | Medium | All six AC forms ask only the same generic Scope question. This may be valid for the phase's Review profile, but does not establish independent verification of AC-01..AC-06's different *end-to-end* obligations. Require a future-stage evidence/acceptance mapping. |
| PF-03 | Medium | Requirement confirmation cites `a6961def87860d3cc1a7ecd1c67595b857b664b7077dc527207d9556610e1660` as canonical DEC tree digest without specifying the path-sorted hash-of-hashes recipe, exclusions or version. Verify unambiguous source→revision binding and mutation invalidation. |
| PF-04 | Medium | The downstream handback of Java, Binding and JUnit evidence to native `test_design`, `implementation_plan`, `development`, `code_review`, `testing`, `completion_verification` lacks an exact per-phase consumer/input revision/Evidence mapping. |
| PF-05 | Medium | The pinned native Standard canonical phase sequence does not have a separate `tdd` phase. Demand verifiable RED/GREEN/REFACTOR evidence within its supported work/phase rules, not a fabricated `tdd` StageOutcome. |
| PF-06 | Low | Explicitly preserve the boundary between P0 integration acceptance and product release (4 Design IDs PLANNED, plus simulated payment/MongoDB/SMS adapters). |

These findings are **preliminary review questions**, not official native Issue/Review records. An isolated reviewer must independently inspect sources, decide each answer, record legitimate Issues/revisions where needed and run official `manual_review.py submit` from their own authorized environment.

## Actual reviewer execution handoff

The full native task ZIP and original pinned source ZIP are supplied as separate download artifacts in the conversation. In a truly new isolated Reviewer session, verify SHA256SUMS and original CLI status, read canonical current-revision `requirement_confirmation.md`, Evidence EVD-000001/2 and the six unaltered forms. Use:

```bash
TASK_DIR=/trusted-workspace/native-doc/version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4
cd /trusted-workspace/common-develop-opt
python scripts/long_task.py validate -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
python scripts/wk.py next -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
python scripts/manual_review.py show -g RequirementAnalysisAgent --task-dir "$TASK_DIR"
```

Only after actual independent review of each acceptance scope may the reviewer complete appropriate forms and call `manual_review.py submit -g RequirementAnalysisAgent --task-dir "$TASK_DIR" --review-file ...`. If review finds inadequate scope/evidence, use official issue/revision pathways to return the draft to Owner. Do not edit historical `task_events.jsonl` or reuse Owner context.

**Issue #1 remains OPEN; P0 remains BLOCKED.** [P0 acceptance ledger](P0-acceptance.md) and [native Requirement Review handoff](P0-requirement-review-handoff.md).
