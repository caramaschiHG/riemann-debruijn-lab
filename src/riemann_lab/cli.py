"""Command line interface for riemann-lab."""

from __future__ import annotations

import argparse
from pathlib import Path

from riemann_lab.constants import ClaimStrength, KNOWN_CANDIDATES, labeled_claim, report_warning_block
from riemann_lab.data.loaders import load_zero_block, load_zero_block_from_gap_csv
from riemann_lab.data.odlyzko import precision_warning_for_dataset
from riemann_lab.debruijn.finite_flow import analyze_finite_flow
from riemann_lab.energy.experiments import compare_alphas
from riemann_lab.experiments.candidate_comparison import (
    DEFAULT_CANDIDATE_SUMMARY,
    DEFAULT_RADIUS_SUMMARY,
    run_candidate_comparison,
)
from riemann_lab.lehmer.certify import estimate_candidate_tail
from riemann_lab.lehmer.explicit_tail import bins_to_rows
from riemann_lab.lehmer.pairs import find_candidate_pairs
from riemann_lab.lehmer.uncertainty import stress_gbar_upper
from riemann_lab.reports.markdown import markdown_report, write_markdown
from riemann_lab.reports.plots import save_line_plot
from riemann_lab.reports.tables import write_dict_rows
from riemann_lab.robin.divisor_sums import sigma_sieve
from riemann_lab.robin.lagarias_scan import lagarias_report, scan_lagarias, write_lagarias_csv
from riemann_lab.robin.robin_scan import robin_report, scan_robin, write_robin_csv


def _load_block_from_args(args: argparse.Namespace):
    zeros = Path(args.zeros)
    if zeros.suffix.lower() == ".csv" and getattr(args, "dataset", None):
        precision_note = args.precision_note or precision_warning_for_dataset(args.dataset)
        return load_zero_block_from_gap_csv(
            zeros,
            dataset=args.dataset,
            name=args.name or args.dataset,
            precision_note=precision_note,
        )
    return load_zero_block(
        zeros,
        name=args.name,
        start_index=args.start_index,
        base_height=args.base_height,
        offset_column=args.offset_column,
        precision_note=args.precision_note or "",
    )


def _parse_alphas(raw: str) -> list[float]:
    return [float(part.strip()) for part in raw.split(",") if part.strip()]


