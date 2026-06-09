from decimal import Decimal

from riemann_lab.data.schemas import make_zero_block
from riemann_lab.lehmer.index import analyze_pair


def test_lehmer_index_known_candidate_fixture() -> None:
    block = make_zero_block(
        name="around_1e12_fixture",
        start_index=1000000008623,
        base_height="267653395647",
        offsets=[
            "2215.1000000000",
            "2215.7218865151",
            "2216.1344650875",
            "2216.1400220558",
            "2216.4120000000",
            "2216.9000000000",
        ],
        precision_note="fixture based on historical around_1e12 candidate offsets",
    )

    result = analyze_pair(block, 1000000008625, radius=2)

    assert abs(result.delta - Decimal("0.0055569683")) < Decimal("1e-13")
    assert result.gbar_local < Decimal("0.8")
    assert result.normalized_gap < 0.03
