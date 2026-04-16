# Worked Example: Release Notes Compilation & Publishing

!!! example "What you're looking at"
    This is a complete, end-to-end application of the Agentic Workflow Framework to a real workflow: **Release Notes Compilation & Publishing** performed by a **Software Engineer (SE)**.

    Each page in this section shows the completed artifact for one stage, with annotations explaining the decisions made.

!!! tip "Three worked examples, three roles"
    This framework includes three worked examples so you can see the methodology applied across genuinely different domains:

    - **This example (Software Engineer)** automates the compilation and publishing of release notes -- a workflow centred on Git history, PR metadata, CI/CD pipelines, and issue trackers. The input is code artifacts, the processing is categorisation and summarisation, and the output is user-facing documentation.
    - **[The CSM example](../worked-example/index.md)** automates the Quarterly Account Health Review -- a workflow centred on customer data, health scoring, and executive reporting. Start there if your role is customer-facing.
    - **[The BA example](../worked-example-ba/index.md)** automates New Feature Request Intake & Impact Assessment -- a workflow that bridges business stakeholders and engineering teams, drawing on Jira backlogs, roadmap data, and architectural dependencies.

    **Which should you follow?**

    - If your work involves **code, releases, CI/CD, monitoring, or engineering operations**, start here. This example will feel familiar to Software Engineers, SREs, DevOps Engineers, Release Managers, and anyone working with code-centric data sources.
    - If your work involves **requirements, backlogs, feature prioritisation, or cross-team coordination**, start with the [BA example](../worked-example-ba/index.md). That example is a better fit for Business Analysts, Product Managers, and anyone at the intersection of business needs and technical delivery.
    - If your work involves **customer relationships, account management, reporting, or portfolio analysis**, start with the [CSM example](../worked-example/index.md). That example is designed for Customer Success, Account Management, and client-facing roles.
    - If your work doesn't neatly fit any of these, **read all three**. Together they demonstrate that the framework's methodology is role-agnostic -- the stages work the same way whether your data comes from a CRM, a Jira board, or the GitHub API.

## Why this workflow

The Release Notes Compilation & Publishing workflow was chosen as the SE worked example for five reasons:

1. **Already referenced throughout the methodology.** The inline SE examples in Stages 1-6 use release notes compilation as their running scenario. This worked example expands those inline references into a complete, end-to-end application.
2. **High automation potential.** The workflow is consistently structured, deterministic in its data gathering steps, and operates on API-accessible data sources. It scores High on every automation-potential criterion: repeatable structure, well-defined inputs, structured deliverable, and natural review checkpoints.
3. **Code-centric data sources.** Where the CSM example pulls from CRM and support systems, and the BA example pulls from Jira and roadmap tools, this example pulls from Git history, PR metadata, issue trackers, and CI/CD pipelines. This validates the framework for workflows where the raw data is code artifacts, not business metrics.
4. **Clean data flow with interesting design challenges.** The pipeline -- tagged PRs → categorised changes → formatted notes → published -- is easy to follow, but the categorisation step introduces a real design challenge: label-based rules handle clean PRs, while LLM-assisted classification handles ambiguous ones. This mix of deterministic and LLM-driven logic is instructive.
5. **Different enough from CSM and BA.** The CSM example follows a *gather-assess-report* pattern on a quarterly cadence. The BA example follows a *triage-analyse-recommend* pattern triggered on demand. This example follows a *fetch-categorise-generate-publish* pattern triggered by a release event. Three patterns, three domains, one framework.

## What each stage shows

| Stage | What you'll see | Key takeaway |
|---|---|---|
| [Decompose](decompose.md) | Full Workflow Inventory Table for an SE role (8+ workflows across release management, code quality, incident management, and documentation) | How to enumerate workflows when your data sources are Git, CI/CD, and monitoring systems |
| [Select](select.md) | Selection Decision Record scoring Release Notes Compilation against On-Call Rotation Handoff, PR Review Triage, and Post-Mortem Compilation | How to choose between engineering workflows with different repeatability profiles |
| [Scope](scope.md) | 11-step workflow map with automation boundaries, data inventory (GitHub API, issue tracker, CI/CD), and decision logic for categorisation and filtering | How to scope a workflow where the hard part is classification, not data gathering |
| [Design](design.md) | Platform-neutral agent design — actions, flow, memory, action specifications, and a feedback-as-control-flow HIL checkpoint | How to design an agent that mixes deterministic processing (fetch, filter) with model-assisted steps (categorise, generate) |
| [Evaluate](evaluate.md) | Five test cases covering clean releases, large releases, hotfixes, breaking changes, and messy metadata | How to test an agent whose output quality depends on the quality of its input metadata |

## How to use this section

You have two options:

- **Read alongside the methodology.** Open the relevant worked example page in a second tab as you work through each [stage](../stages/index.md). Use it as a reference for what the completed artifact should look like.
- **Read first, then do your own.** Skim through all five pages to build a mental model of the end-to-end process before starting your own workflow.

Either way, the annotations (in coloured callout boxes) explain *why* specific decisions were made -- not just what they are. Pay attention to those.

!!! note "No Build stage in this example"
    Like the BA worked example, this example does not include a Build stage (Stage 5). The Design stage provides enough implementation detail that an engineer could build directly from it. This is deliberate: the framework's primary value is in the methodology stages (Decompose through Evaluate), and the [CSM example](../worked-example/index.md) already demonstrates what a Build stage looks like. Adding a second Build page would duplicate the lesson without adding new insight.
