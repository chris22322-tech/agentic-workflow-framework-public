# Stage 1: Decompose

Before you can automate anything, you need to know exactly what you do. Not your job title, not your responsibilities — your actual workflows. The repeatable sequences of steps you perform, the triggers that kick them off, the outputs they produce, and the tools you touch along the way.

Most people skip this step. They jump straight to "I want to automate X" based on whatever feels most painful or interesting. The problem is that gut feel is unreliable — the workflow that frustrates you most is not necessarily the one that will benefit most from automation. You need a complete picture before you can make a good choice.

This stage walks you through breaking your role into a structured inventory of every repeatable workflow you perform, with enough detail about each one to make an informed automation decision in [Stage 2: Select](02-select.md). The goal is not to be exhaustive about every minute of your day — it is to surface the discrete, named workflows that have a trigger, a set of steps, and an output. Those are the building blocks everything else in this framework operates on.

---

## Inputs

!!! info "What You Need"

    - Role title and brief description
    - Optionally: a job description, list of OKRs, or similar role definition artifact

## Output Artifact

!!! info "Key Output"

    A **Workflow Inventory Table** — a structured inventory of every repeatable workflow in the role, annotated with metadata for automation scoring.

!!! abstract "Template"

    Use the [Workflow Inventory template](../blank-templates/workflow-inventory.md) as you work through this stage. It includes the Workflow Inventory Table with all required columns and a Dependencies section.

!!! info "Download Templates"
    [:material-download: Download Spreadsheet](../downloads/Stage 1 - Decompose.xlsx){ .md-button }

    Import into Google Sheets for a pre-formatted template with example rows.

---

## Method

### How to Enumerate Workflows

Most people can list their responsibilities but struggle to enumerate the discrete workflows within them. Use a two-pass approach to get from "I have a role" to a complete inventory.

**Pass 1 — Diverge.** Surface candidates from four angles. Each angle catches workflows the others miss.

- **Time-based.** Walk a typical week, then a typical month, then a typical quarter. Write down every activity that repeats. The weekly walkthrough catches high-frequency work (status updates, triage). The quarterly walkthrough catches high-effort work (reviews, prep cycles).
- **Trigger-based.** List every event that kicks off work for you: calendar entries, incoming requests, deadlines, threshold breaches, someone asking you for something. Each distinct trigger is a candidate workflow.
- **Output-based.** List every deliverable your role produces — reports, decks, assessments, briefs, summaries, emails-with-analysis-attached. Trace backward from each output to the process that creates it.
- **System-based.** List every tool you open during a typical work week. For each one, ask: *what drives me to open this?* Each reason is a candidate workflow.

??? example "What this looks like in practice"

    **A Customer Success Manager** running the four angles might surface:

    | Angle | What it catches |
    |---|---|
    | Time-based (weekly) | Monday standup prep, Friday forecast update |
    | Time-based (quarterly) | Account health reviews, QBR preparation |
    | Trigger-based | Escalation triage (incoming alert), onboarding kickoff (new deal closed), churn risk response (health score drop) |
    | Output-based | Health reports, renewal briefs, stakeholder decks, internal account summaries |
    | System-based | "Why do I open Salesforce?" → pipeline reviews, account updates. "Why do I open Zendesk?" → ticket trend analysis, escalation research |

    Notice how "account health review" appears from three angles (time, output, system). That overlap confirms it is a real workflow. But "churn risk response" only appears from the trigger angle — it is easy to forget because it is reactive rather than scheduled.

    **A Business Analyst** running the same angles might surface:

    | Angle | What it catches |
    |---|---|
    | Time-based (weekly) | Sprint planning prep, requirements backlog grooming |
    | Time-based (monthly) | Stakeholder progress report, metrics dashboard refresh |
    | Trigger-based | New feature request intake (incoming request), production incident analysis (P1 alert), change request impact assessment (change board submission) |
    | Output-based | Requirements documents, process flow diagrams, gap analysis reports, user story sets, UAT test plans |
    | System-based | "Why do I open Jira?" → backlog grooming, sprint tracking. "Why do I open Confluence?" → requirements documentation, process mapping |

    **A Software Engineer** running the same angles might surface:

    | Angle | What it catches |
    |---|---|
    | Time-based (weekly) | On-call rotation handoff, dependency update review |
    | Time-based (per-sprint) | Release notes compilation, post-deploy smoke test checklist |
    | Trigger-based | Bug report triage (incoming ticket), PR review (PR opened), production alert investigation (PagerDuty alert), new service scaffolding (project kickoff) |
    | Output-based | Architecture decision records (ADRs), runbooks, migration guides, API documentation updates, incident post-mortems |
    | System-based | "Why do I open Datadog?" → alert investigation, performance analysis. "Why do I open GitHub?" → PR reviews, release management. "Why do I open the wiki?" → runbook updates, onboarding docs |

    The engineer's list skews toward trigger-based workflows — much of the work is reactive. The system-based angle is particularly useful here because engineers touch many tools, and each tool often maps to a distinct workflow rather than a shared one.

