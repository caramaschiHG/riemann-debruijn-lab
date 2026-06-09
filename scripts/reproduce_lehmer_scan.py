"""Reproduce the Lehmer scan for the historical around_1e12 block."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from riemann_lab.cli import main


DEFAULT_GAPS = Path("artifacts/unpacked/zeta_gap_collision_r80_package/zeta_gap_collision_r80_all_gaps.csv")


if __name__ == "__main__":
    raise SystemExit(
        main(
            [
                "lehmer-scan",
                "--zeros",
                str(DEFAULT_GAPS),
                "--dataset",
                "around_1e12",
                "--radius",
                "80",
                "--out",
                "outputs/reproduction/lehmer_1e12",
            ]
        )
    )
