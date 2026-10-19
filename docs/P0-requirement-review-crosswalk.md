# P0 Requirement Confirmation — Review evidence crosswalk (not approved)

**Status: OWNER PREFLIGHT / NOT INDEPENDENT REVIEW.** This matrix supplements the immutable published requirement artifact; it does not amend that artifact, mutate any native `task_events.jsonl`, or mark any assertion passed.

## Evidence integrity / original native gate

Task `FEATURE-DESC-DAE4FAB5F9F4`, Task Plan `TASK-REQCONF-P0-001`, Owner Attempt `ATTEMPT-TASK-REQCONF-P0-001-I001-A001`. Native `long_task validate` = **PASSED**. Requirement artifact has been PUBLISHED (StageOutcome `SO-FEATURE-DESC-DAE4FAB5F9F4-REQUIREMENT_CONFIRMATION-I001`), **not finalized**. `wk next` = `REVIEW_REQUIRED` / `ISOLATED_REVIEW_SESSION_REQUIRED`, Reviewer `RequirementAnalysisAgent`, `ownerContextReuseAllowed=false`. Six assertions AC-01..AC-06 are **PENDING**; event ledger has **zero `STAGE_OUTCOME_FINALIZED`**. All 27 original SHA256SUMS entries match; original owner Evidence is `EVD-000001` (immutable Markdown) and `EVD-000002` (validation command execution). Neither is independent Review evidence.

## Each acceptance criterion and its missing proofs

| Criterion | Currently grounded | Not yet proved / downstream phase |
|---|---|---|
| AC-01 Native requirement/analysis | Real Owner Attempt, snapshot and Task Plan | Isolated current-revision RequirementAnalysisAgent Review and finalized StageOutcomes of requirement_confirmation and requirement_analysis |
| AC-02 Design identity | 10 canonical upstream DEC YAML files at pinned source commit `4fb21242498746365c201fdf2a7fd8052f3a122a` | Real Design independent Review of exact bytes; Design Owner PASSED Attempt/Artifact and finalized native StageOutcome with current SHA binding |
| AC-03 DEC providers + tests | Existing **fixture-based** DEC/Java/Binding/JUnit CI | Real native-approved Gate consumed by all three fixed Providers; command logs, JUnit and SHA lineage |
| AC-04 Native consumption of DEC outputs | Existing DEC generated Java/Binding/test evidence available | Actual native `test_design`, `implementation_plan`, `development`, `code_review`, `testing`, `completion_verification` Artifact/Evidence and Review, then official archive |
| AC-05 Fail-closed + independent Skill regression | Negative Gate and fixed-version standalone Skill suites passed | Stale/reopened positive-native Gate rejection and re-validation after upstream version changes |
| AC-06 Integration versus Release | Four of 111 Design IDs are PLANNED; simulated payment/MongoDB/SMS adapters | Separate P0 acceptance and Product Release verdicts; no claim of production readiness |

Original traceability has a single `TR-P0-REQCONF-001` connecting all six ACs, with empty `test_case_ids` and `verification_evidence_ids`. The six native `MRQ-SCOPE` forms repeat the same generic scope question. This can be legal for the current phase, but must **not** be treated as completion of six independent end-to-end acceptance tests. Reviewer must judge whether the **requirements themselves** are sufficiently scoped and auditable; later phases must fill detailed evidence.

## Deterministic canonical DEC tree digest — not Git SHA-1

Pinned Integration `scripts/p0_integration.py:digest_path` calculates this hash on `demo/order-payment-yaml/`: sort all included ordinary files by root-relative POSIX path; exclude files beneath `.git`, `target`, `build`, `.gradle`, `__pycache__`, `.idea`, `.mvn`, or `node_modules`. For each file, feed `relative_path.encode('utf-8') + b'\\0' + SHA256(file_bytes).digest()` into a single SHA-256 hasher; render its lowercase hex digest. Expected pinned value: `a6961def87860d3cc1a7ecd1c67595b857b664b7077dc527207d9556610e1660`. The proposed native Design `output_revision` is `sha256:<digest>`; **not yet acceptance-proven**. A changed byte needs a newly reviewed native revision.

## Important portability finding: validation Evidence command

The current Task Plan's `validation_commands[0]` is `python scripts/long_task.py validate -g ProjectManagerAgent --task-dir ../native-doc/version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4 --json`. The historical EVD-000002 command was run from `/mnt/data/p0-native-stage-work/opt-pinned`. This relative command is **layout-dependent** and should not be copied blindly into an isolated Reviewer checkout. For a read-only fresh verification use:

```bash
TASK_DIR=/trusted/path/native-doc/version/V_P0/task/FEATURE-DESC-DAE4FAB5F9F4
cd /trusted/path/common-develop-opt
python scripts/long_task.py validate -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
python scripts/wk.py next -g ProjectManagerAgent --task-dir "$TASK_DIR" --json
```

If the historical Task Plan itself needs changing, do so via official Task Plan/Amendment procedure, not by silently editing post-publication facts. The historical command Evidence remains a fact about its original environment.

## TDD / full Standard phase alignment

Original pinned native Standard has 10 canonical phases: `requirement_confirmation`, `requirement_analysis`, `business_model`, `design`, `test_design`, `implementation_plan`, `development`, `code_review`, `testing`, `completion_verification`. There is **no separate canonical `tdd` StageOutcome** at this pin. Plan tests in `test_design`, record RED→GREEN→REFACTOR evidence in actual `development` task(s), and verify JUnit in `testing` and code review; unit success is not whole-system success.

**The only legal next approval action is a genuinely isolated `RequirementAnalysisAgent` Review.** Owner preflight is not a substitute. [Native Review handoff](P0-requirement-review-handoff.md) · [P0 acceptance](P0-acceptance.md) · [Issue #1](https://github.com/szlwin/common-develop-dec-integration/issues/1).
