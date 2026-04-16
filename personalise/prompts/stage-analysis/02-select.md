# Stage 2: Select — Organisation Analysis

You are analysing how a specific organisation would apply Stage 2 (Select) of
the Agentic Workflow Framework.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml`
2. **Stage documentation**: Read `docs/stages/02-select.md`

## What to Produce

### Scoring Criteria Adjustments

How the five scoring signals (volume/frequency, pattern consistency, data
availability, quality requirements, current time cost) should be weighted or
adjusted for this organisation:
- Which signals matter most given their constraints?
- Are there additional signals this organisation should consider (e.g.,
  regulatory risk, client visibility, cross-role dependency)?

### Role-by-Role Selection Guidance

For each role in the org config:
- Which of their inventoried workflows would likely score highest and why
- Which workflows should be deprioritised despite high scores (compliance risk,
  client-facing, cross-boundary)
- Recommended first automation candidate with justification

### Organisation-Specific Selection Filters

Filters this organisation should apply on top of the standard scoring:
- Data sensitivity gates (can the workflow's data go to an LLM?)
- Client/stakeholder approval requirements
- Regulatory review gates
- Technical feasibility given their systems landscape

### Recommendations

How this organisation should run their selection workshop. Who should be in the
room, what pre-work is needed, and how to handle cross-role workflow dependencies.

## Output

Write a structured markdown report suitable for the team lead running the
selection process.
