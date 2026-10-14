"""Streamlit fallback dashboard for environments without Power BI Desktop."""

from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "powerbi_data"

st.set_page_config(page_title="Migration readiness", layout="wide")
st.title("Can we trust the migrated data?")
st.caption("Synthetic loan migration data; run `make all` before opening this dashboard.")

score_path = DATA / "scorecard_before_after.csv"
if not score_path.exists():
    st.error("No outputs found. Run `make all` from the repository root.")
    st.stop()

score = pd.read_csv(score_path)
before, after = score[score.stage == "before"], score[score.stage == "after"]
st.header("Remediation changes the cutover decision")
cols = st.columns(2)
for col, frame, label in zip(cols, (before, after), ("Before remediation", "After remediation")):
    verdict = frame["verdict"].iloc[0]
    col.metric(label, verdict, f"{(frame.status == 'PASS').sum()}/{len(frame)} checks pass")
st.bar_chart(score.pivot(index="check", columns="stage", values="failures"))

st.header("Check detail")
st.dataframe(score, use_container_width=True)

control = DATA / "before_08_control_totals.csv"
if control.exists():
    st.header("Financial control totals")
    st.dataframe(pd.read_csv(control), use_container_width=True)
