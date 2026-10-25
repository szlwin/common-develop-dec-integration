# P0 native-positive acceptance runbook

This is a procedure for **genuine approved common-develop-opt artifacts**, not a synthetic approval or self-review. P0 remains BLOCKED without the real upstream task and independent Review.

## Native workflow prerequisite

Pin the actual Gitee source revision `b26715f6779b373b4f840b519ba9725fed5d789a`. Use its public command help, not direct edits to internal JSON/JSONL:

~~~sh
python3 scripts/wk.py help --script wk --command start --json
python3 scripts/wk.py help --script wk --command begin --json
python3 scripts/long_task.py help --command publish-artifact --json
python3 scripts/long_task.py help --command finalize-phase --json
~~~

Create and actually complete the order-payment requirement/design workflow through common-develop-opt's authorized agents and **independent reviewer context**. At least requirement_confirmation, requirement_analysis, business_model and design must be real, not prefilled StageOutcome JSON. Publish the real design artifact and finalize its phase via official CLI. Keep Review evidence and source links identifying the exact canonical DEC YAML tree reviewed.

### Approve a content-addressed design revision

Before publishing/reviewing, compute the exact `demo/order-payment-yaml` tree digest using the algorithm in [gate-contract.md](gate-contract.md) (sorted relative paths + NUL + raw file SHA256 bytes). Assign the actual *native artifact* output revision `sha256:<64 lowercase hex tree digest>` **through native commands prior to Review**. The native finalization event must carry this revision. If a native revision policy prohibits that format, a separately reviewed contract-compatible content binding must be developed before lifting P0; never silently bypass the check.

Confirm actual upstream result with the official read-only commands:

~~~sh
python3 scripts/long_task.py validate -g ProjectManagerAgent --task-dir <REAL_TASK_DIR> --json
python3 scripts/long_task.py task-events -g ProjectManagerAgent --task-dir <REAL_TASK_DIR> --include-archive --json
~~~

Require latest finalized `design` PASSED StageOutcome, matching Revision and producer, real `input_revisions` and `evidence_ids`, and no later reopened or invalidated phases.

### Native-to-DEC Gate JSON

Prepare one Gate conforming to [gate-contract.md](gate-contract.md), indexing the real native finalized event. The Gate `revision` must be the exact content-addressed native `output_revision`, the snapshot SHA must match the **current DEC YAML bytes**, the producer must be real, and the reviewer must be a real independent reviewer in upstream evidence. The Gate document does not itself grant approval; the integration must requery the original native CLI. Do not fabricate status, reviewer, event or revision.

### Execute the complete positive chain

Use Python 3.9, Java 21 and a test MySQL environment:

~~~sh
python3 scripts/p0_integration.py \
  --dec-root /path/to/dec-skills \
  --output /safe/p0-native-output \
  --gate /path/to/approved-design-gate.json \
  --native-opt-root /path/to/common-develop-opt \
  --native-task-dir /path/to/native-project/version/V_P0/task/ORDER_PAYMENT
python3 scripts/check_native_positive_evidence.py --output /safe/p0-native-output
~~~

For a **public sanitized demo only**, the manually dispatched [P0 native-approved CI workflow](../.github/workflows/p0-native-positive.yml) can repeat this on GitHub Actions. Commit a sanitized native task *with all of its required doc-root relative references* and an actual Gate to a reviewable commit in this repo. Input `task_dir` and `gate_path` are paths relative to the repository root. The workflow runs the real native validator/events and all DEC providers, then uploads evidence. Do **not** put passwords, tokens, private-user records or sensitive project data into a public repository or Actions artifact; use a trusted local/private runner instead.

Successful design handoff only verifies native design Gate -> DEC. For full original P0 acceptance, common-develop-opt must also manage downstream TDD, Development, Code Review, Testing/Completion stages, with evidence IDs and independent Review where required, and each independent Skill regression must pass. The 4 upstream PLANNED Design IDs keep `productReleaseReady=false`. Keep overall P0 status BLOCKED until authentic records prove the required lifecycle.


## 2026-10-25 current Skill P0 scope correction

**This guide validates a real native design→fixed DEC positive handoff, which remains part of the required Skill A+B acceptance.** The earlier statement that the *same order/payment business application* must subsequently finish RED/TDDReview, Development, Testing and Archive as a condition for **Skill P0** is superseded by the user's clarified [Skill P0 A+B scope matrix](P0-skill-scope-governance-20261025.md). That complete **business-software Standard E2E** now lives in [optional Issue #2](https://github.com/szlwin/common-develop-dec-integration/issues/2). This changes product acceptance **only**: a legitimately Standard-selected native Task (old or new) must still obey all its actual required stages and any applicable TDD/Reviewer Gates; neither this guide nor a fixture authorizes skipping those phases.
