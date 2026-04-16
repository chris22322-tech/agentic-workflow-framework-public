# Personalise — Layer 3: Custom Site

**This is the only file you need to edit and run.** It contains your organisation details, instructions for the AI, and everything it needs to generate a fully personalised version of this documentation site — with your org's name, roles, systems, and worked examples throughout.

**Time:** 60–120 minutes of your attention (mostly reviewing output). The AI does ~10–20 minutes of work.
**Cost:** ~$5.00–15.00 (Claude Sonnet), ~$2.00–6.00 (Gemini Pro), or free tier on most providers.
**Output:** A complete MkDocs site at `personalise/output/site/` that reads as if it was written for your organisation.

**Prerequisites:** Python 3.11+, and `pip install mkdocs mkdocs-material pyyaml` installed.

---

## How to run this file

You have three options. Pick one. Each takes the same single document (this one) and runs it end-to-end. You do not need to paste anything else.

### Option 1 — Gemini CLI (you have `gemini` installed)

```bash
cd /path/to/your/framework/clone
gemini -y -p "$(cat personalise/PERSONALISE-L3-CUSTOM-SITE.md)"
```

The `-y` flag (YOLO mode) auto-approves the file-read and file-write tool calls Gemini needs to produce the full site fork. `-p` runs Gemini in non-interactive prompt mode. Verified with Gemini CLI v0.38.0 — output is written into `personalise/output/site/`.

If you prefer to approve each tool call interactively, drop the `-y` and respond to the prompts as they appear:

```bash
gemini -p "$(cat personalise/PERSONALISE-L3-CUSTOM-SITE.md)"
```

If you do not want to grant tool access at all, use the web-browser option below instead — note that Layer 3 requires writing many files, so CLI mode is strongly preferred.

### Option 2 — Claude Code CLI (you have `claude` installed)

```bash
cd /path/to/your/framework/clone
claude -p "$(cat personalise/PERSONALISE-L3-CUSTOM-SITE.md)" \
  --allowedTools Read,Write,Glob,Grep,Bash \
  --max-turns 40
```

### Option 3 — Web browser (no CLI required)

1. Open claude.ai, gemini.google.com, or chat.openai.com
2. Attach or paste the full contents of this file
3. Also attach or paste every file listed in the "**Files the AI must read**" section below
4. Send. The AI will reply with the site files as markdown — copy each into the directory structure described in the output section

**Note:** Layer 3 produces many files. The CLI options (1 or 2) are strongly recommended as they write files directly. The web browser option works but requires manual file creation.

---

## === SECTION 1: ABOUT YOUR ORGANISATION — EDIT THIS ===

**Fill in the fields below with your organisation details.** Delete the placeholder text. Leave a field blank (or write "N/A") if it does not apply. The more specific you are, the more tailored the site.

### Organisation

- **Name:** <!-- e.g., "Acme Corp" -->
- **Description (1-2 sentences):** <!-- e.g., "Mid-sized insurance firm operating across UK commercial lines and personal lines." -->
- **Division / team:** <!-- e.g., "Claims Operations", "Customer Success", "Client Services" -->
- **Industry:** <!-- e.g., "Insurance", "Financial services", "SaaS", "Healthcare" -->
- **Site title (optional):** <!-- e.g., "Acme Claims Automation Playbook". Defaults to "{Name} Agentic Workflow Framework" -->

### Roles (list 2–5 roles on your team)

A worked example is generated for each role. More roles = higher cost.

!!! tip "Aim for ~150 words per role — specific is better than generic"
    Vague descriptions produce vague output. **Under ~100 words and the AI extrapolates, which is where hallucinations come from.** Include time-of-day texture, exception cases, and hardest recurring decisions.

1. **Role name:** <!-- e.g., "Senior Claims Adjuster" -->
   **What they do day-to-day (~150 words):** <!-- Include typical week rhythm, systems actually touched, exception cases, hardest recurring decisions. See PERSONALISE-L1-APPLICATION-GUIDE.md for a fully worked example. -->

