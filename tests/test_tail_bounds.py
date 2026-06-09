from decimal import Decimal
from pathlib import Path

import pytest

from riemann_lab.data.loaders import load_zero_block_from_gap_csv
from riemann_lab.data.schemas import make_zero_block
from riemann_lab.lehmer.certify import estimate_candidate_tail
from riemann_lab.lehmer.explicit_tail import explicit_tail_bound


def test_tail_bound_positive() -> None:
    result = explicit_tail_bound(
        a_height=Decimal("1000.0"),
        b_height=Decimal("1000.1"),
        left_edge_height=Decimal("999.0"),
        right_edge_height=Decimal("1001.0"),
        q=1.5,
        max_bins_per_side=32,
    )

    assert result.total_tail_G_bound >= Decimal("0")
    assert result.left_tail_G_bound >= Decimal("0")
    assert result.right_tail_G_bound >= Decimal("0")


def test_tail_bound_refinement_not_pathological() -> None:
    coarse = explicit_tail_bound(
        a_height=Decimal("1000.0"),
        b_height=Decimal("1000.1"),
        left_edge_height=Decimal("999.0"),
        right_edge_height=Decimal("1001.0"),
        q=2.0,
        max_bins_per_side=32,
    )
    refined = explicit_tail_bound(
        a_height=Decimal("1000.0"),
        b_height=Decimal("1000.1"),
        left_edge_height=Decimal("999.0"),
        right_edge_height=Decimal("1001.0"),
        q=1.25,
        max_bins_per_side=32,
    )

    assert refined.total_tail_G_bound >= Decimal("0")
    assert coarse.total_tail_G_bound >= Decimal("0")
    assert refined.total_tail_G_bound < coarse.total_tail_G_bound * Decimal("100")


def test_gbar_upper_is_at_least_gbar_local() -> None:
    block = make_zero_block(
        name="tail_fixture",
        start_index=10,
        base_height="1000",
        offsets=["0.0", "1.0", "1.12", "2.0", "3.2", "4.0"],
        precision_note="low test fixture",
    )

    estimate = estimate_candidate_tail(block, 12, radius=1, q=1.5)

    assert estimate.G_total_upper >= estimate.G_local
    assert estimate.gbar_upper >= estimate.gbar_local


def test_more_tail_bins_cannot_decrease_total_upper_contribution() -> None:
    common = {
        "a_height": Decimal("1000.0"),
        "b_height": Decimal("1000.1"),
        "left_edge_height": Decimal("999.0"),
        "right_edge_height": Decimal("1001.0"),
        "q": 1.5,
        "min_bin_contribution": "0",
    }
    short = explicit_tail_bound(**common, max_bins_per_side=4)
    longer = explicit_tail_bound(**common, max_bins_per_side=8)

    assert longer.total_tail_G_bound >= short.total_tail_G_bound


def test_local_window_endpoints_are_not_double_counted_in_first_tail_bins() -> None:
    result = explicit_tail_bound(
        a_height=Decimal("1000.0"),
        b_height=Decimal("1000.1"),
        left_edge_height=Decimal("999.0"),
        right_edge_height=Decimal("1001.0"),
        q=1.5,
        max_bins_per_side=4,
        min_bin_contribution="0",
    )

    first_left = next(item for item in result.bins if item.side == "left")
    first_right = next(item for item in result.bins if item.side == "right")

    assert first_left.known_endpoint_excluded is True
    assert first_right.known_endpoint_excluded is True
    assert Decimal(first_left.count_upper) == max(Decimal("0"), Decimal(first_left.count_upper_raw) - 1)
    assert Decimal(first_right.count_upper) == max(Decimal("0"), Decimal(first_right.count_upper_raw) - 1)


def test_candidate_a_reproduces_full_window_tail_estimate() -> None:
    root = Path(__file__).resolve().parents[1]
    artifact = root / "artifacts/unpacked/zeta_gap_collision_r80_package/zeta_gap_collision_r80_all_gaps.csv"
    if not artifact.exists():
        pytest.skip("historical all-gaps artifact is not available")
    block = load_zero_block_from_gap_csv(
        artifact,
        dataset="around_1e12",
        precision_note="Use base+offset arithmetic for around_1e12 historical artifact.",
    )

    estimate = estimate_candidate_tail(block, 1000000008625, radius=None, q=1.25)

    assert abs(estimate.delta - Decimal("0.0055569683")) < Decimal("1e-13")
    assert abs(estimate.gbar_upper - Decimal("0.0014258627")) < Decimal("2e-8")
