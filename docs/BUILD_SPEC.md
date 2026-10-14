# BUILD SPEC: Migration Readiness Project (Reconciliation, Data Quality Scorecard & KPI Dashboard)

> **Purpose of this file:** the complete build spec, stored at `docs/BUILD_SPEC.md`. GitHub Copilot (agent mode)
> uses it to build the whole project from an empty repo, prepare the demo script and presentation,
> and produce a polished public GitHub repo. The public `README.md` is written last (Phase 8) and replaces the placeholder. The human owner is **Markus Tsui**, applying for the CGI New Grad Data Analyst role (Toronto, Position ID J0926-1947).

---

## 0. Instructions for GitHub Copilot (read first)

You are GitHub Copilot working in **agent mode** inside this repository. Build the project below phase by phase.
Persistent rules also live in `.github/copilot-instructions.md`; reusable phase prompts live in `.github/prompts/`.

**How to work**
1. Do **one phase per chat session**. Start by restating the phase goal and listing the files you will create or change.
2. After each phase run the verification step, fix failures, then commit with the message `phase N: <summary>`.
3. At each **HUMAN CHECKPOINT** (marked below), stop, summarise what you did, and ask the owner to review before continuing.
4. If a requirement is unclear, make the smallest reasonable assumption, write it in `docs/ASSUMPTIONS.md`, and keep going. Do not ask more than one question at a time.

**What Copilot does vs what the owner does**
| Copilot builds | Owner (Markus) does personally |
|---|---|
| Data generator, SQL, Python pipeline, tests, Makefile | Reviews every phase and runs `make all` locally |
| Remediation and before/after scorecard | Builds/saves the Power BI `.pbix` (Copilot writes the DAX and click-by-click steps) |
| Charts, Streamlit fallback dashboard, Excel workbook | Takes the dashboard screenshots |
| Insights memo, slide deck (python-pptx or Marp), demo script | Records the demo video with his own voice (Copilot cannot record a screen) |
| Draft README, interview kit, LinkedIn post draft | Writes the real reflections for `LESSONS_LEARNED.md`, pins the repo, posts on LinkedIn |

**Rules**
1. **Never fabricate results.** Every number in the README, slides, memo, video script and resume bullets must come from an actual run. Read numbers from the generated CSVs.
2. **The data is synthetic.** Say so plainly in the README, slides and video. The project shows an approach, not production results.
3. **Never claim skills or experience the owner has not confirmed** (see Section 2). If something needs a personal reflection (Phase 7), ask the owner; do not invent it.
4. **Reproducibility:** fixed random seed, pinned `requirements.txt`, one command to run everything (`make all`).
5. Write for a non-technical reader first: every artifact opens with the business question and the answer before the method.
6. You cannot run Power BI Desktop (Windows only) or record video. Use the fallbacks stated in Phases 4 and 6 and write exact manual steps for the owner.

**Seed code:** the `seed/` folder contains a working first version (`generate_data.py`, `reconciliation.sql`, `run_reconciliation.py`) that already runs end to end. In Phases 1-2, **move and extend it** into `src/` and `sql/` per Section 5 (add `defect_log.csv`, impact columns, tests) instead of rewriting from scratch. Delete `seed/` when migrated.

**HUMAN CHECKPOINTS:** after Phase 1 (data looks realistic), after Phase 3 (before/after story makes sense), after Phase 4 (dashboard), after Phase 6 (slides/script), and before Phase 8 (final README).

**Definition of done:** the checklist in Section 14 is fully ticked.

---

## 1. Project story (the one-paragraph pitch)

A lender is migrating 50,000 loans from a legacy servicing system to a new platform. Leadership must decide: **GO or NO-GO for cutover?**
This project validates the migrated data with SQL and Python, quantifies the financial and customer impact of every defect, publishes a readiness scorecard and Power BI dashboard, recommends fixes, **applies remediation, re-tests, and shows the defect rate drop** until the data passes the agreed acceptance rules.

**Why this is the right project for the role:** the CGI posting asks for data validation, reconciliation, readiness assessments, system migration support, KPI dashboards, SQL, Power BI/Tableau, and clear communication to technical and non-technical audiences. This project demonstrates each one in a single, easy-to-explain story.

