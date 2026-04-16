# Personalise — Layer 1: Application Guide

**This is the only file you need to edit and run.** It contains your organisation details, instructions for the AI, and everything it needs to produce a tailored Application Guide for your team.

**Time:** 30–60 minutes of your attention (most of that is reviewing output). The AI does ~3–5 minutes of work.
**Cost:** ~$0.50 (Claude Sonnet), ~$0.20 (Gemini Pro), or free tier on most providers.
**Output:** A single markdown file at `personalise/output/APPLICATION-GUIDE.md`.

---

## How to run this file

You have three options. Pick one. Each takes the same single document (this one) and runs it end-to-end. You do not need to paste anything else.

### Option 1 — Gemini CLI (you have `gemini` installed)

```bash
cd /path/to/your/framework/clone
gemini -y -p "$(cat personalise/PERSONALISE-L1-APPLICATION-GUIDE.md)"
```

The `-y` flag (YOLO mode) auto-approves the file-read tool calls Gemini needs to access the framework files referenced below. `-p` runs Gemini in non-interactive prompt mode. Verified with Gemini CLI v0.38.0 — output is written directly to `personalise/output/APPLICATION-GUIDE.md`.

If you prefer to approve each file read interactively, drop the `-y` and respond to the prompts as they appear:

```bash
gemini -p "$(cat personalise/PERSONALISE-L1-APPLICATION-GUIDE.md)"
```

If you do not want to grant file-read access at all, use the web-browser option below instead.

### Option 2 — Claude Code CLI (you have `claude` installed)

```bash
cd /path/to/your/framework/clone
claude -p "$(cat personalise/PERSONALISE-L1-APPLICATION-GUIDE.md)" \
  --allowedTools Read,Write,Glob,Grep \
  --max-turns 25
```

### Option 3 — Web browser (no CLI required)

1. Open claude.ai, gemini.google.com, or chat.openai.com
2. Attach or paste the full contents of this file
3. Also attach or paste every file listed in the "**Files the AI must read**" section below
4. Send. The AI will reply with the application guide as markdown — copy it into `personalise/output/APPLICATION-GUIDE.md`

---

## === SECTION 1: ABOUT YOUR ORGANISATION — EDIT THIS ===

**Fill in the fields below with your organisation details.** Delete the placeholder text. Leave a field blank (or write "N/A") if it does not apply. The more specific you are, the better the output.

### Organisation

- **Name:** <!-- e.g., "Acme Corp" -->
- **Description (1-2 sentences):** <!-- e.g., "Mid-sized insurance firm operating across UK commercial lines and personal lines." -->
- **Division / team:** <!-- e.g., "Claims Operations", "Customer Success", "Client Services" -->
- **Industry:** <!-- e.g., "Insurance", "Financial services", "SaaS", "Healthcare" -->

### Roles (list 2–5 roles on your team)

!!! tip "Aim for ~150 words per role — specific is better than generic"
    Vague descriptions produce vague output. Include time-of-day texture, exception cases, and the hardest recurring decisions. A reader should understand the shape of a typical week for someone in this role. **Under ~100 words and the AI has to extrapolate, which is where hallucinations come from.**

1. **Role name:** <!-- e.g., "Senior Claims Adjuster" -->
   **What they do day-to-day (~150 words):** <!-- Example: "Handles complex claims above £25k. Morning: reviews new files in Guidewire, pulls claim history, and contacts loss adjusters or third-party witnesses to gather evidence on contested claims. Afternoon: reviews settlement recommendations from Claims Handlers, signs off on £5k-£100k settlements, drafts letters for larger claims, and escalates to Head of Claims above £100k. Weekly: prepares a complex-claims summary for senior leadership. Exception cases: reinsurance-triggering events, high-profile media claims requiring corporate comms, claims requiring physical site visits. Hardest recurring decisions: disputed liability on partial losses where the physical evidence is contradictory; settlement offers where the claimant has rejected the first two offers and the next step determines whether the case goes to litigation." -->

2. **Role name:**
   **What they do day-to-day (~150 words):**

3. **Role name:**
   **What they do day-to-day (~150 words):**

<!-- Add more roles below this line if needed -->

### Systems and tools (name the specific systems your team uses)

1. **System name:** <!-- e.g., "Guidewire ClaimCenter" -->
   **Purpose:** <!-- e.g., "Claims management — primary record, workflow, documents" -->
   **Does it have a REST or GraphQL API?** <!-- yes / no / don't know -->

