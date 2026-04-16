# Worked Example Customisation Prompt

You are producing a complete Stage 1-6 worked example for a specific role in an
organisation. The output follows the same structure and depth as the generic
worked examples in this framework — but tailored to the role, workflows, systems,
and constraints described in the organisation config.

This prompt is called once per role by the fork script. The output becomes a new
worked example section in the personalised site.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's context, systems, and constraints.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for role playbooks, quick wins, and recommended first workflows.
3. **Role**: The role to generate the worked example for. Use the role name and
   description from the org config.
4. **Framework stages**: Read all files in `docs/stages/` (01-decompose.md
   through 06-evaluate.md) for the methodology and artifact structure.
5. **Reference worked example**: Read the CSM worked example in
   `docs/worked-example/` (decompose.md, select.md, scope.md, design.md,
   build.md, evaluate.md) for structural reference. Your output must match this
   level of detail.

## Output Structure

Produce six markdown files — one per stage — in the output directory specified
by the caller. Each file must follow the same structure as the corresponding
file in `docs/worked-example/`.

### File 1: `decompose.md` — Stage 1

Produce a complete Workflow Inventory Table for the role:

- Cover 8+ workflows across 3-4 responsibility areas
- Include all eight columns: Responsibility Area, Workflow, Trigger, Frequency,
  Avg Time (hrs), Systems Touched, Output/Deliverable, Automation Potential
- Score each workflow's automation potential (High/Medium/Low)
- Use the org's actual system names from the config

Add annotations (using `!!! note` admonitions) explaining:
- Why High-scoring workflows share common traits
- Why at least one workflow scored Low (to show contrast)
- Patterns and dependencies between workflows

### File 2: `select.md` — Stage 2

Produce a complete Selection Decision Record:

- Candidate comparison table scoring top 4 candidates on all six dimensions
  (Impact, Feasibility, Risk Tolerance, Complexity, Learning Value,
  Organisational Readiness) with weighted composite scores
- Per-criterion scoring with weight, score (1-5), and rationale paragraphs
  referencing the org's actual systems and constraints
- Weighted score calculation with the formula and actual numbers
- Justification paragraph for the chosen workflow
- Risks section specific to this workflow and org

### File 3: `scope.md` — Stage 3

Produce a complete Workflow Scope Document:

