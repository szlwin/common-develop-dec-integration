#!/usr/bin/env python3
"""Read-only consistency gate for the *real* native requirement Review handoff.

Does not write canonical task state, submit manual reviews, or infer approval.
Native long_task validate verifies schema; during requirement_confirmation
the upstream contract defers canonical trace synchronization to requirement_analysis.
Missing/stale trace linkage is reported as a downstream condition, not a
fabricated RequirementAnalysisAgent veto.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_AC = {"AC-01", "AC-02", "AC-03", "AC-04", "AC-05", "AC-06"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def check(task_dir, requirement, skill_root=None):
    task_dir, requirement = Path(task_dir).resolve(strict=True), Path(requirement).resolve(strict=True)
    events = [json.loads(s) for s in (task_dir / "task_events.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    pubs = [(n, e["payload"]["outcome"]) for n, e in enumerate(events)
            if e.get("type") == "STAGE_OUTCOME_PUBLISHED"
            and (e.get("payload", {}).get("outcome") or {}).get("phase") == "requirement_confirmation"]
    if not pubs:
        raise ValueError("official requirement publication not found")
    index, outcome = pubs[-1]
    rev = outcome.get("output_revision", "")
    match = re.fullmatch(r"REQCONF-P0-R\d+@sha256-([a-f0-9]{64})", rev)
    digest = hashlib.sha256(requirement.read_bytes()).hexdigest()
    errors, warnings = [], []
    if not match or match.group(1) != digest:
        errors.append("CURRENT_REQUIREMENT_REVISION_MISMATCH")
    snapshot = task_dir / "evidence" / "objects" / (digest + ".md")
    if not snapshot.is_file() or hashlib.sha256(snapshot.read_bytes()).hexdigest() != digest:
        errors.append("REQUIREMENT_IMMUTABLE_EVIDENCE_MISSING")
    if any(e.get("type") == "STAGE_OUTCOME_SUPERSEDED" and
           (e.get("payload", {}).get("outcome") or {}).get("id") == outcome.get("id")
           for e in events[index+1:]):
        errors.append("CURRENT_REQUIREMENT_OUTCOME_SUPERSEDED")
    attempts = [e["payload"]["attempt"] for e in events
                if e.get("type") == "ATTEMPT_FINISHED"
                and (e.get("payload", {}).get("attempt") or {}).get("phase") == "requirement_confirmation"]
    if not attempts or attempts[-1].get("status") != "PASSED" or attempts[-1].get("output_revision") != rev:
        errors.append("CURRENT_REQUIREMENT_OWNER_ATTEMPT_NOT_PASSED")
    criteria = [a for a in read(task_dir / "acceptance.json").get("assertions", [])
                if a.get("revision") == rev and a.get("phase") == "requirement_confirmation"]
    ids = [a.get("acceptance_id") for a in criteria]
    if set(ids) != EXPECTED_AC or len(ids) != 6:
        errors.append("CURRENT_REVIEW_ASSERTIONS_NOT_COMPLETE")
    if any(a.get("status") != "VERIFIED" for a in criteria):
        warnings.append("INDEPENDENT_REVIEW_STILL_PENDING")
    traces = [x for x in read(task_dir / "traceability.json").get("items", [])
              if x.get("id") == "TR-P0-REQCONF-001"]
    source_digest = traces[0].get("requirement_source_digest") if len(traces) == 1 else None
    if source_digest != digest:
        # The upstream canonical sync-traceability command is authorized for
        # requirement_analysis, NOT a prerequisite to content Review in
        # requirement_confirmation. Keep visible but do not forge a blocker.
        warnings.append("TRACE_SYNC_REQUIRED_IN_REQUIREMENT_ANALYSIS")
    if len(traces) != 1 or set(traces[0].get("acceptance_criteria", [])) != EXPECTED_AC:
        errors.append("TRACE_AC_COVERAGE_INVALID")
    risk = read(task_dir / "risk.json").get("status")
    if risk == "NOT_SCANNED":
        warnings.append("OFFICIAL_RISK_SCAN_NOT_YET_COMPLETED")
    plan = [x for x in read(task_dir / "task_plan.json").get("tasks", [])
            if attempts and x.get("id") == attempts[-1].get("task_id")]
    if len(plan) != 1:
        errors.append("CURRENT_TASK_PLAN_ENTRY_MISSING")
    elif plan[0].get("iteration_id") != outcome.get("iteration_id"):
        warnings.append("TASK_PLAN_STILL_POINTS_TO_PREVIOUS_ITERATION")
    finalized = any(e.get("type") == "STAGE_OUTCOME_FINALIZED"
                    and (e.get("payload", {}).get("outcome") or {}).get("id") == outcome.get("id")
                    for e in events)
    report = {
        "schema": "common-develop-dec/p0-requirement-review-preflight/v1",
        "taskId": task_dir.name, "currentRevision": rev,
        "requirementSha256": digest, "traceSourceSha256": source_digest,
        "outcomeId": outcome.get("id"), "finalizedEventPresent": finalized,
        "reviewAssertionStatus": {a.get("acceptance_id"): a.get("status") for a in criteria},
        "riskStatus": risk, "errors": errors, "warnings": warnings,
        "downstreamDesignGateReady": (
            source_digest == digest and not errors and finalized
            and not any(a.get("status") != "VERIFIED" for a in criteria)
        ),
        "independentReviewVerified": False, "p0AcceptanceStatus": "BLOCKED",
    }
    if skill_root is not None:
        exe = Path(skill_root).resolve(strict=True) / "scripts" / "long_task.py"
        cmd = [sys.executable, str(exe), "validate", "-g", "ProjectManagerAgent",
               "--task-dir", str(task_dir), "--json"]
        result = subprocess.run(cmd, cwd=str(exe.parent.parent), capture_output=True, text=True)
        try:
            native = json.loads(result.stdout)
        except json.JSONDecodeError:
            native = {}
        report["upstreamValidator"] = native.get("status", "FAILED")
        if result.returncode or native.get("status") != "PASSED":
            errors.append("NATIVE_LONG_TASK_VALIDATE_FAILED")
    report["status"] = "BLOCKED_INTEGRITY" if errors else "AWAITING_ISOLATED_REVIEW"
    return report


def main():
    parser = argparse.ArgumentParser(description="Audit only: never approves a native Review")
    parser.add_argument("--task-dir", type=Path, required=True)
    parser.add_argument("--requirement", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = check(args.task_dir, args.requirement, args.skill_root)
        content = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content, encoding="utf-8")
        print(content)
        return 1 if report["errors"] else 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
