# Quick Start: Your First Workflow Inventory

**Time required:** 30 minutes
**What you'll have at the end:** A draft inventory of your repeatable workflows, scored for automation potential, with your best candidate identified.

No tools, no setup, no technical background. Just you and something to write on.

---

## Step 1 — Pick Your Role (2 minutes)

Think about one specific hat you wear at work. Not your job title — one role you actually perform.

"Customer Success Manager" is a job title. "The person who prepares quarterly account health reviews" is closer to what we mean. Pick whatever feels most central to your week.

**Write it down.** One sentence: *"I am the person who ____."*

!!! example "Example"
    *"I am the person who manages the post-sale relationship for a portfolio of mid-market accounts."*

---

## Step 2 — Enumerate Your Workflows (10 minutes)

Open a blank sheet. Set a timer for 10 minutes. You are going to brainstorm from four angles — each one catches workflows the others miss.

**Do not filter yet.** Write down everything. Messy is fine. You will clean up in the next step.

### Angle 1 — Time

Walk through a typical week in your head. Then a typical month. Then a typical quarter.

*What do you do every Monday? What happens at month-end? What takes over your calendar every quarter?*

Write down every activity that repeats.

### Angle 2 — Triggers

List every event that kicks off work for you: calendar reminders, incoming requests, alerts, deadlines, someone pinging you on Slack.

*What makes you stop what you're doing and start something else?*

Each distinct trigger is a candidate workflow.

### Angle 3 — Outputs

List every deliverable your role produces — reports, decks, summaries, briefs, emails-with-analysis-attached.

*What do you hand to someone else when you're done?*

Trace backward from each output to the process that creates it.

### Angle 4 — Systems

List every tool you open during a typical work week. For each one, ask: *what drives me to open this?*

Each reason is a candidate workflow.

---

**When your timer goes off, stop.** Count your items. You should have 8-15 candidates. If you have fewer than 8, you are probably thinking too broadly — "account management" is a responsibility, not a workflow. Break it down.

---

## Step 3 — Filter to Workflows (5 minutes)

Not everything on your list is a workflow. Apply this test to each item:

| Question | If the answer is no… |
|---|---|
| Does it have a **recognisable trigger** that starts it? | It might be a responsibility — too vague |
| Does it follow a **repeatable sequence of steps**? | It might be a task — no consistent structure |
| Does it produce a **concrete output**? | It is not a workflow yet — keep breaking it down |

**Cross out anything that fails the test.** What is left are your actual workflows.

Common items to cross out:

- **Responsibilities** like "manage accounts" or "handle escalations" — too broad, no single trigger or output
- **One-off tasks** like "respond to a customer email" — no repeatable structure, it is different every time
- **Activities** like "attend meetings" — no concrete output

If crossing things out leaves you with fewer than 5 workflows, go back and break your crossed-out responsibilities into their component parts. "Manage renewals" might contain *renewal data compilation*, *risk assessment preparation*, and *renewal brief drafting* — each of which is a real workflow.

---

## Step 4 — Score Automation Potential (5 minutes)

For each surviving workflow, do a quick gut check against four signals. Do not overthink this — you are estimating, not committing.

| Signal | Ask yourself |
|---|---|
| **Repeatable structure** | Do I follow the same steps every time, or do I improvise? |
| **Deterministic output** | Would a colleague with the same data produce basically the same result? |
| **Data accessible digitally** | Can I get the inputs from systems with APIs, or is it all in my head? |
| **Errors are catchable** | Does someone review the output before it matters, or does it go straight out? |

**Score each workflow:**

- **High** — All four signals are strong. Same steps, predictable output, data is accessible, output gets reviewed.
- **Medium** — Three signals are strong but one introduces a judgement call. Could work with a human checkpoint.
- **Low** — Two or more signals are weak. Too contextual or too risky to hand off.

Write H, M, or L next to each workflow. Spend about 30 seconds per workflow.

---

## Step 5 — Spot Your Best Candidate (3 minutes)

Look at your High-rated workflows. Ask one question:

**Which one eats the most hours per month?**

Multiply frequency by time per occurrence. The workflow that scores High on automation potential *and* consumes the most time is probably your best automation candidate.

