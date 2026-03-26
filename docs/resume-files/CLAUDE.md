# Resume Files - Project Instructions

## Application Tracking

**IMPORTANT:** Track all job applications in `APPLICATION_TRACKER.md`

**When to Update:**
- ✅ After submitting an application
- ✅ When creating materials for a new role (mark "In Progress")
- ✅ When deciding not to pursue a role (mark "Skipped" with reason)
- ✅ When receiving interview requests or rejections
- ✅ When accepting/declining offers

**What to Track:**
- Company, role title, salary range
- Application date and status
- Folder location and materials used
- Key details (fit assessment, gaps addressed)
- Next steps and outcomes

See `APPLICATION_TRACKER.md` for current status of all applications.

---

## Workflow Integration

### Job Discovery → Application Materials

**Source:** Jobs discovered via `../../job-hunter/` (automated) or manual (LinkedIn, referrals)

#### When Creating Application from job-hunter Match

1. **Scaffold application folder:**
   ```bash
   python tools/create-application-folder.py \
       --company "CompanyName" \
       --role "Job Title" \
       --url "https://posting-url" \
       --salary "XXX-YYYk" \
       --source "job-hunter"
   ```

2. **Verify job-posting.md** - Auto-populated from job-hunter or manual entry

3. **Customize resume.md** - Start from base-master copy

4. **Follow existing workflow** - Jobscan optimization → cover letter → submit

**Entry in APPLICATION_TRACKER.md will include:**
```markdown
**Source:** job-hunter (YYYY-MM-DD, score: 85/100)
```

### Candidate Profile Sync

**CRITICAL:** job-hunter uses a copy of your resume/profile for AI scoring.

**After updating base-master/resume-base.md, sync to job-hunter:**

**Option A: Manual sync**
```bash
cp base-master/resume-base.md ../../job-hunter/resume.txt
```

**Option B: One-time symlink** (admin Scripting)
```powershell
New-Item -ItemType SymbolicLink `
    -Path "job-hunter\resume.txt" `
    -Target "docs\resume-files\base-master\resume-base.md"
```

**Why this matters:** Out-of-sync resumes = inaccurate job scoring

---

## AI-Assisted Materials Generation

### The `/job-materials` Skill

**Purpose:** Generate customized resume and cover letter using base files as source of truth with ZERO tolerance for hallucinations.

**When to use:**
- Starting application for new job
- Want AI assistance with bullet/competency selection
- Need cover letter based on proven ExampleCompany v2 tone
- Want to save 2-3 hours of manual customization work

**Usage:**
```bash
/job-materials
```

**What it does:**
1. Reads job posting (URL or pasted content)
2. Analyzes requirements, focus areas, gaps, company culture
3. Generates customized resume from base-master (**NO hallucinations**)
4. Generates cover letter using ExampleCompany v2 reference tone
5. Enforces ALL accuracy rules (headlines ≠ titles, no invented content)
6. Shows you EXACTLY what was selected and WHY
7. Runs quality checks for hallucinations
8. Outputs markdown files (you convert to .docx)

**Critical Rules Enforced:**
- ✅ All bullets from `bullets-library.md` (exact text, no modifications)
- ✅ All competencies from `competencies-library.md`
- ✅ Headlines are descriptive (NOT claimed job titles)
- ✅ Job titles are actual titles only
- ✅ Summary from base-master only (unchanged or reordered)
- ❌ **ZERO hallucinations** - all content from base files

**Output Files:**
- `[company-role]/job-posting.md` - Job analysis with gap bridging strategy
- `[company-role]/resume-v1.md` - Customized resume (markdown)
- `[company-role]/cover-letter-v1.md` - Cover letter (markdown)
- `[company-role]/materials-generation-log.md` - Selection reasoning (WHY each bullet chosen)

**Next Steps:**
```bash
# Convert resume to .docx
python tools/md-to-docx.py [company-role]/resume-v1.md

# Convert cover letter to .docx
python tools/cover-letter-template.py --input [company-role]/cover-letter-v1.md

# Jobscan optimization (target 75%+)
# Upload resume-v1.docx + job description to Jobscan.co
```

**Manual Review Required:**
- ✅ Verify 2-page limit (open .docx)
- ✅ Check bullets match your actual experience
- ✅ Ensure no hallucinated content
- ✅ Verify gaps are addressed appropriately
- ✅ Confirm cover letter tone is professional
- ✅ Review `materials-generation-log.md` for selection reasoning

**Time Savings:**
- **Before:** 3-5 hours per application (fully manual)
- **After:** 1-1.5 hours (skill-assisted + review)
- **Savings:** 2-3.5 hours per application

**Quality Assurance:**
- Triple-check system verifies all content against source files
- Materials generation log documents WHY each item was selected
- Quality checks run automatically before completion
- User reviews log before converting to .docx

**See Also:** `.claude/skills/job-materials/SKILL.md` for complete implementation details

---

## CRITICAL RULES - NEVER VIOLATE

### 1. ZERO TOLERANCE FOR HALLUCINATIONS

