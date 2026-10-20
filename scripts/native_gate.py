"""Read-only native common-develop-opt handoff verification.

Only the upstream CLI may validate its own event ledger and independent reviews.
The integration must never synthesize a finalized StageOutcome.
"""
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional

EXPECTED_SCHEMA = 2
FINALIZED_EVENT = "STAGE_OUTCOME_FINALIZED"


def verify_content_bound_revision(gate: dict) -> str:
    """P0 requires the *native approved revision* to commit to the DEC bytes.

    Native opt does not expose a signed mapping from an arbitrary revision label
    to an external DEC directory. A free-form revision in a hand-written gate
    must not upgrade an unreviewed YAML tree to an approved artifact.
    """
    import re
    entries = gate.get("artifacts")
    if not isinstance(entries, list):
        raise ValueError("native Gate missing artifact snapshot")
    digest = next((x.get("sha256") for x in entries
                   if isinstance(x, dict) and x.get("path") == "demo/order-payment-yaml"), None)
    if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
        raise ValueError("native Gate has no valid DEC canonical YAML digest")
    if gate.get("revision") != "sha256:" + digest:
        raise ValueError("native design output revision must be content-bound: sha256:<DEC-YAML-tree-digest>")
    return digest


def interpret_native_evidence(validation: Dict[str, Any],
                              event_query: Dict[str, Any],
                              gate: Dict[str, Any]) -> Dict[str, Any]:
    """Interpret JSON from the real long_task CLI; no private state files read."""
    if not isinstance(validation, dict) or validation.get("status") != "PASSED":
        raise ValueError("native long_task validate did not pass")
    if validation.get("schemaVersion") != EXPECTED_SCHEMA or validation.get("errors"):
        raise ValueError("unsupported native task schema or outstanding validation errors")
    if not isinstance(event_query, dict) or not isinstance(event_query.get("events"), list):
        raise ValueError("native task-events query must return an events array")
    matches = []
    for event in event_query["events"]:
        if not isinstance(event, dict) or event.get("type") != FINALIZED_EVENT:
            continue
        payload = event.get("payload")
        outcome = payload.get("outcome") if isinstance(payload, dict) else None
        if not isinstance(outcome, dict) or outcome.get("phase") != "design":
            continue
        matches.append((event, outcome))
    if not matches:
        raise ValueError("no native finalized design StageOutcome in append-only ledger")
    event, outcome = matches[-1]  # Latest design finalization from upstream task-events.
    selected_index = next(i for i in range(len(event_query["events"]) - 1, -1, -1)
                          if event_query["events"][i] is event)
    # A later native reopen invalidates the earlier approval even if its
    # historical finalized event is still in the append-only ledger.
    for later in event_query["events"][selected_index + 1:]:
        if not isinstance(later, dict):
            continue
        source = str(later.get("source") or "").lower()
        event_type = str(later.get("type") or "").upper()
        payload = later.get("payload")
        payload = payload if isinstance(payload, dict) else {}
        later_outcome = payload.get("outcome") if isinstance(payload.get("outcome"), dict) else {}
        stale = payload.get("stale_event") if isinstance(payload.get("stale_event"), dict) else {}
        if (
            (event_type == "STAGE_OUTCOME_SUPERSEDED" and later_outcome.get("id") == outcome.get("id"))
            or (event_type == "PHASE_STALE" and "design" in (stale.get("invalidated_phases") or []))
            or (event_type == "STAGE_OUTCOME_PUBLISHED" and later_outcome.get("phase") == "design")
            or "reopen-phase" in source or "REOPEN" in event_type or "INVALIDAT" in event_type
        ):
            raise ValueError("native design StageOutcome is stale after a reopen/invalidation event")
    if outcome.get("status") != "PASSED":
        raise ValueError("latest native design StageOutcome is not PASSED")
    if outcome.get("output_revision") != gate.get("revision"):
        raise ValueError("native design output revision does not match handoff gate")
    if outcome.get("produced_by_agent") != gate.get("producer"):
        raise ValueError("native StageOutcome producer does not match handoff gate")
    native_inputs = outcome.get("input_revisions")
    native_evidence = outcome.get("evidence_ids")
    if not isinstance(native_inputs, dict) or not native_inputs:
        raise ValueError("native StageOutcome missing upstream requirement/design input revisions")
    if not isinstance(native_evidence, list) or not native_evidence:
        raise ValueError("native StageOutcome missing actual review/evidence references")
    if not outcome.get("id") or not event.get("event_id"):
        raise ValueError("native finalization missing stable outcome/event identity")
    return {
        "stageOutcomeId": outcome["id"],
        "eventId": event["event_id"],
        "phase": "design",
        "status": "PASSED",
        "outputRevision": outcome["output_revision"],
        "producedByAgent": outcome["produced_by_agent"],
        "nativeValidatorStatus": validation["status"],
        "nativeValidatorSchema": validation["schemaVersion"],
        "inputRevisions": native_inputs,
        "evidenceIds": native_evidence,
        "note": "Native validator confirms consistency; independent reviewer execution is enforced by upstream, not reproduced by this adapter."
    }


