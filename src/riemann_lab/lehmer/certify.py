"""Conditional Lehmer-pair tail estimate assembly."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from riemann_lab.constants import LEHMER_THRESHOLD
from riemann_lab.data.schemas import ZeroBlock, ZeroPair, to_decimal
from riemann_lab.constants import ClaimStrength
from .explicit_tail import ExplicitTailResult, TailBoundAssumptions, explicit_tail_bound_for_block
from .index import analyze_pair, compute_gbar


@dataclass(frozen=True)
class ConditionalTailEstimate:
    """Conditional tail estimate under explicit assumptions and limitations."""

    pair: ZeroPair
    delta: Decimal
    G_local: Decimal
    gbar_local: Decimal
    tail_result: ExplicitTailResult
    G_total_upper: Decimal
    gbar_upper: Decimal
    margin_to_threshold: Decimal
    still_below_threshold: bool
    precision_note: str
    assumptions: TailBoundAssumptions
    claim_strength: ClaimStrength


def estimate_candidate_tail(
    block: ZeroBlock,
    left_index: int,
    *,
    radius: int | None = None,
    q: float = 1.25,
    threshold: float = LEHMER_THRESHOLD,
) -> ConditionalTailEstimate:
    """Estimate a pair's tail contribution under stated assumptions."""

    local = analyze_pair(block, left_index, radius=radius)
    _, tail = explicit_tail_bound_for_block(block, left_index, radius=radius, q=q)
    G_total = local.G_local + tail.total_tail_G_bound
    gbar_upper = compute_gbar(local.delta, G_total)
    threshold_decimal = to_decimal(str(threshold))
    return ConditionalTailEstimate(
        pair=local.pair,
        delta=local.delta,
        G_local=local.G_local,
        gbar_local=local.gbar_local,
        tail_result=tail,
        G_total_upper=G_total,
        gbar_upper=gbar_upper,
        margin_to_threshold=threshold_decimal - gbar_upper,
        still_below_threshold=gbar_upper < threshold_decimal,
        precision_note=block.precision_note,
        assumptions=tail.assumptions,
        claim_strength=ClaimStrength.CONDITIONAL_STATEMENT,
    )


def certify_candidate(*args: object, **kwargs: object) -> ConditionalTailEstimate:
    """Backward-compatible alias; prefer ``estimate_candidate_tail`` in new code."""

    return estimate_candidate_tail(*args, **kwargs)
