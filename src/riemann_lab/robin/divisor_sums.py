"""Divisor-sum and harmonic-number utilities."""

from __future__ import annotations


def sigma_sieve(limit: int) -> list[int]:
    """Compute sigma(n) for ``1 <= n <= limit`` by a divisor sieve."""

    if limit < 1:
        raise ValueError("limit must be positive")
    sigma = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            sigma[multiple] += divisor
    return sigma


def harmonic_numbers(limit: int) -> list[float]:
    """Compute floating harmonic numbers H_n up to ``limit``."""

    if limit < 1:
        raise ValueError("limit must be positive")
    values = [0.0] * (limit + 1)
    acc = 0.0
    for n in range(1, limit + 1):
        acc += 1.0 / n
        values[n] = acc
    return values

