---
name: job-materials
description: AI-assisted resume and cover letter generation with strict hallucination prevention
disable-model-invocation: true
version: 1.0.0
---

# Job Materials Generation Skill

**Purpose:** Generate customized resume and cover letter using base files as single source of truth with ZERO tolerance for hallucinations.

**Invocation:** User types `/job-materials`

---

## CRITICAL: Understanding Optimization vs Hallucination

### What IS Allowed (Jobscan Optimization)

✅ **Combining bullets for brevity**
- Example: Combining "MDM Platform/MDM Solution migration" + "Elevate deployment" into single bullet
- Reason: Fits 2-page limit, improves readability

✅ **Adding job-specific keywords (if accurate/true)**
- Example: Adding "and compliance" to EDR Solution bullet
- Example: Adding "Autopilot" to MDM Platform (if user has used it)
- Reason: Jobscan keyword matching

✅ **Modifying summary to emphasize job-relevant experience**
- Example: Reordering sentences, adding "high-growth environments" if job mentions this
- Reason: Keyword alignment with job posting

✅ **Retitling competency categories for job fit**
- Example: "Endpoint Management & Security" → "Endpoint Management & Device Lifecycle"
- Reason: Keyword alignment with job posting

✅ **Adding related technologies to competencies (if user has used them)**
- Example: Adding "VPN & Network Security" if job mentions VPN
- Reason: Explicit keyword matching

