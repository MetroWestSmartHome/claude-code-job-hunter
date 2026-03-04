---
name: job-apply
description: End-to-end job application workflow from discovery to submission
disable-model-invocation: true
version: 1.0.0
---

# Job Application Workflow

**Purpose:** Automate the complete job application workflow from job-hunter discovery through application submission.

**Invocation:** User types `/job-apply` or when starting job application work

---

## Workflow Phases

### Phase 1: Job Discovery & Scoring

**Steps:**
1. **Run job scraper** (no API key needed)
   ```bash
   cd job-hunter
   python job_hunter.py --no-ai
   ```

2. **Enhance with deduplication**
   ```bash
   python enhance_job_data.py
   ```
   - Adds job hashing for deduplication
   - Creates jobs_enhanced.csv with company rating placeholders

3. **Filter promising roles**
   ```bash
   python filter_promising_jobs.py
   ```
   - Filters for: Remote preference, leadership titles, min salary (all from config.py)
   - Excludes: Helpdesk-only, on-site, low salary
   - Creates promising_jobs_v2.txt

4. **Score jobs (Two-Phase)**

   **Phase 1: Technical Scoring (All Jobs)**
   - Read `candidate_profile.md`
   - For each job in promising_jobs_v2.txt:
     - Score against profile (0-100)
     - Identify technical gaps
     - Initial recommendation: APPLY / CONSIDER / SKIP

   **Phase 2: Company Research (75+ Scores Only)**
   - Search Indeed for company reviews
   - Search Glassdoor for ratings
   - Extract overall rating (X.X/5)
   - Summarize themes: leadership, work-life balance, culture
   - Flag red flags: toxic culture, high turnover, poor management
   - Final recommendation: STRONG FIT / GOOD BUT CONCERNS / SKIP

   **Why Two Phases:** Token efficiency - only research companies for technical fits

5. **Update APPLICATION_TRACKER.md**
   - Add high-scoring jobs (75+) to Discovery Pipeline section
   - Include: job-hunter score, company ratings, concerns
   - Template:
     ```markdown
     ### [Company] - [Role] ⭐ READY FOR REVIEW
     **Discovery Date:** YYYY-MM-DD
     **Job-Hunter Score:** XX/100
     **Company Rating:** X.X/5 (Indeed) | X.X/5 (Glassdoor)
     **Company Notes:** [Key themes from reviews]
     **Salary:** $[MIN]-$[MAX]k
     **Location:** Remote/Hybrid/On-site
     **Job Posting:** https://...
     **Why High Score:** [Technical/skill match]
     **Concerns:** [Cultural issues, gaps, red flags]
     **Next Step:** Review job posting, decide by YYYY-MM-DD
     **Status:** ⏳ Pending Review
     ```

---

### Phase 2: Application Materials Creation

**When:** User decides to pursue a high-scoring job

**Steps:**
1. **Create application folder**
   ```bash
   cd docs\resume-files
   python tools/create-application-folder.py \
       --company "CompanyName" \
       --role "Job Title" \
       --url "https://job-posting-url" \
       --salary "XXX-YYYk" \
       --source "job-hunter"
   ```

   **Creates:**
   - `companyname-jobtitle/` folder
   - `job-posting.md` (pre-populated)
   - `resume.md` (copy of base-master/resume-base.md)
   - `cover-letter-template.md`
   - `README.md` (interview prep template)
   - Updates `APPLICATION_TRACKER.md` with "In Progress" status

2. **Customize resume.md**

   **Critical Rules:**
   - ✅ Only use content from `base-master/resume-base.md`
   - ❌ NEVER hallucinate bullets or combine content
   - ❌ NEVER add false information
   - ✅ Ask user if unsure about content

   **Workshop Best Practices:**
   - Add headline below name: `**IT Leader | [Focus Area]**`
   - 2 pages maximum
   - Current role: 7-9 bullets
   - Previous roles: 3-4 bullets each
   - Remove category headers (for specialist/IC roles)
   - Keep category headers (for Director+ roles managing multiple areas)

   **Customization Steps:**
   a. Read job posting for focus areas
   b. Add relevant headline
   c. Emphasize relevant summary content
   d. Reorder competencies (most relevant first)
   e. Select most relevant bullets from base-master
   f. Address gaps in experience (bridge with transferable skills)

