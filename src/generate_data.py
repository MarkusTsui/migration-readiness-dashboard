"""Generate deterministic synthetic legacy and migrated loan data."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_LOANS = 50_000
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def _date_strings(dates: pd.Series, fmt: str) -> pd.Series:
    return dates.dt.strftime(fmt)


def generate_data(seed: int = SEED, n_loans: int = N_LOANS) -> dict[str, pd.DataFrame]:
    """Return deterministic legacy, new-system, status-map, and defect-log tables."""
    rng = np.random.default_rng(seed)
    loan_ids = np.array([f"L{i:06d}" for i in range(1, n_loans + 1)])
    products = rng.choice(["Personal", "Auto", "Mortgage", "LOC"], n_loans, p=[.30, .25, .25, .20])
    regions = rng.choice(["GTA", "East", "West", "North", "Atlantic"], n_loans, p=[.40, .15, .20, .10, .15])
    dates = pd.Series(pd.Timestamp("2015-01-01") + pd.to_timedelta(rng.integers(0, 3650, n_loans), unit="D"))
    principal = np.round(rng.gamma(shape=2.2, scale=18_000, size=n_loans) + 1_000, 2)
    rates = np.round(np.clip(rng.normal(6.5, 1.8, n_loans), 2, 14), 4)
    statuses = rng.choice(["A", "D", "C", "W"], n_loans, p=[.60, .20, .15, .05])
    ratios = rng.uniform(.05, 1.00, n_loans)
    balances = np.round(principal * ratios, 2)
    balances[np.isin(statuses, ["C", "W"])] = 0
    legacy = pd.DataFrame({
        "loan_id": loan_ids,
        "customer_id": [f"C{i:06d}" for i in rng.integers(1, n_loans * 0.92, n_loans)],
        "product": products,
        "region": regions,
        "origination_date": _date_strings(dates, "%d/%m/%Y"),
        "principal": principal,
        "interest_rate": rates,
        "status": statuses,
        "outstanding_balance": balances,
    })
    mapping = {"A": "ACTIVE", "D": "DELINQUENT", "C": "CLOSED", "W": "WRITTEN_OFF"}
    new = legacy.assign(
        origination_date=_date_strings(dates, "%Y-%m-%d"),
        status=pd.Series(statuses).map(mapping).to_numpy(),
    )

    defect_rows: list[dict[str, object]] = []
    def choose(rate: float) -> np.ndarray:
        return rng.choice(n_loans, size=max(1, round(n_loans * rate)), replace=False)

    # Defects are injected in a stable order so the answer key is reproducible.
    missing = choose(.008)
    new = new.drop(index=missing).reset_index(drop=True)
    defect_rows.extend({"loan_id": loan_ids[i], "defect_type": "missing_in_new"} for i in missing)

    duplicate = rng.choice(new.index.to_numpy(), size=max(1, round(n_loans * .005)), replace=False)
    duplicate_ids = new.loc[duplicate, "loan_id"].to_numpy()
    new = pd.concat([new, new.loc[duplicate]], ignore_index=True)
    defect_rows.extend({"loan_id": loan_id, "defect_type": "duplicate_in_new"} for loan_id in duplicate_ids)

    orphan_ids = np.array([f"LX{i:05d}" for i in range(1, max(2, round(n_loans * .003)) + 1)])
    orphan = new.iloc[: len(orphan_ids)].copy()
    orphan["loan_id"] = orphan_ids
    orphan["customer_id"] = [f"CX{i:05d}" for i in range(1, len(orphan_ids) + 1)]
    new = pd.concat([new, orphan], ignore_index=True)
    defect_rows.extend({"loan_id": x, "defect_type": "orphan_in_new"} for x in orphan_ids)

    rounding = choose(.01)
    rounding_deltas = dict(zip(
        loan_ids[rounding],
        rng.choice([-1, 1], len(rounding)) * rng.uniform(.10, .50, len(rounding)).round(2),
    ))
    rounding_mask = new["loan_id"].isin(rounding_deltas)
    new.loc[rounding_mask, "outstanding_balance"] += new.loc[rounding_mask, "loan_id"].map(rounding_deltas)
    defect_rows.extend({"loan_id": loan_ids[i], "defect_type": "rounding_balance_variance"} for i in rounding)

    material = choose(.005)
    material_multipliers = dict(zip(loan_ids[material], rng.uniform(1.05, 1.40, len(material))))
    material_mask = new["loan_id"].isin(material_multipliers)
    new.loc[material_mask, "outstanding_balance"] *= new.loc[material_mask, "loan_id"].map(material_multipliers)
    new.loc[material_mask, "outstanding_balance"] = new.loc[material_mask, "outstanding_balance"].round(2)
    defect_rows.extend({"loan_id": loan_ids[i], "defect_type": "material_balance_variance"} for i in material)

    status_bad = choose(.007)
    flipped = {"ACTIVE": "DELINQUENT", "DELINQUENT": "ACTIVE", "CLOSED": "WRITTEN_OFF", "WRITTEN_OFF": "CLOSED"}
    bad_status = {
        loan_id: flipped[mapping[legacy.loc[i, "status"]]]
        for i, loan_id in zip(status_bad, loan_ids[status_bad])
    }
    new["status"] = new["loan_id"].map(bad_status).fillna(new["status"])
    defect_rows.extend({"loan_id": loan_ids[i], "defect_type": "wrong_status_mapping"} for i in status_bad)

    null_rate = choose(.004)
    new.loc[new["loan_id"].isin(loan_ids[null_rate]), "interest_rate"] = np.nan
    defect_rows.extend({"loan_id": loan_ids[i], "defect_type": "null_interest_rate"} for i in null_rate)

    date_shift = choose(.003)
    shifts = rng.integers(1, 41, len(date_shift))
    for loan_id, shift in zip(loan_ids[date_shift], shifts):
        idx = new.index[new["loan_id"].eq(loan_id)]
        new.loc[idx, "origination_date"] = (pd.to_datetime(new.loc[idx, "origination_date"]) + pd.Timedelta(days=int(shift))).dt.strftime("%Y-%m-%d")
    defect_rows.extend({"loan_id": loan_ids[i], "defect_type": "date_shift"} for i in date_shift)

    defect_log = pd.DataFrame(defect_rows).drop_duplicates(["loan_id", "defect_type"]).sort_values(["defect_type", "loan_id"])
    return {"legacy": legacy, "new_sys": new, "status_map": pd.DataFrame(mapping.items(), columns=["legacy_status", "new_status"]), "defect_log": defect_log}


def main() -> None:
    tables = generate_data()
    DATA_DIR.mkdir(exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(DATA_DIR / f"{name}.csv", index=False)
    sample_dir = DATA_DIR / "sample"
    sample_dir.mkdir(exist_ok=True)
    for name, frame in tables.items():
        frame.head(200).to_csv(sample_dir / f"{name}.csv", index=False)


if __name__ == "__main__":
    main()
