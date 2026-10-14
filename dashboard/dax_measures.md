# Power BI measures

Import the CSVs from `outputs/powerbi_data/` after running `make all`. The data is synthetic and intended to demonstrate a migration-readiness method.

```DAX
Legacy Loans = COUNTROWS(legacy)
Failure Count = SUM(scorecard_before_after[failures])
Failure % = DIVIDE([Failure Count], [Legacy Loans])
Check Status =
VAR failures = MAX(scorecard_before_after[failure_pct])
VAR threshold = MAX(scorecard_before_after[threshold_pct])
RETURN IF(failures <= threshold, "PASS", "FAIL")
Balance Gap = SUM(control_totals[gap])
Material Variance $ =
CALCULATE(SUM(balance_variance[variance]), balance_variance[severity] = "MATERIAL")
Customers Affected = SUM(scorecard_before_after[customers_affected])
Readiness Verdict =
IF(CALCULATE(COUNTROWS(scorecard_before_after),
    scorecard_before_after[status] = "FAIL") = 0, "GO", "NO-GO")
```

Use a single accent colour and reserve red/green for status. Page headlines should state the takeaway rather than merely naming the chart.