3. **Generate .docx**
   ```bash
   python tools/md-to-docx.py companyname-jobtitle/resume-v1.md
   ```

4. **Jobscan optimization**
   - Upload resume-v1.docx to Jobscan
   - Paste job description
   - Target: 75%+ match
   - Add missing keywords (only if accurate)
   - Regenerate .docx
   - Iterate until 75%+

5. **Generate cover letter**
   ```bash
   cd companyname-jobtitle
   python ../tools/cover-letter-template.py \
       --company "CompanyName" \
       --role "Job Title"
   ```

   **Cover Letter Strategy:**
   - Professional tone (ExampleCompany v2 style)
   - Address key gaps honestly
   - Emphasize differentiators (AI/automation, strategic liaison work)
   - 3-4 paragraphs max

6. **Update APPLICATION_TRACKER.md**
   - Move from "Discovery Pipeline" → "In Progress"
   - Add materials created
   - Add gaps addressed
   - Add next steps

---

### Phase 3: Pre-Submission Checklist

**Before submitting:**
- [ ] Resume is 2 pages maximum
- [ ] Jobscan score 75%+
- [ ] Cover letter addresses key gaps
- [ ] All files follow naming conventions
- [ ] Company ratings reviewed (if concerns, decide whether to proceed)
- [ ] README.md has interview prep notes
- [ ] APPLICATION_TRACKER.md updated with submission date

**Submit application via company portal**

**After submission:**
- Update APPLICATION_TRACKER.md status: ✅ SUBMITTED
- Move from "In Progress" → "Active Applications"
- Add submission date
- Set next steps: "⏳ Wait for response"

---

## Critical Rules

### Resume Content Accuracy
**ZERO TOLERANCE FOR HALLUCINATIONS**

- ❌ NEVER add bullet points not in base-master/resume-base.md
- ❌ NEVER combine/modify bullets without user approval
- ❌ NEVER assume technologies or projects
- ❌ NEVER invent responsibilities or achievements
- ✅ ONLY use content explicitly in base-master or provided by user
- ✅ ALWAYS verify against source of truth
- ✅ ALWAYS ask if uncertain

**Historical Context:** In Feb 2026, Claude hallucinated a Platform SSO bullet combining elements from two real bullets. This is **COMPLETELY UNACCEPTABLE**.

### Markdown-First Workflow
- ALL resume editing happens in .md files
- Convert to .docx via md-to-docx.py
- Never edit .docx directly

### Base Master is Comprehensive
- `base-master/resume-base.md` contains ALL bullets (more than workshop recommends)
- Job-specific variants consolidate to 7-9 bullets per role
- Select from base-master, never create new content

---

## Configuration Files

### Candidate Profile (`job-hunter/candidate_profile.md`)
**MUST STAY IN SYNC** with `docs/resume-files/base-master/resume-base.md`

**Update when:**
- Adding new skills to resume
- Changing role focus
- Adjusting salary range
- Updating must-haves/deal-breakers

### Resume Sync
**Option A: Symlink** (recommended if admin access)
```powershell
New-Item -ItemType SymbolicLink `
    -Path "job-hunter\resume.txt" `
    -Target "docs\resume-files\base-master\resume-base.md"
```

**Option B: Manual Sync**
```bash
cp docs/resume-files/base-master/resume-base.md job-hunter/resume.txt
```

---

