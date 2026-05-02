from __future__ import annotations

from instrument_harness_lab.domain import CalibrationResult, PointPrediction, StandardPoint

MIN_R_SQUARED = 0.995
MAX_ABSOLUTE_ERROR = 1.5


def fit_linear_calibration(points: tuple[StandardPoint, ...]) -> CalibrationResult:
    if len(points) < 2:
        raise ValueError("at least two standard points are required")

    mean_x = sum(point.measured_intensity for point in points) / len(points)
    mean_y = sum(point.concentration for point in points) / len(points)
    numerator = sum(
        (point.measured_intensity - mean_x) * (point.concentration - mean_y) for point in points
    )
    denominator = sum((point.measured_intensity - mean_x) ** 2 for point in points)
    if denominator == 0:
        raise ValueError("measured intensities must not all be identical")

    slope = numerator / denominator
    intercept = mean_y - slope * mean_x
    predictions = _predict_points(points=points, slope=slope, intercept=intercept)
    r_squared = _r_squared(points=points, predictions=predictions)
    max_error = max(prediction.absolute_error for prediction in predictions)

    return CalibrationResult(
        slope=slope,
        intercept=intercept,
        r_squared=r_squared,
        max_absolute_error=max_error,
        accepted=r_squared >= MIN_R_SQUARED and max_error <= MAX_ABSOLUTE_ERROR,
        points=predictions,
    )


def _predict_points(
    points: tuple[StandardPoint, ...],
    slope: float,
    intercept: float,
) -> tuple[PointPrediction, ...]:
    predictions: list[PointPrediction] = []
    for point in points:
        predicted = slope * point.measured_intensity + intercept
        predictions.append(
            PointPrediction(
                concentration=point.concentration,
                measured_intensity=point.measured_intensity,
                predicted_concentration=predicted,
                absolute_error=abs(point.concentration - predicted),
            )
        )
    return tuple(predictions)


def _r_squared(
    points: tuple[StandardPoint, ...],
    predictions: tuple[PointPrediction, ...],
) -> float:
    mean_y = sum(point.concentration for point in points) / len(points)
    total_sum_squares = sum((point.concentration - mean_y) ** 2 for point in points)
    residual_sum_squares = sum(
        (point.concentration - prediction.predicted_concentration) ** 2
        for point, prediction in zip(points, predictions, strict=True)
    )
    if total_sum_squares == 0:
        return 1.0
    return 1 - residual_sum_squares / total_sum_squares
