# Build Your Business Case

You have completed Stages 1-2. You know which workflow to automate. Now you need approval — budget, time, engineering support, or just a green light from your manager.

The artifacts you already have — workflow inventory, time estimates, selection scores, risk assessment — contain everything a business case needs. This page gives you a template to package those findings into a one-page investment case that speaks the language of leadership.

---

## The One-Page Business Case Template

Copy this template and fill it in using the mapping table below.

```markdown
# Business Case: [Workflow Name] Automation

## The Problem
[1-2 sentences: what the workflow is, who does it, how often, how long it takes]

Current state: [X] hours/month spent by [N] people on [workflow name].
This time is spent on [data gathering / synthesis / reporting / coordination]
that follows the same pattern each time.

## The Proposal
Use the Agentic Workflow Framework to build an AI agent that handles the
repetitive parts of this workflow, with human review at [N] checkpoints.

## Expected Impact
- **Time saved:** [X] hours/month (based on Stage 2 Impact score of [N/5])
- **Per-cycle reduction:** From [X] hours to approximately [Y] hours
  ([Z]% of current time is automatable based on Stage 3 boundary analysis)
- **Payback period:** The agent build takes [N] engineering days.
  At [X] hours saved/month, the investment pays back in [M] months.

## What We Need
- **Time:** [N] hours of workflow owner time for Stages 1-3 (already complete / in progress)
- **Integration setup:** [N] weeks for API access, security reviews,
  OAuth provisioning, and IT approvals for [systems from data inventory].
  Start this during Stage 3 scoping — it is almost always the longest lead item.
- **Agent build:** [N] days for Stages 4-5 (design and build the agent logic)
- **Evaluation and iteration:** [N] weeks for Stage 6 (test cases,
  parallel runs, refinement)
- **LLM budget:** Approximately $[X]/month for [model] API calls
  ([N] runs × [M] LLM calls per run × estimated token cost)

## Risk Assessment
- **What if the agent gets it wrong?** [Risk Tolerance score rationale from Stage 2].
  All outputs are reviewed by [role] before [distribution/action]. The blast
  radius of an error is [internal rework / client-visible / irreversible].
- **What if we do nothing?** The team continues spending [X] hours/month on
  this workflow. Meanwhile, [N] team members are already using ChatGPT/Claude
  ad hoc for parts of this work — without guardrails, data classification,
  or quality control. A structured approach is safer than the status quo.

## Timeline
| Week | Milestone |
|---|---|
| 1 | Scope document complete (Stage 3). Begin integration access requests. |
| 1-4 | Integration setup: API access, security reviews, token provisioning (ongoing) |
| 3-4 | Agent logic design and build (Stages 4-5) — once integrations are available |
| 5 | Evaluate with test cases (Stage 6) |
| 6-7 | Parallel run alongside manual process |
| 8+ | Switch to agent-assisted workflow |
```

---

## How to Fill It In

Every field maps directly to an artifact you already produced in Stages 1-2, or will produce in Stage 3. Use this mapping:

| Business case field | Source artifact |
|---|---|
| Time saved | Stage 2: Impact score x Frequency x Avg Time |
| Risk assessment | Stage 2: Risk Tolerance score + justification |
| Systems needed | Stage 3: Data Inventory (or Stage 1: Systems Touched) |
| Integration setup | Highly variable: 1 week to 2 months depending on org security processes, number of systems, and IT approval workflows. Start during Stage 3 — do not wait until build. |
| Agent build estimate | 2-5 days for a first agent (the logic itself, once integrations are in place) |
| Evaluation and iteration | 1-2 weeks for test cases, parallel runs, and refinement |
| LLM budget | Personalise layer cost guidance |
| "What if we do nothing?" | Frame around ad hoc AI use already happening |

If you have completed Stage 2, you can fill in the template in under 30 minutes. The fields that reference Stage 3 artifacts (per-cycle reduction percentage, systems list) can be left as estimates and updated once you complete Stage 3.

---

## The "What If We Do Nothing?" Framing

This section of the business case is critical — and most people underwrite it.

In most organisations, people are already using ChatGPT or Claude for parts of their work — pasting client data into a chat window, copying outputs into reports, using AI to draft emails or summarise documents. This is happening without:

- **Data classification** — sensitive client data entering prompts without review
- **Quality control** — no consistent standard for AI-assisted output
- **Audit trails** — no record of what was generated vs. written by a human
- **Governance** — no organisational policy on which workflows are appropriate for AI assistance

A structured framework with data classification, human review checkpoints, and audit trails is not introducing risk — it is reducing the risk that already exists. Frame your business case accordingly: the question is not "should we use AI?" but "should we use AI with guardrails or without them?"

---

## Generating a Pre-Filled Business Case

If you want a head start, use the [business case prompt](prompts/business-case.md) to generate a pre-filled template from your Stage 1-2 artifacts. The prompt reads your workflow inventory, selection scores, and org config, then produces a draft business case that you review and adjust before presenting.

!!! tip "Tailor for your audience"
    If your manager cares about cost, lead with the payback period. If they care about risk, lead with the "what if we do nothing?" section. If they care about team capacity, lead with the time-saved figure. The template gives you all three — emphasise the one that resonates with your specific approver.