**What should inspire the interviewer:** it is not "I made charts". It is "I treated data like a risk to be managed: I defined acceptance criteria with stakeholders, built automated checks, found and prioritized defects by dollar impact, proposed fixes, re-tested, and gave a clear go/no-go recommendation."

---

## 2. Owner context and positioning (use for tone, README "About", and interview kit)

Confirmed facts only (do not add to this list without asking the owner):

- Postgraduate Certificate, Applied A.I. Solutions Development, George Brown College (completed 2025, GPA 3.93/4.0); B.Eng. (Hons) Electronic & Communication Engineering, City University of Hong Kong (completed 2023).
- Python (advanced), SQL (advanced), R, Tableau, Power BI, SQL Server/SSMS/SSAS, Dataiku DSS, Teradata, Git, Linux, Docker.
- Real hands-on Power BI dashboard experience (KPIs, filters, multiple data sources) from a coursework project.
- Built a Python pipeline that extracts vendor PDF price lists and exports Excel formatted for Shopify/Amazon at Smith's Pharmacy (real data-cleaning and format-conversion experience, directly relevant to migration work).
- Small Business Credit Predictive Analytics: AutoML pipeline in Dataiku DSS/Teradata, 200+ features, 0.87 AUC (a financial-services analytics project).
- Kinectrics AI Solutions Development co-op (Jun-Aug 2025): AI/data pipelines, evaluation of RAG systems (RAGAS/UQLM), CAD extraction pipeline.
- Currently works in catering operations in Toronto (fast-paced, multi-priority environment, up to 300-guest events), which supports the "manage multiple priorities" requirement. Frame it honestly as operations experience, not data experience.
- Not yet worked professionally in the AI/data industry. **Frame this project as how he proves job-ready skills as a new grad.**

**Positioning line for README/LinkedIn:**
"New-grad data analyst who treats data as a risk to manage: validate, reconcile, quantify impact, recommend fixes, and prove the fix works."

---

## 3. Job requirement to evidence map (include in the final README)

| CGI requirement | Evidence in this project | Where |
|---|---|---|
| Data analysis, trends, problem solving | Defect pattern analysis by product/region/severity, root-cause hypotheses | `docs/INSIGHTS_MEMO.md`, dashboard page 3 |
| SQL, Excel/macros | 8+ reconciliation queries; Excel reconciliation workbook with a macro-free formula version and optional VBA | `sql/`, `excel/` |
| Power BI / Tableau | 3-page Power BI dashboard with DAX measures; optional Tableau page | `dashboard/` |
| Data validation, reconciliation, QA | Automated checks, thresholds, PASS/FAIL scorecard, re-test | `src/`, `sql/` |
| Stakeholder management and communication | Business brief, one-page insights memo, 5-minute presentation, demo video | `docs/`, `presentation/`, `demo/` |
| Multiple priorities, fast-paced | Defects ranked by dollar and customer impact; remediation order | memo + dashboard |
| Transformation / migration projects (asset) | The whole scenario: readiness assessment, cutover recommendation, re-test | whole repo |
| Financial systems (asset) | Loan balances, control totals, status codes, interest rates | data spec |
| Python, statistical analysis, ML (listed skills) | Python pipeline; optional anomaly detection on balance variances | `src/`, optional Phase 4b |

---

## 4. Tech stack

- Python 3.11+, `pandas`, `numpy`, `sqlite3` (standard library), `matplotlib`, `pytest`
- SQL (SQLite dialect, written so it ports easily to SQL Server/PostgreSQL; note differences in `docs/SQL_PORTING_NOTES.md`)
- Power BI Desktop (primary dashboard); fallback: a Streamlit or static-HTML dashboard replicating all 3 pages, plus the manual build steps
- Presentation: PowerPoint (`python-pptx`) or Marp/Markdown to PDF
- Video: screen recording by the owner (preferred), or an AI-assembled video from slide images + dashboard screenshots + narration (`moviepy`/`ffmpeg`, any TTS)
- Git/GitHub, `Makefile`

---

## 5. Repository structure (create exactly this)

```
migration-readiness/
├── README.md                  # final public README (written in Phase 8, see Section 11)
├── .github/copilot-instructions.md
├── .github/prompts/*.prompt.md
├── Makefile                   # make data | recon | remediate | retest | report | all | test
├── requirements.txt
├── .gitignore
├── data/                      # generated CSVs (gitignored except small samples)
│   └── sample/                # 200-row samples committed for browsing
├── src/
│   ├── generate_data.py       # Phase 1
│   ├── run_reconciliation.py  # Phase 2/3
│   ├── remediate.py           # Phase 3b: applies fixes, produces "after" data
│   ├── scorecard.py           # builds before/after scorecard + exports
│   └── make_charts.py         # static PNG charts for README/slides
├── sql/
│   └── reconciliation.sql     # named queries, "-- name: xx" convention
├── outputs/                   # generated: powerbi_data/*.csv, charts/*.png
├── excel/
│   └── reconciliation_workbook.xlsx   # formula-based version of 3 key checks
├── dashboard/
│   ├── migration_readiness.pbix       # (owner builds/saves; AI provides steps if it cannot)
│   ├── dax_measures.md
│   └── screenshots/*.png
├── presentation/
│   ├── migration_readiness.pptx
│   └── migration_readiness.pdf
├── demo/
│   ├── demo_script.md         # timed narration
│   ├── demo.mp4               # final video (or link in README if > 100 MB)
│   └── demo.gif               # 20-30 s preview embedded in README
├── docs/
│   ├── BUSINESS_BRIEF.md
│   ├── INSIGHTS_MEMO.md       # one page for non-technical stakeholders
│   ├── DATA_DICTIONARY.md
│   ├── POWERBI_BUILD_STEPS.md
│   ├── LESSONS_LEARNED.md     # Phase 7, filled with the owner's real reflections
│   ├── INTERVIEW_KIT.md       # Section 12
│   ├── BUILD_SPEC.md          # this file
│   └── ASSUMPTIONS.md
└── tests/
    └── test_checks.py         # unit tests proving each check catches its injected defect
```

---

## 6. Business brief (write to `docs/BUSINESS_BRIEF.md`)

- **Context:** 50,000 loans migrating from a legacy servicing system to a new platform.
- **Stakeholders:** Operations lead (customer impact), Finance (balances must tie out), Migration PM (go/no-go), Data Engineering (fixes).
- **Business question:** is the migrated data accurate and complete enough to go live?
- **Decision:** GO / NO-GO plus a prioritized remediation list.
- **KPIs:** record completeness %, duplicate rate %, balance tie-out ($ gap by product), status-mapping accuracy %, field-level quality (null rate, date accuracy %).
- **Acceptance rule (agreed with stakeholders):** each check must fail on no more than **0.1%** of legacy records, and the total control-total gap per product must be within **$1,000**. Any single loan with balance variance over **$1.00** is "material".
- **Out of scope:** customer PII handling, performance testing of the new system.

---

## 7. Data specification (Phase 1)

Generate with seed `42`, **50,000** loans. Tables: `legacy`, `new_sys`, `status_map`.

**Columns:** `loan_id` (L000001...), `customer_id`, `product` (Personal 30%, Auto 25%, Mortgage 25%, LOC 20%), `region` (GTA 40%, East 15%, West 20%, North 10%, Atlantic 15%), `origination_date`, `principal` (gamma, right-skewed), `interest_rate` (normal 6.5, sd 1.8, clipped 2-14), `status`, `outstanding_balance` (5-100% of principal; 0 when closed or written off).

**Legacy formats:** dates `DD/MM/YYYY`; status codes `A, D, C, W`.
**New-system formats:** dates `YYYY-MM-DD`; status `ACTIVE, DELINQUENT, CLOSED, WRITTEN_OFF`.

**Injected defects (keep a hidden `defect_log.csv` as the answer key, used only by tests):**

| Defect | Rate | Realistic cause |
|---|---|---|
| Records missing in new system | 0.8% | batch load failure / filter bug |
| Duplicate records in new | 0.5% | retry without idempotency |
| Orphan records only in new | 0.3% | test data left in production load |
| Small balance rounding difference (+/- $0.10-$0.50) | 1.0% | rounding rules differ |
| Material balance difference (5-40% higher) | 0.5% | interest accrual logic differs |
| Wrong status mapping | 0.7% | incomplete mapping table |
| Null interest rate | 0.4% | field not mapped |
| Origination date shifted 1-40 days | 0.3% | timezone/format conversion |