def require_p0_current_requirement_trace(task_dir: Path) -> str:
    """Fail closed if a P0 native task retains an R01 trace after R02 review.

    Original native validate guarantees its schema, not cross-file content
    identity. This checks the exact known P0 trace independently of any
    hand-written gate.json; never mutates the task or invents reviewer approval.
    """
    import hashlib
    task_dir = task_dir.resolve(strict=True)
    data = json.loads((task_dir / "traceability.json").read_text(encoding="utf-8"))
    entries = [x for x in data.get("items", [])
               if isinstance(x, dict) and x.get("id") == "TR-P0-REQCONF-001"]
    if len(entries) != 1:
        raise ValueError("P0 native Gate requires one current requirement trace")
    document = (task_dir.parent.parent / "requirement" / task_dir.name /
                "requirement_confirmation.md").resolve(strict=True)
    digest = hashlib.sha256(document.read_bytes()).hexdigest()
    if entries[0].get("requirement_source_digest") != digest:
        raise ValueError("P0 native Gate is stale: requirement trace SHA does not match current requirement bytes")
    return digest


def native_commands(skill_root: Path, task_dir: Path):
    root = skill_root.resolve(strict=True)
    task = task_dir.resolve(strict=True)
    skill_file = root / "SKILL.md"
    validator = root / "scripts/long_task.py"
    if not skill_file.is_file() or not validator.is_file():
        raise ValueError("missing common-develop-opt public entrypoint or SKILL.md")
    # This checks only the explicitly supplied Skill identity. The exact commit is recorded by CI.
    front = skill_file.read_text(encoding="utf-8").split("---", 2)
    if len(front) < 3 or "name: common-develop-opt" not in front[1].splitlines():
        raise ValueError("expected common-develop-opt, refusing a different workflow implementation")
    return {
        "validate": [sys.executable, str(validator), "validate", "-g", "ProjectManagerAgent",
                     "--task-dir", str(task), "--json"],
        "events": [sys.executable, str(validator), "task-events", "-g", "ProjectManagerAgent",
                   "--task-dir", str(task), "--include-archive", "--json"],
    }


def validate_native_with_runner(runner, skill_root: Path, task_dir: Path, gate: dict) -> dict:
    commands = native_commands(skill_root, task_dir)
    runner.command("native-workflow", "task-validate", commands["validate"], cwd=skill_root)
    runner.command("native-workflow", "task-events", commands["events"], cwd=skill_root)
    path = runner.output / "logs"
    validation = json.loads((path / "native-workflow-task-validate.log").read_text(encoding="utf-8"))
    event_query = json.loads((path / "native-workflow-task-events.log").read_text(encoding="utf-8"))
    result = interpret_native_evidence(validation, event_query, gate)
    result["currentRequirementTraceSha256"] = require_p0_current_requirement_trace(task_dir)
    return result
