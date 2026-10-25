#!/usr/bin/env python3
"""Fail-closed v2 native Skill+DEC design handoff evidence checker.

This verifies a *completed Runner output*. It never creates or substitutes an
independent native Reviewer approval, and it does not close the full Skill
lifecycle or authorize a product release.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EXPECTED_DEPENDENCIES = {
    "dec/canonical-yaml/v1": [],
    "dec/generated-html": ["dec/canonical-yaml/v1"],
    "java/generated-source": ["dec/canonical-yaml/v1"],
    "dec/implementation-binding/v1": ["dec/canonical-yaml/v1"],
    "dec/test-evidence/v1": ["dec/canonical-yaml/v1", "dec/implementation-binding/v1"],
}
EXPECTED_COMMANDS = {
    ("dec-design", "validate"),
    ("dec-design", "converter-check"),
    ("dec-design", "render-html"),
    ("dec-java-lite", "install-runtime"),
    ("dec-java-lite", "inspect"),
    ("dec-java-lite", "generate"),
    ("dec-java-lite", "test-generated"),
    ("dec-implementation", "binding-static"),
    ("binding-evidence", "real-tests"),
    ("binding-evidence", "evidence-check"),
    ("release-readiness", "require-ready"),
}


def _sha(value):
    return isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value) is not None


def _required(value, description):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(description + " missing")
    return value


def verify(root: Path) -> dict:
    report = json.loads((root / "p0-report.json").read_text(encoding="utf-8"))
    graph = json.loads((root / "artifact-manifest.json").read_text(encoding="utf-8"))
    if report.get("integrationStatus") != "DEC_VERIFIED_TWO_NATIVE_SOURCES_CONSUMED":
        raise ValueError("v2 two-native-source Runner result missing")
    if report.get("p0AcceptanceStatus") != "NATIVE_TWO_SOURCE_HANDOFF_VERIFIED_LIFECYCLE_PENDING":
        raise ValueError("v2 lifecycle boundary missing or overstated")
    if report.get("productReleaseReady") is not False:
        raise ValueError("product release cannot be declared READY")

    gate = report.get("workflowGate") or {}
    if (gate.get("provenance") != "native-export"
            or gate.get("nativeWorkflowExecutionVerified") is not True
            or gate.get("nativeDesignStageOutcomeVerified") is not True
            or not _sha(gate.get("fixedProviderSourceSha256"))):
        raise ValueError("native provenance or executable Provider SHA missing")
    two = gate.get("twoSourceNativeApproval") or {}
    if (two.get("schema") != "common-develop-dec/dual-source-design-binding/v1"
            or two.get("status") != "TWO_SOURCE_NATIVE_EVIDENCE_MATCHED"
            or two.get("p0AcceptanceStatus") != "BLOCKED_PENDING_FULL_SKILL_ACCEPTANCE"
            or two.get("productReleaseReady") is not False
            or two.get("reviewerScopeAuthority") != "UPSTREAM_NATIVE_REVIEW_ONLY"):
        raise ValueError("two-source native evidence is missing or overclaims review")
    for source in ("skill", "dec"):
        item = two.get(source) or {}
        if (not _sha(item.get("digest"))
                or item.get("revision") != "sha256:" + item["digest"]
                or not all(item.get(key) for key in ("stageOutcomeId", "scopeEvidenceId", "producer"))):
            raise ValueError(source + " native design SHA/StageOutcome/Scope Evidence missing")
    skill_task = Path(_required(gate.get("nativeSkillTaskDir"), "Skill task"))
    dec_task = Path(_required(gate.get("nativeDecTaskDir"), "DEC task"))
    if (skill_task == dec_task or skill_task.name == dec_task.name
            or not skill_task.is_absolute() or not dec_task.is_absolute()):
        raise ValueError("separate native Skill/DEC task identities required")
    dec_digest = two["dec"]["digest"]
    if (gate.get("gateRevision") != two["dec"]["revision"]
            or gate.get("decGateProducer") != two["dec"]["producer"]):
        raise ValueError("DEC Gate revision/producer differs from approved DEC design")

    if (graph.get("schema") != "common-develop-dec/p0-artifacts/v1"
            or graph.get("workflowGate") != gate):
        raise ValueError("Artifact Manifest is not tied to this exact v2 Gate")
    entries = graph.get("artifacts")
    if (not isinstance(entries, list) or len(entries) != len(EXPECTED_DEPENDENCIES)
            or {e.get("type") for e in entries if isinstance(e, dict)} != set(EXPECTED_DEPENDENCIES)):
        raise ValueError("incomplete or duplicate fixed DEC Artifact graph")
    seen = {}
    for entry in entries:
        kind = entry["type"]
        if not _sha(entry.get("sha256")):
            raise ValueError("Artifact SHA-256 missing")
        inputs = entry.get("inputs")
        if not isinstance(inputs, list):
            raise ValueError("Artifact inputs absent")
        if kind == "dec/canonical-yaml/v1":
            if entry["sha256"] != dec_digest:
                raise ValueError("approved DEC design SHA differs from produced YAML")
            if inputs != [{"type": "common-develop-opt/design-gate",
                           "revision": two["dec"]["revision"], "provenance": "native-export"}]:
                raise ValueError("canonical YAML not bound to DEC native Gate")
        else:
            expected = [{"type": dependency, "sha256": seen[dependency]}
                        for dependency in EXPECTED_DEPENDENCIES[kind] if dependency in seen]
            if len(expected) != len(EXPECTED_DEPENDENCIES[kind]) or inputs != expected:
                raise ValueError("Artifact parent SHA/dependency mismatch")
        seen[kind] = entry["sha256"]

    transitions = {(s.get("name"), s.get("state")) for s in report.get("stages", [])
                   if isinstance(s, dict) and s.get("name") == "workflow-gate"}
    if (("workflow-gate", "TWO_NATIVE_DESIGNS_EVIDENCE_MATCHED") not in transitions
            or ("workflow-gate", "TWO_NATIVE_SOURCES_RECHECKED_AFTER_PROVIDERS") not in transitions):
        raise ValueError("v2 pre/post Provider native approval recheck missing")

    commands = [s for s in report.get("stages", []) if isinstance(s, dict) and "returnCode" in s]
    if {(s.get("name"), s.get("step")) for s in commands} != EXPECTED_COMMANDS:
        raise ValueError("missing/extra actual DEC Provider/Java/JUnit/Binding commands")
    for command in commands:
        rel = Path(_required(command.get("log"), "command log"))
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("unsafe command log path")
        log = (root / rel).resolve(strict=True)
        if root.resolve(strict=True) not in log.parents or not log.is_file():
            raise ValueError("command log outside evidence directory")
        if not _sha(command.get("logSha256")) or hashlib.sha256(log.read_bytes()).hexdigest() != command["logSha256"]:
            raise ValueError("command log SHA mismatch")
        if command.get("name") == "release-readiness":
            if command["returnCode"] == 0:
                raise ValueError("unexpected product release READY")
        elif command["returnCode"] != 0:
            raise ValueError("actual native DEC chain command failed")

    return {
        "status": "TWO_NATIVE_DESIGN_HANDOFF_AND_DEC_VERIFIED",
        "skillDesignStageOutcomeId": two["skill"]["stageOutcomeId"],
        "decDesignStageOutcomeId": two["dec"]["stageOutcomeId"],
        "skillDesignSha256": two["skill"]["digest"],
        "decYamlTreeSha256": dec_digest,
        "fixedProviderSourceSha256": gate["fixedProviderSourceSha256"],
        "realDecCommands": len(commands),
        "completeSkillLifecycleVerified": False,
        "independentReviewerAuthorityVerifiedByThisChecker": False,
        "productReleaseReady": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.output), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print("P0 dual native-positive evidence BLOCKED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
