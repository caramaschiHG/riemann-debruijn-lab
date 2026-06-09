"""Candidate-pair discovery from zero gaps."""

from __future__ import annotations

from dataclasses import dataclass

from riemann_lab.data.schemas import ZeroBlock
from riemann_lab.zeros.gaps import GapRecord, top_gaps
from .index import LehmerIndexResult, analyze_pair


@dataclass(frozen=True)
class CandidatePair:
    """Ranked adjacent pair candidate."""

    rank: int
    gap: GapRecord
    lehmer: LehmerIndexResult | None = None


def find_candidate_pairs(
    block: ZeroBlock,
    *,
    top: int = 25,
    radius: int | None = None,
    by: str = "normalized_gap",
) -> list[CandidatePair]:
    """Find candidate pairs by smallest raw or normalized gap."""

    pairs: list[CandidatePair] = []
    for rank, gap in enumerate(top_gaps(block, top=top, by=by), start=1):
        lehmer = analyze_pair(block, gap.left_index, radius=radius) if radius is not None else None
        pairs.append(CandidatePair(rank=rank, gap=gap, lehmer=lehmer))
    return pairs