**Pass 2 — Converge.** Clean up the raw list.

1. **Validate granularity.** Each candidate must have a trigger, a repeatable sequence of steps, and a concrete output. If any of these is missing, it is not a workflow yet — break it down further (see *What Makes a Workflow* below).
2. **Split compound entries.** If a candidate takes more than half a day and touches more than three systems, it probably contains two or more workflows bundled under one name. Split them.
3. **Merge duplicates.** Different angles will surface the same workflow under different names. "The thing I do every Monday morning" (time-based) and "the status summary I send to the PM" (output-based) may be the same workflow.

### What Makes a Workflow (Not a Responsibility)

A workflow has three properties:

1. **A recognisable trigger** that starts it — a calendar event, an incoming request, a threshold breach
2. **A repeatable sequence of steps** you perform in roughly the same order each time
3. **A concrete output** when you are done — a report, a decision, a deliverable

If any of these is missing, you are looking at something else:

| Entry | Trigger | Steps | Output | Verdict |
|---|---|---|---|---|
| "Account management" | None identifiable | Vague | None specific | **Responsibility** — too broad, break it down |
| "Respond to customer emails" | Incoming email | Varies completely | Varies | **Task** — no repeatable structure |
| "Quarterly account health review" | Calendar (end of quarter) | Same sequence each time | Health report + exec summary | **Workflow** — has all three properties |

??? example "More examples across roles"

    **CSM examples:**

    | Entry | Verdict | Why |
    |---|---|---|
    | "Manage renewals" | Responsibility | No single trigger or output — contains renewal prep, risk assessment, negotiation support, and contract processing |
    | "Renewal preparation" | Workflow | Trigger: 90 days before renewal. Steps: pull usage data, assess health, compile risk factors, draft renewal brief. Output: renewal brief + risk assessment |
    | "Send check-in email" | Task | No repeatable structure — what you write depends entirely on the account context |
    | "Onboarding kickoff preparation" | Workflow | Trigger: deal closed notification. Steps: pull contract details, set up project plan template, compile stakeholder list, draft kickoff deck. Output: kickoff pack |

    **Business Analyst examples:**

    | Entry | Verdict | Why |
    |---|---|---|
    | "Requirements gathering" | Responsibility | No single trigger — contains intake sessions, documentation, validation, and stakeholder sign-off across multiple timelines |
    | "New feature request intake" | Workflow | Trigger: incoming feature request. Steps: log request, assess against roadmap, check for duplicates, estimate complexity, draft impact summary. Output: triaged request with impact assessment |
    | "Answer a stakeholder question" | Task | No repeatable structure — each question requires different research and context |
    | "Sprint planning prep" | Workflow | Trigger: 2 days before sprint planning. Steps: review backlog priorities, check dependency status, compile velocity metrics, draft capacity recommendation. Output: sprint planning brief |

    **Software Engineer examples:**

    | Entry | Verdict | Why |
    |---|---|---|
    | "Backend development" | Responsibility | No single trigger or output — contains feature work, bug fixes, refactoring, and tech debt reduction across different timelines |
    | "Bug report triage" | Workflow | Trigger: new bug ticket assigned. Steps: reproduce issue, check logs, identify affected component, assess severity, write initial findings. Output: triaged ticket with reproduction steps and severity assessment |
    | "Fix a bug" | Task | No repeatable structure — each fix depends entirely on what is broken and where |
    | "On-call rotation handoff" | Workflow | Trigger: rotation changeover (weekly). Steps: compile open alerts, summarise active incidents, document workarounds in progress, brief incoming engineer. Output: handoff document |
    | "Release notes compilation" | Workflow | Trigger: release branch cut. Steps: pull merged PRs since last release, categorise by type, extract user-facing changes, draft release notes, get sign-off. Output: published release notes |

