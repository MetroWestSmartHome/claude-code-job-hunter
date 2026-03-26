# Detailed Setup Guide

Follow these steps to personalize the system with YOUR resume and preferences.

## Part 0: Job Search Configuration (5-10 minutes)

**CRITICAL:** Do this first - the job hunter reads your preferences from these files.

### Location: `job-hunter/`

### Step 1: Configure Search Parameters

```bash
cd job-hunter/
cp config-TEMPLATE.py config.py
```

Edit `config.py` and customize:

**Search terms:**
```python
"search_terms": [
    "YOUR JOB TITLE 1 remote",      # e.g., "IT Director remote"
    "YOUR JOB TITLE 2 remote",      # e.g., "Senior IT Manager remote"
    # Add 5-8 variations of your target roles
],
```

**Remote and local search:**
```python
"location": "United States",          # Country/region for remote search (Pass 1)
"distance_miles": 50,                 # Ignored for remote roles

# Pass 2: Local/hybrid search — set to True and add your towns if open to hybrid/on-site
"local_search_enabled": False,
"commutable_areas": [
    # "Your City, ST",      # Add towns within your commute radius
    # "Nearby Town, ST",
],
"local_distance_miles": 15,           # Tight radius per town
```

**Filtering criteria:**
```python
"min_salary": 123456,  # Your minimum acceptable salary

"target_titles": [
    "director", "manager", "head", "vp",
    # Leadership levels you want
],

"it_subspecialties": [
    "platform", "engineering", "operations",
    # Your domains (examples: 'security', 'data', 'cloud', 'devops')
],

"negative_keywords": [
    "helpdesk", "service desk",
    # Roles you want to avoid
],
```

### Step 2: Define Candidate Profile

```bash
cp candidate_profile-TEMPLATE.md candidate_profile.md
```

Edit `candidate_profile.md` and define:

**Must-haves (deal breakers):**
- Remote work required? (or hybrid acceptable?)
- Management level (IC / Manager / Director / VP)
- Minimum salary
- Preferred domains (SaaS, Enterprise, Healthcare, etc.)
- Tech stack alignment

**Negatives (automatic reject):**
- On-site only
- Contract/temporary
- Security clearance required
- Add your specific deal-breakers

**Scoring criteria:**
Define what matters most to you for the AI scoring (0-100 scale).

---

## Part 1: Resume Base Files (15-20 minutes)

### Location: `docs/resume-files/base-master/`

### Step 1: Copy Template Files

```bash
cd docs/resume-files/base-master/
cp resume-base-TEMPLATE.md resume-base.md
cp bullets-library-TEMPLATE.md bullets-library.md
cp competencies-library-TEMPLATE.md competencies-library.md
```

### Step 2: Personalize resume-base.md

Open `resume-base.md` and replace:

**Header:**
- `[YOUR_NAME]` → Your full name
- `[Your City, State] [ZIP]` → Your location
- `[Your Phone]` → Your phone number
- `[your.email@example.com]` → Your email
- `[linkedin.com/in/yourprofile]` → Your LinkedIn URL

**Professional Summary:**
- Replace entire paragraph with YOUR summary
- Keep to 3-5 sentences
- Focus on: years of experience, core domains, leadership approach

**Core Competencies:**
- Replace `[Competency Category 1]` with your actual categories
- Example: "Cloud Infrastructure & IaaS", "Identity Management"
- List YOUR technologies for each category

**Professional Experience:**
- Replace `[Your Current Role Title]` with your actual job title
- Replace company names, locations, dates
- Add YOUR actual work experience
- Keep to 7-9 bullets for current role, 3-4 for previous roles

**Education:**
- Replace with YOUR degrees, schools, graduation years

**Validation:** Search for `[` in the file - if any found, you missed a placeholder.

### Step 3: Personalize bullets-library.md

This file contains ALL your experience bullets organized by category.

**Structure:**
```markdown
## Current Role - [Your Title]

### Category 1
- Bullet 1
- Bullet 2

### Category 2
- Bullet 3
```

**Add YOUR bullets:**
- Use action verbs (Led, Architected, Implemented, Managed)
- Include metrics where possible (team size, % improvement, $ saved)
- Be specific about technologies used
- Focus on outcomes, not just tasks

**Why this file matters:**
- The `/job-materials` skill selects bullets from this library
- ALL resume bullets MUST exist in this file (hallucination prevention)
- Add more bullets than you'll use (library = comprehensive, resume = selective)

### Step 4: Personalize competencies-library.md

List ALL technologies you've used, organized by category.

**Example:**
```markdown
## Cloud Infrastructure & IaaS
Cloud Platform (IaaS/PaaS), AWS (EC2, S3, Lambda), Docker, Kubernetes, Terraform

## Identity Management
Enterprise IdP, Enterprise IdP, Identity Platform, SAML, OAuth 2.0, SCIM
```

**Why this file matters:**
- Skills select competencies from this library
- Prevents hallucinated technologies on resume

---

## Part 2: Job Search Configuration (5-10 minutes)

