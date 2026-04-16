# Glossary Customisation Prompt

You are extending the framework's glossary with organisation-specific terms.
The generic glossary covers platform-neutral framework concepts (actions,
memory, HIL checkpoints, design patterns, error handling strategies). You are
adding terms from this organisation's domain — their systems, their industry
jargon, their internal terminology — so the glossary serves as a complete
reference for anyone in the org using the framework.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for industry,
   systems, constraints, and operating model.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for domain context and terminology used in the guide.
3. **Generic glossary**: Read `docs/reference/glossary.md` for the existing
   glossary structure and terms.

## What to Produce

Add a new section at the end of the glossary titled "Organisation-Specific
Terms" with terms relevant to this organisation. Include:

### System terms
For each system in the org config, add a glossary entry explaining what the
system is and how it is used in the context of the framework. Example:

> **Jira**
> :   Project tracking platform used for delivery milestones, sprint management,
>     and ticket workflows. *In the framework context: a primary data source for
>     workflow inventory (Stage 1) and a target system for agent integrations
>     (Stage 5).*

### Industry terms
Add terms specific to the org's industry that appear in the application guide
or would be needed when applying the framework. For a financial services org,
this might include terms like "KYC", "AML", "MSA". For a healthcare org, "PHI",
"HIPAA", "ePHI".

### Operating model terms
If the org has a specific operating model (vendor, platform, marketplace), add
terms that clarify what that means for framework application. For a vendor org,
this might include "client boundary", "MSA", "SOW".

### Role-specific terms
Add terms for role titles or internal concepts that are specific to this org
and would not be obvious to a new joiner reading the framework.

## Output

Produce the complete glossary — the full content of the generic glossary with
the new "Organisation-Specific Terms" section appended. Do not modify the
existing generic terms.

Write to the output path specified by the caller.

## Quality Standards

- Preserve the exact format of existing glossary entries (definition list with
  `:   ` syntax, italic technical notes, cross-references)
- New entries must follow the same format as existing ones
- Do not duplicate terms that already exist in the generic glossary
- Every term must have a "In the framework context" note explaining its
  relevance to automation and agent building
- Only include terms that someone using the framework at this org would
  actually need — do not pad with generic industry terms that add no value
