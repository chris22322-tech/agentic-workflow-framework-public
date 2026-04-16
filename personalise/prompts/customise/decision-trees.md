# Decision Tree Customisation Prompt

You are extending the framework's decision trees with organisation-specific
constraint gates. The generic decision trees help users decide whether to
automate a step and which graph pattern to use. You are adding early gates
that check for org-specific constraints before the user reaches the generic
decision logic.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for constraints,
   regulatory environment, operating model, and data sensitivity.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for guardrails, risk register, and data sensitivity analysis.
3. **Generic decision trees**: Read `docs/reference/decision-trees.md` for the
   existing decision tree structure.

## What to Personalise

### "Should I Automate This Step?" tree

Add 1-3 early gate nodes at the top of the tree, before the existing first
question. These gates check for org-specific constraints that would immediately
rule out or restrict automation. The gates should be derived from the org config:

- **If `constraints.client_facing: true`**: Add a gate: "Does this step produce
  client-facing output?" → If Yes, route to "HIL required — client deliverables
  need human review" before continuing to the generic tree.
- **If `operating_model.client_boundary: true`**: Add a gate: "Does this step
  cross the client boundary?" → If Yes, route to "Check MSA/SOW for AI clauses
  before proceeding."
- **If `constraints.regulatory` is not empty**: Add a gate: "Does this step
  involve regulated data ({specific regulation from config})?" → If Yes, route
  to "Apply data classification policy — see Guardrails."
- **If `constraints.data_sensitivity` mentions PII or PHI**: Add a gate: "Does
  this step process PII/PHI?" → If Yes, route to "Anonymise or use on-premise
  model — do not send to external LLM."

Only add gates that are relevant to this org's config. Do not add gates for
constraints that are blank or false.

### "What Graph Pattern Should I Use?" tree

This tree is technical and universal — do not modify it. Copy it unchanged.

## Output

Produce the complete decision trees page — the full content with the
personalised "Should I Automate?" tree and the unchanged "What Graph Pattern?"
tree. Preserve all existing content, Mermaid syntax, styling, admonitions, and
cross-references.

The personalised Mermaid diagram must:
- Use the same styling conventions (fill colours, arrows)
- Add org-specific gate nodes at the top, flowing into the existing tree
- Use `style` directives matching the existing colour scheme
- Be valid Mermaid `flowchart TD` syntax

Write to the output path specified by the caller.

## Quality Standards

- The Mermaid diagrams must render correctly — validate syntax before output
- Org-specific gates must reference actual constraints from the config, not
  generic placeholders
- New gate nodes must use clear, concise questions (one line)
- The flow from org-specific gates into the generic tree must be logical —
  passing an org gate should lead to the existing first question
- Preserve all existing admonitions, cross-references, and pattern links
