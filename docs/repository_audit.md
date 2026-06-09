# Repository Audit for Public v0.1

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Commit

Commit source, tests, docs, curated small processed data, and public result
summaries:

- `src/riemann_lab/`
- `tests/`
- `scripts/`
- `docs/`
- `data/provenance.json`
- `data/processed/candidate_comparison/*.csv`
- `README.md`
- `REPRODUCIBILITY.md`
- `CONTRIBUTING.md`
- `CITATION.cff`
- `SECURITY.md`
- `.github/ISSUE_TEMPLATE/*.md`
- selected lightweight outputs under `outputs/candidate_comparison/` and
  `outputs/reproduction/` when intentionally refreshed for a release

## Ignore

Ignore generated local build and cache files:

- `__pycache__/`
- `.pytest_cache/`
- `.ruff_cache/`
- `*.egg-info/`
- virtual environments

Ignore heavy or duplicated historical bundles:

- root `*.zip`
- `artifacts/unpacked/`
- `artifacts/**/*.zip`

These artifacts are useful locally but should not be treated as canonical
source code.

## Data Policy

Raw Odlyzko-scale zero tables should normally be downloaded or restored from a
documented external source, not silently committed as opaque generated data.
For v0.1, the repository includes small curated processed CSVs needed by
`riemann-lab compare-candidates`. Larger historical all-gaps tables remain
local artifacts unless they are published as release assets with provenance.

## Generated Outputs

`outputs/` contains generated reports, CSVs, and plots. Release outputs can be
committed when they are deliberately refreshed and referenced by docs. Temporary
logs are ignored.

## Machine-Specific Paths

Public docs and scripts should use relative paths. Existing generated reports
are checked for dangerous mathematical claims; local absolute paths should not
be added to public-facing docs.

## Stale Artifacts

Historical packages under `artifacts/unpacked/` may use older wording such as
"certificate". Public docs now use "explicit-style tail estimate" unless
assumptions and limitations are explicit.

