"""Odlyzko zero-table metadata helpers."""

from __future__ import annotations

from .schemas import ZeroBlock, make_zero_block

ODLYZKO_SOURCE = "Odlyzko zeta zero tables"

HIGH_TABLE_WARNING = (
    "High-zero Odlyzko blocks can have limited displayed precision. Use "
    "base+offset arithmetic and include endpoint uncertainty stress tests."
)


def precision_warning_for_dataset(name: str) -> str:
    """Return a precision note appropriate for known dataset labels."""

    lowered = name.lower()
    if "1e21" in lowered or "10^21" in lowered or "10e21" in lowered:
        return HIGH_TABLE_WARNING
    if "1e12" in lowered or "10^12" in lowered:
        return "Use base+offset arithmetic; displayed offsets are the trusted gap source."
    return "Low-height table; float summaries may be acceptable, but gaps use offsets here."


def make_odlyzko_block(
    name: str,
    start_index: int,
    base_height: str,
    offsets: list[str],
    source: str = ODLYZKO_SOURCE,
) -> ZeroBlock:
    """Construct an Odlyzko ``ZeroBlock`` with a dataset-specific warning."""

    return make_zero_block(
        name=name,
        start_index=start_index,
        base_height=base_height,
        offsets=offsets,
        precision_note=precision_warning_for_dataset(name),
        source=source,
    )

