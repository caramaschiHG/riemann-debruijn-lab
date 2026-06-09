# Explicit Tail Audit

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Scope

This note audits the explicit-style tail pipeline in:

- `src/riemann_lab/lehmer/explicit_tail.py`
- `src/riemann_lab/lehmer/tail.py`
- `src/riemann_lab/lehmer/certify.py`
- `src/riemann_lab/zeros/offsets.py`

The current rigor level is `explicit_style`, not a fully reviewed rigorous
certificate.

## Definitions

For adjacent zeros `gamma_n` and `gamma_{n+1}`:

- `Delta = gamma_{n+1} - gamma_n`
- `G_local = sum(1/(gamma - gamma_n)^2 + 1/(gamma - gamma_{n+1})^2)` over
  known zeros in the chosen local window, excluding the candidate endpoints
- `G_tail = sum(...)` over zeros outside that local window
- `G_total = G_local + G_tail`
- `g_bar = Delta^2 * G_total`

The classical Lehmer-pair threshold is `g_bar < 4/5`. A value below this
threshold is a Lehmer-pair diagnostic under the adopted definition and data. It
does not imply RH and does not imply `Lambda <= 0`.

## Formula Currently Used

The explicit-style tail code partitions the unknown region outside a known
local window into geometric bins. For a left-side bin, distances from the left
candidate endpoint are between `d_near` and `d_far`; the right side is analogous
using the right candidate endpoint.

For each bin `[A, B]`, it computes an upper-style zero count:

`count_upper(A, B) = ceil(N_upper(B) - N_lower(A))`.

The zero-count envelopes use the Riemann-von Mangoldt main term:

`N0(T) = T/(2pi) log(T/(2pi)) - T/(2pi) + 7/8`

with a Trudgian-style error envelope:

`|S(T)| <= 0.112 log T + 0.278 log log T + 2.510`

and an additional `+/- 1` slack term in `N_upper` and `N_lower`.

For a bin at distance at least `d` from the nearer endpoint, the code uses

`fmax(d, Delta) = 1/d^2 + 1/(d + Delta)^2`.

The bin contribution is:

`G_bin <= count_upper_adjusted * fmax(d_near, Delta)`.

The current endpoint policy subtracts the known local-window endpoint from the
first tail bin on each side:

`count_upper_adjusted = max(0, count_upper_raw - 1)` for the first bin.

This is intended to avoid double-counting the known edge zero already included
in `G_local`.

## Arithmetic Policy

High-zero data are represented as:

`height = base_height + offset`.

Tiny gaps are computed as:

`offset[j+1] - offset[j]`.

The package intentionally avoids:

`float(base + offset[j+1]) - float(base + offset[j])`.

That bad pattern is catastrophic near heights such as `1e21`.

## Hidden Assumptions

- The input table window is contiguous and correctly ordered.
- The candidate pair indices refer to adjacent zeros in that table.
- The local window endpoints are known zeros and are already included in
  `G_local` unless they are the candidate endpoints.
- The zero-count envelope is applicable over every bin used.
- The displayed Odlyzko offsets carry enough precision for the intended
  comparison.
- The `S(T)` constants and slack terms are sufficient for the claimed use.
- Binned monotonicity is conservative only if the maximum contribution over a
  bin is taken at the nearest possible distance.
- The first-bin endpoint subtraction is valid only because the edge zero is
  known to lie in the raw closed interval counted by the envelope.

## Off-By-One and Endpoint Audit

`ZeroBlock.local_offsets(left_index, radius)` returns an inclusive window
`[lo, hi]`. The candidate endpoints are at positions `pair_pos` and
`pair_pos + 1`.

`G_local` iterates over the inclusive window and excludes exactly those two
candidate endpoints. Therefore the local endpoint zeros at `lo` and `hi` are
included when they are not the candidate endpoints.

The tail estimate requires `lo < pair_pos` and `hi > pair_pos + 1`. This
ensures at least one known zero outside the candidate pair on both sides. The
first tail bin on each side subtracts one known endpoint from the zero-count
upper envelope so that local endpoints are not intentionally counted twice.

This policy is conservative but not automatically rigorous until the
zero-count envelope and endpoint conventions are checked against the exact
theorem being used.

## Current Classification

- `Delta`: `NUMERICAL_COMPUTATION`
- `G_local`: `NUMERICAL_COMPUTATION`
- heuristic density tail: `HEURISTIC_ESTIMATE`
- binned explicit-style tail: `EXPLICIT_STYLE_BOUND`
- statement that `g_bar_upper < 0.8`: `CONDITIONAL_STATEMENT`
- RH or `Lambda <= 0`: `OPEN_PROBLEM`

## Current Limitations

- The implementation uses an explicit-style envelope, but the constants and
  preconditions have not been independently audited against a primary source.
- The code does not perform interval arithmetic.
- Source-table endpoint uncertainty is not integrated into the tail bound
  itself; it is handled by separate stress tests.
- The treatment of endpoints is documented and tested, but should be reviewed
  against the exact zero-counting convention.
- The result is not a proof of RH, not a proof that `Lambda <= 0`, and not a
  global statement about all zeros.

## What Would Be Required for a Truly Rigorous Certificate

- Pin the exact zero-counting theorem, constants, domain restrictions, and
  endpoint convention to primary literature.
- Prove that every bin count is an upper bound for the intended open or closed
  interval after endpoint subtraction.
- Use interval arithmetic or directed rounding for all local offsets,
  distances, gaps, and bin contributions.
- Incorporate source-table precision and endpoint uncertainty directly into
  the inequality.
- Validate the table indexing and adjacency assumptions from source metadata.
- Have the full argument reviewed independently by someone qualified in
  analytic number theory and rigorous numerical computation.

