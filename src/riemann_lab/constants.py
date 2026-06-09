"""Shared constants and required honesty language."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math

EULER_GAMMA = 0.577215664901532860606512090082402431
EXP_EULER_GAMMA = math.exp(EULER_GAMMA)
LEHMER_THRESHOLD = 4.0 / 5.0

REPORT_DISCLAIMER = (
    "Nothing in this report proves the Riemann Hypothesis. Results are "
    "numerical, conditional, or heuristic unless explicitly stated otherwise."
)

REQUIRED_REPORT_WARNINGS = (
    "This does not prove RH.",
    "This is numerical/heuristic unless explicitly stated.",
    "Lambda <= 0 is not established.",
)

FORBIDDEN_PROOF_CLAIMS = (
    "we solved RH",
    "this proves RH",
    "we solved the Millennium Problem",
    "this proves Lambda <= 0",
)


@dataclass(frozen=True)
class KnownCandidate:
    """Reference values copied from historical lab reports."""

    label: str
    dataset: str
    left_index: int
    right_index: int
    delta: float | None = None
    normalized_gap: float | None = None
    gbar_local: float | None = None
    gbar_upper: float | None = None
    naive_collision_time: float | None = None
    finite_flow_collision_time: float | None = None
    note: str = ""


KNOWN_CANDIDATES: dict[str, KnownCandidate] = {
    "A": KnownCandidate(
        label="Candidate A",
        dataset="around_1e12",
        left_index=1000000008625,
        right_index=1000000008626,
        delta=0.0055569683,
        normalized_gap=0.021646226566,
        gbar_local=0.0014248568,
        gbar_upper=0.0014258627,
        naive_collision_time=-3.859987e-6,
        finite_flow_collision_time=-3.860660e-6,
        note="Current strongest candidate in the historical lab artifacts.",
    ),
    "B": KnownCandidate(
        label="Candidate B",
        dataset="first_100k",
        left_index=95248,
        right_index=95249,
        delta=0.0147014760005,
        normalized_gap=0.0218604660555,
    ),
    "C": KnownCandidate(
        label="Candidate C",
        dataset="around_1e21",
        left_index=1000000000000000001635,
        right_index=1000000000000000001636,
        delta=0.00530012000002,
        normalized_gap=0.0376047696726,
        gbar_upper=0.0057798888,
        note="High-zero table precision warning required; use base+offset arithmetic.",
    ),
    "D": KnownCandidate(
        label="Classical Lehmer pair",
        dataset="first_100k",
        left_index=6709,
        right_index=6710,
        note="Classical reference pair when zero data are available.",
    ),
}


class ClaimStrength(str, Enum):
    """Reader-facing strength labels for mathematical and numerical claims."""

    FACT_FROM_SOURCE_DATA = "FACT_FROM_SOURCE_DATA"
    NUMERICAL_COMPUTATION = "NUMERICAL_COMPUTATION"
    HEURISTIC_ESTIMATE = "HEURISTIC_ESTIMATE"
    EXPLICIT_STYLE_BOUND = "EXPLICIT_STYLE_BOUND"
    CONDITIONAL_STATEMENT = "CONDITIONAL_STATEMENT"
    OPEN_PROBLEM = "OPEN_PROBLEM"


def labeled_claim(strength: ClaimStrength, text: str) -> str:
    """Prefix report text with an explicit claim-strength label."""

    return f"[{strength.value}] {text}"


def report_warning_block() -> str:
    """Return the standard report warning block."""

    lines = [REPORT_DISCLAIMER, *REQUIRED_REPORT_WARNINGS]
    return "\n".join(lines)
