# Reproducibility

This project does not prove the Riemann Hypothesis.
This project does not establish Lambda <= 0.
Finite-flow and gap-energy experiments are heuristic diagnostics.

## Install

```bash
python -m pip install -e ".[dev]"
```

## Validate

```bash
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

```bash
riemann-lab compare-candidates --out outputs/candidate_comparison
```

## Historical Artifact Reproduction

```bash
python scripts/reproduce_lehmer_scan.py
python scripts/reproduce_gap_energy.py
```

Historical reproduction scripts may require the local historical artifacts under
`artifacts/unpacked/`. The public candidate-comparison command uses curated
processed CSVs under `data/processed/candidate_comparison/`.

Some historical artifact names and copied source reports use legacy
`cert`/`certificate` wording. Public claims in this repository are governed by
the current claim-strength labels and disclaimers: these files are treated as
historical generated artifacts, not proof certificates.

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