### Location: `job-hunter/`

### Step 1: Configure Search Parameters

```bash
cd job-hunter/
cp config-TEMPLATE.py config.py
```

Edit `config.py`:
1. Set your location and commute radius
2. List your target job titles
3. Set minimum salary
4. Configure remote preference

**Example:**
```python
"location": "United States",
"distance_miles": 50,
"search_terms": [
    "IT Director remote",
    "Senior IT Manager remote",
],
"min_salary": 100000,           # Your minimum
"local_search_enabled": False,  # Set True if open to hybrid/on-site
"commutable_areas": [],         # Add towns if local_search_enabled
```

### Step 2: Define Candidate Profile

```bash
cp candidate_profile-TEMPLATE.md candidate_profile.md
```

Edit `candidate_profile.md`:
1. List your must-haves (remote, management level, domains)
2. List your deal-breakers (on-site only, clearance required)
3. Define scoring criteria (what matters most to you?)

**Example:**
```markdown
## MUST HAVES
- Remote position (fully remote required)
- Management level (not individual contributor)
- Located in/open to Eastern US timezone

## STRONG POSITIVES
- Focus on [your domain]
- [Your tech stack]
- Salary range $XXk–$YYYk+

## NEGATIVES
- On-site/hybrid required
- Roles outside your expertise
- Contract/temp positions
```

---

## Part 3: Test & Verify (5 minutes)

### Test Job Discovery

```bash
cd job-hunter
python job_hunter.py --no-ai
```

Expected output: CSV file with job listings

### Test Materials Generation

In Claude Code CLI:
```bash
/job-materials
```

Paste a sample job posting (from Indeed or LinkedIn).

**Verify:**
- Resume generated with YOUR bullets
- No `[PLACEHOLDER]` text in output
- Cover letter uses YOUR name and experience

---

## Part 4: Create Resume Copy for Job Hunter (Optional)

The job hunter uses a copy of your resume for AI scoring.

**Option A: Create copy**
```bash
cp docs/resume-files/base-master/resume-base.md job-hunter/resume.txt
```

**Remember:** Update this copy whenever you update base-master/resume-base.md

**Option B: Symlink (Advanced - requires admin)**

On Windows (Scripting as admin):
```powershell
New-Item -ItemType SymbolicLink `
    -Path "job-hunter\resume.txt" `
    -Target "docs\resume-files\base-master\resume-base.md"
```

On Mac/Linux:
```bash
ln -s ../docs/resume-files/base-master/resume-base.md job-hunter/resume.txt
```

---

## Troubleshooting

### "Claude Code can't find skills"
- Ensure `.claude/skills/` directory is in your workspace root
- Run `claude --version` to verify Claude Code is installed
- Restart Claude Code session

### "Job scraping fails"
- Check `job-hunter/requirements.txt` is installed: `pip install -r job-hunter/requirements.txt`
- Verify internet connection
- Try `--no-ai` flag first to test scraping without Claude

### "Resume has placeholder text"
- Search files for `[` and `]` - replace all placeholders
- Common misses: phone number, email, LinkedIn URL
- Use find in editor: search for "[YOUR" or "[Your"

### "Materials generation fails"
- Verify all base files exist (no `-TEMPLATE` suffix)
- Check bullets-library.md is populated with YOUR bullets
- Ensure resume-base.md has your actual experience
- Verify no `[PLACEHOLDER]` text remains

### "Python version error"
- Check Python version: `python --version` (need 3.11+)
- Update Python if needed
- Create virtual environment if desired:
  ```bash
  python -m venv venv
  source venv/bin/activate  # Mac/Linux
  venv\Scripts\activate     # Windows
  ```

### "Anthropic API key errors"
- If using Claude Code with paid plan: **You don't need an API key**
- If running standalone: Set `ANTHROPIC_API_KEY` environment variable
- Or edit `config.py` to add key (less secure)

---

## Next Steps

1. ✅ Verify all placeholders replaced
2. ✅ Test job discovery
3. ✅ Test materials generation
4. ✅ Review generated resume/cover letter
5. ✅ Start using `/job-apply` for real job search

## Getting Help

- **Documentation:** See [docs/resume-files/CLAUDE.md](docs/resume-files/CLAUDE.md) for complete workflow
- **Job Discovery:** See [job-hunter/CLAUDE.md](job-hunter/CLAUDE.md) for details
- **Skills Reference:** See [.claude/skills/README.md](.claude/skills/README.md)

## Validation Checklist

Before starting your job search:

- [ ] All template files copied (no `-TEMPLATE` suffix)
- [ ] No `[PLACEHOLDER]` text in any file
- [ ] config.py has your location, job titles, salary
- [ ] candidate_profile.md reflects your actual preferences
- [ ] resume-base.md has your actual work history
- [ ] bullets-library.md has comprehensive bullet list
- [ ] competencies-library.md has all your technologies
- [ ] Job discovery test runs successfully
- [ ] Materials generation test produces valid output

Once complete, you're ready to start your AI-assisted job search!
