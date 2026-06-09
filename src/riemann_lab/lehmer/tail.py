"""Heuristic tail estimates for Lehmer G sums."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

import mpmath as mp

from riemann_lab.data.schemas import to_decimal


@dataclass(frozen=True)
class HeuristicTailResult:
    """Density-tail estimate; not a rigorous certificate."""

    left_tail_G: Decimal
    right_tail_G: Decimal
    total_tail_G: Decimal
    local_density: float


def local_zero_density(height: float | Decimal) -> float:
    """Approximate local zero density ``log(T/(2*pi))/(2*pi)``."""

    T = mp.mpf(str(to_decimal(height)))
    if T <= 2 * mp.pi:
        raise ValueError("height must exceed 2*pi")
    return float(mp.log(T / (2 * mp.pi)) / (2 * mp.pi))


def density_tail_G(
    a_offset: Decimal | str | float,
    b_offset: Decimal | str | float,
    left_edge_offset: Decimal | str | float,
    right_edge_offset: Decimal | str | float,
    mid_height: Decimal | str | float,
) -> HeuristicTailResult:
    """Estimate omitted G contribution by integrating local zero density.

    This is a heuristic density model and must be reported as such.
    """

    a = to_decimal(a_offset)
    b = to_decimal(b_offset)
    left_edge = to_decimal(left_edge_offset)
    right_edge = to_decimal(right_edge_offset)
    rho = Decimal(str(local_zero_density(to_decimal(mid_height))))
    left_dist_a = a - left_edge
    left_dist_b = b - left_edge
    right_dist_a = right_edge - a
    right_dist_b = right_edge - b
    if min(left_dist_a, left_dist_b, right_dist_a, right_dist_b) <= 0:
        raise ValueError("tail edges must lie outside the candidate pair")
    left = rho * (Decimal(1) / left_dist_a + Decimal(1) / left_dist_b)
    right = rho * (Decimal(1) / right_dist_a + Decimal(1) / right_dist_b)
    return HeuristicTailResult(
        left_tail_G=left,
        right_tail_G=right,
        total_tail_G=left + right,
        local_density=float(rho),
    )


def stress_multiplier_to_threshold(
    gbar_local: Decimal | str | float,
    tail_gbar_unit: Decimal | str | float,
    threshold: float = 0.8,
) -> Decimal:
    """Return tail multiplier required to reach the Lehmer threshold."""

    local = to_decimal(gbar_local)
    unit = to_decimal(tail_gbar_unit)
    if unit <= 0:
        return Decimal("Infinity")
    return (to_decimal(str(threshold)) - local) / unit
