"""Create small static charts used by the memo and presentation."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    out = ROOT / "outputs" / "charts"
    out.mkdir(parents=True, exist_ok=True)
    score = pd.read_csv(ROOT / "outputs" / "powerbi_data" / "scorecard_before_after.csv")
    pivot = score.pivot(index="check", columns="stage", values="failures")
    ax = pivot.plot(kind="bar", figsize=(10, 5), color=["#d95f02", "#1b9e77"])
    ax.set_title("Remediation reduces migration check failures")
    ax.set_ylabel("Failing records or groups")
    ax.set_xlabel("")
    plt.tight_layout()
    plt.savefig(out / "before_after_failures.png", dpi=150)
    plt.close()


if __name__ == "__main__":
    main()