2. **Role name:**
   **What they do day-to-day:**

3. **Role name:**
   **What they do day-to-day:**

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

- **Typical review cycle for new AI / model deployments:** <!-- e.g., "8-12 weeks" or "2-4 weeks" or "minimal" -->
- **Approval authorities in your chain:** <!-- e.g., "DPO, CISO, Head of Compliance" -->

### Domain-specific terms (optional, 3–10 terms)

List terms specific to your industry or organisation that should appear in the site glossary.

1. <!-- e.g., "FNOL — First Notification of Loss: the initial report of a claim" -->
2. <!-- e.g., "Subrogation — recovering costs from a third party after paying a claim" -->
3. <!-- e.g., "TPA — Third Party Administrator: external claims handling partner" -->

---

## === SECTION 2: INSTRUCTIONS FOR THE AI — DO NOT EDIT ===

You are producing a personalised version of the Agentic Workflow Framework documentation site for the organisation described above. The six-stage methodology is universal and stays unchanged. Everything around it adapts to this organisation's context.

### Files the AI must read

Read each of these files from the repository. These paths are relative to the repo root.

**Core framework (do not modify — copy as-is into the output site):**

1. `docs/index.md` — framework home
2. `docs/framework-overview.md` — six stages summary
3. `docs/stages/01-decompose.md`
4. `docs/stages/02-select.md`
5. `docs/stages/03-scope.md`
6. `docs/stages/04-design.md`
7. `docs/stages/05-build.md`
8. `docs/stages/06-evaluate.md`
9. `docs/stages/index.md`

**Reference materials (read for context, then personalise):**

10. `docs/getting-started/index.md`
11. `docs/getting-started/quick-start.md`
12. `docs/getting-started/prerequisites.md`
13. `docs/worked-example/index.md`
14. `docs/worked-example/decompose.md`
15. `docs/worked-example/select.md`
16. `docs/worked-example/scope.md`
17. `docs/worked-example/design.md`
18. `docs/worked-example/evaluate.md`
19. `docs/worked-example/build.md`
20. `docs/reference/glossary.md`
21. `docs/reference/decision-trees.md`
22. `docs/reference/checklist.md`
23. `docs/blank-templates/index.md`

**Site configuration:**

24. `mkdocs.yml` — site structure and navigation

**Before producing any output**, confirm that you have successfully read all files listed above. List the ones you read. If any file could not be read, note which ones and proceed with what you have.

**If you cannot read files directly** (interactive web chat, no file access): the user will paste these contents into the conversation. Work with whatever is provided.

### What to personalise

| Section | Action | Details |
|---|---|---|
| **Getting Started** | Partially personalise | Add org-specific role descriptions to "Who it's for". Add org's systems to prerequisites. |
| **Stages 1-6** | Copy unchanged | Methodology is universal. Do not modify. |
| **Worked Examples** | Add new examples | Keep the generic CSM example. Add one new worked example per role from Section 1, following the same structure. |
| **Templates** | Partially personalise | Pre-fill "Systems Touched" columns, Data Inventory "Data Source" columns, and Integration Requirements with the org's systems. |
| **Glossary** | Extend | Add domain-specific terms from Section 1 alongside the generic terms. |
| **Decision Trees** | Extend | Add org-specific constraints as early gates (e.g., regulatory checks, data sensitivity checks). |
| **Checklist** | Extend | Add org-specific checklist items per stage. |
| **Quick Start** | Partially personalise | Replace the mini-example with one using an org-specific role and workflow. |

### Output structure

Create a complete MkDocs site at `personalise/output/site/` with this structure:

