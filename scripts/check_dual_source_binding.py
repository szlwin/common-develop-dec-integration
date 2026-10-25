#!/usr/bin/env python3
"""Fail-closed TWO-NATIVE-SOURCE design binding preflight for Skill A+B.

This is a read-only EVIDENCE CHECKER, not a StageOutcome generator or an
approval exporter. It cannot attest that an independent reviewer really read
the identified material; authoritative scope approval belongs to the native
Reviewer and its immutable evidence.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    from native_gate import interpret_native_evidence, native_commands, require_p0_current_requirement_trace
    from p0_integration import digest_path
except ImportError:
    from scripts.native_gate import interpret_native_evidence, native_commands, require_p0_current_requirement_trace
    from scripts.p0_integration import digest_path

SHA = re.compile(r"^[a-f0-9]{64}$")
SCHEMA = "common-develop-dec/dual-source-design-binding/v1"
DEC_PATH = "demo/order-payment-yaml"
PINNED_DEC = "4fb21242498746365c201fdf2a7fd8052f3a122a"


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _assert_pinned_dec_checkout(dec_root):
    """Reject dirty/current-main substitutions for the reviewed fixed DEC tree."""
    def run(argv):
        result = subprocess.run(argv, capture_output=True, text=True)
        if result.returncode:
            raise ValueError("DEC checkout Git evidence unavailable")
        return result.stdout.strip()
    head = run(["git", "-C", str(dec_root), "rev-parse", "HEAD"])
    if head != PINNED_DEC:
        raise ValueError("DEC source commit differs from audited pin")
    # This is executable Provider provenance, not just design YAML integrity.
    # Check the entire fixed checkout before running any generator scripts.
    dirty = run(["git", "-C", str(dec_root), "status", "--porcelain", "--untracked-files=all"])
    if dirty:
        raise ValueError("DEC Provider checkout is dirty (YAML, scripts, generators or untracked files)")


def _provider_source_digest(dec_root):
    """Hash fixed tracked executable Provider sources, not generated target/ output."""
    p = subprocess.run(["git", "-C", str(dec_root), "ls-files", "-z"],
                       capture_output=True, check=False)
    if p.returncode:
        raise ValueError("DEC tracked Provider source list unavailable")
    prefixes = ("skills/dec-design/", "skills/dec-implementation/", "dec-java-lite/",
                "demo/order-payment-app/", "demo/order-payment-implementation-binding.yaml")
    files = sorted(item.decode("utf-8") for item in p.stdout.split(b"\0") if item
                   and item.decode("utf-8").startswith(prefixes))
    if not files:
        raise ValueError("DEC fixed Provider execution sources missing")
    h = hashlib.sha256()
    for name in files:
        target = (dec_root / name).resolve(strict=True)
        if dec_root.resolve() not in target.parents or not target.is_file() or target.is_symlink():
            raise ValueError("DEC tracked Provider source unsafe")
        h.update(name.encode("utf-8") + b"\0")
        h.update(hashlib.sha256(target.read_bytes()).digest())
    return h.hexdigest()


def _native_query(root, task):
    commands = native_commands(root, task)
    result = {}
    for kind, command in commands.items():
        p = subprocess.run(command, cwd=str(root), text=True, capture_output=True)
        if p.returncode:
            raise ValueError("native " + kind + " failed: " + (p.stdout + p.stderr)[-1200:])
        try:
            result[kind] = json.loads(p.stdout)
        except json.JSONDecodeError:
            raise ValueError("native " + kind + " was not valid JSON")
    return result


def _immutable_review_manifest(task, evidence_id, required, expected_digest):
    registry = task / "evidence/registry.jsonl"
    if not registry.is_file():
        raise ValueError("native scope Evidence registry missing")
    matches = [json.loads(line) for line in registry.read_text(encoding="utf-8").splitlines()
               if line.strip() and json.loads(line).get("evidence_id") == evidence_id]
    if len(matches) != 1:
        raise ValueError("native reviewed scope Evidence ID not unique/found")
    record = matches[0]
    if record.get("type") != "design_ref" or record.get("capture_mode") != "SNAPSHOT":
        raise ValueError("native review scope must be immutable design_ref SNAPSHOT")
    relative = Path(record.get("ref") or "")
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("native scope snapshot path unsafe")
    resolved = (task / relative).resolve(strict=True)
    if task.resolve() not in resolved.parents or not resolved.is_file():
        raise ValueError("native scope snapshot escapes task")
    body = resolved.read_bytes()
    if hashlib.sha256(body).hexdigest() != record.get("digest"):
        raise ValueError("native scope snapshot digest mismatch")
    try:
        manifest = json.loads(body)
    except (ValueError, UnicodeDecodeError):
        raise ValueError("native design scope snapshot is not JSON")
    for key, value in required.items():
        if manifest.get(key) != value:
            raise ValueError("native design scope manifest " + key + " mismatch")
    if manifest.get("sourceSha256") != expected_digest:
        raise ValueError("review scope does not name approved content digest")
    return record.get("digest")


def verify(binding, opt_root, skill_task, dec_task, skill_source, dec_root, query=_native_query):
    if not isinstance(binding, dict) or set(binding) != {"schema", "skill", "dec"}:
        raise ValueError("dual source schema/fields invalid")
    if binding["schema"] != SCHEMA:
        raise ValueError("unsupported dual-source binding schema")
    if skill_task.resolve() == dec_task.resolve():
        raise ValueError("Skill design and DEC design must use distinct native tasks")
    skill_sha = digest_path(skill_source)
    dec_design = dec_root / DEC_PATH
    dec_sha = digest_path(dec_design)
    expected_sources = (
        ("skill", skill_task, skill_sha, "skill-design"),
        ("dec", dec_task, dec_sha, "dec-yaml-design"),
    )
    # Validate identities and both byte digests first. Otherwise a missing
    # native StageOutcome can obscure stale/tampered second-source bytes.
    for kind, task, digest, scope in expected_sources:
        part = binding[kind]
        fields = {"taskId", "designRevision", "stageOutcomeId", "finalizationEventId",
                  "sourceSha256", "reviewScopeEvidenceId", "designSourceKind"}
        if not isinstance(part, dict) or set(part) != fields:
            raise ValueError(kind + ": missing/extra binding fields")
        if task.name != part["taskId"] or part["sourceSha256"] != digest:
            raise ValueError(kind + ": source digest or native Task identity mismatch")
        if part["designSourceKind"] != scope:
            raise ValueError(kind + ": review scope kind mismatch")
        if not SHA.fullmatch(digest) or part["designRevision"] != "sha256:" + digest:
            raise ValueError(kind + ": design revision not content-bound")
    results = {}
    for kind, task, digest, scope in expected_sources:
        part = binding[kind]
        facts = query(opt_root, task)
        events = facts["events"].get("events") or []
        finalized = [e for e in events if e.get("type") == "STAGE_OUTCOME_FINALIZED"
                     and (e.get("payload", {}).get("outcome") or {}).get("phase") == "design"]
        if not finalized:
            raise ValueError(kind + ": missing native finalized design")
        real = finalized[-1]["payload"]["outcome"]
        stage = interpret_native_evidence(facts["validate"], facts["events"], {
            "revision": part["designRevision"],
            "producer": real.get("produced_by_agent")})
        if stage["stageOutcomeId"] != part["stageOutcomeId"] or stage["eventId"] != part["finalizationEventId"]:
            raise ValueError(kind + ": native event identity mismatch")
        if part["reviewScopeEvidenceId"] not in stage["evidenceIds"]:
            raise ValueError(kind + ": approved StageOutcome does not bind reviewed scope Evidence")
        # Even a PASSED StageOutcome is insufficient if the immutable reviewed
        # source/scope does not name the exact bytes being consumed.
        manifest_fields = {"schema": "common-develop-dec/review-scope/v1",
                           "designSourceKind": scope, "taskId": task.name}
        _immutable_review_manifest(task, part["reviewScopeEvidenceId"], manifest_fields, digest)
        require_p0_current_requirement_trace(task)
        results[kind] = {"stageOutcomeId": stage["stageOutcomeId"],
                         "revision": stage["outputRevision"],
                         "digest": digest, "scopeEvidenceId": part["reviewScopeEvidenceId"]}
    # Even for successful mechanical checks, authority/isolation are decided by
    # the real upstream tool; never conflate this with P0 approval.
    return {"schema": SCHEMA, "status": "TWO_SOURCE_NATIVE_EVIDENCE_MATCHED",
            "skill": results["skill"], "dec": results["dec"],
            "p0AcceptanceStatus": "BLOCKED_PENDING_FULL_SKILL_ACCEPTANCE",
            "productReleaseReady": False,
            "reviewerScopeAuthority": "UPSTREAM_NATIVE_REVIEW_ONLY"}


def main():
    a = argparse.ArgumentParser(description="Read-only dual-source native evidence preflight")
    a.add_argument("--binding", type=Path, required=True)
    a.add_argument("--opt-root", type=Path, required=True)
    a.add_argument("--skill-task-dir", type=Path, required=True)
    a.add_argument("--dec-task-dir", type=Path, required=True)
    a.add_argument("--skill-design-source", type=Path, required=True)
    a.add_argument("--dec-root", type=Path, required=True)
    args = a.parse_args()
    try:
        if args.dec_root.resolve(strict=True) == args.skill_design_source.resolve(strict=True):
            raise ValueError("Skill design source must differ from DEC repo source")
        _assert_pinned_dec_checkout(args.dec_root.resolve(strict=True))
        result = verify(_read_json(args.binding), args.opt_root.resolve(strict=True),
                        args.skill_task_dir.resolve(strict=True),
                        args.dec_task_dir.resolve(strict=True),
                        args.skill_design_source.resolve(strict=True),
                        args.dec_root.resolve(strict=True))
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc),
                          "p0AcceptanceStatus": "BLOCKED"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