Write `docs/DATA_DICTIONARY.md` documenting every column, format and rule.

**Verification:** counts above are within rounding of the target rates; `legacy` has unique `loan_id`; script is deterministic (two runs give identical files).

---

## 8. Build phases

### Phase 2: SQL reconciliation (`sql/reconciliation.sql`)
Named queries (one CSV output each):
1. `01_row_counts` (rows and distinct IDs per system)
2. `02_missing_in_new` (LEFT JOIN anti-join)
3. `03_orphans_in_new`
4. `04_duplicates_in_new` (GROUP BY ... HAVING COUNT > 1)
5. `05_balance_variance` (severity: MATERIAL if abs > 1.00 else ROUNDING; dedupe `new_sys` first)
6. `06_status_mismatch` (via `status_map`)
7. `07_null_and_date_checks` (convert legacy `DD/MM/YYYY` with `substr` before comparing)
8. `08_control_totals` (legacy vs new balance sums and gap by product)
Add comments explaining *why* each check exists (migration risk it covers).

### Phase 3: Python runner and scorecard
- `run_reconciliation.py` loads CSVs into SQLite, runs each named query, exports to `outputs/powerbi_data/`.
- Scorecard columns: `check, failures, failure_pct, threshold_pct, status (PASS/FAIL), dollar_impact, customers_affected`. Overall verdict: GO only if every check passes.
- Add **impact ranking**: sort defects by dollar impact and by customers affected (a missing $2M mortgage matters more than 300 rounding cents).
- **Phase 3b `remediate.py`:** apply documented fixes (de-duplicate, reload missing loans from legacy, remove orphans after confirming not in legacy, correct status mapping, restore nulls from legacy, correct dates; for material balance variance, flag for manual review and correct from legacy after confirming accrual rule). Save `new_loans_after.csv`.
- Re-run all checks on the "after" data. Produce a **before/after scorecard**. Expected outcome: most checks pass; keep 1-2 items intentionally "residual risk" (e.g., a small number of unresolved balance cases pending Finance sign-off) so the story is realistic, not magical.

### Phase 4: Dashboard (3 pages, Power BI)
Load the CSVs from `outputs/powerbi_data/`. Relationships: product and region dimension tables, `loan_id` where useful.
- **Page 1 Readiness summary:** overall GO/NO-GO card (before and after), a card per check with PASS/FAIL colour, defect counts, before/after bar chart.
- **Page 2 Financial tie-out:** control totals by product (legacy vs new vs gap), variance distribution (histogram), material vs rounding split, top 10 largest variances table.
- **Page 3 Defect drill-down:** slicers (product, region, severity, defect type), defect volume by region/product matrix, table for the remediation team with loan IDs.
Write `dashboard/dax_measures.md` with at least: `Legacy Loans`, `Failure Count`, `Failure %`, `Check Status` (SWITCH on threshold), `Balance Gap`, `Material Variance $`, `Customers Affected`, `Readiness Verdict`.
Design rules: one accent colour plus red/green for status only; every page title states the takeaway ("Mortgage carries 60% of the balance gap"), not just the topic; consistent fonts; no pie charts with more than 4 slices.
**Fallback if Power BI cannot be run:** build the same 3 pages in Streamlit, and write `docs/POWERBI_BUILD_STEPS.md` with click-by-click instructions and the DAX so the owner can reproduce it in Power BI Desktop and save the `.pbix`.

### Phase 4b (optional, adds ML/statistics): anomaly detection
Use z-score or isolation forest on balance variance and balance-to-principal ratio to flag suspicious records *not* caught by the rule checks. Report precision/recall against the hidden `defect_log.csv`. Keep it to one page; explain it in plain language.

### Phase 5: Insights memo (`docs/INSIGHTS_MEMO.md`, max one page)
Structure: **Recommendation (GO/NO-GO + conditions)** → **Top 3 findings with numbers** → **Root-cause hypotheses** → **Recommended fixes, owners, and dates** → **Residual risks** → **Next steps**. Plain language, no jargon, every number sourced from the scorecard.

### Phase 6: Presentation and demo video (see Section 9 for details)

### Phase 7: Lessons learned (see Section 10)

### Phase 8: GitHub polish (see Section 11)

