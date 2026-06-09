# Riemann de Bruijn Lab

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Claim Policy](https://img.shields.io/badge/claims-explicitly_labeled-purple)

A reproducible Python laboratory for finite numerical experiments around zeta
zeros, Lehmer pairs, explicit-style tail estimates, and local
de Bruijn-Newman diagnostics.

This repository is designed for skeptical readers: every public result should
be reproducible, every data source should have provenance, and every
mathematical claim should be labeled by strength.

## Research Contract

This lab is intentionally conservative about mathematical language.

- It does not prove the Riemann Hypothesis.
- It does not establish `Lambda <= 0`.
- Finite-flow and gap-energy experiments are heuristic diagnostics.
- Explicit-style tail estimates are conditional on stated assumptions.
- Large historical artifacts are not treated as canonical source truth.

## What This Repository Contains

- `riemann_lab`, a Python package for zero-table loading, gap analysis,
  Lehmer-style diagnostics, finite scans, local flow experiments, and reports.
- `riemann-lab`, a CLI for reproducible experiments.
- Curated processed data for candidate comparison.
- Public result summaries under `outputs/`.
- Claim-language checks that fail on dangerous public phrasing.
- Issue templates for reproducibility problems and mathematical claim review.

## Claim Labels

Public reports use explicit claim-strength labels:

- `FACT_FROM_SOURCE_DATA`
- `NUMERICAL_COMPUTATION`
- `HEURISTIC_ESTIMATE`
- `EXPLICIT_STYLE_BOUND`
- `CONDITIONAL_STATEMENT`
- `OPEN_PROBLEM`

These labels are part of the repository's quality bar, not decoration.

## Quickstart

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python scripts/check_claim_language.py
```

## Clone-Safe Reproduction

The following command uses committed curated CSVs and should work from a clean
clone after installation:

```powershell
riemann-lab compare-candidates --out outputs/candidate_comparison
```

The historical reproduction scripts under `scripts/reproduce_*.py` may require
local artifacts under `artifacts/unpacked/`. Those large and duplicated
historical packages are intentionally ignored by Git and should be distributed
as release assets or restored from documented sources when needed.

## Example CLI Commands

Robin and Lagarias finite scan:

```powershell
riemann-lab robin-scan --N 1000000 --out outputs/robin_1M
```

Candidate comparison from committed curated data:

```powershell
riemann-lab compare-candidates --out outputs/candidate_comparison
```

Lehmer scan from a restored historical all-gaps artifact:

```powershell
riemann-lab lehmer-scan `
  --zeros artifacts/unpacked/zeta_gap_collision_r80_package/zeta_gap_collision_r80_all_gaps.csv `
  --dataset around_1e12 `
  --radius 80 `
  --out outputs/lehmer_1e12
```

Explicit-style tail estimate from a restored historical all-gaps artifact:

```powershell
riemann-lab certify-tail `
  --zeros artifacts/unpacked/zeta_gap_collision_r80_package/zeta_gap_collision_r80_all_gaps.csv `
  --dataset around_1e12 `
  --candidate 1000000008625 `
  --radius 80 `
  --out outputs/cert_1e12
```

## Current Finite Candidate Summary

Within the committed public summaries and local historical artifacts:

- Candidate A: `1000000008625 / 1000000008626`, around zero index `10^12`.
- Delta: approximately `0.0055569683`.
- Normalized gap: approximately `0.021646226566`.
- Explicit-style `gbar_upper`: approximately `0.0014258627`.
- Candidate A is strongest by normalized gap and explicit-style `gbar_upper`
  among the available comparison rows.
- The `around_1e21` pair
  `1000000000000000001635 / 1000000000000000001636` ranks strongest by the
  finite-flow near-collision diagnostic, with a stronger source-precision
  caution.

These are finite computational findings. They do not prove RH and do not
establish `Lambda <= 0`.

## Repository Map

- `src/riemann_lab/`: package code.
- `tests/`: regression tests for loaders, numerical routines, reports, and
  claim language.
- `scripts/`: reproducibility and report-building entry points.
- `docs/`: mathematical background, limitations, provenance, roadmap, and
  release checklists.
- `data/processed/`: small curated processed data committed for clean-clone
  workflows.
- `outputs/`: intentionally published result summaries, tables, and plots.
- `artifacts/`: local historical packages and unpacked generated artifacts;
  ignored by Git unless intentionally published elsewhere.

## Quality Gates

Before publishing changes:

```powershell
python -m pytest
python -m compileall -q src scripts tests
python -m ruff check .
python scripts/check_claim_language.py
```

These checks are intentionally short enough to run locally before each public
update.

## Limitations

- Finite scans do not prove infinite statements.
- Explicit-style tail estimates depend on zero-count envelopes, endpoint
  policies, source precision, and implementation details.
- The `around_1e21` block is precision-sensitive.
- Finite local zero-flow is not the full `H_t` flow.
- Gap energies are exploratory diagnostics, not established global
  inequalities.

See [docs/limitations.md](docs/limitations.md) and
[REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the full caveat set.

## References

- Clay Mathematics Institute, Riemann Hypothesis:
  https://www.claymath.org/millennium/riemann-hypothesis/
- Odlyzko zeta zero tables:
  http://www.dtc.umn.edu/~odlyzko/zeta_tables/
- Rodgers and Tao, work on the de Bruijn-Newman constant.
- Polymath work on de Bruijn-Newman bounds.
- Trudgian-style explicit estimates for zero-counting error terms.
- Robin and Lagarias RH-equivalent criteria.

## Citation

If you use this repository, cite the repository and separately cite the primary
mathematical and data sources you rely on. See [CITATION.cff](CITATION.cff).

## License

MIT. See [LICENSE](LICENSE).
