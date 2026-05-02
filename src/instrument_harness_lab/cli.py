from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from instrument_harness_lab.controller import calibrate_fixture


def main() -> None:
    parser = argparse.ArgumentParser(prog="instrument-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    calibrate_parser = subparsers.add_parser("calibrate", help="run a deterministic calibration")
    calibrate_parser.add_argument("--fixture", default="stable", help="fixture name")

    args = parser.parse_args()
    if args.command == "calibrate":
        result = calibrate_fixture(args.fixture)
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2, sort_keys=True))
