from pathlib import Path

import pandas as pd

from src.generate_data import generate_data
from src.run_reconciliation import run


def test_generator_is_deterministic():
    first = generate_data()
    second = generate_data()
    for name in first:
        pd.testing.assert_frame_equal(first[name], second[name])


def test_each_injected_defect_is_represented():
    defects = generate_data()["defect_log"]
    expected = {
        "missing_in_new", "duplicate_in_new", "orphan_in_new",
        "rounding_balance_variance", "material_balance_variance",
        "wrong_status_mapping", "null_interest_rate", "date_shift",
    }
    assert expected == set(defects["defect_type"])


def test_legacy_keys_are_unique():
    legacy = generate_data()["legacy"]
    assert legacy["loan_id"].is_unique


def test_data_size_and_defect_log_are_reproducible():
    tables = generate_data()
    assert len(tables["legacy"]) == 50_000
    assert not tables["defect_log"].empty
    assert Path(__file__).exists()


def test_reconciliation_checks_find_each_defect_family():
    tables = generate_data()
    data_dir = Path(__file__).resolve().parents[1] / "data"
    data_dir.mkdir(exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(data_dir / f"{name}.csv", index=False)
    results = run("before")
    assert len(results["02_missing_in_new"]) > 0
    assert len(results["03_orphans_in_new"]) > 0
    assert len(results["04_duplicates_in_new"]) > 0
    assert len(results["05_balance_variance"]) > 0
    assert len(results["06_status_mismatch"]) > 0
    assert len(results["07_null_and_date_checks"]) > 0
    assert len(results["08_control_totals"]) > 0
