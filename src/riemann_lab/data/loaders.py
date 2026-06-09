"""Load zeta-zero blocks from text or CSV files."""

from __future__ import annotations

import csv
from decimal import Decimal
from pathlib import Path
from typing import Iterable

from .schemas import ZeroBlock, make_zero_block, to_decimal


def _split_numeric_line(line: str) -> list[str]:
    return [part for part in line.replace(",", " ").split() if part]


def load_offsets_text(path: Path | str, value_column: int = -1) -> list[Decimal]:
    """Load offsets from a whitespace or comma separated text file.

    Comment lines beginning with ``#`` are ignored. By default the final
    numeric column is used, which handles simple Odlyzko-style offset files.
    """

    offsets: list[Decimal] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = _split_numeric_line(line)
            offsets.append(to_decimal(parts[value_column]))
    if len(offsets) < 2:
        raise ValueError(f"{path} did not contain at least two offsets")
    return offsets


def load_offsets_csv(path: Path | str, offset_column: str | None = None) -> list[Decimal]:
    """Load offsets from a CSV file with an explicit or inferred offset column."""

    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no CSV header")
        candidates = [
            offset_column,
            "offset",
            "offset_left",
            "gamma",
            "height",
            "zero",
        ]
        column = next((name for name in candidates if name and name in reader.fieldnames), None)
        if column is None:
            raise ValueError(
                f"Could not infer offset column in {path}; fields are {reader.fieldnames}"
            )
        return [to_decimal(row[column]) for row in reader if row.get(column)]


def load_zero_block(
    path: Path | str,
    *,
    name: str | None = None,
    start_index: int = 1,
    base_height: str | int | float | Decimal = "0",
    offset_column: str | None = None,
    precision_note: str = "",
    source: str = "",
) -> ZeroBlock:
    """Load a zero block from text or CSV offsets.

    For high tables, pass the large common height in ``base_height`` and store
    only small offsets in the file. Gap computations then use offsets only.
    """

    path = Path(path)
    if path.suffix.lower() == ".csv":
        if offset_column is None:
            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                fields = set(reader.fieldnames or [])
            gap_fields = {"zero_index_left", "zero_index_right", "offset_left", "offset_right"}
            if gap_fields.issubset(fields):
                return load_zero_block_from_gap_csv(
                    path,
                    name=name or path.stem,
                    precision_note=precision_note,
                    source=source or str(path),
                )
        try:
            offsets = load_offsets_csv(path, offset_column=offset_column)
        except ValueError:
            return load_zero_block_from_gap_csv(
                path,
                name=name or path.stem,
                precision_note=precision_note,
                source=source or str(path),
            )
    else:
        offsets = load_offsets_text(path)
    return make_zero_block(
        name=name or path.stem,
        start_index=start_index,
        base_height=base_height,
        offsets=offsets,
        precision_note=precision_note,
        source=source or str(path),
    )


def load_zero_block_from_gap_csv(
    path: Path | str,
    *,
    dataset: str | None = None,
    name: str | None = None,
    precision_note: str = "",
    source: str = "",
) -> ZeroBlock:
    """Reconstruct a ``ZeroBlock`` from an existing all-gaps CSV artifact."""

    path = Path(path)
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"zero_index_left", "zero_index_right", "offset_left", "offset_right"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{path} is not a recognized all-gaps CSV")
        for row in reader:
            if dataset is None or row.get("dataset") == dataset:
                rows.append(row)
    if not rows:
        raise ValueError(f"No rows found for dataset {dataset!r} in {path}")

    rows.sort(key=lambda row: int(row["zero_index_left"]))
    start_index = int(rows[0]["zero_index_left"])
    base_height = rows[0].get("base_height") or "0"
    offsets = [to_decimal(rows[0]["offset_left"])]
    last_right_index = int(rows[0]["zero_index_left"])
    for row in rows:
        left = int(row["zero_index_left"])
        if left != last_right_index:
            # A gap CSV can be filtered. Stop at the first discontinuity so the
            # block remains a valid adjacent sequence.
            break
        offsets.append(to_decimal(row["offset_right"]))
        last_right_index = int(row["zero_index_right"])

    return make_zero_block(
        name=name or dataset or path.stem,
        start_index=start_index,
        base_height=base_height,
        offsets=offsets,
        precision_note=precision_note,
        source=source or str(path),
    )


def write_zero_block_csv(path: Path | str, block: ZeroBlock) -> Path:
    """Write a zero block as offsets suitable for reloading."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["zero_index", "offset"])
        for offset_pos, offset in enumerate(block.offsets):
            writer.writerow([block.start_index + offset_pos, str(offset)])
    return path


def load_many_blocks(paths: Iterable[Path | str], **kwargs: object) -> list[ZeroBlock]:
    """Load multiple zero blocks with common keyword arguments."""

    return [load_zero_block(path, **kwargs) for path in paths]
