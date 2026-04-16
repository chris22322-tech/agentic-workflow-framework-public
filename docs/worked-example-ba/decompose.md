# Worked Example: Stage 1 -- Decompose

!!! example "Worked Example"
    We're applying Stage 1 to: **a Business Analyst (BA) role**. The goal is to break this role into a structured inventory of discrete, repeatable workflows.

## Completed Artifact: Workflow Inventory Table

| Responsibility Area | Workflow | Trigger | Frequency | Avg Time (hrs) | Systems Touched | Output/Deliverable | Automation Potential |
|---|---|---|---|---|---|---|---|
| Requirements Management | **New Feature Request Intake & Impact Assessment** | Incoming feature request (Jira, email, or Slack) | Ad hoc (3-5x/week) | 2-3 | Jira, Confluence, Roadmap tool, OKR tracker | Triaged request with impact assessment | High |
| Requirements Management | Backlog Grooming Prep | 2 days before grooming session | Biweekly | 1-2 | Jira, Confluence, Roadmap tool | Prioritised backlog with context summaries | High |
| Requirements Management | Requirements Documentation | Feature approved for development | Per feature | 4-6 | Confluence, Jira, Figma, Meeting notes | Requirements spec (BRD + user stories) | Low |
| Analysis & Reporting | Sprint Velocity Analysis | Sprint close | Biweekly | 1-2 | Jira, Spreadsheet/BI tool | Velocity report with trend analysis | High |
| Analysis & Reporting | Stakeholder Progress Report | Monthly reporting cycle | Monthly | 4-5 | Jira, Confluence, Roadmap tool, Slides | Progress report + recommendations | Medium |
| Analysis & Reporting | Gap Analysis Report | New initiative or system evaluation | Ad hoc (1-2x/quarter) | 6-8 | Confluence, Jira, Architecture docs, Stakeholder interviews | Gap analysis document + recommendations | Medium |
| Process Coordination | Sprint Planning Prep | 2 days before sprint planning | Biweekly | 2-3 | Jira, Confluence, Capacity tracker | Sprint planning brief (capacity, priorities, dependency flags) | High |
| Process Coordination | UAT Coordination | Feature enters QA stage | Per feature | 3-4 | Jira, Test management tool, Confluence, Slack | UAT plan + test results summary | Medium |
| Process Coordination | Change Request Impact Assessment | Change board submission | Ad hoc (2-3x/month) | 3-5 | Jira, Confluence, Architecture docs, Dependency map | Impact assessment document | Medium |
| Stakeholder Management | Requirements Review Facilitation | Requirements draft complete | Per feature | 2-3 | Confluence, Jira, Meeting tools | Signed-off requirements + action items | Low |
| Stakeholder Management | Project Status Briefing | Weekly cadence or ad hoc (exec request) | Weekly | 1-2 | Jira, Confluence, Slack, Slides | Status briefing (deck or written update) | Medium |

## Workflow Dependencies

### Shared data sources

- New Feature Request Intake, Backlog Grooming Prep, Sprint Planning Prep share Jira data source (backlog items, ticket status, estimates, sprint metadata)
- New Feature Request Intake, Gap Analysis Report, Change Request Impact Assessment share Confluence data source (architecture docs, requirements specs, dependency maps)
- New Feature Request Intake, Stakeholder Progress Report share roadmap tool data (initiative status, priority rankings, OKR alignment)

### Sequential dependencies

- New Feature Request Intake → Backlog Grooming Prep (triaged and prioritised requests feed the grooming backlog)
- Sprint Planning Prep → Sprint Velocity Analysis (sprint commitments inform velocity tracking at sprint close)
- Requirements Documentation → UAT Coordination (signed-off requirements define the UAT scope and test criteria)

### Independent workflows

- Stakeholder Progress Report, Project Status Briefing are independent of each other — one is monthly analytical reporting, the other is weekly status communication
- Change Request Impact Assessment operates on its own ad-hoc trigger, independent of the sprint cycle workflows

## Annotations

