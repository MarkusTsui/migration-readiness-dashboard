# Insights memo

## Recommendation

Run `make all` and use the generated `outputs/powerbi_data/scorecard_before_after.csv` as the source for the current GO/NO-GO recommendation. The initial run is designed to show a NO-GO caused by injected migration defects; the remediated run should be reviewed for any residual risk before cutover.

## Findings

The exact failure counts, percentages, dollar impacts, and affected customers are intentionally read from the generated scorecard rather than written by hand. This prevents stale or fabricated numbers in a public portfolio artifact.

## Root-cause hypotheses

The injected defects model batch-load filtering, non-idempotent retries, test records in a production extract, rounding-rule differences, accrual logic differences, incomplete status mapping, null field mapping, and date conversion shifts.

## Recommended owners and next steps

Data Engineering owns reload, de-duplication, orphan removal, mapping, and field restoration. Finance signs off on material balance corrections and control-total gaps. Operations validates customer impact. The migration PM repeats the checks and records the final decision.
