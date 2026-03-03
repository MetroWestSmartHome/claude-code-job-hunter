# Claude Code Job Hunter - Quick Start

Get your AI-assisted job search running in 30 minutes.

## Prerequisites

- Python 3.11+
- Claude Code CLI ([install guide](https://github.com/anthropics/claude-code))
  - **With paid Claude plan (Pro/Team):** No API key needed - skills run within your Claude Code session
  - **Without Claude Code:** Anthropic API key required for standalone Python usage
  - **Recommendation:** Use Claude Code with paid plan for best experience

## 5-Step Setup

### 1. Install Dependencies (5 min)

```bash
pip install -r job-hunter/requirements.txt
pip install python-docx  # For resume conversion
```

### 2. Configure Job Search (5 min)

**Do this FIRST** - the job hunter needs your preferences.

```bash
cd job-hunter/

# Copy configuration templates
cp config-TEMPLATE.py config.py
cp candidate_profile-TEMPLATE.md candidate_profile.md

# Edit config.py with YOUR preferences:
# - search_terms: ["Your Job Title 1", "Your Job Title 2"]
# - location: "Your City, State"
# - remote_only: True/False
# - min_salary: 123456 (your minimum)
# - target_titles: ["director", "manager"] (leadership levels)
# - it_subspecialties: ["platform", "cloud"] (your domains)
# - negative_keywords: ["helpdesk", "support"] (roles to avoid)

# Edit candidate_profile.md:
# - Define must-haves and deal-breakers
# - Customize scoring criteria
```

### 3. Personalize Your Resume (15 min)

Navigate to `docs/resume-files/base-master/` and follow instructions:

```bash
cd docs/resume-files/base-master/

# Copy template files
cp resume-base-TEMPLATE.md resume-base.md
cp bullets-library-TEMPLATE.md bullets-library.md
cp competencies-library-TEMPLATE.md competencies-library.md

# Edit each file and replace ALL [PLACEHOLDER] text with YOUR information
# Search for "[" to find any missed placeholders
```

See [SETUP.md](SETUP.md) for detailed instructions on what to replace.

### 4. Test the System (3 min)

```bash
# Test job discovery (no AI, just scraping)
cd job-hunter
python job_hunter.py --no-ai

# Output: jobs_for_review.csv with scraped jobs
```

If using Claude Code, test materials generation:

```bash
# In Claude Code CLI
/job-materials

# Paste a sample job posting when prompted
# Verify resume generated with YOUR bullets
```

### 5. Start Job Hunting (2 min)

```bash
# Run complete workflow in Claude Code
/job-apply
```

## What Each Skill Does

- **`/job-apply`** - End-to-end: discovery → scoring → materials → tracking
- **`/job-materials`** - Generate resume + cover letter for specific job posting
- **Resume tools** - Convert markdown to .docx for submission

## Time Savings

- **Traditional process:** 5-8 hours per application
- **With this system:** 2-2.5 hours per application
- **Savings:** 3-5.5 hours per application

## Next Steps

- Read [SETUP.md](SETUP.md) for detailed personalization guide
- Review [docs/resume-files/CLAUDE.md](docs/resume-files/CLAUDE.md) for complete workflow
- Check [APPLICATION_TRACKER.md](docs/resume-files/APPLICATION_TRACKER.md) for tracking applications

## Troubleshooting

**"Skills not found"**
- Ensure `.claude/skills/` directory is in your workspace root
- Verify Claude Code is installed: `claude --version`

**"Job scraping fails"**
- Check `requirements.txt` is installed
- Try `--no-ai` flag first to test without Claude

**"Resume has placeholders"**
- Search files for `[` - replace all placeholders
- Common misses: phone, email, LinkedIn URL

See [SETUP.md](SETUP.md) for more troubleshooting help.
