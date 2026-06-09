# Contributing

This project welcomes careful, skeptical contributions.

## Ground Rules

- Do not claim this project proves RH.
- Do not claim this project establishes `Lambda <= 0`.
- Label finite computations, heuristic diagnostics, explicit-style estimates,
  and conditional statements clearly.
- Add provenance for new data.
- Add or update tests for numerical code.

## Development Setup

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
```

## Pull Request Checklist

- Run `python -m pytest`.
- Run `python -m compileall -q src scripts tests`.
- Run `python -m ruff check .`.
- Run `python scripts/check_claim_language.py`.
- Keep large historical artifacts out of Git unless they are intentionally
  published as release assets with provenance.

## Mathematical Claims

Any stronger mathematical claim must include:

- precise statement,
- assumptions,
- source references,
- reproducible computation if numerical,
- independent review path.

Prefer weaker language when in doubt.
