"""
Job Hunter Configuration Template

Copy this file to config.py and customize with your search parameters.
"""

import os

CONFIG = {
    # Your Anthropic API key (only needed if running standalone without Claude Code)
    # If using Claude Code with paid plan, leave this empty - skills run in your session
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),

    # Search parameters
    # Customize these search terms for your target roles
    "search_terms": [
        "YOUR JOB TITLE 1 remote",      # e.g., "Software Engineering Manager remote"
        "YOUR JOB TITLE 2 remote",      # e.g., "Director of Engineering remote"
        "YOUR JOB TITLE 3 remote",      # e.g., "VP Engineering remote"
        # Add 5-10 search term variations
    ],

    "location": "Boston, MA",              # Your city/region for proximity-based searches
    "distance_miles": 50,                  # Commute radius (0 for remote-only)
    "results_per_search": 20,              # Results per site per search term
    "hours_old": 72,                       # Only jobs posted in last N hours
    "remote_only": True,                   # Set to False if open to on-site/hybrid

    # Job boards (Indeed and Google Jobs are reliable)
    "sites": ["indeed", "google"],

    # AI scoring threshold (only roles scoring >= this appear in report)
    "min_score": 65,

    # Resume file path (relative to this script)
    "resume_file": "resume.txt",

    # Filtering criteria (used by filter_promising_jobs.py)
    "min_salary": 123456,  # Minimum acceptable salary (e.g., $123,456)

    # Commutable areas for hybrid/on-site roles (optional)
    # List cities/towns you're willing to commute to for exceptional opportunities
    # Leave empty [] to only consider remote roles
    # Example for Boston suburbs: ["cambridge", "somerville", "brookline", "newton", "waltham"]
    "commutable_areas": [],

    # Leadership titles to filter for (customize to your target level)
    "target_titles": [
        "director", "manager", "head", "vp",
        "senior manager", "lead"
    ],

    # Domain keywords that match your expertise
    # Customize for your field (examples: 'devops', 'data', 'cloud', 'security', 'infrastructure')
    "it_subspecialties": [
        "engineering", "platform", "systems",
        "operations", "technology"
    ],

    # Keywords to exclude (roles you want to avoid)
    "negative_keywords": [
        "intern", "junior", "associate"
    ],

    # Output files
    "output_file": "job_report.html",
    "seen_jobs_file": "seen_jobs.json",   # Tracks jobs already shown
}