If you cannot fill in the **Trigger** and **Output/Deliverable** columns in the table below, your entry has not passed this test.

### The Workflow Inventory Table

Build a table with the following columns for every workflow you identify:

| Column | What to Capture |
|---|---|
| **Responsibility Area** | Group workflows by area (e.g., "Account Health", "Commercial") |
| **Workflow** | A specific, named workflow (not a vague responsibility) |
| **Trigger** | What kicks it off (calendar event, incoming request, threshold breach) |
| **Frequency** | Daily / Weekly / Monthly / Quarterly / Ad hoc |
| **Avg Time (hrs)** | Time per occurrence |
| **Systems Touched** | Tools, platforms, data sources involved |
| **Output/Deliverable** | What the workflow produces |
| **Automation Potential** | High / Medium / Low with a brief rationale |

Aim for a minimum of **8 discrete workflows**. If you have fewer, you are probably bundling multiple workflows under a single name. Break them apart.

### How to Score Automation Potential

**High** — The workflow is largely deterministic, the inputs and outputs are well-defined, the data is accessible programmatically, and errors are recoverable (you can review before it goes out).

**Medium** — The workflow has predictable structure but requires judgement calls at certain points. Could be automated with human-in-the-loop checkpoints.

**Low** — The workflow is highly contextual, depends on tacit knowledge, or involves sensitive interpersonal dynamics where agent involvement would be inappropriate or risky.

#### The Four Signals

When you are unsure where a workflow falls, evaluate it against these four signals:

| Signal | What to Ask | Strong (→ Higher) | Weak (→ Lower) |
|---|---|---|---|
| **Structural repeatability** | Does this workflow follow the same sequence of steps each time, regardless of which account or project it applies to? | Steps are the same across instances — only the data changes | You improvise the approach depending on context |
| **Determinism** | Given the same inputs, would two competent people produce substantially the same output? | Yes — the output follows from the data and a known framework | No — the output depends on individual judgement or relationship knowledge |
| **Data availability** | Can the inputs be accessed programmatically? | All key data sources have APIs or structured exports | Critical inputs exist only in someone's head or in unstructured conversations |
| **Error recoverability** | If the agent gets it wrong, what happens? | Output is reviewed before anyone external sees it — errors are catchable | Output goes directly to a client or triggers an irreversible action |

**High** requires strong signals across all four. **Medium** typically means three are strong but one introduces a judgement dependency. **Low** means two or more signals are weak.