def cmd_robin_scan(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    sigma = sigma_sieve(args.N)
    robin_rows = scan_robin(args.N, top=args.top, sigma=sigma)
    write_robin_csv(out / "robin_worst.csv", robin_rows)
    report_parts = [robin_report(args.N, robin_rows)]
    if args.lagarias:
        lagarias_rows = scan_lagarias(args.N, top=args.top, sigma=sigma)
        write_lagarias_csv(out / "lagarias_worst.csv", lagarias_rows)
        report_parts.append(lagarias_report(args.N, lagarias_rows))
    write_markdown(out / "report.md", "\n".join(report_parts))
    print(f"Wrote Robin scan outputs to {out}")
    return 0


def cmd_lehmer_scan(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    block = _load_block_from_args(args)
    pairs = find_candidate_pairs(block, top=args.top, radius=args.radius, by=args.by)
    rows = []
    for pair in pairs:
        row = {
            "rank": pair.rank,
            "dataset": block.name,
            "zero_index_left": pair.gap.left_index,
            "zero_index_right": pair.gap.right_index,
            "offset_left": str(pair.gap.left_offset),
            "offset_right": str(pair.gap.right_offset),
            "gap_delta": str(pair.gap.gap),
            "mid_height": str(pair.gap.mid_height),
            "normalized_gap": pair.gap.normalized_gap,
        }
        if pair.lehmer is not None:
            row.update(
                {
                    "radius": pair.lehmer.radius,
                    "zeros_used_in_G": pair.lehmer.zeros_used_in_G,
                    "edge_ok": pair.lehmer.edge_ok,
                    "G_local": str(pair.lehmer.G_local),
                    "gbar_local": str(pair.lehmer.gbar_local),
                    "is_lehmer_under_truncation": pair.lehmer.below_threshold_local,
                }
            )
        rows.append(row)
    write_dict_rows(out / "lehmer_candidates.csv", rows)
    best = rows[0]
    report = markdown_report(
        "Lehmer Scan Report",
        input_data=block.source or block.name,
        precision_notes=block.precision_note,
        parameters={"radius": args.radius, "top": args.top, "ranking": args.by},
        results=[
            f"Best candidate: {best['zero_index_left']}/{best['zero_index_right']}",
            f"gap Delta: {best['gap_delta']}",
            f"normalized gap: {best['normalized_gap']}",
            f"local gbar label: {best.get('gbar_local', 'not computed')}",
        ],
        interpretation=(
            "Pairs are ranked by finite numerical diagnostics. A local or truncated "
            "gbar value is not the true infinite gbar."
        ),
        limitations=[
            "Input table precision controls all numerical conclusions.",
            "Tail zeros outside the selected window are not included unless separately certified.",
        ],
    )
    write_markdown(out / "report.md", report)
    print(f"Wrote Lehmer scan outputs to {out}")
    return 0


def cmd_certify_tail(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    block = _load_block_from_args(args)
    estimate = estimate_candidate_tail(block, args.candidate, radius=args.radius, q=args.q)
    summary = {
        "dataset": block.name,
        "zero_index_left": estimate.pair.left_index,
        "zero_index_right": estimate.pair.right_index,
        "q_geometric": args.q,
        "gap_delta": str(estimate.delta),
        "G_local": str(estimate.G_local),
        "gbar_local": str(estimate.gbar_local),
        "tail_G_upper": str(estimate.tail_result.total_tail_G_bound),
        "G_total_upper": str(estimate.G_total_upper),
        "gbar_upper": str(estimate.gbar_upper),
        "margin_to_0_8": str(estimate.margin_to_threshold),
        "still_below_0_8": estimate.still_below_threshold,
        "tail_label": estimate.tail_result.label,
        "claim_strength": estimate.claim_strength.value,
        "tail_claim_strength": estimate.tail_result.claim_strength.value,
        "rigor_level": estimate.assumptions.rigor_level,
        "precision_note": estimate.precision_note,
    }
    write_dict_rows(out / "tail_estimate_summary.csv", [summary])
    write_dict_rows(
        out / "tail_estimate_bins.csv",
        bins_to_rows(
            estimate.tail_result.bins,
            block.name,
            f"{estimate.pair.left_index}/{estimate.pair.right_index}",
            args.q,
        ),
    )
    write_dict_rows(out / "tail_assumptions.csv", estimate.assumptions.as_rows())
    report = markdown_report(
        "Explicit-Style Tail Estimate Report",
        input_data=block.source or block.name,
        precision_notes=block.precision_note,
        parameters={"candidate": args.candidate, "radius": args.radius, "q": args.q},
        results=[
            labeled_claim(ClaimStrength.NUMERICAL_COMPUTATION, f"Delta: {estimate.delta}"),
            labeled_claim(ClaimStrength.NUMERICAL_COMPUTATION, f"G_local: {estimate.G_local}"),
            labeled_claim(
                ClaimStrength.EXPLICIT_STYLE_BOUND,
                f"tail upper-style contribution: {estimate.tail_result.total_tail_G_bound}",
            ),
            labeled_claim(
                ClaimStrength.EXPLICIT_STYLE_BOUND,
                f"G_total upper-style estimate: {estimate.G_total_upper}",
            ),
            labeled_claim(ClaimStrength.CONDITIONAL_STATEMENT, f"gbar upper-style estimate: {estimate.gbar_upper}"),
            labeled_claim(ClaimStrength.CONDITIONAL_STATEMENT, f"margin to 0.8: {estimate.margin_to_threshold}"),
            labeled_claim(
                ClaimStrength.CONDITIONAL_STATEMENT,
                f"below 0.8 under stated assumptions: {estimate.still_below_threshold}",
            ),
        ],
        interpretation=(
            "Under the stated assumptions, a positive margin is evidence that the selected "
            "candidate remains below the Lehmer threshold in this explicit-style model. "
            "This is not a proof of RH, not a proof that Lambda <= 0, and not a fully "
            "reviewed rigorous certificate."
        ),
        limitations=[
            "The explicit-style tail implementation needs mathematical review before stronger claims.",
            "The zero-count envelope, endpoint policy, and source table precision are assumptions.",
            "The word certificate is intentionally avoided here except as a possible future goal.",
        ],
    )
    report += "\n## Tail Bound Assumptions\n" + "\n".join(estimate.assumptions.markdown_lines()) + "\n"
    write_markdown(out / "report.md", report)
    print(f"Wrote explicit-style tail estimate outputs to {out}")
    return 0


def _known_candidate_by_left(left_index: int):
    for candidate in KNOWN_CANDIDATES.values():
        if candidate.left_index == left_index:
            return candidate
    return None


def cmd_uncertainty_stress(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    known = _known_candidate_by_left(args.candidate)
    gbar_upper = args.gbar_upper
    gap_delta = args.gap_delta
    if known is not None:
        gbar_upper = gbar_upper or known.gbar_upper
        gap_delta = gap_delta or known.delta
    if gbar_upper is None or gap_delta is None:
        raise SystemExit("Provide --gbar-upper and --gap-delta, or use a known candidate index")
    result = stress_gbar_upper(str(gbar_upper), str(gap_delta), args.epsilon)
    row = {
        "candidate": args.candidate,
        "gbar_upper": str(result.gbar_upper),
        "gap_delta": str(result.gap_delta),
        "epsilon": str(result.epsilon),
        "worst_gap_delta": str(result.worst_gap_delta),
        "stressed_gbar_upper": str(result.stressed_gbar_upper),
        "multiplier": str(result.multiplier),
        "still_below_0_8": result.still_below_threshold,
    }
    write_dict_rows(out / "uncertainty_stress.csv", [row])
    report = markdown_report(
        "Uncertainty Stress Report",
        input_data="Known candidate constants or supplied CLI values",
        precision_notes="Endpoint uncertainty is modeled as a worst-case gap increase by 2*epsilon.",
        parameters={"candidate": args.candidate, "epsilon": args.epsilon},
        results=[
            f"base gbar upper: {result.gbar_upper}",
            f"worst gap delta: {result.worst_gap_delta}",
            f"stressed gbar upper: {result.stressed_gbar_upper}",
            f"still below 0.8: {result.still_below_threshold}",
        ],
        interpretation="This tests sensitivity to endpoint precision, not a new tail proof.",
    )
    write_markdown(out / "report.md", report)
    print(f"Wrote uncertainty stress outputs to {out}")
    return 0


def cmd_gap_energy(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    block = _load_block_from_args(args)
    alphas = _parse_alphas(args.alphas)
    results = compare_alphas(block, alphas, weight=args.weight)
    rows = [
        {"dataset": block.name, "alpha": item.alpha, "weight": item.weight, "energy": item.energy}
        for item in results
    ]
    write_dict_rows(out / "gap_energy.csv", rows)
    try:
        save_line_plot(
            out / "gap_energy_by_alpha.png",
            [item.alpha for item in results],
            [item.energy for item in results],
            title="Gap Energy by Alpha",
            xlabel="alpha",
            ylabel="energy",
        )
    except Exception as exc:  # pragma: no cover - plotting backend dependent
        print(f"Plot skipped: {exc}")
    report = markdown_report(
        "Gap Energy Report",
        input_data=block.source or block.name,
        precision_notes=block.precision_note,
        parameters={"alphas": args.alphas, "weight": args.weight},
        results=[f"alpha {item.alpha}: E = {item.energy}" for item in results],
        interpretation="Gap energies are experimental diagnostics for comparing zero blocks.",
        limitations=["No global boundedness or monotonicity claim is established."],
    )
    write_markdown(out / "report.md", report)
    print(f"Wrote gap energy outputs to {out}")
    return 0


def cmd_finite_flow(args: argparse.Namespace) -> int:
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    block = _load_block_from_args(args)
    result = analyze_finite_flow(block, args.candidate, radius=args.radius)
    row = {
        "dataset": block.name,
        "zero_index_left": result.left_index,
        "zero_index_right": result.right_index,
        "radius": result.radius,
        "pair_gap": result.pair_gap,
        "dgap_dt0_finite_flow": result.dgap_dt0_finite_flow,
        "naive_pair_collision_t": result.naive_pair_collision_t,
        "linearized_collision_t": result.linearized_collision_t,
        "finite_threshold_t": result.finite_threshold_t,
        "window_zero_count": result.window_zero_count,
    }
    write_dict_rows(out / "finite_flow.csv", [row])
    report = markdown_report(
        "Finite Flow Report",
        input_data=block.source or block.name,
        precision_notes=block.precision_note,
        parameters={"candidate": args.candidate, "radius": args.radius},
        results=[
            f"pair gap: {result.pair_gap}",
            f"finite-flow dgap/dt at t=0: {result.dgap_dt0_finite_flow}",
            f"naive two-body collision time: {result.naive_pair_collision_t}",
            f"finite local threshold time: {result.finite_threshold_t}",
        ],
        interpretation=(
            "This supports or weakens local near-collision interpretation within the finite "
            "model only. It is not the full H_t flow."
        ),
        limitations=["Finite local flow is heuristic and does not prove Lambda <= 0."],
    )
    write_markdown(out / "report.md", report)
    print(f"Wrote finite-flow outputs to {out}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    root = Path(args.input)
    files = sorted(path for path in root.rglob("*") if path.is_file())
    lines = [
        "# Consolidated Research Report",
        "",
        report_warning_block(),
        "",
        "## Input Data",
        f"Collected from: {root}",
        "",
        "## Results",
    ]
    lines.extend(f"- {path.relative_to(root)}" for path in files[:200])
    if len(files) > 200:
        lines.append(f"- ... {len(files) - 200} additional files omitted from listing")
    lines.extend(
        [
            "",
            "## Interpretation",
            "This report is an index of generated outputs. Read each experiment report",
            "for parameters, precision notes, assumptions, and limitations.",
            "",
            "## Limitations",
            "- Consolidation does not add mathematical force to finite computations.",
            "- Tail and finite-flow outputs remain assumption-labeled diagnostics.",
            "",
            "## Next Steps",
            "- Review generated tables against source artifacts.",
            "- Add new zero blocks through base+offset loaders.",
        ]
    )
    text = "\n".join(lines) + "\n"
    output = Path(args.output) if args.output else root / f"consolidated_report.{args.format}"
    if args.format == "latex":
        from riemann_lab.reports.latex import markdown_to_simple_latex

        output.write_text(markdown_to_simple_latex(text), encoding="utf-8")
    else:
        output.write_text(text, encoding="utf-8")
    print(f"Wrote consolidated report to {output}")
    return 0


def cmd_compare_candidates(args: argparse.Namespace) -> int:
    result = run_candidate_comparison(
        candidate_summary=args.candidate_summary,
        radius_summary=args.radius_summary,
        output_dir=args.out,
    )
    print(f"Wrote candidate comparison CSV to {result.csv_path}")
    print(f"Wrote candidate comparison report to {result.report_path}")
    for path in result.plot_paths:
        print(f"Wrote plot {path}")
    return 0


def add_zero_block_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--zeros", required=True, help="Zero table path, offsets CSV, or all-gaps CSV")
    parser.add_argument("--dataset", help="Dataset label when loading an all-gaps CSV")
    parser.add_argument("--name", help="Dataset name for reports")
    parser.add_argument("--start-index", type=int, default=1, help="Global index of the first offset")
    parser.add_argument("--base-height", default="0", help="Large common height for base+offset tables")
    parser.add_argument("--offset-column", help="CSV offset column name")
    parser.add_argument("--precision-note", default="", help="Precision warning to include in reports")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="riemann-lab", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("robin-scan", help="Run a finite Robin criterion scan")
    p.add_argument("--N", type=int, required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--lagarias", action=argparse.BooleanOptionalAction, default=True)
    p.set_defaults(func=cmd_robin_scan)

    p = sub.add_parser("lehmer-scan", help="Scan a zero table for Lehmer candidates")
    add_zero_block_arguments(p)
    p.add_argument("--radius", type=int, default=80)
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--by", choices=["gap", "normalized_gap"], default="normalized_gap")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_lehmer_scan)

    p = sub.add_parser("certify-tail", help="Run an explicit-style tail estimate under assumptions")
    add_zero_block_arguments(p)
    p.add_argument("--candidate", type=int, required=True)
    p.add_argument("--radius", type=int, default=80)
    p.add_argument("--q", type=float, default=1.25)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_certify_tail)

    p = sub.add_parser("uncertainty-stress", help="Stress gbar under endpoint uncertainty")
    p.add_argument("--candidate", type=int, required=True)
    p.add_argument("--epsilon", required=True)
    p.add_argument("--gbar-upper", type=float)
    p.add_argument("--gap-delta", type=float)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_uncertainty_stress)

    p = sub.add_parser("gap-energy", help="Compute experimental gap energies")
    add_zero_block_arguments(p)
    p.add_argument("--alphas", default="1,1.5,2,3")
    p.add_argument("--weight", choices=["index", "none"], default="index")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_gap_energy)

    p = sub.add_parser("finite-flow", help="Run finite local zero-flow diagnostics")
    add_zero_block_arguments(p)
    p.add_argument("--candidate", type=int, required=True)
    p.add_argument("--radius", type=int, default=80)
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_finite_flow)

    p = sub.add_parser("report", help="Collect generated outputs into one report")
    p.add_argument("--input", required=True)
    p.add_argument("--format", choices=["markdown", "latex"], default="markdown")
    p.add_argument("--output")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser(
        "compare-candidates",
        help="Compare available Odlyzko-derived Lehmer candidate diagnostics",
    )
    p.add_argument("--candidate-summary", default=str(DEFAULT_CANDIDATE_SUMMARY))
    p.add_argument("--radius-summary", default=str(DEFAULT_RADIUS_SUMMARY))
    p.add_argument("--out", default="outputs/candidate_comparison")
    p.set_defaults(func=cmd_compare_candidates)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
