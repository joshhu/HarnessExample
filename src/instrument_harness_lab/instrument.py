from __future__ import annotations

import random
from dataclasses import dataclass

from instrument_harness_lab.domain import StandardPoint


@dataclass(frozen=True)
class InstrumentFixture:
    name: str
    slope: float
    intercept: float
    noise: float
    seed: int
    curvature: float = 0.0


FIXTURES: dict[str, InstrumentFixture] = {
    "stable": InstrumentFixture(
        name="stable",
        slope=2.05,
        intercept=0.8,
        noise=0.18,
        seed=20260502,
    ),
    "drifted": InstrumentFixture(
        name="drifted",
        slope=2.05,
        intercept=0.8,
        noise=1.0,
        seed=20260502,
        curvature=0.03,
    ),
}


class SpectrometerSimulator:
    def __init__(self, fixture: InstrumentFixture) -> None:
        self._fixture = fixture

    def scan(self, concentrations: tuple[float, ...]) -> tuple[StandardPoint, ...]:
        rng = random.Random(self._fixture.seed)
        points: list[StandardPoint] = []
        for concentration in concentrations:
            drift = self._fixture.curvature * (concentration - 50.0) ** 2
            ideal = self._fixture.slope * concentration + self._fixture.intercept + drift
            measured = ideal + rng.uniform(-self._fixture.noise, self._fixture.noise)
            points.append(StandardPoint(concentration=concentration, measured_intensity=measured))
        return tuple(points)


def get_fixture(name: str) -> InstrumentFixture:
    try:
        return FIXTURES[name]
    except KeyError as exc:
        available = ", ".join(sorted(FIXTURES))
        raise ValueError(f"unknown fixture '{name}', available fixtures: {available}") from exc
