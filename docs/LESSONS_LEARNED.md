# Lessons learned

## 1. Row counts are not enough

A migration can preserve the overall number of rows while still containing duplicate keys, orphans, missing loans, and incorrect field values. The project therefore combines anti-joins, duplicate checks, field comparisons, and product-level controls.

## 2. Financial checks need two views

The balance check reports both individual variances and aggregate product gaps. This separates a large individual error from many small rounding differences and gives Finance a control-total view.

## 3. Remediation must be re-tested

The corrected file is not treated as proof. The same SQL checks run against the `after` extract, and the scorecard records both stages so the change in decision is visible.

## 4. The next useful improvements

A production version would add run IDs, source-file checksums, an exception workflow, approval history, and database-native execution for larger volumes.
