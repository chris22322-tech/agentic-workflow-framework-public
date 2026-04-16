# Quick Start Customisation Prompt

You are adapting the framework's Quick Start page so the mini-example uses an
org-specific role and workflow instead of the generic CSM example. The structure
and teaching approach stay identical — only the example content changes.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for roles,
   systems, and constraints.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for recommended first workflows and quick wins.
3. **Generic Quick Start**: Read `docs/getting-started/quick-start.md` for the
   existing page structure.

## What to Personalise

### The Mini-Example section

Replace the "Mini-Example: CSM in 30 Minutes" section at the end of the page
with an equivalent example using this organisation's context:

- **Role**: Pick the most representative role from the org config — ideally the
  one with the clearest quick win identified in the application guide.
- **Enumerate**: Use the org's actual systems and the kind of workflows this
  role performs. The four angles (Time, Triggers, Outputs, Systems) stay the
  same — the content changes.
- **Filter**: Show the same filtering exercise with org-specific workflows.
  Include at least one item that gets crossed out (responsibility, not a
  workflow) to demonstrate the filtering step.
- **Score**: Score 3-4 surviving workflows using the four signals. At least one
  should score High and one should score Medium or Low for contrast.
- **Best candidate**: Identify the best candidate with a realistic time-savings
  calculation using the org's actual workflow frequency and duration.

### The example admonition in Step 1

Replace the example text in the `!!! example` block in Step 1 with an
equivalent for the chosen org role. Keep the same format: *"I am the person
who ____."*

### Systems references in Step 2

In Angle 4 (Systems), the instructional text is generic and stays unchanged.
No modification needed.

## What Stays Unchanged

- All instructional content (Steps 1-6)
- The scoring guide table
- The filtering criteria table
- The "You Are Here" ASCII diagram
- The "What's Next" section and call-to-action button
- All admonitions (tips, info boxes) except the example in Step 1

## Output

Produce the complete Quick Start page — all instructional content preserved,
with only the example content and the Step 1 admonition replaced with
org-specific equivalents.

Write to the output path specified by the caller.

## Quality Standards

- The teaching flow must be identical — same steps, same progression, same
  pedagogical approach
- The org-specific example must be realistic for the role described in the config
- Workflow names must be specific (not "do reporting" but "compile weekly
  delivery status report")
- The time-savings calculation must use plausible numbers
- The example must include at least one crossed-out item to demonstrate filtering
- Preserve all MkDocs formatting: admonitions, tables, code blocks, buttons
