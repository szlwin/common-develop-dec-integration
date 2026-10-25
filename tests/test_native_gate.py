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

    def test_only_content_addressed_native_revision_is_accepted(self):
        good_sha = "a" * 64
        artifact = {"path": "demo/order-payment-yaml", "sha256": good_sha}
        gate = {"revision": "sha256:" + good_sha, "artifacts": [artifact]}
        self.assertEqual(native.verify_content_bound_revision(gate), good_sha)
        gate["revision"] = "DESIGN-R01@arbitrary-label"
        with self.assertRaisesRegex(ValueError, "content-bound"):
            native.verify_content_bound_revision(gate)

    def test_reopen_after_finalized_design_invalidates_approval(self):
        self.events["events"].append({
            "type": "TASK_STATE_PATCHED", "source": "long_task.py reopen-phase",
            "event_id": "TE-002", "payload": {}})
        with self.assertRaisesRegex(ValueError, "stale after"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_native_stage_superseded_event_blocks_old_approval(self):
        self.events["events"].append({
            "type": "STAGE_OUTCOME_SUPERSEDED", "event_id": "TE-002",
            "payload": {"outcome": {"id": "SO-DESIGN-1", "phase": "design"}}
        })
        with self.assertRaisesRegex(ValueError, "stale after"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_native_phase_stale_event_blocks_approval_without_source_tag(self):
        self.events["events"].append({
            "type": "PHASE_STALE", "event_id": "TE-002",
            "payload": {"stale_event": {"invalidated_phases": ["design", "testing"]}}
        })
        with self.assertRaisesRegex(ValueError, "stale after"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_new_published_unreviewed_design_invalidates_old_finalization(self):
        self.events["events"].append({
            "type": "STAGE_OUTCOME_PUBLISHED", "event_id": "TE-002",
            "payload": {"outcome": {"phase": "design", "id": "SO-DESIGN-2"}}
        })
        with self.assertRaisesRegex(ValueError, "stale after"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_producer_must_equal_native_event_producer(self):
        self.outcome["produced_by_agent"] = "DifferentAgent"
        with self.assertRaisesRegex(ValueError, "producer"):
            native.interpret_native_evidence(self.validation, self.events, self.gate)

    def test_native_design_handoff_requires_formal_analysis_trace(self):
        import hashlib
        import json
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "version/V_P0"
            task = root / "task/FEATURE-TEST"
            task.mkdir(parents=True)
            doc_dir = root / "requirement/FEATURE-TEST"
            doc_dir.mkdir(parents=True)
            old = doc_dir / "requirement_confirmation.md"
            old.write_text("old R02", encoding="utf-8")
            (task / "traceability.json").write_text(json.dumps({"items": [{
                "id": "TR-P0-REQCONF-001", "status": "PENDING",
                "requirement_refs": ["version/V_P0/requirement/FEATURE-TEST/requirement_confirmation.md"],
                "requirement_source_digest": hashlib.sha256(old.read_bytes()).hexdigest(),
                "acceptance_criteria": ["AC-01"],
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "canonical requirement.md"):
                native.require_p0_current_requirement_trace(task)

            current = doc_dir / "requirement.md"
            current.write_text("official source", encoding="utf-8")
            digest = hashlib.sha256(current.read_bytes()).hexdigest()
            row = {
                "id": "TR-REQ-P0-001-001", "status": "PENDING",
                "requirement_refs": ["version/V_P0/requirement/FEATURE-TEST/requirement.md"],
                "requirement_source_digest": "1" * 64,
                "acceptance_criteria": ["AC-REQ-P0-001-001"],
            }
            (task / "traceability.json").write_text(json.dumps({"items": [row]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "trace SHA"):
                native.require_p0_current_requirement_trace(task)
            row["requirement_source_digest"] = digest
            (task / "traceability.json").write_text(json.dumps({"items": [row]}), encoding="utf-8")
            self.assertEqual(native.require_p0_current_requirement_trace(task), digest)

    def test_skill_ab_task_rejects_dec_only_legacy_native_gate(self):
        class Runner:
            def command(self, *_args, **_kwargs):
                raise AssertionError("must block before any native or DEC command")
        with tempfile.TemporaryDirectory() as t:
            path = Path(t) / "FEATURE-DESC-2AD10B7DBDCA"
            path.mkdir()
            with self.assertRaisesRegex(ValueError, "two independently reviewed design sources"):
                native.validate_native_with_runner(Runner(), path, path, {})

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
