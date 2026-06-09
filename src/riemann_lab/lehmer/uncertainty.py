"""Endpoint uncertainty stress tests for g_bar upper bounds."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from riemann_lab.data.schemas import to_decimal


@dataclass(frozen=True)
class UncertaintyStressResult:
    """Worst-case endpoint perturbation summary."""

    gbar_upper: Decimal
    gap_delta: Decimal
    epsilon: Decimal
    worst_gap_delta: Decimal
    stressed_gbar_upper: Decimal
    multiplier: Decimal
    still_below_threshold: bool


def stress_gbar_upper(
    gbar_upper: Decimal | str | float,
    gap_delta: Decimal | str | float,
    epsilon: Decimal | str | float,
    *,
    threshold: Decimal | str | float = "0.8",
) -> UncertaintyStressResult:
    """Stress ``gbar_upper`` by allowing endpoints to increase the gap by 2*epsilon."""

    gbar = to_decimal(gbar_upper)
    gap = to_decimal(gap_delta)
    eps = to_decimal(epsilon)
    if gap <= 0:
        raise ValueError("gap_delta must be positive")
    if eps < 0:
        raise ValueError("epsilon must be non-negative")
    worst_gap = gap + Decimal(2) * eps
    multiplier = (worst_gap / gap) ** 2
    stressed = gbar * multiplier
    return UncertaintyStressResult(
        gbar_upper=gbar,
        gap_delta=gap,
        epsilon=eps,
        worst_gap_delta=worst_gap,
        stressed_gbar_upper=stressed,
        multiplier=multiplier,
        still_below_threshold=stressed < to_decimal(threshold),
    )

