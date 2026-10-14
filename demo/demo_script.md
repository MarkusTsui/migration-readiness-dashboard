# Demo script

Use the generated scorecard and dashboard outputs from `make all` when recording the walkthrough.

**0:00-0:20 — Title:** A lender is migrating 50,000 synthetic loans. The question is whether the data is safe to go live.

**0:20-0:50 — Method:** Show legacy and target extracts flowing through named SQL checks, a Python scorecard, remediation, and re-test. Explain that the thresholds are illustrative.

**0:50-1:30 — Before:** Run `make recon` and show the generated scorecard. Call out the highest-impact defect using the actual dollar and customer figures from the CSV.

**1:30-2:15 — Dashboard:** Walk through readiness, financial tie-out, and the remediation queue. Lead with each page's takeaway.

**2:15-2:45 — After:** Run the remediation and re-test. Show the before/after chart and state any residual risk honestly.

**2:45-3:00 — Close:** State the recommendation, limitations of synthetic data, and the repository link.
