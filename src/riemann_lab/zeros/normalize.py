"""Normalization of zero gaps by local average spacing."""

from __future__ import annotations

from decimal import Decimal
import math


def average_zero_spacing(height: float | Decimal) -> float:
    """Approximate local mean spacing near height ``T``.

    The formula is ``2*pi/log(T/(2*pi))`` and is numerical context, not a
    rigorous local spacing bound.
    """

    T = float(height)
    if T <= 2 * math.pi:
        raise ValueError("average spacing formula expects T > 2*pi")
    return 2.0 * math.pi / math.log(T / (2.0 * math.pi))


def normalized_gap(gap: float | Decimal, height: float | Decimal) -> float:
    """Normalize a gap by the local average spacing near ``height``."""

    return float(gap) / average_zero_spacing(height)

