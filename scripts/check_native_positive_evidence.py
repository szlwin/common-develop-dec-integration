#!/usr/bin/env python3
"""Fail-closed positive P0 handoff evidence check.

A PASSED native design Gate and PASSED DEC chain are not by themselves proof of
the *complete* common-develop-opt lifecycle or independent full-Skill regressions.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_ARTIFACTS = {
    "dec/canonical-yaml/v1",
    "dec/generated-html",
    "java/generated-source",
    "dec/implementation-binding/v1",
    "dec/test-evidence/v1",
}


def verify(root: Path) -> dict:
    report = json.loads((root / "p0-report.json").read_text(encoding="utf-8"))
    graph = json.loads((root / "artifact-manifest.json").read_text(encoding="utf-8"))
    if report.get("integrationStatus") != "DEC_VERIFIED_NATIVE_GATE_CONSUMED":
        raise ValueError("real native Gate plus DEC chain has not passed")
    if report.get("p0AcceptanceStatus") != "NATIVE_HANDOFF_VERIFIED_DUAL_SKILL_REGRESSION_PENDING":
        raise ValueError("invalid native positive acceptance boundary")
    gate = report.get("workflowGate") or {}
    if gate.get("provenance") != "native-export" or gate.get("nativeWorkflowExecutionVerified") is not False:
        raise ValueError("native source provenance incorrect or full workflow wrongly claimed")
    if gate.get("nativeDesignStageOutcomeVerified") is not True:
        raise ValueError("real native finalized design StageOutcome not verified")
    evidence = gate.get("nativeEvidence") or {}
    digest = evidence.get("approvedDesignTreeSha256")
    if (not isinstance(digest, str) or len(digest) != 64
            or evidence.get("outputRevision") != "sha256:" + digest
            or evidence.get("status") != "PASSED"
            or not evidence.get("stageOutcomeId")
            or not evidence.get("inputRevisions")
            or not evidence.get("evidenceIds")):
        raise ValueError("native source-to-DEC digest, requirement or review evidence missing")
    if report.get("productReleaseReady") is not False:
        raise ValueError("pinned upstream order-payment Demo is not product release-ready")
    entries = graph.get("artifacts") or []
    if {a.get("type") for a in entries} != EXPECTED_ARTIFACTS or len(entries) != len(EXPECTED_ARTIFACTS):
        raise ValueError("missing or duplicate DEC artifact graph node")
    if not any(a.get("type") == "dec/canonical-yaml/v1" and a.get("sha256") == digest for a in entries):
        raise ValueError("design revision and produced DEC YAML have different content digests")
    by_type = {}
    for entry in entries:
        if not isinstance(entry.get("sha256"), str) or len(entry["sha256"]) != 64:
            raise ValueError("artifact digest missing")
        for parent in entry.get("inputs", []):
            if parent.get("type") == "common-develop-opt/design-gate":
                if parent.get("revision") != evidence["outputRevision"] or parent.get("provenance") != "native-export":
                    raise ValueError("artifact Gate provenance does not match native event")
            elif (parent.get("type") not in by_type or
                  by_type[parent["type"]]["sha256"] != parent.get("sha256")):
                raise ValueError("artifact dependency mismatch")
        by_type[entry["type"]] = entry
    command_records = [s for s in report.get("stages", []) if "returnCode" in s]
    native_steps = [s for s in command_records if s.get("name") == "native-workflow"]
    if {s.get("step") for s in native_steps} != {"task-validate", "task-events"}:
        raise ValueError("native CLI invocation not recorded")
    if len(command_records) < 13:
        raise ValueError("missing native/DEC real execution commands")
    for entry in command_records:
        log = root / entry["log"]
        if not log.is_file() or hashlib.sha256(log.read_bytes()).hexdigest() != entry["logSha256"]:
            raise ValueError("command log digest mismatch")
        if entry.get("name") != "release-readiness" and entry.get("returnCode") != 0:
            raise ValueError("native/DEC command failed")
    return {
        "status": "NATIVE_DESIGN_HANDOFF_AND_DEC_VERIFIED",
        "completeDualSkillLifecycleVerified": False,
        "productReleaseReady": False,
        "nativeStageOutcomeId": evidence["stageOutcomeId"],
        "nativeDesignTreeSha256": digest,
        "realCommands": len(command_records),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    try:
        print(json.dumps(verify(args.output), indent=2))
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print("P0 native-positive evidence check BLOCKED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