✅ **Changing non-technical phrasing for keyword matching**
- Example: "service desk" vs "helpdesk" (use job's terminology)
- Reason: Match job posting language

### What IS FORBIDDEN (Hallucinations)

❌ **Claiming job titles user never had**
- Example: Headline "Director of Information Technology" when title is "[Your Job Title]"
- Why forbidden: Dishonest, fails background check

❌ **Inventing work user never did**
- Example: Adding "Led ISO 27001 certification" if user didn't
- Why forbidden: Indefensible in interviews

❌ **Inventing metrics/numbers**
- Example: Adding "80% reduction" if you don't know the actual number
- Why forbidden: Unprovable, will be asked about

❌ **Adding technologies user never used**
- Example: Adding "Terraform" if user hasn't used it
- Why forbidden: Will be tested in interviews

**Key Principle:**
- **OPTIMIZATION** = Making true content more scannable/keyword-rich
- **HALLUCINATION** = Inventing content that isn't true

### Workflow Protocol

**BEFORE writing ANY content:**
1. Read `base-master/bullets-library.md` in FULL
2. Read `base-master/competencies-library.md` in FULL
3. Read `base-master/resume-base.md` for summary
4. Read a prior `[company-role]/resume.md` (if one exists) for optimization examples
5. Read a prior cover letter in `docs/resume-files/` for tone reference (if one exists)
6. Extract job keywords for optimization

**DURING content generation:**
- Select bullets from bullets-library.md, then OPTIMIZE (combine, add keywords if accurate)
- Select competencies, then OPTIMIZE (retitle categories, add tech if accurate)
- Modify summary to emphasize job-relevant experience
- Add job-specific keywords (if true)

**AFTER content generation:**
- Show user materials-generation-log.md with optimizations made
- Ask user to verify optimizations are accurate
- Document what was combined, what keywords were added

**ASK USER if uncertain about:**
- Whether user has used a specific technology
- Whether a metric is accurate
- Whether combining bullets loses important context
- Whether a keyword addition is truthful

**When uncertain:** ASK the user. Better to ask than to guess.

---

## Workflow

### Phase 1: Information Gathering

**Step 1.1: Prompt User for Inputs**

Ask user for:
1. **Job posting** - URL or paste full content
2. **Company name** - For folder naming and materials
3. **Role title** - Exact title from posting
4. **Generate what?** - Resume only / Cover letter only / Both

**Step 1.2: Read Source Files**

Read these files IN FULL before proceeding:

**Resume Sources:**
- `docs\resume-files\base-master\resume-base.md`
- `docs\resume-files\base-master\competencies-library.md`
- `docs\resume-files\base-master\bullets-library.md`

**Cover Letter Reference:**
- A prior cover letter from `docs\resume-files\` (if one exists — use for tone reference)

**Step 1.3: Fetch Job Posting (if URL provided)**

If user provided URL, use WebFetch to get job posting content.

**Step 1.4: Create Application Folder**

Run `create-application-folder.py` if it exists, otherwise create folder manually:
```bash
mkdir -p "docs\resume-files\[company-slug]-[role-slug]"
```

Folder naming: lowercase, hyphens, e.g., `acmecorp-director-of-engineering`

---

### Phase 2: Job Analysis

**Step 2.1: Analyze Job Requirements**

Extract from job posting:
1. **Must-have requirements** - What are non-negotiables?
2. **Nice-to-have requirements** - What's preferred but not required?
3. **Technologies mentioned** - List ALL technologies in posting
4. **Role level** - IC / Manager / Senior Manager / Director / VP?
5. **Focus areas** - Primary domains (Identity Management, cloud, endpoint, automation, workplace tech)?
6. **Reporting structure** - Who does role report to?
7. **Team size** - How many direct/indirect reports?

**Step 2.2: Gap Analysis**

Compare job requirements to user's base-master content:
1. **Technologies user lacks** - What's in posting but not in competencies-library?
2. **Experience gaps** - What job asks for that isn't in bullets-library?
3. **Title mismatch** - Job is Director but user is Manager?
4. **Industry/company type** - SaaS vs enterprise vs startup differences?

For each gap, determine:
- **Severity** - Dealbreaker / Important / Nice-to-have?
- **Bridging strategy** - How to position user's equivalent experience?

**Step 2.3: Cultural Analysis**

Extract from job posting:
1. **Company values** - What principles/values are mentioned?
2. **Leadership style** - What kind of leader are they looking for?
3. **Culture signals** - Formal vs casual? Scrappy vs structured?
4. **Mission/vision** - What problem does company solve?

**Step 2.4: Output Job Analysis**

Save to `[company-role]/job-posting.md`:
```markdown
# [Company] - [Role]

**Job URL:** [url]
**Date Analyzed:** [date]

## Requirements

### Must-Have
- Requirement 1
- Requirement 2

### Nice-to-Have
- Requirement 1
- Requirement 2

### Technologies Mentioned
- Tech 1
- Tech 2

## Gap Analysis

### Gap 1: [Technology/Experience]
- **Severity:** Dealbreaker / Important / Nice-to-have
- **What they want:** [Specific requirement]
- **What user has:** [Equivalent from base-master]
- **Bridging strategy:** [How to position]

[Repeat for each gap]

## Cultural Analysis

**Company Values:** [List]
**Leadership Style:** [Description]
**Culture:** [Formal/Casual, Scrappy/Structured]

## Recommendation

**Technical Fit:** X/10
**Cultural Fit:** X/10
**Overall:** STRONG / GOOD / MODERATE / WEAK

**Reasoning:** [Why this score]
```

---

### Phase 3: Resume Generation

**Only proceed if user requested resume generation.**

**Step 3.1: Select Headline**

Based on job focus areas from Phase 2, create headline:

**Format:** `"IT Leader | [Focus Area 1], [Focus Area 2] & [Focus Area 3]"`

**Examples:**
- Job focuses on Identity Management + cloud + automation → "IT Leader | Identity Management, Cloud Infrastructure & Automation"
- Job focuses on endpoint + Enterprise Platform + service delivery → "IT Leader | End User Services, Endpoint Management & Workplace Technology"
- Job focuses on security + compliance + Identity Management → "IT Leader | Cybersecurity, Compliance & Identity Governance"

**Rules:**
- ❌ DO NOT claim job title user doesn't have (e.g., don't say "Director of IT" if user is Manager)
- ✅ Use descriptive focus areas from user's actual experience
- ✅ Keep to 3 focus areas maximum

**Step 3.2: Optimize Summary for Job**

Read base-master/resume-base.md Professional Summary section.

**Task:** Modify summary to emphasize job-relevant experience and add keywords.

**Allowed Optimizations:**
- Reorder sentences to put most relevant experience first
- Add job-specific keywords if accurate (e.g., "high-growth environments" if job mentions this)
- Modify phrasing to match job terminology (e.g., "fast-paced SaaS environments")
- Emphasize relevant years of experience (e.g., "X+ years leading teams" for leadership role)

**Example:**
- Base: "Strategic [field] leader with [N]+ years managing [scope] operations..."
- Optimized: "Strategic [field] leader with [N]+ years in [scope] operations, including [Y]+ years leading teams in [job-relevant environment]..."
- Changes: Added job-relevant keyword, clarified management duration

**ASK user if:**
- Unsure if keyword is accurate (e.g., "SaaS experience" when user isn't in SaaS)
- Major rewrite needed (not just keyword additions)

**Step 3.3: Optimize Competency Categories for Job**

Read competencies-library.md in full.

Based on technologies mentioned in job posting, select 4-6 competency categories most relevant.

**Selection criteria:**
1. **Overlap** - How many technologies from job are in this category?
2. **Job focus** - Is this category central to role or peripheral?
3. **Gap bridging** - Does this category help bridge gaps identified in Phase 2?

**Allowed Optimizations:**

✅ **Retitle categories to match job keywords**
- Example: "Endpoint Management & Security" → "Endpoint Management & Device Lifecycle" (if job emphasizes device lifecycle)
- Example: "Leadership & Team Development" → "Leadership & Operations" (if job emphasizes operations)

✅ **Add job-relevant technologies to categories (if user has used them)**
- Example: Add "VPN & Network Security" if job mentions VPN
- Example: Add "Autopilot" to MDM Platform category if job mentions Autopilot
- **CRITICAL:** ASK user if uncertain whether they've used a technology

✅ **Reorder categories by job relevance**
- Leadership first for Director roles
- Technical first for IC roles
- Most job-relevant categories first

**Example (ExampleCompany):**
- Original category: "Endpoint Management & Security"
- Optimized: "IT Systems & Infrastructure" with added technologies: "VPN & Network Security"
- Reason: Job posting emphasized "systems management" and "VPN"

**Step 3.4: Select and Optimize Bullets for Job**

Read bullets-library.md in full.

**Selection targets:**
- **Current role ([Your Job Title]):** 7-9 bullets
- **Previous role ([Your Job Title]):** 3-4 bullets
- **[Your Job Title]:** 2-3 bullets
- **Helpdesk Associate:** 0-2 bullets (only if relevant to job)

**Selection criteria:**
1. **Technology overlap** - Bullet mentions tech from job posting
2. **Domain overlap** - Bullet's domain (Identity Management, cloud, endpoint) matches job focus
3. **Leadership level** - Bullet demonstrates leadership level matching job (IC vs Manager vs Director)
4. **Gap bridging** - Bullet helps bridge gaps identified in Phase 2
5. **Achievement scale** - Bullet shows impact appropriate for role level

**Allowed Optimizations (After Selection):**

✅ **Combine related bullets for brevity**
- Example: Combine "MDM Platform/MDM Solution migration" + "Elevate deployment" into single bullet
- Reason: Fits 2-page limit, reduces redundancy
- Document in materials-generation-log.md

✅ **Add job-specific keywords if accurate**
- Example: Add "and compliance" to EDR Solution bullet if job mentions compliance
- Example: Add "for distributed workforce" if job emphasizes distributed operations
- **CRITICAL:** Only add if truthful

✅ **Change terminology to match job posting**
- Example: "service desk" vs "helpdesk" (use job's term)
- Example: "business disruption" vs "disruption" (add context if job uses it)

**For each bullet, document:**
- Which bullets from bullets-library.md were used
- What optimizations were made (combined, keywords added)
- WHY selected (technology match, domain overlap, gap bridging)

**Example (ExampleCompany):**
- Selected: EDR Solution deployment (bullets-library.md line 17)
- Optimized: Added "and compliance" at end
- Reason: Job posting emphasized "compliance" keyword

**Category headers:**
- **Remove** if job is IC/Specialist role (Identity Management Engineer, Automation Engineer, etc.)
- **Keep** if job is Director+ managing multiple domains
- If uncertain, remove (safer choice)

**Step 3.5: Generate Resume Markdown**

Create `[company-role]/resume-v1.md`:

```markdown
# [YOUR NAME]

**[Selected Headline]**

**[YOUR_CITY, STATE] 02101**
**555-123-4567** | **jordan.smith@example.com**
**[linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)**

---

## PROFESSIONAL SUMMARY

[Copy from base-master, possibly reordered]

---

## CORE COMPETENCIES

**[Category 1]:** [All technologies from this category]

**[Category 2]:** [All technologies from this category]

[... 4-6 categories total]

---

## PROFESSIONAL EXPERIENCE

### [Your Job Title]
**[Your Current Company]** | [YOUR_CITY, STATE] (Remote) | [START_DATE] – Present

[Role description from base-master]

[If keeping category headers:]
**[Category Name]:**
- [Bullet 1]
- [Bullet 2]

**[Category Name]:**
- [Bullet 3]
- [Bullet 4]

[If removing category headers:]
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]
[... 7-9 bullets total]

