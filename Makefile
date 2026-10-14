PYTHON ?= python

.PHONY: data recon remediate retest report all test clean

data:
	$(PYTHON) src/generate_data.py

recon: data
	$(PYTHON) src/run_reconciliation.py --stage before

remediate: recon
	$(PYTHON) src/remediate.py

retest: remediate
	$(PYTHON) src/run_reconciliation.py --stage after

report: retest
	$(PYTHON) src/scorecard.py
	$(PYTHON) src/make_charts.py

all: report

test:
	$(PYTHON) -m pytest -q

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in [Path('outputs'), Path('data')] if p.exists()]; Path('data/sample').mkdir(parents=True, exist_ok=True)"

