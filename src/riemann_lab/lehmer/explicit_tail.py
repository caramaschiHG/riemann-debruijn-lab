"""Explicit-style conservative tail estimates.

The implementation follows an N(T)-style binned bound pattern, but the package
labels this as an explicit-style conservative estimate unless the constants and
all mathematical preconditions are independently reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, Literal

import mpmath as mp

from riemann_lab.constants import ClaimStrength
from riemann_lab.data.schemas import ZeroBlock, to_decimal
from .index import compute_G_local

mp.mp.dps = 80


RigorLevel = Literal["heuristic", "explicit_style", "rigorous_under_assumptions"]


@dataclass(frozen=True)
class TailBoundAssumptions:
    """Assumptions and policies behind an explicit-style tail estimate."""

    zero_count_formula: str
    s_t_bound: str
    table_precision_note: str
    endpoint_policy: str
    local_window_policy: str
    high_precision_policy: str
    rigor_level: RigorLevel

    def as_rows(self) -> list[dict[str, str]]:
        """Return rows suitable for CSV output."""

        return [
            {"assumption": "zero_count_formula", "value": self.zero_count_formula},
            {"assumption": "s_t_bound", "value": self.s_t_bound},
            {"assumption": "table_precision_note", "value": self.table_precision_note},
            {"assumption": "endpoint_policy", "value": self.endpoint_policy},
            {"assumption": "local_window_policy", "value": self.local_window_policy},
            {"assumption": "high_precision_policy", "value": self.high_precision_policy},
            {"assumption": "rigor_level", "value": self.rigor_level},
        ]

    def markdown_lines(self) -> list[str]:
        """Return markdown bullets for reports."""

        return [f"- {row['assumption']}: {row['value']}" for row in self.as_rows()]


def default_tail_bound_assumptions(block: ZeroBlock | None = None) -> TailBoundAssumptions:
    """Return the default assumptions used by this implementation."""

    precision_note = block.precision_note if block is not None else "No table precision note supplied."
    return TailBoundAssumptions(
        zero_count_formula=(
            "Riemann-von Mangoldt main term N0(T)=T/(2pi)log(T/(2pi))-T/(2pi)+7/8 "
            "with envelope N_lower <= N(T) <= N_upper."
        ),
        s_t_bound="Trudgian-style |S(T)| <= 0.112 log T + 0.278 log log T + 2.510, plus a +/-1 slack term.",
        table_precision_note=precision_note or "No table precision note supplied.",
        endpoint_policy=(
            "The local window endpoints are known zeros included in G_local. The first "
            "tail bin on each side subtracts that known endpoint from the zero-count "
            "upper envelope to avoid double-counting local zeros."
        ),
        local_window_policy=(
            "G_local sums known zeros in the selected inclusive window and excludes the "
            "candidate pair endpoints. Tail bins cover only zeros outside that window."
        ),
        high_precision_policy=(
            "Candidate gaps and local distances use Decimal/mpmath base+offset arithmetic; "
            "tiny gaps are never computed by subtracting huge float64 heights."
        ),
        rigor_level="explicit_style",
    )


def _mp(value: Decimal | str | float | int | mp.mpf) -> mp.mpf:
    if isinstance(value, mp.mpf):
        return value
    if isinstance(value, Decimal):
        return mp.mpf(str(value))
    return mp.mpf(str(value))


def N_main(T: mp.mpf | Decimal | str | float) -> mp.mpf:
    """Main Riemann-von Mangoldt zero-counting term."""

    t = _mp(T)
    return t / (2 * mp.pi) * mp.log(t / (2 * mp.pi)) - t / (2 * mp.pi) + mp.mpf("0.875")


def S_error_bound(T: mp.mpf | Decimal | str | float) -> mp.mpf:
    """Trudgian-style configurable bound for |S(T)| used in historical scripts."""

    t = _mp(T)
    if t < mp.e:
        t = mp.e
    return mp.mpf("0.112") * mp.log(t) + mp.mpf("0.278") * mp.log(mp.log(t)) + mp.mpf("2.510")


def N_upper(T: mp.mpf | Decimal | str | float) -> mp.mpf:
    """Upper zero-counting envelope."""

    t = _mp(T)
    return N_main(t) + S_error_bound(t) + mp.mpf("1")


def N_lower(T: mp.mpf | Decimal | str | float) -> mp.mpf:
    """Lower zero-counting envelope."""

    t = _mp(T)
    return N_main(t) - S_error_bound(t) - mp.mpf("1")


def count_upper(A: mp.mpf | Decimal | str | float, B: mp.mpf | Decimal | str | float) -> mp.mpf:
    """Conservative upper count for zeros in [A, B]."""

    a = _mp(A)
    b = _mp(B)
    if b <= a:
        return mp.mpf("0")
    return max(mp.mpf("0"), mp.ceil(N_upper(b) - N_lower(a)))


@dataclass(frozen=True)
class TailBin:
    """One geometric bin in an explicit-style tail estimate."""

    side: str
    A: str
    B: str
    distance_near: str
    distance_far: str
    count_upper_raw: str
    count_upper: str
    known_endpoint_excluded: bool
    fmax: str
    G_bound: str


@dataclass(frozen=True)
class ExplicitTailResult:
    """Explicit-style tail result for omitted zeros."""

    left_tail_G_bound: Decimal
    right_tail_G_bound: Decimal
    total_tail_G_bound: Decimal
    bins: tuple[TailBin, ...]
    q_geometric: float
    assumptions: TailBoundAssumptions
    claim_strength: ClaimStrength = ClaimStrength.EXPLICIT_STYLE_BOUND
    label: str = "explicit-style conservative estimate"


def fmax_for_distance(distance: mp.mpf, gap: mp.mpf) -> mp.mpf:
    """Maximum pair contribution for a zero at least ``distance`` from an endpoint."""

    if distance <= 0:
        raise ValueError("distance must be positive")
    return 1 / (distance**2) + 1 / ((distance + gap) ** 2)


def explicit_tail_bound(
    *,
    a_height: Decimal | str | float,
    b_height: Decimal | str | float,
    left_edge_height: Decimal | str | float,
    right_edge_height: Decimal | str | float,
    q: float = 1.25,
    max_bins_per_side: int = 512,
    min_bin_contribution: str = "1e-40",
    assumptions: TailBoundAssumptions | None = None,
) -> ExplicitTailResult:
    """Bound omitted G contribution outside a known window by geometric bins."""

    if q <= 1.0:
        raise ValueError("q must exceed 1")
    a = _mp(a_height)
    b = _mp(b_height)
    left_edge = _mp(left_edge_height)
    right_edge = _mp(right_edge_height)
    gap = b - a
    if gap <= 0:
        raise ValueError("candidate endpoints must be strictly increasing")
    if not (left_edge < a < b < right_edge):
        raise ValueError("tail edges must satisfy left_edge < a < b < right_edge")
    threshold = _mp(min_bin_contribution)
    q_mp = _mp(q)
    bins: list[TailBin] = []
    left_total = mp.mpf("0")
    right_total = mp.mpf("0")

    def add_side(side: str, initial_distance: mp.mpf) -> mp.mpf:
        total = mp.mpf("0")
        distance_near = initial_distance
        for bin_index in range(max_bins_per_side):
            distance_far = distance_near * q_mp
            if side == "left":
                A = a - distance_far
                B = a - distance_near
                if B <= mp.e:
                    break
                if A < mp.e:
                    A = mp.e
            else:
                A = b + distance_near
                B = b + distance_far
            c_upper_raw = count_upper(A, B)
            known_endpoint_excluded = bin_index == 0
            c_upper = max(mp.mpf("0"), c_upper_raw - 1) if known_endpoint_excluded else c_upper_raw
            fmax = fmax_for_distance(distance_near, gap)
            G_bound = c_upper * fmax
            total += G_bound
            bins.append(
                TailBin(
                    side=side,
                    A=mp.nstr(A, 18),
                    B=mp.nstr(B, 18),
                    distance_near=mp.nstr(distance_near, 18),
                    distance_far=mp.nstr(distance_far, 18),
                    count_upper_raw=mp.nstr(c_upper_raw, 18),
                    count_upper=mp.nstr(c_upper, 18),
                    known_endpoint_excluded=known_endpoint_excluded,
                    fmax=mp.nstr(fmax, 18),
                    G_bound=mp.nstr(G_bound, 18),
                )
            )
            if G_bound < threshold and distance_near > 1:
                break
            distance_near = distance_far
        return total

    left_total = add_side("left", a - left_edge)
    right_total = add_side("right", right_edge - b)
    return ExplicitTailResult(
        left_tail_G_bound=to_decimal(mp.nstr(left_total, 40)),
        right_tail_G_bound=to_decimal(mp.nstr(right_total, 40)),
        total_tail_G_bound=to_decimal(mp.nstr(left_total + right_total, 40)),
        bins=tuple(bins),
        q_geometric=q,
        assumptions=assumptions or default_tail_bound_assumptions(),
    )


def explicit_tail_bound_for_block(
    block: ZeroBlock,
    left_index: int,
    *,
    radius: int | None = None,
    q: float = 1.25,
) -> tuple[Decimal, ExplicitTailResult]:
    """Compute local G and an explicit-style tail estimate for a zero block."""

    pair_pos = block.position_of(left_index)
    lo, hi, _ = block.local_offsets(left_index, radius)
    if lo >= pair_pos or hi <= pair_pos + 1:
        raise ValueError(
            "explicit-style tail estimate requires at least one known zero outside "
            "the candidate pair on both sides of the local window"
        )
    a = block.base_height + block.offsets[pair_pos]
    b = block.base_height + block.offsets[pair_pos + 1]
    left_edge = block.base_height + block.offsets[lo]
    right_edge = block.base_height + block.offsets[hi]
    G_local, _, _ = compute_G_local(block, left_index, radius=radius)
    tail = explicit_tail_bound(
        a_height=a,
        b_height=b,
        left_edge_height=left_edge,
        right_edge_height=right_edge,
        q=q,
        assumptions=default_tail_bound_assumptions(block),
    )
    return G_local, tail


def bins_to_rows(
    bins: Iterable[TailBin],
    dataset: str,
    zero_index_pair: str,
    q: float,
) -> list[dict[str, str]]:
    """Convert tail bins to CSV-friendly dictionaries."""

    return [
        {
            "dataset": dataset,
            "zero_index_pair": zero_index_pair,
            "q_geometric": str(q),
            "side": item.side,
            "A": item.A,
            "B": item.B,
            "distance_near": item.distance_near,
            "distance_far": item.distance_far,
            "count_upper_raw": item.count_upper_raw,
            "count_upper": item.count_upper,
            "known_endpoint_excluded": str(item.known_endpoint_excluded),
            "fmax": item.fmax,
            "G_bound": item.G_bound,
        }
        for item in bins
    ]
