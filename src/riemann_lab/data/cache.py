"""Filesystem helpers for reproducible outputs."""

from __future__ import annotations

from pathlib import Path


def ensure_directory(path: Path | str) -> Path:
    """Create and return an output directory."""

    resolved = Path(path)
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved

