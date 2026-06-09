"""Experiment helpers for comparing gap-energy choices."""

from __future__ import annotations

from riemann_lab.data.schemas import ZeroBlock
from .gap_energy import GapEnergyResult, inverse_gap_energy


def compare_alphas(block: ZeroBlock, alphas: list[float], weight: str = "index") -> list[GapEnergyResult]:
    """Compute one energy value for each alpha."""

    return [inverse_gap_energy(block, alpha=alpha, weight=weight) for alpha in alphas]

