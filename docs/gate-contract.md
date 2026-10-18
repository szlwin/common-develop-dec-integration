# P0 external workflow design Gate snapshot

This is **this adapter's input contract**, not an assertion that current Gitee common-develop-opt exports this shape. The native workflow is responsible for enforcing its own lifecycle, independent Reviewers and user/Agent authorization. An integration bridge must map native output into this file **without inventing decisions**.

```json
{
  "schema": "common-develop-dec/p0-gate/v1",
  "workflow": "common-develop-opt",
  "phase": "design",
  "status": "PASSED",
  "revision": "V_3.0:design:actual-revision-from-workflow",
  "producer": "DesignAgent",
  "reviewer": "SpecReviewAgent",
  "review": "PASSED",
  "provenance": "native-export",
  "artifacts": [
    {"path": "demo/order-payment-yaml", "sha256": "<computed-tree-digest>"}
  ]
}
```

The phase `design` is the **handoff checkpoint**, not proof that every prior phase was re-run by this adapter. `producer != reviewer`, exact field set, required status/phase, project-contained path and frozen digest are enforced. `native-export` is a **declaration**; it is *not signed/cryptographically authenticated*. The actor running the adapter must establish chain of custody. Design digest algorithm: for each file recursively (except ignored output/cache directories), sorted relative path + NUL + raw file SHA256 bytes, then SHA256 over the concatenated byte stream. It checks integrity only, not DEC semantics; DEC's own validator is mandatory.

A synthetic `fixture` gate is generated only with `--demo-fixture-gate`, has its own explicit provenance, and is disallowed with `--gate` in native integration mode. Do not relabel a fixture as `native-export` or copy synthetic decisions into production.

## P0 artifact flow

```text
common-develop-opt external design Gate + frozen DEC YAML tree
    -> verify Gate and input integrity
    -> dec-design: validate canonical YAML -> XML --check -> rendered HTML
    -> verify Gate still matches
    -> dec-java-lite: build/install -> inspect -> generate Java -> generated project test
    -> dec-implementation: static Binding symbol check
    -> dec-implementation: real test wrapper -> evidence check
    -> dec-implementation: release-ready gate (independent boolean)
    -> recheck frozen design tree, emit p0-report.json
```

Any non-release stage failure stops downstream execution. A failed release-ready check remains a **failed product gate**, not a reason to claim the optional unfinished design nodes have been implemented. If the project later reaches 111/111 VERIFIED, the same integration flow can record `productReleaseReady: true`.

## Native opt stage contract (actual upstream CLI)

Verified Gitee source revision: `b26715f6779b373b4f840b519ba9725fed5d789a`. The real StageOutcome is emitted by `scripts/long_task.py finalize-phase` as an append-only `STAGE_OUTCOME_FINALIZED` event whose payload contains an `outcome` object. It includes `phase`, `status`, `output_revision`, `produced_by_agent` and `id`. Native read-only entrypoints are:

```sh
python3 scripts/long_task.py validate -g ProjectManagerAgent --task-dir <TASK_DIR> --json
python3 scripts/long_task.py task-events -g ProjectManagerAgent --task-dir <TASK_DIR> --include-archive --json
```

A successful native validation of an INITIALIZED task does NOT mean design was approved. The integration additionally verifies the most recent finalized design event and requires status PASSED, output_revision == handoff revision, and producer identity match. All missing/stale/mismatched evidence is BLOCKED. Native review consistency is checked by the upstream validator; the adapter does not change Reviewer identities or infer independent contexts from JSON strings. The native task and the DEC YAML mapping must both exist before a positive integration claim.
