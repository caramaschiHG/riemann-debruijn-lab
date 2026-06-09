# Explicit-Style Tail Estimate Report

Date/time: 2026-06-08T21:03:16.665699+00:00

Nothing in this report proves the Riemann Hypothesis. Results are numerical, conditional, or heuristic unless explicitly stated otherwise.
This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Input Data
artifacts\unpacked\zeta_gap_collision_r80_package\zeta_gap_collision_r80_all_gaps.csv

## Precision Notes
Use base+offset arithmetic; displayed offsets are the trusted gap source.

## Parameters
- candidate: 1000000008625
- radius: 80
- q: 1.25

## Results
- [NUMERICAL_COMPUTATION] Delta: 0.0055569683
- [NUMERICAL_COMPUTATION] G_local: 45.4179904624241448966040193559882092410308421076677973430924
- [EXPLICIT_STYLE_BOUND] tail upper-style contribution: 1.321878324309634860599509012906368976429
- [EXPLICIT_STYLE_BOUND] G_total upper-style estimate: 46.7398687867337797572035283688945782174598421076677973430924
- [CONDITIONAL_STATEMENT] gbar upper-style estimate: 0.00144332231930785168679117078419779163067710335398708925952099
- [CONDITIONAL_STATEMENT] margin to 0.8: 0.798556677680692148313208829215802208369322896646012910740479
- [CONDITIONAL_STATEMENT] below 0.8 under stated assumptions: True

## Interpretation
Under the stated assumptions, a positive margin is evidence that the selected candidate remains below the Lehmer threshold in this explicit-style model. This is not a proof of RH, not a proof that Lambda <= 0, and not a fully reviewed rigorous certificate.

## Limitations
- The explicit-style tail implementation needs mathematical review before stronger claims.
- The zero-count envelope, endpoint policy, and source table precision are assumptions.
- The word certificate is intentionally avoided here except as a possible future goal.

## Next Steps
- Review assumptions before using results in a stronger claim.

## Tail Bound Assumptions
- zero_count_formula: Riemann-von Mangoldt main term N0(T)=T/(2pi)log(T/(2pi))-T/(2pi)+7/8 with envelope N_lower <= N(T) <= N_upper.
- s_t_bound: Trudgian-style |S(T)| <= 0.112 log T + 0.278 log log T + 2.510, plus a +/-1 slack term.
- table_precision_note: Use base+offset arithmetic; displayed offsets are the trusted gap source.
- endpoint_policy: The local window endpoints are known zeros included in G_local. The first tail bin on each side subtracts that known endpoint from the zero-count upper envelope to avoid double-counting local zeros.
- local_window_policy: G_local sums known zeros in the selected inclusive window and excludes the candidate pair endpoints. Tail bins cover only zeros outside that window.
- high_precision_policy: Candidate gaps and local distances use Decimal/mpmath base+offset arithmetic; tiny gaps are never computed by subtracting huge float64 heights.
- rigor_level: explicit_style
