# Claude Code Job Hunter

AI-assisted job search automation using Claude Code. Automates job discovery, resume customization, and cover letter generation with strict accuracy controls.

## What This Does

Transform your job search from 5-8 hours per application to 2-2.5 hours with:

- **Job Discovery:** Two-pass scraper — remote nationwide + local/hybrid in your commutable areas
- **Company Research:** Check Indeed/Glassdoor ratings before applying
- **Resume Optimization:** AI-assisted customization with hallucination prevention (optimizes for jobscan without inventing experience)
- **Cover Letter Generation:** Professional, company-specific letters addressing gaps
- **Application Tracking:** Organized pipeline from discovery to offer

**Time Savings:** 3-5.5 hours per application

## Quick Start

Get running in 30 minutes:

```bash
# 1. Install dependencies
pip install -r job-hunter/requirements.txt
pip install python-docx

# 2. Configure job search (DO THIS FIRST)
cp job-hunter/config-TEMPLATE.py job-hunter/config.py
cp job-hunter/candidate_profile-TEMPLATE.md job-hunter/candidate_profile.md
# Edit config.py: search_terms, location, min_salary, target_titles, it_subspecialties
# Edit candidate_profile.md: must-haves, deal-breakers, scoring criteria

# 3. Personalize your resume
# Follow docs/resume-files/base-master/SETUP.md - copy TEMPLATE files and fill in your info

# 4. Test job discovery
cd job-hunter
python job_hunter.py --no-ai

# 5. Start job hunting (in Claude Code)
/job-apply
```

See [QUICKSTART.md](QUICKSTART.md) for detailed setup.

## Prerequisites

