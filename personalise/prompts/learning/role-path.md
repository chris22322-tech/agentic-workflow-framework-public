# Role Learning Path Generator

You are producing a personalised learning path for a specific role adopting the
Agentic Workflow Framework. The learning path takes someone from "I've never
heard of this" to "I've completed my own Stage 1-3 artifacts" — using their
actual workflows, systems, and responsibilities throughout.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's context, roles, systems, constraints, and goals.
2. **Target role**: The user will specify which role from the org config to
   generate the learning path for. If not specified, ask.
3. **Framework stages 1-3**: Read `docs/stages/01-decompose.md`,
   `docs/stages/02-select.md`, and `docs/stages/03-scope.md` for the
   methodology the learning path teaches.
4. **Worked examples**: Read the worked example files in `docs/worked-example/`
   (decompose.md, select.md, scope.md) for structural reference — the learning
   path's worked example should follow the same format.
5. **Quick Start**: Read `docs/getting-started/quick-start.md` for the
   simplified entry point the learning path builds on.
6. **Application guide** (optional): If `personalise/output/APPLICATION-GUIDE.md`
   exists, read it for richer org-specific context including role playbooks and
   quick wins.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output Structure

Produce seven markdown files, one per section below. Every file must reference
the organisation's actual role title, systems, and workflows — not generic
placeholders. Write all output to `personalise/output/learning/{role-name}/`
where `{role-name}` is the role name in lowercase with spaces replaced by
hyphens (e.g., `account-manager`).

### 1. `introduction.md` — Role-Specific Framework Orientation

A 1-2 page introduction written directly to the person in this role. Cover:

- What the Agentic Workflow Framework is, in one paragraph — plain language, no
  jargon, framed in terms of what it means for their daily work
- Why it matters for their specific role — connect to 2-3 workflows they
  perform that are strong automation candidates (use the org config and
  application guide to identify these)
- What they will learn — the three non-technical stages (Decompose, Select,
  Scope) and what each one produces
- What they will NOT need to do — they are not building agents or writing code;
  they are identifying and defining the right workflows for automation
- A concrete example of the end state — "By the end of this learning path, you
  will have a complete inventory of your workflows, a scored selection of your
  best automation candidate, and a step-by-step scope document that an engineer
  can use to build your first agent"

Tone: direct, encouraging, practical. Not a corporate training introduction —
more like a capable colleague explaining why this is worth their time.

### 2. `stage-1-walkthrough.md` — Guided Decompose Exercise

A facilitator script that walks the person through Stage 1 (Decompose). Structure:

**Warm-up** (5 minutes)
- 3-5 example workflows from their domain pre-populated based on the org config
  role description and systems. These are priming examples, not the final
  inventory — frame them as "workflows people in your role commonly perform"
- Prompts to surface more: "What do you do every Monday morning?", "What report
  takes you the longest?", "What task do you procrastinate on because it's
  tedious, not because it's hard?"

**Four-angle enumeration** (15 minutes)
- Walk through each angle from Stage 1 (time-based, trigger-based, output-based,
  system-based) with role-specific examples for each angle
- Use the systems from the org config to populate the system-based angle

**Filtering and validation** (10 minutes)
- Apply the trigger/steps/output test to each candidate
- Role-specific examples of responsibilities vs workflows vs tasks for this role
- Guide them to split compound entries

**Scoring** (10 minutes)
- Apply the four signals (structural repeatability, determinism, data
  availability, error recoverability) to each workflow
- Pre-populated example scoring for 2-3 of the priming workflows so they can
  see the pattern before doing their own

**Output**: A completed Workflow Inventory Table with 8+ workflows.

### 3. `stage-2-walkthrough.md` — Guided Selection Exercise

A facilitator script for Stage 2 (Select). Structure:

