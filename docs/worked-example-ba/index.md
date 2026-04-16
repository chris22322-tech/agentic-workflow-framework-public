# Worked Example: New Feature Request Intake & Impact Assessment

!!! example "What you're looking at"
    This is a complete, end-to-end application of the Agentic Workflow Framework to a real workflow: **New Feature Request Intake & Impact Assessment** performed by a **Business Analyst (BA)**.

    Each page in this section shows the completed artifact for one stage, with annotations explaining the decisions made.

!!! tip "Two worked examples, two roles"
    This framework includes two worked examples so you can see the methodology applied in genuinely different contexts:

    - **This example (Business Analyst)** automates the intake and impact assessment of new feature requests -- a workflow that bridges business stakeholders and engineering teams, drawing on Jira backlogs, roadmap data, and architectural dependencies.
    - **[The CSM example](../worked-example/index.md)** automates the Quarterly Account Health Review -- a workflow centred on customer data, health scoring, and executive reporting. Start there if your role is customer-facing.
    - **[The SE example](../worked-example-se/index.md)** automates Release Notes Compilation & Publishing -- a workflow centred on Git history, PR metadata, and CI/CD pipelines. Start there if your role is engineering-focused.

    **Which should you follow?**

    - If your work involves **requirements, backlogs, feature prioritisation, or cross-team coordination**, start here. This example will feel familiar to Business Analysts, Product Managers, Project Managers, and anyone working at the intersection of business needs and technical delivery.
    - If your work involves **customer relationships, account management, reporting, or portfolio analysis**, start with the [CSM example](../worked-example/index.md). That example is a better fit for Customer Success, Account Management, and client-facing roles.
    - If your work involves **code, releases, CI/CD, monitoring, or engineering operations**, start with the [SE example](../worked-example-se/index.md). That example is designed for Software Engineers, SREs, DevOps Engineers, and Release Managers.
    - If your work doesn't neatly fit any of these, **read all three**. The three examples together show that the framework's methodology is role-agnostic -- the stages work the same way regardless of your domain.

## Why this workflow

The New Feature Request Intake & Impact Assessment was chosen as the BA worked example for four reasons:

1. **High automation potential.** The workflow scores High on the automation potential criteria: it follows a repeatable structure, draws from well-defined data sources, and produces a structured deliverable. A BA typically spends 2-3 hours per request on intake and assessment -- across a steady stream of incoming requests, that adds up fast.
2. **Multiple data sources.** The workflow pulls from Jira (backlog and estimation history), Confluence (architecture docs and decision records), roadmap tools, and OKR tracking. This exercises the framework's guidance on data inventory and integration design in ways the CSM example does not.
3. **Both quantitative and qualitative steps.** Duplicate checking and complexity estimation are structured and data-driven. Strategic alignment assessment and stakeholder impact narrative require judgement. This mix makes it a good test of the framework's automation boundary guidance.
4. **Different domain, different pattern.** Where the CSM example follows a *gather-assess-report* pattern on a quarterly cadence, this workflow follows a *triage-analyse-recommend* pattern triggered on demand. Seeing both patterns proves the framework generalises beyond a single workflow shape.

## What each stage shows

| Stage | What you'll see | Key takeaway |
|---|---|---|
| [Decompose](decompose.md) | Full Workflow Inventory Table for a BA role (8+ workflows across 4 responsibility areas) | How to enumerate workflows when your role spans business and technical domains |
| [Select](select.md) | Selection Decision Record with scored criteria, showing why intake & assessment beats other candidates | How to choose between workflows that all seem like strong candidates |
| [Scope](scope.md) | 10-step workflow map with automation boundaries, data inventory, and integration requirements | How to draw automation boundaries when some steps require human judgement |
| [Design](design.md) | Platform-neutral agent design — actions, flow, memory, action specifications, and error handling | How to design an agent with multiple HIL checkpoints and cross-system data gathering |
| [Evaluate](evaluate.md) | Five test cases covering happy path, edge cases, and an iteration cycle | How to test an agent that produces qualitative assessments, not just structured data |

## How to use this section

You have two options:

- **Read alongside the methodology.** Open the relevant worked example page in a second tab as you work through each [stage](../stages/index.md). Use it as a reference for what the completed artifact should look like.
- **Read first, then do your own.** Skim through all five pages to build a mental model of the end-to-end process before starting your own workflow.

Either way, the annotations (in coloured callout boxes) explain *why* specific decisions were made -- not just what they are. Pay attention to those.

!!! note "No Build stage in this example"
    Unlike the CSM worked example, this example does not include a Build stage (Stage 5). The Design stage is written with enough detail that an engineer could implement directly from it. This is deliberate: the framework's primary value is in the methodology stages (Decompose through Design and Evaluate), and we wanted to show that a thorough design document is a valid stopping point -- especially for BAs who will hand off implementation to an engineering team.
