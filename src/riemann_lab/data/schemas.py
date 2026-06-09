"""Schemas for zeta-zero data.

The central representation is ``ZeroBlock``: a large base height plus small
offsets. This makes high-zero computations resistant to float64 cancellation.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from typing import Iterable, Sequence

getcontext().prec = 50


DecimalLike = Decimal | int | float | str


def to_decimal(value: DecimalLike) -> Decimal:
    """Convert a numeric value to Decimal without routing through binary float text."""

    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(value)


@dataclass(frozen=True)
class ZeroPair:
    """Adjacent zero pair identified by global left and right indices."""

    left_index: int
    right_index: int

    @classmethod
    def adjacent(cls, left_index: int) -> "ZeroPair":
        return cls(left_index=left_index, right_index=left_index + 1)


@dataclass
class ZeroBlock:
    """A block of zeta-zero ordinates stored as base height plus offsets.

    ``offsets`` are the authoritative values for gap computations. Reports
    should warn when ``base_height`` is large or ``precision_note`` is nonempty.
    """

    name: str
    start_index: int
    base_height: Decimal | str | int | float
    offsets: Sequence[Decimal]
    precision_note: str = ""
    source: str = ""

    def __post_init__(self) -> None:
        self.base_height = to_decimal(self.base_height)
        self.offsets = [to_decimal(value) for value in self.offsets]
        if len(self.offsets) < 2:
            raise ValueError("ZeroBlock requires at least two offsets")

    @property
    def end_index(self) -> int:
        return self.start_index + len(self.offsets) - 1

    @property
    def zero_count(self) -> int:
        return len(self.offsets)

    @property
    def uses_high_base(self) -> bool:
        return abs(self.base_height) >= Decimal("1e12")

    def position_of(self, global_index: int) -> int:
        pos = global_index - self.start_index
        if pos < 0 or pos >= len(self.offsets):
            raise IndexError(
                f"zero index {global_index} is outside block "
                f"{self.start_index}..{self.end_index}"
            )
        return pos

    def offset_at(self, global_index: int) -> Decimal:
        """Return the small offset for a global zero index."""

        return self.offsets[self.position_of(global_index)]

    def height_at(self, global_index: int) -> Decimal:
        """Return the high-precision absolute height for reporting."""

        return self.base_height + self.offset_at(global_index)

    def gap_at(self, left_index: int) -> Decimal:
        """Compute an adjacent gap from offsets, not by subtracting float heights."""

        pos = self.position_of(left_index)
        if pos + 1 >= len(self.offsets):
            raise IndexError(f"zero index {left_index} has no right neighbor in block")
        return self.offsets[pos + 1] - self.offsets[pos]

    def local_offsets(self, left_index: int, radius: int | None) -> tuple[int, int, list[Decimal]]:
        """Return local offset window around an adjacent pair.

        The returned tuple is ``(lo_pos, hi_pos, offsets)`` with inclusive
        positions in the original block.
        """

        pos = self.position_of(left_index)
        if pos + 1 >= len(self.offsets):
            raise IndexError(f"zero index {left_index} has no right neighbor in block")
        if radius is None:
            lo = 0
            hi = len(self.offsets) - 1
        else:
            lo = max(0, pos - radius)
            hi = min(len(self.offsets) - 1, pos + 1 + radius)
        return lo, hi, list(self.offsets[lo : hi + 1])


def make_zero_block(
    name: str,
    start_index: int,
    base_height: DecimalLike,
    offsets: Iterable[DecimalLike],
    precision_note: str = "",
    source: str = "",
) -> ZeroBlock:
    """Construct a ``ZeroBlock`` while normalizing numeric inputs."""

    return ZeroBlock(
        name=name,
        start_index=start_index,
        base_height=to_decimal(base_height),
        offsets=[to_decimal(value) for value in offsets],
        precision_note=precision_note,
        source=source,
    )

