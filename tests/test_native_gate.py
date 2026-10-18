"""P0 native evidence interpretation and artifact-lineage failure tests."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts"
spec = importlib.util.spec_from_file_location("p0_native", SCRIPT / "native_gate.py")
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


class NativeGateTests(unittest.TestCase):
    def setUp(self):
        self.gate = {"revision": "DESIGN-R01@123", "producer": "DesignAgent"}
        self.validation = {"status": "PASSED", "schemaVersion": 2, "errors": []}
        self.outcome = {"id": "SO-DESIGN-1", "phase": "design", "status": "PASSED",
                        "output_revision": self.gate["revision"],
                        "produced_by_agent": self.gate["producer"],
                        "input_revisions": {"requirement_analysis": "REQ-R01@sha"},
                        "evidence_ids": ["REV-DESIGN-R01"]}
        self.events = {"count": 1, "events": [
            {"type": "STAGE_OUTCOME_FINALIZED", "event_id": "TE-001",
             "payload": {"outcome": self.outcome}}]}

    def test_valid_finalization_is_only_native_result_match(self):
        a = native.interpret_native_evidence(self.validation, self.events, self.gate)
        self.assertEqual(a["stageOutcomeId"], "SO-DESIGN-1")
        self.assertEqual(a["outputRevision"], self.gate["revision"])

    def test_validation_alone_is_not_a_finalized_gate(self):
        self.events["events"] = [{"type": "TASK_STATE_PATCHED", "payload": {}}]
        with self.assertRaisesRegex(ValueError, "no native finalized"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_failed_review_or_invalid_native_schema_is_blocked(self):
        self.validation["status"] = "FAILED"
        with self.assertRaisesRegex(ValueError, "did not pass"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)
        self.validation["status"] = "PASSED"
        self.validation["schemaVersion"] = 1
        with self.assertRaisesRegex(ValueError, "unsupported"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_stale_or_different_native_design_revision_blocks(self):
        self.outcome["output_revision"] = "OLD"
        with self.assertRaisesRegex(ValueError, "output revision"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_latest_design_finalization_wins_even_if_older_passed(self):
        self.events["events"].append({"type": "STAGE_OUTCOME_FINALIZED", "event_id": "TE-002",
             "payload": {"outcome": {"id": "SO-NEW", "phase": "design", "status": "FAILED",
                                     "output_revision": "NEW", "produced_by_agent": "DesignAgent"}}})
        with self.assertRaisesRegex(ValueError, "not PASSED"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_native_requirements_and_review_evidence_required(self):
        self.outcome["input_revisions"] = {}
        with self.assertRaisesRegex(ValueError, "input revisions"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)
        self.outcome["input_revisions"] = {"requirement_analysis": "REQ-R01@sha"}
        self.outcome["evidence_ids"] = []
        with self.assertRaisesRegex(ValueError, "review/evidence"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_producer_must_equal_native_event_producer(self):
        self.outcome["produced_by_agent"] = "DifferentAgent"
        with self.assertRaisesRegex(ValueError, "producer"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_wrong_skill_cannot_be_used_as_native_opt(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "scripts").mkdir()
            (root / "scripts/long_task.py").write_text("pass\n")
            (root / "SKILL.md").write_text("---\nname: common-develop\n---\n")
            with self.assertRaisesRegex(ValueError, "expected common-develop-opt"):
                native.native_commands(root, root)


if __name__ == "__main__":
    unittest.main()
