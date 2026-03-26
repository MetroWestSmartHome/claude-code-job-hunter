#!/usr/bin/env python3
"""
Job Hunter - AI-powered job scraper and resume matcher
Scrapes Indeed, Google Jobs, ZipRecruiter and uses Claude to score matches
against your resume and preferences.
"""

import os
import json
import time
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

import anthropic
from jobspy import scrape_jobs

# Import configuration from external files
from config import CONFIG

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
# Configuration moved to config.py - edit that file to customize search parameters
# Candidate profile moved to candidate_profile.md - edit that file to update preferences

# Load candidate profile from markdown file
CANDIDATE_PROFILE = Path("candidate_profile.md").read_text(encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────────
# CORE LOGIC
# ─────────────────────────────────────────────────────────────────────────────

def load_resume(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return "[Resume not loaded — place resume.txt next to job_hunter.py]"
    return p.read_text(encoding="utf-8")


def load_seen_jobs(path: str) -> set:
    p = Path(path)
    if p.exists():
        try:
            return set(json.loads(p.read_text()))
        except Exception:
            return set()
    return set()


def save_seen_jobs(path: str, seen: set):
    Path(path).write_text(json.dumps(list(seen)), encoding="utf-8")


def job_fingerprint(job) -> str:
    key = f"{job.get('title','')}{job.get('company','')}{job.get('location','')}"
    return hashlib.md5(key.encode()).hexdigest()


def scrape_all_jobs(config: dict) -> list[dict]:
    all_jobs = []
    seen_fingerprints = set()

    # ── Pass 1: Remote jobs (nationwide) ────────────────────────────────────
    print("  [Pass 1: Remote nationwide]")
    for term in config["search_terms"]:
        print(f"    Searching: '{term}'...")
        try:
            results = scrape_jobs(
                site_name=config["sites"],
                search_term=term,
                location=config["location"],
                distance=config["distance_miles"],
                is_remote=True,
                results_wanted=config["results_per_search"],
                hours_old=config["hours_old"],
                description_format="markdown",
                linkedin_fetch_description=False,
            )

            for _, row in results.iterrows():
                job = row.to_dict()
                fp = job_fingerprint(job)
                if fp not in seen_fingerprints:
                    seen_fingerprints.add(fp)
                    job["_fingerprint"] = fp
                    all_jobs.append(job)

            print(f"      Found {len(results)} results")
            time.sleep(3)  # be polite between searches

        except Exception as e:
            print(f"      Error scraping '{term}': {e}")

    # ── Pass 2: Local/hybrid jobs in commutable areas ────────────────────────
    # Set local_search_enabled: True and populate commutable_areas in config.py
    # to search for hybrid/on-site roles near you in addition to remote roles.
    if config.get("local_search_enabled") and config.get("commutable_areas"):
        print(f"\n  [Pass 2: Local/hybrid in commutable areas]")
        # Use a focused subset of search terms for local — leadership titles only
        leadership_keywords = config.get("target_titles", ["director", "manager", "head", "vp"])
        local_terms = [t for t in config["search_terms"]
                       if any(k in t.lower() for k in leadership_keywords)]
        for location in config["commutable_areas"]:
            for term in local_terms:
                # Strip "remote" from term for local search
                local_term = term.replace(" remote", "").replace("remote ", "")
                print(f"    Searching: '{local_term}' near {location}...")
                try:
                    results = scrape_jobs(
                        site_name=config["sites"],
                        search_term=local_term,
                        location=location,
                        distance=config.get("local_distance_miles", 15),
                        is_remote=False,
                        results_wanted=10,  # smaller batch per town
                        hours_old=config["hours_old"],
                        description_format="markdown",
                        linkedin_fetch_description=False,
                    )

                    new_count = 0
                    for _, row in results.iterrows():
                        job = row.to_dict()
                        fp = job_fingerprint(job)
                        if fp not in seen_fingerprints:
                            seen_fingerprints.add(fp)
                            job["_fingerprint"] = fp
                            all_jobs.append(job)
                            new_count += 1

                    if new_count > 0:
                        print(f"      Found {new_count} new results (of {len(results)})")
                    time.sleep(2)

                except Exception as e:
                    print(f"      Error scraping '{local_term}' near {location}: {e}")

    print(f"\n  Total unique jobs found: {len(all_jobs)}")
    return all_jobs


def score_job_with_claude(client: anthropic.Anthropic, job: dict, resume: str) -> dict:
    """Ask Claude to score the job against resume and preferences."""

    title = job.get("title", "Unknown")
    company = job.get("company", "Unknown")
    location = job.get("location", "Unknown")
    description = str(job.get("description", ""))[:4000]  # cap to avoid token bloat
    salary_min = job.get("min_amount", "")
    salary_max = job.get("max_amount", "")
    salary_str = f"${salary_min}–${salary_max}" if salary_min and salary_max else "Not listed"
    job_type = job.get("job_type", "")
    is_remote = job.get("is_remote", "")

    prompt = f"""You are helping an IT professional evaluate job postings against their resume and preferences.

## CANDIDATE PROFILE & PREFERENCES
{CANDIDATE_PROFILE}

## CANDIDATE'S RESUME
{resume}

## JOB POSTING
Title: {title}
Company: {company}
Location: {location}
Remote: {is_remote}
Job Type: {job_type}
Salary: {salary_str}

Description:
{description}

## TASK
Evaluate this job posting and respond ONLY with valid JSON (no markdown, no explanation outside the JSON):

{{
  "score": <integer 0-100>,
  "recommendation": "<STRONG MATCH | GOOD MATCH | WEAK MATCH | SKIP>",
  "headline": "<one sentence summary of why this is or isn't a fit>",
  "pros": ["<pro 1>", "<pro 2>", "<pro 3>"],
  "cons": ["<con 1>", "<con 2>"],
  "salary_fit": "<good | unknown | low | high>",
  "remote_status": "<fully remote | hybrid | on-site | unclear>",
  "seniority_fit": "<good | over-qualified | under-qualified | unclear>",
  "red_flags": ["<flag if any, else empty list>"]
}}

Score guidelines:
- 85-100: Near-perfect match, strong apply signal
- 70-84: Good match, worth applying
- 55-69: Partial match, apply if job hunting actively
- 40-54: Weak match, significant gaps
- 0-39: Skip
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        # Strip any accidental markdown fences
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        return {
            "score": 0,
            "recommendation": "ERROR",
            "headline": f"Scoring failed: {e}",
            "pros": [],
            "cons": [],
            "salary_fit": "unknown",
            "remote_status": "unclear",
            "seniority_fit": "unclear",
            "red_flags": []
        }


# ─────────────────────────────────────────────────────────────────────────────
# HTML REPORT GENERATION
# ─────────────────────────────────────────────────────────────────────────────

def score_color(score: int) -> str:
    if score >= 85: return "#22c55e"
    if score >= 70: return "#84cc16"
    if score >= 55: return "#f59e0b"
    return "#ef4444"


def recommendation_badge(rec: str) -> str:
    colors = {
        "STRONG MATCH": ("bg-green", "#dcfce7", "#166534"),
        "GOOD MATCH":   ("bg-lime",  "#ecfccb", "#3f6212"),
        "WEAK MATCH":   ("bg-amber", "#fef3c7", "#92400e"),
        "SKIP":         ("bg-red",   "#fee2e2", "#991b1b"),
        "ERROR":        ("bg-gray",  "#f3f4f6", "#374151"),
    }
    bg, text = colors.get(rec, colors["ERROR"])[1], colors.get(rec, colors["ERROR"])[2]
    return f'<span style="background:{bg};color:{text};padding:2px 10px;border-radius:99px;font-size:0.75rem;font-weight:600;">{rec}</span>'


def generate_html_report(scored_jobs: list[dict], config: dict) -> str:
    now = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    total = len(scored_jobs)

    # Stats
    strong = sum(1 for j in scored_jobs if j["ai"]["recommendation"] == "STRONG MATCH")
    good   = sum(1 for j in scored_jobs if j["ai"]["recommendation"] == "GOOD MATCH")

    cards = ""
    for job in scored_jobs:
        ai = job["ai"]
        score = ai.get("score", 0)
        color = score_color(score)
        badge = recommendation_badge(ai.get("recommendation", ""))
        title = job.get("title", "Unknown Title")
        company = job.get("company", "Unknown Company")
        location = job.get("location", "")
        salary_min = job.get("min_amount", "")
        salary_max = job.get("max_amount", "")
        salary_str = f"${int(salary_min):,}–${int(salary_max):,}/yr" if salary_min and salary_max else "Salary not listed"
        url = job.get("job_url", "#")
        site = str(job.get("site", "")).capitalize()
        posted = str(job.get("date_posted", ""))
        remote_status = ai.get("remote_status", "unclear")
        seniority = ai.get("seniority_fit", "unclear")

        pros_html = "".join(f'<li>✓ {p}</li>' for p in ai.get("pros", []))
        cons_html = "".join(f'<li>✗ {c}</li>' for c in ai.get("cons", []))
        flags_html = ""
        if ai.get("red_flags"):
            flags = "".join(f'<li>⚠ {f}</li>' for f in ai["red_flags"])
            flags_html = f'<div class="red-flags"><ul>{flags}</ul></div>'

        cards += f"""
        <div class="card">
            <div class="card-header">
                <div class="score-ring" style="border-color:{color};">
                    <span style="color:{color};">{score}</span>
                </div>
                <div class="card-title-block">
                    <h2><a href="{url}" target="_blank">{title}</a></h2>
                    <div class="meta">
                        <span class="company">{company}</span>
                        {f'<span class="sep">·</span><span>{location}</span>' if location else ''}
                        <span class="sep">·</span><span class="site-tag">{site}</span>
                        {f'<span class="sep">·</span><span class="posted">Posted {posted}</span>' if posted else ''}
                    </div>
                    <div class="badges">
                        {badge}
                        <span class="info-badge">💰 {salary_str}</span>
                        <span class="info-badge">🌐 {remote_status.title()}</span>
                        <span class="info-badge">📊 Seniority: {seniority.title()}</span>
                    </div>
                </div>
            </div>
            <div class="headline">"{ai.get('headline','')}"</div>
            <div class="pros-cons">
                <div class="pros"><ul>{pros_html}</ul></div>
                <div class="cons"><ul>{cons_html}</ul></div>
            </div>
            {flags_html}
            <div class="card-footer">
                <a href="{url}" target="_blank" class="apply-btn">View Job →</a>
                <span class="salary-fit">Salary fit: {ai.get('salary_fit','unknown')}</span>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Job Hunt Report — {now}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         background: #0f172a; color: #e2e8f0; min-height: 100vh; }}
  .header {{ background: #1e293b; border-bottom: 1px solid #334155;
             padding: 24px 32px; display: flex; justify-content: space-between; align-items: center; }}
  .header h1 {{ font-size: 1.5rem; font-weight: 700; color: #f8fafc; }}
  .header h1 span {{ color: #60a5fa; }}
  .run-info {{ font-size: 0.8rem; color: #94a3b8; }}
  .stats {{ background: #1e293b; padding: 16px 32px; display: flex; gap: 32px;
            border-bottom: 1px solid #334155; }}
  .stat {{ display: flex; flex-direction: column; }}
  .stat .num {{ font-size: 1.5rem; font-weight: 700; color: #f8fafc; }}
  .stat .label {{ font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }}
  .container {{ max-width: 900px; margin: 32px auto; padding: 0 24px; }}
  .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px;
           padding: 24px; margin-bottom: 20px; transition: border-color 0.2s; }}
  .card:hover {{ border-color: #60a5fa; }}
  .card-header {{ display: flex; gap: 20px; align-items: flex-start; margin-bottom: 12px; }}
  .score-ring {{ width: 64px; height: 64px; border-radius: 50%; border: 3px solid;
                 display: flex; align-items: center; justify-content: center;
                 flex-shrink: 0; }}
  .score-ring span {{ font-size: 1.25rem; font-weight: 800; }}
  .card-title-block {{ flex: 1; }}
  .card-title-block h2 {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; }}
  .card-title-block h2 a {{ color: #f8fafc; text-decoration: none; }}
  .card-title-block h2 a:hover {{ color: #60a5fa; }}
  .meta {{ font-size: 0.8rem; color: #94a3b8; display: flex; flex-wrap: wrap; gap: 6px;
           align-items: center; margin-bottom: 8px; }}
  .company {{ font-weight: 600; color: #cbd5e1; }}
  .sep {{ color: #475569; }}
  .site-tag {{ background: #1d4ed8; color: #bfdbfe; padding: 1px 7px; border-radius: 4px; font-size: 0.7rem; }}
  .posted {{ color: #64748b; }}
  .badges {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .info-badge {{ background: #0f172a; border: 1px solid #334155; color: #94a3b8;
                 padding: 2px 8px; border-radius: 99px; font-size: 0.72rem; }}
  .headline {{ background: #0f172a; border-left: 3px solid #60a5fa; padding: 10px 14px;
               border-radius: 0 6px 6px 0; font-size: 0.875rem; color: #cbd5e1;
               margin: 12px 0; font-style: italic; }}
  .pros-cons {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0; }}
  .pros ul, .cons ul {{ list-style: none; font-size: 0.82rem; }}
  .pros li {{ color: #86efac; padding: 2px 0; }}
  .cons li {{ color: #fca5a5; padding: 2px 0; }}
  .red-flags {{ background: #450a0a; border: 1px solid #7f1d1d; border-radius: 6px;
                padding: 10px 14px; margin: 8px 0; }}
  .red-flags ul {{ list-style: none; font-size: 0.82rem; }}
  .red-flags li {{ color: #fca5a5; }}
  .card-footer {{ display: flex; justify-content: space-between; align-items: center;
                  margin-top: 14px; padding-top: 14px; border-top: 1px solid #334155; }}
  .apply-btn {{ background: #2563eb; color: #fff; padding: 6px 18px; border-radius: 6px;
                text-decoration: none; font-size: 0.85rem; font-weight: 600; }}
  .apply-btn:hover {{ background: #1d4ed8; }}
  .salary-fit {{ font-size: 0.78rem; color: #94a3b8; }}
  .empty {{ text-align: center; color: #64748b; padding: 80px 0; font-size: 1rem; }}
  @media (max-width: 600px) {{ .pros-cons {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>🎯 Job Hunt <span>Report</span></h1>
  <div class="run-info">Generated {now}</div>
</div>
<div class="stats">
  <div class="stat"><span class="num">{total}</span><span class="label">Matches Found</span></div>
  <div class="stat"><span class="num" style="color:#22c55e">{strong}</span><span class="label">Strong Matches</span></div>
  <div class="stat"><span class="num" style="color:#84cc16">{good}</span><span class="label">Good Matches</span></div>
  <div class="stat"><span class="num" style="color:#94a3b8">{config['min_score']}+</span><span class="label">Score Threshold</span></div>
</div>
<div class="container">
  {''.join([cards]) if cards else '<div class="empty">No matches above threshold. Try lowering min_score or expanding search terms.</div>'}
</div>
</body>
</html>"""

    return html


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def export_csv(jobs: list[dict], path: Path):
    """Export scraped jobs to CSV for manual review in Claude Code."""
    import csv
    fields = ["title", "company", "location", "is_remote", "job_type",
              "min_amount", "max_amount", "date_posted", "site", "job_url", "description"]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for job in jobs:
            row = {k: job.get(k, "") for k in fields}
            desc = str(row.get("description", ""))
            row["description"] = desc[:3000] if desc else ""
            writer.writerow(row)

    print(f"  CSV saved: {path} ({len(jobs)} jobs)")


def main():
    parser = argparse.ArgumentParser(description="AI-powered job hunter")
    parser.add_argument("--no-cache", action="store_true", help="Ignore seen-jobs cache")
    parser.add_argument("--min-score", type=int, default=None, help="Override min score threshold")
    parser.add_argument("--dry-run", action="store_true", help="Scrape only, no output")
    parser.add_argument("--no-ai", action="store_true",
                        help="Scrape and dedup only — output CSV for manual review in Claude Code. No API key needed.")
    args = parser.parse_args()

    if args.min_score:
        CONFIG["min_score"] = args.min_score

    api_key = CONFIG["anthropic_api_key"]
    if not api_key and not args.dry_run and not args.no_ai:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable or add it to CONFIG.")
        print("       To scrape without AI scoring, run with --no-ai flag.")
        return

    script_dir = Path(__file__).parent
    resume_path = script_dir / CONFIG["resume_file"]
    seen_path   = script_dir / CONFIG["seen_jobs_file"]
    output_path = script_dir / CONFIG["output_file"]
    csv_path    = script_dir / "jobs_for_review.csv"

    print("=" * 60)
    print("  JOB HUNTER")
    if args.no_ai:
        print("  Mode: Scrape only -> CSV (for Claude Code review)")
    print("=" * 60)

    seen_jobs = load_seen_jobs(str(seen_path)) if not args.no_cache else set()

    # 1. Scrape
    step_total = "2" if args.no_ai else "3"
    print(f"\n[1/{step_total}] Scraping job boards...")
    all_jobs = scrape_all_jobs(CONFIG)

    new_jobs = [j for j in all_jobs if j["_fingerprint"] not in seen_jobs]
    print(f"  New jobs (not seen before): {len(new_jobs)}")

    if not new_jobs:
        print("\nNo new jobs found. Try --no-cache to start fresh.")
        return

    if args.dry_run:
        print(f"\n[DRY RUN] Found {len(new_jobs)} new jobs. Exiting.")
        return

    # --no-ai path: dump CSV and exit
    if args.no_ai:
        print(f"\n[2/2] Exporting to CSV...")
        export_csv(new_jobs, csv_path)
        for job in new_jobs:
            seen_jobs.add(job["_fingerprint"])
        save_seen_jobs(str(seen_path), seen_jobs)
        print(f"\n✓ Done! Feed jobs_for_review.csv to Claude Code for scoring.")
        print(f"  Use the prompt in CLAUDE_CODE_PROMPT.md")
        print("=" * 60)
        return

    # Standard AI scoring path
    resume = load_resume(str(resume_path))
    if "[Resume not loaded" in resume:
        print(f"\n⚠  Resume not found at {resume_path}")
        print("   Add resume.txt for better scoring.\n")

    print(f"\n[2/3] Scoring {len(new_jobs)} jobs with Claude...")
    client = anthropic.Anthropic(api_key=api_key)

    scored = []
    for i, job in enumerate(new_jobs, 1):
        title = job.get("title", "?")
        company = job.get("company", "?")
        print(f"  [{i}/{len(new_jobs)}] {title} @ {company}", end="", flush=True)

        ai_result = score_job_with_claude(client, job, resume)
        score = ai_result.get("score", 0)
        print(f" -> {score}/100 ({ai_result.get('recommendation','')})")

        seen_jobs.add(job["_fingerprint"])

        if score >= CONFIG["min_score"]:
            job["ai"] = ai_result
            scored.append(job)

        time.sleep(0.5)

    scored.sort(key=lambda x: x["ai"].get("score", 0), reverse=True)
    save_seen_jobs(str(seen_path), seen_jobs)

    print(f"\n  Jobs above threshold ({CONFIG['min_score']}+): {len(scored)}")

    print(f"\n[3/3] Generating HTML report...")
    html = generate_html_report(scored, CONFIG)
    output_path.write_text(html, encoding="utf-8")
    print(f"  Report saved: {output_path}")
    print(f"\n✓ Done! Open {output_path} in your browser.")
    print("=" * 60)


if __name__ == "__main__":
    main()
