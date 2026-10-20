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


## 2026-10-19 — read-only reviewer evidence crosswalk (no new approval)

Original owner-stage task and six blank AC forms were restored and verified using the exact pinned Gitee Skill. The original 27-entry SHA-256 manifest matches. Fresh `long_task validate` = PASSED (structural integrity), `wk next` = REVIEW_REQUIRED / ISOLATED_REVIEW_SESSION_REQUIRED, and all six manual assertions remain PENDING. **There are 0 STAGE_OUTCOME_FINALIZED events**. An updated self-contained handoff packet, containing the untouched original native task and Skill ZIPs, native CLI outputs, per-AC evidence matrix, digest specification and README, has been supplied in the conversation. This is not a StageOutcome or Review result.

Additional Reviewer concern **PF-07**: the historical task's validation command references `../native-doc/...` relative to `/mnt/data/p0-native-stage-work/opt-pinned`, which is valid only for that source-run layout and cannot be used unchanged in a separately restored environment. Run portable read-only CLI commands with an explicit absolute `--task-dir`; any change to the canonical Task Plan must follow native amendment/version rules. See [detailed AC-01..AC-06 evidence and downstream phase crosswalk](P0-requirement-review-crosswalk.md), including the exact DEC tree hashing algorithm and absence of a separate canonical `tdd` StageOutcome in the pinned native Standard workflow.

**Current native requirement_confirmation remains Owner PASSED / Artifact PUBLISHED / independent Review PENDING; P0 remains BLOCKED.** The only approval-capable next step is an actual independent RequirementAnalysisAgent session reviewing the current revision.


## 2026-10-20 — independent contents Review NEEDS_CHANGES, genuine Owner R02 rework PUBLISHED

The independent contents review [2026-10-19 NEEDS_CHANGES](reviews/P0-REQUIREMENT-CONFIRMATION-INDEPENDENT-REVIEW-20261019.md) found R-01..R-06 substantive gaps and R-07 absence of the formal isolated Reviewer gate. These issues were **not** passed through the native `manual_review.py`.

The Owner resumed the **original task** `FEATURE-DESC-DAE4FAB5F9F4` on a restored copy of the authenticated pinned Gitee Skill. It used the original official `long_task reopen-phase` command to create `requirement_confirmation` Iteration 002 and invalidate all downstream stages, preserving R01's published-but-not-finalized history and `EVD-000001/000002`. A completely reworked canonical `requirement_confirmation.md` in the new iteration documents deterministic DEC SHA-256 tree hashing, Design output revision and invalidation policy, native ten-stage/DEC Artifact handback, TDD RED/GREEN/REFACTOR subgate ownership, six differentiated AC criteria, and security/credential/cross-module risk assessments.

**New native facts:**
- Owner Attempt `ATTEMPT-TASK-REQCONF-P0-001-I002-A001` finished **PASSED** via the official CLI.
- Current requirement Revision `REQCONF-P0-R02@sha256-b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2`.
- `EVD-000003` is the exact new requirement snapshot; `EVD-000004` is the actual owner command Evidence.
- Current `SO-FEATURE-DESC-DAE4FAB5F9F4-REQUIREMENT_CONFIRMATION-I002` is **PUBLISHED**, not FINALIZED/PASSED. R01's old outcome was **SUPERSEDED** by the genuine native reopen event.
- All six newly registered current-revision manual Review assertions remain **PENDING**; `wk next` returns `REVIEW_REQUIRED / ISOLATED_REVIEW_SESSION_REQUIRED`; no `STAGE_OUTCOME_FINALIZED` exists.
- The original `task_plan.json` history still contains a non-portable relative validation command. The reviewer must use an absolute task path on restoration. The original `risk.json` remains `NOT_SCANNED`; the native `risk_detect.py scan` cannot run at requirement_confirmation without a development Revision. These remain disclosed review/phase risk items, not silently waived.
- The self-contained **R02 native task and Review handoff ZIP** was generated in the conversation and its ZIP integrity checked; its 34-file SHA256SUMS and six blank reviewer forms are available to the isolated Reviewer.

