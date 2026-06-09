"""Base+offset arithmetic helpers."""

from __future__ import annotations

from decimal import Decimal

from riemann_lab.data.schemas import ZeroBlock, to_decimal


def gap_from_offsets(left_offset: Decimal | str | float, right_offset: Decimal | str | float) -> Decimal:
    """Compute a gap from small offsets.

    This intentionally avoids subtracting absolute high ordinates represented
    as binary floats.
    """

    return to_decimal(right_offset) - to_decimal(left_offset)


def gap_at(block: ZeroBlock, left_index: int) -> Decimal:
    """Return the adjacent gap in ``block`` using offset arithmetic."""

    return block.gap_at(left_index)


def midpoint_height(block: ZeroBlock, left_index: int) -> Decimal:
    """Return the high-precision midpoint height for an adjacent pair."""

    left = block.offset_at(left_index)
    right = block.offset_at(left_index + 1)
    return block.base_height + (left + right) / Decimal(2)


def assert_no_float64_cancellation(block: ZeroBlock) -> None:
    """Raise when a high block has no precision note documenting the risk."""

    if block.uses_high_base and not block.precision_note:
        raise ValueError("High zero block requires a precision note and base+offset handling")


def unsafe_float_height_gap(block: ZeroBlock, left_index: int) -> float:
    """Demonstrate the float64 pattern that high-zero code must not use.

    This helper exists only for tests and audits. Production computations should
    use ``gap_at``.
    """

    left = float(block.height_at(left_index))
    right = float(block.height_at(left_index + 1))
    return right - left
