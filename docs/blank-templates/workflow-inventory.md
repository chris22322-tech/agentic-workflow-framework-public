# Workflow Inventory Template

Output artifact for [Stage 1: Decompose](../stages/01-decompose.md).

Fill in one row per workflow. Group by responsibility area.

[:material-download: Download spreadsheet template](../downloads/workflow-inventory.xlsx){ .md-button .md-button--primary }

The spreadsheet includes dropdown validation for **Frequency** and **Automation Potential** fields, plus a scoring guide reference sheet. Open it in Excel, Google Sheets, or any compatible application.

---

## Workflow Inventory Table

| Responsibility Area | Workflow | Trigger | Frequency | Avg Time (hrs) | Systems Touched | Output/Deliverable | Automation Potential |
|---|---|---|---|---|---|---|---|
| *e.g., Account Management* | *e.g., Quarterly Review* | *e.g., Calendar trigger* | *e.g., Weekly* | *e.g., 4* | *e.g., CRM, Slack* | *e.g., Status report* | *e.g., High* |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |
| | | | | | | | |

Add rows as needed. Aim for 8+ workflows across all responsibility areas.

---

## Workflow Dependencies

Your workflows rarely operate in isolation. Record dependencies here — they affect which workflow you select in [Stage 2](../stages/02-select.md).

### Shared data sources

List workflows that consume the same data. Automating one creates reusable data-retrieval tools for others.

- *e.g., Quarterly Health Review, Renewal Preparation share CRM data source*

### Sequential dependencies

List workflows where one's output feeds another's input. Use arrow notation — automate upstream first.

- *e.g., Quarterly Health Review → Exec Business Review Prep (health report feeds EBR deck)*

### Independent workflows

List workflows with no data or sequencing relationship. These can be automated in any order.

- *e.g., Cross-team Standup Prep, Escalation Triage are independent*

---

## Automation Potential Scoring Guide

**High** — The workflow is largely deterministic, the inputs and outputs are well-defined, the data is accessible programmatically, and errors are recoverable (you can review before it goes out).

**Medium** — The workflow has predictable structure but requires judgement calls at certain points. Could be automated with human-in-the-loop checkpoints.

**Low** — The workflow is highly contextual, depends on tacit knowledge, or involves sensitive interpersonal dynamics where agent involvement would be inappropriate or risky.
