"""Build before/after readiness scorecards from exported reconciliation results."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config" / "thresholds.json").read_text(encoding="utf-8"))


def _score(stage: str) -> pd.DataFrame:
    out = ROOT / "outputs" / "powerbi_data"
    counts = len(pd.read_csv(ROOT / "data" / "legacy.csv"))
    missing = len(pd.read_csv(out / f"{stage}_02_missing_in_new.csv"))
    orphan = len(pd.read_csv(out / f"{stage}_03_orphans_in_new.csv"))
    dup = len(pd.read_csv(out / f"{stage}_04_duplicates_in_new.csv"))
    balance = pd.read_csv(out / f"{stage}_05_balance_variance.csv")
    status = len(pd.read_csv(out / f"{stage}_06_status_mismatch.csv"))
    null_date = pd.read_csv(out / f"{stage}_07_null_and_date_checks.csv")
    control = pd.read_csv(out / f"{stage}_08_control_totals.csv")
    failed_products = int((control["gap"].abs() > CONFIG["control_total_gap"]).sum())
    checks = [
        ("Missing loans", missing, CONFIG["checks"]["missing_loans"], 0.0),
        ("Orphan loans", orphan, CONFIG["checks"]["orphan_loans"], 0.0),
        ("Duplicate loan IDs", dup, CONFIG["checks"]["duplicate_loan_ids"], 0.0),
        ("Balance variance", len(balance), CONFIG["checks"]["balance_variance"], balance["variance"].abs().sum() if len(balance) else 0),
        ("Status mismatch", status, CONFIG["checks"]["status_mismatch"], 0.0),
        ("Null/date defects", len(null_date), CONFIG["checks"]["null_date_defects"], 0.0),
        ("Control-total gap", failed_products, CONFIG["checks"]["control_total_gap"], control["gap"].abs().sum()),
    ]
    rows = []
    for check, failures, threshold, dollar in checks:
        pct = failures / counts * 100
        rows.append({"stage": stage, "check": check, "failures": failures, "failure_pct": round(pct, 4),
                     "threshold_pct": threshold, "status": "PASS" if pct <= threshold else "FAIL",
                     "dollar_impact": round(float(dollar), 2), "customers_affected": failures})
    return pd.DataFrame(rows)


def build_scorecard() -> pd.DataFrame:
    out = ROOT / "outputs" / "powerbi_data"
    before = _score("before")
    after = _score("after")
    score = pd.concat([before, after], ignore_index=True)
    score["verdict"] = score.groupby("stage")["status"].transform(lambda s: "GO" if (s == "PASS").all() else "NO-GO")
    score.to_csv(out / "scorecard_before_after.csv", index=False)
    score[score.stage == "before"].to_csv(out / "scorecard_before.csv", index=False)
    score[score.stage == "after"].to_csv(out / "scorecard_after.csv", index=False)
    return score


if __name__ == "__main__":
    build_scorecard()