- Step-by-step workflow map with minimum 10 steps in the standard table format
  (Step #, Step Name, Action, Input, Output, Decision Logic, Boundary)
- Every step must have a populated Decision Logic column
- Each step marked AUTOMATE, HIL, or MANUAL with reasoning
- Data inventory with access method, format, auth, notes
- Integration requirements for the engineer
- Constraints and assumptions from the org config
- Error Path Register for failure modes

### File 4: `design.md` — Stage 4

Produce a Design Document:

- Scope-to-action mapping table (every scope step mapped to an action in the flow)
- Flow diagram (Mermaid) showing actions, routing, and HIL checkpoints
- Memory schema with typed fields
- Action specifications: purpose, tools, logic summary, prompt pattern
- HIL checkpoint specifications
- Error handling strategy

### File 5: `build.md` — Stage 5 (STUB — 20-40 lines max)

**Stage 5 is deliberately a stub page.** The generic [Stage 5: Build](../stages/05-build.md) methodology applies universally regardless of role or organisation — project structure, code layout, prompt externalisation principles, and testing strategy do not meaningfully change per org. Do not regenerate that content here.

Produce a short stub with exactly this structure:

1. **Page title**: `# Stage 5: Build — <workflow name> (<role>)`
2. **Pointer paragraph** (2-3 sentences): Explain that Stage 5 build guidance follows the framework methodology and link to `../stages/05-build.md`. Note that the items below are the *only* things that genuinely change for this organisation and workflow — everything else is framework-standard.
3. **Organisation-specific deltas** (markdown bullet list, 3-5 items). Include only things that are genuinely specific to this org's systems, data, or constraints. Examples of what qualifies:
    - Concrete client wrappers needed (e.g., `guidewire_client.py` — auth method, specific endpoints, known gotchas)
    - Specific values to externalise to config (e.g., scoring thresholds from the org's existing rubric, specific tier benchmarks)
    - Specific test data sources the engineer must use (e.g., "20 historical fraud cases from the prior 12 months with both 'Cleared' and 'Referred' outcomes")
    - Specific deployment or runtime constraints (e.g., "UK South region endpoints only per ICO data residency")
    - Specific CI/CD or ops integration points (e.g., "deploys as a ServiceNow workflow trigger, not a standalone service")

**Do NOT include** (all of this lives in the generic page):

- Project directory structure diagrams
- Generic testing strategy sections (unit / integration / evaluation)
- Prompt externalisation principles or YAML layout explanations
- Generic tool wrapper architecture explanations
- Generic `tests/` folder layout

If there are fewer than 3 genuine organisation-specific deltas, write fewer bullets. Do not invent filler. Brevity is the point — a reader should be able to scan this page in 30 seconds and know exactly what's different about their build.

### File 6: `evaluate.md` — Stage 6 (STUB — 20-40 lines max)

**Stage 6 is deliberately a stub page.** The generic [Stage 6: Evaluate](../stages/06-evaluate.md) methodology applies universally — test case design, failure categorisation, systematic diagnosis, iteration process, and graduation criteria do not meaningfully change per org. Do not regenerate that content here.

Produce a short stub with exactly this structure:

1. **Page title**: `# Stage 6: Evaluate — <workflow name> (<role>)`
2. **Pointer paragraph** (2-3 sentences): Link to `../stages/06-evaluate.md` and note that Stage 6 follows framework methodology. The items below are the *only* evaluation details that are org-specific.
3. **Organisation-specific deltas** (markdown bullet list, 3-5 items):
    - Specific test cases grounded in this org's real historical data (e.g., "Use 40 real cases from Q4 2024: 20 with known 'Approved' outcomes, 20 with known 'Declined' outcomes")
    - Specific quality bars tied to the org's existing human performance (e.g., "Agent score must match the senior analyst's score within 10% across the historical set")
    - Specific failure modes unique to this org's systems or data (e.g., "Guidewire claim note timestamps can be incorrect when adjusters batch-edit — test cases must include timestamp-ambiguity scenarios")
    - Specific sign-off authorities and gates (e.g., "Production sign-off requires Head of Claims + Head of Risk + DPO confirmation")
    - Specific regulatory evaluation requirements (e.g., "SR 11-7 model risk documentation pack required before production")

**Do NOT include** (all of this lives in the generic page):

- Generic test case design guidance (happy path / data gap / edge case templates)
- Generic failure category definitions (tool / prompt / flow / scope)
- Generic graduation checklist structure
- Generic iteration log format
- Generic quality dimension rubrics

If there are fewer than 3 genuine organisation-specific deltas, write fewer bullets. Do not invent filler.

## Quality Standards

- The output must be indistinguishable in structure and depth from the CSM
  worked example in `docs/worked-example/` **for Stages 1-4**. Stages 5 and 6
  are deliberately thin stub pages (see File 5 and File 6 instructions above).
- Use the org's actual system names, role titles, and constraints throughout —
  never use generic placeholders
- If the application guide recommends a first workflow for this role, use that
  workflow as the worked example subject
- Automation potential scores must be internally consistent
- Annotations should explain the *reasoning* behind decisions, not restate them
- The scope document must be detailed enough that an engineer could build from it
- **If the org config declares `regulatory_environment.governance_cycle_weeks > 4`**,
  any timeline in Stage 2 (Select) or in the output must reflect realistic
  build phases — do not default to 3-month first-agent pilots for regulated
  industries. Compute `phase_2_start_month = 1 + ceil(cycle_weeks / 4)`.

## Assumptions block — REQUIRED on every generated file

End **every** generated file (decompose.md, select.md, scope.md, design.md,
build.md, evaluate.md) with an `## Assumptions` section, even if the file is
the Stage 5 or Stage 6 stub. Format:

```markdown
## Assumptions

!!! note "What I inferred vs what was stated"
    - **<thing assumed>:** <your reasoning>
    - ⚠ **<load-bearing assumption>:** <reasoning and blast radius if wrong>
    - ...
```

Prefix load-bearing assumptions (ones where the reader's decisions would
change if the assumption is wrong) with ⚠. If the file has no assumptions
because every fact was grounded in the org config, write:

```markdown
## Assumptions

No assumptions — all content is grounded in the organisation config.
```

This is non-negotiable: a reader must be able to scroll to the bottom of any
generated file and instantly see what the AI made up vs what they told it.
