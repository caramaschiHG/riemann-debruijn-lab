"""Build a consolidated reproduction report from historical artifacts."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from riemann_lab.constants import KNOWN_CANDIDATES, report_warning_block


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts" / "unpacked"
OUT = ROOT / "outputs" / "reproduction"


def first_row(path: Path, predicate=None) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if predicate is None or predicate(row):
                return row
    raise RuntimeError(f"No matching row in {path}")


def copy_if_exists(source: Path, target_dir: Path) -> None:
    if source.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target_dir / source.name)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = OUT / "tables"
    figures = OUT / "figures"
    reports = OUT / "source_reports"
    for path in [
        ARTIFACTS / "rh_lab_package" / "rh_lab_run_1M_robin_worst.csv",
        ARTIFACTS / "zeta_gap_collision_r80_package" / "zeta_gap_collision_r80_top_pairs.csv",
        ARTIFACTS / "lehmer_index_package_plus" / "lehmer_index_top25_by_lambda.csv",
        ARTIFACTS / "lehmer_explicit_tail_cert_package" / "lehmer_explicit_tail_cert_summary.csv",
        ARTIFACTS / "lehmer_hp_offset_cert_package_plus" / "lehmer_hp_offset_cert_summary.csv",
        ARTIFACTS / "lehmer_hp_offset_cert_package_plus" / "lehmer_hp_offset_uncertainty_stress.csv",
        ARTIFACTS / "gap_energy_flow_package" / "gap_energy_flow_candidate_summary.csv",
    ]:
        copy_if_exists(path, tables)
    for path in [
        ARTIFACTS / "gap_energy_flow_package" / "gap_energy_flow_finite_flow_collision_time_by_radius.png",
        ARTIFACTS / "gap_energy_flow_package" / "gap_energy_flow_normalized_gap_vs_energy.png",
        ARTIFACTS / "lehmer_hp_offset_cert_package_plus" / "lehmer_hp_offset_cert_gbar_upper_by_q.png",
    ]:
        copy_if_exists(path, figures)
    for path in [
        ARTIFACTS / "rh_lab_package" / "rh_lab_run_1M_report.txt",
        ARTIFACTS / "zeta_gap_collision_r80_package" / "zeta_gap_collision_r80_report.txt",
        ARTIFACTS / "lehmer_index_package_plus" / "lehmer_index_report.txt",
        ARTIFACTS / "lehmer_explicit_tail_cert_package" / "lehmer_explicit_tail_cert_report.txt",
        ARTIFACTS / "lehmer_hp_offset_cert_package_plus" / "lehmer_hp_offset_cert_report.txt",
        ARTIFACTS / "gap_energy_flow_package" / "gap_energy_flow_report.txt",
    ]:
        copy_if_exists(path, reports)

    robin = first_row(ARTIFACTS / "rh_lab_package" / "rh_lab_run_1M_robin_worst.csv")
    top_gap = first_row(
        ARTIFACTS / "zeta_gap_collision_r80_package" / "zeta_gap_collision_r80_top_pairs.csv",
        lambda row: row["dataset"] == "around_1e12",
    )
    lehmer = first_row(
        ARTIFACTS / "lehmer_index_package_plus" / "lehmer_index_top25_by_lambda.csv",
        lambda row: row["zero_index_left"] == "1000000008625",
    )
    tail = first_row(
        ARTIFACTS / "lehmer_hp_offset_cert_package_plus" / "lehmer_hp_offset_cert_summary.csv",
        lambda row: row["zero_index_left"] == "1000000008625"
        and row["q_geometric"] == "1.25",
    )
    high = first_row(
        ARTIFACTS / "lehmer_hp_offset_cert_package_plus" / "lehmer_hp_offset_cert_summary.csv",
        lambda row: row["zero_index_left"] == "1000000000000000001635"
        and row["q_geometric"] == "1.25",
    )
    flow = first_row(
        ARTIFACTS / "gap_energy_flow_package" / "gap_energy_flow_candidate_summary.csv",
        lambda row: row["zero_index_left"] == "1000000008625",
    )
    candidate_a = KNOWN_CANDIDATES["A"]
    text = f"""# Consolidated Reproduction Report