2. **System name:**
   **Purpose:**
   **API available?**

3. **System name:**
   **Purpose:**
   **API available?**

<!-- Add more systems below this line if needed -->

### Constraints

- **Regulatory environment:** <!-- e.g., "FCA regulated UK insurer", "HIPAA", "SOX", "none" -->
- **Data sensitivity:** <!-- e.g., "Customer PII, claim details, medical records", "Internal only" -->
- **Client-facing outputs?** <!-- yes / no -->
- **Approval requirements:** <!-- e.g., "Senior adjuster sign-off on settlements above £50k" -->

### Goals

- **Primary goal for automation:** <!-- e.g., "Reduce time adjusters spend on triage and evidence collation" -->
- **Known target workflows (optional):** <!-- e.g., "Initial claim triage, fraud red-flag screening, settlement letter drafting" -->
- **Timeline:** <!-- e.g., "First working agent within 3 months" -->

### Team capability

- **Can your team build Stages 4–6 (engineering)?** <!-- yes / no / partial -->
- **Engineering support model:** <!-- e.g., "Dedicated platform team", "Shared data science team", "External consultants" -->
- **Existing automation:** <!-- e.g., "Rule-based routing in Guidewire, no ML", "None" -->

### Regulatory jurisdictions

- **Which jurisdictions apply?** <!-- e.g., "FCA (UK), EIOPA (EU)" or "None" -->
- **Data residency requirements:** <!-- e.g., "UK only", "EU only", "No restrictions" -->

### Governance cycle time

- **Typical review cycle for new AI / model deployments:** <!-- e.g., "8-12 weeks (DPO, CISO, third-party risk assessment, Head of Compliance sign-off)" or "2-4 weeks (lightweight internal AI governance only)" or "minimal — this is exploratory work" -->
- **Approval authorities in your chain:** <!-- e.g., "DPO, CISO, Head of Compliance, Board audit committee for material models" or "Head of team + tech lead" -->

---

## === SECTION 2: INSTRUCTIONS FOR THE AI — DO NOT EDIT ===

You are producing a tailored Application Guide for the organisation described above. Your job is to read the framework methodology and produce a comprehensive guide that is **specific** to this organisation — naming their systems, roles, constraints, and workflows throughout. Do not use generic placeholders like "your CRM" or "your support platform" — use the specific names from Section 1.

### Files the AI must read

