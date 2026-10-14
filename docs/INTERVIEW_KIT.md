# Interview kit

## 60-second pitch

I built a synthetic loan-migration validation workflow that answers a practical cutover question: can leadership trust the target data? Python generates reproducible source and target extracts, SQLite runs named reconciliation checks, and a scorecard ranks defects by operational and financial impact. A remediation step applies documented fixes and the checks run again. The project demonstrates the method honestly; its data is synthetic and the final metrics come from generated outputs.

## STAR story

**Situation:** a migration needs evidence before go-live. **Task:** provide a defensible decision. **Action:** define thresholds, reconcile records and balances, quantify defects, document fixes, and re-test. **Result:** the scorecard gives a repeatable GO/NO-GO outcome and makes residual risk visible.

## Questions to prepare

- Why synthetic data, and what limitations remain?
- How would stakeholders set thresholds in production?
- How would you scale the checks to 50 million rows?
- What can row reconciliation miss if both systems are wrong in the same way?
- How do you explain a NO-GO to an executive?