[Full R-01..R-07 Owner remediation disposition](reviews/P0-REQUIREMENT-CONFIRMATION-OWNER-REMEDIATION-20261020.md). **Current Phase: Owner PASSED / Artifact PUBLISHED / isolated Review PENDING**. **P0 Overall BLOCKED**, Issue #1 OPEN, no Product Release permission and no P1.


## 2026-10-20 — R02 new cross-file consistency finding and fail-closed code repair

Independent GitHub contents Review is still 2026-10-19 `NEEDS_CHANGES`; R02 is Owner PUBLISHED, not independently PASSED. A read-only exact-Task replay found **R-08 STALE_REQUIREMENT_TRACE_DIGEST**: the current R02 content SHA-256 is `b0ae33da8cc4d416cd012eeebfa450239a46c8ee09bf2a631e685f9727bc40d2`, but `TR-P0-REQCONF-001.requirement_source_digest` still says R01 `130eb2a1a3d5b74f175755101737fe5b74a25e8fdee33665158af514a16a7db4`. Original native structural `validate=PASSED` does not catch this equality gap. New `check_requirement_review_handoff.py` now **fails closed** for the R02 task; stale/superseded Design StageOutcome checks and dirty-pinned-DEC checks are added as well. `risk.json` remains NOT_SCANNED; native Task Plan references its old iteration. No native events, approvals or original sources were rewritten. [Full reproducible findings](reviews/P0-R02-TECHNICAL-RECHECK-20261020.md); P0 still **BLOCKED** until legitimate native rework, fresh independent Review and full lifecycle approval.


### Enforcement refinement — real positive handoff also checks R-08

Starting at commit `83bdfdfd9ea9dd5bd5991fa011a54b9d0624ced5`, the actual `native_gate.validate_native_with_runner` path (not just the optional handoff preflight script) verifies `TR-P0-REQCONF-001.requirement_source_digest == SHA256(current requirement_confirmation.md bytes)`. A stale R01 Trace on the published R02 requirement makes the real native Design Gate **fail closed**, even when upstream structural `long_task validate` reports PASSED. A negative regression test covers both stale and correctly bound trace digests. This is a **code-level guard, not a native approval**. Official Task Record rework and isolated Review remain outstanding.


## 2026-10-21 — correction to R-08 gate timing, verified against pinned native contract

The original [R02 technical recheck](reviews/P0-R02-TECHNICAL-RECHECK-20261020.md) correctly identified a current requirement source digest mismatch, but its wording that this **automatically blocks `requirement_confirmation` content Review** was too strict. The pinned Gitee native contract expressly places `requirement_doc.py sync-traceability` **after requirement-analysis validation**, as part of `requirement_analysis` (see `scripts/document_core/requirement_doc.py:command_sync_traceability` and `references/core/lifecycle-core.detail.md`). The native requirement confirmation gate judges scope and semantics, not completed test/trace execution.

**Corrected enforcement (commit `56ef90a69003056fa739cd884541e549a1d89435`):**
- The read-only `check_requirement_review_handoff.py` reports the stale R01 digest as `TRACE_SYNC_REQUIRED_IN_REQUIREMENT_ANALYSIS` **warning** while independently checking R02 content bytes, immutable Evidence, current Owner Attempt and pending Reviewer assertions. It **never** claims Review PASSED; independent `RequirementAnalysisAgent` review still must occur.
- The actual positive `native_gate.py` checks the authoritative `version/V_P0/requirement/{TARGET}/requirement.md`, not legacy `requirement_confirmation.md`, and requires at least one **current non-STALE** canonical Trace with matching SHA-256 and Acceptance coverage before Design→DEC consumption. Missing canonical source, missing trace, stale digest or no Acceptance coverage **fails closed**.
- `risk.json=NOT_SCANNED`, the original Task Plan iteration mismatch, and all 6 Reviewer assertions PENDING remain separately disclosed; none are silently repaired by this code change.

**Status:** No later R02 independent Review was found in GitHub before this change. The published R02 is **not approved**; the original native historical task is not mutated, and no StageOutcome is finalized. R-08 remains a required downstream analysis/Design Gate synchronization task, not an automatic substitute for independent content Reviewer judgment. **P0 remains BLOCKED / Issue #1 OPEN.**
