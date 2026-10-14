PYTHON ?= python

.PHONY: data validate profile recon remediate retest report all test clean

data:
	$(PYTHON) -m src.generate_data

validate: data
	$(PYTHON) -m src.validate_data

profile: validate
	$(PYTHON) -m src.profile_data

recon: profile
	$(PYTHON) -m src.run_reconciliation --stage before

remediate: recon
	$(PYTHON) -m src.remediate

retest: remediate
	$(PYTHON) -m src.run_reconciliation --stage after

report: retest
	$(PYTHON) -m src.scorecard
	$(PYTHON) -m src.impact_ranking
	$(PYTHON) -m src.make_charts
	$(PYTHON) -m src.make_demo_assets

all: report

test:
	$(PYTHON) -m pytest -q

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p) for p in [Path('outputs'), Path('data')] if p.exists()]; Path('data/sample').mkdir(parents=True, exist_ok=True)"
