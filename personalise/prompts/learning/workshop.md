# Workshop Facilitator Plan Generator

You are producing a facilitated workshop plan for introducing the Agentic
Workflow Framework to a team. The output is a complete facilitator guide —
session structure, timing, exercises, facilitator notes, and post-workshop
reinforcement — adapted to the organisation's roles, systems, and context.

The workshop is designed to be run by a non-technical facilitator (team lead,
enablement manager, L&D partner) who has read the framework but is not an expert.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's roles, systems, constraints, and goals.
2. **Framework stages 1-3**: Read `docs/stages/01-decompose.md`,
   `docs/stages/02-select.md`, and `docs/stages/03-scope.md` for the
   methodology being taught.
3. **Quick Start**: Read `docs/getting-started/quick-start.md` for the
   simplified entry point used as pre-work.
4. **Application guide** (optional): If `personalise/output/APPLICATION-GUIDE.md`
   exists, read it for role playbooks and quick wins to reference during the
   workshop.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output

Write a single markdown file to `personalise/output/learning/workshop/workshop-plan.md`.

## Workshop Structure

Generate a complete facilitator plan with the following sections:

### Pre-work (15 minutes, asynchronous)

- Each participant reads the Quick Start page
- Each participant lists 3 workflows they perform regularly (use a shared
  document or form)
- The facilitator reviews submissions before the session to identify common
  themes and select a volunteer for the live example

Include the facilitator note: how to select the best volunteer (pick someone
whose workflows are visible to the group and likely to generate discussion, not
the most senior person).

### Session 1: Group Walkthrough — Stage 1 (30 minutes)

- Facilitator introduces the framework (5 min) — use the org-specific framing
  from the introduction prompt, not a generic explanation
- Live example: walk through Stage 1 using one participant's role (20 min)
  - Run the four-angle enumeration (time, trigger, output, system) as a group
  - Use the org's actual systems from the org config to populate the system angle
  - Demonstrate the trigger/steps/output validation test
  - Score 2-3 workflows live using the four signals
- Debrief: what surprised you? (5 min)

Facilitator notes:
- How to keep the group engaged (ask "what's missing?" not "does this look right?")
- How to handle a participant whose workflows are mostly Low automation potential
  (reframe as learning which workflows to protect from automation, not just which
  to automate)
- Time management cues (when to move on from enumeration)

### Session 2: Individual Practice — Stage 1 (30 minutes)

- Each participant completes their own Workflow Inventory Table
- Use the table format from Stage 1 with all eight columns
- Facilitator circulates and checks for common mistakes:
  - Listing responsibilities instead of workflows
  - Missing the frequency or time columns
  - All workflows scored the same (usually all High — push back on this)
- Final 5 minutes: each person shares their count (how many workflows?) and
  their most surprising find (the workflow they almost forgot)

Facilitator notes:
- Provide 2-3 worked examples from the org's roles as reference (generate these
  from the org config)
- Have the Quick Start mini-example visible for format reference

### Session 3: Pairs — Stage 2 Scoring (30 minutes)

- Participants pair up
- Each person scores their top 3 candidates across the six dimensions
- Partners challenge each other's scores: "Why did you rate Feasibility as 4
  when that system has no API?"
- Each pair calculates weighted composites and identifies a top candidate
- Final 5 minutes: 2-3 pairs share their top candidate and why

Facilitator notes:
- Provide a printed or shared scoring matrix with the dimension descriptions
- Common scoring mistakes to watch for: Impact based on pain rather than time
  saved, Feasibility assumptions about APIs that have not been verified,
  Organisational Readiness scored 5 when no one outside the pair has been
  consulted
- How to handle disagreements between partners (both scores are valid — discuss
  what drives the difference)

### Session 4: Group Discussion (30 minutes)

- Each pair shares their selected workflow (2 min per pair)
- Group identifies shared systems and dependencies: "Three of you chose
  workflows that pull from [CRM system] — building that integration once
  benefits all three"
- Group identifies the best first-build candidate for the team (not just each
  individual)
- Facilitator summarises: what the team will do next, who owns what, timeline
- Close with the takeaway checklist

Facilitator notes:
- Use the org's actual systems to identify shared infrastructure
- If multiple candidates score similarly, apply the tiebreaker criteria from
  Stage 2
- Capture commitments (who will complete their Stage 3 scope document, by when)

### Takeaway

Each participant leaves the workshop with:
- A completed Stage 1 Workflow Inventory Table
- A shortlisted Stage 2 candidate with scored rationale
- A buddy partner for the reinforcement exercises

### Spaced Repetition Schedule

The workshop is not a one-off event. Generate a reinforcement schedule with
15-minute micro-exercises:

**Week 1** — Revisit your Stage 1 inventory: add any workflows you missed,
refine descriptions, check for duplicates. Share your updated inventory with
your buddy.

**Week 2** — Revisit your Stage 2 scoring: has anything changed? Did you
discover a new quick win? Update your selection record. Meet your buddy for
20 minutes to compare progress.

**Week 4** — Progress check: where is your Stage 3 scope document? Share it
with your buddy for review. Identify blockers. Report status to the facilitator.

For each week, include:
- What to do (specific action, not "review your work")
- How long it takes (target 15 minutes)
- What to share and with whom
- What "done" looks like

### Peer Learning Structure — Buddy System

Generate the buddy system details:

**Pairing criteria**: Pair people from different roles where possible — a CSM
and an engineer will challenge each other's assumptions in ways two CSMs will
not. If the team is single-role, pair by sub-team or portfolio.

**Buddy responsibilities** (each person does this for their partner):
- Review the other person's workflow inventory for completeness and accuracy
- Challenge at least one scoring decision ("Why did you rate this Medium instead
  of High?")
- Identify one workflow the other person missed
- Meet for 20 minutes in Week 2 to compare progress

**Facilitator tracking**: How to monitor buddy engagement without
micromanaging — check whether buddy reviews were submitted, follow up with
pairs who went silent.

### Reflective Assessment Exercise

Include a comprehension check for facilitators to gauge understanding:

**The exercise**: "Explain in 3 sentences why you scored this workflow High on
one signal but Medium on another."

**What it tests**: Understanding of the selection methodology — not just
completion of the template. A good answer shows the participant understands
*why* signals differ, not just that they filled in different scores.

**How to use the responses**: Facilitators review answers to identify who needs
additional support. Red flags: all signals scored the same (did not engage with
the nuance), justification that restates the score without explaining why,
references to "gut feel" without connecting to the four signals.

## Adaptation Requirements

- Use the org's role names, system names, and industry jargon throughout
- Generate role-specific examples from the org config (not generic ones)
- If the org config includes target workflows in the goals section, use those
  as priming examples during the group walkthrough
- Adjust timing guidance for team size: a team of 4 needs less group discussion
  time than a team of 12
- If the org has regulatory constraints, include a note in Session 4 about
  checking automation candidates against compliance requirements

## Quality Standards

- The workshop plan must be runnable by a non-technical facilitator who has
  read the framework but is not an expert
- Facilitator notes should address the three most common failure modes the
  facilitator will encounter (participants listing responsibilities instead of
  workflows, scoring inflation, and difficulty distinguishing HIL from AUTOMATE)
- Timing must be realistic — a 30-minute session with 10 minutes of
  instructions, 15 minutes of work, and 5 minutes of debrief is tight but
  achievable. A 30-minute session with 20 minutes of instructions and 10
  minutes of work is not useful
- The spaced repetition schedule must have concrete deliverables, not vague
  "review your work" instructions
