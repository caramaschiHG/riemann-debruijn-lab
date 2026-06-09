"""Reproduce gap-energy and finite-flow diagnostics for the historical candidate."""

from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from riemann_lab.cli import main


DEFAULT_GAPS = Path("artifacts/unpacked/zeta_gap_collision_r80_package/zeta_gap_collision_r80_all_gaps.csv")


if __name__ == "__main__":
    rc = main(
        [
            "gap-energy",
            "--zeros",
            str(DEFAULT_GAPS),
            "--dataset",
            "around_1e12",
            "--alphas",
            "1,1.5,2,3",
            "--out",
            "outputs/reproduction/energy_1e12",
        ]
    )
    if rc == 0:
        rc = main(
            [
                "finite-flow",
                "--zeros",
                str(DEFAULT_GAPS),
                "--dataset",
                "around_1e12",
                "--candidate",
                "1000000008625",
                "--radius",
                "80",
                "--out",
                "outputs/reproduction/flow_1e12",
            ]
        )
    raise SystemExit(rc)
