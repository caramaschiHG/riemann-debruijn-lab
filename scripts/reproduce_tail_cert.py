"""Reproduce an explicit-style tail estimate for the historical candidate."""

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
                "certify-tail",
                "--zeros",
                str(DEFAULT_GAPS),
                "--dataset",
                "around_1e12",
                "--candidate",
                "1000000008625",
                "--radius",
                "80",
                "--out",
                "outputs/reproduction/cert_1e12",
            ]
        )
    )
