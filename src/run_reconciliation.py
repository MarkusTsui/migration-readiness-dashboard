"""Run named SQL reconciliation checks and export dashboard-ready CSVs."""

from __future__ import annotations

import argparse
import logging
import re
import sqlite3
from pathlib import Path

import pandas as pd

from src.validate_data import validate_files

ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger(__name__)


def load_queries(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^-- name: ", text)[1:]
    return {block.splitlines()[0].strip(): block.split("\n", 1)[1].strip() for block in blocks}


def run(stage: str = "before") -> dict[str, pd.DataFrame]:
    data_dir = ROOT / "data"
    output_dir = ROOT / "outputs" / "powerbi_data"
    output_dir.mkdir(parents=True, exist_ok=True)
    if stage == "before":
        validate_files(data_dir)
    new_name = "new_sys.csv" if stage == "before" else "new_loans_after.csv"
    conn = sqlite3.connect(":memory:")
    for name in ("legacy", "status_map"):
        pd.read_csv(data_dir / f"{name}.csv").to_sql(name, conn, index=False, if_exists="replace")
    pd.read_csv(data_dir / new_name).to_sql("new_sys", conn, index=False, if_exists="replace")
    results: dict[str, pd.DataFrame] = {}
    for name, sql in load_queries(ROOT / "sql" / "reconciliation.sql").items():
        frame = pd.read_sql_query(sql, conn)
        results[name] = frame
        frame.to_csv(output_dir / f"{stage}_{name}.csv", index=False)
        LOGGER.info("%s: %d rows", name, len(frame))
    results["stage"] = pd.DataFrame({"stage": [stage]})
    conn.close()
    return results


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["before", "after"], default="before")
    args = parser.parse_args()
    run(args.stage)


if __name__ == "__main__":
    main()
