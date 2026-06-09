"""Lehmer index calculations.

All local gaps are computed from offsets. Values using truncated windows are
reported as local or truncated diagnostics, not as the true infinite g_bar.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext

from riemann_lab.constants import LEHMER_THRESHOLD
from riemann_lab.data.schemas import ZeroBlock, ZeroPair, to_decimal
from riemann_lab.zeros.normalize import normalized_gap

getcontext().prec = 60


@dataclass(frozen=True)
class LehmerIndexResult:
    """Local or bounded Lehmer diagnostic for one adjacent pair."""

    pair: ZeroPair
    delta: Decimal
    midpoint_height: Decimal
    normalized_gap: float
    G_local: Decimal
    gbar_local: Decimal
    radius: int | None
    zeros_used_in_G: int
    edge_ok: bool

    @property
    def below_threshold_local(self) -> bool:
        return self.gbar_local < to_decimal(str(LEHMER_THRESHOLD))


def compute_gap(block: ZeroBlock, left_index: int) -> Decimal:
    """Return ``Delta = gamma_{n+1} - gamma_n`` using offsets."""

    return block.gap_at(left_index)


def compute_normalized_gap(block: ZeroBlock, left_index: int) -> float:
    """Return normalized gap using local average spacing at pair midpoint."""

    pos = block.position_of(left_index)
    midpoint = block.base_height + (block.offsets[pos] + block.offsets[pos + 1]) / Decimal(2)
    return normalized_gap(block.gap_at(left_index), midpoint)


def compute_G_local(block: ZeroBlock, left_index: int, radius: int | None = None) -> tuple[Decimal, int, bool]:
    """Compute local truncated G for a selected adjacent pair.

    The sum excludes the pair endpoints. When ``radius`` is not ``None``, the
    window includes at most ``radius`` zeros on each side. ``edge_ok`` is false
    if the requested radius was clipped by the available table.
    """

    pair_pos = block.position_of(left_index)
    if pair_pos + 1 >= block.zero_count:
        raise IndexError("left_index has no right neighbor in block")
    a = block.offsets[pair_pos]
    b = block.offsets[pair_pos + 1]
    lo, hi, window = block.local_offsets(left_index, radius)
    G = Decimal(0)
    zeros_used = 0
    for offset_pos, z in enumerate(window, start=lo):
        if offset_pos in (pair_pos, pair_pos + 1):
            continue
        G += Decimal(1) / ((z - a) ** 2) + Decimal(1) / ((z - b) ** 2)
        zeros_used += 1
    edge_ok = True
    if radius is not None:
        edge_ok = (pair_pos - radius >= 0) and (pair_pos + 1 + radius < block.zero_count)
    return G, zeros_used, edge_ok


def compute_gbar(delta: Decimal | str | float, G: Decimal | str | float) -> Decimal:
    """Compute ``g_bar = Delta^2 * G``."""

    d = to_decimal(delta)
    return d * d * to_decimal(G)


def is_lehmer_pair(gbar: Decimal | str | float, threshold: float = LEHMER_THRESHOLD) -> bool:
    """Return whether ``gbar`` is below the classical 4/5 threshold."""

    return to_decimal(gbar) < to_decimal(str(threshold))


def analyze_pair(block: ZeroBlock, left_index: int, radius: int | None = None) -> LehmerIndexResult:
    """Compute the local Lehmer diagnostic for one adjacent pair."""

    pair_pos = block.position_of(left_index)
    delta = block.gap_at(left_index)
    midpoint = block.base_height + (block.offsets[pair_pos] + block.offsets[pair_pos + 1]) / Decimal(2)
    G_local, zeros_used, edge_ok = compute_G_local(block, left_index, radius=radius)
    return LehmerIndexResult(
        pair=ZeroPair.adjacent(left_index),
        delta=delta,
        midpoint_height=midpoint,
        normalized_gap=normalized_gap(delta, midpoint),
        G_local=G_local,
        gbar_local=compute_gbar(delta, G_local),
        radius=radius,
        zeros_used_in_G=zeros_used,
        edge_ok=edge_ok,
    )


def naive_lambda_scale(delta: Decimal | str | float) -> Decimal:
    """Return the two-body scale ``-Delta^2/8`` used as a local heuristic."""

    d = to_decimal(delta)
    return -(d * d) / Decimal(8)

