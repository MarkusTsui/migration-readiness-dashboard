"""Validate source and target extracts before reconciliation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLUMNS = {
    "loan_id", "customer_id", "product", "region", "origination_date",
    "principal", "interest_rate", "status", "outstanding_balance",
}


def validate_frame(frame: pd.DataFrame, system: str) -> list[str]:
    """Return validation errors for one source-system extract."""
    errors: list[str] = []
    missing = REQUIRED_COLUMNS.difference(frame.columns)
    if missing:
        errors.append(f"{system}: missing columns: {sorted(missing)}")
    if "loan_id" in frame and frame["loan_id"].isna().any():
        errors.append(f"{system}: loan_id contains nulls")
    if "principal" in frame and (frame["principal"] < 0).any():
        errors.append(f"{system}: principal contains negative values")
    if "outstanding_balance" in frame and (frame["outstanding_balance"] < 0).any():
        errors.append(f"{system}: outstanding_balance contains negative values")
    if system == "legacy" and "loan_id" in frame and not frame["loan_id"].is_unique:
        errors.append("legacy: loan_id is not unique")
    return errors


def validate_files(data_dir: Path = ROOT / "data") -> None:
    """Raise ValueError when a required extract violates a source contract."""
    errors: list[str] = []
    for name in ("legacy", "new_sys"):
        path = data_dir / f"{name}.csv"
        if not path.exists():
            errors.append(f"missing file: {path}")
            continue
        errors.extend(validate_frame(pd.read_csv(path), name))
    if errors:
        raise ValueError("Data contract failed:\n- " + "\n- ".join(errors))


if __name__ == "__main__":
    validate_files()
