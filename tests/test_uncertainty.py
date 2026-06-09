from decimal import Decimal

from riemann_lab.lehmer.uncertainty import stress_gbar_upper


def test_uncertainty_stress_does_not_decrease_worst_case_bound() -> None:
    result = stress_gbar_upper("0.0057798888", "0.00530012000002", "1e-6")

    assert result.stressed_gbar_upper >= Decimal("0.0057798888")
    assert result.worst_gap_delta > result.gap_delta

