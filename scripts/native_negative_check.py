#!/usr/bin/env python3
"""Live, fail-closed negative test against the *actual* Gitee common-develop-opt CLI.

Creates a disposable task using the native init command. A schema-valid empty task
must NEVER be accepted as an approved design handoff. This is deliberately NOT a
positive end-to-end dual-Skill workflow validation.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from native_gate import native_commands, interpret_native_evidence


def run_json(argv, cwd):
    result = subprocess.run(argv, cwd=str(cwd), text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError("native command failed: {}: {}".format(" ".join(argv), result.stderr[-1000:]))
    return json.loads(result.stdout)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--opt-root", required=True, type=Path)
    args = p.parse_args()
    root = args.opt_root.resolve(strict=True)
    validator = root / "scripts/long_task.py"
    with tempfile.TemporaryDirectory(prefix="p0-opt-native-negative-") as tmp:
        doc_root = Path(tmp)
        task_dir = doc_root / "version/V_1.0/task/P0-NATIVE-NEGATIVE"
        init = subprocess.run([sys.executable, str(validator), "init", "-g",
                "ProjectManagerAgent", "--doc-root", str(doc_root), "--version", "V_1.0",
                "--target", "P0-NATIVE-NEGATIVE", "--json"], cwd=str(root),
                text=True, capture_output=True, check=False)
        if init.returncode:
            raise RuntimeError("native init failed: " + init.stderr[-1200:])
        commands = native_commands(root, task_dir)
        validation = run_json(commands["validate"], root)
        events = run_json(commands["events"], root)
        if validation.get("status") != "PASSED":
            raise RuntimeError("expected schema-valid initial task, got " + str(validation))
        fake_gate = {"revision": "SYNTHETIC-NOT-NATIVE", "producer": "DesignAgent"}
        try:
            interpret_native_evidence(validation, events, fake_gate)
        except ValueError as exc:
            if "no native finalized design StageOutcome" not in str(exc):
                raise
            print(json.dumps({"liveNativeCli": "PASSED", "fakeDesignGate": "BLOCKED",
                "nativeFinalizationPresent": False, "reason": str(exc)}, ensure_ascii=False))
            return 0
        raise RuntimeError("SAFETY REGRESSION: native empty task wrongly accepted as design PASSED")


if __name__ == "__main__":
    sys.exit(main())
