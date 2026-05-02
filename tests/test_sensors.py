from __future__ import annotations

from pathlib import Path

import pytest

from instrument_harness_lab.sensors import run_feedback
from instrument_harness_lab.sensors.architecture_sensor import check_architecture
from instrument_harness_lab.sensors.maintainability_sensor import check_maintainability


def test_architecture_sensor_passes_current_codebase() -> None:
    violations = check_architecture(Path("src"))

    assert violations == []


def test_maintainability_sensor_passes_current_codebase() -> None:
    violations = check_maintainability(Path("src"))

    assert violations == []


def test_sensor_runner_passes_without_tests(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["harness-sensors"])

    run_feedback.main()

    assert "[sensor-pass]" in capsys.readouterr().out


def test_sensor_runner_fails_when_pytest_fails(monkeypatch) -> None:
    class FailedProcess:
        returncode = 1

    monkeypatch.setattr("sys.argv", ["harness-sensors", "--with-tests"])
    monkeypatch.setattr(run_feedback.subprocess, "run", lambda *args, **kwargs: FailedProcess())

    with pytest.raises(SystemExit):
        run_feedback.main()
