# common-develop-dec-integration — P0

Integrates **common-develop-opt (external workflow owner)** with three **fixed, independently usable DEC providers**. This repository is an *adapter*, not a fork of either upstream Skill, and does not implement a generic P1 capability registry.

- `dec-design` validates canonical YAML, checks deterministic XML conversion and regenerates HTML.
- `dec-java-lite` builds Runtime, inspects YAML, generates Java to an isolated output directory, and tests the generated project.
- `dec-implementation` checks real Design ID bindings, runs the existing Demo test-evidence wrapper, validates evidence, and evaluates `--require-ready` separately.

**Safety and provenance:** The Gitee-hosted `common-develop-opt` workflow cannot currently be invoked through a documented native CLI/export contract in this repository. The adapter **does not** assert that its lifecycle, independent reviews or approvals ran. A provided external Gate snapshot is strictly checked against the current DEC design digest; an explicit **synthetic fixture** exists only for demonstrating DEC integration. The P0 report sets `nativeWorkflowExecutionVerified: false` unless the real native CLI and finalized design event are validated. A JSON snapshot is not a cryptographic attestation: the originating workflow must validate its own Agent roles, Review independence, Gate and revision before exporting it. Upstream Gitee connectivity/current schema needs separate end-to-end verification.

## Local quick start

