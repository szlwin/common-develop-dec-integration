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
    event, outcome = matches[-1]  # The latest finalized design revision, never any stale prior pass.
    if outcome.get("status") != "PASSED":
        raise ValueError("latest native design StageOutcome is not PASSED")
    if outcome.get("output_revision") != gate.get("revision"):
        raise ValueError("native design output revision does not match handoff gate")
    if outcome.get("produced_by_agent") != gate.get("producer"):
        raise ValueError("native StageOutcome producer does not match handoff gate")
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
        "note": "Native validator confirms consistency; independent reviewer execution is enforced by upstream, not reproduced by this adapter."
    }


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
    return interpret_native_evidence(validation, event_query, gate)
