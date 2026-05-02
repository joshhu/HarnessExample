from __future__ import annotations

import pytest

from instrument_harness_lab.calibration import fit_linear_calibration
from instrument_harness_lab.controller import calibrate_fixture
from instrument_harness_lab.domain import StandardPoint
from instrument_harness_lab.instrument import get_fixture


def test_stable_fixture_is_accepted() -> None:
    result = calibrate_fixture("stable")

    assert result.accepted is True
    assert result.r_squared >= 0.995
    assert result.max_absolute_error <= 1.5
    assert len(result.points) == 5


def test_drifted_fixture_is_rejected() -> None:
    result = calibrate_fixture("drifted")

    assert result.accepted is False
    assert result.max_absolute_error > 1.5


def test_calibration_keeps_traceable_point_predictions() -> None:
    result = calibrate_fixture("stable")

    for point in result.points:
        assert point.measured_intensity >= 0
        assert point.absolute_error >= 0
        assert isinstance(point.predicted_concentration, float)


def test_unknown_fixture_lists_available_fixtures() -> None:
    with pytest.raises(ValueError, match="available fixtures"):
        get_fixture("missing")


def test_calibration_requires_two_points() -> None:
    with pytest.raises(ValueError, match="at least two"):
        fit_linear_calibration((StandardPoint(concentration=1.0, measured_intensity=2.0),))


def test_calibration_rejects_identical_measurements() -> None:
    with pytest.raises(ValueError, match="must not all be identical"):
        fit_linear_calibration(
            (
                StandardPoint(concentration=1.0, measured_intensity=2.0),
                StandardPoint(concentration=2.0, measured_intensity=2.0),
            )
        )


def test_r_squared_is_perfect_when_concentrations_do_not_vary() -> None:
    result = fit_linear_calibration(
        (
            StandardPoint(concentration=1.0, measured_intensity=1.0),
            StandardPoint(concentration=1.0, measured_intensity=2.0),
        )
    )

    assert result.r_squared == 1.0