!!! note "Why New Feature Request Intake scored High — and why we chose it"
    This workflow hits all four signals for High automation potential. (1) **Structurally repeatable** — the BA follows the same checklist every time: log the request, search for duplicates, pull roadmap context, estimate complexity, assess strategic alignment, and draft an impact summary. The steps don't change; only the request does. (2) **Deterministic** — duplicate checking is keyword matching against an existing backlog, and complexity estimation follows documented heuristics based on component history. Two BAs with the same data would reach similar conclusions. (3) **Data available** — Jira backlog, Confluence architecture docs, roadmap tools, and OKR trackers all have APIs or structured exports. (4) **Errors recoverable** — the impact assessment is reviewed by the BA before it reaches the prioritisation committee. At 3-5 requests per week and 2-3 hours each, this is also a volume workflow — small per-occurrence time savings compound into 6-15 hours per week. This is the workflow we carry through the remaining stages.

!!! note "Why Change Request Impact Assessment scored Medium, not High"
    On the surface, this workflow looks similar to feature request intake — assess an incoming item, trace its dependencies, produce a structured document. But the judgement layer is significantly heavier. Change requests arrive mid-sprint with varying degrees of political urgency. Assessing "how much does this disrupt what we're already building" requires understanding team capacity, sprint commitments, and which stakeholders are pushing hardest. An agent could map the technical dependencies (which services are affected, which teams own them, what's currently in-flight), but weighing the organisational dynamics — whether to absorb the disruption or push back — is a call that depends on context the BA carries from standups, hallway conversations, and relationship history. The structure is there; the judgement density makes it a Human-in-the-Loop candidate, not a primarily automated one.

!!! note "Why Gap Analysis Report scored Medium despite high time cost"
    At 6-8 hours, this is the most time-intensive workflow on the list. So why Medium and not High? Because time cost alone does not determine automation potential. A gap analysis requires the BA to define what "the gap" even is — synthesising stakeholder expectations, current system capabilities, and strategic direction into a diagnosis that's unique to each engagement. One gap analysis might compare a legacy billing system against new regulatory requirements; the next might assess whether an internal tool can support a new market segment. The data gathering is automatable (pull system capabilities, compile feature lists, extract stakeholder requirements from Confluence), but the interpretive framework changes every time. This is a workflow where the [sub-workflow pattern](../stages/01-decompose.md#when-a-workflow-scores-medium-the-sub-workflow-pattern) applies well: split data compilation (High) from synthesis and diagnosis (Low).

!!! note "Why Backlog Grooming Prep scored High"
    At 1-2 hours biweekly, this workflow is modest per occurrence. It scores High because of its mechanical nature: pull ticket statuses from Jira, check which items have stale acceptance criteria, flag tickets missing estimates, cross-reference against the roadmap for priority shifts, and compile the results into a summary the product owner can act on. There is very little interpretation involved — the BA is mostly reformatting information that already exists in structured systems into a view that's useful for a grooming session. High frequency + low judgement = strong automation candidate, even when individual time savings are small.

!!! note "Why Requirements Review Facilitation scored Low"
    This might look like it should be automatable — it has a trigger, a set of steps, and a deliverable. But the value of this workflow is not the artifact (signed-off requirements and action items). It's the live conversation: drawing out unstated assumptions, mediating between conflicting stakeholder views, and building alignment on scope trade-offs that weren't visible in the written requirements. These are fundamentally interpersonal dynamics. An agent could prepare the meeting — pull the requirements, compile open questions, pre-populate an agenda — but the facilitation itself is where the BA's expertise lives. When a workflow's core value is relational rather than informational, automation addresses the wrong problem.

!!! tip "Pattern to notice"
    In BA workflows, the line between High and Medium is not about complexity — it's about **where the thinking happens**. The workflows that score High apply **documented criteria to structured data**: Is this a duplicate? What's the historical velocity? Which items meet the priority threshold? The workflows that score Medium require the BA to **interpret what the data means in a specific context**: What story do these metrics tell? Which teams will push back on this change? How does this gap reshape the roadmap? If the answer depends on criteria you could write down, the workflow is likely High. If the answer depends on context you carry in your head, it's likely Medium.

---

[:octicons-arrow-left-24: Back to Stage 1: Decompose](../stages/01-decompose.md){ .md-button }