---

## 9. Presentation and demo video (Phase 6)

### 9.1 Presentation (7-8 slides, `presentation/migration_readiness.pptx` + PDF)
1. **Title + one-line answer:** "Can we trust the migrated data? Not yet, here's what to fix, and the re-test proving it."
2. **The business problem and decision** (stakeholders, GO/NO-GO).
3. **Approach:** diagram of legacy + new → SQL checks → scorecard → dashboard → remediation → re-test.
4. **Findings (before):** scorecard with the biggest dollar and customer impacts.
5. **Dashboard walkthrough:** 2-3 screenshots with callouts.
6. **Remediation and re-test:** before/after chart; residual risk.
7. **Recommendation + next steps.**
8. **What I learned** (3 honest lessons from `docs/LESSONS_LEARNED.md`) and a contact slide.
Rules: one message per slide, headline = takeaway, max ~25 words of body text, charts from `outputs/charts/` (generated by `make_charts.py`), speaker notes with the narration.

### 9.2 Demo video (target 3 minutes, max 4)
**Preferred (best impression): the owner records their own screen and voice** following `demo/demo_script.md`. A real voice reads as authentic and is what interviewers remember. The AI's job is to write the script, prepare the recording environment, and make the recording easy.
**Fallback (AI-assembled):** render slides and dashboard screenshots to images, generate narration with TTS, assemble with `moviepy`/`ffmpeg`, burn in captions. Label it "narrated with a text-to-speech voice" in the README.

**Timed script (adjust to real numbers):**
| Time | On screen | Narration idea |
|---|---|---|
| 0:00-0:20 | Title slide | "A lender is migrating 50,000 loans. The question: is the data safe to go live? I built a validation workflow to answer it." |
| 0:20-0:50 | Architecture diagram | Explain inputs, SQL checks, thresholds agreed with stakeholders, Python automation. |
| 0:50-1:30 | Terminal: `make recon`, scorecard output | Show the run finishing and the NO-GO verdict with the top defects. |
| 1:30-2:15 | Power BI dashboard pages 1-3 | Lead with the takeaway; drill into the largest dollar-impact defect. |
| 2:15-2:45 | Before/after scorecard | Show remediation and re-test; state the residual risk honestly. |
| 2:45-3:00 | Closing slide | Recommendation, one lesson learned, call to action (repo link, LinkedIn). |

**Also produce:** a 20-30 second silent `demo.gif` (terminal run to scorecard to dashboard) for the top of the GitHub README, since GitHub does not autoplay mp4 reliably. If `demo.mp4` exceeds 100 MB, host it on YouTube (unlisted) or GitHub Releases and link it.
**Quality gates for the video:** clear audio, 1080p, readable text at 100% zoom, no secrets or personal data on screen, no unexplained jargon in the first 60 seconds, ends with the recommendation.

---

## 10. Lessons learned (Phase 7, `docs/LESSONS_LEARNED.md`)

This is the section that convinces an interviewer you learn and reflect. **The AI must not invent it.** Instead:
1. During the build, keep a running `docs/BUILD_LOG.md` of real obstacles hit (errors, wrong assumptions, rework) and what fixed them.
2. At the end, interview the owner with the questions below, and write the answers in his own voice, tightened for clarity.
3. Use this structure:
   - **What I set out to do and why**
   - **3 things that surprised me or went wrong** (each: what happened, how I found it, what I changed)
   - **What I would do differently** (e.g., agree acceptance thresholds first, add idempotent load checks, profile data before writing rules)
   - **Skills I strengthened** (specific, e.g., anti-joins, handling date formats across systems, DAX measures, communicating NO-GO)
   - **How this connects to my past work** (e.g., my PDF-to-Excel pipeline taught me format conversion pitfalls; my Power BI coursework taught me dashboard design)
   - **What I'd explore next** (e.g., orchestration with Airflow, data quality frameworks like Great Expectations, dbt tests)

**Interview questions for the owner:** What was the hardest bug? What did you assume that turned out wrong? Which check found the most important defect and why? What did you learn about explaining a NO-GO to non-technical people? What would you add with more time?

---

## 11. Final GitHub README structure (what the public repo README should look like)

