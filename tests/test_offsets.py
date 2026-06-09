from decimal import Decimal

from riemann_lab.data.schemas import make_zero_block
from riemann_lab.zeros.offsets import gap_at, gap_from_offsets, unsafe_float_height_gap


def test_gap_computation_uses_offsets() -> None:
    block = make_zero_block(
        name="huge_base_fixture",
        start_index=1,
        base_height="1e21",
        offsets=[Decimal("0.001"), Decimal("0.006")],
        precision_note="high base fixture",
    )

    assert gap_at(block, 1) == Decimal("0.005")
    assert gap_from_offsets("0.001", "0.006") == Decimal("0.005")


def test_bad_float64_subtraction_is_inaccurate_for_high_zero_blocks() -> None:
    block = make_zero_block(
        name="high_base_float64_failure_fixture",
        start_index=1,
        base_height="1e21",
        offsets=[Decimal("0.001"), Decimal("0.006")],
        precision_note="high base fixture",
    )

    assert gap_at(block, 1) == Decimal("0.005")
    assert unsafe_float_height_gap(block, 1) != float(gap_at(block, 1))
