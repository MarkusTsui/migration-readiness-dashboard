# Copilot instructions for this repository

This repo is a data-analyst portfolio project: validating a simulated loan-system migration (SQL + Python), with a Power BI dashboard, a presentation, and a demo video. Owner: Markus Tsui, applying for a New Grad Data Analyst role.

**Source of truth:** `docs/BUILD_SPEC.md`. Read it before any task and follow its phase order, file structure and acceptance rules.

## Non-negotiable rules
- Never invent numbers. Every figure in docs, slides, scripts and resume bullets must be read from generated outputs (`outputs/`).
- The data is synthetic. State this in every public-facing document.
- Do not claim skills or experience the owner has not confirmed. Ask when unsure.
- Keep the project reproducible: seed 42, pinned `requirements.txt`, `make all` runs everything.
- Never commit secrets, personal data, or large raw data files.

## Code conventions
- Python 3.11+, type hints on public functions, short docstrings, `pandas` + `sqlite3`.
- SQL: lowercase table names, one named query per `-- name: xx_description` block, a comment above each query explaining the migration risk it covers.
- Keep SQL portable (SQLite now, SQL Server/PostgreSQL later); note dialect differences in `docs/SQL_PORTING_NOTES.md`.
- Every check has a unit test in `tests/` proving it catches its injected defect.
- Small commits, one per phase: `phase N: <summary>`.

## Writing style
- Plain language for non-technical readers; lead with the answer, then the method.
- Headlines state takeaways, not topics.
- Be honest about limits and residual risk.

## Things you cannot do (use fallbacks)
- You cannot run Power BI Desktop or record the screen. Provide DAX in `dashboard/dax_measures.md`, click-by-click steps in `docs/POWERBI_BUILD_STEPS.md`, and a Streamlit fallback. The owner records the demo video; you write `demo/demo_script.md`.
- Personal reflections in `docs/LESSONS_LEARNED.md` come from the owner. Keep `docs/BUILD_LOG.md` of real obstacles and interview the owner at the end.
