#!/usr/bin/env python3
"""P0 fixed-provider DEC integration runner. Python 3.9+, standard library only.

The runner does NOT implement common-develop-opt's lifecycle/review engine. It
consumes an external gate as a frozen, auditable prerequisite and fails closed.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

try:
    from native_gate import validate_native_with_runner, verify_content_bound_revision
except ImportError:  # Allows direct imports by the unit-test harness.
    from scripts.native_gate import validate_native_with_runner, verify_content_bound_revision

VERSION = 'common-develop-dec/p0/v1'
GATE_VERSION = 'common-develop-dec/p0-gate/v1'
STAGES = ('workflow-gate', 'dec-design', 'dec-java-lite', 'dec-implementation', 'binding-evidence', 'release-readiness')
IGNORE = {'.git', 'target', 'build', '.gradle', '__pycache__', '.idea', '.mvn', 'node_modules'}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest_path(root: Path) -> str:
    """Snapshot file bytes for integrity; never interprets or modifies YAML/XML."""
    root = root.resolve(strict=True)
    if root.is_file():
        return hashlib.sha256(root.read_bytes()).hexdigest()
    files = sorted((f for f in root.rglob('*') if f.is_file() and not any(p in IGNORE for p in f.relative_to(root).parts)), key=lambda f: f.relative_to(root).as_posix())
    if any(f.is_symlink() for f in files):
        raise ValueError('symlink files are forbidden in artifact snapshots')
    if not files:
        raise ValueError('empty artifact directory: ' + str(root))
    h = hashlib.sha256()
    for f in files:
        rel = f.relative_to(root).as_posix()
        h.update(rel.encode('utf-8') + b'\0')
        h.update(hashlib.sha256(f.read_bytes()).digest())
    return h.hexdigest()


def within(root: Path, relative: str) -> Path:
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError('artifact path must be project-relative and without ..: ' + relative)
    base = root.resolve(strict=True)
    result = (base / p).resolve(strict=True)
    if result != base and base not in result.parents:
        raise ValueError('artifact path escapes root: ' + relative)
    return result


def check_gate(gate: dict, dec_root: Path, allow_fixture: bool = False) -> dict:
    required = {'schema', 'workflow', 'phase', 'status', 'revision', 'producer', 'reviewer', 'review', 'provenance', 'artifacts'}
    if not isinstance(gate, dict) or set(gate) != required:
        raise ValueError('gate requires exactly: ' + ', '.join(sorted(required)))
    expected = (GATE_VERSION, 'common-develop-opt', 'design', 'PASSED', 'PASSED')
    actual = tuple(gate[k] for k in ('schema', 'workflow', 'phase', 'status', 'review'))
    if actual != expected:
        raise ValueError('invalid workflow/phase/status/review, expected ' + str(expected))
    if not all(isinstance(gate[k], str) and gate[k].strip() for k in ('revision', 'producer', 'reviewer')):
        raise ValueError('revision and agent identities must be nonempty')
    if gate['producer'] == gate['reviewer']:
        raise ValueError('self-reviewed workflow gate is forbidden')
    if gate['provenance'] not in ('native-export', 'fixture'):
        raise ValueError('unknown gate provenance')
    if gate['provenance'] == 'fixture' and not allow_fixture:
        raise ValueError('fixture gate is prohibited in native integration mode')
    if not isinstance(gate['artifacts'], list) or not gate['artifacts']:
        raise ValueError('missing gate artifact attestations')
    checked = []
    paths = set()
    for artifact in gate['artifacts']:
        if not isinstance(artifact, dict) or set(artifact) != {'path', 'sha256'}:
            raise ValueError('invalid artifact attestation')
        rel = artifact['path']
        if not isinstance(rel, str) or rel in paths:
            raise ValueError('duplicate or invalid gate artifact path')
        paths.add(rel)
        actual_hash = digest_path(within(dec_root, rel))
        if actual_hash != artifact['sha256']:
            raise ValueError('STALE upstream gate for ' + rel)
        checked.append({'path': rel, 'sha256': actual_hash})
    if 'demo/order-payment-yaml' not in paths:
        raise ValueError('gate must freeze demo/order-payment-yaml')
    return {'gateRevision': gate['revision'], 'provenance': gate['provenance'], 'artifacts': checked,
            'nativeWorkflowExecutionVerified': False}


def demo_gate(dec_root: Path) -> dict:
    """Synthetic fixture only. NEVER claim a native common-develop-opt pass."""
    return {'schema': GATE_VERSION, 'workflow': 'common-develop-opt', 'phase': 'design',
            'status': 'PASSED', 'revision': 'DEMO-FIXTURE-NOT-NATIVE',
            'producer': 'FixtureProducer', 'reviewer': 'FixtureReviewer', 'review': 'PASSED',
            'provenance': 'fixture', 'artifacts': [
                {'path': 'demo/order-payment-yaml', 'sha256': digest_path(dec_root / 'demo/order-payment-yaml')} ]}


def atomic_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    tmp.replace(path)


class Runner:
    def __init__(self, dec_root: Path, output: Path, static_only: bool):
        self.dec_root = dec_root.resolve(strict=True)
        self.output = output.resolve()
        if self.output == self.dec_root or self.dec_root in self.output.parents:
            raise ValueError('output must be outside the DEC repository to avoid source mutations')
        self.output.mkdir(parents=True, exist_ok=True)
        self.static_only = static_only
        self.summary: Dict = {'schema': VERSION, 'createdAt': utc_now(),
            'mode': 'STATIC_ONLY' if static_only else 'END_TO_END',
            'sources': {'dec': str(self.dec_root)}, 'stages': [], 'artifacts': [],
            'integrationStatus': 'BLOCKED', 'productReleaseReady': None,
            'p0AcceptanceStatus': 'BLOCKED_NATIVE_WORKFLOW_UNVERIFIED'}

    def record(self, name: str, state: str, details: Optional[dict] = None) -> None:
        self.summary['stages'].append({'name': name, 'state': state, 'at': utc_now(), **(details or {})})
        atomic_json(self.output / 'p0-report.json', self.summary)

    def command(self, stage: str, label: str, argv: List[str], cwd: Optional[Path] = None,
                allow_failure: bool = False) -> int:
        log_dir = self.output / 'logs'
        log_dir.mkdir(exist_ok=True)
        log_name = stage + '-' + label + '.log'
        log = log_dir / log_name
        try:
            with log.open('wb') as sink:
                completed = subprocess.run(argv, cwd=str(cwd or self.dec_root), stdout=sink,
                                           stderr=subprocess.STDOUT, check=False)
            code = completed.returncode
        except (OSError, ValueError) as exc:
            log.write_text(repr(exc), encoding='utf-8')
            code = 127
        self.record(stage, 'FAILED' if code != 0 else 'PASSED',
                    {'step': label, 'command': argv, 'returnCode': code,
                     'log': str(log.relative_to(self.output)), 'logSha256': digest_path(log)})
        if code != 0 and not allow_failure:
            raise RuntimeError('{} / {} returned {}'.format(stage, label, code))
        return code

    def artifact(self, kind: str, path: Path) -> None:
        dependencies = {
            'dec/canonical-yaml/v1': [],
            'dec/generated-html': ['dec/canonical-yaml/v1'],
            'java/generated-source': ['dec/canonical-yaml/v1'],
            'dec/implementation-binding/v1': ['dec/canonical-yaml/v1'],
            'dec/test-evidence/v1': ['dec/canonical-yaml/v1', 'dec/implementation-binding/v1'],
        }
        known = {a['type']: a for a in self.summary['artifacts']}
        parents = []
        for expected in dependencies.get(kind, []):
            if expected not in known:
                raise ValueError('artifact dependency missing: ' + expected)
            parents.append({'type': expected, 'sha256': known[expected]['sha256']})
        gate_info = self.summary.get('workflowGate') or {}
        if kind == 'dec/canonical-yaml/v1':
            parents.append({'type': 'common-develop-opt/design-gate',
                            'revision': gate_info.get('gateRevision'),
                            'provenance': gate_info.get('provenance')})
        entry = {'type': kind, 'path': str(path), 'sha256': digest_path(path),
                 'inputs': parents, 'recordedAt': utc_now()}
        self.summary['artifacts'].append(entry)
        atomic_json(self.output / 'artifact-manifest.json', {
            'schema': 'common-develop-dec/p0-artifacts/v1',
            'workflowGate': gate_info, 'artifacts': self.summary['artifacts']})
        atomic_json(self.output / 'p0-report.json', self.summary)

    def execute(self, gate: dict, fixture: bool = False,
                native_opt_root: Optional[Path] = None,
                native_task_dir: Optional[Path] = None,
                dual_binding: Optional[dict] = None,
                skill_task_dir: Optional[Path] = None,
                skill_design_source: Optional[Path] = None) -> dict:
        try:
            verified = check_gate(gate, self.dec_root, allow_fixture=fixture)
            self.summary['workflowGate'] = verified
            if native_opt_root is not None and dual_binding is not None:
                try:
                    from check_dual_source_binding import verify as verify_two_sources, _assert_pinned_dec_checkout, _provider_source_digest
                except ImportError:
                    from scripts.check_dual_source_binding import verify as verify_two_sources, _assert_pinned_dec_checkout, _provider_source_digest
                if skill_task_dir is None or skill_design_source is None:
                    raise ValueError("dual-source requires the original Skill task and design source")
                if gate.get("revision") != dual_binding.get("dec", {}).get("designRevision"):
                    raise ValueError("DEC Gate revision not bound to second native design source")
                bound_digest = verify_content_bound_revision(gate)
                if bound_digest != dual_binding["dec"]["sourceSha256"]:
                    raise ValueError("DEC Gate bytes not bound to approved second design source")
                _assert_pinned_dec_checkout(self.dec_root)
                provider_source_before = _provider_source_digest(self.dec_root)
                native_evidence = verify_two_sources(dual_binding, native_opt_root, skill_task_dir,
                                                     native_task_dir, skill_design_source, self.dec_root)
                if gate["producer"] != native_evidence["dec"]["producer"]:
                    raise ValueError("DEC Gate producer differs from real native DEC StageOutcome")
                self.summary["workflowGate"].update({
                    "nativeWorkflowExecutionVerified": True,
                    "fixedProviderSourceSha256": provider_source_before,
                    "nativeDesignStageOutcomeVerified": True,
                    "twoSourceNativeApproval": native_evidence,
                    "nativeSkillTaskDir": str(skill_task_dir.resolve(strict=True)),
                    "nativeDecTaskDir": str(native_task_dir.resolve(strict=True)),
                    "nativeSkillRoot": str(native_opt_root.resolve(strict=True)),
                })
                self.record("workflow-gate", "TWO_NATIVE_DESIGNS_EVIDENCE_MATCHED",
                            {"skillRevision": native_evidence["skill"]["revision"],
                             "decRevision": native_evidence["dec"]["revision"]})
            elif native_opt_root is not None:
                bound_digest = verify_content_bound_revision(gate)
                native_evidence = validate_native_with_runner(self, native_opt_root, native_task_dir, gate)
                native_evidence["approvedDesignTreeSha256"] = bound_digest
                self.summary['workflowGate'].update({
                    'nativeWorkflowExecutionVerified': False,
                    'nativeDesignStageOutcomeVerified': True,
                    'nativeEvidence': native_evidence,
                    'nativeSkillRoot': str(native_opt_root.resolve()),
                    'nativeTaskDir': str(native_task_dir.resolve())})
                self.record('workflow-gate', 'NATIVE_STAGE_OUTCOME_VERIFIED',
                            {'revision': verified['gateRevision'],
                             'nativeStageOutcomeId': native_evidence['stageOutcomeId']})
            else:
                self.record('workflow-gate', 'FIXTURE_ONLY' if fixture else 'EXTERNAL_EVIDENCE_UNVERIFIED',
                            {'revision': verified['gateRevision'],
                             'note': 'No native CLI StageOutcome checked; the gate JSON is insufficient for P0 acceptance'})
            root = self.dec_root
            design = root / 'demo/order-payment-yaml'
            binding = root / 'demo/order-payment-implementation-binding.yaml'
            project = root / 'demo/order-payment-app'
            design_cli = root / 'skills/dec-design/scripts'
            impl_cli = root / 'skills/dec-implementation/scripts'
            mvnw = root / 'dec-java-lite/mvnw'
            pom = root / 'dec-java-lite/pom.xml'
            cli_jar = root / 'dec-java-lite/dec-lite-cli/target/dec-lite-cli-0.1.0.jar'
            self.command('dec-design', 'validate', [sys.executable, str(design_cli / 'validate_dec_yaml.py'), str(design)])
            self.command('dec-design', 'converter-check', [sys.executable, str(design_cli / 'yaml_to_xml.py'), str(design), '--check'])
            html = self.output / 'design-html'
            self.command('dec-design', 'render-html', [sys.executable, str(design_cli / 'render_dec_graph.py'), str(design), '-o', str(html)])
            self.artifact('dec/canonical-yaml/v1', design)
            self.artifact('dec/generated-html', html)
            # Before running implementation, pin the design gate again against the current inputs.
            check_gate(gate, root, allow_fixture=fixture)
            if self.static_only:
                self.record('dec-java-lite', 'NOT_RUN', {'reason': '--static-only'})
            else:
                self.command('dec-java-lite', 'install-runtime', [str(mvnw), '-f', str(pom), 'install', '-DskipTests'])
                self.command('dec-java-lite', 'inspect', ['java', '-jar', str(cli_jar), 'inspect', '--yaml', str(design)])
                generated = self.output / 'generated-java'
                self.command('dec-java-lite', 'generate', ['java', '-jar', str(cli_jar), 'generate', '--yaml', str(design),
                                                        '--output', str(generated), '--base-package', 'com.example.p0demo'])
                self.command('dec-java-lite', 'test-generated', [str(mvnw), '-f', str(generated / 'pom.xml'), 'test'])
                self.artifact('java/generated-source', generated)
            self.command('dec-implementation', 'binding-static', [sys.executable, str(impl_cli / 'validate_binding.py'),
                        '--design', str(design), '--binding', str(binding), '--project-root', str(project),
                        '--require-complete', '--require-tests', '--require-symbols'])
            self.artifact('dec/implementation-binding/v1', binding)
            if self.static_only:
                self.record('binding-evidence', 'NOT_RUN', {'reason': '--static-only: no test execution'})
                self.record('release-readiness', 'NOT_RUN', {'reason': '--static-only'})
                self.summary['integrationStatus'] = 'PARTIAL_STATIC_ONLY'
            else:
                self.command('binding-evidence', 'real-tests', [sys.executable, str(impl_cli / 'run_binding_verification.py'),
                             '--design', str(design), '--binding', str(binding), '--project-root', str(project),
                             '--input', '../../dec-java-lite', '--input', '../../skills/dec-implementation', '--',
                             '../../dec-java-lite/mvnw', '-q', 'clean', 'test'])
                self.command('binding-evidence', 'evidence-check', [sys.executable, str(impl_cli / 'validate_binding.py'),
                             '--design', str(design), '--binding', str(binding), '--project-root', str(project),
                             '--require-complete', '--require-evidence'])
                evidence = project / 'target/dec-binding-evidence.json'
                self.artifact('dec/test-evidence/v1', evidence)
                # --require-ready is a true release gate; its failure is recorded, not bypassed.
                ready = self.command('release-readiness', 'require-ready', [sys.executable,
                             str(impl_cli / 'validate_binding.py'), '--design', str(design), '--binding', str(binding),
                             '--project-root', str(project), '--require-ready'], allow_failure=True)
                self.summary['productReleaseReady'] = ready == 0
                self.summary['integrationStatus'] = ('VERIFIED_WITH_FIXTURE' if fixture else
                    'DEC_VERIFIED_NATIVE_GATE_CONSUMED' if native_opt_root is not None else
                    'DEC_VERIFIED_EXTERNAL_GATE_CONSUMED')
                if native_opt_root is not None:
                    self.summary['p0AcceptanceStatus'] = 'NATIVE_HANDOFF_VERIFIED_DUAL_SKILL_REGRESSION_PENDING'
            check_gate(gate, root, allow_fixture=fixture)
            if dual_binding is not None:
                # Re-query both native ledgers and source digests AFTER every
                # Provider/JUnit command. Reject reopen or source mutations
                # during the run, not just at initial Gate dispatch.
                after = verify_two_sources(dual_binding, native_opt_root, skill_task_dir,
                                           native_task_dir, skill_design_source, root)
                if after != native_evidence:
                    raise ValueError("native dual-source approvals changed during Provider run")
                if _provider_source_digest(root) != provider_source_before:
                    raise ValueError("fixed Provider executable sources changed during Provider run")
                self.summary["workflowGate"]["twoSourceNativeApproval"] = after
                if not self.static_only:
                    self.summary["integrationStatus"] = "DEC_VERIFIED_TWO_NATIVE_SOURCES_CONSUMED"
                    self.summary["p0AcceptanceStatus"] = "NATIVE_TWO_SOURCE_HANDOFF_VERIFIED_LIFECYCLE_PENDING"
                    self.record("workflow-gate", "TWO_NATIVE_SOURCES_RECHECKED_AFTER_PROVIDERS")
        except Exception as exc:
            self.summary['integrationStatus'] = 'BLOCKED'
            self.record('stop', 'BLOCKED', {'reason': str(exc)})
        self.summary['finishedAt'] = utc_now()
        atomic_json(self.output / 'p0-report.json', self.summary)
        return self.summary


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description='P0 DEC integration: no native workflow gates are fabricated')
    p.add_argument('--dec-root', type=Path, required=True, help='local checkout of doc-eq-code-Dgremlin-skills')
    p.add_argument('--output', type=Path, required=True, help='run directory outside DEC checkout')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--gate', type=Path, help='external common-develop-opt design gate JSON')
    g.add_argument('--demo-fixture-gate', action='store_true', help='explicit synthetic gate: never production evidence')
    p.add_argument('--native-opt-root', type=Path,
                   help='actual common-develop-opt Skill root; verifies native CLI (never an arbitrary JSON claim)')
    p.add_argument('--native-task-dir', type=Path,
                   help='actual common-develop-opt task root with finalized design StageOutcome')
    p.add_argument('--dual-binding', type=Path,
                   help='separate original native Skill and DEC Design StageOutcome references')
    p.add_argument('--skill-task-dir', type=Path,
                   help='the separately reviewed Skill architecture native Task')
    p.add_argument('--skill-design-source', type=Path,
                   help='exact Skill design file/directory reviewed by its native Design Reviewer')
    p.add_argument('--static-only', action='store_true', help='skip generator and real tests, result always PARTIAL')
    args = p.parse_args(argv)
    try:
        if (args.native_opt_root is None) != (args.native_task_dir is None):
            raise ValueError('--native-opt-root and --native-task-dir are required together')
        if args.demo_fixture_gate and args.native_opt_root is not None:
            raise ValueError('synthetic gate cannot be accepted as native evidence')
        if args.dual_binding is not None:
            if args.demo_fixture_gate or args.native_opt_root is None or args.native_task_dir is None:
                raise ValueError('dual-source mode requires real native opt + DEC task and external native Gate')
            if args.skill_task_dir is None or args.skill_design_source is None:
                raise ValueError('dual-source mode requires Skill task and design source')
        elif args.skill_task_dir is not None or args.skill_design_source is not None:
            raise ValueError('Skill task/source arguments require --dual-binding')
        root = args.dec_root.resolve(strict=True)
        gate = demo_gate(root) if args.demo_fixture_gate else json.loads(args.gate.read_text(encoding='utf-8'))
        result = Runner(root, args.output, args.static_only).execute(
            gate, fixture=args.demo_fixture_gate,
            native_opt_root=args.native_opt_root, native_task_dir=args.native_task_dir,
            dual_binding=json.loads(args.dual_binding.read_text(encoding='utf-8')) if args.dual_binding else None,
            skill_task_dir=args.skill_task_dir, skill_design_source=args.skill_design_source)
        print(json.dumps({'integrationStatus': result['integrationStatus'], 'report': str((args.output / 'p0-report.json').resolve())}, ensure_ascii=False))
        return 1 if result['integrationStatus'] == 'BLOCKED' else 0
    except (ValueError, FileNotFoundError, OSError, json.JSONDecodeError) as exc:
        print('BLOCKED: {}'.format(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
