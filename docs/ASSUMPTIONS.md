# Project assumptions

- All records are synthetic and contain no customer-identifying information.
- The legacy extract is the reference for key, status, date, and balance corrections.
- A production remediation would require Finance approval for material balance changes and an immutable audit record.
- The acceptance thresholds in `config/thresholds.json` are illustrative and should be agreed with business owners before a real cutover.