### [Your Job Title]
**[Previous Company]** | [YOUR_CITY, STATE] | [START_DATE] – [END_DATE]

[Role description from base-master]

- [Bullet 1]
- [Bullet 2]
[... 3-4 bullets total]

### [Your Job Title]
**[Previous Company]** | [YOUR_CITY, STATE] | [START_DATE] – [END_DATE]

[Role description from base-master]

- [Bullet 1]
- [Bullet 2]
[... 2-3 bullets total]

### Helpdesk Associate (Contract to Level 2)
**[Previous Company]** | [YOUR_CITY, STATE] | [START_DATE] – [END_DATE]

[Role description from base-master]

[Only include if relevant to job - 0-2 bullets]

---

## EDUCATION

**Associate's Degree in Business Administration**
[COLLEGE_NAME], [CITY], [STATE] | Graduated [YEAR]
```

**Step 3.6: Create Materials Generation Log**

Create `[company-role]/materials-generation-log.md`:

```markdown
# Materials Generation Log
**Company:** [Company]
**Role:** [Role]
**Generated:** [Date]

## Resume Customization Decisions

### Headline Selected
**Headline:** "[Headline text]"
**Reasoning:** Job posting emphasizes [focus areas], which match user's experience in [areas from base-master].

### Summary
**Decision:** Kept original / Reordered sentences
**Reasoning:** [Why this approach]

### Competencies Selected (X categories)
1. **[Category 1]** - [Why selected]
2. **[Category 2]** - [Why selected]
[... list all]

**Categories NOT selected:**
- [Category X] - [Why not relevant to this job]

### Bullets Selected (X total)

**Current Role - [Your Job Title] (X bullets):**
1. "[Exact bullet text]"
   - **Why selected:** [Reason - tech overlap / domain match / gap bridging]
   - **Source:** bullets-library.md line [X]

[... list all bullets with reasoning]

**Previous Role - [Your Job Title] (X bullets):**
[... list all with reasoning]

**[Your Job Title] (X bullets):**
[... list all with reasoning]

**Helpdesk Associate (X bullets):**
[... list all with reasoning OR "Not included - not relevant to Director-level role"]

