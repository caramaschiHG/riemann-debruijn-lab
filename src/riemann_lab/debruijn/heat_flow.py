"""Experimental heat-flow placeholders.

The true de Bruijn-Newman heat deformation is delicate. This module exposes
small numerical helpers but does not claim to implement a rigorous H_t solver.
"""

from __future__ import annotations

import mpmath as mp

from .xi import Xi


def gaussian_smoothed_Xi(x: float, t: float, width: float = 6.0) -> mp.mpf:
    """Toy Gaussian smoothing diagnostic around Xi.

    This is an exploratory numerical proxy, not the full H_t equation.
    """

    if t <= 0:
        return mp.re(Xi(x))
    sigma = mp.sqrt(4 * t)
    norm = 1 / (sigma * mp.sqrt(2 * mp.pi))

    def integrand(u: mp.mpf) -> mp.mpf:
        return norm * mp.e ** (-(u**2) / (2 * sigma**2)) * mp.re(Xi(x - u))

    return mp.quad(integrand, [-width * sigma, width * sigma])

