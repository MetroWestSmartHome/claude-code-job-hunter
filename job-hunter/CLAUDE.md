# Job Hunter - Automated Job Discovery

## Purpose

Automated job scraping and AI-powered matching against your resume and preferences.
Feeds high-quality leads into the manual application workflow in `docs/resume-files/`.

**Quick Start:** Type `/job-apply` to launch the full guided workflow (scraping → scoring → materials creation)

---

## Job Sources & Safety

**Current sources (safe for scraping):**
- ✅ **Indeed** - No rate limiting, best scraper (per JobSpy docs)
- ✅ **Google Jobs** - Public API, safe to use
- ❌ **ZipRecruiter** - Removed (Cloudflare 403 blocking)

**Not using (requires proxies):**
- ❌ **LinkedIn** - Rate limits around 10th page, high IP ban risk

**IP Ban Risk:** LOW - Indeed and Google Jobs are designed for programmatic access

---

## Workflow

### Daily Discovery Run

```bash
cd job-hunter
python job_hunter.py
```

Opens `job_report.html` in your browser with scored matches (65+ by default).

**What it does:**
- Scrapes Indeed and Google Jobs (ZipRecruiter removed due to Cloudflare blocking)
- Uses Claude API to score each job against your resume + preferences
- Outputs styled HTML report with match analysis
- Caches seen jobs in `seen_jobs.json` to avoid duplicates
- **Deduplication:** Automatically skips previously seen jobs (91 found → 15 new, 76 duplicates filtered)

### When to Use --no-ai Mode

```bash
python job_hunter.py --no-ai
```

**Output:** `jobs_for_review.csv` with all scraped jobs (no AI scoring)

**Use cases:**
- API cost control
- Manual review preference (use Claude Max plan instead of API)
- Testing scraper without API calls

**Then:** Follow the Claude Code scoring workflow below

---

## Integration with Application Workflow

### When You Find a Strong Match (Score 75+)

1. **Review in browser** - Open `job_report.html`, click "View Job" to review full posting

2. **Create application folder** (if pursuing):
   ```bash
   cd docs\resume-files
   python tools/create-application-folder.py \
       --company "CompanyName" \
       --role "Job Title" \
       --url "https://job-posting-url" \
       --salary "XXX-YYYk" \
       --source "job-hunter"
   ```

**This creates:**
- `companyname-jobtitle/` folder with templates
- Pre-populated `job-posting.md`
- Copy of `resume-base.md` → `resume.md`
- Cover letter template
- README.md with interview prep sections
- Entry in `APPLICATION_TRACKER.md` with source metadata

3. **Customize materials** - Follow resume-files workflow (see `docs/resume-files/CLAUDE.md`)

---

## Configuration

### Search Terms (config.py)

Edit `search_terms` list to adjust discovery focus.

**Example strategy:**
- Target senior leadership roles (Director/VP level)
- Remote or hybrid positions
- Focus on your primary domain expertise

**Example configuration:**
See `config-TEMPLATE.py` for all customizable search parameters, including:
- Search terms (your target job titles)
- Location and remote preference
- Job boards to search
- Results per search

### Candidate Profile (candidate_profile.md)

**MUST STAY IN SYNC** with `docs/resume-files/base-master/resume-base.md`

**What it contains:**
- Must-haves (work location preference, management level, etc.)
- Strong positives (your domain focus, tech stack, culture preferences, salary range)
- Negatives (deal-breakers specific to your search - see template for examples)

**Update when:**
- Adding new skills to resume
- Changing role focus
- Adjusting salary range
- Updating must-haves/deal-breakers

### Resume Sync

job_hunter.py reads `resume.txt` for AI scoring context.

**Option A: Symlink (Recommended)**

One-time setup in **admin Scripting**:
```powershell
New-Item -ItemType SymbolicLink `
    -Path "job-hunter\resume.txt" `
    -Target "docs\resume-files\base-master\resume-base.md"
```

