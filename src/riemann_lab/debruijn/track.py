"""Root tracking helpers for small Xi experiments."""

from __future__ import annotations

from dataclasses import dataclass

import mpmath as mp

from .xi import Xi


@dataclass(frozen=True)
class RootTrackResult:
    """One root-tracking result for a small numerical experiment."""

    start: float
    root: float
    residual: float
    status: str


def refine_Xi_zero(start: float, tol: float = 1e-20) -> RootTrackResult:
    """Refine a zero of Xi near ``start`` using mpmath findroot."""

    try:
        root = mp.findroot(lambda x: mp.re(Xi(x)), start, tol=tol)
        residual = abs(mp.re(Xi(root)))
        return RootTrackResult(float(start), float(root), float(residual), "ok")
    except Exception as exc:  # pragma: no cover - depends on mpmath convergence
        return RootTrackResult(float(start), float("nan"), float("nan"), f"failed: {exc}")

