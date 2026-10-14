# Loan migration readiness

This project builds a small, reproducible data-quality workflow for a lender moving loan records from a legacy servicing platform to a new system.

The central question is simple: **is the target data complete, consistent, and financially safe to use?**

The workflow generates two synthetic extracts, introduces controlled migration defects, validates the file contracts, reconciles the systems with SQL, profiles the data, ranks the impact, applies documented corrections, and runs the checks again. The dashboard presents the result as a cutover readiness review.

> All records are synthetic. The project demonstrates a method for migration validation; it is not a production banking system.

## Results from seed 42

Run `make all` to reproduce the current results. The generated scorecard records the exact values used by the dashboard.

| Stage | Decision | Checks passed |
|---|---|---:|
| Before remediation | NO-GO | 0 / 7 |
| After remediation | GO | 7 / 7 |

The initial extract contains missing records, duplicate keys, orphan records, balance differences, status mismatches, and field-level defects. Remediation reloads missing source records, removes target-only records and duplicate keys, restores source fields, and re-tests the result.

## Project workflow

```text
legacy.csv + new_sys.csv
          |
   file-contract validation
          |
   data profile and null-rate review
          |
   eight named SQLite checks
          |
   scorecard and impact ranking
          |
   remediation
          |
   independent re-test
```

### Checks

1. Row counts and distinct loan IDs
2. Missing loans
3. Orphan loans
4. Duplicate loan IDs
5. Balance variance, split into material and rounding differences
6. Status mapping accuracy
7. Null interest rates and date shifts
8. Product-level balance control totals

Thresholds are stored in [`config/thresholds.json`](config/thresholds.json), rather than embedded in the scoring code. This makes the acceptance criteria visible and easy to change during a stakeholder review.

## Repository guide

| Path | Purpose |
|---|---|
| `src/generate_data.py` | Generates deterministic legacy, target, mapping, and defect-log tables |
| `src/validate_data.py` | Enforces the input data contract before SQL runs |
| `src/profile_data.py` | Produces column-level row, null, and distinct-value summaries |
| `src/run_reconciliation.py` | Loads CSVs into SQLite and exports each named query result |
| `src/remediate.py` | Applies the documented correction rules |
| `src/scorecard.py` | Builds before/after pass-fail results and impact totals |
| `sql/reconciliation.sql` | Portable, named reconciliation queries |
| `dashboard/app.py` | Streamlit view of the scorecard and control totals |
| `tests/` | Determinism, contract, injected-defect, and reconciliation tests |
| `docs/` | Business context, field definitions, porting notes, and dashboard instructions |

## Quickstart

```powershell
python -m pip install -r requirements.txt
make all
make test
streamlit run dashboard/app.py
```

The pipeline creates generated CSVs under `data/` and `outputs/`; those files are ignored so a clean clone remains small. `data/sample/` contains small browsing samples.

## Dashboard preview

![Readiness summary](dashboard/screenshots/01_readiness_summary.png)

![Financial tie-out](dashboard/screenshots/02_financial_tieout.png)

![Defect drill-down](dashboard/screenshots/03_defect_drilldown.png)

The GIF and MP4 in [`demo/`](demo/) are a short visual walkthrough of the generated dashboard views. The Power BI build notes and DAX measures are in [`docs/POWERBI_BUILD_STEPS.md`](docs/POWERBI_BUILD_STEPS.md) and [`dashboard/dax_measures.md`](dashboard/dax_measures.md).

## What I learned

- Reconciliation needs both row-level checks and aggregate controls: a system can have the right row count while balances still fail to tie out.
- Date parsing should be explicit at system boundaries; comparing formatted strings hides conversion errors.
- Remediation needs an audit trail and a second run. A lower defect count is not evidence of correctness unless the same checks are applied again.
- Configuring acceptance thresholds separately from code makes the review easier to explain and change.

## Limitations and next steps

The data is synthetic, SQLite replaces an enterprise database, and the thresholds are illustrative. The remediation step represents a controlled exercise rather than a production change process. A production implementation would add source-file manifests, immutable run IDs, approvals for financial corrections, row-level audit history, database-scale execution, and monitoring for new loads.

## Author

Markus Tsui