**Benefits:**
- Single source of truth
- Always up to date
- No manual sync needed

**Drawbacks:**
- Requires admin privileges
- OneDrive sometimes handles symlinks poorly

**Option B: Manual Sync**

After updating `base-master/resume-base.md`:
```bash
cp docs/resume-files/base-master/resume-base.md job-hunter/resume.txt
```

**Benefits:**
- No admin required
- Explicit control

**Drawbacks:**
- Can get out of sync
- Requires discipline

**Validation (optional):**
Create `tools/check-sync.py` that compares files and warns if different.

---

## Claude Code Scoring Workflow (No API Key)

If you want to use Claude Code (Max plan) instead of API calls:

### Step 1: Scrape Jobs
```bash
python job_hunter.py --no-ai
# Creates jobs_for_review.csv
```

### Step 2: Enhance with Company Ratings & Deduplication
```bash
python enhance_job_data.py
# Creates jobs_enhanced.csv with:
# - Deduplication tracking (job_hash, is_duplicate, first_seen_date)
# - Company rating placeholders (to be filled by Claude Code)
```

### Step 3: Filter for Promising Roles
```bash
python filter_promising_jobs.py
# Reads filters from config.py:
# - Remote preference (config: remote_only)
# - IT leadership titles (config: target_titles)
# - Salary minimum (config: min_salary)
# - IT subspecialties matching your expertise (config: it_subspecialties)
# - Excludes negative keywords (config: negative_keywords)
# Creates promising_jobs_v2.txt with job IDs
```

### Step 4: Claude Code Scoring

Ask Claude Code to:
1. Read `candidate_profile.md` (your preferences)
2. Read `jobs_enhanced.csv` for promising job IDs
3. For each job:
   - Score against your profile (0-100)
   - Identify gaps and how to address them
   - Recommend: APPLY / CONSIDER / SKIP
4. **Only for high-scoring jobs (75+):** Search company reviews (Indeed, Glassdoor) and add rating/notes
5. Generate scored report with company ratings for strong matches
6. Add top matches to `APPLICATION_TRACKER.md` Discovery Pipeline

**Token Optimization:** Company rating searches are only done for strong technical fits (score 75+). No point researching company culture if the job itself isn't a good match.

### Step 5: Application Materials

For high-scoring jobs with good company ratings, use the `/job-apply` skill or manual workflow:

**Option A: Use skill (recommended)**
```bash
/job-apply
# Guides through complete workflow including materials creation
```

**Option B: Manual workflow**
```bash
cd ../docs/resume-files
# Manually customize resume.md from base-master/resume-base.md
# Use tools/md-to-docx.py to generate .docx
# Create cover letter
# See docs/resume-files/CLAUDE.md for full process
```

**Note:** `create-application-folder.py` is planned but not yet implemented. Currently creating folders manually.

---

## Deduplication & Company Ratings

### How Deduplication Works

**Job Hash:** Combination of company + title + location
**Tracking File:** `seen_jobs.json`

When you run `enhance_job_data.py`:
- Generates unique hash for each job
- Checks against `seen_jobs.json`
- Marks duplicates (previously seen)
- Updates `seen_jobs.json` with new jobs

**Benefits:**
- Won't re-score same job posting multiple times
- Tracks when job was first discovered
- Can identify re-posts (same job posted again weeks later)

### Company Rating Integration

**Rating Sources:**
- Indeed company reviews
- Glassdoor ratings
- Employee review themes (leadership, work-life balance, pay, culture)

**Two-Phase Approach (Token Efficient):**

**Phase 1: Technical Scoring (All Jobs)**
- Score job against your profile (0-100)
- Identify technical gaps
- Make initial recommendation

