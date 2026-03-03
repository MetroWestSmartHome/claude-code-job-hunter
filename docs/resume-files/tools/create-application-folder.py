#!/usr/bin/env python3
"""
Create application folder structure with templates.

Usage:
    python tools/create-application-folder.py \
        --company "CompanyName" \
        --role "Job Title" \
        --url "https://job-posting-url" \
        --salary "XXX-YYYk" \
        --source "job-hunter"
"""

import argparse
import re
from pathlib import Path
from datetime import datetime
import shutil

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def create_job_posting_md(company, role, url, salary):
    """Create job-posting.md template."""
    return f"""# {company} - {role}

**Job URL:** {url}
**Salary Range:** {salary}
**Location:** [Fill in - Remote/Hybrid/On-site]
**Date Reviewed:** {datetime.now().strftime('%Y-%m-%d')}

---

## Job Description

[Paste full job description here]

---

## Requirements Analysis

### Must-Have Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

### Nice-to-Have Requirements
- [ ] Requirement 1
- [ ] Requirement 2

### Technologies/Skills Mentioned
- Technology 1
- Technology 2
- Technology 3

---

## Gap Analysis

### Gaps to Address

**Gap 1: [Technology/Experience]**
- **What they want:** [Specific requirement]
- **What you have:** [Your equivalent experience]
- **How to bridge:** [Positioning strategy]

**Gap 2: [Technology/Experience]**
- **What they want:** [Specific requirement]
- **What you have:** [Your equivalent experience]
- **How to bridge:** [Positioning strategy]

---

## Why This Role Fits

### Strong Alignment
- ✅ Alignment point 1
- ✅ Alignment point 2
- ✅ Alignment point 3

### Transferable Experience
- Experience 1 → How it applies
- Experience 2 → How it applies
- Experience 3 → How it applies

---

## Application Strategy

### Resume Customization
- **Headline:** [Suggested headline]
- **Competencies to emphasize:** [List 3-5 key areas]
- **Bullets to prioritize:** [Which experiences to highlight]

### Cover Letter Focus
- Paragraph 1: [Key theme]
- Paragraph 2: [Key theme]
- Paragraph 3: [Key theme]
- Gap addressing: [Which gaps to address and how]

---

## Company Research

### Company Overview
[Add company description, size, industry, stage]

### Company Culture
**Ratings:**
- Indeed: X.X/5
- Glassdoor: X.X/5

**Key Themes from Reviews:**
- Positive: [Theme 1, Theme 2]
- Concerns: [Theme 1, Theme 2]

**Red Flags:** [Any concerns about culture, leadership, turnover]

---

## Interview Preparation

### Questions to Prepare For
1. [Anticipated question 1]
2. [Anticipated question 2]
3. [Anticipated question 3]

### Questions to Ask Them
1. [Your question 1]
2. [Your question 2]
3. [Your question 3]

---

**Status:** Materials being created
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

def create_readme_md(company, role, url, salary, source):
    """Create README.md with application summary."""
    return f"""# {company} - {role}

**Application Status:** Materials Created - Ready for Review
**Discovery Date:** {datetime.now().strftime('%Y-%m-%d')}
**Source:** {source}

---

## Quick Summary

**Why This Role:**
- [Fill in key reasons]

**Company:** {company}
**Job URL:** {url}

---

## Files in This Folder

- **`job-posting.md`** - Full job description, requirements, gap analysis, application strategy
- **`resume.md`** - Markdown source (customized for {company})
- **`resume-v1.docx`** - Generated resume (ready for Jobscan) - TO BE CREATED
- **`cover-letter.md`** - Cover letter draft - TO BE CREATED
- **`cover-letter.docx`** - Final cover letter - TO BE CREATED
- **`README.md`** - This file

---

## Key Customizations

**Resume Headline:**
"[TO BE DETERMINED based on job posting]"

**Summary Emphasis:**
- [Key theme 1]
- [Key theme 2]
- [Key theme 3]

**Core Competencies Reordered:**
1. [Most relevant competency first]
2. [Second most relevant]
3. [Third most relevant]

**Experience Bullets:**
- [Note which bullets to prioritize from current role]
- [Note which bullets to prioritize from previous roles]

---

## Gaps & How We Address Them

### 1. [Gap Name]
**Bridge:** [Strategy to position your experience as equivalent]

### 2. [Gap Name]
**Bridge:** [Strategy to position your experience as equivalent]

---

## Strengths to Emphasize

✅ [Strength 1 - direct requirement match]
✅ [Strength 2 - direct requirement match]
✅ [Strength 3 - direct requirement match]

---

## Next Steps

1. **Complete job-posting.md** - Paste full job description and complete analysis
2. **Customize resume.md** - Based on job-posting.md analysis
3. **Generate resume-v1.docx** - Run `python ../tools/md-to-docx.py resume.md`
4. **Run Jobscan** - Target 75%+ match
5. **Create cover letter** - Run `python ../tools/cover-letter-template.py`
6. **Final review** - Check 2-page limit, gaps addressed
7. **Submit application**

---

## Interview Prep Topics

**Be ready to discuss:**

1. **[Topic 1]:**
   - [Preparation notes]

2. **[Topic 2]:**
   - [Preparation notes]

3. **[Topic 3]:**
   - [Preparation notes]

---

**Status:** Ready for customization
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

