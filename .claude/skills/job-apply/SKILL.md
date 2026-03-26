---
name: job-apply
description: Create application materials (resume, cover letter, folder) for a specific role. Run after /job-scraper finds actionable roles.
disable-model-invocation: true
version: 2.0.0
---

# Job Application Materials Workflow

**Purpose:** Create tailored application materials for a specific role already identified as worth pursuing.

**Invocation:** User types `/job-apply` — assumes a role has already been chosen. If no role is specified, ask: "Which role are you applying to?"

**For discovery/scraping:** Use `/job-scraper` instead.

---

## Steps

### 1. Create application folder
```bash
cd docs/resume-files
python tools/create-application-folder.py \
    --company "CompanyName" \
    --role "Job Title" \
    --url "https://job-posting-url" \
    --salary "150-200k" \
    --source "job-hunter"
```

Creates:
- `companyname-jobtitle/` folder
- `job-posting.md` (pre-populated)
- `resume.md` (copy of base-master/resume-base.md)
- `cover-letter-template.md`
- `README.md` (interview prep template)
- Updates `APPLICATION_TRACKER.md` with "In Progress" status

### 2. Customize resume.md

**ZERO TOLERANCE FOR HALLUCINATIONS:**
- ❌ NEVER add bullets not in `base-master/resume-base.md`
- ❌ NEVER combine or modify bullets without user approval
- ❌ NEVER invent responsibilities, technologies, or achievements
- ✅ ONLY use content explicitly in base-master or provided by user
- ✅ ALWAYS ask if uncertain

**Historical Context:** In Feb 2026, Claude hallucinated a bullet combining two real bullets. This is COMPLETELY UNACCEPTABLE.

**Customization steps:**
a. Read job posting for focus areas
b. Add headline: `**[Your Title] | [Focus Area]**`
c. Emphasize relevant summary content
d. Reorder competencies (most relevant first)
e. Select most relevant bullets from base-master
f. Address gaps with transferable skills

**Format:**
- 2 pages maximum
- Current role: 7-9 bullets
- Previous roles: 3-4 bullets each
- Keep category headers for Director+ roles, remove for IC roles

### 3. Generate .docx
```bash
python tools/md-to-docx.py companyname-jobtitle/resume-v1.md
```

### 4. Jobscan optimization
- Upload resume-v1.docx to Jobscan
- Paste job description
- Target: 75%+ match
- Add missing keywords (only if accurate)
- Iterate until 75%+

### 5. Generate cover letter
```bash
cd companyname-jobtitle
python ../tools/cover-letter-template.py \
    --company "CompanyName" \
    --role "Job Title"
```

**Cover letter strategy:**
- Professional tone (use your best cover letter example as reference)
- Address key gaps honestly
- Emphasize your differentiators
- 3-4 paragraphs max

### 6. Update APPLICATION_TRACKER.md
- Move from "Discovery Pipeline" → "In Progress"
- Add materials created, gaps addressed, next steps

---

## Pre-Submission Checklist

- [ ] Resume is 2 pages maximum
- [ ] Jobscan score 75%+
- [ ] Cover letter addresses key gaps
- [ ] All files follow naming conventions
- [ ] Company ratings reviewed
- [ ] README.md has interview prep notes
- [ ] APPLICATION_TRACKER.md updated with submission date

After submitting:
- Update status: ✅ SUBMITTED
- Move to "Active Applications"
- Set next steps: "⏳ Wait for response"

---

## Common Pitfalls

- ❌ Check your minimum salary in config.py — don't apply below your threshold
- ❌ Verify commutability for any hybrid/on-site roles against your commutable_areas config
- ❌ Never edit .docx directly — always edit .md then regenerate

---

**Version:** 2.0.0
**Last Updated:** 2026-03-26
