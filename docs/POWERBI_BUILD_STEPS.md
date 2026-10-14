# Power BI build steps

Power BI Desktop is not available in this environment. The Streamlit fallback is `dashboard/app.py`; the following steps reproduce the intended three-page report.

1. Run `make all`.
2. Open Power BI Desktop and select **Get data > Text/CSV**.
3. Import the CSVs under `outputs/powerbi_data/`: `scorecard_before_after.csv`, `before_05_balance_variance.csv`, `before_08_control_totals.csv`, and their `after_` counterparts.
4. Create a `stage` slicer and a `check` table on page 1. Add the measures in `dashboard/dax_measures.md`.
5. Page 1 title: **"Remediation changes the cutover decision"**. Add before/after verdict cards, check status cards, and a clustered bar chart of failures.
6. Page 2 title: **"Control totals show where financial risk sits"**. Add product totals, a variance histogram, severity split, and a top-10 variance table.
7. Page 3 title: **"The remediation queue is specific and actionable"**. Add product, region, severity, and defect-type slicers plus a loan-level table.
8. Save the file as `dashboard/migration_readiness.pbix` and capture three screenshots in `dashboard/screenshots/`.
