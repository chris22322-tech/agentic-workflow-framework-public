# Worked Example: Stage 1 -- Decompose

!!! example "Worked Example"
    We're applying Stage 1 to: **a Customer Success Manager (CSM) role**. The goal is to break this role into a structured inventory of discrete, repeatable workflows.

## Completed Artifact: Workflow Inventory Table

| Responsibility Area | Workflow | Trigger | Frequency | Avg Time (hrs) | Systems Touched | Output/Deliverable | Automation Potential |
|---|---|---|---|---|---|---|---|
| Account Health | Quarterly Account Health Review | Calendar (end of quarter) | Quarterly | 6-8 | CRM, Support tickets, Product usage data, Internal docs, Slack | Health report + exec summary | High |
| Account Health | Escalation Triage | Incoming alert/flag | Ad hoc (2-3x/week) | 1-2 | CRM, Slack, Support platform | Triage assessment + action plan | Medium |
| Commercial | Renewal Preparation | 90 days before renewal | Per account cycle | 4-6 | CRM, Finance, Contract system | Renewal brief + risk assessment | High |
| Commercial | Upsell Opportunity Identification | Quarterly review or ad hoc | Quarterly | 3-4 | Product usage data, CRM, Roadmap | Opportunity brief | Medium |
| Delivery Coordination | Cross-team Standup Prep | Weekly standup cadence | Weekly | 1 | Jira, Slack, Internal docs | Status summary + blockers list | High |
| Delivery Coordination | Go-live Readiness Assessment | Pre-go-live milestone | Per project phase | 4-6 | Jira, Test results, Runbooks | Readiness checklist + risk register | Medium |
| Stakeholder Mgmt | Exec Business Review Prep | Quarterly or semi-annual | Quarterly | 8-12 | CRM, Product data, Finance, Slides | EBR deck + talking points | Medium |
| Stakeholder Mgmt | Internal Account Briefing | Ad hoc (new stakeholder, exec visit) | Ad hoc | 2-3 | CRM, Internal docs, Slack history | Briefing doc | High |

## Workflow Dependencies

### Shared data sources

- Quarterly Account Health Review, Renewal Preparation, Upsell Opportunity Identification share CRM data source (account metadata, ARR, contract dates, activity history)
- Quarterly Account Health Review, Escalation Triage share support ticket data (ticket history, severity, CSAT)
- Quarterly Account Health Review, Exec Business Review Prep share product usage data (DAU/MAU, feature adoption, API call volume)

### Sequential dependencies

- Quarterly Account Health Review → Exec Business Review Prep (health report feeds EBR deck and talking points)
- Upsell Opportunity Identification → Renewal Preparation (upsell insights inform renewal strategy and expansion positioning)

### Independent workflows

- Cross-team Standup Prep, Internal Account Briefing are independent of each other and of the health review cycle
- Escalation Triage operates on its own ad-hoc trigger, independent of all scheduled workflows

## Annotations

!!! note "Why Quarterly Account Health Review scored High"
    This workflow hits all three criteria for High automation potential: (1) it is largely deterministic -- gather data, assess against a framework, produce a report; (2) the inputs and outputs are well-defined -- CRM data, support tickets, usage metrics in, structured health report out; (3) errors are recoverable because the report is reviewed internally before any client sees it. The consistent structure across accounts is what makes this automatable, not the fact that it is simple.

!!! note "Why Escalation Triage scored Medium, not High"
    Escalation triage has a predictable structure (assess severity, determine owner, propose action), but the judgement calls at each step are highly contextual. The "right" response depends on the account's relationship history, the political dynamics of the escalation, and sometimes information that only exists in someone's head. An agent could prepare the initial assessment, but a human needs to be deeply involved at every decision point -- making it a Human-in-the-Loop candidate rather than a primarily automated workflow.

!!! note "Why EBR Prep scored Medium despite high time cost"
    At 8-12 hours, Exec Business Review Prep is the most time-consuming workflow on this list. So why Medium and not High? Because the output is a presentation deck with narrative framing that is heavily shaped by relationship context and political sensitivity. The data gathering portion is automatable, but the "what story do we tell the exec sponsor" portion requires deep human judgement. The workflow would need to be broken into sub-workflows, with only the data-gathering and initial analysis sub-workflow automated.

!!! note "Why Cross-team Standup Prep scored High"
    Despite being only 1 hour per occurrence, this workflow scores High because of its frequency (weekly) and its mechanical nature. It is almost entirely data retrieval and reformatting: pull status from Jira, pull updates from Slack, compile into a summary. There is very little judgement involved. High frequency + low complexity = strong automation candidate.

!!! tip "Pattern to notice"
    The workflows that score High share a common pattern: they are primarily about **gathering data from known sources and producing a structured output**. The ones that score Medium add a layer of **contextual judgement** that makes full automation risky. This distinction is the core of the automation potential assessment.

---

[:octicons-arrow-left-24: Back to Stage 1: Decompose](../stages/01-decompose.md){ .md-button }
