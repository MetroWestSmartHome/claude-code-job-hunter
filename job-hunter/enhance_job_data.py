#!/usr/bin/env python3
"""
Enhance job data with company ratings and deduplication.
Run this AFTER job scraping to add company review data.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

def load_seen_jobs():
    """Load previously seen jobs for deduplication."""
    seen_file = Path("seen_jobs.json")
    if seen_file.exists():
        with open(seen_file, 'r') as f:
            data = json.load(f)
            # Handle migration from old list format to new dict format
            if isinstance(data, list):
                # Convert list of hashes to dict format
                return {hash_val: {"first_seen": datetime.now().isoformat()} for hash_val in data}
            return data
    return {}

def save_seen_jobs(seen_jobs):
    """Save updated seen jobs list."""
    with open("seen_jobs.json", 'w') as f:
        json.dump(seen_jobs, f, indent=2)

def generate_job_hash(row):
    """Generate unique hash for job (company + title + location)."""
    import hashlib
    key = f"{row['company']}|{row['title']}|{row['location']}".lower()
    return hashlib.md5(key.encode()).hexdigest()

def main():
    # Read scraped jobs
    csv_path = Path("jobs_for_review.csv")
    if not csv_path.exists():
        print("Error: jobs_for_review.csv not found")
        return

    df = pd.read_csv(csv_path)

    # Load seen jobs
    seen_jobs = load_seen_jobs()

    # Add job hash for deduplication
    df['job_hash'] = df.apply(generate_job_hash, axis=1)

    # Mark duplicates
    df['is_duplicate'] = df['job_hash'].apply(lambda h: h in seen_jobs)
    df['first_seen_date'] = df['job_hash'].apply(
        lambda h: seen_jobs.get(h, {}).get('first_seen', datetime.now().isoformat())
    )

    # Add placeholder for company rating (to be filled by Claude Code or manual)
    df['company_rating_indeed'] = None
    df['company_rating_glassdoor'] = None
    df['company_review_notes'] = ''

    # Update seen jobs
    for _, row in df.iterrows():
        if row['job_hash'] not in seen_jobs:
            seen_jobs[row['job_hash']] = {
                'first_seen': datetime.now().isoformat(),
                'company': row['company'],
                'title': row['title'],
                'location': row['location']
            }

    save_seen_jobs(seen_jobs)

    # Save enhanced CSV
    output_path = Path("jobs_enhanced.csv")
    df.to_csv(output_path, index=False)

    new_jobs = (~df['is_duplicate']).sum()
    duplicate_jobs = df['is_duplicate'].sum()

    print(f"Enhanced job data saved to: {output_path}")
    print(f"Total jobs: {len(df)}")
    print(f"New jobs: {new_jobs}")
    print(f"Duplicates (previously seen): {duplicate_jobs}")
    print(f"\nNext: Claude Code will add company ratings during scoring")

if __name__ == "__main__":
    main()
