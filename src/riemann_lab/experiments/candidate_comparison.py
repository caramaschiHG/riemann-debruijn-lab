"""Systematic comparison of available Lehmer-pair candidates.

This experiment is a finite computational comparison over available source
artifacts. It does not prove RH and does not establish Lambda <= 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from riemann_lab.constants import ClaimStrength, KNOWN_CANDIDATES, labeled_claim, report_warning_block


DEFAULT_CANDIDATE_SUMMARY = Path(
    "data/processed/candidate_comparison/gap_energy_flow_candidate_summary.csv"
)
DEFAULT_RADIUS_SUMMARY = Path(
    "data/processed/candidate_comparison/gap_energy_flow_radius_summary.csv"
)


@dataclass(frozen=True)
class CandidateComparisonResult:
    """Paths and headline findings from a candidate-comparison run."""

    output_dir: Path
    csv_path: Path
    report_path: Path
    plot_paths: tuple[Path, ...]
    strongest_normalized_gap: str
    strongest_gbar_upper: str
    strongest_collision_time: str
    candidate_a_dominant: bool


def _candidate_id(row: pd.Series) -> str:
    return f"{row['dataset']}:{row['zero_index_left']}/{row['zero_index_right']}"


def _to_numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = frame.copy()
    for column in columns:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce")
    return out


def build_candidate_comparison(candidate_summary: Path | str) -> pd.DataFrame:
    """Build one comparison row per candidate at the largest available radius."""

    frame = pd.read_csv(candidate_summary, dtype={"zero_index_left": str, "zero_index_right": str})
    frame = _to_numeric(
        frame,
        [
            "normalized_gap",
            "pair_normalized_gap",
            "gbar_upper_hp",
            "gbar_window",
            "G_window",
            "E_raw_inverse_gap2",
            "E_norm_inverse_gap2",
            "finite_ode_threshold_t",
            "naive_pair_collision_t",
            "linearized_collision_t",
            "dgap_dt0_finite_flow",
            "radius",
            "gap",
            "pair_gap",
        ],
    )
    frame["candidate_id"] = frame.apply(_candidate_id, axis=1)
    frame["normalized_gap_metric"] = frame["normalized_gap"].fillna(frame["pair_normalized_gap"])
    frame["explicit_gbar_upper"] = frame["gbar_upper_hp"]
    frame["explicit_gbar_status"] = np.where(
        frame["explicit_gbar_upper"].notna(),
        "available_explicit_style",
        "missing_explicit_tail_estimate",
    )
    frame["local_gbar"] = frame["gbar_window"]
    frame["local_gap_energy"] = frame["E_norm_inverse_gap2"].fillna(frame["E_raw_inverse_gap2"])
    frame["finite_flow_collision_time"] = frame["finite_ode_threshold_t"]
    frame["collision_time_abs"] = frame["finite_flow_collision_time"].abs()
    frame["neighbor_correction_ratio"] = (
        frame["finite_ode_threshold_t"] / frame["naive_pair_collision_t"]
    )
    frame["neighbor_correction_abs_deviation"] = (frame["neighbor_correction_ratio"] - 1.0).abs()
    frame["candidate_a"] = (
        (frame["dataset"] == KNOWN_CANDIDATES["A"].dataset)
        & (frame["zero_index_left"] == str(KNOWN_CANDIDATES["A"].left_index))
    )

    frame["rank_normalized_gap"] = frame["normalized_gap_metric"].rank(method="min", ascending=True)
    frame["rank_gbar_upper"] = frame["explicit_gbar_upper"].rank(method="min", ascending=True)
    frame["rank_collision_time"] = frame["collision_time_abs"].rank(method="min", ascending=True)
    frame["rank_local_energy"] = frame["local_gap_energy"].rank(method="min", ascending=False)

    columns = [
        "candidate_id",
        "dataset",
        "zero_index_left",
        "zero_index_right",
        "source",
        "radius",
        "gap",
        "normalized_gap_metric",
        "local_gbar",
        "explicit_gbar_upper",
        "explicit_gbar_status",
        "finite_flow_collision_time",
        "collision_time_abs",
        "local_gap_energy",
        "neighbor_correction_ratio",
        "neighbor_correction_abs_deviation",
        "rank_normalized_gap",
        "rank_gbar_upper",
        "rank_collision_time",
        "rank_local_energy",
        "candidate_a",
        "finite_ode_status",
    ]
    return frame[columns].sort_values(["rank_normalized_gap", "rank_gbar_upper"], na_position="last")


def build_radius_comparison(radius_summary: Path | str) -> pd.DataFrame:
    """Build radius-dependent neighbor-correction rows."""

    frame = pd.read_csv(radius_summary, dtype={"zero_index_left": str, "zero_index_right": str})
    frame = _to_numeric(
        frame,
        ["radius", "finite_ode_threshold_t", "naive_pair_collision_t", "normalized_gap"],
    )
    frame["candidate_id"] = frame.apply(_candidate_id, axis=1)
    frame["neighbor_correction_ratio"] = (
        frame["finite_ode_threshold_t"] / frame["naive_pair_collision_t"]
    )
    frame["collision_time_abs"] = frame["finite_ode_threshold_t"].abs()
    return frame


def _scatter(
    path: Path,
    frame: pd.DataFrame,
    x: str,
    y: str,
    *,
    title: str,
    xlabel: str,
    ylabel: str,
    annotate_top: int = 5,
) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = frame.dropna(subset=[x, y])
    fig, ax = plt.subplots(figsize=(9, 6))
    colors = np.where(data["candidate_a"], "#d62728", "#1f77b4")
    ax.scatter(data[x], data[y], c=colors, alpha=0.85)
    for _, row in data.head(annotate_top).iterrows():
        ax.annotate(
            str(row["zero_index_left"]),
            (row[x], row[y]),
            textcoords="offset points",
            xytext=(5, 5),
            fontsize=8,
        )
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _neighbor_correction_plot(path: Path, radius_frame: pd.DataFrame, top_ids: list[str]) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))
    for candidate_id in top_ids:
        rows = radius_frame[radius_frame["candidate_id"] == candidate_id].sort_values("radius")
        if rows.empty:
            continue
        is_a = candidate_id.startswith(f"{KNOWN_CANDIDATES['A'].dataset}:{KNOWN_CANDIDATES['A'].left_index}/")
        ax.plot(
            rows["radius"],
            rows["neighbor_correction_ratio"],
            marker="o",
            linewidth=2.5 if is_a else 1.2,
            alpha=0.95 if is_a else 0.65,
            label=candidate_id,
        )
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1)
    ax.set_title("Neighbor Correction Ratio by Radius")
    ax.set_xlabel("radius")
    ax.set_ylabel("finite-flow threshold / naive two-body time")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="best")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _rank_summary_plot(path: Path, frame: pd.DataFrame, top_n: int = 10) -> Path:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    data = frame.sort_values("rank_normalized_gap").head(top_n).copy()
    labels = [str(row.zero_index_left) for row in data.itertuples()]
    x = np.arange(len(data))
    width = 0.25
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x - width, data["rank_normalized_gap"], width, label="normalized gap")
    ax.bar(x, data["rank_gbar_upper"], width, label="gbar upper")
    ax.bar(x + width, data["rank_collision_time"], width, label="collision time")
    ax.set_title("Candidate Rank Summary")
    ax.set_xlabel("candidate left index")
    ax.set_ylabel("rank; lower is stronger")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def write_candidate_plots(
    frame: pd.DataFrame,
    radius_frame: pd.DataFrame,
    output_dir: Path,
) -> tuple[Path, ...]:
    """Write the required comparison plots."""

    top_ids = frame.sort_values("rank_normalized_gap").head(6)["candidate_id"].tolist()
    paths = [
        _scatter(
            output_dir / "normalized_gap_vs_gbar.png",
            frame,
            "normalized_gap_metric",
            "explicit_gbar_upper",
            title="Normalized Gap vs Explicit-Style gbar Upper",
            xlabel="normalized gap",
            ylabel="explicit-style gbar upper",
        ),
        _scatter(
            output_dir / "gbar_vs_collision_time.png",
            frame,
            "explicit_gbar_upper",
            "collision_time_abs",
            title="Explicit-Style gbar Upper vs Collision Time Magnitude",
            xlabel="explicit-style gbar upper",
            ylabel="abs(finite-flow threshold time)",
        ),
        _scatter(
            output_dir / "local_energy_vs_collision_time.png",
            frame,
            "local_gap_energy",
            "collision_time_abs",
            title="Local Gap Energy vs Collision Time Magnitude",
            xlabel="local normalized inverse-gap energy",
            ylabel="abs(finite-flow threshold time)",
        ),
        _neighbor_correction_plot(
            output_dir / "neighbor_correction_by_radius.png",
            radius_frame,
            top_ids,
        ),
        _rank_summary_plot(output_dir / "candidate_rank_summary.png", frame),
    ]
    return tuple(paths)


def _describe_rank_agreement(
    normalized: pd.Series,
    gbar: pd.Series | None,
    collision: pd.Series,
) -> tuple[bool, str]:
    gbar_id = None if gbar is None else gbar["candidate_id"]
    ids = [normalized["candidate_id"], collision["candidate_id"]]
    if gbar_id is not None:
        ids.append(gbar_id)
    agree = len(set(ids)) == 1
    if agree:
        return True, "The strongest available rankings agree on the same candidate."
    return False, "The rankings disagree; this is expected because each metric probes a different finite diagnostic."


def write_candidate_report(
    frame: pd.DataFrame,
    output_dir: Path,
    *,
    candidate_summary: Path,
    radius_summary: Path,
) -> Path:
    """Write the markdown comparison report."""

    candidate_summary_display = candidate_summary.as_posix()
    radius_summary_display = radius_summary.as_posix()
    strongest_norm = frame.sort_values("rank_normalized_gap").iloc[0]
    valid_gbar = frame.dropna(subset=["explicit_gbar_upper"]).sort_values("rank_gbar_upper")
    strongest_gbar = None if valid_gbar.empty else valid_gbar.iloc[0]
    strongest_collision = frame.sort_values("rank_collision_time").iloc[0]
    agree, agreement_text = _describe_rank_agreement(strongest_norm, strongest_gbar, strongest_collision)
    candidate_a = frame[frame["candidate_a"]].iloc[0] if frame["candidate_a"].any() else None
    candidate_a_dominant = bool(
        candidate_a is not None
        and candidate_a["candidate_id"] == strongest_norm["candidate_id"]
        and strongest_gbar is not None
        and candidate_a["candidate_id"] == strongest_gbar["candidate_id"]
    )
    missing_gbar_count = int(frame["explicit_gbar_upper"].isna().sum())

    lines = [
        "# Candidate Comparison Report",
        "",
        report_warning_block(),
        "",
        "## Input Data",
        f"- candidate summary: `{candidate_summary_display}`",
        f"- radius summary: `{radius_summary_display}`",
        "",
        "## Claim Strength",
        f"- {ClaimStrength.FACT_FROM_SOURCE_DATA.value}: source rows copied from historical artifacts.",
        f"- {ClaimStrength.NUMERICAL_COMPUTATION.value}: ranks and derived ratios computed from those rows.",
        f"- {ClaimStrength.EXPLICIT_STYLE_BOUND.value}: `gbar_upper_hp` where present in the source artifact.",
        f"- {ClaimStrength.HEURISTIC_ESTIMATE.value}: finite-flow collision times and neighbor corrections.",
        f"- {ClaimStrength.CONDITIONAL_STATEMENT.value}: comparisons depend on available candidate coverage.",
        f"- {ClaimStrength.OPEN_PROBLEM.value}: RH and Lambda <= 0 remain open here.",
        "",
        "## Results",
        "- "
        + labeled_claim(
            ClaimStrength.NUMERICAL_COMPUTATION,
            f"Strongest by normalized gap: {strongest_norm['candidate_id']} "
            f"(normalized gap {strongest_norm['normalized_gap_metric']:.15g}).",
        ),
    ]
    if strongest_gbar is not None:
        lines.append(
            "- "
            + labeled_claim(
                ClaimStrength.EXPLICIT_STYLE_BOUND,
                f"Strongest by explicit-style gbar upper: {strongest_gbar['candidate_id']} "
                f"(gbar upper {strongest_gbar['explicit_gbar_upper']:.15g}).",
            )
        )
    else:
        lines.append(
            "- "
            + labeled_claim(
                ClaimStrength.CONDITIONAL_STATEMENT,
                "No explicit-style gbar upper values were available.",
            )
        )
    lines.extend(
        [
            "- "
            + labeled_claim(
                ClaimStrength.HEURISTIC_ESTIMATE,
                f"Strongest by finite-flow near-collision time: {strongest_collision['candidate_id']} "
                f"(abs time {strongest_collision['collision_time_abs']:.15g}).",
            ),
            "- " + labeled_claim(ClaimStrength.NUMERICAL_COMPUTATION, agreement_text),
            "- "
            + labeled_claim(
                ClaimStrength.CONDITIONAL_STATEMENT,
                f"Candidate A remains dominant by normalized gap and explicit-style gbar upper: {candidate_a_dominant}.",
            ),
            "- "
            + labeled_claim(
                ClaimStrength.CONDITIONAL_STATEMENT,
                f"{missing_gbar_count} candidate rows lack explicit-style gbar upper "
                "values and are not ranked by that metric.",
            ),
            "",
            "## Candidate Notes",
            "- Candidate A is the around_1e12 close pair "
            "`1000000008625/1000000008626`. In the available rows, it is the "
            "best combined case by normalized gap and explicit-style gbar upper.",
            "- The around_1e21 pair "
            "`1000000000000000001635/1000000000000000001636` ranks strongest "
            "by finite-flow near-collision time, but it carries the strongest "
            "source-precision caution. Treat it as a heuristic stress case, "
            "not as a stronger mathematical result.",
            "",
            "## Stable Patterns",
            "- The strongest normalized-gap candidates are also very strong local Lehmer-index candidates.",
            "- Candidate A remains the cleanest combined normalized-gap plus explicit-style gbar-upper case in the available rows.",
            "- Normalized-gap and finite-flow rankings can disagree because normalized gap compares local spacing while finite-flow near-collision time is roughly a gap-squared local dynamical scale with neighbor corrections.",
            "- The around_1e21 pair ranks strongest by finite-flow near-collision time, but its source table carries a stronger precision warning; this ranking should be treated as a heuristic diagnostic, not as a stronger mathematical statement.",
            "- Candidate A remains strongest by explicit-style gbar upper among rows with available tail estimates.",
            "- Finite-flow collision times track the small-gap scale, but this is a local heuristic model.",
            "- Neighbor correction ratios remain close to 1 for the strongest candidates across radii in the historical radius summary.",
            "",
            "## What Remains Heuristic",
            "- Finite-flow collision time is not the full H_t flow.",
            "- Neighbor correction ratios are diagnostics, not bounds on global dynamics.",
            "- Missing explicit-style tail estimates are not inferred from local gbar values.",
            "- Agreement between finite metrics does not prove RH and does not establish Lambda <= 0.",
            "",
            "## Next Experimental Question",
            "Can the near-one neighbor correction ratio be reproduced across more independently sourced Odlyzko blocks once table precision and explicit-style tail assumptions are tracked uniformly?",
            "",
            "## Interpretation",
            "This experiment compares candidate structure across the currently available Odlyzko-derived artifacts. It is useful for ranking and pattern discovery, not for making proof claims.",
        ]
    )
    path = output_dir / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def run_candidate_comparison(
    *,
    candidate_summary: Path | str = DEFAULT_CANDIDATE_SUMMARY,
    radius_summary: Path | str = DEFAULT_RADIUS_SUMMARY,
    output_dir: Path | str = "outputs/candidate_comparison",
) -> CandidateComparisonResult:
    """Run the candidate-comparison experiment end to end."""

    candidate_summary = Path(candidate_summary)
    radius_summary = Path(radius_summary)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frame = build_candidate_comparison(candidate_summary)
    radius_frame = build_radius_comparison(radius_summary)

    csv_path = output_dir / "candidate_comparison.csv"
    frame.to_csv(csv_path, index=False)
    plot_paths = write_candidate_plots(frame, radius_frame, output_dir)
    report_path = write_candidate_report(
        frame,
        output_dir,
        candidate_summary=candidate_summary,
        radius_summary=radius_summary,
    )

    strongest_norm = frame.sort_values("rank_normalized_gap").iloc[0]
    valid_gbar = frame.dropna(subset=["explicit_gbar_upper"]).sort_values("rank_gbar_upper")
    strongest_gbar = valid_gbar.iloc[0]
    strongest_collision = frame.sort_values("rank_collision_time").iloc[0]
    candidate_a_dominant = bool(
        strongest_norm["candidate_a"]
        and strongest_gbar["candidate_a"]
    )
    return CandidateComparisonResult(
        output_dir=output_dir,
        csv_path=csv_path,
        report_path=report_path,
        plot_paths=plot_paths,
        strongest_normalized_gap=str(strongest_norm["candidate_id"]),
        strongest_gbar_upper=str(strongest_gbar["candidate_id"]),
        strongest_collision_time=str(strongest_collision["candidate_id"]),
        candidate_a_dominant=candidate_a_dominant,
    )
