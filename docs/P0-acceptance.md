# P0 acceptance ledger — 2026-10-18

## Audit and corrections

Original P0 commit: cc76aca55f93797f36117ae144cd7c8e9e5aaffb.
Initial CI run [#39118665593](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39118665593) failed because PyYAML was not installed.

P0-1: CI now uses version-pinned PyYAML==6.0.2 and jsonschema==4.23.0.
P0-2: [#39141480949](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39141480949) succeeded in BOTH unit and demo-fixed-providers. DEC source was pinned at 4fb21242498746365c201fdf2a7fd8052f3a122a. The real DEC YAML/XML/HTML/Java generation/Maven/Binding/test-evidence chain ran with an explicitly synthetic upstream Gate. Its logs and test evidence are CI artifacts.
P0-3 (partial): The exact Gitee common-develop-opt source has been queried via read-only GitHub Actions checkout, SHA b26715f6779b373b4f840b519ba9725fed5d789a. We now verify the native long_task validate CLI AND append-only task-events; only a latest finalized PASSED design StageOutcome with matching revision/producer can serve as a native handoff. An empty native task that passes schema validation must be rejected.
P0-4: A separate artifact-manifest.json provides the SHA-256 input dependencies and the upstream workflow revision for DEC artifacts, rather than duplicating design facts.
P0-5: Tests cover false finalization, changed revision, wrong producer, invalid Skill identity and failed/stale validation. CI runs the real opt CLI on an unapproved disposable task to confirm it cannot unlock design.
P0-6: this ledger records what is verified versus not.

## Acceptance matrix

| Requirement | Current conclusion |
| --- | --- |
| Repository / Integration Skill / three fixed DEC Providers | PASSED |
| Fixed DEC provider chain on real order-payment Demo | PASSED at pinned DEC baseline (CI #39141480949) |
| Artifact lineage | IMPLEMENTED; latest CI evidence must be checked |
| Negative Gate scenarios and native CLI blocking | IMPLEMENTED; latest CI evidence must be checked |
| True common-develop-opt design Review and StageOutcome | NOT VERIFIED: no approved native task directory was provided |
| Complete requirement → design → TDD → test dual-Skill workflow | NOT VERIFIED |
| Both upstream Skill standalone regression suites | **PASSED** — [native 360, dec-design 80, dec-implementation 24, Java Maven](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39146485409) |
| Product Release Gate | NOT READY; upstream Demo has 4 PLANNED design IDs |

**P0 final acceptance: BLOCKED / PARTIALLY IMPLEMENTED.** Successful fixture-based DEC CI is not full dual-Skill acceptance.

## Requirements for a true positive native handoff

Run common-develop-opt's own authorized Agent workflow and independent Review until its genuine design finalize-phase records a PASSED StageOutcome, with its current task-event ledger. Bind that exact output_revision to the approved DEC YAML digest in an immutable handoff Gate. Invoke the adapter with --gate, --native-opt-root and --native-task-dir and collect native validate/task-events logs, Artifact manifest, all DEC commands, real JUnit reports and Binding evidence. Regress each independent Skill. Review all evidence before changing this P0 verdict; preserve productReleaseReady independently (four PLANNED IDs remain).

Do not edit upstream canonical DEC YAML/XML to make integration checks pass. No fixture or actor-name switch is a real independent Review.


### Review of 2026-10-19 and additional hardening

The independent re-review confirmed CI 21/21 adapter tests and 34/34 JUnit with real DEC generated code/Binding, but no native approved design handoff. To avoid treating arbitrary revision labels as a provable native→DEC design mapping, the native positive path now requires `output_revision = sha256:<DEC-tree-digest>`, checked against bytes. Historical finalized events are invalid after a later reopen/invalidation. This strengthens admission correctness but does **not** create the missing independent Review or full native-positive run. Overall P0 remains **BLOCKED** until real native approval evidence is supplied and exercised.


### Native-positive workflow prepared (not run with approved inputs)

A manual-only [P0 native approved Gate to DEC](../.github/workflows/p0-native-positive.yml) workflow was added, with corresponding [positive evidence checker](../scripts/check_native_positive_evidence.py), negative tests and [real approval runbook](native-positive-runbook.md). It verifies the actual upstream CLI + content-addressed design approval followed by all DEC providers. **No independently reviewed positive native task or Gate has been supplied or run as of this update. The overall P0 decision is unchanged: BLOCKED / PARTIALLY IMPLEMENTED.**


## 2026-10-19 — standalone regression verified

Original audit finding P0-5 requested regressions of the two upstream Skills separately, not just the integration's Demo. A new standalone workflow now checks exact source baselines independently:

- **common-develop-opt** from Gitee commit `b26715f6779b373b4f840b519ba9725fed5d789a`: Python 3.9, **360/360 native tests PASSED**. Test discovery uses the upstream `tests/` directory and explicitly installs `jsonschema` and PyYAML. The first attempts failed due to incorrect test discovery and missing StageResult schema dependencies; the corrected CI succeeds.
- **dec-design** from GitHub commit `4fb21242498746365c201fdf2a7fd8052f3a122a`: **80/80 Python tests PASSED**, independently of the integration runner.
- **dec-implementation** at the same pin: **24/24 Python tests PASSED** independently.
- **dec-java-lite** at the same pin: **the complete standalone Maven Reactor test job PASSED** on Java 21 (MySQL test service configured).

Evidence: [GitHub Actions run #39146485409](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39146485409), all three jobs successful.

### Native revision compatibility finding

The public Gitee `publish-artifact` implementation reads the published revision from the current **PASSED task Attempt's `output_revision`**, not a caller-provided arbitrary Gate JSON. `finalize-phase` additionally requires a published current artifact, completed tasks, real evidence, Review pass where required, no blocking issues, and traceability free of GAP/STALE. Consequently the proposed content-addressed design revision must be established **during the native Attempt and its real approval**, not retrofitted by Integration. This confirms the handoff design path, **not** successful acceptance of that precise revision format in a completed real approved task.

### Remaining P0 blocker

The verified independent regression closes the testing gap in P0-5. However **no genuine order/payment common-develop-opt task with an independent design Review and finalized PASSED StageOutcome was provided or generated**. The manual-only positive workflow is ready but **has not run against authentic approved evidence**. End-to-end Requirement → Design Review → DEC → TDD/Code Review/Testing and archival handoffs therefore remain **NOT VERIFIED**. A CI fixture must never be used to upgrade P0 acceptance. Final P0 decision remains **BLOCKED / PARTIALLY IMPLEMENTED**. Product Release remains NOT READY because of the four PLANNED IDs.


## 2026-10-19 — authentic design Review candidate prepared (not approved)

The exact fixed-version DEC design can now be exported as a **content-addressed, unapproved** Review candidate using `scripts/build_native_review_packet.py` and [the candidate workflow](../.github/workflows/p0-review-candidate.yml).

- **Source design:** pinned upstream DEC commit `4fb21242498746365c201fdf2a7fd8052f3a122a`, exactly 10 canonical order/payment YAML files.
- **Execution evidence:** [candidate-generation Actions #39147972411](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39147972411) passed; its downloadable artifact is named `p0-native-unapproved-design-review-candidate`.
- **Candidate status:** `AWAITING_INDEPENDENT_NATIVE_REVIEW`; `approved=false`; `nativeStageOutcomeId=null`. Neither this job nor a SHA hash constitutes an independent Review.
- **Scope and genuine prerequisites:** [order-payment native design Review specification](P0-native-design-review.md).
- **Tracking:** [P0 authentic Review + full lifecycle blocker #1](https://github.com/szlwin/common-develop-dec-integration/issues/1).

The real approved upstream task, independent Reviewer execution, native PASSED StageOutcome, and subsequent lifecycle handoffs are still **missing**, so **P0 overall remains BLOCKED**. No credentials or private tasks should be published to the public repository.


## 2026-10-19 — genuine native task created; official first-stage Gate still BLOCKED

A **real** `common-develop-opt` task was created through its official `wk start --apply` CLI (not manually constructed). A genuine `task_events.jsonl` exists for `FEATURE-DESC-DAE4FAB5F9F4`. The official `wk begin --apply` returns `BLOCKED / EXECUTION_REQUIRED`, required Agent `RequirementConfirmationAgent`, reason `ARTIFACT_NOT_PUBLISHED`, with next legal `long_task.task-context` and `long_task.start-attempt`. This is the native lifecycle correctly rejecting advancement before a PASSED requirement-confirmation attempt and Artifact. There is no Review approval or design StageOutcome.

**Native evidence:** [Actions #39150138291](https://github.com/szlwin/common-develop-dec-integration/actions/runs/39150138291) (passed kickoff), artifact `p0-real-native-unreviewed-task` containing the authentic native task directory, event ledger and two CLI JSON responses. [How to resume authentic native execution](P0-native-task-handoff.md); [Issue #1](https://github.com/szlwin/common-develop-dec-integration/issues/1) remains OPEN. Overall P0 is still **BLOCKED**; do not equate `CREATED` or `EXECUTION_REQUIRED` with a PASSED design Gate.

## 2026-10-19 — RequirementConfirmationAgent real Attempt and official published handoff

The previously created task `FEATURE-DESC-DAE4FAB5F9F4` was resumed from its authentic CI evidence and checked against the exact Gitee source `b26715f6779b373b4f840b519ba9725fed5d789a`. The existing task had no plan tasks. A genuine, pending `task_plan.json` entry was authored for `TASK-REQCONF-P0-001`, along with the actual requirements confirmation Markdown. The original `long_task validate` accepted this plan.

The **original native CLI** then ran:
- `long_task task-context` for the actual Task ID;
- `long_task start-attempt` -> `ATTEMPT-TASK-REQCONF-P0-001-I001-A001`, RUNNING;
- `evidence snapshot-register` -> `EVD-000001`, immutable requirement Markdown snapshot;
- `long_task finish-attempt --auto-evidence` -> **owner Attempt PASSED**, command Evidence `EVD-000002`;
- the real Trace `TR-P0-REQCONF-001` mapped six Acceptance IDs `AC-01`…`AC-06` to the owner Task. All Trace/Review approvals remain PENDING;
- `acceptance ensure-review` registered six **PENDING** `MANUAL_REVIEW` assertions for `RequirementAnalysisAgent`;
- `long_task publish-artifact` -> **PUBLISHED**, StageOutcome ID `SO-FEATURE-DESC-DAE4FAB5F9F4-REQUIREMENT_CONFIRMATION-I001`, and phase Revision `REQCONF-P0-R01@sha256-130eb2a1a3d5b74f175755101737fe5b74a25e8fdee33665158af514a16a7db4`;
- `long_task validate` -> PASSED (runtime structural integrity only);
- `wk next` -> `REVIEW_REQUIRED`, `requiredAgent=RequirementAnalysisAgent`, `executionContext=ISOLATED_REVIEW_SESSION_REQUIRED`, `ownerContextReuseAllowed=false`.

**Important status distinctions:** Owner Attempt PASSED is **not** independent Review PASSED. The StageOutcome is **PUBLISHED/RUNNING**, not `STAGE_OUTCOME_FINALIZED`. No Design StageOutcome exists; neither positive DEC native handoff nor complete P0 is verified. Review forms are prepared but **not submitted**. No P1 work has started.

The authentic source and review handoff archive was generated separately for download in the task conversation, with six default-unanswered Review forms, the original append-only ledger, source snapshots, and checksums. [Exact review-handoff procedure](P0-requirement-review-handoff.md) and [P0 blocker Issue #1](https://github.com/szlwin/common-develop-dec-integration/issues/1) describe the isolated Reviewer boundary. **P0 still BLOCKED.**


## 2026-10-19 — native Requirement Review preflight (NOT approval)

The authentic published owner handoff was restored from its ZIP and checked with the **original pinned native CLI**. `long_task validate` is PASSED for structure, while `wk next` still requires an actually isolated `RequirementAnalysisAgent` session for `requirement_confirmation`. The append-only event ledger contains exactly one `STAGE_OUTCOME_PUBLISHED` and **zero `STAGE_OUTCOME_FINALIZED`**. Six native Review forms are still unanswered.

The pre-review uncovered specific questions about the six ACs using one generic Review prompt, the tree-hash mapping algorithm, per-native-phase DEC Evidence handback, and TDD mapping to the original canonical phases. These are not independently adjudicated Findings or Review approvals. [Full preflight](P0-independent-review-preflight.md) and [Issue #1](https://github.com/szlwin/common-develop-dec-integration/issues/1) track the remaining handoff.

**Current requirement_confirmation: Owner PASSED / Artifact PUBLISHED / independent Review PENDING / StageOutcome not finalized. P0 overall BLOCKED.**
