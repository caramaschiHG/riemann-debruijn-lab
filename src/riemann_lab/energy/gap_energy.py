"""Experimental inverse-gap energy diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from riemann_lab.data.schemas import ZeroBlock


@dataclass(frozen=True)
class GapEnergyResult:
    """One weighted inverse-gap energy value."""

    alpha: float
    energy: float
    gap_count: int
    weight: str


def inverse_gap_energy(block: ZeroBlock, alpha: float = 2.0, *, weight: str = "index") -> GapEnergyResult:
    """Compute ``sum w_j / g_j^2`` for experimental diagnostics.

    Supported weights:
    - ``index``: w_j = 1 / j^alpha
    - ``none``: w_j = 1
    """

    if alpha < 0:
        raise ValueError("alpha must be non-negative")
    energy = 0.0
    for pos in range(block.zero_count - 1):
        gap = float(block.offsets[pos + 1] - block.offsets[pos])
        if gap <= 0:
            raise ValueError("zero offsets must be strictly increasing")
        if weight == "index":
            global_index = block.start_index + pos
            w = 1.0 / (global_index**alpha)
        elif weight == "none":
            w = 1.0
        else:
            raise ValueError("weight must be 'index' or 'none'")
        energy += w / (gap * gap)
    return GapEnergyResult(alpha=alpha, energy=energy, gap_count=block.zero_count - 1, weight=weight)


def local_inverse_gap_energy(block: ZeroBlock, left_index: int, radius: int = 80) -> float:
    """Compute local unweighted inverse-gap energy around a candidate."""

    pair_pos = block.position_of(left_index)
    lo = max(0, pair_pos - radius)
    hi = min(block.zero_count - 2, pair_pos + radius)
    total = Decimal(0)
    for pos in range(lo, hi + 1):
        gap = block.offsets[pos + 1] - block.offsets[pos]
        total += Decimal(1) / (gap * gap)
    return float(total)

