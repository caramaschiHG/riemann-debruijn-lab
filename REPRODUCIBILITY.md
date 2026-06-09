# Reproducibility

This project does not prove the Riemann Hypothesis.
This project does not establish Lambda <= 0.
Finite-flow and gap-energy experiments are heuristic diagnostics.

## Install

```powershell
python -m pip install -e ".[dev]"
```

## Validate

```powershell
python -m pytest
python -m compileall -q src scripts tests
python -m ruff check .
python scripts/check_claim_language.py
```

Expected current status:

- pytest: all tests pass
- compileall: no output and exit code 0
- ruff: all checks passed
- claim-language linter: no dangerous public claims found

## Clone-Safe Reproduction

This command uses committed curated CSVs and should work from a clean clone:

```powershell
riemann-lab compare-candidates --out outputs/candidate_comparison
```

## Historical Artifact Reproduction

```powershell
python scripts/reproduce_lehmer_scan.py
python scripts/reproduce_gap_energy.py
```

Historical reproduction scripts may require the local historical artifacts under
`artifacts/unpacked/`. The public candidate-comparison command uses curated
processed CSVs under `data/processed/candidate_comparison/`.

## Expected Key Values

- Candidate A: `1000000008625 / 1000000008626`
- Candidate A Delta: approximately `0.0055569683`
- Candidate A explicit-style `gbar_upper`: approximately `0.0014258627`
- Candidate A remains strongest by normalized gap and explicit-style
  `gbar_upper` in the available comparison rows.
- The `around_1e21` pair
  `1000000000000000001635 / 1000000000000000001636` ranks strongest by the
  finite-flow near-collision diagnostic in the current comparison.

Small numerical differences can occur due to library versions, plotting
backends, optional local artifacts, or source-table precision.

## Outputs

Important generated locations:

- `outputs/reproduction/`
- `outputs/candidate_comparison/`

Generated outputs must retain the standard disclaimer and claim-strength
labels.
