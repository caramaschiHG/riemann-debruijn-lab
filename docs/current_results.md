# Current Results

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## A. Candidate Comparison

The current candidate comparison uses the curated processed CSVs under
`data/processed/candidate_comparison/`.

- Candidate A, `around_1e12:1000000008625/1000000008626`, is strongest by
  normalized gap.
- Candidate A is also strongest among available explicit-style `gbar_upper`
  values.
- The `around_1e21:1000000000000000001635/1000000000000000001636` pair is
  strongest by the finite-flow near-collision diagnostic.
- These rankings do not fully agree.

Interpretation: normalized gap, explicit-style `gbar_upper`, and finite-flow
time measure different finite aspects of candidate "dangerousness." Disagreement
between them is useful signal for further study, not a contradiction and not a
proof claim.

## How to Read This Result

The normalized gap rescales a zero spacing by the local average spacing near
that height. A smaller normalized gap means that two consecutive zeros are
unusually close relative to their neighborhood.

The explicit-style `gbar_upper` value is an upper-style estimate for a
Lehmer-pair diagnostic after adding modeled tail contributions under stated
assumptions. Smaller values are interesting in this finite comparison, but the
estimate depends on source precision, endpoint policy, and the tail model.

The finite-flow near-collision diagnostic asks how quickly a local finite zero
model would push a close pair toward collision. It is a local dynamical proxy,
not the full `H_t` flow.

These rankings can disagree because they measure different finite features:
local spacing, tail-adjusted Lehmer structure, and local flow dynamics. A pair
can be strongest under one metric without being strongest under another.

None of this proves RH. RH is a global statement about all non-trivial zeta
zeros, while these are finite computations on selected data with explicit
precision and modeling assumptions. These results also do not establish
`Lambda <= 0`.

## B. Best Candidates in This Repository

### Candidate A

- Dataset: around zero index `10^12`
- Pair: `1000000008625 / 1000000008626`
- Delta: approximately `0.0055569683`
- Normalized gap: approximately `0.021646226566`
- Explicit-style `gbar_upper`: approximately `0.0014258627`

### Candidate B

- Dataset: first 100,000 zeros
- Pair: `95248 / 95249`
- Gap: approximately `0.0147014760005`
- Normalized gap: approximately `0.0218604660555`

### Candidate C

- Dataset: around zero index `10^21`
- Pair: `1000000000000000001635 / 1000000000000000001636`
- Gap: approximately `0.00530012000002`
- Precision caution: stronger source precision warning; use base+offset
  arithmetic and endpoint uncertainty stress.

### Classical Lehmer Reference

- Pair: `6709 / 6710`
- Included as a reference when supporting data are available.

## C. Meaning of These Results

These results identify interesting local zero structures:

- extremely small normalized gaps,
- small local Lehmer indices,
- small explicit-style `gbar_upper` values where available,
- finite local flow behavior close to two-body near-collision scales.

They do not prove anything global about RH. They do not establish `Lambda <= 0`.

## D. Mathematically Meaningful Next Steps

- Independent review of explicit-style tail assumptions.
- Interval arithmetic for small certified cases.
- Systematic Odlyzko sweeps with provenance records.
- More comparisons of candidate energy functionals.
- Search for stable structural inequalities that could be stated independently
  of the current finite datasets.
