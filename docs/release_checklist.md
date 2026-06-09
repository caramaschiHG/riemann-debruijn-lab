# Release Checklist

Use this before publishing a public release.

- [ ] `python -m pytest` passes
- [ ] `python -m ruff check .` passes
- [ ] `python -m compileall -q src scripts tests` passes
- [ ] `python scripts/reproduce_lehmer_scan.py` passes
- [ ] `python scripts/reproduce_gap_energy.py` passes
- [ ] `riemann-lab compare-candidates` passes
- [ ] `python scripts/check_claim_language.py` passes
- [ ] README reviewed for claim safety
- [ ] `docs/current_results.md` updated
- [ ] `docs/data_provenance.md` updated
- [ ] `data/provenance.json` updated
- [ ] `outputs/reproduction/` refreshed intentionally
- [ ] `outputs/candidate_comparison/` refreshed intentionally
- [ ] no large accidental files committed
- [ ] no machine-specific paths in public docs
- [ ] no false mathematical claims