### Category Headers Decision
**Decision:** Kept / Removed
**Reasoning:** [Job is Director+ managing multiple domains / Job is IC specialist role]

## Quality Verification

**Resume Quality Checks:**
- [ ] All bullets verified in bullets-library.md (exact text match)
- [ ] All competencies verified in competencies-library.md
- [ ] Headline is descriptive (NOT claiming false job title)
- [ ] Job titles are ACTUAL titles ([Your Job Title], not modified)
- [ ] Summary from base-master (not modified or only reordered)
- [ ] No invented technologies or achievements

**Status:** PASS / FAIL

**Issues Found:** [List any issues or "None"]
```

---

### Phase 4: Cover Letter Generation

**Only proceed if user requested cover letter generation.**

**Step 4.1: Read Reference Cover Letter**

If the user has a prior cover letter saved in `docs/resume-files/`, read it in FULL.

Extract:
- **Tone** - Match the user's authentic voice (professional, confident)
- **Structure** - Note paragraph count and flow (opening, experience, strategic/hands-on, team dev, culture fit, gap addressing)
- **Phrasing patterns** - How achievements are described, how gaps are addressed

If no prior letter exists, ask the user: "Do you have a previous cover letter you'd like me to use as a tone reference? If not, I'll draft based on your resume and the SOP structure."

**Step 4.2: Generate Paragraph 1 - Opening**

**Template:**
"The [Role] role at [Company] caught my attention because [what makes it compelling]. [Establish credibility with relevant experience]."

**Example:**
"The [ROLE] role at [COMPANY] caught my attention because it's looking for someone who works both strategically and hands-on. That has been my approach to [YOUR FIELD] leadership throughout my career."

**What makes it compelling:** Extract from job posting (challenging problem, interesting tech stack, company mission, role scope)

**Credibility:** Reference user's years of experience and relevant domain from base-master

**Step 4.3: Generate Paragraph 2 - Experience Alignment + Gap Bridging (Optimized)**

**Purpose:** Address primary gap proactively while demonstrating relevant expertise.

**CRITICAL:** This paragraph requires OPTIMIZATION for gap bridging. Don't just copy templates - adapt to job-specific gaps.

**Structure:**
1. Acknowledge potential gap/concern directly (honest, not dismissive)
2. Explain platform-agnostic principles that transfer (with technical specifics)
3. Show depth of expertise with specific examples from bullets-library.md
4. Add adjacent experience if available (end-user familiarity, similar platforms)
5. Confident tone (not apologetic)

**Example (industry/category gap):**
"While [YOUR COMPANY] is not technically [THEIR CATEGORY], our operations have much in common with [THEIR ENVIRONMENT]: [specific shared characteristic 1], [shared characteristic 2], and [shared characteristic 3]. I have [specific achievement from bullets-library that demonstrates the relevant skill]..."

**Example from ExampleCompany (ITSM Platform vs. PLATFORM_B gap):**
"My ITSM platform experience centers on Atlassian Jira Service Management rather than ITSM Platform, but the fundamental principles are identical: both platforms implement ITIL best practices for incident, problem, change, and request management. I have built comprehensive PLATFORM_B ecosystems with AI-powered support automation, custom workflows, and API integrations that streamline service delivery. The same automation strategies, workflow orchestration patterns, and integration architectures I have applied to PLATFORM_B translate directly to ITSM Platform's platform."

**For this job:**
- Identify primary gap from Phase 2 analysis (ITSM Platform, Google Workspace, SaaS, industry, etc.)
- Select 2-3 bullets from bullets-library that demonstrate relevant expertise
- **OPTIMIZATION:** Add technical specifics that show transferability:
  - Platform gap → automation patterns, workflow orchestration, API integration
  - Cloud gap → IaC principles, automation, identity/access patterns
  - Domain gap → operational principles, support strategies, compliance rigor
- Reference specific technologies/achievements (ONLY from bullets-library)
- **OPTIMIZATION:** Add adjacent experience if available:
  - End-user familiarity with target platform
  - Similar platform experience (Jira → ITSM Platform, Enterprise Platform → Google Workspace)
  - Related domain (corporate IT → DC support via compliance/high-availability)
- Confident tone: "natural progression", "translate directly", not "I think I could"

**Document in cover-letter-generation-log.md:**
- Which gap addressed
- Which bullets from bullets-library referenced (include line numbers)
- What technical specifics used for transferability
- What adjacent experience added (verify accuracy)
- Effectiveness: STRONG / MODERATE / WEAK

**Step 4.4: Generate Paragraph 3 - Strategic/Hands-On Balance**

**Template:**
"I balance [tactical activities] with [strategic activities]. [Explain how staying hands-on improves strategic decisions]."

**Example:**
"I balance tactical work—architecture, automation, infrastructure-as-code—with strategic responsibilities like roadmapping and cross-functional collaboration. Staying close to the technology helps me make better decisions..."

**For this job:**
- Reference tactical work from bullets-library (architecture, automation, hands-on tech)
- Reference strategic work from bullets-library (roadmap, vendor mgmt, collaboration)
- Connect tactical to strategic (why hands-on matters for leadership)

**Step 4.5: Generate Paragraph 4 - Team Development**

**Template:**
"[Concrete before/after example of team development]. [Mentorship outcome]. [Culture of learning approach]."

**Example (use YOUR story from base-master or candidate_profile.md):**
"When I [inherited/took over/built] [team or function], I [what you changed — mindset, process, approach]. [Concrete outcome: a team member's growth, a metric, a before/after]. I give my team [your philosophy in their words]."

**For this job:**
- Use YOUR real team development story from bullets-library or candidate_profile.md
- Reference a specific mentorship outcome (role → role, not names)
- Show your culture of learning approach in your own words
- Keep example generic (don't use names)

**Step 4.6: Generate Paragraph 5 - Culture Fit**

**Template:**
"[Reference company values from job posting]. [Show company research]. [Demonstrate alignment with specific example]."

**Example:**
"Your leadership principles—'Find the shortest path' and 'Bias toward action'—resonate with my approach. Your investment in AI-powered customer engagement resonates strongly. I have adopted LLMs for development work, paired with code review requirements..."

**For this job:**
- Extract company values from job posting (Phase 2 cultural analysis)
- Show research (reference company's product, mission, or tech)
- Demonstrate alignment with specific example from user's experience

**If no values mentioned in posting:** Reference company mission or product focus.

**Step 4.7: Generate Paragraph 6 - Gap Addressing (REQUIRED for significant gaps)**

**When to include:** If Phase 2 identified significant technical gaps (platform differences, domain experience, etc.)

**Gap Types That REQUIRE Addressing:**

1. **Platform Differences (ITSM, Cloud, etc.):**
   - ITSM Platform vs. PLATFORM_B
   - Google Workspace vs. Enterprise Platform
   - AWS/GCP vs. Cloud Platform

2. **Domain Experience Gaps:**
   - No SaaS experience when job requires it
   - No distribution center/warehouse support when job requires it
   - No specific industry experience (retail, healthcare, finance)

3. **Technology Gaps:**
   - Job requires Terraform, user has CloudFormation
   - Job requires Kubernetes, user has Docker Swarm

**Template:**
"[Acknowledge gap candidly]. [Explain transferability with specifics]. [Add relevant adjacent experience]. [Express confidence, not apology]."

**Example (ExampleCompany - ITSM Platform vs. PLATFORM_B):**
```
My ITSM platform experience centers on Atlassian Jira Service Management rather
than ITSM Platform, but the fundamental principles are identical: both platforms
implement ITIL best practices for incident, problem, change, and request
management. I have built comprehensive PLATFORM_B ecosystems with AI-powered support
automation, custom workflows, and API integrations that streamline service
delivery. The same automation strategies, workflow orchestration patterns, and
integration architectures I have applied to PLATFORM_B translate directly to
ITSM Platform's platform. I have worked extensively with ITSM Platform's knowledge
base and ticketing systems as an end user and understand its capabilities -
transitioning to administering it would be a natural progression.
```

**Key Elements:**
1. ✅ **Acknowledge directly:** "My ITSM platform experience centers on Atlassian Jira Service Management rather than ITSM Platform"
2. ✅ **Bridge with principles:** "both platforms implement ITIL best practices"
3. ✅ **Show expertise depth:** Reference specific achievements from bullets-library.md
4. ✅ **Explain transferability:** "automation strategies, workflow orchestration patterns, integration architectures" (technical specifics)
5. ✅ **Add adjacent experience:** "worked extensively with ITSM Platform's knowledge base and ticketing systems as an end user"
6. ✅ **Confident tone:** "natural progression" (not "I think I could" or "I hope to")

**For this job:**
- Address 1-2 most significant gaps from Phase 2 analysis
- Use platform-agnostic principles (ITSM = ITIL, Cloud = IaC + automation, Identity Management = SSO + SCIM)
- Reference bullets from bullets-library.md that show relevant expertise
- Include adjacent experience (end-user familiarity, similar platforms, transferable domains)
- 4-6 sentences for major gaps, 2-3 sentences for minor gaps
- Confident tone (not apologetic)

**If no significant gaps:** Skip this paragraph.

**Step 4.8: Generate Closing**

**Template:**
"Thank you for your consideration. I look forward to discussing how my experience aligns with your needs."

**Keep closing generic and professional.**

**Step 4.9: Output Cover Letter Markdown**

Create `[company-role]/cover-letter-v1.md`:

```markdown
# Cover Letter - [Company] - [Role]

