"""Negative contract for manually triggered native-approved handoff verification."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_native_positive_evidence.py"
spec = importlib.util.spec_from_file_location("native_positive_check", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class NativePositiveCheckerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "artifact-manifest.json").write_text(json.dumps({"artifacts": []}))

    def test_fixture_dec_success_cannot_satisfy_native_positive_gate(self):
        (self.root / "p0-report.json").write_text(json.dumps({
            "integrationStatus": "VERIFIED_WITH_FIXTURE",
            "p0AcceptanceStatus": "BLOCKED_NATIVE_WORKFLOW_UNVERIFIED"}))
        with self.assertRaisesRegex(ValueError, "real native Gate"):
            mod.verify(self.root)

    def test_positive_status_without_native_evidence_is_rejected(self):
        (self.root / "p0-report.json").write_text(json.dumps({
            "integrationStatus": "DEC_VERIFIED_NATIVE_GATE_CONSUMED",
            "p0AcceptanceStatus": "NATIVE_HANDOFF_VERIFIED_DUAL_SKILL_REGRESSION_PENDING",
            "workflowGate": {"provenance": "native-export",
                             "nativeWorkflowExecutionVerified": False}}))
        with self.assertRaisesRegex(ValueError, "StageOutcome"):
            mod.verify(self.root)


if __name__ == "__main__":
    unittest.main()
