# Project Log

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## 2026-06-08

- Unpacked all zip packages into `artifacts/unpacked/`.
- Created a clean Python package under `src/riemann_lab`.
- Added base+offset zero schemas, loaders, gap ranking, Robin/Lagarias scans,
  Lehmer diagnostics, tail estimates, finite-flow diagnostics, gap-energy
  diagnostics, report helpers, and the `riemann-lab` CLI.
- Preserved historical artifacts as source data for reproduction.
- Added scripts to reproduce scans and build a consolidated reproduction report.

## Historical Results Preserved

- Robin scan to 1,000,000: best candidate `n = 10080`.
- Strongest observed finite gap candidate: `1000000008625 / 1000000008626`.
- Candidate A high-precision explicit-style `gbar_upper` around `0.0014258627`.
- Candidate A finite local flow threshold around `-3.860660e-6`.

