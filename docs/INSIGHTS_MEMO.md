# Insights memo

## Recommendation

The generated before-remediation scorecard is **NO-GO** because multiple completeness, consistency, and financial checks fail. The remediated extract is **GO** for this synthetic test because all configured checks pass on the independent re-test.

## Findings

- Completeness issues are visible through missing, orphan, and duplicate loan IDs.
- Balance reconciliation is the highest-risk check because it converts record-level differences into a financial control total.
- Status, date, and interest-rate checks catch defects that would not be visible from row counts alone.

The exact counts, percentages, and dollar totals are exported to `outputs/powerbi_data/scorecard_before_after.csv` after `make all`.

## Root-cause hypotheses

The injected defects represent common migration failure modes: incomplete batch loads, non-idempotent retries, test data in a target extract, rounding-rule differences, accrual-rule differences, incomplete mappings, and field conversion errors.

## Production follow-up

Data Engineering would own the reload and mapping corrections. Finance would approve material balance changes. Operations would review customer-impacting defects. The migration lead would retain the run ID, source-file manifest, exception list, approvals, and final cutover decision.
