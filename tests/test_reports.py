from riemann_lab.constants import REQUIRED_REPORT_WARNINGS, REPORT_DISCLAIMER
from riemann_lab.lehmer.explicit_tail import default_tail_bound_assumptions
from riemann_lab.reports.markdown import markdown_report
from riemann_lab.zeros.validate import validate_report_language


def test_no_false_claims_in_reports() -> None:
    report = markdown_report(
        "Test Report",
        input_data="fixture",
        precision_notes="fixture precision",
        parameters={"radius": 1},
        results=["finite result"],
        interpretation="This is a test interpretation.",
    )

    assert REPORT_DISCLAIMER in report
    for warning in REQUIRED_REPORT_WARNINGS:
        assert warning in report
    validate_report_language(report)


def test_tail_assumptions_report_includes_rigor_level_and_policies() -> None:
    assumptions = default_tail_bound_assumptions()

    text = "\n".join(assumptions.markdown_lines())

    assert "rigor_level" in text
    assert "explicit_style" in text
    assert "endpoint_policy" in text
    assert "high_precision_policy" in text