Read each of these files from the repository. These paths are relative to the repo root (the directory containing this file's parent directory).

1. `docs/index.md` — framework home
2. `docs/framework-overview.md` — six stages summary
3. `docs/stages/01-decompose.md`
4. `docs/stages/02-select.md`
5. `docs/stages/03-scope.md`
6. `docs/stages/04-design.md`
7. `docs/stages/05-build.md`
8. `docs/stages/06-evaluate.md`
9. `docs/blank-templates/index.md`
10. `docs/worked-example/index.md` — reference for what "good" output looks like

**Before producing any output**, confirm that you have successfully read all files listed above. List the ones you read. If any file could not be read, note which ones and proceed with what you have.

**If you cannot read files directly** (interactive web chat, no file access): the user will paste these contents into the conversation. Work with whatever is provided. If files are missing, note which ones and proceed with what you have.

### Output structure — produce exactly these sections

Write the output as a single markdown document. **Do not ask the user any questions before producing the guide.** If Section 1 is missing a field, make a reasonable assumption and note it in an "Assumptions" line at the end of the guide. Produce the guide in one pass.

#### 1. Executive Summary (5–8 sentences)

- What the framework offers **this specific organisation** (name them)
- Which roles (by name from Section 1) benefit most immediately, and why
- What the quickest wins are — name specific workflows these roles actually do
- What the biggest risks are — name specific constraints from Section 1
- A one-sentence recommended starting point

#### 2. Recommended Rollout Plan (phased, realistic for this org's governance cycle)

**The rollout plan MUST reflect the governance cycle time stated in Section 1.** Do not default to a 3-month first-agent build for regulated industries. For environments with 8-12 week compliance cycles (FCA, PRA, HIPAA, SOX, etc.), Phase 2 cannot begin until Month 3 at the earliest, and Phase 3 should span Months 6-12. If Section 1 states a shorter cycle, scale accordingly.

- **Phase 1 (Month 1, parallel: file the compliance pack)** — which roles start, what they do each week, what artifacts they produce. In regulated environments: submit the initial compliance pack (the Stage 3 Scope Document, data flow diagram, and risk assessment) in parallel with Phase 1 work. Do NOT wait for Phase 1 to complete before engaging compliance.
- **Phase 2 (First Agent Build) — start month depends on Section 1's cycle time** — which workflow to build first and why. Name the systems and owning role from Section 1. Compute start month as: `Month 1 + ceil(governance cycle weeks ÷ 4)`. For 8-12 weeks this is Month 3-4; for 2-4 weeks this is Month 2.
- **Phase 3 (Expansion) — start month = Phase 2 end + buffer** — second and third workflows across the roles listed in Section 1. Allow 4 weeks between Phase 2 production go-live and Phase 3 kickoff for lessons-learned review.

Include a timeline table: month, milestone, active role(s), deliverables, **compliance gate status** (Not started / In flight / Approved).

#### 3. Role-Specific Playbooks

For **every role listed in Section 1**, produce a playbook containing:

- **Top 3 automation candidates** — specific workflows this role does, scored on the five Stage 2 signals (volume, pattern consistency, data availability, quality requirements, current time cost)
- **Which stages they own vs. collaborate on** — Stages 1-3 are thinking work, Stages 4-6 are engineering
- **Constraints that apply to this role** — from Section 1's constraints
- **Recommended first workflow** for this role, with justification

#### 4. Quick Wins (3–5 workflows)

3-5 workflows that could be automated in the first quarter with high confidence. For each:

- Workflow name and owning role (from Section 1)
- Why it's a quick win (high volume, internal-only, data readily available)
- Estimated time savings per occurrence
- Systems involved (from Section 1)
- Composite automation score (five Stage 2 signals)

#### 5. Data Sensitivity Analysis

For **every system listed in Section 1**:

- What data it contains (make a reasonable guess if not stated)
- Sensitivity classification (Public / Internal / Confidential / Restricted)
- Whether that data can be sent to external LLM APIs given Section 1's constraints
- If restricted: the alternative (on-prem model, redaction pipeline, manual step)

#### 6. Guardrails

Framework-neutral guardrails tailored to this organisation's regulatory environment and constraints. Cover HIL checkpoints, audit logging, prompt versioning, and the review gate between Stage 6 and production.

#### 7. Risk Register

5-10 risks specific to this organisation. For each: likelihood (H/M/L), impact (H/M/L), mitigation, owner.

#### 8. Recommended Next Actions (numbered, ≤10 items)

Concrete, time-bounded next steps the user can act on this week. Each item should name a specific person or role and a specific deliverable.

#### 9. Assumptions — REQUIRED (always produce this section)

You **must** end the output with an Assumptions section, even if your assumptions were minor. List every fact you inferred or extrapolated beyond what Section 1 explicitly stated. Format each assumption as a bullet: `**<thing assumed>:** <your reasoning>`. If an assumption is **load-bearing** (if it's wrong, the reader's decisions would change), prefix it with ⚠ to flag it.

Example format:

> - **Regulatory cycle duration:** Assumed 8-12 weeks for FCA approval based on typical UK insurance compliance practice. Used this to set Phase 2 timing.
> - ⚠ **Existing model risk management function:** Assumed the org has a model risk function that can sign off AI deployments. If not, Phase 3 extends by 3-4 months.
> - **External data access:** Assumed Guidewire API access is already provisioned for the engineering team. If not, add 2-3 weeks to Phase 2.

If you genuinely made no assumptions, write: `No assumptions — all content is grounded in Section 1 details.`

### Output location

**Write your result to:** `personalise/output/APPLICATION-GUIDE.md`

If you cannot write files (web chat mode), produce the markdown in your reply and the user will save it manually.

### Quality bar

- **No generic placeholders.** Every mention of "your CRM" must be replaced with the actual system name from Section 1. If you catch yourself writing generic text, stop and replace it.
- **No invented systems.** Do not mention systems that are not in Section 1.
- **No invented regulations.** Use only the jurisdictions listed in Section 1.
- **Cite framework stages by name.** When you recommend an action, tie it to Stage 1 (Decompose), Stage 2 (Select), Stage 3 (Scope), etc.

Begin now. Produce the full guide in one reply.