Requirements: Python >= 3.9, Java 21, Maven wrapper executability, and a checkout of [doc-eq-code-Dgremlin-skills](https://github.com/szlwin/doc-eq-code-Dgremlin-skills). Full tests require an available MySQL test database; see the DEC Demo docs. No edits to either upstream source repo are needed.

```bash
# Run adapter unit and negative tests (no remote dependencies)
python3 -m unittest discover -v -s tests

# Clone upstream outside this integration repository (when network is available)
git clone https://github.com/szlwin/doc-eq-code-Dgremlin-skills.git ../doc-eq-code-Dgremlin-skills

# A fixture-only local smoke run. Output MUST be outside the DEC checkout.
python3 scripts/p0_integration.py \
  --dec-root ../doc-eq-code-Dgremlin-skills \
  --output ../p0-evidence --demo-fixture-gate --static-only

# Full integration exercise against DEC real scripts, compiler, Maven and tests:
python3 scripts/p0_integration.py \
  --dec-root ../doc-eq-code-Dgremlin-skills \
  --output ../p0-full-evidence --demo-fixture-gate
```

For **externally approved workflow evidence**, replace `--demo-fixture-gate` with `--gate /path/to/design-gate.json`. The gate must come from a real `common-develop-opt` run and use the contract described in [`docs/gate-contract.md`](docs/gate-contract.md). The runner cannot attest the native workflow; it can only check the exported evidence's structure, separation of stated identities and snapshot integrity.

## Native common-develop-opt task handoff (P0 read-only bridge)

The actual Gitee source has been inspected at commit `b26715f6779b373b4f840b519ba9725fed5d789a`. The exact public commands are `scripts/long_task.py validate` and `scripts/long_task.py task-events`. The integration calls those read-only commands and requires the **latest** finalized `design/PASSED` StageOutcome to match the handoff revision and producer. The upstream validator—not a self-reported JSON reviewer string—checks the task ledger and independent Review rules.

```bash
python3 scripts/p0_integration.py \
  --dec-root ../doc-eq-code-Dgremlin-skills \
  --output ../p0-native-output \
  --gate /path/to/actual-design-handoff.json \
  --native-opt-root /path/to/common-develop/skills/common-develop-opt \
  --native-task-dir /path/to/project_doc/version/V_3.0/task/TARGET-ID
```

The external handoff JSON still freezes the canonical DEC YAML tree digest and must be bound to the native `output_revision`. It is *not* a substitute for a native StageOutcome. Unless both `--native-opt-root` and `--native-task-dir` are provided, external gate JSON remains **unverified** even if it claims `native-export`. A synthetic fixture cannot be combined with native validation.

CI now has a separate job that fetches the pinned Gitee Skill and **proves a native unapproved task fails closed**. This is not a positive, independently reviewed dual-Skill scenario; see [P0 acceptance ledger](docs/P0-acceptance.md). The P0 acceptance field remains blocked until such a run is recorded.

## Run outputs and quality semantics

`p0-report.json` records actual commands, exit codes and log SHA-256 hashes. `artifact-manifest.json` records typed output hashes, parent artifact digests and the upstream design Gate revision. `logs/` stores stdout/stderr, `design-html/` regenerated HTML, `generated-java/` new generator output. `demo/order-payment-app/target/dec-binding-evidence.json` is produced by DEC's own real test wrapper inside the **throwaway DEC checkout**, and must be archived separately by CI if required. Do not use the adapter to modify canonical YAML or generated XML directly.

| Result | Meaning |
| --- | --- |
| `BLOCKED` | A prerequisite, real DEC command, test or binding check failed. No downstream success can be inferred. |
| `PARTIAL_STATIC_ONLY` | Validator, XML check, HTML and static Binding passed. Generation and real tests were explicitly not run. |
| `VERIFIED_WITH_FIXTURE` | All three DEC providers ran successfully with a **synthetic gate**. **Does not verify common-develop-opt.** |
| `DEC_VERIFIED_EXTERNAL_GATE_CONSUMED` | All DEC checks ran and an external native-export-shaped gate was accepted. Still **does not independently verify** upstream lifecycle. |

`productReleaseReady` is separate. Current upstream Demo documentation states that **107/111 IDs are VERIFIED and 4 are PLANNED**. Consequently `--require-ready` should fail, and the adapter must preserve that fact even if the fixed-provider integration tests succeed. Unit tests alone never justify a product-ready claim.

## Scope and known limits

P0 provides a **fixed** adapter and an auditable, sequential dependency chain. It does **not** (1) replace the common-develop-opt workflow engine or its Review gates; (2) support dynamic provider selection, Standard/Lightweight/-min mode routing, or generic SPI (planned P1); (3) validate real external payment/SMS/MongoDB systems; (4) declare the Demo product release-ready. The provided GitHub Actions workflow uses a fixture gate and is therefore only DEC-side integration verification. Full native dual-Skill validation requires an actual, verifiable common-develop-opt export.

Sources: [DEC Demo](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/blob/main/demo/README.md), [DEC integration results](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/blob/main/demo/INTEGRATION.md), [dec-design](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/blob/main/skills/dec-design/SKILL.md), [dec-implementation](https://github.com/szlwin/doc-eq-code-Dgremlin-skills/blob/main/skills/dec-implementation/SKILL.md).


### P0 native content-binding requirement

For positive native handoffs, the **native** design `output_revision` and the Gate `revision` must both equal `sha256:<DEC-YAML-tree-digest>` (digest algorithm in `docs/gate-contract.md`). This revision must be set through common-develop-opt's **real** approved artifact and independent Review process, *before* native `finalize-phase`; the adapter does not rewrite task events or create approvals. Any later native phase reopen/invalidation blocks reuse of the old design StageOutcome. Existing arbitrary-label gates remain valid for fixture-only DEC validation, but not native-positive handoff.


### Approved native handoff: reproducible positive test entrypoint

See [native-positive-runbook.md](docs/native-positive-runbook.md) for the approved design lifecycle, SHA-bound Revision convention, and the exact StageOutcome/Review evidence requirements. [p0-native-positive.yml](.github/workflows/p0-native-positive.yml) is an **explicitly triggered** CI job for a real, sanitized approved task + Gate stored in this repo. It runs the native opt CLI and DEC providers, then [check_native_positive_evidence.py](scripts/check_native_positive_evidence.py). Neither the task nor a successful independent Review is presently included. The CI remains unexecuted for a genuine positive task; the overall P0 Gate remains BLOCKED.