??? example "Applying the four signals"

    **CSM — Quarterly Account Health Review:**

    | Signal | Assessment |
    |---|---|
    | Structural repeatability | **Strong.** Same steps every quarter for every account — pull data, assess against framework, score, write report |
    | Determinism | **Strong.** Two CSMs with the same data and scoring rubric would produce similar assessments |
    | Data availability | **Strong.** CRM, support platform, and usage analytics all have APIs |
    | Error recoverability | **Strong.** Report is reviewed internally before the client sees it |
    | **Verdict** | **High** — strong across all four |

    **CSM — Escalation Triage:**

    | Signal | Assessment |
    |---|---|
    | Structural repeatability | **Strong.** Same general flow: assess severity, identify owner, propose action |
    | Determinism | **Weak.** Two CSMs might make very different calls depending on relationship history and political context |
    | Data availability | **Strong.** Ticket data and CRM context are accessible |
    | Error recoverability | **Strong.** Triage recommendation is reviewed before action is taken |
    | **Verdict** | **Medium** — determinism is the weak signal. An agent could prepare the initial assessment, but a human needs to make the judgement calls |

    **Business Analyst — New Feature Request Intake:**

    | Signal | Assessment |
    |---|---|
    | Structural repeatability | **Strong.** Same checklist every time: log, assess against roadmap, check duplicates, estimate, summarise |
    | Determinism | **Strong.** Duplicate checking and complexity estimation follow documented criteria |
    | Data availability | **Strong.** Jira backlog, roadmap, and estimation history are all queryable |
    | Error recoverability | **Strong.** Intake summary is reviewed before prioritisation meeting |
    | **Verdict** | **High** — strong across all four |

    **Business Analyst — Production Incident Analysis:**

    | Signal | Assessment |
    |---|---|
    | Structural repeatability | **Weak.** Each incident is different — investigation steps depend on what system is affected and what went wrong |
    | Determinism | **Weak.** Root cause analysis depends heavily on experience and system knowledge |
    | Data availability | **Strong.** Logs, monitoring dashboards, and incident tickets are accessible |
    | Error recoverability | **Strong.** Analysis is reviewed in post-mortem before actions are taken |
    | **Verdict** | **Low** — two signals are weak. Data is available but the analysis itself is too contextual to automate meaningfully |

    **Software Engineer — Release Notes Compilation:**

    | Signal | Assessment |
    |---|---|
    | Structural repeatability | **Strong.** Same steps every release: pull merged PRs, categorise, extract user-facing changes, draft notes |
    | Determinism | **Strong.** Two engineers pulling the same PR list and applying the same categorisation rules would produce near-identical notes |
    | Data availability | **Strong.** Git history, PR metadata, and issue tracker are all queryable via API |
    | Error recoverability | **Strong.** Draft is reviewed by the team before publishing |
    | **Verdict** | **High** — strong across all four. This is almost entirely data retrieval and reformatting |

    **Software Engineer — Production Alert Investigation:**

    | Signal | Assessment |
    |---|---|
    | Structural repeatability | **Weak.** The investigation path depends on which service is alerting, what the symptoms are, and whether it is a known or novel failure mode |
    | Determinism | **Weak.** Two engineers may follow completely different diagnostic paths and reach different conclusions about root cause |
    | Data availability | **Strong.** Logs, metrics, traces, and alert history are all accessible programmatically |
    | Error recoverability | **Weak.** A wrong diagnosis during an active incident can lead to incorrect remediation — making things worse before they get better |
    | **Verdict** | **Low** — three signals are weak. Even though the data is rich, the investigation itself requires deep system knowledge and real-time judgement |

The consistent structure across instances is what makes a workflow automatable — not the fact that it is simple. A complex workflow with consistent structure is a better automation candidate than a simple workflow that changes shape each time.

### When a Workflow Scores Medium: The Sub-Workflow Pattern

A Medium rating often hides a useful distinction. When a workflow scores Medium because some steps are automatable and others require deep judgement, consider splitting it into sub-workflows with separate automation scores.

