from __future__ import annotations

from instrument_harness_lab.calibration import fit_linear_calibration
from instrument_harness_lab.domain import CalibrationResult
from instrument_harness_lab.instrument import SpectrometerSimulator, get_fixture

DEFAULT_STANDARDS = (0.0, 25.0, 50.0, 75.0, 100.0)


def calibrate_fixture(
    fixture_name: str,
    standards: tuple[float, ...] = DEFAULT_STANDARDS,
) -> CalibrationResult:
    fixture = get_fixture(fixture_name)
    simulator = SpectrometerSimulator(fixture)
    points = simulator.scan(standards)
    return fit_linear_calibration(points)
