# Quality Assessment Rubric Generator

You are producing a rubric for evaluating completed framework artifacts. The
rubric helps facilitators, champions, and reviewers assess whether someone's
Stage 1-3 outputs are "good enough" to proceed — or whether they need to go
back and improve specific areas.

The rubric is based on the framework's guiding questions and common mistakes,
adapted to the organisation's context.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's roles, systems, and constraints.
2. **Framework stages 1-3**: Read `docs/stages/01-decompose.md`,
   `docs/stages/02-select.md`, and `docs/stages/03-scope.md` — specifically
   the Guiding Questions and Common Mistakes sections.
3. **Worked examples**: Read `docs/worked-example/decompose.md`,
   `docs/worked-example/select.md`, and `docs/worked-example/scope.md` for
   reference of what "done well" looks like at full depth.
4. **Application guide** (optional): If `personalise/output/APPLICATION-GUIDE.md`
   exists, read it for role-specific context.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output

Write a single markdown file to `personalise/output/learning/assessment-rubric.md`.

## Output Structure

For each of the three stages, produce a rubric section with three tiers.
Adapt all examples and criteria to the organisation's roles and systems.

### Stage 1: Decompose — Workflow Inventory Table

**What "done well" looks like:**
- 8+ workflows across 3-4 responsibility areas
- Every row has all eight columns populated (no blanks in Trigger, Frequency,
  Avg Time, Systems Touched, or Output/Deliverable)
- Workflows reference the organisation's actual systems from the org config
  (e.g., "[CRM system]", "[project tracking tool]") — not generic system names
- At least one Medium-rated workflow has been considered for splitting into
  sub-workflows
- A Dependencies section is present, identifying shared data sources and
  sequential relationships
- Automation potential scores are distributed (not all High) with brief
  rationale for each

Generate 2-3 org-specific examples of what a good inventory entry looks like
for different roles in the org config.

**What "needs improvement" looks like:**
- Fewer than 6 workflows (probably still thinking in responsibilities, not
  workflows)
- Missing columns — especially Trigger (suggests the entry is a responsibility,
  not a workflow) or Systems Touched (needed for feasibility assessment in
  Stage 2)
- All workflows scored the same automation potential (usually all High — this
  means the scoring signals were not applied rigorously)
- No Dependencies section
- Workflows are too broad (each covering half a day or more of work) or too
  narrow (individual tasks rather than repeatable sequences)

**Red flags:**
- Fewer than 4 entries — the person either has a very narrow role or has not
  engaged with the four-angle enumeration
- No Medium or Low scores — every workflow scored High, which means the four
  signals were not applied (structural repeatability, determinism, data
  availability, error recoverability)
- Entries that fail the trigger/steps/output test: no identifiable trigger,
  no repeatable sequence, or no concrete output
- The inventory does not mention any system from the org config — the person
  may have completed it without considering their actual tooling

### Stage 2: Select — Selection Decision Record

**What "done well" looks like:**
- 3-4 candidates compared across all six dimensions with scores and rationale
- Weighted composite calculated correctly (check the arithmetic)
- The chosen workflow is justified with a one-paragraph explanation that
  references the scores, not just gut feel
- Known risks are identified and specific to the workflow
- At least one candidate was considered and rejected with a clear reason
- If two candidates scored within 0.5 points, the tiebreaker criteria were
  applied

Generate an example of a well-justified selection for a role in the org config.

**What "needs improvement" looks like:**
- Only one candidate scored (no comparison)
- Rationale does not reference the actual scores — it reads like a gut-feel
  justification written after the fact
- Impact score based on emotional pain ("this is the workflow I hate most")
  rather than the time formula (time × frequency × instances)
- Feasibility assumed without checking — the person scored 4 or 5 on a system
  they have not verified has an API
- Organisational Readiness scored without consulting the team that performs the
  workflow
- No risks identified (every workflow has risks)

**Red flags:**
- The chosen workflow is not the highest composite scorer and no explanation is
  given for why
- All six dimensions scored 4 or 5 — no differentiation suggests the scoring
  was not rigorous
- The workflow triggers a "when NOT to automate" disqualifier (value comes from
  the relationship, stakeholders would react negatively, data sources are
  inaccessible, workflow changes shape each time, team is actively hostile) and
  this was not addressed
- Impact score exceeds what the inventory data supports (e.g., scoring Impact 5
  for a workflow that runs monthly and takes 1 hour)

### Stage 3: Scope — Workflow Scope Document

**What "done well" looks like:**
- Step-by-step workflow map with 8+ steps in the standard table format
- Every step has a populated Decision Logic column — data retrieval steps
  include validation logic (what to check, what to do if data is missing), not
  just "None"
- Automation boundaries (AUTOMATE, HIL, MANUAL) are assigned to every step
  with reasoning
- At least one step is marked HIL (if nothing requires human judgement, the
  workflow is either trivially simple or the person underestimated the judgement
  required)
- At least one step is marked MANUAL (distribution, final approval, or similar)
- Data inventory covers every system mentioned in the workflow map
- Constraints and assumptions section addresses org-specific factors from the
  org config (regulatory requirements, data sensitivity, client-facing outputs)

Generate an example of a well-scoped step for a workflow relevant to the org.

**What "needs improvement" looks like:**
- Fewer than 6 steps (the workflow has not been decomposed enough — major steps
  are probably bundled together)
- Decision Logic column is empty or says "None" for most steps (even data
  retrieval steps should note what validation to perform)
- All steps marked AUTOMATE (no human judgement anywhere — either the workflow
  is trivial or the person did not consider where judgement is required)
- Data inventory is missing or incomplete (systems mentioned in the workflow
  map are not listed in the data inventory)
- No constraints section

**Red flags:**
- The scope document describes what the *agent* will do rather than what the
  *human currently does* — scoping maps the current workflow first, then draws
  the automation boundary. If the document starts with agent architecture, the
  person skipped scoping and jumped to design
- No HIL steps and the workflow involves qualitative assessment, sentiment
  analysis, or stakeholder-facing outputs — the person has likely underestimated
  the judgement required
- Steps that combine multiple distinct actions into one row (e.g., "Pull all
  data and analyse" — these should be separate steps)
- The data inventory lists systems but omits access method and auth requirements
  — this information is needed by the engineer in Stage 4

## Cross-Stage Quality Checks

Generate checks that span all three stages:

- **Consistency**: Do the systems mentioned in Stage 1 appear in Stage 3's data
  inventory? Does the Stage 2 selection match a workflow from Stage 1?
- **Traceability**: Can you trace from a Stage 1 inventory entry to a Stage 2
  selection to a Stage 3 scope document without gaps?
- **Realism**: Are the time estimates in Stage 1, the feasibility scores in
  Stage 2, and the integration requirements in Stage 3 internally consistent?
  (e.g., if Stage 2 scored Feasibility 4, Stage 3 should not reveal that a
  critical system has no API)

## Quality Standards

- The rubric must be specific enough that two reviewers evaluating the same
  artifact would reach similar conclusions
- Org-specific examples must reference actual systems and roles from the org
  config
- Red flags must be actionable — each one should tell the reviewer what the
  person needs to fix, not just that something is wrong
- The rubric should be usable by a champion or facilitator, not just by someone
  who wrote the framework