## Automation Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `job_hunter.py` | Scrape jobs (Indeed, Google Jobs, ZipRecruiter) | `job-hunter/` |
| `enhance_job_data.py` | Add deduplication + company rating placeholders | `job-hunter/` |
| `filter_promising_jobs.py` | Filter for IT leadership roles | `job-hunter/` |
| `create-application-folder.py` | Scaffold application materials | `docs/resume-files/tools/` |
| `md-to-docx.py` | Convert markdown → Word .docx | `docs/resume-files/tools/` |
| `cover-letter-template.py` | Generate cover letter from template | `docs/resume-files/tools/` |

---

## Success Metrics

### Discovery Phase
- Time from scrape → scored report: < 30 minutes
- False positive rate (score 75+ but not worth applying): < 20%
- Company rating research: Only for 75+ scores (token efficient)

### Application Phase
- Time from decision → materials ready: < 2 hours
- Resume customization: ~1 hour (vs. ~2 hours manual)
- Cover letter generation: ~30 min (vs. ~1 hour manual)
- Jobscan score: 75%+ on first or second iteration

### Quality
- Zero hallucinated resume content
- Zero SEO keyword stuffing (only accurate keywords)
- Zero missing gap addressing in cover letters

---

## Common Pitfalls

### Salary Threshold
❌ Assuming $130k is acceptable
✅ User minimum salary from config.py (flexible for exceptional fit with great benefits)

### Hybrid Roles
❌ Assuming "[City] area" is commutable
✅ Only YOUR_CITY area is commutable
✅ Check commute time for your area

### IT Focus Areas
✅ IT subspecialties defined in config.py (it_subspecialties)
❌ Roles matching negative keywords from config.py (negative_keywords)

### Company Ratings
❌ Researching every company (token waste)
✅ Only research companies for 75+ technical fit scores
❌ Ignoring low ratings (< 3.0)
✅ Flag red flags: toxic culture, high turnover, leadership issues

---

## Integration Points

### Task Orchestrator
- Create task for each application: "Apply to [Company] - [Role]"
- Track status: pending → in_progress → completed
- Log sections for decisions (why pursuing, gaps addressed, etc.)

### Application Tracker
- Discovery Pipeline: High-scoring jobs not yet pursued
- In Progress: Materials being created
- Active Applications: Submitted applications awaiting response
- Closed: Rejected, withdrawn, or offered

### MCP Servers
- None required for job application workflow
- All operations are file-based and web searches

---

## Example Invocation

User: `/job-apply`

Claude Code:
```
=== Job Application Workflow ===

Phase 1: Job Discovery & Scoring

Step 1: Running job scraper...
[Runs job_hunter.py --no-ai]
✅ 94 jobs scraped

Step 2: Enhancing with deduplication...
[Runs enhance_job_data.py]
✅ jobs_enhanced.csv created (0 duplicates detected)

Step 3: Filtering promising roles...
[Runs filter_promising_jobs.py]
✅ 6 promising jobs found

Step 4: Scoring jobs...

Job #27 - ExampleCompany Sr. Director IT End User Services
  Technical Score: 85/100
  Gaps: ITSM Platform (have PLATFORM_B), Site-specific support
  Company Rating: Researching...
  [Searches Indeed] → X.X/5 ⚠️ LOW RATING
  Key Issues: [SPECIFIC CONCERNS]
  Final Recommendation: STRONG TECHNICAL FIT but CULTURAL CONCERNS

Job #32 - ExampleCompany B Director IT
  Technical Score: 75/100
  Gaps: Industry-specific systems
  Company Rating: Researching...
  [No Indeed reviews found] → N/A
  Final Recommendation: GOOD FIT - Verify remote flexibility

[... continues for other jobs ...]

Step 5: Updating APPLICATION_TRACKER.md...
✅ 2 jobs added to Discovery Pipeline

Next Steps:
- Review high-scoring jobs in APPLICATION_TRACKER.md
- Decide which to pursue
- Run create-application-folder.py for chosen role
```

---

**Version:** 1.0.0
**Last Updated:** [DATE]
**Status:** Implemented