**DO NOT EVER generate, infer, or assume resume content that doesn't exist in the source of truth.**

**Source of Truth:** `Your_Name_Resume_Base_Master.docx`

**What This Means:**

✅ **ALLOWED (Jobscan Optimization):**
- Combine related bullets for brevity (fits 2-page limit)
- Add job-specific keywords if accurate ("and compliance", "high-growth environments")
- Retitle competency categories to match job terminology
- Modify summary to emphasize job-relevant experience
- Change phrasing to match job posting language ("service desk" vs "helpdesk")

❌ **FORBIDDEN (Hallucinations):**
- Claim job titles you never had ("Director" when you're "Manager")
- Invent work you never did ("Led ISO 27001 certification")
- Invent metrics/numbers ("80% reduction" if you don't know the actual number)
- Add technologies you've never used ("Terraform" if you haven't used it)

✅ **ALWAYS:**
- Verify optimizations are accurate (ask if uncertain)
- Document what was combined, what keywords were added
- Check against `base-master/resume-base.md` or base master .docx

**Historical Context:**
In Feb 2026, Claude hallucinated a Platform SSO bullet point in `build_resume.js` (line 106-107) that combined elements from two separate real bullets and added false information about "Mac fleet device authentication." This created inaccurate resume content that could have been submitted to employers. This is **COMPLETELY UNACCEPTABLE** and must never happen again.

**Verification Protocol:**
Before writing ANY resume content:
1. Read `base-master/resume-base.md` or reference base master .docx
2. Verify EXACT wording exists in source
3. If combining/modifying bullets, get explicit user approval
4. If unsure, ask user rather than assume

### 2. Markdown-First Workflow

**ALL resume editing happens in markdown (.md), NEVER directly in .docx**

**Process:**
1. Edit `base-master/resume-base.md` (source of truth in markdown)
2. OR create job-specific variant in `job-folder/resume-v1.md`
3. Convert using `tools/md-to-docx.py`
4. Review .docx output for formatting

**Why:** Markdown is version-controllable, diffable, and prevents binary .docx corruption.

### 3. Base Master Contains EVERYTHING

**`base-master/resume-base.md` is comprehensive** - it has:
- ALL bullets from entire work history
- Category headers (Security & Identity Management, Infrastructure Modernization, etc.)
- More bullets than workshop recommends (that's intentional)

**Specialized variants consolidate** - they have:
- 5-7 bullets per role (workshop guidance)
- NO category headers (workshop says remove these)
- Headline added (workshop best practice)
- Content selected from base master only

### 4. Workshop Best Practices - Context Matters

**Workshop Guidelines:**
- 2 pages maximum
- 3-5 bullets per role (current role can have 5-7)
- Add headline below name
- Calibri 10-11pt font
- Success language: Led, managed, improved (avoid clichés)

**Category Headers - Contextual Decision:**

❌ **Remove categories for:**
- Specialist/IC roles (Identity Management Engineer, Automation Specialist, Security Analyst)
- Narrow-focus positions
- Tight 2-page constraints

✅ **Keep categories for:**
- Director/VP level roles (shows strategic organization)
- Multi-domain complexity (Security + Infrastructure + Operations)
- 10+ bullets that benefit from grouping
- Leadership positions managing multiple functional areas

**Base master keeps categories** - it's the comprehensive source.

**Specialized variants decide based on role level** - specialist roles remove, leadership roles may keep.

---

## File Structure

```
resume-files/
├── Your_Name_Resume_Base_Master.docx  ← SOURCE OF TRUTH (.docx)
├── base-master/
│   ├── resume-base.md                     ← SOURCE OF TRUTH (markdown)
│   ├── competencies-library.md
│   ├── bullets-library.md
│   └── README.md
├── tools/
│   ├── md-to-docx.py                      ← Markdown → .docx converter
│   └── README.md
├── best-practices-reference/
│   ├── WORKSHOP_BEST_PRACTICES.md
│   └── image.png ... image(10).png
├── it-leadership-generic/
├── iam-identity-specialist/
├── automation-devops-engineer/
├── azure-cloud-architect/
├── infosec-security-director/
├── base-master-comprehensive/
├── [company-role]/               ← your application folders go here
└── deprecated/
    ├── build_resume.js.backup             ← HALLUCINATED CONTENT
    ├── build_resume_v2_optimized.js.backup
    └── README.md
```

---

## Creating Job-Specific Resumes

### Step 1: Copy Base Master
```bash
cp base-master/resume-base.md newcompany-jobtitle/resume-v1.md
```

### Step 2: Add Headline (Workshop Requirement)
Below the name:
```markdown
# [YOUR_NAME]
**IT Leader | [Area of Focus from Job Description]**
```

Examples:
- "IT Leader | Cloud Infrastructure & Cybersecurity Operations"
- "Identity Management Architect"
- "Automation & DevOps Leader"

### Step 3: Customize Summary
Emphasize areas relevant to job posting.

### Step 4: Select Competencies
Copy relevant sections from `base-master/competencies-library.md`.

### Step 5: Consolidate Bullets (Workshop Guidance)
**Current role:** Select 5-7 most relevant bullets
**Previous roles:** Select 3-4 bullets each
**REMOVE category headers** (workshop says no sub-bullets/categories)

**CRITICAL:** Only select bullets that exist in base-master/resume-base.md. DO NOT create new bullets.

### Step 6: Convert to .docx
```bash
python tools/md-to-docx.py newcompany-jobtitle/resume-v1.md
```

### Step 7: Verify 2-Page Limit
Open .docx and check page count. If over 2 pages, remove lower-priority bullets.

---

## Jobscan Optimization

**Target:** 75%+ match score

**Process:**
1. Upload resume .docx to Jobscan
2. Paste job description
3. Review keyword gaps
4. Add missing keywords to markdown (verify they're accurate!)
5. Regenerate .docx
6. Rescan

**NEVER sacrifice honesty for match score** - if a keyword doesn't apply, don't force it.

---

## Cover Letters

**Process documented in:** `Cover_Letter_SOP.md`

**Key Points:**
- Address gaps (SaaS experience, Google Workspace, ISO 27001)
- Connect experience to job requirements
- Keep to 3-4 paragraphs
- Match resume's customization level

---

## Accuracy Requirements

### Headlines vs. Job Titles - CRITICAL DISTINCTION

**Headlines (below name):**
- ✅ Describe your professional identity/focus area
- ✅ Can include aspirational elements (e.g., "IT Leader & Architect")
- ✅ Should contain relevant keywords
- ❌ **MUST NOT claim job titles you don't hold**

**Good Headlines:**
- "Information Technology Leader & Architect | Cloud Infrastructure & Cybersecurity"
- "IT Leader | Enterprise Infrastructure & Team Development"
- "Identity Management Architect"

**BAD Headlines (claiming false titles):**
- ❌ "Director of Information Technology" (when you're [Your Job Title])
- ❌ "VP of IT Operations" (when you're a manager)
- ❌ "Chief Technology Officer" (when you're not C-level)

**Job Titles (in experience section):**
✅ Use ACTUAL titles only ([Your Job Title])
❌ Don't add false titles (e.g., "[Your Job Title] / Director")
❌ Don't modify titles to match job posting

### Experience Duration
✅ Use YOUR actual years — e.g., "X+ years in [field], Y+ years leading teams"
❌ Don't inflate tenure (e.g., "15 years managing" if only 7 were in management)

### Certifications & Compliance
✅ "Aligned with SOC 2/ISO 27001 control frameworks"
✅ "Maintained PCI and SOX compliance"
❌ "Implemented ISO 27001 certification" (not true)

### Verb Tenses
✅ Completed work = past tense ("Led", "Implemented")
✅ Ongoing work = present tense ("Architecting", "Driving")
❌ Mixing tenses incorrectly

### Project Scope
✅ "Led EDR Solution deployment for Enterprise IT"
❌ "Spearheaded company-wide EDR Solution deployment" (implies more scope than reality)

---

## Tools

### md-to-docx.py
**Purpose:** Convert markdown → Word .docx with proper formatting

**Usage:**
```bash
python tools/md-to-docx.py path/to/resume.md
```

**Output:** Creates `resume.docx` in same directory

**Formatting:**
- Calibri 10pt body, 11pt headers
- Margins: 0.5" top/bottom, 0.7" left/right
- Section headers: 11pt bold with bottom border
- Job titles: 11pt bold
- Job descriptions: 10pt italic
- Bullets: Word bullet format

---

## Deprecated Files

**`deprecated/build_resume.js.backup`** - CORRUPTED with hallucinated content
- Line 106-107: Hallucinated Platform SSO bullet combining Mac fleet authentication (false) with Ultron IDP (real)
- DO NOT USE as reference
- Kept for historical record only

**`deprecated/build_resume_v2_optimized.js.backup`** - ExampleCompany-specific hardcoded script
- Not reusable
- Built from corrupted build_resume.js
- Deprecated in favor of markdown workflow

---

## Interview Preparation

After customizing resume, prepare for common questions:

### ISO 27001 Experience
**Q:** "Do you have ISO 27001 certification experience?"
**A:** "I've maintained PCI and SOX compliance programs, which share many control frameworks with SOC 2 and ISO 27001—identity governance, access control, audit trails, security automation. My work aligns with those frameworks' principles, positioning me well to lead a formal certification program, though I haven't formally certified an environment to those standards yet."

### Leadership Experience
**Q:** "How long have you been in leadership?"
**A:** "[Fill in with YOUR honest answer] — e.g., 'I've been in [field] for X years. I've been formally leading teams for Y+ years in titled management roles, but even before that I was a peer mentor and technical lead.'"

### Project Ownership
**Q:** "Did you personally deploy [technology]?"
**A:** Be specific about hands-on vs. delegation. Example: "I led the EDR Solution deployment for Enterprise IT—made deployment strategy and management decisions, did a mix of hands-on work and delegation to my team."

---

**Last Updated:** [DATE]
**Status:** Infrastructure rebuilt, markdown-first workflow implemented
