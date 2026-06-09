"""Validation and report-language checks."""

from __future__ import annotations

from riemann_lab.constants import FORBIDDEN_PROOF_CLAIMS, REQUIRED_REPORT_WARNINGS, REPORT_DISCLAIMER


def forbidden_claims_found(text: str) -> list[str]:
    """Return forbidden proof-like phrases found in ``text``."""

    lowered = text.lower()
    return [claim for claim in FORBIDDEN_PROOF_CLAIMS if claim.lower() in lowered]


def missing_required_warnings(text: str) -> list[str]:
    """Return required warning sentences absent from ``text``."""

    required = (REPORT_DISCLAIMER, *REQUIRED_REPORT_WARNINGS)
    return [warning for warning in required if warning not in text]


def validate_report_language(text: str) -> None:
    """Raise if report text misses warnings or contains forbidden claims."""

    forbidden = forbidden_claims_found(text)
    if forbidden:
        raise ValueError(f"Forbidden report claims found: {forbidden}")
    missing = missing_required_warnings(text)
    if missing:
        raise ValueError(f"Report is missing required warnings: {missing}")

