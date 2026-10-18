#!/usr/bin/env python3
"""Start a *real* common-develop-opt task; no synthetic approval or ledger edits.

This is a genuine invocation of the pinned upstream wk public CLI, and leaves the
task for its normal requirement, design and independent Review stages.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

FEATURE = (
    "P0 order-payment DEC fixed-provider interoperability: "
    "review the published 10 canonical design YAML files at "
    "4fb21242498746365c201fdf2a7fd8052f3a122a and their exact content digest; "
    "validate the real native requirement/design/independent Review lifecycle, "
    "consume its finalized StageOutcome in the fixed three-Provider DEC pipeline, "
    "and return generated code, Binding and JUnit evidence through subsequent "
    "native test_design, implementation_plan, development, code_review, testing, "
    "completion_verification and archive steps. This public Demo is not product-release-ready."
)


def launch(skill_root: Path, doc_root: Path, output_dir: Path):
    wk = (skill_root / "scripts/wk.py").resolve(strict=True)
    script_cwd = wk.parent.parent
    args = [sys.executable, str(wk), "start", "-g", "ProjectManagerAgent",
            "--doc-root", str(doc_root.resolve()), "--version", "V_P0",
            "-f", FEATURE, "--classification", "new-requirement",
            "--reason", "Independent native workflow acceptance of existing P0 integration",
            "--no-auto", "--apply", "--json"]
    result = subprocess.run(args, cwd=str(script_cwd), capture_output=True, text=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "native-wk-start.stdout.json").write_text(result.stdout, encoding="utf-8")
    (output_dir / "native-wk-start.stderr.log").write_text(result.stderr, encoding="utf-8")
    info = {"schema": "common-develop-dec/p0-real-native-task-bootstrap/v1",
            "status": "REAL_NATIVE_TASK_UNREVIEWED",
            "approved": False,
            "cli": "original common-develop-opt/scripts/wk.py start --apply",
            "cliExitCode": result.returncode,
            "nativeDesignGateVerified": False,
            "feature": FEATURE,
            "note": "Only native wk start may write task files; no independent Reviewer ran and no StageOutcome was created by this integration."}
    try:
        payload = json.loads(result.stdout)
        info["nativeStatus"] = payload.get("status")
        info["nativeNextAction"] = payload.get("nextAction") or payload.get("next_action")
        info["nativeNextReviewer"] = payload.get("nextReviewer")
    except (json.JSONDecodeError, AttributeError):
        info["nativeStatus"] = "NON_JSON"
    (output_dir / "bootstrap-status.json").write_text(
        json.dumps(info, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(info, ensure_ascii=False))
    if result.returncode:
        raise RuntimeError("Native wk start did not accept the task. Inspect native stdout/nextAction.")
    events = sorted(doc_root.rglob("task_events.jsonl"))
    print("Native append-only task ledgers discovered:", len(events))
    for p in events:
        print("Task ledger:", p.relative_to(doc_root))
    if not events:
        raise RuntimeError("Native wk start reported success but did not create a native task event ledger")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--skill-root", type=Path, required=True)
    p.add_argument("--doc-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    if a.output.resolve().is_relative_to(a.doc_root.resolve()):
        raise ValueError("Output must be outside native doc root")
    launch(a.skill_root, a.doc_root, a.output)


if __name__ == "__main__":
    main()