def create_cover_letter_template_md(company, role):
    """Create cover-letter-template.md for user to fill in."""
    return f"""# Cover Letter Template - {company}

**Role:** {role}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

---

## Instructions

Fill in the sections below, then run:
```bash
python ../tools/cover-letter-template.py --input cover-letter-template.md
```

This will generate `cover-letter.docx` with proper formatting.

---

## Template

### Why Interested
[2-3 sentences explaining what makes this role compelling to you]

### Paragraph 1: Experience Alignment
[3-4 sentences connecting your experience to their requirements]

### Paragraph 2: Technical Depth
[3-4 sentences demonstrating deep technical expertise in key areas they need]

### Paragraph 3: Leadership & Approach
[3-4 sentences showing your leadership philosophy and how it fits their culture]

### Paragraph 4: Gap Addressing (if needed)
[2-3 sentences honestly addressing key gaps and positioning your transferable experience]

---

## Reference: ExampleCompany v2 Tone (Professional Middle-Ground)

- Direct but not overly casual
- Confident but not arrogant
- Honest about gaps without apologizing
- Emphasize strategic + hands-on balance
- Show enthusiasm without being desperate

**Example opening:**
"I'm reaching out regarding the {role} role at {company}. [What makes it compelling]. My 15+ years in IT leadership, particularly [key experience area], aligns well with what you're looking for."

**Example gap addressing:**
"While my experience is primarily with [your tech], the underlying principles of [concept] are platform-agnostic, and I'm confident in quickly adapting to [their tech]."

---

**Status:** Template ready - fill in and generate
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

def update_application_tracker(company, role, url, salary, source, folder_name):
    """Add entry to APPLICATION_TRACKER.md Discovery Pipeline."""
    tracker_path = Path("APPLICATION_TRACKER.md")

    if not tracker_path.exists():
        print(f"Warning: {tracker_path} not found - skipping tracker update")
        return

    content = tracker_path.read_text(encoding='utf-8')

    # Find Discovery Pipeline section
    if "## Discovery Pipeline" not in content:
        print("Warning: 'Discovery Pipeline' section not found in APPLICATION_TRACKER.md")
        return

    # Create new entry
    entry = f"""
### {company} - {role} 📋 MATERIALS CREATED
**Discovery Date:** {datetime.now().strftime('%Y-%m-%d')}
**Source:** {source}
**Salary:** {salary}
**Folder:** `{folder_name}/`
**Job Posting:** {url}
**Status:** Materials created, ready for customization

**Next Steps:**
1. Complete job-posting.md analysis
2. Customize resume.md
3. Generate cover letter
4. Submit application

---
"""

    # Insert after Discovery Pipeline header
    discovery_section = "## Discovery Pipeline"
    parts = content.split(discovery_section, 1)
    if len(parts) == 2:
        # Find the next line after the header (skip blank lines and workflow description)
        lines = parts[1].split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('**') and not line.startswith('Jobs flagged'):
                insert_index = i
                break

        lines.insert(insert_index, entry)
        new_content = parts[0] + discovery_section + '\n'.join(lines)

        tracker_path.write_text(new_content, encoding='utf-8')
        print(f"✅ Updated APPLICATION_TRACKER.md")
    else:
        print("Warning: Could not parse Discovery Pipeline section")

def main():
    parser = argparse.ArgumentParser(description='Create application folder structure')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--role', required=True, help='Job title')
    parser.add_argument('--url', required=True, help='Job posting URL')
    parser.add_argument('--salary', required=True, help='Salary range (e.g., "XXX-YYYk")')
    parser.add_argument('--source', default='manual', help='Source (job-hunter, linkedin, referral, manual)')

    args = parser.parse_args()

    # Create folder name
    folder_name = f"{slugify(args.company)}-{slugify(args.role)}"
    folder_path = Path(folder_name)

    if folder_path.exists():
        print(f"Error: Folder '{folder_name}' already exists")
        return 1

    print(f"Creating application folder: {folder_name}")
    folder_path.mkdir(parents=True)

    # Create job-posting.md
    print("  Creating job-posting.md...")
    job_posting_path = folder_path / "job-posting.md"
    job_posting_path.write_text(create_job_posting_md(args.company, args.role, args.url, args.salary), encoding='utf-8')

    # Create README.md
    print("  Creating README.md...")
    readme_path = folder_path / "README.md"
    readme_path.write_text(create_readme_md(args.company, args.role, args.url, args.salary, args.source), encoding='utf-8')

    # Create cover-letter-template.md
    print("  Creating cover-letter-template.md...")
    cover_letter_template_path = folder_path / "cover-letter-template.md"
    cover_letter_template_path.write_text(create_cover_letter_template_md(args.company, args.role), encoding='utf-8')

    # Copy resume-base.md to resume.md
    base_master_path = Path("base-master/resume-base.md")
    if base_master_path.exists():
        print("  Copying base-master/resume-base.md -> resume.md...")
        resume_path = folder_path / "resume.md"
        shutil.copy(base_master_path, resume_path)
    else:
        print("  Warning: base-master/resume-base.md not found - skipping resume copy")

    # Update APPLICATION_TRACKER.md
    print("  Updating APPLICATION_TRACKER.md...")
    update_application_tracker(args.company, args.role, args.url, args.salary, args.source, folder_name)

    print(f"\n✅ Application folder created: {folder_name}/")
    print(f"\nNext steps:")
    print(f"1. cd {folder_name}")
    print(f"2. Complete job-posting.md analysis")
    print(f"3. Customize resume.md")
    print(f"4. python ../tools/md-to-docx.py resume.md")
    print(f"5. Fill in cover-letter-template.md")
    print(f"6. python ../tools/cover-letter-template.py --input cover-letter-template.md")

    return 0

if __name__ == "__main__":
    exit(main())
