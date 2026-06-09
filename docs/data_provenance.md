# Data Provenance

Nothing in this report proves the Riemann Hypothesis. Results are numerical,
conditional, or heuristic unless explicitly stated otherwise.

This does not prove RH.
This is numerical/heuristic unless explicitly stated.
Lambda <= 0 is not established.

## Source Families

### Odlyzko Zero Tables

The zero ordinates used by the historical experiments are derived from
Odlyzko-style zeta zero tables. The project records three relevant blocks:

- `first_100k`: first 100,000 zeta zeros used in low-height experiments.
- `around_1e12`: a block around zero index `10^12`.
- `around_1e21`: a block around zero index `10^21`.

High-zero blocks require base+offset arithmetic. Tiny gaps must be computed as
`offset_right - offset_left`, not by subtracting two huge floating-point
heights.

### Historical Generated Artifacts

The original exploratory lab produced zip packages and unpacked CSV/PNG/TXT
artifacts. They are historical inputs to this refactor, not primary source
truth. Public-facing claims should cite them as historical generated artifacts.

### Curated Processed Data

The public comparison command uses small curated CSVs:

- `data/processed/candidate_comparison/gap_energy_flow_candidate_summary.csv`
- `data/processed/candidate_comparison/gap_energy_flow_radius_summary.csv`

These are copied from the historical `gap_energy_flow_package` output and
carry the same limitations.

## Reproduced Outputs

Current release outputs are generated under:

- `outputs/reproduction/`
- `outputs/candidate_comparison/`

Some files in `outputs/reproduction/source_reports/` are copied historical
reports. They are provenance evidence, not newly validated proofs.

## Precision Notes

- `first_100k`: low-height table; ordinary float summaries are less risky, but
  package gap computations should still use stored ordinates or offsets.
- `around_1e12`: use base+offset arithmetic; displayed offsets are trusted for
  gap-scale calculations in this repository.
- `around_1e21`: high-zero precision is weaker. Treat comparisons as sensitive
  to endpoint uncertainty and source precision.

## Replacing Data

To replace or extend datasets:

1. Add raw data under `data/raw/` only if licensing and size are acceptable.
2. Prefer documenting an external download source and adding a loader script.
3. Convert high-zero tables to `ZeroBlock(base_height, offsets)`.
4. Update `data/provenance.json`.
5. Refresh relevant outputs.
6. Run the claim-language linter before publishing.

## Not Bundled

Large original zero tables and duplicated zip packages are not required as
canonical public source files. They may be distributed separately as release
assets if their provenance and licensing are documented.

