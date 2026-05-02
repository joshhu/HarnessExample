from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StandardPoint:
    concentration: float
    measured_intensity: float


@dataclass(frozen=True)
class PointPrediction:
    concentration: float
    measured_intensity: float
    predicted_concentration: float
    absolute_error: float


@dataclass(frozen=True)
class CalibrationResult:
    slope: float
    intercept: float
    r_squared: float
    max_absolute_error: float
    accepted: bool
    points: tuple[PointPrediction, ...]
