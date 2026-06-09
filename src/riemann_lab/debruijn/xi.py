"""Completed xi and Xi numerical helpers."""

from __future__ import annotations

import mpmath as mp


def xi(s: complex | mp.mpc) -> mp.mpc:
    """Compute the completed xi function numerically with mpmath."""

    z = mp.mpc(s)
    return mp.mpf("0.5") * z * (z - 1) * mp.power(mp.pi, -z / 2) * mp.gamma(z / 2) * mp.zeta(z)


def Xi(x: float | mp.mpf) -> mp.mpc:
    """Compute ``Xi(x) = xi(1/2 + i x)`` numerically."""

    return xi(mp.mpf("0.5") + 1j * mp.mpf(x))