!!! tip
    Do not commit yet — [Stage 2](../stages/02-select.md) has a rigorous scoring framework that factors in feasibility, dependencies, and risk. But you should have a strong intuition about your front-runner right now.

Write down your top candidate and why you picked it.

---

## Step 6 — What's Next

**You now have a draft Stage 1 inventory.** In 30 minutes, you have done the core thinking work that most people skip entirely.

Here is how to keep going:

1. **Transfer your work into the full inventory format.** [Stage 1: Decompose](../stages/01-decompose.md) has the complete Workflow Inventory Table with all eight columns (trigger, frequency, average time, systems touched, output, and more). Fill it in for each workflow. This adds the detail that makes Stage 2 selection work.

2. **Move to Stage 2.** Once your inventory is complete, [Stage 2: Select](../stages/02-select.md) gives you a structured scoring framework to choose the right workflow — not just the one that feels right.

[:material-download: Download the Stage 1 Template](../downloads/Stage 1 - Decompose.xlsx){ .md-button }

A spreadsheet with pre-formatted columns, example rows, and data validation. Transfer your quick-start work into it and fill in the detail columns.

---

## Mini-Example: CSM in 30 Minutes

Here is what this exercise looks like end to end for a Customer Success Manager.

### Role

*"I am the person who manages post-sale relationships for a portfolio of 30 mid-market accounts."*

### Enumerate (10 min)

| Angle | What I wrote down |
|---|---|
| Time | Monday forecast update, quarterly account health reviews, monthly stakeholder reports |
| Triggers | New deal closed → onboarding kickoff, health score drops → churn risk response, support ticket escalated → escalation triage |
| Outputs | Health reports, renewal briefs, QBR decks, onboarding plans |
| Systems | Salesforce (pipeline, account data), Zendesk (ticket trends), Gainsight (health scores), Google Slides (decks) |

Raw count: 11 candidates after deduplication.

### Filter (5 min)

| Candidate | Trigger | Steps | Output | Verdict |
|---|---|---|---|---|
| Quarterly account health review | End of quarter | Pull data → assess health → score → write report | Health report + summary | **Workflow** |
| Onboarding kickoff prep | Deal closed notification | Pull contract → build plan → compile stakeholders → draft deck | Kickoff pack | **Workflow** |
| Renewal brief preparation | 90 days before renewal | Pull usage data → assess risk → compile factors → draft brief | Renewal brief | **Workflow** |
| "Manage accounts" | — | Varies | — | ~~Responsibility — crossed out~~ |
| "Respond to customer emails" | Incoming email | Varies completely | Varies | ~~Task — crossed out~~ |

4 workflows survived (showing 3 above for brevity).

### Score (5 min)

| Workflow | Repeatable | Deterministic | Data accessible | Errors catchable | Score |
|---|---|---|---|---|---|
| Quarterly account health review | Same steps every quarter | Two CSMs would score similarly | CRM + support + usage APIs | Reviewed internally first | **High** |
| Onboarding kickoff prep | Same checklist each time | Standard template | Contract + CRM data accessible | Reviewed before kickoff | **High** |
| Renewal brief preparation | Same data-pull sequence | Follows documented criteria | CRM + usage data accessible | Reviewed before outreach | **High** |

### Best candidate

**Quarterly account health review** — it runs 4× per year across 30 accounts (120 occurrences), takes 2-3 hours each, and scored High. That is 240-360 hours per year of highly automatable work.

Runner-up: Renewal brief preparation (fewer occurrences but similar structure).

---

## You Are Here

```
 ┌─────────────────────────────────────────────────┐
 │  ★ You just did a compressed version of this    │
 │                                                 │
 │  Stage 1          Stage 2         Stage 3       │
 │  Decompose   →    Select    →    Scope     →  … │
 │  ~~~~~~~~                                       │
 │  List your        Pick the       Map it in      │
 │  workflows        best one       full detail    │
 │                                                 │
 │  Next step: flesh out your inventory,           │
 │  then move to Stage 2.                          │
 └─────────────────────────────────────────────────┘
```

The hardest part — starting — is behind you. The rest is refining what you already have.

[Continue to Stage 1: Decompose →](../stages/01-decompose.md){ .md-button .md-button--primary }
