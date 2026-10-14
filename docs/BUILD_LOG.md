# Build log

## Reproducibility

The pipeline uses NumPy seed `42` and writes generated data and reports to ignored directories. Running `make all` from a clean checkout rebuilds the same source extracts, reconciliation results, scorecard, charts, and demo assets.

## Decisions recorded during implementation

- Source extracts are checked before they enter SQLite so missing columns, null keys, negative amounts, and duplicate legacy keys fail early.
- Reconciliation SQL is split into named queries so each migration risk has an independently inspectable output.
- Acceptance thresholds live in `config/thresholds.json`; changing a business rule does not require editing the scoring algorithm.
- Remediation is followed by a separate `after` reconciliation run rather than treating the corrected file as proof of success.
- Generated raw files are ignored, while small samples remain committed for repository browsing.
