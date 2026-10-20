#!/usr/bin/env python3
"""Prepare an immutable DEC design review *candidate*, never an approval.

This intentionally cannot write a StageOutcome, change canonical YAML/XML,
or manufacture a common-develop-opt PASSED Gate. An independent Reviewer must
inspect and approve the exact digest via the upstream native workflow.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from p0_integration import digest_path

ROOT_REL = "demo/order-payment-yaml"
EXPECTED_FILE_COUNT = 10
DEFAULT_DEC_PIN = "4fb21242498746365c201fdf2a7fd8052f3a122a"


def build_packet(root: Path, source_revision: str) -> dict:
    root = root.resolve(strict=True)
    design = root / ROOT_REL
    if not design.is_dir():
        raise ValueError("missing canonical order-payment YAML directory")
    actual = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", actual):
        raise ValueError("invalid upstream DEC Git commit")
    if source_revision and actual != source_revision:
        raise ValueError("DEC source commit changed; review new revision first")
    yaml_files = sorted(f for f in design.iterdir() if f.suffix in (".yaml", ".yml") and f.is_file())
    if len(yaml_files) != EXPECTED_FILE_COUNT:
        raise ValueError("unexpected canonical design file count")
    # The review digest must describe exactly the pinned tracked source bytes.
    # A clean HEAD alone does not prove the checkout contains no local edits.
    dirty = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--", ROOT_REL],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    if dirty:
        raise ValueError("DEC canonical source is modified/untracked; independent review requires clean pinned bytes")
    included = sorted(
        f for f in design.rglob("*") if f.is_file()
        and not any(part in {".git", "target", "build", ".gradle", "__pycache__", ".idea", ".mvn", "node_modules"}
                    for part in f.relative_to(design).parts)
    )
    if {f.resolve() for f in included} != {f.resolve() for f in yaml_files}:
        raise ValueError("DEC canonical tree contains files beyond the ten reviewed YAMLs")
    digest = digest_path(design)
    files = [{"path": f"{ROOT_REL}/{f.name}", "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
             for f in yaml_files]
    if digest != digest_path(design):
        raise ValueError("canonical YAML mutated during candidate preparation")
    return {
        "schema": "common-develop-dec/p0-native-review-candidate/v1",
        "status": "AWAITING_INDEPENDENT_NATIVE_REVIEW",
        "approved": False,
        "nativeStageOutcomeId": None,
        "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repository": "szlwin/doc-eq-code-Dgremlin-skills",
        "sourceCommit": actual,
        "canonicalRoot": ROOT_REL,
        "designTreeSha256": digest,
        "proposedNativeOutputRevision": "sha256:" + digest,
        "files": files,
        "requiredNativeStages": ["requirement_confirmation", "requirement_analysis", "business_model", "design"],
        "requiredEvidence": [
            "Native PASSED attempts for all preceding required stages",
            "Design artifact published via common-develop-opt with this exact revision",
            "Independent Review results covering these exact canonical YAML bytes",
            "Latest finalized native design/PASSED StageOutcome with matching output_revision",
            "Native task-events history and long_task validate --json = PASSED",
            "Requirement input_revisions and linked genuine evidence_ids",
            "Native DEC downstream TDD, Development, Code Review, Testing and archive evidence",
        ],
        "productReleaseReady": False,
        "knownProductLimitations": [
            "4 / 111 DEC Design IDs remain PLANNED",
            "External payment provider, MongoDB, and SMS integrations use local demo substitutes"
        ],
        "warning": "THIS FILE IS ONLY A REVIEW CANDIDATE. DO NOT RELABEL OR IMPORT IT AS A PASSED STAGE OUTCOME."
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Prepare exact DEC design candidate for upstream independent review")
    ap.add_argument("--dec-root", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--expected-dec-commit", default=DEFAULT_DEC_PIN)
    args = ap.parse_args()
    try:
        if args.output.resolve() == args.dec_root.resolve() or args.dec_root.resolve() in args.output.resolve().parents:
            raise ValueError("review output must be outside DEC source checkout")
        packet = build_packet(args.dec_root, args.expected_dec_commit)
        args.output.mkdir(parents=True, exist_ok=True)
        target = args.output / "p0-native-review-candidate.json"
        target.write_text(json.dumps(packet, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"candidate": str(target), "status": packet["status"],
                          "designSha256": packet["designTreeSha256"], "fileCount": len(packet["files"])},
                         ensure_ascii=False))
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        print("REVIEW CANDIDATE BLOCKED: " + str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