```
personalise/output/site/
├── mkdocs.yml                    (adapted from root mkdocs.yml, with org name in title and nav updated)
├── docs/
│   ├── index.md                  (personalised home page with org name)
│   ├── framework-overview.md     (copied unchanged)
│   ├── getting-started/
│   │   ├── index.md              (personalised)
│   │   ├── quick-start.md        (personalised mini-example)
│   │   └── prerequisites.md      (personalised with org systems)
│   ├── stages/
│   │   ├── index.md              (copied unchanged)
│   │   ├── 01-decompose.md       (copied unchanged)
│   │   ├── 02-select.md          (copied unchanged)
│   │   ├── 03-scope.md           (copied unchanged)
│   │   ├── 04-design.md          (copied unchanged)
│   │   ├── 05-build.md           (copied unchanged)
│   │   └── 06-evaluate.md        (copied unchanged)
│   ├── worked-example/
│   │   ├── index.md              (updated to list both generic and org-specific examples)
│   │   ├── decompose.md          (generic — copied unchanged)
│   │   ├── select.md             (generic — copied unchanged)
│   │   ├── scope.md              (generic — copied unchanged)
│   │   ├── design.md             (generic — copied unchanged)
│   │   ├── evaluate.md           (generic — copied unchanged)
│   │   ├── build.md              (generic — copied unchanged)
│   │   └── {role-name}/          (one directory per role from Section 1)
│   │       ├── decompose.md
│   │       ├── select.md
│   │       └── scope.md
│   ├── reference/
│   │   ├── glossary.md           (extended with org terms)
│   │   ├── decision-trees.md     (extended with org constraints)
│   │   └── checklist.md          (extended with org items)
│   └── blank-templates/
│       └── index.md              (pre-filled with org systems)
└── .framework-version            (hash of the upstream framework version for drift detection)
```

### How to produce each personalised section

**Home page (`docs/index.md`):**
Replace generic descriptions with org-specific framing. The site title should use the org name (or the custom site title from Section 1). Keep the framework's value proposition but frame it for this organisation's industry and goals.

**Worked examples (per role):**
For each role in Section 1, produce a Stage 1-3 worked example following the same structure and depth as the CSM health review example. Select the most representative workflow for each role. Use the org's actual systems, constraints, and terminology throughout.

**Templates (`docs/blank-templates/index.md`):**
Pre-fill system-dependent fields with the org's systems from Section 1. Leave role-dependent and workflow-dependent fields blank for the user to fill.

**Glossary (`docs/reference/glossary.md`):**
Copy all existing generic terms. Add a "Domain-Specific Terms" section with the terms from Section 1 (and any additional terms implied by the org's industry and systems).

**Decision trees (`docs/reference/decision-trees.md`):**
Add org-specific early gates. For example, if the org is FCA regulated, add a "Does this workflow handle regulated data?" gate before the feasibility assessment.

**Checklist (`docs/reference/checklist.md`):**
Add org-specific checklist items under each stage. For example, Stage 3 might gain "Verify data residency requirements for each system in the data inventory" if the org has data residency constraints.

**`.framework-version` file:**
Write a single line containing the git commit hash of the current framework version (or "manual" if git is not available).

### After writing all files

If you have shell access, build and verify the site:

```bash
cd personalise/output/site/
pip install mkdocs mkdocs-material --quiet
mkdocs build --strict 2>&1
```

Report any build errors. If the site builds cleanly, note this in your output.

### Output location

**Write all results to:** `personalise/output/site/`

If you cannot write files (web chat mode), produce the key personalised files in your reply (home page, one worked example, glossary, decision trees, checklist, templates) and note which files should be copied unchanged from the original site. The user will assemble the site manually.

### Quality bar

- **No generic placeholders.** Use the actual org name, system names, role titles from Section 1 throughout.
- **No invented systems or regulations.** Only reference what is in Section 1.
- **Methodology unchanged.** The six stage files must be copied exactly — do not rewrite the methodology.
- **Worked examples must match reference depth.** Each role's worked example should be as detailed as the CSM health review in `docs/worked-example/`.
- **Site must build.** The output must be a valid MkDocs site with no broken internal links.
- **Cite framework stages by name.** When referencing the methodology, use Stage 1 (Decompose), Stage 2 (Select), etc.

Begin now. Produce the full personalised site for the organisation described in Section 1.
