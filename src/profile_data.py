"""Create a compact, reproducible profile of the generated extracts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def profile(frame: pd.DataFrame, system: str) -> pd.DataFrame:
    """Return row counts, null rates, and distinct counts by column."""
    rows = []
    for column in frame.columns:
        rows.append({
            "system": system,
            "column": column,
            "rows": len(frame),
            "null_count": int(frame[column].isna().sum()),
            "null_pct": round(float(frame[column].isna().mean() * 100), 4),
            "distinct_count": int(frame[column].nunique(dropna=True)),
        })
    return pd.DataFrame(rows)


def build_profile(data_dir: Path = ROOT / "data", output_dir: Path = ROOT / "outputs") -> pd.DataFrame:
    """Write a column profile and a human-readable HTML report."""
    frames = [
        profile(pd.read_csv(data_dir / "legacy.csv"), "legacy"),
        profile(pd.read_csv(data_dir / "new_sys.csv"), "new_sys"),
    ]
    result = pd.concat(frames, ignore_index=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_dir / "data_profile.csv", index=False)
    result.to_html(output_dir / "data_profile.html", index=False, border=0)
    return result


if __name__ == "__main__":
    build_profile()