**Date:** [Date]

---

[YOUR_NAME]
[YOUR_CITY, STATE] 02101
555-123-4567
jordan.smith@example.com
linkedin.com/in/yourprofile

[Date]

Dear [Company] Hiring Team,

[Paragraph 1: Opening]

[Paragraph 2: Experience Alignment]

[Paragraph 3: Strategic/Hands-On Balance]

[Paragraph 4: Team Development]

[Paragraph 5: Culture Fit]

[Paragraph 6: Gap Addressing - if needed]

Thank you for your consideration. I look forward to discussing how my experience aligns with your needs.

Sincerely,

[YOUR_NAME]
```

**Step 4.10: Create Cover Letter Generation Log**

Create `[company-role]/cover-letter-generation-log.md`:

**CRITICAL:** Document EVERY optimization, gap bridging strategy, and bullet reference. This provides transparency and allows verification that nothing was hallucinated.

```markdown
# Cover Letter Generation Log
**Company:** [Company]
**Role:** [Role]
**Generated:** [Date]

## Cover Letter Structure & Optimization

### Paragraph 1: Opening (Optimized)

**Base Template (ExampleCompany v2):**
[Show template]

**Generated for [Company]:**
[Show actual paragraph]

**Optimizations Made:**
1. ✅ Emphasized job keywords: [list keywords added]
2. ✅ Matched job focus: [explain why this opening aligns]
3. ✅ Established credibility: [years of experience referenced]

