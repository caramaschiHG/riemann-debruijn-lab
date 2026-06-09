"""Gap records and ranking utilities."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from riemann_lab.data.schemas import ZeroBlock
from .normalize import normalized_gap


@dataclass(frozen=True)
class GapRecord:
    """One adjacent gap and numerical normalized-gap diagnostic."""

    left_index: int
    right_index: int
    left_offset: Decimal
    right_offset: Decimal
    gap: Decimal
    mid_height: Decimal
    normalized_gap: float


def compute_gaps(block: ZeroBlock) -> list[GapRecord]:
    """Compute adjacent gaps from offsets for a zero block."""

    records: list[GapRecord] = []
    for pos in range(block.zero_count - 1):
        left_index = block.start_index + pos
        left = block.offsets[pos]
        right = block.offsets[pos + 1]
        gap = right - left
        mid = block.base_height + (left + right) / Decimal(2)
        records.append(
            GapRecord(
                left_index=left_index,
                right_index=left_index + 1,
                left_offset=left,
                right_offset=right,
                gap=gap,
                mid_height=mid,
                normalized_gap=normalized_gap(gap, mid),
            )
        )
    return records


def top_gaps(block: ZeroBlock, top: int = 25, by: str = "normalized_gap") -> list[GapRecord]:
    """Return smallest gaps ranked by raw or normalized gap."""

    if by not in {"gap", "normalized_gap"}:
        raise ValueError("by must be 'gap' or 'normalized_gap'")
    key = (lambda record: record.gap) if by == "gap" else (lambda record: record.normalized_gap)
    return sorted(compute_gaps(block), key=key)[:top]