**How to split.** Give each sub-workflow its own row in the inventory table, with its own trigger (the second sub-workflow's trigger is the completion of the first), its own time estimate, and its own automation potential score. Use the parent workflow name in the Responsibility Area column so the relationship stays visible.

For example, a 10-hour quarterly preparation workflow might split into a 6-hour data-gathering-and-initial-analysis sub-workflow (High) and a 4-hour narrative-framing-and-presentation sub-workflow (Low). The first becomes a strong automation candidate on its own. The second stays human.

??? example "Splitting in practice"

    **CSM — Exec Business Review Prep** (originally one Medium entry at 8-12 hours):

    | Sub-Workflow | Trigger | Time | Automation Potential | Rationale |
    |---|---|---|---|---|
    | EBR data gathering and initial analysis | EBR scheduled (6 weeks out) | 5-6 hrs | High | Pull usage metrics, support trends, renewal timeline, product adoption data. Compile into a structured analysis. Same steps every time. |
    | EBR narrative and deck creation | Data pack complete | 3-6 hrs | Low | Shape the story for the exec sponsor. Requires relationship context, political sensitivity, and knowledge of what messaging will land. |

    The first sub-workflow is a strong automation candidate — it is data gathering and structured analysis. The second stays human because the value comes from the CSM's relationship knowledge and narrative judgement.

    **Business Analyst — Stakeholder Progress Report** (originally one Medium entry at 4-5 hours):

    | Sub-Workflow | Trigger | Time | Automation Potential | Rationale |
    |---|---|---|---|---|
    | Progress metrics compilation | Monthly reporting cycle | 2-3 hrs | High | Pull velocity data from Jira, compile feature completion rates, gather test coverage metrics, calculate burn-down trends. Same queries and format each month. |
    | Progress narrative and recommendations | Metrics compiled | 2 hrs | Medium | Interpret what the metrics mean for the project, flag risks, recommend adjustments. Requires project context but follows a predictable structure with a human review checkpoint. |

    Notice the BA example splits into High and Medium rather than High and Low — the narrative portion has enough structure (there is a template, the recommendations follow from the data) that it could work as a human-in-the-loop workflow rather than being entirely manual.

    **Software Engineer — On-call Rotation Handoff** (originally one Medium entry at 1-2 hours):

    | Sub-Workflow | Trigger | Time | Automation Potential | Rationale |
    |---|---|---|---|---|
    | Handoff data compilation | Rotation changeover (weekly) | 45 min | High | Pull open alerts from PagerDuty, active incident summaries from the incident tracker, recent deploy history from CI/CD, and pending maintenance windows from the calendar. Same queries every week. |
    | Handoff narrative and context briefing | Data pack compiled | 30-45 min | Low | Explain *why* certain alerts matter right now, which workarounds are fragile, which stakeholders are watching which issues. Requires context the outgoing engineer carries in their head. |

    The engineer example shows the same pattern as the CSM and BA cases: data gathering splits cleanly from contextual interpretation. The first half is API queries; the second half is institutional knowledge.

**When not to split.** Only split when the automatable and judgement-dependent portions are temporally separable — you finish one before starting the other. If judgement is interleaved throughout every step (you are making calls at each stage, not just at the end), the workflow is genuinely Medium and should stay as a single entry.

### Workflow Dependencies

Your inventory captures workflows as independent items, but workflows rarely operate in isolation. Before moving to selection, note where workflows depend on each other.

Three types of dependencies to look for:

Shared data sources
:   Multiple workflows consume the same data (e.g., several workflows pull from the CRM). Automating one creates a reusable data-retrieval tool that benefits others.

Sequential dependencies
:   Workflow A's output is Workflow B's input. For example, "quarterly health review" produces data consumed by "executive briefing preparation." Automation order matters — automating the upstream workflow first gives you more leverage.

Independent workflows
:   No data or sequencing relationship. These can be automated in any order.

Record dependencies as a brief list below your inventory table:

```
Dependencies:
- Quarterly Health Review → Exec Business Review Prep (health report feeds EBR deck)
- Quarterly Health Review, Renewal Preparation share CRM data source
- Cross-team Standup Prep, Escalation Triage are independent
```

!!! tip
    Dependencies affect which workflow you select in [Stage 2: Select](02-select.md). A workflow that unblocks two others has higher effective impact than its individual time savings suggest. If you plan to automate multiple workflows over time, start with the one whose output others consume.

!!! example "See it in practice"
    - [Customer Success Manager — Quarterly Account Health Review](../worked-example/decompose.md)
    - [Business Analyst — New Feature Request Intake](../worked-example-ba/decompose.md)
    - [Software Engineer — Release Notes Compilation](../worked-example-se/decompose.md)

---

## Guiding Questions

??? question "Guiding Questions"

    Use these prompts to surface workflows you might otherwise overlook:

    - What do you spend time on that follows roughly the same pattern each time?
    - What do you do that involves gathering information from multiple sources and synthesising it?
    - Where do you act as a relay — taking input from one system/person and reformatting it for another?
    - What tasks do you procrastinate on because they're tedious, not because they're hard?
    - What would you delegate to a competent junior if you had one?

---

## Common Mistakes

!!! warning "Common Mistakes"

    - **Listing responsibilities instead of workflows.** "Account management" is a responsibility. "Quarterly account health review" is a workflow. If it doesn't have a trigger, a cadence, and an output, it's not specific enough.
    - **Skipping the metadata columns.** Every column matters for Stage 2 scoring. "Systems Touched" determines feasibility. "Frequency" and "Avg Time" determine impact. Don't leave them blank.
    - **Inflating automation potential.** Be honest about where judgement is required. Overrating automation potential here leads to painful scope creep in Stage 3.

---

## Next Step

Once your inventory table is complete, move to [Stage 2: Select](02-select.md) to choose the right workflow to automate.
