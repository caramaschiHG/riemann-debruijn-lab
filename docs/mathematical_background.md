# Mathematical Background

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Zeta, Xi, and RH

For `Re(s) > 1`, the Riemann zeta function is

`zeta(s) = sum_{n >= 1} n^(-s)`.

It has analytic continuation to the complex plane except for a pole at `s = 1`.
The completed xi function is

`xi(s) = 1/2 * s * (s - 1) * pi^(-s/2) * Gamma(s/2) * zeta(s)`.

Define `Xi(x) = xi(1/2 + i x)`. RH is equivalent to all zeros of `Xi(x)` being
real.

## de Bruijn-Newman Lambda

The de Bruijn-Newman program studies a heat-deformed family `H_t`. The
constant `Lambda` marks the transition after which all zeros are real. RH is
equivalent to `Lambda <= 0`. Rodgers and Tao proved `Lambda >= 0`, so this
route would require `Lambda = 0` for RH.

This project only performs finite numerical and structural exploration around
that route.

## Lehmer Pairs

Given adjacent zeros `gamma_n` and `gamma_{n+1}`, define

- `Delta = gamma_{n+1} - gamma_n`
- `G = sum(1/(gamma - gamma_n)^2 + 1/(gamma - gamma_{n+1})^2)` over other zeros
- `g_bar = Delta^2 * G`

The classical Lehmer-pair threshold is `g_bar < 4/5`. In this package,
truncated values are labeled `gbar_local`; tail-assisted values are labeled
`gbar_upper` or `gbar_tail_estimated`. A tail-assisted value is still only as
strong as its zero-count assumptions, endpoint policy, and source-table
precision.

## Claim Strength Labels

- `FACT_FROM_SOURCE_DATA`: copied directly from a named source artifact.
- `NUMERICAL_COMPUTATION`: computed from input data by package code.
- `HEURISTIC_ESTIMATE`: uses an uncontrolled or diagnostic model.
- `EXPLICIT_STYLE_BOUND`: uses explicit constants and conservative envelopes,
  but still requires verification of assumptions and implementation.
- `CONDITIONAL_STATEMENT`: true only if stated inputs and assumptions are
  accepted.
- `OPEN_PROBLEM`: not established here.

## Robin and Lagarias Criteria

Robin's criterion states that RH is equivalent to

`sigma(n) < exp(gamma) n log log n` for all `n > 5040`.

Lagarias' criterion gives another equivalent inequality involving `sigma(n)`
and the harmonic number `H_n`:

`sigma(n) <= H_n + exp(H_n) log(H_n)`.

Finite scans of these criteria are diagnostics only.

## Odlyzko Tables

Odlyzko's zero tables are central input data for this lab. High-zero blocks
must be handled as `base_height + offset`. Tiny gaps must be computed from
offset differences, never by subtracting two huge float64 heights.
