# Candidate Comparison Report

Nothing in this report proves the Riemann Hypothesis. Results are numerical, conditional, or heuristic unless explicitly stated otherwise.
This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Input Data
- candidate summary: `data\processed\candidate_comparison\gap_energy_flow_candidate_summary.csv`
- radius summary: `data\processed\candidate_comparison\gap_energy_flow_radius_summary.csv`

## Claim Strength
- FACT_FROM_SOURCE_DATA: source rows copied from historical artifacts.
- NUMERICAL_COMPUTATION: ranks and derived ratios computed from those rows.
- EXPLICIT_STYLE_BOUND: `gbar_upper_hp` where present in the source artifact.
- HEURISTIC_ESTIMATE: finite-flow collision times and neighbor corrections.
- CONDITIONAL_STATEMENT: comparisons depend on available candidate coverage.
- OPEN_PROBLEM: RH and Lambda <= 0 remain open here.

## Results
- [NUMERICAL_COMPUTATION] Strongest by normalized gap: around_1e12:1000000008625/1000000008626 (normalized gap 0.0216462265659802).
- [EXPLICIT_STYLE_BOUND] Strongest by explicit-style gbar upper: around_1e12:1000000008625/1000000008626 (gbar upper 0.0014258627321561).
- [HEURISTIC_ESTIMATE] Strongest by finite-flow near-collision time: around_1e21:1000000000000000001635/1000000000000000001636 (abs time 3.51391325984075e-06).
- [NUMERICAL_COMPUTATION] The rankings disagree; this is expected because each metric probes a different finite diagnostic.
- [CONDITIONAL_STATEMENT] Candidate A remains dominant by normalized gap and explicit-style gbar upper: True.
- [CONDITIONAL_STATEMENT] 3 candidate rows lack explicit-style gbar upper values and are not ranked by that metric.

## Stable Patterns
- The strongest normalized-gap candidates are also very strong local Lehmer-index candidates.
- Candidate A remains the cleanest combined normalized-gap plus explicit-style gbar-upper case in the available rows.
- Normalized-gap and finite-flow rankings can disagree because normalized gap compares local spacing while finite-flow near-collision time is roughly a gap-squared local dynamical scale with neighbor corrections.
- The around_1e21 pair ranks strongest by finite-flow near-collision time, but its source table carries a stronger precision warning; this ranking should be treated as a heuristic diagnostic, not as a stronger mathematical statement.
- Candidate A remains strongest by explicit-style gbar upper among rows with available tail estimates.
- Finite-flow collision times track the small-gap scale, but this is a local heuristic model.
- Neighbor correction ratios remain close to 1 for the strongest candidates across radii in the historical radius summary.

## What Remains Heuristic
- Finite-flow collision time is not the full H_t flow.
- Neighbor correction ratios are diagnostics, not bounds on global dynamics.
- Missing explicit-style tail estimates are not inferred from local gbar values.
- Agreement between finite metrics does not prove RH and does not establish Lambda <= 0.

## Next Experimental Question
Can the near-one neighbor correction ratio be reproduced across more independently sourced Odlyzko blocks once table precision and explicit-style tail assumptions are tracked uniformly?

## Interpretation
This experiment compares candidate structure across the currently available Odlyzko-derived artifacts. It is useful for ranking and pattern discovery, not for making proof claims.
