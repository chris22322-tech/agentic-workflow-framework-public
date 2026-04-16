# Stage 3: Scope — Organisation Analysis

You are analysing how a specific organisation would apply Stage 3 (Scope) of
the Agentic Workflow Framework.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml`
2. **Stage documentation**: Read `docs/stages/03-scope.md`

## What to Produce

### Scoping Considerations

For each role in the org config:
- What makes scoping harder for their workflows (ambiguous boundaries, shared
  ownership, variable inputs)
- Where the automation boundary likely falls — which steps stay human, which
  get automated
- How to handle workflows that cross role boundaries

### Systems Integration Mapping

For each system in the org config:
- What data it provides to scoped workflows
- API capabilities and limitations relevant to scoping
- Authentication and access patterns
- Rate limits or data volume constraints that affect scope decisions

### Constraint Impact on Scope

How the organisation's constraints (regulatory, data sensitivity, client-facing
requirements) affect scope decisions:
- Which workflow steps cannot be automated due to compliance requirements
- Where human-in-the-loop checkpoints are mandatory
- How approval gates should be built into the scope document

### Scope Document Adaptations

What this organisation should add to the standard scope document template:
- Organisation-specific fields or sections
- Compliance sign-off requirements
- Data classification for each input/output

## Output

Write a structured markdown report. The person producing the scope document
should be able to use your output as a companion guide alongside the framework's
standard Stage 3 instructions.
