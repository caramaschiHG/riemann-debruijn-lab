"""Reproduce the Robin/Lagarias finite scan."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from riemann_lab.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["robin-scan", "--N", "1000000", "--out", "outputs/reproduction/robin_1M"]))
