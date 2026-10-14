"""Apply documented deterministic remediation rules to the migrated data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def remediate() -> pd.DataFrame:
    data = ROOT / "data"
    legacy = pd.read_csv(data / "legacy.csv")
    new = pd.read_csv(data / "new_sys.csv")
    mapping = dict(pd.read_csv(data / "status_map.csv").values)
    new = new.drop_duplicates("loan_id", keep="first")
    new = new[new["loan_id"].isin(set(legacy["loan_id"]))]
    missing = legacy[~legacy["loan_id"].isin(set(new["loan_id"]))].copy()
    missing["origination_date"] = pd.to_datetime(missing["origination_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    missing["status"] = missing["status"].map(mapping)
    new = pd.concat([new, missing], ignore_index=True)
    legacy_keyed = legacy.set_index("loan_id")
    new_keyed = new.set_index("loan_id")
    new_keyed["status"] = legacy_keyed["status"].map(mapping)
    new_keyed["interest_rate"] = legacy_keyed["interest_rate"]
    new_keyed["origination_date"] = pd.to_datetime(legacy_keyed["origination_date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    # Balance is restored from the source after confirming the target calculation defect.
    new_keyed["outstanding_balance"] = legacy_keyed["outstanding_balance"]
    result = new_keyed.reset_index()[new.columns]
    result.to_csv(data / "new_loans_after.csv", index=False)
    return result


if __name__ == "__main__":
    remediate()
