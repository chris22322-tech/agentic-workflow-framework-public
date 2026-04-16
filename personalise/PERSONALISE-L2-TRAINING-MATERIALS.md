# Personalise — Layer 2: Training Materials

**This is the only file you need to edit and run.** It contains your organisation details, instructions for the AI, and everything it needs to produce personalised training materials for your team's roles.

**Time:** 45–90 minutes of your attention (mostly reviewing output). The AI does ~5–10 minutes of work per role.
**Cost:** ~$1.00–3.00 per role (Claude Sonnet), ~$0.40–1.20 per role (Gemini Pro), or free tier on most providers.
**Output:** A set of markdown files at `personalise/output/learning/{role-name}/` for each role you specify.

---

## How to run this file

You have three options. Pick one. Each takes the same single document (this one) and runs it end-to-end. You do not need to paste anything else.

### Option 1 — Gemini CLI (you have `gemini` installed)

```bash
cd /path/to/your/framework/clone
gemini -y -p "$(cat personalise/PERSONALISE-L2-TRAINING-MATERIALS.md)"
```

The `-y` flag (YOLO mode) auto-approves the file-read tool calls Gemini needs to access the framework files referenced below. `-p` runs Gemini in non-interactive prompt mode. Verified with Gemini CLI v0.38.0 — output is written into `personalise/output/learning/`.

If you prefer to approve each file read interactively, drop the `-y` and respond to the prompts as they appear:

```bash
gemini -p "$(cat personalise/PERSONALISE-L2-TRAINING-MATERIALS.md)"
```

If you do not want to grant file-read access at all, use the web-browser option below instead.

### Option 2 — Claude Code CLI (you have `claude` installed)

```bash
cd /path/to/your/framework/clone
claude -p "$(cat personalise/PERSONALISE-L2-TRAINING-MATERIALS.md)" \
  --allowedTools Read,Write,Glob,Grep \
  --max-turns 30
```

### Option 3 — Web browser (no CLI required)

1. Open claude.ai, gemini.google.com, or chat.openai.com
2. Attach or paste the full contents of this file
3. Also attach or paste every file listed in the "**Files the AI must read**" section below
4. Send. The AI will reply with the training materials as markdown — copy each section into the appropriate file under `personalise/output/learning/`

---

## === SECTION 1: ABOUT YOUR ORGANISATION — EDIT THIS ===

**Fill in the fields below with your organisation details.** Delete the placeholder text. Leave a field blank (or write "N/A") if it does not apply. The more specific you are, the better the output.

### Organisation

- **Name:** <!-- e.g., "Acme Corp" -->
- **Description (1-2 sentences):** <!-- e.g., "Mid-sized insurance firm operating across UK commercial lines and personal lines." -->
- **Division / team:** <!-- e.g., "Claims Operations", "Customer Success", "Client Services" -->
- **Industry:** <!-- e.g., "Insurance", "Financial services", "SaaS", "Healthcare" -->

### Roles (list 2–5 roles on your team)

Training materials are generated **per role**. List every role you want learning paths for.

!!! tip "Aim for ~150 words per role — specific is better than generic"
    Vague descriptions produce vague output. Include time-of-day texture, exception cases, and the hardest recurring decisions. **Under ~100 words and the AI has to extrapolate, which produces generic training content that could apply to any insurance firm.**

1. **Role name:** <!-- e.g., "Senior Claims Adjuster" -->
   **What they do day-to-day (~150 words):** <!-- Include typical week rhythm, systems actually touched, exception cases, hardest recurring decisions. Example: "Handles complex claims above £25k. Morning: reviews new files in Guidewire, pulls claim history, contacts loss adjusters. Afternoon: reviews settlement recommendations from junior colleagues, signs off on £5k-£100k settlements, drafts letters, escalates to Head of Claims above £100k. Weekly: prepares complex-claims summary for senior leadership. Exception cases: reinsurance-triggering events, high-profile media claims requiring corporate comms, claims requiring physical site visits. Hardest recurring decisions: disputed liability on partial losses where physical evidence is contradictory." -->

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

### Team capability

