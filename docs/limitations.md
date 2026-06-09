# Limitations

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Finite Computation

Finite scans can find dangerous examples, stable candidates, and correlations.
They cannot prove claims over all integers or all zeta zeros.

## Odlyzko Precision

High-zero tables can have limited displayed precision. The package uses
base+offset arithmetic to avoid float64 cancellation, but correct arithmetic
does not recover precision absent from the source table.

## Tail Estimates

The explicit-style tail code uses zero-counting envelopes and binned
contributions. It should be reviewed before being called a rigorous certificate
or proof. The default report language is deliberately conservative.

Current tail outputs are labeled `EXPLICIT_STYLE_BOUND` or
`CONDITIONAL_STATEMENT`, not `FACT_FROM_SOURCE_DATA`.

The current endpoint policy subtracts the known local-window endpoint from the
first tail bin on each side, so the local endpoint zeros are not intentionally
double-counted. This depends on the input table really containing an ordered
contiguous local window.

## Finite Flow

The model `dx_j/dt = 2 sum_{k != j} 1/(x_j - x_k)` is a finite local heuristic.
It is useful for local near-collision diagnostics but is not the full `H_t`
equation.

## Gap Energy

Weighted gap energies are experimental. Observed stability or correlation does
not establish a global inequality.
