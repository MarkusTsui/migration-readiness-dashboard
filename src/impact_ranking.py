"""Export the highest-impact defects for review and remediation planning."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def build_impact_outputs(
    input_dir: Path = ROOT / "outputs" / "powerbi_data",
    output_dir: Path = ROOT / "outputs" / "powerbi_data",
) -> None:
    """Write top balance variances and a product/region defect summary."""
    variance = pd.read_csv(input_dir / "before_05_balance_variance.csv")
    variance.assign(abs_variance=variance["variance"].abs()).sort_values(
        "abs_variance", ascending=False
    ).head(10).to_csv(output_dir / "top_balance_variances.csv", index=False)

    detail = variance.assign(defect_type=variance["severity"].str.lower() + "_balance_variance")
    summary = (
        detail.groupby(["product", "region", "defect_type"], as_index=False)
        .agg(defect_count=("loan_id", "count"), dollar_impact=("variance", lambda values: values.abs().sum()))
        .sort_values(["dollar_impact", "defect_count"], ascending=False)
    )
    summary.to_csv(output_dir / "defect_summary_by_product_region.csv", index=False)


if __name__ == "__main__":
    build_impact_outputs()