- **Python 3.11+**
- **Claude Code CLI** ([install guide](https://github.com/anthropics/claude-code))
  - **With paid Claude plan (Pro/Team):** No API key needed - skills run within your Claude Code session
  - **Without Claude Code:** Anthropic API key required for standalone Python usage (AI job scoring)
  - **Recommendation:** Use Claude Code with paid plan for best experience
- **Microsoft Word or LibreOffice** (for .docx review)
- **Optional:** [Jobscan.co](https://www.jobscan.co/) account (for ATS optimization)

## Features

### 1. Job Discovery (job-hunter/)

Automates job board searches with intelligent filtering:

- Scrapes Indeed and Google Jobs using [python-jobspy](https://github.com/Bunsly/JobSpy)
- **Two-pass search:** Pass 1 scrapes remote roles nationwide; Pass 2 optionally scrapes local/hybrid roles near your commutable areas (configured in `config.py`)
- Filters by salary, job titles, domains, and negative keywords — all driven from `config.py`
- Scores jobs against your profile (0-100 technical + cultural fit)
- Checks company ratings (Indeed/Glassdoor)
- Identifies gaps to address in cover letter

**How python-jobspy is used:** The `job_hunter.py` script imports python-jobspy directly and calls its `scrape_jobs()` function with your search parameters. The library provides a unified interface to scrape job listings from multiple boards. No modifications to python-jobspy - we use it as a dependency.

**Job Sources - IP Ban Risk & Safety:**

| Source | Status | IP Ban Risk | Notes |
|--------|--------|-------------|-------|
| ✅ **Indeed** | **RECOMMENDED** | LOW | No rate limiting, designed for programmatic access, best scraper per JobSpy docs |
| ✅ **Google Jobs** | **RECOMMENDED** | LOW | Public API, safe to use, aggregates from multiple sources |
| ❌ **ZipRecruiter** | NOT RECOMMENDED | HIGH | Cloudflare 403 blocking, JobSpy struggles with this source |
| ❌ **LinkedIn** | NOT RECOMMENDED | HIGH | Rate limits around page 10, high IP ban risk after repeated scraping |

**Default Configuration:** The system defaults to Indeed and Google Jobs only (see `config-TEMPLATE.py`). These sources are designed for programmatic access and have LOW IP ban risk.

**Why avoid LinkedIn/ZipRecruiter:**
- LinkedIn aggressively rate-limits scraping (common 429 errors)
- ZipRecruiter uses Cloudflare protection (403 forbidden)
- Both may temporarily or permanently ban your IP address
- Risk not worth the marginal additional listings (Indeed/Google aggregate most postings)

### 2. Resume Optimization (.claude/skills/job-materials/)

AI-assisted customization with zero tolerance for hallucinations:

- Selects bullets from YOUR experience library (bullets-library.md)
- Optimizes for job posting keywords (combining bullets, adding accurate keywords)
- Retitles competency categories to match job terminology
- Enforces accuracy (no invented work, metrics, or technologies)
- Documents every optimization for transparency

**Optimization vs. Hallucination:**
- ✅ Combining related bullets for brevity (fits 2-page limit)
- ✅ Adding job-specific keywords if accurate ("and compliance")
- ✅ Retitling competencies to match job posting ("Device Lifecycle" vs "Security")
- ❌ Claiming job titles you never had
- ❌ Inventing work you never did
- ❌ Making up metrics or technologies

### 3. Cover Letter Generation

Professional, company-specific letters:

- Uses proven structure (opening, experience, strategic/hands-on, team development, culture fit, gap addressing)
- Addresses platform differences (ITSM Platform vs. PLATFORM_B, Enterprise Platform vs. Google Workspace)
- References company values from job posting
- Confident tone (not apologetic when addressing gaps)

### 4. Conversion Tools (docs/resume-files/tools/)

- `md-to-docx.py` - Convert markdown resume to formatted Word document
- `cover-letter-template.py` - Format cover letter for submission

### 5. Application Tracking (APPLICATION_TRACKER.md)

Organized pipeline:
- Discovery Pipeline (jobs scored, not yet applied)
- In Progress (materials being generated)
- Active Applications (submitted, awaiting response)
- Closed (rejected/withdrawn/accepted)

## Workflow

### Complete End-to-End (2-2.5 hours per application)

In Claude Code CLI:

```bash
# Run complete scrape pipeline (primary entry point)
/job-scraper

# Then create materials for a specific role
/job-apply
```

**What `/job-scraper` does:**
1. Scrapes job boards — Pass 1 remote nationwide, Pass 2 local/hybrid if configured (5-10 min)
2. Enhances with deduplication
3. Filters by your criteria (titles, salary, domains — all from config.py)
4. Scores filtered jobs against your candidate profile (AI-assisted)
5. Checks company ratings for high-scoring jobs
6. Reports results, adds 75+ scores to APPLICATION_TRACKER.md

**What `/job-apply` does:**
1. You choose which role to pursue
2. Generates resume + cover letter (30-35 min)
3. Documents all optimizations (materials-generation-log.md)
4. You review, convert to .docx, run Jobscan
5. Tracks in APPLICATION_TRACKER.md

### Quick Materials Only (30-45 minutes)

If you already found a job posting:

```bash
# Generate resume + cover letter for specific job
/job-materials
```

Paste job posting when prompted. System will:
- Analyze job requirements and gaps
- Select relevant bullets and competencies
- Generate optimized resume (markdown)
- Generate cover letter addressing gaps
- Document all selections and optimizations

Then convert to .docx and submit.

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 30-minute setup guide
- **[SETUP.md](SETUP.md)** - Detailed personalization steps
- **[docs/resume-files/CLAUDE.md](docs/resume-files/CLAUDE.md)** - Complete resume workflow
- **[job-hunter/CLAUDE.md](job-hunter/CLAUDE.md)** - Job discovery details
- **[.claude/skills/README.md](.claude/skills/README.md)** - Skills reference

## Architecture

### Key Design Decisions

**Markdown-First Workflow:**
- All editing in markdown (.md files)
- Convert to .docx for submission
- Version control friendly, diffable

**Hallucination Prevention:**
- All bullets from bullets-library.md (exact text)
- All competencies from competencies-library.md
- Quality checks verify no invented content
- Materials-generation-log.md documents every selection

**Optimization for Jobscan:**
- System optimizes TRUE content to be more scannable
- Adds accurate keywords, combines related bullets
- Retitles categories to match job posting
- Does NOT invent false content

### File Structure

```
claude-code-job-hunter/
├── .claude/skills/          # Claude Code skills
├── job-hunter/              # Job discovery scripts
├── docs/resume-files/       # Resume/cover letter system
│   ├── base-master/         # Your source of truth (templates)
│   ├── tools/               # Conversion scripts
│   └── [company-role]/      # Generated application materials
└── APPLICATION_TRACKER.md   # Application pipeline
```

## Customization

### For Your Resume

1. Copy template files in `docs/resume-files/base-master/`
2. Replace ALL `[PLACEHOLDER]` text with your information
3. See [SETUP.md](SETUP.md) for step-by-step guide

### For Your Job Search

1. Copy `job-hunter/config-TEMPLATE.py` → `config.py`
2. Set your location, job titles, salary, preferences
3. Copy `job-hunter/candidate_profile-TEMPLATE.md` → `candidate_profile.md`
4. Define your must-haves and scoring criteria

### For Your Industry

The system is designed for IT leadership roles but can be adapted:
- Update job search terms in `config.py`
- Modify competency categories in `competencies-library.md`
- Adjust skills to match your industry terminology
- Update cover letter structure in job-materials skill if needed

## FAQ

**Q: Does this work for non-IT roles?**
A: Yes, with customization. The structure works for any professional role - you'll need to update terminology, competencies, and bullet examples for your field.

**Q: How does it prevent hallucinations?**
A: Strict source file verification. All resume bullets MUST exist in bullets-library.md. All competencies MUST exist in competencies-library.md. The system optimizes (adds keywords, combines bullets) but never invents work you didn't do.

**Q: Do I need an Anthropic API key?**
A: **Not if you use Claude Code with a paid plan (Pro/Team).** The skills run within your Claude Code session using your existing subscription. You only need a separate API key if running the Python scripts standalone without Claude Code.

**Q: Can I use this without Claude Code?**
A: Partially. Job scraping works without Claude. Skills require Claude Code CLI. You could manually select bullets and create resumes, but you'd lose the AI assistance and optimization.

**Q: What's the difference between optimization and hallucination?**
A: Optimization = making TRUE content more scannable (combining bullets, adding accurate keywords). Hallucination = inventing FALSE content (fake job titles, made-up projects, invented metrics).

**Q: How accurate is job scoring?**
A: Depends on your candidate_profile.md specificity. More detailed profile = better scoring. Review scores manually - AI suggestions are helpful but not perfect.

## Troubleshooting

See [SETUP.md](SETUP.md) troubleshooting section for common issues.

## Contributing

This is a personal project shared for community benefit. If you'd like to contribute:
- Open issues for bugs or feature requests
- Submit PRs with improvements
- Share your success stories

## License

MIT License - see [LICENSE](LICENSE) for details.

## Credits

**Built with:**
- [Claude Code](https://github.com/anthropics/claude-code) by Anthropic
- [python-jobspy](https://github.com/Bunsly/JobSpy) for job scraping
- Microsoft Word/python-docx for document formatting
