# CSM Framework Discovery Prompt

Use this prompt with Claude, ChatGPT, or any capable AI assistant. Paste it along with your own context to get a personalised assessment of what you need to learn to apply the Agentic Workflow Framework to your CSM role.

---

## The Prompt

```
You are helping a Customer Success Manager prepare to use the Agentic Workflow
Framework — a six-stage methodology for identifying, scoping, and building
AI agents that automate repetitive knowledge work.

The CSM will complete Stages 1-3 independently (no coding required) and hand
off to an engineer for Stages 4-6. Your job is to assess what this specific
CSM needs to learn, based on their current situation.

## About Me (fill this in before running)

Role: Customer Success Manager
Company/Industry: [e.g., "B2B SaaS", "Core banking vendor", "FinTech"]
Portfolio size: [e.g., "25 mid-market accounts", "8 enterprise accounts"]
Typical workflows I do repeatedly:
- [e.g., "Weekly client check-in prep"]
- [e.g., "Quarterly health reviews"]
- [e.g., "Renewal preparation"]
- [e.g., "Escalation triage"]

Systems I use daily: [e.g., "Salesforce, Zendesk, Slack, Gainsight, Google Sheets"]
Technical comfort level: [e.g., "I can use APIs through Postman but don't write code",
  "I'm comfortable with spreadsheets and formulas but nothing technical",
  "I've built simple Zapier automations"]
Previous AI experience: [e.g., "I use ChatGPT for drafting emails",
  "None", "I've used Copilot in Excel"]
What I hope to get from this: [e.g., "Save time on weekly reporting",
  "Produce more consistent health reviews across my book",
  "Stop spending Fridays doing data gathering"]

## What I Need You To Do

Read the framework documentation (I'll paste the key pages below, or you can
read from the docs/ directory if you have file access). Then produce a
personalised learning needs assessment covering:

### 1. Concept Check
For each concept below, rate my likely familiarity (Already Know / Need Introduction / Need Deep Dive) based on my profile above, and explain in one sentence WHY it matters for my specific workflows:

- What a "workflow" is vs a responsibility or task
- How to enumerate workflows systematically (not just listing what comes to mind)
- How to score automation potential using structured criteria (not gut feel)
- How to use weighted scoring to pick the right workflow to automate first
- What "automation boundary" means — AUTOMATE vs HUMAN-IN-THE-LOOP vs MANUAL
- How to map a workflow step by step (the "write it for a new hire" test)
- What decision logic capture is and why it matters
- What an error path is and why you need to map them
- What a human-in-the-loop checkpoint is and when to use one
- What happens after you hand off to an engineer (what Stage 4 looks like from your side)
- How to evaluate whether the agent's output is good enough
- How to give feedback that actually improves the agent

### 2. Skills Gap Analysis
Based on my profile, identify which of these skills I likely have vs need to develop:

**Process documentation skills:**
- Can I map a workflow step by step with enough detail that someone else could follow it?
- Can I articulate my decision criteria explicitly (not just "I know it when I see it")?
- Can I identify where I apply judgement vs where I follow a deterministic rule?

**Data awareness skills:**
- Do I know which of my systems have APIs? (Do I even need to know this?)
- Can I list every data source I touch during a workflow?
- Do I understand what "data quality" means for my CRM/CS platform data?

**Evaluation skills:**
- Can I define what "good output" looks like for my workflows?
- Can I compare an agent's draft against what I would have produced manually?
- Can I give structured feedback ("the risk rating is wrong because X") rather than vague feedback ("this doesn't feel right")?

**Collaboration skills:**
- Can I explain my workflow to an engineer who has never done my job?
- Can I validate a design document against my scope document?
- Can I participate in testing without needing to understand the code?

### 3. My Workflows Mapped to the Framework
For each workflow I listed above, give me:
- Which framework stage it maps to (is it a Stage 1 inventory item, a Stage 2 candidate, or something I should scope in Stage 3?)
- A rough automation potential score (High/Medium/Low) with one-line rationale
- The likely automation boundary (what stays human, what could be automated)
- The single biggest risk or gotcha I should watch for
- One question I should ask myself before deciding to automate this

### 4. Personalised Learning Path
Based on everything above, create a sequenced learning plan:

**Week 1: Foundation (2-3 hours)**
- What to read (specific framework pages)
- What to do (specific exercise — not "read the page" but "do this with your own workflows")
- What to produce (specific artifact)

**Week 2: Depth (2-3 hours)**
- What to read
- What to do
- What to produce

**Week 3: Application (3-4 hours)**
- What to read
- What to do
- What to produce — this should be a complete Stage 1-3 pass for one real workflow

**Week 4: Handoff Preparation (1-2 hours)**
- How to prepare your scope document for handoff
- What to expect from the engineer
- How to stay involved during build and evaluation

### 5. Red Flags and Misconceptions
Based on CSMs you've seen try to apply automation frameworks, what are the
top 5 mistakes I'm likely to make? For each, give me:
- The mistake
- Why CSMs specifically make this mistake (not engineers, not BAs — CSMs)
- How the framework prevents it (which stage/tool/check catches it)
- What to watch for in my own work

### 6. Quick Confidence Builder
Give me ONE workflow from my list that I should start with — the one where:
- I'm most likely to succeed on my first try
- The risk is lowest (internal output, easily corrected)
- The time savings are tangible enough to justify the learning investment
- The pattern transfers to at least one other workflow

Explain in 3-4 sentences why this is the right starting point for ME specifically.
```

---

## How to Use This Prompt

1. **Fill in the "About Me" section** with your real details. The more specific you are, the more useful the output.

2. **Run it** — paste into Claude.ai, ChatGPT, or your preferred AI assistant. If using Claude Code with file access, it will read the framework docs directly for richer context.

3. **Review the output** — especially the Skills Gap Analysis and Red Flags sections. These tell you where you'll struggle before you hit the wall.

4. **Follow the learning path** — it's sequenced so each week builds on the last. By Week 3 you should have a complete Stage 1-3 pass for a real workflow.

5. **Share the output with your manager** — the Concept Check and Workflows Mapped sections make a strong case for why the time investment is worthwhile. Pair it with the [Business Case template](../../docs/personalise/business-case.md) if you need formal approval.

## What This Produces vs. What the Framework's Learning Path Produces

This prompt is a **pre-assessment** — it tells you what you need to learn. The framework's [Layer 2 Learning Path](role-path.md) is the **actual training** — it walks you through each stage with your org's context. Use this prompt first to understand your gaps, then use the learning path to close them.
