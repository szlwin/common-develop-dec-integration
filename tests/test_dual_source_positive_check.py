"""Offline v2 output-checker fixtures; never stand in for native approvals."""
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/check_dual_source_positive_evidence.py"
spec = importlib.util.spec_from_file_location("dual_positive_check", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class DualPositiveEvidenceTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        skill, dec = digest("skill test-only"), digest("dec test-only")
        two = {
            "schema": "common-develop-dec/dual-source-design-binding/v1",
            "status": "TWO_SOURCE_NATIVE_EVIDENCE_MATCHED",
            "p0AcceptanceStatus": "BLOCKED_PENDING_FULL_SKILL_ACCEPTANCE",
            "productReleaseReady": False,
            "reviewerScopeAuthority": "UPSTREAM_NATIVE_REVIEW_ONLY",
            "skill": {"stageOutcomeId": "SO-SKILL", "scopeEvidenceId": "EVD-SKILL",
                      "producer": "SkillDesignAgent", "revision": "sha256:" + skill, "digest": skill},
            "dec": {"stageOutcomeId": "SO-DEC", "scopeEvidenceId": "EVD-DEC",
                    "producer": "DecDesignAgent", "revision": "sha256:" + dec, "digest": dec},
        }
        gate = {
            "provenance": "native-export",
            "nativeWorkflowExecutionVerified": True,
            "nativeDesignStageOutcomeVerified": True,
            "fixedProviderSourceSha256": digest("provider executable test-only"),
            "twoSourceNativeApproval": two,
            "nativeSkillTaskDir": "/trusted/task/SKILL-TASK",
            "nativeDecTaskDir": "/trusted/task/DEC-TASK",
            "decGateProducer": "DecDesignAgent",
            "gateRevision": "sha256:" + dec,
        }
        artifacts = []
        by_type = {}
        for kind, parents in mod.EXPECTED_DEPENDENCIES.items():
            sha = dec if kind == "dec/canonical-yaml/v1" else digest(kind)
            if kind == "dec/canonical-yaml/v1":
                inputs = [{"type": "common-develop-opt/design-gate",
                           "revision": "sha256:" + dec, "provenance": "native-export"}]
            else:
                inputs = [{"type": dep, "sha256": by_type[dep]} for dep in parents]
            artifacts.append({"type": kind, "path": "/fixture/" + kind,
                              "sha256": sha, "inputs": inputs})
            by_type[kind] = sha
        stages = [
            {"name": "workflow-gate", "state": "TWO_NATIVE_DESIGNS_EVIDENCE_MATCHED"},
            {"name": "workflow-gate", "state": "TWO_NATIVE_SOURCES_RECHECKED_AFTER_PROVIDERS"},
        ]
        logs = self.root / "logs"
        logs.mkdir()
        for i, (name, step) in enumerate(sorted(mod.EXPECTED_COMMANDS)):
            data = (name + ":" + step).encode("utf-8")
            rel = "logs/command-{0}.txt".format(i)
            (self.root / rel).write_bytes(data)
            stages.append({"name": name, "step": step, "returnCode": 1 if name == "release-readiness" else 0,
                           "log": rel, "logSha256": hashlib.sha256(data).hexdigest()})
        self.report = {
            "integrationStatus": "DEC_VERIFIED_TWO_NATIVE_SOURCES_CONSUMED",
            "p0AcceptanceStatus": "NATIVE_TWO_SOURCE_HANDOFF_VERIFIED_LIFECYCLE_PENDING",
            "productReleaseReady": False,
            "workflowGate": gate,
            "stages": stages,
        }
        self.graph = {"schema": "common-develop-dec/p0-artifacts/v1",
                      "workflowGate": copy.deepcopy(gate), "artifacts": artifacts}
        self.save()

    def save(self):
        (self.root / "p0-report.json").write_text(json.dumps(self.report), encoding="utf-8")
        (self.root / "artifact-manifest.json").write_text(json.dumps(self.graph), encoding="utf-8")

    def test_test_only_dual_positive_output_structure(self):
        result = mod.verify(self.root)
        self.assertEqual(result["status"], "TWO_NATIVE_DESIGN_HANDOFF_AND_DEC_VERIFIED")
        self.assertFalse(result["completeSkillLifecycleVerified"])
        self.assertFalse(result["independentReviewerAuthorityVerifiedByThisChecker"])
        self.assertFalse(result["productReleaseReady"])
        self.assertEqual(result["realDecCommands"], 11)

    def test_legacy_one_source_status_rejected(self):
        self.report["integrationStatus"] = "DEC_VERIFIED_NATIVE_GATE_CONSUMED"
        self.save()
        with self.assertRaisesRegex(ValueError, "v2 two-native"):
            mod.verify(self.root)

    def test_fixture_provenance_rejected(self):
        self.report["workflowGate"]["provenance"] = "fixture"
        self.graph["workflowGate"]["provenance"] = "fixture"
        self.save()
        with self.assertRaisesRegex(ValueError, "native provenance"):
            mod.verify(self.root)

    def test_missing_skill_source_evidence_rejected(self):
        self.report["workflowGate"]["twoSourceNativeApproval"]["skill"]["scopeEvidenceId"] = ""
        self.graph["workflowGate"]["twoSourceNativeApproval"]["skill"]["scopeEvidenceId"] = ""
        self.save()
        with self.assertRaisesRegex(ValueError, "skill native design"):
            mod.verify(self.root)

    def test_reused_native_task_identity_rejected(self):
        self.report["workflowGate"]["nativeSkillTaskDir"] = self.report["workflowGate"]["nativeDecTaskDir"]
        self.graph["workflowGate"]["nativeSkillTaskDir"] = self.graph["workflowGate"]["nativeDecTaskDir"]
        self.save()
        with self.assertRaisesRegex(ValueError, "separate native"):
            mod.verify(self.root)

    def test_gate_producer_substitution_rejected(self):
        self.report["workflowGate"]["decGateProducer"] = "Impersonator"
        self.graph["workflowGate"]["decGateProducer"] = "Impersonator"
        self.save()
        with self.assertRaisesRegex(ValueError, "Gate revision/producer"):
            mod.verify(self.root)

    def test_manifest_cannot_be_swapped_after_execution(self):
        self.graph["workflowGate"]["fixedProviderSourceSha256"] = digest("other")
        self.save()
        with self.assertRaisesRegex(ValueError, "not tied to this exact v2 Gate"):
            mod.verify(self.root)

    def test_changed_dec_artifact_sha_rejected(self):
        self.graph["artifacts"][0]["sha256"] = digest("different YAML")
        self.save()
        with self.assertRaisesRegex(ValueError, "approved DEC design SHA"):
            mod.verify(self.root)

    def test_missing_post_provider_recheck_rejected(self):
        self.report["stages"] = [x for x in self.report["stages"]
                                 if x.get("state") != "TWO_NATIVE_SOURCES_RECHECKED_AFTER_PROVIDERS"]
        self.save()
        with self.assertRaisesRegex(ValueError, "pre/post Provider"):
            mod.verify(self.root)

    def test_failed_java_test_command_rejected(self):
        target = next(x for x in self.report["stages"] if x.get("step") == "test-generated")
        target["returnCode"] = 1
        self.save()
        with self.assertRaisesRegex(ValueError, "chain command failed"):
            mod.verify(self.root)

    def test_command_log_tampering_rejected(self):
        (self.root / self.report["stages"][2]["log"]).write_text("tampered")
        with self.assertRaisesRegex(ValueError, "log SHA mismatch"):
            mod.verify(self.root)

    def test_product_ready_claim_rejected(self):
        self.report["productReleaseReady"] = True
        self.save()
        with self.assertRaisesRegex(ValueError, "product release"):
            mod.verify(self.root)


if __name__ == "__main__":
    unittest.main()