1. Title and one-line value statement; demo GIF directly under it; badges (Python, SQL, Power BI).
2. **The question and the answer** (3-4 lines, with the real before/after numbers).
3. Link to the demo video and the presentation PDF.
4. **Dashboard screenshots** (3 images).
5. **How it works** (architecture diagram + the check table).
6. **Key findings** and recommendation (from the memo).
7. **Quickstart:** `pip install -r requirements.txt && make all`.
8. **What I learned** (short version, link to `LESSONS_LEARNED.md`).
9. **Limitations:** synthetic data with injected defects; SQLite instead of an enterprise database; thresholds are illustrative.
10. **About me** and contact (name: Markus (Wai Ho) Tsui; email waiho0311@gmail.com; linkedin.com/in/markustsui).
**Repo hygiene:** meaningful commit history (one commit per phase), no large raw data, topics set (`data-analysis`, `sql`, `power-bi`, `data-quality`, `data-migration`), repo pinned on the GitHub profile.

---

## 12. Interview kit (`docs/INTERVIEW_KIT.md`)

**60-second pitch:** problem, approach, outcome (with real numbers), what I learned.

**STAR story (use real numbers):**
- Situation: a migration with no proof the data was safe.
- Task: give leadership a go/no-go with evidence.
- Action: defined acceptance criteria, wrote SQL checks, automated them, ranked defects by dollar impact, built a dashboard, proposed fixes, re-tested.
- Result: defect rates from X% to Y%, clear recommendation, residual risk documented.

**Questions to prepare answers for:**
- Why is this data synthetic, and how does that limit the project? (Honest answer: it demonstrates method; real data adds messier edge cases, access constraints, and stakeholder negotiation.)
- How did you decide the thresholds? How would you set them with real stakeholders?
- How do you prioritize 6 defect types when time is limited? (Dollar impact, customer impact, fix effort, regulatory risk.)
- How would this scale to 50 million rows? (Move checks to the database, hash-based row comparison, partitioned reconciliation, sampling for field-level checks.)
- What's the difference between reconciliation and validation?
- How would you explain a NO-GO to a non-technical executive?
- Where could your checks miss a problem? (Consistent wrong values in both systems, logic errors invisible to row comparison.)
- Connect to experience: format conversion pipeline (PDF to Excel), Power BI dashboards, credit analytics, handling many priorities in a busy operations job.

**Resume bullets (fill X, Y with real numbers):**
- Built an automated migration validation workflow (Python, SQL) reconciling 50K loan records across two systems; detected missing, duplicate, orphan and mismatched records and produced a PASS/FAIL readiness scorecard.
- Quantified $X of material balance variance across Y loans, ranked defects by financial and customer impact, and recommended remediation that reduced the failure rate from X% to Y% on re-test.
- Designed a 3-page Power BI dashboard (KPIs, control totals, defect drill-down) and a 3-minute walkthrough video to support a go/no-go recommendation for non-technical stakeholders.

---

## 13. Testing and quality

- `tests/test_checks.py`: for each injected defect type, assert the matching check finds it (compare with `defect_log.csv`); assert the remediated data passes the expected checks; assert the pipeline is deterministic.
- Run `make test` before every commit; CI optional (GitHub Actions running `pytest`).
- Reconcile the dashboard to the CSVs: spot-check three numbers by hand.
- Lint SQL and Python formatting (`ruff`/`black`) if available.

---

## 14. Final checklist (definition of done)

- [ ] `make all` runs from a clean clone and reproduces every output
- [ ] All numbers in README, slides, memo and script match the generated CSVs
- [ ] Scorecard shows before (NO-GO) and after (improved, residual risk stated)
- [ ] Dashboard has 3 pages with takeaway titles; `.pbix` saved (or build steps + Streamlit fallback delivered)
- [ ] Insights memo is one page and readable by a non-technical person
- [ ] Presentation PDF and PPTX done; speaker notes included
- [ ] Demo video (about 3 min) and 20-30 s GIF done; README embeds the GIF and links the video
- [ ] `LESSONS_LEARNED.md` written from the owner's real reflections
- [ ] Interview kit complete with real numbers
- [ ] README states the data is synthetic and lists limitations
- [ ] No personal data, secrets or large files committed
- [ ] Repo topics, description, pinned on GitHub profile; LinkedIn post drafted linking the repo
