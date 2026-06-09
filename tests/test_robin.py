from riemann_lab.robin.robin_scan import scan_robin


def test_robin_10080_detected() -> None:
    rows = scan_robin(10080, top=10)

    assert any(row.n == 10080 for row in rows)
    best = rows[0]
    assert best.n == 10080
    assert abs(best.ratio_sigma_over_n_loglogn - 1.755814338925) < 1e-12

