"""Finite local zero-flow model.

This module implements the local finite model

    dx_j/dt = 2 * sum_{k != j} 1/(x_j - x_k)

as a heuristic diagnostic. It is not the full heat-deformed H_t equation.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from riemann_lab.data.schemas import ZeroBlock
from riemann_lab.lehmer.index import naive_lambda_scale


@dataclass(frozen=True)
class FiniteFlowResult:
    """Finite local zero-flow summary for one pair and radius."""

    left_index: int
    right_index: int
    radius: int
    pair_gap: float
    dgap_dt0_finite_flow: float
    naive_pair_collision_t: float
    linearized_collision_t: float
    finite_threshold_t: float
    window_zero_count: int


def finite_flow_velocities(offsets: list[float]) -> list[float]:
    """Compute velocities for the finite local model."""

    velocities: list[float] = []
    for j, xj in enumerate(offsets):
        total = 0.0
        for k, xk in enumerate(offsets):
            if j == k:
                continue
            total += 1.0 / (xj - xk)
        velocities.append(2.0 * total)
    return velocities


def naive_two_body_collision_time(delta: Decimal | float | str) -> float:
    """Return the two-body heuristic scale ``-Delta^2/8``."""

    return float(naive_lambda_scale(delta))


def analyze_finite_flow(block: ZeroBlock, left_index: int, radius: int = 80) -> FiniteFlowResult:
    """Analyze one candidate in the finite local zero-flow model."""

    pair_pos = block.position_of(left_index)
    lo, _hi, window_dec = block.local_offsets(left_index, radius)
    window = [float(value) for value in window_dec]
    pair_pos_window = pair_pos - lo
    velocities = finite_flow_velocities(window)
    gap = window[pair_pos_window + 1] - window[pair_pos_window]
    dgap_dt = velocities[pair_pos_window + 1] - velocities[pair_pos_window]
    linear = float("nan") if dgap_dt <= 0 else -gap / dgap_dt
    # Since d(gap^2)/dt = 2 gap gap', this finite local scale is comparable
    # to -gap^2/8 for a clean two-body near-collision.
    finite_threshold = float("nan") if dgap_dt <= 0 else -(gap * gap) / (2.0 * gap * dgap_dt)
    return FiniteFlowResult(
        left_index=left_index,
        right_index=left_index + 1,
        radius=radius,
        pair_gap=gap,
        dgap_dt0_finite_flow=dgap_dt,
        naive_pair_collision_t=naive_two_body_collision_time(block.gap_at(left_index)),
        linearized_collision_t=linear,
        finite_threshold_t=finite_threshold,
        window_zero_count=len(window),
    )

