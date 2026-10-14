-- Each query is portable SQLite SQL and is executed by src/run_reconciliation.py.

-- name: 01_row_counts
-- Detects batch truncation or unexpected load volume changes.
SELECT 'legacy' AS system, COUNT(*) AS rows, COUNT(DISTINCT loan_id) AS distinct_ids FROM legacy
UNION ALL
SELECT 'new_sys', COUNT(*), COUNT(DISTINCT loan_id) FROM new_sys;

-- name: 02_missing_in_new
-- An anti-join detects loans that were not loaded into the target system.
SELECT l.* FROM legacy l
LEFT JOIN new_sys n ON n.loan_id = l.loan_id
WHERE n.loan_id IS NULL;

-- name: 03_orphans_in_new
-- Target-only records may be test data or an incorrectly scoped source extract.
SELECT n.* FROM new_sys n
LEFT JOIN legacy l ON l.loan_id = n.loan_id
WHERE l.loan_id IS NULL;

-- name: 04_duplicates_in_new
-- Duplicate keys indicate a non-idempotent retry or replayed source file.
SELECT loan_id, COUNT(*) AS duplicate_count FROM new_sys
GROUP BY loan_id HAVING COUNT(*) > 1;

-- name: 05_balance_variance
-- Balance differences expose calculation, rounding, or accrual-rule mismatches.
WITH deduped AS (
  SELECT * FROM (
    SELECT n.*, ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY rowid) AS rn FROM new_sys n
  ) WHERE rn = 1
)
SELECT l.loan_id, l.product, l.region, l.outstanding_balance AS legacy_balance,
       d.outstanding_balance AS new_balance,
       ROUND(d.outstanding_balance - l.outstanding_balance, 2) AS variance,
       CASE WHEN ABS(d.outstanding_balance - l.outstanding_balance) > 1.00
            THEN 'MATERIAL' ELSE 'ROUNDING' END AS severity
FROM legacy l JOIN deduped d ON d.loan_id = l.loan_id
WHERE ABS(d.outstanding_balance - l.outstanding_balance) > 0.00;

-- name: 06_status_mismatch
-- The mapping check catches semantically wrong status translations.
SELECT l.loan_id, l.status AS legacy_status, n.status AS new_status
FROM legacy l JOIN new_sys n ON n.loan_id = l.loan_id
JOIN status_map m ON m.legacy_status = l.status
WHERE n.status <> m.new_status;

-- name: 07_null_and_date_checks
-- Explicit date parsing catches format shifts and null field mappings.
SELECT l.loan_id, l.interest_rate AS legacy_interest_rate, n.interest_rate AS new_interest_rate,
       l.origination_date AS legacy_date, n.origination_date AS new_date,
       CASE WHEN n.interest_rate IS NULL THEN 'NULL_INTEREST_RATE'
            WHEN date(substr(l.origination_date, 7, 4) || '-' ||
                      substr(l.origination_date, 4, 2) || '-' ||
                      substr(l.origination_date, 1, 2)) <> date(n.origination_date)
                 THEN 'DATE_MISMATCH' END AS defect_type
FROM legacy l JOIN new_sys n ON n.loan_id = l.loan_id
WHERE n.interest_rate IS NULL
   OR date(substr(l.origination_date, 7, 4) || '-' ||
           substr(l.origination_date, 4, 2) || '-' ||
           substr(l.origination_date, 1, 2)) <> date(n.origination_date);

-- name: 08_control_totals
-- Product-level control totals catch financially material aggregate gaps.
WITH deduped AS (
  SELECT * FROM (
    SELECT n.*, ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY rowid) AS rn FROM new_sys n
  ) WHERE rn = 1
)
SELECT l.product, ROUND(SUM(l.outstanding_balance), 2) AS legacy_total,
       ROUND(COALESCE(SUM(d.outstanding_balance), 0), 2) AS new_total,
       ROUND(COALESCE(SUM(d.outstanding_balance), 0) - SUM(l.outstanding_balance), 2) AS gap
FROM legacy l LEFT JOIN deduped d ON d.loan_id = l.loan_id
GROUP BY l.product ORDER BY l.product;