Date/time: {datetime.now(timezone.utc).isoformat()}

{report_warning_block()}

## Input Data
- Historical packages unpacked under `artifacts/unpacked/`.
- Selected source CSVs and reports copied into `outputs/reproduction/`.

## Precision Notes
- The 10^12 candidate is handled by base+offset values in the historical tables.
- High 10^21 rows require base+offset arithmetic and an explicit source precision warning.
- Existing tail outputs are treated as explicit-style conservative estimates pending mathematical review.

## Parameters
- Reproduction source: extracted historical artifacts.
- Candidate A: {candidate_a.left_index}/{candidate_a.right_index}

## Claim Strength Legend
- FACT_FROM_SOURCE_DATA: copied from historical source artifacts.
- NUMERICAL_COMPUTATION: computed from source data by a finite calculation.
- HEURISTIC_ESTIMATE: diagnostic model output without full analytic control.
- EXPLICIT_STYLE_BOUND: conservative explicit-style envelope pending mathematical review.
- CONDITIONAL_STATEMENT: depends on stated data and assumptions.
- OPEN_PROBLEM: not established by this lab.

## Results
- [NUMERICAL_COMPUTATION] Robin best candidate up to 1,000,000: n = {robin['n']}, ratio = {robin['ratio_sigma_over_n_loglogn']}, margin = {robin['margin_exp_gamma_minus_ratio']}.
- [FACT_FROM_SOURCE_DATA] Best around_1e12 zero-gap pair from the historical artifact: {top_gap['zero_index_left']}/{top_gap['zero_index_right']}, gap = {top_gap['gap']}, normalized gap = {top_gap['normalized_gap']}.
- [NUMERICAL_COMPUTATION] Lehmer local index for Candidate A: gbar local/truncated = {lehmer['gbar_delta2_G']}, local two-body scale = {lehmer['lambda_lower_truncated']}.
- [EXPLICIT_STYLE_BOUND] High-precision tail estimate for Candidate A: G local = {tail['G_local_input']}, tail upper-style contribution = {tail['total_tail_G_bound_hp']}, gbar upper-style value = {tail['gbar_upper_hp']}.
- [CONDITIONAL_STATEMENT] Candidate A remains below the Lehmer threshold in this explicit-style calculation if the source table, zero-count envelope, endpoint policy, and arithmetic assumptions are accepted.
- [FACT_FROM_SOURCE_DATA] High-zero offset candidate: {high['zero_index_left']}/{high['zero_index_right']}, gbar upper-style value = {high['gbar_upper_hp']}; source note: {high['source_accuracy_note']}.
- [HEURISTIC_ESTIMATE] Finite-flow Candidate A radius {flow['radius']}: naive two-body time = {flow['naive_pair_collision_t']}, finite threshold time = {flow['finite_ode_threshold_t']}.
- [OPEN_PROBLEM] No global inequality controlling all gaps under the true H_t flow is proved here.

## Interpretation
These outputs reproduce the current lab summary: the strongest observed finite candidate remains the Odlyzko around_1e12 pair. It is interesting because the gap is extremely small after local normalization, the local Lehmer index is far below 4/5, the explicit-style tail contribution is tiny compared with the local sum, and the finite local flow behaves close to the two-body near-collision scale.

This does not imply RH because RH is an infinite global statement about all non-trivial zeros, while these are finite computations on selected tables plus modeled tails. It does not imply Lambda <= 0 because the finite local flow is not the true H_t flow and no global energy or monotonicity inequality has been proved.

## Limitations
- Finite computation does not prove an infinite statement.
- The explicit-style tail implementation must be reviewed before any stronger rigorous-certificate language.
- High-zero table precision can dominate conclusions; base+offset arithmetic avoids float64 cancellation but cannot create missing source precision.
- The finite flow is a local heuristic model, not the full H_t dynamics.

## Next Steps
- Add more Odlyzko blocks with source metadata and offset fixtures.
- Compare normalized gap, gbar, local energy, and finite collision time across all candidates.
- Improve H_t tracking with higher-quality quadrature.
- Explore interval arithmetic for small certified cases.
"""
    (OUT / "consolidated_reproduction_report.md").write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
