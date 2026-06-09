from pathlib import Path

import pandas as pd

from riemann_lab.experiments.candidate_comparison import run_candidate_comparison


def _write_fixture_csvs(tmp_path: Path) -> tuple[Path, Path]:
    candidate = tmp_path / "candidate_summary.csv"
    radius = tmp_path / "radius_summary.csv"
    candidate.write_text(
        "\n".join(
            [
                "dataset,zero_index_left,zero_index_right,source,gbar_upper_hp,gap,normalized_gap,pair_normalized_gap,radius,G_window,gbar_window,E_raw_inverse_gap2,E_norm_inverse_gap2,dgap_dt0_finite_flow,naive_pair_collision_t,linearized_collision_t,finite_ode_threshold_t,finite_ode_status",
                "around_1e12,1000000008625,1000000008626,hp,0.0014,0.0055,0.021,0.021,80,45,0.0013,30000,2500,719,-0.0000038,-0.0000076,-0.0000039,ok",
                "first_100k,95248,95249,hp,0.0020,0.0147,0.022,0.022,80,9,0.0020,5000,2400,272,-0.000027,-0.000054,-0.000027,ok",
                "first_100k,44555,44556,top,,0.0295,0.040,0.040,80,6,0.0056,1600,890,135,-0.000109,-0.000218,-0.000109,ok",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    radius.write_text(
        "\n".join(
            [
                "dataset,zero_index_left,zero_index_right,source,gbar_upper_hp,gap,normalized_gap,radius,finite_ode_threshold_t,naive_pair_collision_t",
                "around_1e12,1000000008625,1000000008626,hp,0.0014,0.0055,0.021,5,-0.00000385,-0.0000038",
                "around_1e12,1000000008625,1000000008626,hp,0.0014,0.0055,0.021,80,-0.0000039,-0.0000038",
                "first_100k,95248,95249,hp,0.0020,0.0147,0.022,5,-0.0000271,-0.000027",
                "first_100k,95248,95249,hp,0.0020,0.0147,0.022,80,-0.000027,-0.000027",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return candidate, radius


def test_candidate_comparison_pipeline_outputs_files(tmp_path: Path) -> None:
    candidate, radius = _write_fixture_csvs(tmp_path)
    out = tmp_path / "out"

    result = run_candidate_comparison(
        candidate_summary=candidate,
        radius_summary=radius,
        output_dir=out,
    )

    assert result.csv_path.exists()
    assert result.report_path.exists()
    assert len(result.plot_paths) == 5
    assert all(path.exists() for path in result.plot_paths)
    assert result.strongest_normalized_gap == "around_1e12:1000000008625/1000000008626"
    assert result.strongest_gbar_upper == "around_1e12:1000000008625/1000000008626"
    assert result.candidate_a_dominant is True

    frame = pd.read_csv(result.csv_path)
    assert "neighbor_correction_ratio" in frame.columns
    assert "explicit_gbar_status" in frame.columns
    assert "missing_explicit_tail_estimate" in set(frame["explicit_gbar_status"])


def test_candidate_comparison_report_keeps_claims_limited(tmp_path: Path) -> None:
    candidate, radius = _write_fixture_csvs(tmp_path)
    result = run_candidate_comparison(
        candidate_summary=candidate,
        radius_summary=radius,
        output_dir=tmp_path / "out",
    )

    report = result.report_path.read_text(encoding="utf-8")

    assert "Nothing in this report proves the Riemann Hypothesis" in report
    assert "HEURISTIC_ESTIMATE" in report
    assert "EXPLICIT_STYLE_BOUND" in report
    assert "does not establish Lambda <= 0" in report