**Verification:** [Confirm years/experience are accurate]

---

### Paragraph 2: Experience Alignment + Gap Bridging (Optimized)

**Purpose:** Address [gap name] proactively while demonstrating [domain] expertise

**Gap Identified (from job-posting.md):**
- **Gap:** [Description]
- **Bridge Strategy:** [How to address]

**Base Template (ExampleCompany v2):**
[Show template]

**Generated for [Company]:**
[Show actual paragraph]

**Optimizations Made:**
1. ✅ Acknowledged gap directly: [exact phrasing]
2. ✅ Bridged with principles: [platform-agnostic principles used]
3. ✅ Showed depth of expertise: Referenced bullets from bullets-library.md:
   - [Bullet description] (line X)
   - [Bullet description] (line Y)
4. ✅ Explained transferability: [what transfers across platforms]
5. ✅ Added adjacent experience: [end-user familiarity, related platforms]
6. ✅ Confident tone: [example phrasing - "natural progression", not "I hope to"]

**Verification:** All accurate
- [Bullet 1]: bullets-library.md line X
- [Bullet 2]: bullets-library.md line Y
- [Adjacent experience]: [confirm accuracy]

---

[REPEAT for Paragraphs 3, 4, 5, 6, 7 with same structure]

---

## Gap Bridging Summary

### Gap 1: [Gap Name] (ADDRESSED in Paragraph X)

**Gap:** [Description]
**Bridging Strategy:**
- ✅ Acknowledged directly: [how]
- ✅ Explained platform-agnostic principles: [which principles]
- ✅ Showed depth of expertise: [bullets referenced]
- ✅ Explained transferability: [what transfers]
- ✅ Added adjacent experience: [if any]
- ✅ Confident tone: [example phrasing]

**Effectiveness:** STRONG / MODERATE / WEAK - [explain]

[REPEAT for all gaps]

---

## Quality Verification

### Cover Letter Quality Checks:

**Structure:**
- ✅ X paragraphs (opening, experience + gap bridging, strategic/hands-on, team dev, culture fit, gap addressing if needed, closing)
- ✅ ExampleCompany v2 tone (professional, no contractions, confident)
- ✅ Specific achievements (all from bullets-library.md)

**Gap Addressing:**
- ✅ [Gap 1] - STRONG/MODERATE/WEAK bridging (paragraph X)
- ✅ [Gap 2] - STRONG/MODERATE/WEAK bridging (paragraph Y)
[... list all gaps]

**Accuracy:**
- ✅ All bullets referenced exist in bullets-library.md
- ✅ All technologies mentioned are in user's tech stack
- ✅ No invented work or metrics
- ✅ Mentorship outcomes are accurate
- ✅ [Compliance/certification claims] are accurate

**Tone:**
- ✅ Professional (no contractions)
- ✅ Confident (not apologetic when addressing gaps)
- ✅ Outcome-focused (business impact mentioned)
- ✅ Company research evident (company focus areas referenced)

**Word Count:** X words (target: 350-450 for Manager/Senior Manager, 450-550 for Director/Sr. Director)

**STATUS:** ✅ PASSED / ❌ FAILED - [explain]

---

## Optimizations Summary

**Paragraph 1 (Opening):**
- [List optimizations]

**Paragraph 2 ([Gap] Bridging):**
- [List optimizations]

**Paragraph 3 (Strategic/Hands-On):**
- [List optimizations, bullets referenced with line numbers]

**Paragraph 4 (Team Development):**
- [List optimizations, examples used]

**Paragraph 5 (Culture Fit):**
- [List optimizations, company research evident, bullets referenced]

**Paragraph 6 (Gap Addressing):**
- [List gaps addressed, bridging strategies]

**Paragraph 7 (Closing):**
- [Optimizations if any]

**Total Optimizations:** X optimizations across Y paragraphs, 0 hallucinations

---

## Files for [Company] Application

**Resume:** Use `resume-vX-optimized.md` / `.docx`
**Cover Letter:** Use `cover-letter-vX-optimized.md` (this version)
**Documentation:**
- `materials-generation-log-vX.md` (resume optimizations)
- `cover-letter-generation-log-vX.md` (cover letter optimizations + gap bridging)

**Next Steps:**
1. ✅ Review cover-letter-generation-log-vX.md (verify gap bridging strategy)
2. ⏳ Convert to .docx: `python tools/cover-letter-template.py --input cover-letter-vX-optimized.md`
3. ⏳ Upload resume to Jobscan (target 75%+)
4. ⏳ Submit application

