---
name: job-scraper
description: Run a fresh job scrape, enhance, filter, and score. Automatically continues to /job-apply if actionable roles are found.
version: 1.1.0
---

# Job Scraper

**Purpose:** Run a complete fresh scrape pipeline — scrape → enhance → filter → score. No questions asked.

**Invocation:** User types `/job-scraper`

---

## CLI Flags (for reference / ad-hoc use)

```bash
python job_hunter.py              # Normal run with built-in AI scoring, opens job_report.html
python job_hunter.py --no-ai      # Scrape only, outputs jobs_for_review.csv (used by this skill)
python job_hunter.py --no-cache   # Ignore seen_jobs.json cache, rescore everything
python job_hunter.py --min-score 55  # Lower score threshold
```

---

## Cache Management

`seen_jobs.json` — prevents re-showing same jobs, tracks first-seen dates.

**Reset when:** 30+ days old, significantly changing search terms, or changing candidate profile focus.
```bash
rm seen_jobs.json
```

---

## Behavior

**Just run it. No asking.** Execute all steps sequentially and report results at the end.

---

## Steps

### 1. Scrape
```bash
cd <path-to-job-hunter>
python job_hunter.py --no-ai
```
- Takes 5-10 minutes
- Run in background, wait for completion
- Report: total scraped, new vs duplicates filtered

### 2. Enhance
```bash
python enhance_job_data.py
```
- Adds deduplication hashes
- Report: jobs_enhanced.csv created

### 3. Filter
```bash
python filter_promising_jobs.py
```
- Broad filter — do NOT tighten it
- Report: how many passed filter

### 4. Score all filtered jobs

Read `candidate_profile.md`, then for each job in `promising_jobs_v2.txt`:

- Score 0-100 against profile
- Identify key gaps
- Recommend: APPLY / CONSIDER / SKIP

**Phase 2 — Company research (75+ only):**
- Search Indeed/Glassdoor for company rating
- Flag red flags (< 3.0, high turnover, toxic culture)
- Final recommendation: STRONG FIT / CONCERNS / SKIP

### 5. Report results

Present a scored table. Then:

**If any jobs scored 75+:**
- Add to `APPLICATION_TRACKER.md` Discovery Pipeline
- Tell user: "X roles worth reviewing. Use `/job-apply` to create materials."

**If nothing scored 75+:**
- Say so clearly. No further action needed.
- Do NOT suggest running again or ask follow-up questions.

---

## Rules

- ❌ NEVER ask the user what they want to do before scraping — just scrape
- ❌ NEVER present stale results as fresh — check file timestamps if in doubt
- ❌ NEVER skip waiting for the scrape to actually finish
- ✅ Run scrape in background with `run_in_background: true`, then block on TaskOutput
- ✅ After scoring, hand off to `/job-apply` only if there are actionable roles

---

## File Timestamps

Before running, check `jobs_for_review.csv` timestamp. If it's from today, tell the user and ask if they want to re-scrape or use existing results. Otherwise, just run.

```bash
ls -la jobs_for_review.csv
```

---

**Version:** 1.1.0
**Last Updated:** 2026-03-26
