# Template Customisation Prompt

You are personalising the framework's blank templates by pre-filling fields that
are constant for this organisation — system names, data sources, integration
details — so users start from a template that already reflects their environment.

This prompt is called once by the fork script. It processes all template files
in a single pass.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for systems,
   constraints, and roles.
2. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` (if it
   exists) for data sensitivity analysis and system details.
3. **Generic templates**: Read all files in `docs/blank-templates/` for the
   template structures to personalise.

## What to Personalise

For each template, pre-fill the fields that are constant across all workflows
in the organisation. Leave workflow-specific fields blank — the user fills those
in when they apply the template to a specific workflow.

### Workflow Inventory (`workflow-inventory.md`)

- Pre-fill the example row's "Systems Touched" column with the org's actual
  systems (e.g., "Jira, Confluence, Salesforce" instead of "CRM, Slack")
- Update placeholder text in examples to use org-specific role and workflow names

### Scope Document (`scope-document.md`)

- **Data Inventory section**: Pre-fill rows for each system in the org config.
  For each system, fill in: Data Source (system name), Access Method (REST API
  if `api_available: true`, "Manual export" otherwise), Auth Required (based on
  system type). Leave Format and Notes blank for the user.
- **Integration Requirements section**: Pre-fill "Agent framework or platform:"
  with whatever the org has chosen in its config (if present), or leave as
  "your team's chosen platform — see Choose a Platform" if not specified.
  Leave "Language model provider" at the platform-neutral default. List each org
  system under "Tool wrappers needed" with a brief note about what data to pull.
- **Constraints and Assumptions section**: Pre-fill the Data sensitivity /
  governance field with the org's regulatory constraints and data sensitivity
  from the config.

### Selection Record (`selection-record.md`)

- Update placeholder text in examples to use org-specific role and workflow names

### Design Document (`design-document.md`)

- No structural changes — placeholder text updates only

### Evaluation Report (`evaluation-report.md`)

- No structural changes — placeholder text updates only

## Output

For each template file, produce the personalised version. The output must:

- Preserve all existing structure, headings, admonitions, and formatting
- Preserve all instructional text — do not remove guidance
- Only replace placeholder/example text with org-specific equivalents
- Keep blank rows for the user to fill in
- Add the org's systems as pre-filled example rows where indicated above

Write each personalised template to the output path specified by the caller,
mirroring the `docs/blank-templates/` directory structure.

## Quality Standards

- Templates must still function as templates — pre-filling must not remove the
  blank rows users need to fill in
- System names must match the org config exactly
- Do not invent systems or data sources not in the org config
- Preserve all MkDocs Material formatting (admonitions, tabs, definition lists)
- The download links to spreadsheet files should be preserved unchanged
