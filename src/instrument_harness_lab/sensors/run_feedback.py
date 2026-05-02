from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from instrument_harness_lab.sensors.architecture_sensor import check_architecture
from instrument_harness_lab.sensors.maintainability_sensor import check_maintainability


def main() -> None:
    parser = argparse.ArgumentParser(prog="harness-sensors")
    parser.add_argument("--with-tests", action="store_true", help="also run pytest")
    args = parser.parse_args()

    repo_root = Path.cwd()
    src_root = repo_root / "src"

    failures = []
    failures.extend(violation.message for violation in check_architecture(src_root))
    failures.extend(violation.message for violation in check_maintainability(src_root))

    if args.with_tests:
        completed = subprocess.run(["uv", "run", "pytest"], cwd=repo_root, check=False)
        if completed.returncode != 0:
            failures.append("pytest failed; inspect the test output above")

    if failures:
        for failure in failures:
            print(f"[sensor-fail] {failure}", file=sys.stderr)
        raise SystemExit(1)

    print("[sensor-pass] architecture, maintainability, and requested tests passed")
