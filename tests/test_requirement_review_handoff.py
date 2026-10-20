"""Tests proving stale R01 refs do not look like valid current R02 evidence."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

script = Path(__file__).resolve().parents[1] / "scripts/check_requirement_review_handoff.py"
spec = importlib.util.spec_from_file_location("req_review_check", script)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class RequirementHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.task = root / "task"
        self.task.mkdir()
        self.doc = root / "requirement_confirmation.md"
        self.doc.write_text("R02 requirement")
        self.digest = hashlib.sha256(self.doc.read_bytes()).hexdigest()
        self.rev = "REQCONF-P0-R02@sha256-" + self.digest
        objects = self.task / "evidence/objects"
        objects.mkdir(parents=True)
        (objects / (self.digest + ".md")).write_bytes(self.doc.read_bytes())
        self.events = [
            {"type": "ATTEMPT_FINISHED", "payload": {"attempt": {
                "task_id": "TASK-1", "phase": "requirement_confirmation",
                "status": "PASSED", "output_revision": self.rev}}},
            {"type": "STAGE_OUTCOME_PUBLISHED", "payload": {"outcome": {
                "id": "SO-2", "iteration_id": "ITER-002",
                "phase": "requirement_confirmation", "output_revision": self.rev}}},
        ]
        self.assertions = [{"acceptance_id": "AC-%02d" % i, "phase": "requirement_confirmation",
                            "revision": self.rev, "status": "PENDING"} for i in range(1, 7)]
        self.source_digest = self.digest
        self.write()

    def write(self):
        (self.task / "task_events.jsonl").write_text("\n".join(json.dumps(x) for x in self.events))
        for name, payload in [
            ("acceptance", {"assertions": self.assertions}),
            ("traceability", {"items": [{"id": "TR-P0-REQCONF-001",
                                        "acceptance_criteria": ["AC-%02d" % i for i in range(1, 7)],
                                        "requirement_source_digest": self.source_digest}]}),
            ("risk", {"status": "NOT_SCANNED"}),
            ("task_plan", {"tasks": [{"id": "TASK-1", "iteration_id": "ITER-002"}]})
        ]:
            (self.task / (name + ".json")).write_text(json.dumps(payload))

    def test_review_pending_is_not_falsely_approved(self):
        status = mod.check(self.task, self.doc)
        self.assertEqual(status["errors"], [])
        self.assertFalse(status["independentReviewVerified"])
        self.assertEqual(status["status"], "AWAITING_ISOLATED_REVIEW")
        self.assertEqual(status["p0AcceptanceStatus"], "BLOCKED")

    def test_r01_trace_stale_after_r02_publication_is_blocking(self):
        self.source_digest = "1" * 64
        self.write()
        self.assertIn("STALE_REQUIREMENT_TRACE_DIGEST", mod.check(self.task, self.doc)["errors"])

    def test_changed_requirement_file_is_blocked(self):
        self.doc.write_text("Changed after review")
        self.assertIn("CURRENT_REQUIREMENT_REVISION_MISMATCH", mod.check(self.task, self.doc)["errors"])

    def test_old_revision_review_assertion_does_not_count(self):
        self.assertions[0]["revision"] = "old"
        self.write()
        self.assertIn("CURRENT_REVIEW_ASSERTIONS_NOT_COMPLETE", mod.check(self.task, self.doc)["errors"])

    def test_superseded_published_outcome_blocks(self):
        self.events.append({"type": "STAGE_OUTCOME_SUPERSEDED",
                            "payload": {"outcome": {"id": "SO-2"}}})
        self.write()
        self.assertIn("CURRENT_REQUIREMENT_OUTCOME_SUPERSEDED", mod.check(self.task, self.doc)["errors"])


if __name__ == "__main__":
    unittest.main()