---

**Log completed:** [Date]
**Version:** vX-optimized (with gap bridging documentation)
**Status:** Ready for .docx conversion and submission
```

**CRITICAL QUALITY CHECKS:**

**For EACH paragraph:**
1. Verify all bullets referenced exist in bullets-library.md (include line numbers)
2. Verify all technologies mentioned are in user's tech stack
3. Verify mentorship outcomes are accurate (not exaggerated)
4. Verify gap bridging is honest (acknowledges gap, doesn't minimize inappropriately)

**For gap bridging:**
1. Each gap MUST be from Phase 2 job-posting.md analysis
2. Bridge strategy MUST use platform-agnostic principles (not hand-waving)
3. Adjacent experience MUST be accurate (verify with user if uncertain)
4. Tone MUST be confident (not "I think I could" or "I hope to")

**Hallucination Prevention:**
- ❌ NEVER claim experience user doesn't have
- ❌ NEVER minimize significant gaps dishonestly
- ❌ NEVER reference bullets that don't exist in bullets-library.md
- ❌ NEVER invent mentorship outcomes
- ✅ ALWAYS verify adjacent experience claims (ask user if uncertain)
- [ ] Specific achievements referenced (from bullets-library only)
- [ ] Gaps addressed confidently (not apologetic)
- [ ] Company research evident (values/mission referenced)
- [ ] Word count 350-450

**Status:** PASS / FAIL

**Issues Found:** [List any issues or "None"]
```

---

### Phase 5: Quality Checks

**Step 5.1: Resume Quality Verification**

**For EACH bullet in resume-v1.md:**
1. Find source bullet(s) in bullets-library.md
2. Verify optimization is valid:
   - ✅ Combined related bullets? (Document in log)
   - ✅ Added job keywords? (Verify accuracy with user if uncertain)
   - ✅ Changed terminology to match job? (Verify truthful)
   - ❌ Invented new work? (FLAG - hallucination)
   - ❌ Invented metrics? (FLAG - hallucination)

**For EACH competency category in resume-v1.md:**
1. Find original category in competencies-library.md OR verify retitling is job-appropriate
2. Verify technologies:
   - ✅ Added job-relevant tech user has used? (Document in log, confirm with user if uncertain)
   - ❌ Added tech user never used? (FLAG - hallucination)

**For summary:**
1. Compare to base-master/resume-base.md summary
2. Verify optimization is valid:
   - ✅ Reordered sentences for relevance? (Document)
   - ✅ Added job keywords if accurate? (Verify with user)
   - ❌ Invented experience? (FLAG - hallucination)

**For headline:**
1. Verify it's descriptive (focus areas)
2. ❌ FLAG if claims job title user doesn't have ("Director" when user is "Manager")

**For job titles:**
1. Verify they match base-master exactly ([Your Job Title], etc.)
2. ❌ FLAG if any title modified

**Step 5.2: Cover Letter Quality Verification**

For tone:
1. Check for contractions (should be removed)
2. Verify professional voice (not apologetic)
3. Compare structure to ExampleCompany v2

For achievements:
1. Verify ALL achievements referenced are from bullets-library
2. Flag if any invented achievement

For gaps:
1. Verify gaps addressed are from Phase 2 analysis
2. Verify tone is confident, not apologetic

For company research:
1. Verify values/principles referenced are from job posting
2. Flag if generic (not company-specific)

For word count:
1. Count words
2. Flag if <300 or >500

**Step 5.3: Report Quality Check Results**

Display to user:

```
=== QUALITY CHECK RESULTS ===

RESUME:
✅ All bullets traced to bullets-library.md (X bullets, Y combined, Z keywords added)
✅ All competencies verified (X categories, Y retitled for job fit, Z technologies added)
✅ Headline is descriptive (not claiming false title)
✅ Job titles are actual titles (unchanged from base-master)
✅ Summary optimized for job (keywords: [list], reordered: [yes/no])
✅ No invented work, metrics, or technologies

OPTIMIZATIONS MADE:
- Combined bullets: [list pairs combined]
- Keywords added: [list additions with job relevance]
- Competency retitling: [list changes]
- Summary modifications: [list keyword additions]

COVER LETTER:
✅ Professional tone (ExampleCompany v2 style, no contractions)
✅ Specific achievements (all from bullets-library)
✅ Gaps addressed confidently (not apologetic)
✅ Company research evident ([X] values referenced)
✅ Word count: [X] words (target: 350-450)

STATUS: PASSED - Materials ready for conversion

[OR if issues found:]
STATUS: FAILED - Issues require attention

ISSUES FOUND:
❌ [Issue 1]
❌ [Issue 2]

Please review materials-generation-log.md for details.
```

**If FAILED:** Stop and ask user to review issues before proceeding.

**If PASSED:** Show user next steps.

---

### Phase 6: Next Steps Guidance

After quality checks PASS, guide user:

```
=== MATERIALS GENERATED SUCCESSFULLY ===

Files created:
- [company-role]/job-posting.md       (Job analysis)
- [company-role]/resume-v1.md         (Customized resume)
- [company-role]/cover-letter-v1.md   (Cover letter)
- [company-role]/materials-generation-log.md  (Selection reasoning)

NEXT STEPS:

1. Review materials-generation-log.md
   - Verify bullet selections make sense
   - Check reasoning for competency choices
   - Confirm gaps are addressed appropriately

2. Convert resume to .docx:
   cd docs\resume-files\[company-role]
   python ../tools/md-to-docx.py resume-v1.md

   This creates: resume-v1.docx

3. Verify 2-page limit:
   - Open resume-v1.docx in Word
   - Check page count (must be 2 pages max)
   - If over, remove lowest-priority bullets and regenerate

4. Jobscan optimization:
   - Upload resume-v1.docx to Jobscan.co
   - Paste job description
   - Target: 75%+ match score
   - Add missing keywords if accurate (don't force)
   - Regenerate .docx after keyword additions

5. Convert cover letter to .docx:
   python ../tools/cover-letter-template.py --input cover-letter-v1.md

   This creates: cover-letter-v1.docx

6. Final review:
   - Open both .docx files
   - Verify formatting is professional
   - Check for any errors
   - Ensure no placeholder text remains

7. Submit application:
   - Go to job posting URL
   - Upload resume-v1.docx
   - Upload cover-letter-v1.docx (if requested)
   - Fill out application form

8. Update APPLICATION_TRACKER.md:
   - Status: ✅ SUBMITTED
   - Date: [submission date]

TIME ESTIMATE:
- Review: 15-20 minutes
- Conversion: 2 minutes
- Jobscan: 30-45 minutes
- Submission: 15-30 minutes
Total: ~1-1.5 hours

MANUAL REVIEW REQUIRED:
You MUST verify no hallucinated content made it through.
Check bullets against base-master to be certain.
```

---

## Error Handling

### If Job Posting URL Fetch Fails

```
Unable to fetch job posting from URL.

Please paste the full job description below:
[Wait for user input]
```

### If Source Files Not Found

```
ERROR: Cannot find required source files.

Missing files:
- [file path 1]
- [file path 2]

Required file structure:
docs\resume-files\
├── base-master/
│   ├── resume-base.md
│   ├── competencies-library.md
│   └── bullets-library.md
└── [company-role]/               ← created when you run /job-apply
    └── Your_Name_Cover_Letter_CompanyName.md

Please ensure all source files exist before running /job-materials.
```

### If Quality Check Fails

```
❌ QUALITY CHECK FAILED

The following issues were detected:

RESUME:
[List issues found]

COVER LETTER:
[List issues found]

RECOMMENDATION:
These materials contain errors or potentially hallucinated content.
Do NOT proceed with conversion until issues are resolved.

Options:
1. Regenerate materials (I will fix the issues)
2. Manual review (you review materials-generation-log.md and decide)
3. Cancel (stop and investigate)

What would you like to do? (1/2/3)
```

### If User Finds Hallucinated Content

```
CRITICAL: Hallucination Detected

You found content that doesn't exist in source files.

This is a CRITICAL ERROR. The hallucination prevention system failed.

Immediately:
1. Delete generated files (resume-v1.md, cover-letter-v1.md)
2. Report this issue
3. Do NOT use these materials

I will regenerate from scratch with additional verification steps.

[Regenerate with triple-check system]
```

---

## Integration with Workflow

### Before This Skill (Manual Process)

1. Copy base-master/resume-base.md to job folder
2. Manually select bullets (2-3 hours)
3. Manually reorder competencies
4. Write cover letter from scratch (1-2 hours)
5. Total: 3-5 hours per application

### After This Skill (AI-Assisted)

1. Run `/job-materials` (10-15 minutes)
2. Review materials-generation-log.md (15-20 minutes)
3. Convert to .docx (2 minutes)
4. Jobscan optimization (30-45 minutes)
5. Total: 1-1.5 hours per application

**Time Savings:** 2-3.5 hours per application

---

## Success Criteria

**Resume Generated:**
- ✅ All bullets from bullets-library.md (exact text)
- ✅ All competencies from competencies-library.md
- ✅ Headline descriptive (not false title)
- ✅ 7-9 bullets current role, 3-4 previous roles
- ✅ Quality check PASSES

**Cover Letter Generated:**
- ✅ Professional tone (ExampleCompany v2 style)
- ✅ Company-specific (references values from posting)
- ✅ Gaps addressed confidently
- ✅ 350-450 words
- ✅ Quality check PASSES

**Materials Log Created:**
- ✅ Documents WHY each bullet selected
- ✅ Documents WHY each competency selected
- ✅ Documents gap bridging strategy
- ✅ User can verify reasoning

**No Hallucinations:**
- ✅ Zero invented bullets
- ✅ Zero invented technologies
- ✅ Zero modified bullet text
- ✅ Zero false title claims

---

## Version History

- **1.0.0** ([DATE]): Initial implementation
  - Resume generation with hallucination prevention
  - Cover letter generation (ExampleCompany v2 tone)
  - Quality checks with triple-verification
  - Materials generation log for transparency

---

**Last Updated:** [DATE]
**Status:** Active - Ready for use