- **Can your team build Stages 4–6 (engineering)?** <!-- yes / no / partial -->
- **Engineering support model:** <!-- e.g., "Dedicated platform team", "Shared data science team", "External consultants" -->

### Regulatory jurisdictions

- **Which jurisdictions apply?** <!-- e.g., "FCA (UK), EIOPA (EU)" or "None" -->
- **Data residency requirements:** <!-- e.g., "UK only", "EU only", "No restrictions" -->

### Governance cycle time

- **Typical review cycle for new AI / model deployments:** <!-- e.g., "8-12 weeks" or "2-4 weeks" or "minimal" -->
- **Approval authorities in your chain:** <!-- e.g., "DPO, CISO, Head of Compliance" -->

---

## === SECTION 2: INSTRUCTIONS FOR THE AI — DO NOT EDIT ===

You are producing personalised training materials for the organisation and roles described above. Your job is to read the framework methodology and produce a comprehensive learning path for **every role listed in Section 1** — using their actual workflows, systems, constraints, and responsibilities throughout. Do not use generic placeholders.

### Files the AI must read

Read each of these files from the repository. These paths are relative to the repo root (the directory containing this file's parent directory).

1. `docs/index.md` — framework home
2. `docs/framework-overview.md` — six stages summary
3. `docs/stages/01-decompose.md` — Stage 1 methodology
4. `docs/stages/02-select.md` — Stage 2 methodology
5. `docs/stages/03-scope.md` — Stage 3 methodology
6. `docs/worked-example/decompose.md` — structural reference for Stage 1 output
7. `docs/worked-example/select.md` — structural reference for Stage 2 output
8. `docs/worked-example/scope.md` — structural reference for Stage 3 output
9. `docs/getting-started/quick-start.md` — simplified entry point

**Before producing any output**, confirm that you have successfully read all files listed above. List the ones you read. If any file could not be read, note which ones and proceed with what you have.

**If you cannot read files directly** (interactive web chat, no file access): the user will paste these contents into the conversation. Work with whatever is provided. If files are missing, note which ones and proceed with what you have.

**Optional enrichment:** If `personalise/output/APPLICATION-GUIDE.md` exists (Layer 1 output), read it for richer org-specific context including role playbooks and quick wins.

### Output structure — produce these files for EVERY role in Section 1

For each role, write output to `personalise/output/learning/{role-name}/` where `{role-name}` is the role name in lowercase with spaces replaced by hyphens (e.g., `senior-claims-adjuster`).

**Do not ask the user any questions before producing the materials.** If Section 1 is missing a field, make a reasonable assumption and note it. Produce all materials in one pass.

#### For each role, produce these 8 files:

**1. `introduction.md` — Role-Specific Framework Orientation**

A 1-2 page introduction written directly to the person in this role. Cover:

- What the Agentic Workflow Framework is, in one paragraph — plain language, framed in terms of what it means for their daily work
- Why it matters for their specific role — connect to 2-3 of their workflows that are strong automation candidates
- What they will learn — the three non-technical stages (Decompose, Select, Scope) and what each produces
- What they will NOT need to do — they are not building agents or writing code
- A concrete example of the end state

Tone: direct, encouraging, practical. Not corporate training speak.

**2. `stage-1-walkthrough.md` — Guided Decompose Exercise**

A facilitator script that walks the person through Stage 1. Include:

- Warm-up (5 min): 3-5 example workflows from their domain as priming examples
- Four-angle enumeration (15 min): time-based, trigger-based, output-based, system-based — with role-specific examples for each, using systems from Section 1
- Filtering and validation (10 min): trigger/steps/output test, role-specific responsibilities-vs-workflows examples
- Scoring (10 min): four signals applied to 2-3 priming workflows as demonstration
- An embedded comprehension check (e.g., "Which of these is a workflow and which is a responsibility?")

Output: A completed Workflow Inventory Table template with 8+ workflows.

**3. `stage-2-walkthrough.md` — Guided Selection Exercise**

A facilitator script for Stage 2. Include:

- How to pick candidates from the inventory
- Each scoring dimension with role-specific guidance: what Impact means for this role, how to assess Feasibility given their systems
- A pre-populated scoring example for one of their workflows
- The weighted composite formula with a worked calculation
- An embedded comprehension check (e.g., "Is this score evidence-based or assumption-based?")

Output: A completed Selection Decision Record template.

**4. `stage-3-walkthrough.md` — Guided Scoping Exercise**

A facilitator script for Stage 3. Include:

- How to map the selected workflow step by step
- Guidance on automation boundaries (AUTOMATE vs HIL vs MANUAL) with role-specific examples
- How to build the data inventory using their org's actual systems
- A pre-populated partial scope map (3-5 steps) for one of their workflows
- An embedded comprehension check (e.g., "Is this step specific enough to define an automation boundary?")

Output: A completed Workflow Scope Document template.

**5. `worked-example.md` — Complete Stage 1-3 Walkthrough**

A full worked example using a specific workflow from this role. Select the workflow that is most representative and most likely to be a strong automation candidate. Follow the same structure and depth as the CSM health review example:

- Stage 1: Complete Workflow Inventory Table (8+ workflows across 3-4 responsibility areas)
- Stage 2: Full Selection Decision Record with candidate comparison, per-criterion scores, composite calculation
- Stage 3: Complete step-by-step workflow map with automation boundaries, data inventory, integration requirements

Use the org's actual systems and constraints throughout.

**6. `exercises.md` — Practice Exercises**

"Now do it yourself" exercises for each stage. Each exercise must have clear instructions, expected output description, and a self-check. Include:

- Stage 1: Complete your own inventory, split a compound workflow, map dependencies
- Stage 2: Score your top 3-4 candidates, calculate composites, apply the "when NOT to automate" checklist
- Stage 3: Map your workflow step by step (8+ steps), set automation boundaries, build the data inventory

**7. `calibration-exercises.md` — Calibration Exercises**

One per stage. Each presents a deliberately flawed artifact for the learner to critique before building their own:

- Stage 1: An inventory where some entries are responsibilities, not workflows. Learner identifies which are which.
- Stage 2: A scoring record with desire bias and familiarity bias. Learner identifies biased scores and re-scores.
- Stage 3: A scope document missing decision points, exception paths, and human/AI boundaries. Learner identifies gaps.

Each includes the flawed artifact, learner task, and reference answer with explanations.

**8. `assessment-rubric.md` — Quality Checklist**

A rubric for evaluating completed artifacts. For each stage:

- What "done well" looks like — with org-specific examples
- What "needs improvement" looks like — common gaps for this role
- Red flags — indicators of skipped steps or over-abstraction

### Additionally, produce one shared file:

**`personalise/output/learning/workshop/workshop-plan.md` — Team Workshop Plan**

A facilitated 2-hour workshop plan covering all roles. Include:

- Facilitator notes and preparation checklist
- Session breakdown with timing, activities, and materials needed
- Group exercises (cross-role) and individual exercises (role-specific)
- A spaced repetition schedule (micro-exercises at weeks 1, 2, and 4)
- A peer learning structure (buddy pairs who review each other's work)
- Common objections and how to handle them

### Output location

**Write all results to:** `personalise/output/learning/`

If you cannot write files (web chat mode), produce the markdown in your reply organised by file name and the user will save them manually.

### Quality bar

- **No generic placeholders.** Every mention of "your CRM" or "your system" must use the actual system name from Section 1.
- **No invented systems.** Do not mention systems that are not in Section 1.
- **No invented regulations.** Use only the jurisdictions listed in Section 1.
- **Role-specific, not generic.** Each role's materials must reflect their actual responsibilities, not generic knowledge-worker examples.
- **Structurally consistent.** Worked examples must match the depth and format of the CSM health review example in `docs/worked-example/`.
- **Facilitator-ready.** Scripts should be usable by someone who has read the framework but is not an expert.
- **Cite framework stages by name.** Tie recommendations to Stage 1 (Decompose), Stage 2 (Select), Stage 3 (Scope).

Begin now. Produce the full set of training materials for every role listed in Section 1, in one reply.
