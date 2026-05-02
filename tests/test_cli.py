from __future__ import annotations

import json

from instrument_harness_lab import cli


def test_cli_outputs_calibration_certificate(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["instrument-lab", "calibrate", "--fixture", "stable"])

    cli.main()

    certificate = json.loads(capsys.readouterr().out)
    assert certificate["accepted"] is True
    assert "r_squared" in certificate
    assert len(certificate["points"]) == 5
