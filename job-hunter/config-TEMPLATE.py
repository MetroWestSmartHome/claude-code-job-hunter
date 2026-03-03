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
        "YOUR JOB TITLE 1 remote",      # e.g., "IT Director remote"
        "YOUR JOB TITLE 2 remote",      # e.g., "Senior IT Manager remote"
        "YOUR JOB TITLE 3 remote",      # e.g., "Director of IT remote"
        # Add more search terms as needed
    ],

    "location": "YOUR_CITY, YOUR_STATE",  # e.g., "[YOUR_CITY, STATE]"
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

    # Filtering criteria (used by filter_it_roles_v2.py)
    "min_salary": 0,  # Minimum acceptable salary (e.g., 123456 for $123k)

    # Leadership titles to filter for
    "target_titles": [
        "director", "manager", "head", "vp",
        "senior manager", "sr. director", "sr director", "lead"
    ],

    # IT subspecialties that match your expertise
    # Customize for your domain (examples: 'security', 'devops', 'data', 'cloud')
    "it_subspecialties": [
        "engineering", "platform", "systems",
        "operations", "technology", "infrastructure"
    ],

    # Keywords to exclude (roles you want to avoid)
    "negative_keywords": [
        "helpdesk", "service desk",
        "support specialist", "technical support"
    ],

    # Output files
    "output_file": "job_report.html",
    "seen_jobs_file": "seen_jobs.json",   # Tracks jobs already shown
}
