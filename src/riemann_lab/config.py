"""Small configuration helpers used by CLI and scripts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OutputLayout:
    """Resolved output paths for one experiment run."""

    root: Path

    @property
    def tables(self) -> Path:
        return self.root / "tables"

    @property
    def figures(self) -> Path:
        return self.root / "figures"

    @property
    def reports(self) -> Path:
        return self.root / "reports"

    def create(self) -> "OutputLayout":
        for path in (self.root, self.tables, self.figures, self.reports):
            path.mkdir(parents=True, exist_ok=True)
        return self

