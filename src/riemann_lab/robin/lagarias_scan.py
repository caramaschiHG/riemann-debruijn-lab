"""Lagarias criterion scan."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import math
from pathlib import Path

from riemann_lab.constants import report_warning_block
from .divisor_sums import harmonic_numbers, sigma_sieve


@dataclass(frozen=True)
class LagariasRecord:
    """A finite Lagarias inequality margin."""

    rank: int
    n: int
    sigma_n: int
    rhs: float
    margin_rhs_minus_sigma: float


def scan_lagarias(limit: int, top: int = 20, sigma: list[int] | None = None) -> list[LagariasRecord]:
    """Scan Lagarias' RH-equivalent criterion over a finite range."""

    if limit < 1:
        raise ValueError("limit must be positive")
    sigma_values = sigma if sigma is not None else sigma_sieve(limit)
    harmonic = harmonic_numbers(limit)
    rows: list[LagariasRecord] = []
    for n in range(1, limit + 1):
        h_n = harmonic[n]
        rhs = h_n + math.exp(h_n) * math.log(h_n)
        rows.append(
            LagariasRecord(
                rank=0,
                n=n,
                sigma_n=sigma_values[n],
                rhs=rhs,
                margin_rhs_minus_sigma=rhs - sigma_values[n],
            )
        )
    rows.sort(key=lambda row: row.margin_rhs_minus_sigma)
    return [
        LagariasRecord(
            rank=i + 1,
            n=row.n,
            sigma_n=row.sigma_n,
            rhs=row.rhs,
            margin_rhs_minus_sigma=row.margin_rhs_minus_sigma,
        )
        for i, row in enumerate(rows[:top])
    ]


def write_lagarias_csv(path: Path | str, rows: list[LagariasRecord]) -> Path:
    """Write Lagarias scan candidates to CSV."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["rank", "n", "sigma_n", "rhs", "margin_rhs_minus_sigma"])
        for row in rows:
            writer.writerow(
                [
                    row.rank,
                    row.n,
                    row.sigma_n,
                    f"{row.rhs:.15g}",
                    f"{row.margin_rhs_minus_sigma:.15g}",
                ]
            )
    return path


def lagarias_report(limit: int, rows: list[LagariasRecord]) -> str:
    """Build a markdown Lagarias scan report."""

    best = rows[0]
    lines = [
        "# Lagarias Scan Report",
        "",
        report_warning_block(),
        "",
        "## Parameters",
        f"- N: {limit}",
        "- Criterion checked: sigma(n) <= H_n + exp(H_n) log(H_n)",
        "",
        "## Results",
        f"- Tightest finite candidate: n = {best.n}",
        f"- sigma(n): {best.sigma_n}",
        f"- RHS: {best.rhs:.15f}",
        f"- margin RHS - sigma(n): {best.margin_rhs_minus_sigma:.15f}",
        "",
        "## Interpretation",
        "This is a finite check only. Lagarias' criterion is equivalent to RH as",
        "an infinite statement, not as a finite scan.",
    ]
    return "\n".join(lines) + "\n"

