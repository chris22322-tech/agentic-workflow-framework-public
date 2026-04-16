# Getting Started Customisation Prompt

You are adding organisation-specific context to the framework's Getting Started
page. The page explains what the framework is, who it is for, and how to start.
You are extending the "Who is this for?" section with descriptions that match
this organisation's roles and adding the org's systems to the prerequisites
context.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for roles,
   systems, industry, and constraints.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for role playbooks and recommended starting points.
3. **Generic Getting Started page**: Read `docs/getting-started/index.md` for
   the existing page structure.

## What to Personalise

### "Who is this for?" section

The generic page describes three personas: Knowledge workers, Business analysts,
and Software engineers. Add a new subsection **before** these three, titled
"At {Organisation Name}":

For each role in the org config, write 2-3 sentences describing how that role
would use the framework. Reference:
- The kind of workflows they perform (from the role description)
- Which stages they would own vs. collaborate on
- Their most likely first automation candidate (from the application guide, if
  available)

Keep the existing three persona descriptions unchanged after the org-specific
section.

### "What kind of workflows work best?" section

Add an admonition (`!!! example "At {Organisation Name}"`) after the existing
"Good candidates" paragraph. List 2-3 concrete examples of good automation
candidates from this org, derived from the org config's goals and target
workflows. For example:

> **Weekly delivery status report** — pulls data from Jira and Confluence,
> follows the same structure every week, reviewed by the DM before distribution.
> Classic high-automation candidate.

### Systems context

In the "Where do I start?" section, add a brief note about the org's systems
if the org config lists 3+ systems with API access:

> !!! tip "Your systems"
>     Your team uses {system list} — all of which have API access. This means
>     the data-gathering steps in most of your workflows are strong automation
>     candidates from day one.

## What Stays Unchanged

- The opening "What is this framework?" section
- The six-stage plain-language summary
- The three generic persona descriptions (Knowledge workers, BA, SE)
- The "What will I have at the end?" section
- The "How long does this take?" section
- The bottom-line quote block

## Output

Produce the complete Getting Started page — all existing content preserved, with
org-specific additions inserted at the locations described above.

Write to the output path specified by the caller.

## Quality Standards

- Org-specific additions must feel native — same tone, same level of detail,
  same practical focus as the surrounding content
- Role descriptions must match the org config, not invent capabilities
- Workflow examples must be realistic for the described roles and systems
- Do not repeat information that is already in the generic persona descriptions
- Preserve all MkDocs formatting: admonitions, definition lists, tables, links
