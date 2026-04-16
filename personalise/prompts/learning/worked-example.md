# Custom Worked Example Generator

You are producing a complete Stage 1-3 worked example for a specific role and
workflow combination. The output follows the same structure and depth as the CSM
Quarterly Account Health Review worked example — but tailored to the role,
workflow, systems, and constraints the user provides.

This is a standalone prompt. A team lead can run it multiple times to generate
worked examples for different role + workflow combinations across the team.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's context, systems, and constraints.
2. **Role**: The user will specify a role name and description. If a matching
   role exists in the org config, use that description and enrich with the
   org's systems and constraints. If not, use whatever the user provides.
3. **Workflow**: The user will specify a workflow name and brief description.
4. **Key systems**: The user will specify the main systems involved in this
   workflow. Cross-reference with the org config's system list for API
   availability and access details.
5. **Framework stages 1-3**: Read `docs/stages/01-decompose.md`,
   `docs/stages/02-select.md`, and `docs/stages/03-scope.md` for the
   methodology and artifact structure.
6. **Reference worked example**: Read `docs/worked-example/decompose.md`,
   `docs/worked-example/select.md`, and `docs/worked-example/scope.md` for
   structural reference. Your output must match this level of detail.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output Structure

Produce a single markdown file with three major sections. Write the output to
`personalise/output/learning/worked-examples/{role-name}-{workflow-name}.md`
where names are lowercase with hyphens.

### Section 1: Stage 1 — Decompose

Produce a complete Workflow Inventory Table for the role. The table must:

- Cover 8+ workflows across 3-4 responsibility areas
- Include all eight columns: Responsibility Area, Workflow, Trigger, Frequency,
  Avg Time (hrs), Systems Touched, Output/Deliverable, Automation Potential
- Score each workflow's automation potential (High/Medium/Low)
- Place the target workflow in context alongside the other workflows the role
  performs

Add annotations (using `!!! note` admonitions) explaining:
- Why the target workflow scored the way it did
- Why at least one other workflow scored differently (to show contrast)
- The pattern that distinguishes High from Medium candidates for this role

Include a Dependencies section listing shared data sources, sequential
dependencies, and independent workflows.

### Section 2: Stage 2 — Select

Produce a complete Selection Decision Record:

- **Candidate comparison table**: Score the top 4 candidates on all six
  dimensions (Impact, Feasibility, Risk Tolerance, Complexity, Learning Value,
  Organisational Readiness) with the weighted composite
- **Per-criterion scoring for the chosen workflow**: Each criterion with weight,
  score (1-5), and a rationale paragraph that references the org's actual
  systems, constraints, and team context
- **Weighted score calculation**: Show the formula with actual numbers
- **Justification**: One paragraph explaining why this workflow is the right
  first build
- **Risks**: Known risks or caveats specific to this workflow and org

Add annotations explaining:
- Why the chosen workflow won over the runner-up
- At least one scoring decision that might seem counterintuitive, with the
  reasoning explained

### Section 3: Stage 3 — Scope

Produce a complete Workflow Scope Document:

- **Step-by-step workflow map**: Minimum 10 steps in the standard table format
  (Step #, Step Name, Action, Input, Output, Decision Logic, Boundary). Each
  step must have a populated Decision Logic column — not just "None" for data
  retrieval steps, but what validation or error conditions to check
- **Automation boundaries**: Each step marked as AUTOMATE, HIL, or MANUAL with
  the reasoning embedded in the Boundary column
- **Data inventory**: Every data source with access method, format, auth
  requirements, and notes
- **Integration requirements**: Technical requirements for the engineer who will
  build the agent
- **Constraints and assumptions**: Org-specific constraints from the org config
  plus workflow-specific assumptions

Add annotations explaining:
- Why specific steps are HIL rather than fully automated
- Where the automation boundary might shift in future versions
- The pattern that makes this workflow a good automation candidate

## Quality Standards

- The output must be indistinguishable in structure and depth from the CSM
  worked example in `docs/worked-example/`
- All examples must use the org's actual system names, role titles, and
  constraints — never generic placeholders
- Automation potential scores must be internally consistent: if you rate a
  workflow High, it must pass all four signals (structural repeatability,
  determinism, data availability, error recoverability)
- The scope document's step-by-step map must be detailed enough that an
  engineer could use it as a specification — not a summary
- Annotations should explain the *reasoning* behind decisions, not just
  restate what the decision was
