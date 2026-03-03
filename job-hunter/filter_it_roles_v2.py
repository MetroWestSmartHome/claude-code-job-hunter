import pandas as pd
import re
from config import CONFIG

df = pd.read_csv('jobs_for_review.csv')

# Filter criteria (from config.py)
MIN_SALARY = CONFIG.get("min_salary", 0)
target_titles = CONFIG.get("target_titles", ['director', 'manager', 'head', 'vp'])
it_subspecialties = CONFIG.get("it_subspecialties", ['engineering', 'platform', 'operations'])
negative_keywords = CONFIG.get("negative_keywords", ['helpdesk', 'service desk'])

promising = []

for idx, row in df.iterrows():
    if not row['is_remote']:
        continue

    title_lower = str(row['title']).lower()
    desc_lower = str(row['description']).lower() if pd.notna(row['description']) else ''

    # Check if it's a leadership role
    is_leadership = any(t in title_lower for t in target_titles)

    if not is_leadership:
        continue

    # Check if it's IT-related
    is_it_related = any(keyword in title_lower or keyword in desc_lower[:500] for keyword in ['it ', 'information technology', 'technology', 'information'])

    if not is_it_related:
        continue

    # Check for IT subspecialties
    has_subspecialty = any(spec in title_lower or spec in desc_lower[:1000] for spec in it_subspecialties)

    # Check for negative keywords (support-focused)
    is_support_focused = any(neg in title_lower for neg in negative_keywords)

    # Check salary
    salary_min = row['min_amount'] if pd.notna(row['min_amount']) else None
    meets_salary = salary_min is None or salary_min >= MIN_SALARY

    # Location check for hybrid (reads user's city from config)
    location = str(row['location'])
    user_city = CONFIG.get("location", "").split(",")[0].strip().lower()  # Extract city from "City, State"
    is_local_area = user_city and user_city in location.lower()

    # Categorize
    if has_subspecialty and meets_salary and not is_support_focused:
        score_note = ""
        if salary_min and salary_min >= (MIN_SALARY + 10000):
            score_note = "[STRONG SALARY]"
        elif salary_min and salary_min >= MIN_SALARY:
            score_note = "[Meets min]"
        elif not salary_min:
            score_note = "[Salary TBD]"

        if is_local_area:
            score_note += f" | [{user_city.title()} area - check commute]"

        promising.append((idx+1, row, score_note))

print(f'Found {len(promising)} promising IT leadership roles:\n')
print('='*100)

for job_num, row, note in promising:
    salary = f"${int(row['min_amount']/1000)}k-${int(row['max_amount']/1000)}k" if pd.notna(row['min_amount']) else 'Salary not listed'
    print(f"{job_num:2d}. {row['title'][:55]:55s} - {row['company'][:25]:25s}")
    print(f"    {salary:25s} | {note}")
    print(f"    {row['location']}")
    print()

# Save IDs for detailed scoring
with open('promising_jobs_v2.txt', 'w') as f:
    f.write(f"Promising IT Leadership Roles (Min Salary: ${int(MIN_SALARY/1000)}k)\n")
    f.write(f"Total found: {len(promising)}\n\n")
    for job_num, row, note in promising:
        f.write(f"{job_num}\n")
