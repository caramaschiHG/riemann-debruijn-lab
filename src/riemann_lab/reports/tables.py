"""CSV table helpers."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


def write_dict_rows(path: Path | str, rows: Iterable[dict[str, object]]) -> Path:
    """Write dictionaries to CSV, preserving keys from the first row."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path

