# Business Case Generator

You are producing a pre-filled one-page business case for a specific workflow
automation. The audience is a team lead's manager or steering committee who
needs to approve budget, time, or engineering resources.

## Inputs

1. **Workflow Inventory**: Read `personalise/output/APPLICATION-GUIDE.md` or the
   user's Stage 1 Workflow Inventory Table for workflow details (name, frequency,
   average time, systems touched).
2. **Selection Decision Record**: The user's Stage 2 output — selected workflow
   name, composite score, dimension scores, and justification.
3. **Organisation config**: Read `personalise/org-config.yaml` for organisation
   context (role titles, systems, constraints).

If running in interactive mode, the user will paste these contents into the
conversation.

## Output Structure

Produce a completed business case using this exact structure:

### Business Case: [Workflow Name] Automation

#### The Problem

Write 1-2 sentences describing the workflow: what it is, who performs it, how
often, and how long it takes. Use the organisation's actual role titles and
system names.

Then state the current cost:
- Monthly hours = Time per occurrence x Monthly frequency x Number of instances
- Pull these figures directly from the workflow inventory

#### The Proposal

One paragraph: use the Agentic Workflow Framework to build an AI agent that
handles the repetitive parts of this workflow. Specify the number of human
review checkpoints based on the workflow's Risk Tolerance score:
- Risk Tolerance 1-2: review at every output step
- Risk Tolerance 3: review at key decision points
- Risk Tolerance 4-5: review at final output only

#### Expected Impact

Calculate from the Stage 2 scores and inventory data:
- **Time saved**: Monthly hours from the Impact calculation
- **Per-cycle reduction**: Estimate the automatable percentage based on the
  workflow structure. Data gathering and formatting steps are typically 70-90%
  automatable. Synthesis and judgement steps are 30-50% automatable (agent
  produces a draft, human refines).
- **Payback period**: Use 2-5 engineering days as the build estimate (2 days
  for Complexity 4-5, 3 days for Complexity 3, 5 days for Complexity 1-2).
  Calculate months to payback based on engineering day cost vs. hours saved.

#### What We Need

- **Time**: Stages 1-3 require approximately 4-8 hours of the workflow owner's
  time. Note which stages are already complete.
- **Engineering**: 2-5 days based on Complexity score (see above)
- **Access**: List all systems from the workflow inventory's "Systems Touched"
  column. Flag any with Feasibility concerns from Stage 2.
- **LLM budget**: Estimate based on workflow complexity:
    - Simple (Complexity 4-5): 3-5 LLM calls per run, ~$0.05-0.15 per run
    - Moderate (Complexity 3): 5-10 LLM calls per run, ~$0.15-0.50 per run
    - Complex (Complexity 1-2): 10-20 LLM calls per run, ~$0.50-2.00 per run
    - Multiply per-run cost by monthly frequency for monthly estimate

#### Risk Assessment

**What if the agent gets it wrong?** Use the Risk Tolerance score and its
rationale from Stage 2. State who reviews the output, what happens before it
reaches its audience, and what the blast radius of an error is.

**What if we do nothing?** Frame around ad hoc AI usage:
- State how many team members are likely already using ChatGPT/Claude for parts
  of their work (if the org has not banned AI tools, assume some usage)
- Note the absence of guardrails: no data classification, no quality control,
  no audit trail
- Frame the structured approach as risk reduction, not risk introduction

#### Timeline

Produce a week-by-week timeline:
- Week 1: Scope document (Stage 3) — if not already complete
- Weeks 2-3: Design and build (Stages 4-5)
- Week 4: Evaluate with test cases (Stage 6)
- Weeks 5-6: Parallel run alongside manual process
- Week 7+: Switch to agent-assisted workflow

Adjust if Stages 1-3 are already complete (compress the early weeks).

## Output

- **CLI mode**: Write to `personalise/output/BUSINESS-CASE.md`
- **Interactive mode**: Output in the conversation

## Quality Standards

- Maximum 1 page when rendered as a document — this is a one-page business case
- Use the organisation's actual name, role titles, and system names throughout
- All numbers must be derived from the Stage 1-2 artifacts — do not invent
  figures. If a figure cannot be calculated, use a clearly marked placeholder
  with the calculation method: "[X — calculate from Y]"
- Tone: professional, direct, factual. This is an internal approval document
- The "what if we do nothing?" section must reference ad hoc AI usage as the
  risk baseline — this is the key framing that distinguishes a proactive
  business case from a speculative one
