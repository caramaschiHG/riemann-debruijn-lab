# Summary

- 

## Claim-Safety Checklist

- [ ] No stronger mathematical claim was introduced without assumptions,
      provenance, and review path.
- [ ] Public docs and generated reports still say this project does not prove
      RH or establish `Lambda <= 0`.
- [ ] New data has provenance, source notes, and precision limitations.
- [ ] Numerical changes include tests or reproducibility notes.

## Validation

```powershell
python -m pytest
python -m compileall -q src scripts tests
python -m ruff check .
python scripts/check_claim_language.py
```
