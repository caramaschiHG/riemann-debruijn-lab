# Consolidated Reproduction Report

Date/time: 2026-06-08T20:57:55.094728+00:00

Nothing in this report proves the Riemann Hypothesis. Results are numerical, conditional, or heuristic unless explicitly stated otherwise.
This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Input Data
- Historical packages unpacked under `artifacts/unpacked/`.
- Selected source CSVs and reports copied into `outputs/reproduction/`.

## Precision Notes
- The 10^12 candidate is handled by base+offset values in the historical tables.
- High 10^21 rows require base+offset arithmetic and an explicit source precision warning.
- Existing tail outputs are treated as explicit-style conservative estimates pending mathematical review.

## Parameters
- Reproduction source: extracted historical artifacts.
- Candidate A: 1000000008625/1000000008626

## Claim Strength Legend
- FACT_FROM_SOURCE_DATA: copied from historical source artifacts.
- NUMERICAL_COMPUTATION: computed from source data by a finite calculation.
- HEURISTIC_ESTIMATE: diagnostic model output without full analytic control.
- EXPLICIT_STYLE_BOUND: conservative explicit-style envelope pending mathematical review.
- CONDITIONAL_STATEMENT: depends on stated data and assumptions.
- OPEN_PROBLEM: not established by this lab.

## Results
- [NUMERICAL_COMPUTATION] Robin best candidate up to 1,000,000: n = 10080, ratio = 1.755814338925297, margin = 0.025258079064901.
- [FACT_FROM_SOURCE_DATA] Best around_1e12 zero-gap pair from the historical artifact: 1000000008625/1000000008626, gap = 0.00555696829997032, normalized gap = 0.0216462265659802.
- [NUMERICAL_COMPUTATION] Lehmer local index for Candidate A: gbar local/truncated = 0.0014248568277801, local two-body scale = -3.8606750672474535e-06.
- [EXPLICIT_STYLE_BOUND] High-precision tail estimate for Candidate A: G local = 46.1418910247119700, tail upper-style contribution = 0.0325747320640552423, gbar upper-style value = 0.00142586273215612362.
- [CONDITIONAL_STATEMENT] Candidate A remains below the Lehmer threshold in this explicit-style calculation if the source table, zero-count envelope, endpoint policy, and arithmetic assumptions are accepted.
- [FACT_FROM_SOURCE_DATA] High-zero offset candidate: 1000000000000000001635/1000000000000000001636, gbar upper-style value = 0.00577988877287867924; source note: around_1e21 data are stated by Odlyzko as not guaranteed/probably accurate to 1e-6.
- [HEURISTIC_ESTIMATE] Finite-flow Candidate A radius 80: naive two-body time = -3.859987085859381e-06, finite threshold time = -3.860659994242403e-06.
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
