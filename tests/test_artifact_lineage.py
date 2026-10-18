"""Independent artifact lineage tests; no DEC runtime or fake green integration."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "scripts/p0_integration.py"
spec = importlib.util.spec_from_file_location("p0_manifest", SRC)
p0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p0)


class ArtifactLineageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / "dec"
        self.root.mkdir()
        self.runner = p0.Runner(self.root, self.base / "out", static_only=True)
        self.runner.summary["workflowGate"] = {"gateRevision": "DESIGN-R01@sha", "provenance": "fixture"}
        self.design = self.base / "design"
        self.design.mkdir()
        (self.design / "a.txt").write_text("canonical snapshot")

    def test_manifest_contains_parent_digests_and_revision(self):
        self.runner.artifact("dec/canonical-yaml/v1", self.design)
        html = self.base / "html"
        html.mkdir()
        (html / "index.html").write_text("<p>navigation</p>")
        self.runner.artifact("dec/generated-html", html)
        manifest = json.loads((self.base / "out/artifact-manifest.json").read_text())
        self.assertEqual(manifest["schema"], "common-develop-dec/p0-artifacts/v1")
        self.assertEqual(manifest["artifacts"][0]["inputs"][0]["revision"], "DESIGN-R01@sha")
        self.assertEqual(manifest["artifacts"][1]["inputs"][0]["sha256"],
                         manifest["artifacts"][0]["sha256"])

    def test_missing_artifact_parent_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "artifact dependency missing"):
            self.runner.artifact("dec/test-evidence/v1", self.design)

    def test_native_acceptance_is_never_default(self):
        self.assertEqual(self.runner.summary["p0AcceptanceStatus"],
                         "BLOCKED_NATIVE_WORKFLOW_UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
