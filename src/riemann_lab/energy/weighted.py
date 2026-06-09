"""Reusable weight functions for gap-energy experiments."""

from __future__ import annotations

import math


def index_weight(index: int, alpha: float) -> float:
    """Return ``1/index^alpha``."""

    if index <= 0:
        raise ValueError("index must be positive")
    return 1.0 / (index**alpha)


def local_decay_weight(distance: int, beta: float) -> float:
    """Return exponential local-decay weight ``exp(-distance/beta)``."""

    if beta <= 0:
        raise ValueError("beta must be positive")
    return math.exp(-abs(distance) / beta)


def normalized_gap_weight(normalized_gap: float) -> float:
    """Return inverse-square normalized-gap weight."""

    if normalized_gap <= 0:
        raise ValueError("normalized_gap must be positive")
    return 1.0 / (normalized_gap * normalized_gap)

