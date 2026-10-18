"""Unit + isolated script-level integration tests, not DEC Runtime verification."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / 'scripts' / 'p0_integration.py'
spec = importlib.util.spec_from_file_location('p0_integration', SRC)
p0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p0)


class GateTest(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / 'upstream'
        (self.root / 'demo/order-payment-yaml').mkdir(parents=True)
        (self.root / 'demo/order-payment-yaml/one.yaml').write_text('kind: example\n', encoding='utf-8')
        self.gate = p0.demo_gate(self.root)

    def test_fixture_is_never_accepted_as_native(self):
        with self.assertRaisesRegex(ValueError, 'fixture gate'):
            p0.check_gate(self.gate, self.root)
        data = p0.check_gate(self.gate, self.root, allow_fixture=True)
        self.assertEqual(data['provenance'], 'fixture')
        self.assertFalse(data['nativeWorkflowExecutionVerified'])

    def test_native_export_frozen_hash(self):
        self.gate['provenance'] = 'native-export'
        self.gate['revision'] = 'V_1.0:design:rev-7'
        self.assertEqual(p0.check_gate(self.gate, self.root)['gateRevision'], self.gate['revision'])
        (self.root / 'demo/order-payment-yaml/one.yaml').write_text('kind: changed\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'STALE'):
            p0.check_gate(self.gate, self.root)

    def test_reviewer_independence(self):
        self.gate['reviewer'] = self.gate['producer']
        with self.assertRaisesRegex(ValueError, 'self-reviewed'):
            p0.check_gate(self.gate, self.root, allow_fixture=True)

    def test_path_traversal_and_symlink_forbidden(self):
        with self.assertRaises(ValueError):
            p0.within(self.root, '../outside')
        forbidden = Path(self.t.name) / 'secret.txt'
        forbidden.write_text('secret')
        (self.root / 'link').symlink_to(forbidden)
        with self.assertRaisesRegex(ValueError, 'escapes root'):
            p0.within(self.root, 'link')

    def test_snapshot_rejects_external_symlink_inside_directory(self):
        secret = Path(self.t.name) / 'secret.txt'
        secret.write_text('secret')
        (self.root / 'demo/order-payment-yaml/link').symlink_to(secret)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            p0.digest_path(self.root / 'demo/order-payment-yaml')

    def test_failed_and_missing_artifact_rejected(self):
        self.gate['status'] = 'FAILED'
        with self.assertRaisesRegex(ValueError, 'invalid workflow'):
            p0.check_gate(self.gate, self.root, allow_fixture=True)
        self.gate['status'] = 'PASSED'
        self.gate['artifacts'] = []
        with self.assertRaisesRegex(ValueError, 'missing gate'):
            p0.check_gate(self.gate, self.root, allow_fixture=True)

    def test_duplicate_artifacts_and_extra_gate_fields_rejected(self):
        self.gate['artifacts'].append(dict(self.gate['artifacts'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            p0.check_gate(self.gate, self.root, allow_fixture=True)
        self.gate['artifacts'].pop()
        self.gate['statusOverride'] = 'PASSED'
        with self.assertRaisesRegex(ValueError, 'requires exactly'):
            p0.check_gate(self.gate, self.root, allow_fixture=True)

    def test_run_fail_closed_on_design_validation(self):
        out = Path(self.t.name) / 'out'
        result = p0.Runner(self.root, out, static_only=True).execute(self.gate, fixture=True)
        self.assertEqual(result['integrationStatus'], 'BLOCKED')
        report = json.loads((out / 'p0-report.json').read_text())
        self.assertEqual(report['stages'][-1]['name'], 'stop')
        self.assertIn('dec-design', [r['name'] for r in report['stages']])

    def test_prevent_upstream_source_mutation_via_output(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            p0.Runner(self.root, self.root / 'demo/output', static_only=True)

    def test_digest_detects_added_file(self):
        original = p0.digest_path(self.root / 'demo/order-payment-yaml')
        (self.root / 'demo/order-payment-yaml/two.yaml').write_text('kind: api\n')
        self.assertNotEqual(original, p0.digest_path(self.root / 'demo/order-payment-yaml'))


if __name__ == '__main__':
    unittest.main()