**Phase 2: Company Research (75+ Scores Only)**
- Search Indeed/Glassdoor for company reviews
- Extract overall rating (1-5 stars)
- Summarize key themes (leadership, work-life balance, culture)
- Flag red flags (toxic culture, high turnover, poor management)
- Final recommendation: STRONG FIT / GOOD BUT CULTURAL CONCERNS / SKIP

**Why Two Phases:** Avoids wasting tokens researching companies for jobs that aren't technical fits. Only research culture for roles worth pursuing.

**Example:**
```
Job: Sr. Director, IT - ExampleCompany
Score: 85/100 (technical fit)
Company Rating: X.X/5 (Indeed) - ⚠️ LOW
Key Issues: Frequent leadership changes, poor communication from executives
Recommendation: STRONG TECHNICAL FIT but CULTURAL CONCERNS - research further before applying
```

---

## Cache Management

`seen_jobs.json` prevents showing the same jobs repeatedly and enables deduplication.

**Reset cache (start fresh):**
```bash
rm seen_jobs.json
python job_hunter.py --no-cache
```

**When to reset:**
- After 30+ days (job postings may have changed)
- When significantly changing search terms
- When changing candidate profile focus

---

## Command-Line Options

```bash
# Normal run with AI scoring
python job_hunter.py

# Ignore cache (rescore everything)
python job_hunter.py --no-cache

# Lower minimum score threshold
python job_hunter.py --min-score 55

# Skip AI scoring, export CSV only
python job_hunter.py --no-ai
```

---

## Automation (Optional)

### Windows Task Scheduler

Run daily at 7 AM:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "python" `
    -Argument "job-hunter\job_hunter.py" `
    -WorkingDirectory "job-hunter"

$trigger = New-ScheduledTaskTrigger -Daily -At 7am

Register-ScheduledTask -Action $action -Trigger $trigger `
    -TaskName "Job Hunter Daily" `
    -Description "Automated job discovery"
```

**Output location:** `job_report.html` opens automatically in browser

### Auto-Open Report (Optional)

```bash
python job_hunter.py && start job_report.html
```

---

## Cost Estimate

Each job scored ≈ 1 Claude API call (~1,500 tokens in/out)

**Typical rates:**
- 50 jobs/day ≈ $0.05-0.10/day
- Monthly (with caching) ≈ $1-3 total

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'jobspy'"

Install dependencies:
```bash
pip install python-jobspy anthropic
```

### "ANTHROPIC_API_KEY not set"

Set environment variable:
```bash
# Scripting
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Or edit CONFIG in config.py (less secure)
```

### Resume not found

Verify `resume.txt` exists (symlink or copy of base-master/resume-base.md)

### Scores seem off

Refine `candidate_profile.md` to be more specific about must-haves and negatives.
Expect 2-3 iterations before scores feel accurate.

---

## Quick Reference

### Command Skill
- `/job-apply` - Full guided workflow (scraping → scoring → materials)
- See `.claude/skills/job-apply/SKILL.md` for complete documentation

### Scripts
- `job_hunter.py --no-ai` - Scrape jobs without API
- `enhance_job_data.py` - Add deduplication + company rating placeholders
- `filter_promising_jobs.py` - Filter using criteria from config.py (salary, titles, subspecialties)

### Key Files
- `config.py` - Search terms, job sources, filters
- `candidate_profile.md` - Your preferences (must-haves, negatives)
- `resume.txt` - Resume for scoring (sync with base-master/resume-base.md)
- `seen_jobs.json` - Deduplication cache

## See Also

- **Job application skill:** `.claude/skills/job-apply/SKILL.md`
- **Application workflow:** `docs/resume-files/CLAUDE.md`
- **Application tracking:** `docs/resume-files/APPLICATION_TRACKER.md`
- **Manual Claude Code review:** `reference-files/CLAUDE_CODE_PROMPT.md`
- **Original README:** `reference-files/README.md`

---

**Last Updated:** [DATE]
**Status:** Active integration with resume-files workflow. Skill-based automation implemented.
