# Methodology Stages

The framework has six stages. Each stage has a defined purpose, required inputs, a concrete output artifact, and guiding questions. Work through them sequentially — each stage's output feeds the next.

Stages 1-3 are non-technical — any knowledge worker can complete them. Stages 4-6 require software engineering skills if your team uses a code-first agent framework; if your team uses a low-code builder, all six stages can be completed without writing code. See [How to Use This Framework](../getting-started/how-to-use.md) for guidance on which stages apply to your role, and [Choose a Platform](../getting-started/choose-a-platform.md) for current options.

```mermaid
graph LR
    S1[1. Decompose] --> S2[2. Select]
    S2 --> S3[3. Scope]
    S3 --> H["Handoff ↘"]
    H --> S4[4. Design]
    S4 --> S5[5. Build]
    S5 --> S6[6. Evaluate]

    style S1 fill:#4051b5,color:#fff
    style S2 fill:#4051b5,color:#fff
    style S3 fill:#4051b5,color:#fff
    style H fill:#7c4dff,color:#fff,stroke-dasharray: 5 5
    style S4 fill:#4051b5,color:#fff
    style S5 fill:#4051b5,color:#fff
    style S6 fill:#4051b5,color:#fff
```

## Thinking Stages (1-3)

### [1. Decompose](01-decompose.md)

Break a role down into a structured inventory of workflows, annotated with metadata that enables informed automation decisions. Most people can name their responsibilities but cannot enumerate the discrete, repeatable workflows within them.

### [2. Select](02-select.md)

Choose a single workflow to automate from the inventory. The goal is not to pick the most impressive target — it's to pick the one most likely to succeed and deliver value, given current constraints.

### [3. Scope](03-scope.md)

Map the chosen workflow in full detail as a human currently performs it, then draw an explicit boundary between what the agent will do and what stays human. A well-scoped workflow is straightforward to design and build; a poorly scoped one produces an agent that either does too little to be useful or too much to be trustworthy.

---

## Handoff: Scope → Design

If the person who completed Stages 1-3 is not the person who will execute Stages 4-6, you need a structured handoff. Skipping this produces a design that the workflow owner does not recognise and an engineer who guesses at intent. Thirty minutes of structured conversation prevents weeks of rework. (If you are using a low-code builder and completing all six stages yourself, you can skip the formal handoff — but still review the checklist questions below to sharpen your design thinking.)

!!! warning "When to use this"
    If the same person owns both scope and design, skim the checklist below and move on. If different people (or different teams) own each side, treat this as a required gate.

### Briefing the engineer

The workflow owner walks the engineer through the Workflow Scope Document from [Stage 3](03-scope.md). Cover these in order:

1. **The business problem** — Why this workflow matters, who it serves, and what failure looks like for the end user. Do not assume the engineer has organisational context.
2. **The step-by-step workflow map** — Walk through each step as you actually do it. Flag where you take shortcuts, apply judgement, or deviate from documented process.
3. **The automation boundary** — Explain why each step is tagged AUTOMATE, HUMAN-IN-THE-LOOP, or MANUAL. The rationale matters more than the tag.
4. **Error paths and edge cases** — These are the things that will bite during build. Explain what happens when inputs are missing, formats change, or upstream systems are down.
5. **Data inventory** — Where data lives, how you access it today, and any authentication or permission constraints the engineer will need to navigate.

### Questions the engineer should ask

The engineer should work through this checklist during or after the briefing. Do not proceed to Stage 4 until both parties are satisfied with the answers.

- [ ] For each AUTOMATE step: what does "done correctly" look like? How would you verify the output?
- [ ] For each HUMAN-IN-THE-LOOP step: what specifically does the human review? What are they approving or rejecting?
- [ ] Are there implicit ordering dependencies between steps that are not captured in the workflow map?
- [ ] Which steps have the highest variance in how long they take or how they are executed?
- [ ] What data is sensitive, regulated, or subject to access controls?
- [ ] Are there downstream consumers of this workflow's output who will be affected by automation?
- [ ] What is the minimum viable version — which steps could be deferred to a later iteration?

### 30-minute design review session

After the engineer produces a first-pass scope-to-action mapping (the first artifact in [Stage 4](04-design.md)), hold a 30-minute review with the workflow owner. Use this format:

| Time | Activity | Owner |
|------|----------|-------|
| 0-5 min | Engineer presents the proposed action mapping — which scope steps map to which actions, and where steps were consolidated or split | Engineer |
| 5-15 min | Workflow owner validates: does each action correspond to a recognisable unit of work? Are any steps missing, merged incorrectly, or split unnecessarily? | Workflow owner |
| 15-25 min | Walk through human-in-the-loop checkpoints together — the workflow owner confirms these are the right pause points and that the review criteria are correct | Both |
| 25-30 min | Agree on open items, assign owners, set a deadline for the final design document | Both |

!!! tip "Artefact"
    The output of this session is a **validated scope-to-action mapping** — annotated with any corrections from the workflow owner. Attach it to the design document as a sign-off record.

### Ownership during Stages 4-6

Once the handoff is complete, use this responsibility matrix:

| Activity | Workflow Owner | Engineer |
|----------|:-:|:-:|
| Writing the design document (Stage 4) | **Consulted** | **Responsible** |
| Validating scope-to-action mapping | **Responsible** | **Consulted** |
| Approving human-in-the-loop design | **Responsible** | **Consulted** |
| Implementation (Stage 5) | Informed | **Responsible** |
| Defining evaluation criteria (Stage 6) | **Responsible** | **Consulted** |
| Running evaluation tests (Stage 6) | Consulted | **Responsible** |
| Accepting final agent output | **Responsible** | Informed |

The workflow owner remains accountable for whether the agent faithfully represents their workflow. The engineer is accountable for whether it works technically. Neither can sign off alone.

---

## Building Stages (4-6)

### [4. Design](04-design.md)

Translate the scoped workflow into an agent architecture. This is where the human workflow map becomes an agent architecture — specifying what the agent does at each step, what data flows between steps, and where it pauses for human review.

### [5. Build](05-build.md)

Implement the designed agent. How you build it depends on your platform — code-first frameworks use code, low-code builders use a UI. This stage provides structural patterns and conventions — the specifics depend on your chosen platform, data sources, and environment.

### [6. Evaluate](06-evaluate.md)

Validate that the agent works correctly, handles edge cases, and produces output quality comparable to (or better than) the manual process. Establish a feedback loop for iterative improvement.
