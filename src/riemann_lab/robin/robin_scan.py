"""Robin criterion scan."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import math
from pathlib import Path

from riemann_lab.constants import EXP_EULER_GAMMA, report_warning_block
from .divisor_sums import sigma_sieve


@dataclass(frozen=True)
class RobinRecord:
    """A candidate near Robin's inequality boundary."""

    rank: int
    n: int
    sigma_n: int
    ratio_sigma_over_n_loglogn: float
    margin_exp_gamma_minus_ratio: float


def scan_robin(limit: int, top: int = 20, sigma: list[int] | None = None) -> list[RobinRecord]:
    """Scan Robin's criterion for ``n > 5040`` and return dangerous candidates.

    This is a finite computation and is not a proof of any infinite statement.
    """

    if limit <= 5040:
        raise ValueError("Robin scan limit must exceed 5040")
    sigma_values = sigma if sigma is not None else sigma_sieve(limit)
    rows: list[RobinRecord] = []
    for n in range(5041, limit + 1):
        denom = n * math.log(math.log(n))
        ratio = sigma_values[n] / denom
        rows.append(
            RobinRecord(
                rank=0,
                n=n,
                sigma_n=sigma_values[n],
                ratio_sigma_over_n_loglogn=ratio,
                margin_exp_gamma_minus_ratio=EXP_EULER_GAMMA - ratio,
            )
        )
    rows.sort(key=lambda row: row.ratio_sigma_over_n_loglogn, reverse=True)
    return [
        RobinRecord(
            rank=i + 1,
            n=row.n,
            sigma_n=row.sigma_n,
            ratio_sigma_over_n_loglogn=row.ratio_sigma_over_n_loglogn,
            margin_exp_gamma_minus_ratio=row.margin_exp_gamma_minus_ratio,
        )
        for i, row in enumerate(rows[:top])
    ]


def write_robin_csv(path: Path | str, rows: list[RobinRecord]) -> Path:
    """Write Robin scan candidates to CSV."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "rank",
                "n",
                "sigma_n",
                "ratio_sigma_over_n_loglogn",
                "margin_exp_gamma_minus_ratio",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.rank,
                    row.n,
                    row.sigma_n,
                    f"{row.ratio_sigma_over_n_loglogn:.15g}",
                    f"{row.margin_exp_gamma_minus_ratio:.15g}",
                ]
            )
    return path


def robin_report(limit: int, rows: list[RobinRecord]) -> str:
    """Build a markdown Robin scan report."""

    best = rows[0]
    lines = [
        "# Robin Scan Report",
        "",
        report_warning_block(),
        "",
        "## Parameters",
        f"- N: {limit}",
        "- Criterion checked: sigma(n) < exp(gamma) n log log n for n > 5040",
        "",
        "## Results",
        f"- Best finite candidate: n = {best.n}",
        f"- Ratio sigma(n)/(n log log n): {best.ratio_sigma_over_n_loglogn:.15f}",
        f"- Margin exp(gamma) - ratio: {best.margin_exp_gamma_minus_ratio:.15f}",
        "",
        "## Interpretation",
        "This is a finite Robin scan. It can identify dangerous candidates in the",
        "chosen range, but it does not establish RH or any infinite Robin bound.",
    ]
    return "\n".join(lines) + "\n"

