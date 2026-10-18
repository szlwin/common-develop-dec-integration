#!/usr/bin/env python3
"""Verify fixed P0 CI artifact lineage, commands and explicit acceptance boundaries."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_TYPES = {
    "dec/canonical-yaml/v1",
    "dec/generated-html",
    "java/generated-source",
    "dec/implementation-binding/v1",
    "dec/test-evidence/v1",
}


def verify(output: Path):
    report = json.loads((output / "p0-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((output / "artifact-manifest.json").read_text(encoding="utf-8"))
    if report.get("integrationStatus") != "VERIFIED_WITH_FIXTURE":
        raise ValueError("CI only accepts explicit DEC fixture integration success")
    if report.get("p0AcceptanceStatus") != "BLOCKED_NATIVE_WORKFLOW_UNVERIFIED":
        raise ValueError("fixture must never be accepted as native P0 approval")
    if report.get("productReleaseReady") is not False:
        raise ValueError("pinned demo must not be declared product-release-ready")
    if manifest.get("schema") != "common-develop-dec/p0-artifacts/v1":
        raise ValueError("missing typed artifact manifest")
    recorded = manifest.get("artifacts")
    if not isinstance(recorded, list) or {a.get("type") for a in recorded} != EXPECTED_TYPES:
        raise ValueError("missing or duplicate required artifact types")
    by_type = {}
    for a in recorded:
        kind = a["type"]
        if kind in by_type:
            raise ValueError("duplicate artifact type: " + kind)
        path = Path(a["path"])
        if not path.exists() or len(a["sha256"]) != 64:
            raise ValueError("missing artifact/digest: " + kind)
        by_type[kind] = a
        for dep in a.get("inputs", []):
            if dep.get("type") == "common-develop-opt/design-gate":
                if dep.get("provenance") != "fixture":
                    raise ValueError("missing explicit fixture provenance")
            elif dep.get("type") not in by_type or by_type[dep["type"]]["sha256"] != dep.get("sha256"):
                raise ValueError("invalid artifact parent: " + kind)
    stages = report.get("stages", [])
    checked = 0
    for stage in stages:
        if "returnCode" not in stage:
            continue
        checked += 1
        log = output / stage["log"]
        if not log.is_file():
            raise ValueError("missing subprocess log")
        digest = hashlib.sha256(log.read_bytes()).hexdigest()
        if digest != stage.get("logSha256"):
            raise ValueError("subprocess log digest mismatch")
        if stage.get("name") != "release-readiness" and stage["returnCode"] != 0:
            raise ValueError("one of the DEC fixed-provider commands failed")
    if checked < 9 or not any(s.get("name") == "release-readiness" and s.get("returnCode") != 0 for s in stages):
        raise ValueError("missing real DEC commands or independent release gate")
    return {"checkedCommands": checked, "artifactTypes": sorted(by_type),
            "decFixtureIntegration": "PASSED", "nativeP0Approval": "BLOCKED",
            "productReleaseReady": False}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    try:
        result = verify(a.output)
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print("P0 evidence INVALID: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