- How to pick candidates from the inventory (High and Medium rated)
- Walk through each of the six scoring dimensions with role-specific guidance:
  what Impact means for this role, how to assess Feasibility given their systems,
  what Risk Tolerance looks like for their typical outputs
- A pre-populated scoring example for one workflow from their domain
- The weighted composite formula with a worked calculation
- Tiebreaker guidance and the "when NOT to automate" checklist applied to their
  context

**Output**: A completed Selection Decision Record.

### 4. `stage-3-walkthrough.md` — Guided Scoping Exercise

A facilitator script for Stage 3 (Scope). Structure:

- How to map their selected workflow step by step
- Guidance on setting automation boundaries (AUTOMATE vs HIL vs MANUAL) with
  examples relevant to their role and risk profile
- How to build the data inventory using their org's actual systems
- How to identify constraints and assumptions specific to their org
- A pre-populated partial scope map (3-5 steps) for one of their workflows to
  demonstrate the format before they do their own

**Output**: A completed Workflow Scope Document.

### 5. `worked-example.md` — Complete Stage 1-3 Walkthrough

A full worked example using a specific workflow from this role. Select the
workflow that is most representative of the role's work and most likely to be a
strong automation candidate based on the org config.

The worked example must follow the same structure and depth as the CSM health
review example in `docs/worked-example/`:

- **Stage 1 section**: Complete Workflow Inventory Table for the role (8+
  workflows across 3-4 responsibility areas) with annotations explaining scoring
  decisions
- **Stage 2 section**: Full Selection Decision Record with candidate comparison
  table, per-criterion scores with rationale, weighted composite calculation,
  justification, and risks
- **Stage 3 section**: Complete step-by-step workflow map with automation
  boundaries, data inventory, integration requirements, and constraints

Use the org's actual systems and constraints throughout. The worked example
should read as if it was written by someone who works at this organisation.

### 6. `exercises.md` — Practice Exercises

"Now do it yourself" exercises for each stage. Each exercise must have:

- Clear instructions (what to do)
- Expected output description (what "done" looks like — not just "fill in the
  table" but "a table with 8+ workflows, each with all columns populated, each
  scored High/Medium/Low with a brief rationale")
- A self-check (how to verify your own work)

**Stage 1 exercises:**
1. Complete your own Workflow Inventory Table
2. Identify at least one compound workflow and split it into sub-workflows
3. Map dependencies between your workflows

**Stage 2 exercises:**
1. Score your top 3-4 candidates across all six dimensions
2. Calculate weighted composites and identify your top candidate
3. Apply the "when NOT to automate" checklist to your shortlist

**Stage 3 exercises:**
1. Map your selected workflow step by step (minimum 8 steps)
2. Set automation boundaries for each step with justification
3. Build the data inventory for your workflow

### 7. `assessment-rubric.md` — Quality Checklist

A rubric for evaluating whether this role's completed artifacts meet the bar.
For each stage:

- **What "done well" looks like** — with org-specific examples (e.g., "Your
  inventory includes workflows that touch [system A] and [system B] from the org
  config, not just the obvious ones")
- **What "needs improvement" looks like** — common gaps for this role
- **Red flags** — indicators that the person skipped a step or abstracted too
  much (e.g., "Your inventory has fewer than 5 entries" or "Your scope document
  has no HIL steps — you either have a trivially simple workflow or you
  underestimated the judgement required")

Base the rubric on the guiding questions and common mistakes from each stage
file, adapted to this role's context.

## Quality Standards

- Every file must be self-contained — someone could read any single file without
  needing the others (though they build on each other)
- Role-specific examples must be realistic for the role described in the org
  config — not generic knowledge-worker examples
- The worked example must match the depth and structure of the CSM health review
  example in `docs/worked-example/`
- Facilitator scripts should be usable by someone who has read the framework but
  is not an expert — include enough context that they can run the exercise without
  additional preparation
- Do not use corporate training language ("In this module, learners will...").
  Write as if explaining to a colleague
