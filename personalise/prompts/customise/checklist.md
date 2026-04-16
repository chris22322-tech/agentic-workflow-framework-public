# Checklist Customisation Prompt

You are extending the framework's application checklist with organisation-specific
items. The generic checklist covers the universal steps for each stage. You are
adding items that reflect this organisation's constraints, approval gates, and
compliance requirements.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for constraints,
   regulatory environment, operating model, and approval requirements.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for guardrails, policies, and risk register.
3. **Generic checklist**: Read `docs/reference/checklist.md` for the existing
   checklist structure.

## What to Personalise

Add org-specific checklist items to the relevant stages. Insert them after the
generic items in each stage section, under a clearly marked sub-heading:
`### {Organisation Name} — Additional Items`.

### Stage 1: Decompose
- If the org has specific systems, add: "Verified that all {system names} are
  represented in the Systems Touched column"
- If the org has multiple roles, add: "Cross-referenced workflow inventory
  across roles for shared workflows and dependencies"

### Stage 2: Select
- If `operating_model.client_boundary: true`, add: "Confirmed selected workflow
  does not require MSA amendment for AI usage"
- If `constraints.regulatory` is not empty, add: "Checked that selected workflow
  complies with {regulation} requirements"

### Stage 3: Scope
- If `constraints.data_sensitivity` is not empty, add: "Data inventory includes
  sensitivity classification for each source"
- If `constraints.client_facing: true`, add: "All client-facing outputs have a
  HIL checkpoint before delivery"
- If `constraints.approval_requirements` is not empty, add: "Approval gate for
  {approval requirement} is documented in the workflow map"

### Stage 4: Design
- If `regulatory_environment.data_residency` is not empty, add: "LLM provider
  and data routing comply with {data residency} requirements"

### Stage 5: Build
- If `regulatory_environment.existing_ai_policy: true`, add: "Implementation
  reviewed against organisation's AI usage policy"
- If `constraints.data_sensitivity` mentions PII, add: "PII handling follows
  organisation's data classification policy"

### Stage 6: Evaluate
- If `constraints.client_facing: true`, add: "Test cases include a
  client-facing output reviewed by a domain expert"
- If `operating_model.type` is "vendor", add: "Evaluation includes a mock
  client review scenario"

Only add items that are relevant to this org's config. Do not add items for
constraints that are blank or false.

## Output

Produce the complete checklist — the full content of the generic checklist with
org-specific items added under each stage. Do not modify existing checklist
items.

Write to the output path specified by the caller.

## Quality Standards

- Preserve the exact format: task list syntax (`- [ ]`), stage headings,
  existing items unchanged
- Org-specific items must reference actual constraints from the config
- Each new item must be actionable and verifiable — not vague guidance
- Do not duplicate items that are already in the generic checklist
- Keep the checklist concise — add only items that represent real requirements,
  not aspirational best practices
