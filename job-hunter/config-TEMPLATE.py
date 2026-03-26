"""
Job Hunter Configuration Template

Copy this file to config.py and customize with your search parameters.
"""

import os

CONFIG = {
    # Your Anthropic API key (only needed if running standalone without Claude Code)
    # If using Claude Code with paid plan, leave this empty - skills run in your session
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),

    # ── Search Terms ─────────────────────────────────────────────────────────
    # Organize by priority tiers — start broad, add specific domain terms
    # Tip: append "remote" to remote-first terms; omit for local searches
    "search_terms": [
        # ===== TIER 1: Dream Roles =====
        "YOUR ROLE TITLE remote",           # e.g., "IT Director remote"
        "Director of YOUR FIELD remote",    # e.g., "Director of Engineering remote"
        "VP YOUR FIELD remote",             # e.g., "VP Engineering remote"

        # ===== TIER 2: Senior Management + Domain Focus =====
        "Senior YOUR ROLE Manager remote",  # e.g., "Senior IT Manager remote"
        "YOUR DOMAIN Manager remote",       # e.g., "Cloud Infrastructure Manager remote"

        # ===== TIER 3: Domain Specialist Roles =====
        "YOUR ROLE YOUR TECH remote",       # e.g., "IT Manager Azure M365 remote"
        # Add 5-15 total search term variations for best coverage
    ],

    # ── Remote Search (Pass 1) ───────────────────────────────────────────────
    "location": "United States",    # Country/region for remote search
    "distance_miles": 50,           # Ignored for remote roles
    "results_per_search": 20,       # Results per site per search term
    "hours_old": 72,                # Only jobs posted in last N hours

    # ── Local/Hybrid Search (Pass 2) ─────────────────────────────────────────
    # Set local_search_enabled to True if you're open to hybrid/on-site roles.
    # Populate commutable_areas with cities/towns within reasonable commute distance.
    # Leave commutable_areas empty [] to only consider remote roles.
    "local_search_enabled": False,
    "commutable_areas": [
        # "Your City, ST",          # e.g., "Cambridge, MA"
        # "Nearby Town, ST",        # e.g., "Somerville, MA"
        # Add all towns within your commute radius
    ],
    "local_distance_miles": 15,     # Tight radius per town for Pass 2

    # ── Job Boards ───────────────────────────────────────────────────────────
    # Indeed and Google Jobs are reliable. ZipRecruiter has active Cloudflare blocking.
    "sites": ["indeed", "google"],

    # ── AI Scoring ───────────────────────────────────────────────────────────
    # Only roles scoring >= this threshold appear in the HTML report
    "min_score": 65,

    # ── Resume ───────────────────────────────────────────────────────────────
    "resume_file": "resume.txt",    # Path relative to this script

    # ── Output ───────────────────────────────────────────────────────────────
    "output_file": "job_report.html",
    "seen_jobs_file": "seen_jobs.json",   # Tracks jobs already shown

    # ── Filtering Criteria (used by filter_promising_jobs.py) ────────────────
    "min_salary": 100000,           # Minimum acceptable salary (e.g., 100000 = $100k)

    "target_titles": [              # Job titles to include — customize for your level
        "director", "manager", "head", "vp",
        "senior manager", "lead"
    ],

    "it_subspecialties": [          # Domain keywords that match your expertise
        "engineering", "platform", "systems",
        "operations", "technology", "infrastructure",
        "security", "cloud", "data"
    ],

    "negative_keywords": [          # Roles to exclude — customize to avoid irrelevant matches
        "intern", "junior", "associate", "helpdesk", "service desk"
    ],
}
