"""Exploratory generation of highly divisible Robin candidates."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from riemann_lab.constants import EXP_EULER_GAMMA


SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)


@dataclass(frozen=True)
class RobinCandidate:
    """A generated highly divisible candidate and Robin ratio."""

    n: int
    exponents: tuple[int, ...]
    sigma_n: int
    ratio: float
    margin: float


def sigma_from_factorization(primes: Iterable[int], exponents: Iterable[int]) -> int:
    """Compute sigma(n) from prime powers."""

    total = 1
    for prime, exponent in zip(primes, exponents):
        total *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return total


def decreasing_exponent_candidates(
    limit: int,
    primes: tuple[int, ...] = SMALL_PRIMES,
    max_exponent: int = 64,
) -> list[tuple[int, tuple[int, ...]]]:
    """Generate ``n`` with nonincreasing exponents over successive primes."""

    results: list[tuple[int, tuple[int, ...]]] = []

    def rec(pos: int, max_exp: int, current_n: int, exps: list[int]) -> None:
        if current_n > 5040:
            results.append((current_n, tuple(exps)))
        if pos >= len(primes):
            return
        prime = primes[pos]
        value = current_n
        for exp in range(1, max_exp + 1):
            value *= prime
            if value > limit:
                break
            rec(pos + 1, exp, value, [*exps, exp])

    rec(0, max_exponent, 1, [])
    return sorted(set(results), key=lambda item: item[0])


def rank_robin_candidates(limit: int, top: int = 25) -> list[RobinCandidate]:
    """Rank highly divisible candidate numbers by Robin ratio."""

    rows: list[RobinCandidate] = []
    for n, exponents in decreasing_exponent_candidates(limit):
        sigma_n = sigma_from_factorization(SMALL_PRIMES, exponents)
        ratio = sigma_n / (n * math.log(math.log(n)))
        rows.append(
            RobinCandidate(
                n=n,
                exponents=exponents,
                sigma_n=sigma_n,
                ratio=ratio,
                margin=EXP_EULER_GAMMA - ratio,
            )
        )
    rows.sort(key=lambda row: row.ratio, reverse=True)
    return rows[:top]

