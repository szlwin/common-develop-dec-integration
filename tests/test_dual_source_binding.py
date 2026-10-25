"""Dual source binding is NOT a substitute for native independent approval."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("dual_source", ROOT / "scripts/check_dual_source_binding.py")
import sys
sys.path.insert(0, str(ROOT / "scripts"))
dual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dual)


class DualBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.opt = base / "opt"
        self.opt.mkdir()
        self.skill_task = base / "skill-doc/version/V_P0/task/SKILL-TASK"
        self.dec_task = base / "dec-doc/version/V_P0/task/DEC-TASK"
        self.skill_task.mkdir(parents=True)
        self.dec_task.mkdir(parents=True)
        self.skill_source = base / "skill-design.md"
        self.skill_source.write_text("Skill routing and integration design")
        self.dec_root = base / "dec"
        design = self.dec_root / "demo/order-payment-yaml"
        design.mkdir(parents=True)
        (design / "sample.yaml").write_text("system: demo\n")
        self.ssha = dual.digest_path(self.skill_source)
        self.dsha = dual.digest_path(design)
        self.binding = {
            "schema": dual.SCHEMA,
            "skill": {"taskId": "SKILL-TASK", "designRevision": "sha256:" + self.ssha,
                      "stageOutcomeId": "SO-SKILL", "finalizationEventId": "TE-SKILL",
                      "sourceSha256": self.ssha, "reviewScopeEvidenceId": "EVD-SKILL",
                      "designSourceKind": "skill-design"},
            "dec": {"taskId": "DEC-TASK", "designRevision": "sha256:" + self.dsha,
                    "stageOutcomeId": "SO-DEC", "finalizationEventId": "TE-DEC",
                    "sourceSha256": self.dsha, "reviewScopeEvidenceId": "EVD-DEC",
                    "designSourceKind": "dec-yaml-design"},
        }

    def check(self, query=lambda *_: {"validate": {"status": "FAILED"}, "events": {"events": []}}):
        return dual.verify(self.binding, self.opt, self.skill_task, self.dec_task,
                           self.skill_source, self.dec_root, query=query)

    def test_missing_second_source_is_rejected(self):
        self.binding.pop("dec")
        with self.assertRaisesRegex(ValueError, "schema/fields"):
            self.check()

    def test_misrepresenting_skill_design_as_dec_is_rejected(self):
        self.binding["dec"] = dict(self.binding["skill"])
        with self.assertRaisesRegex(ValueError, "native Task identity mismatch"):
            self.check()

    def test_same_native_task_cannot_approve_both_sources(self):
        with self.assertRaisesRegex(ValueError, "distinct native tasks"):
            dual.verify(self.binding, self.opt, self.skill_task, self.skill_task,
                        self.skill_source, self.dec_root)

    def test_changed_dec_yaml_invalidates_binding(self):
        (self.dec_root / "demo/order-payment-yaml/sample.yaml").write_text("system: changed")
        with self.assertRaisesRegex(ValueError, "source digest"):
            self.check()

    def test_changed_skill_design_invalidates_binding(self):
        self.skill_source.write_text("new skill design")
        with self.assertRaisesRegex(ValueError, "source digest"):
            self.check()

    def test_wrong_design_revision_is_rejected(self):
        self.binding["skill"]["designRevision"] = "DESIGN-R01"
        with self.assertRaisesRegex(ValueError, "not content-bound"):
            self.check()

    def test_missing_native_finalized_event_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing native finalized design"):
            self.check(query=lambda *_: {"validate": {"status": "PASSED", "schemaVersion": 2, "errors": []},
                                         "events": {"events": []}})

    def test_scope_snapshot_must_be_immutable(self):
        import json
        scope = self.skill_task / "evidence"
        scope.mkdir()
        (scope / "registry.jsonl").write_text(json.dumps({
            "evidence_id": "EVD-SKILL", "type": "design_ref",
            "capture_mode": "DIRECT", "ref": "blob.json", "digest": self.ssha
        }) + "\n")
        (scope / "blob.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "immutable"):
            dual._immutable_review_manifest(self.skill_task, "EVD-SKILL",
                                              {"schema": "common-develop-dec/review-scope/v1"}, self.ssha)

    def test_review_scope_with_wrong_content_is_rejected(self):
        import hashlib
        import json
        p = self.skill_task / "evidence/objects/scope.json"
        p.parent.mkdir(parents=True)
        raw = json.dumps({"schema": "common-develop-dec/review-scope/v1",
                          "designSourceKind": "skill-design", "taskId": "SKILL-TASK",
                          "sourceSha256": "f" * 64}).encode()
        p.write_bytes(raw)
        (self.skill_task / "evidence/registry.jsonl").write_text(json.dumps({
            "evidence_id": "EVD-SKILL", "type": "design_ref", "capture_mode": "SNAPSHOT",
            "ref": "evidence/objects/scope.json", "digest": hashlib.sha256(raw).hexdigest()
        }) + "\n")
        with self.assertRaisesRegex(ValueError, "approved content digest"):
            dual._immutable_review_manifest(self.skill_task, "EVD-SKILL",
                                              {"schema": "common-develop-dec/review-scope/v1",
                                               "designSourceKind": "skill-design", "taskId": "SKILL-TASK"},
                                              self.ssha)


if __name__ == "__main__":
    unittest.main()
