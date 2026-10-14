# Business brief

**Question:** Is the migrated loan data accurate and complete enough to go live?

A lender is moving 50,000 synthetic loans from a legacy servicing system to a new platform. Operations needs customer-impact visibility, Finance needs balances to tie out, the migration PM needs a go/no-go decision, and Data Engineering needs an ordered fix list.

The workflow checks completeness, duplicates, orphans, balance variances, status mappings, null rates, date accuracy, and product-level control totals. A check fails when more than 0.1% of legacy records fail; each product's control-total gap must remain within $1,000. A single balance variance above $1.00 is material.

Customer PII and target-system performance testing are out of scope.
