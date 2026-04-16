# Layer 2: Personalised Learning

!!! tip "One-file shortcut"
    Use `personalise/PERSONALISE-L2-TRAINING-MATERIALS.md` — one file to open, edit, and run with any AI CLI (Gemini, Claude, ChatGPT). [Quick start →](index.md#quick-start-one-file-one-command)

Generate role-specific training materials tailored to your organisation. Each role gets a personalised learning path with worked examples grounded in their actual workflows — not generic ones.

!!! tip "New to personalisation?"
    Walk through the [interactive Personalisation Guide](../learning/personalise/01-why-personalise.html) first — it explains the three layers, what you get, and how the process works in 4 visual pages (~50 minutes). Then come back here to run the prompts.

!!! tip "Looking for the generic training?"
    The framework includes [ready-to-use learning pathways](../enablement/index.md) that work for any organisation — no personalisation needed. Start there if you want to learn the framework quickly. Come back here when you want training materials that reference your specific systems, workflows, and roles.

## What this costs

| Layer | Input tokens | Output tokens | Estimated cost (Claude Sonnet) | Estimated cost (Gemini Pro) |
|---|---|---|---|---|
| **Layer 2** (per role) | ~30-50K | ~15-25K | $1.00-3.00 | $0.30-0.75 |

For a team of four roles, expect $4-12 total. Running the workshop prompt adds another $1-2.

## Prerequisites

- [x] Layer 1 completed: `org-config.yaml` filled in
- [ ] Optionally: Layer 1 application guide generated (provides richer context for learning materials)

---

## What you get

For each role in your org config, the learning prompts generate:

**Role Introduction**
:   "You are a [role] at [company]. Here is how this framework applies to your work." Grounded in their actual responsibilities, not generic.

**Guided Stage Walkthroughs (Stages 1-3)**
:   A facilitator script that walks the person through each stage. Pre-populated with 3-5 example workflows from their domain to prime the pump. Includes prompts like "What do you do every Monday morning?" and "What report takes you the longest?" Each walkthrough embeds 2-3 inline comprehension checks — quick questions that force the learner to distinguish concepts before continuing (e.g., "Before you continue — which of these is a workflow and which is a responsibility?"). These catch drift early, before it compounds into flawed artifacts.

**Personalised Worked Example**
:   A complete Stage 1-3 walkthrough using a workflow from their role. Same structure as the [CSM health review example](../worked-example/index.md), but using their workflow, their systems, their decision points.

**Practice Exercises**
:   "Now do it yourself" exercises for each stage. Stage 1: "List your workflows using the inventory table." Stage 2: "Score your top 3 candidates." Stage 3: "Map your chosen workflow step by step."

**Calibration Exercises**
:   One per stage. Each presents a deliberately flawed artifact for the learner to critique before they build their own. The learner identifies errors, then compares their assessment against a reference answer with explanations. This teaches evaluation criteria experientially — learners internalise what "good" looks like by diagnosing what "wrong" looks like first.

**Assessment Rubric**
:   How to evaluate whether someone's artifacts are "good enough." Based on the framework's guiding questions and common mistakes, adapted to the org's context.

### Calibration exercise format

Each calibration exercise follows the same three-step pattern: review a flawed artifact, identify errors, then check your diagnosis against the reference answer.

??? example "Stage 1 — Spot the non-workflows"

    **Flawed artifact**: An inventory table where some entries are responsibilities ("stakeholder management", "quality assurance") rather than workflows (repeatable sequences with a trigger and an output).

    **Learner task**: Mark each row as *workflow* or *not a workflow* and explain why.

    **Reference answer**: Reveals which entries are responsibilities masquerading as workflows, explains the distinguishing criteria (Does it have a trigger? Does it produce an output? Can you walk through its steps?), and shows how to decompose a responsibility into its constituent workflows.

    !!! tip "Comprehension check to embed in the Stage 1 walkthrough"
        *Before you continue — look at these two items: (a) "Prepare the monthly client report" and (b) "Client relationship management." Which is a workflow and which is a responsibility? What makes them different?*

??? example "Stage 2 — Detect scoring bias"

    **Flawed artifact**: A selection record where the scorer has conflated feasibility with desire — a workflow scores high on "AI readiness" because the scorer *wants* it automated, not because the workflow's characteristics actually support automation. Another workflow is scored low on "impact" despite clear time savings, because the scorer finds it boring.

    **Learner task**: Identify which scores are biased, explain the bias, and re-score with justification.

    **Reference answer**: Walks through each biased score, names the specific bias (desire bias, familiarity bias), and provides the corrected score with evidence-based reasoning.

    !!! tip "Comprehension check to embed in the Stage 2 walkthrough"
        *Before you score — a colleague rates "Email triage" as 9/10 for AI readiness because "AI is great at email." Is this score evidence-based or assumption-based? What evidence would you need?*

??? example "Stage 3 — Find the missing boundaries"

    **Flawed artifact**: A scope document that maps workflow steps but omits decision points, exception paths, and the human/AI boundary — it reads as a flat task list rather than a structured process map with clear automation boundaries.

    **Learner task**: Identify what's missing (decision points, exception handling, boundary definitions) and mark where in the document they should appear.

    **Reference answer**: Shows the complete scope document with decision points, exception paths, and human/AI boundaries annotated. Explains why each omission matters — a flat task list produces an automation that breaks on the first exception.

    !!! tip "Comprehension check to embed in the Stage 3 walkthrough"
        *Before you continue — your scope document lists "Review the report" as a single step. Is this specific enough to define an automation boundary? What sub-steps might be hidden inside it?*

---

## Generate a learning path for a single role

Choose whichever option matches your setup. All three produce the same output.

=== "Option A: Interactive (paste into AI chat)"

    1. Open your AI assistant (Claude, ChatGPT, or similar)
    2. Paste the contents of `personalise/prompts/learning/role-path.md`
    3. Paste the contents of your `org-config.yaml`
    4. Attach or paste the framework stage files from `docs/stages/` (01-decompose.md through 03-scope.md)
    5. Specify which role to generate for
    6. The AI produces the learning path

    !!! tip
        For best results, also attach one of the worked examples (e.g., `docs/worked-example/decompose.md`, `select.md`, `scope.md`) as a structural reference.

=== "Option B: CLI (Claude Code)"

    ```bash
    claude -p "$(cat personalise/prompts/learning/role-path.md)" \
      --allowedTools Read,Write,Glob,Grep \
      --max-turns 20
    ```

    The AI reads the framework docs and org config, then writes the learning path to `personalise/output/learning/{role-name}/`.

=== "Option C: Web-based (zero tooling)"

    1. Open Claude.ai or ChatGPT in your browser
    2. Paste the contents of your `org-config.yaml`
    3. Paste the contents of `personalise/prompts/learning/role-path.md`
    4. Paste the framework stage files (or upload them as attachments)
    5. Tell it which role to generate for
    6. Copy the output into markdown files and save them

Output: `personalise/output/learning/{role-name}/`

```
personalise/output/learning/
├── {role-1-name}/
│   ├── introduction.md
│   ├── stage-1-walkthrough.md
│   ├── stage-2-walkthrough.md
│   ├── stage-3-walkthrough.md
│   ├── worked-example.md
│   ├── exercises.md
│   ├── calibration-exercises.md
│   └── assessment-rubric.md
├── {role-2-name}/
│   └── ...
└── workshop/
    └── workshop-plan.md
```

---

## Generate learning paths for all roles at once

```bash
for role in "Account Manager" "Business Analyst" "Engineering Lead"; do
  claude -p "Generate learning path for role: $role. $(cat personalise/prompts/learning/role-path.md)" \
    --allowedTools Read,Write,Glob,Grep \
    --max-turns 20
done
```

Replace the role names with those from your `org-config.yaml`.

---

## Generate a standalone worked example

Use `personalise/prompts/learning/worked-example.md` to generate a complete Stage 1-3 worked example for any role + workflow combination. You provide:

- Role name and description
- Workflow name and brief description
- Key systems involved

The AI produces a complete Stage 1-3 worked example following the same structure as the [CSM health review example](../worked-example/index.md): inventory table (for the role), selection record (scoring the workflow), and scope document (full step-by-step map with boundaries).

This is the most reusable prompt — a team lead can generate 5-10 worked examples for different roles and workflows in a single session.

=== "CLI"

    ```bash
    claude -p "$(cat personalise/prompts/learning/worked-example.md)" \
      --allowedTools Read,Write,Glob,Grep \
      --max-turns 20
    ```

=== "Interactive"

    1. Paste the contents of `personalise/prompts/learning/worked-example.md`
    2. Paste the contents of your `org-config.yaml`
    3. Paste the framework stage files and at least one worked example for structural reference
    4. Specify the role, workflow, and key systems

---

## Generate a team workshop

Use `personalise/prompts/learning/workshop.md` to generate a facilitated 2-hour workshop plan with facilitator notes, group exercises, and individual practice time.

=== "CLI"

    ```bash
    claude -p "$(cat personalise/prompts/learning/workshop.md)" \
      --allowedTools Read,Write,Glob,Grep \
      --max-turns 15
    ```

=== "Interactive"

    1. Paste the contents of `personalise/prompts/learning/workshop.md`
    2. Paste the contents of your `org-config.yaml`
    3. The AI produces a workshop plan adapted to your roles and systems

Output: `personalise/output/learning/workshop/workshop-plan.md`

The workshop includes a spaced repetition schedule (micro-exercises at weeks 1, 2, and 4), a peer learning structure (buddy pairs who review each other's work), and a reflective assessment exercise for facilitators to gauge understanding.

---

## Learning Modalities

The workshop above assumes synchronous, co-located delivery. For distributed teams, larger rollouts, or participants who cannot attend live sessions, adapt the format.

### Video walkthrough scripts

Each stage has a natural 10-minute screencast structure. A facilitator records one per stage using the personalised worked example as the on-screen content. These become the async alternative to the live workshop.

**Script template** (per stage):

| Segment | Duration | Content |
|---|---|---|
| Context | 1 min | "You're a [role] at [company]. Here's the workflow we're mapping." |
| Walkthrough | 6 min | Work through the stage using the personalised worked example, narrating decisions as you go |
| Common mistakes | 2 min | Show the 2-3 mistakes from the assessment rubric and how to avoid them |
| Your turn | 1 min | "Pause this video. Open your template and do the same for your workflow. Come back when you're done." |

!!! tip "Generating video scripts with AI"
    Add this to your `workshop.md` prompt: *"Also generate a 10-minute video walkthrough script for each stage, using the worked example as the screencast content. Format as a two-column facilitator script with on-screen actions in the left column and spoken narration in the right column."*

    The AI produces a ready-to-record script. The facilitator reads it while screen-sharing the worked example — no improvisation required.

### Async learning path

Sequence the written materials into a self-paced path with check-in points. This replaces the live workshop for participants who cannot attend synchronously.

| Step | Material | Exercise | Check-in |
|---|---|---|---|
| 1 | Read Quick Start | List 3 of your workflows in a shared doc | Facilitator reviews list within 48 hours |
| 2 | Watch Stage 1 video (or read stage-1-walkthrough) | Complete your Workflow Inventory Table | Buddy reviews inventory, flags gaps |
| 3 | Watch Stage 2 video (or read stage-2-walkthrough) | Score your top 3 candidates | Facilitator reviews scores, challenges one rating async |
| 4 | Watch Stage 3 video (or read stage-3-walkthrough) | Draft scope document for your top candidate | Buddy reviews scope, facilitator signs off |

**Facilitator role in async mode**: Review artifacts within 48 hours of submission. Leave written feedback using the assessment rubric. Flag participants who stall at Step 2 — this is where most drop-off happens.

**Completion target**: 2 weeks from start to Step 4 sign-off, with no more than 30 minutes per step.

### Cross-timezone workshops

For teams spanning multiple time zones (e.g., London, Singapore, Sydney), replace the 2-hour synchronous block with a split format:

**Async pre-work** (45 minutes, individual)

- Read the Quick Start page
- Watch the Stage 1 video walkthrough (or read the written walkthrough)
- Complete the Stage 1 Workflow Inventory Table
- Submit the inventory to the shared document before the synchronous session

**Synchronous session** (60 minutes)

- Skip the Stage 1 walkthrough — participants have already done it
- Open with a 10-minute gallery walk: review 2-3 submitted inventories as a group
- Run Session 3 (Stage 2 scoring in pairs) and Session 4 (group discussion) from the standard workshop plan
- Close with commitments and buddy assignments

!!! note "Scheduling the synchronous session"
    For a London/Singapore/Sydney spread, the only viable overlap is typically 08:00–09:00 GMT (16:00–17:00 SGT, 19:00–20:00 AEDT). A 60-minute session fits this window. If there is no viable overlap, run two regional sessions and share outputs between groups asynchronously.

This split format covers the same ground as the full 2-hour workshop but requires only 60 minutes of synchronous time.

---

## Drive adoption across the team

Two additional prompts support long-term adoption:

### Champion programme

`personalise/prompts/learning/champion-programme.md` generates a champion programme for driving adoption: champion selection criteria, a structured training path, defined responsibilities, and a monthly check-in template.

```bash
claude -p "$(cat personalise/prompts/learning/champion-programme.md)" \
  --allowedTools Read,Write,Glob,Grep \
  --max-turns 15
```

### Facilitator development path

The champion programme identifies *who* drives adoption. This section addresses the next problem: turning champions into facilitators who can run workshops independently — critical once you're rolling out beyond a single team or location.

#### Progression model

Each aspiring facilitator follows a three-stage progression:

- [x] **Shadow**: Observe a full workshop run by an experienced facilitator. Note pacing, how exercises are introduced, and how questions are handled.
- [ ] **Co-facilitate**: Run at least one workshop section (e.g., the Stage 1 group exercise) alongside the experienced facilitator, who provides live feedback.
- [ ] **Solo**: Deliver a full workshop independently. An experienced facilitator observes and completes the observation checklist below.

!!! tip "Observation checklist (for the observer during a solo session)"
    Use this as a lightweight scoring sheet during the solo facilitation:

    - [ ] Opens with clear framing: what the framework is, what participants will leave with
    - [ ] Explains each stage before the exercise, not during
    - [ ] Gives participants enough silent working time (does not rush exercises)
    - [ ] Checks understanding before moving on ("Show me your inventory table — does everyone have at least 3 rows?")
    - [ ] Handles questions without dismissing them or going off-track
    - [ ] Closes with concrete next steps and the reinforcement schedule

#### Handling common objections

Facilitators will encounter the same objections repeatedly. Prepare for these rather than improvising:

| Objection | What's behind it | How to respond |
|---|---|---|
| "My workflow is too unique for a generic framework" | Fear of oversimplification | "The framework doesn't simplify your workflow — it maps it in detail first. Let's try Stage 1 on one of yours and see whether it captures the nuance." |
| "I don't trust AI to do this" | Loss of control, quality concerns | "You're not handing anything over. Stage 3 defines exactly where AI helps and where it doesn't. You set the boundaries." |
| "I already know how I work — I don't need to document it" | Perceived busywork | "The inventory often surfaces steps you do on autopilot. The value isn't documenting what you know — it's finding what you've stopped noticing." |
| "We tried something like this before and it didn't stick" | Change fatigue | "Fair. What was missing last time? This framework is designed to be completed in stages, not adopted all at once. You start with one workflow." |

#### Certification criteria

A facilitator is certified to run workshops independently when they meet all of the following:

1. **Personal completion**: Have completed Stages 1-3 themselves on at least one real workflow (not a practice exercise)
2. **Facilitation reps**: Have facilitated 2+ workshops (co-facilitated or solo) with participant feedback scores averaging 4/5 or above
3. **Observer sign-off**: An experienced facilitator has completed the observation checklist during a solo session with no critical gaps
4. **Objection handling**: Can articulate responses to at least 3 of the 4 common objections above without referring to notes

!!! note "Scaling guideline"
    One certified facilitator can comfortably support 3-4 workshops per month. For rollouts targeting 50+ people across multiple teams, aim for at least 2-3 certified facilitators before starting the main wave.

### Community of practice

The workshop creates initial capability. The champion programme creates individual change agents. Neither sustains peer learning — the mechanism that turns isolated completions into organisational knowledge. A community of practice provides the ongoing cadence where teams learn from each other's artifacts, not just their own.

Use `personalise/prompts/learning/workshop.md` with the additional instruction below to generate a community of practice plan tailored to your org.

!!! tip "Add this to your workshop prompt"
    Append to your `workshop.md` prompt: *"Also generate a community of practice plan including: a bi-weekly show-and-tell format, a shared artifact library structure, and a Slack/Teams channel template with weekly prompts. Tailor all examples to our organisation's roles and workflows."*

#### Bi-weekly show-and-tell

A 30-minute session, every two weeks, open to anyone who has completed the workshop. One team presents, everyone else learns.

| Segment | Duration | What happens |
|---|---|---|
| Present | 10 min | One team walks through a completed Stage 1-3 artifact set — what the workflow was, what they learned mapping it, where they drew the human/AI boundary |
| Group critique | 10 min | Attendees ask questions using the assessment rubric as a lens: "How did you score feasibility?" "What exception paths did you find in Stage 3?" |
| Pattern harvest | 5 min | Facilitator captures reusable patterns: scoring heuristics that worked, scope document structures worth copying, common pitfalls the team avoided |
| Next steps | 5 min | Identify who presents next fortnight. Flag any artifacts worth adding to the shared library |

!!! note "Scheduling"
    Bi-weekly is the minimum viable cadence. Weekly burns out presenters; monthly loses momentum. If attendance drops below 5 people, switch to monthly and make each session a double feature (two teams present).

#### Shared artifact library

A folder (shared drive, SharePoint, Notion — whatever your org already uses) where completed artifacts are catalogued for reuse. Not a template library — a library of *real, completed examples* from your organisation.

**Folder structure**:

```
shared-artifacts/
├── stage-1-inventories/
│   ├── {team-name}-{date}.md
│   └── ...
├── stage-2-selections/
│   ├── {team-name}-{date}.md
│   └── ...
├── stage-3-scopes/
│   ├── {team-name}-{date}.md
│   └── ...
└── patterns/
    ├── scoring-heuristics.md
    └── common-exception-paths.md
```

The `patterns/` folder is curated by champions. After each show-and-tell, the facilitator adds any harvested patterns. Over time this becomes the most valuable folder — a cross-team pattern library of what actually works in your organisation.

!!! warning "Quality gate"
    Only add artifacts that have been reviewed against the assessment rubric and scored as "good enough." A library of unchecked artifacts teaches bad habits faster than no library at all.

#### Slack/Teams channel

Create a dedicated channel (e.g., `#workflow-framework-practice`) with a weekly prompt rotation to keep peer learning alive between show-and-tell sessions.

**Weekly prompt examples** (rotate these):

- *Share one workflow you considered but decided NOT to automate — and why.*
- *What was the hardest human/AI boundary decision you made this week?*
- *Post your Stage 2 scoring for a workflow. Challenge someone else's scores.*
- *What exception path surprised you when you mapped a workflow in Stage 3?*
- *Share a "before and after" — how your understanding of a workflow changed from Stage 1 to Stage 3.*

Pin a message at the top linking to the shared artifact library and the show-and-tell schedule. Champions take turns posting the weekly prompt each Monday.

### Adoption tracker

`personalise/prompts/learning/adoption-tracker.md` generates a tracking template pre-populated with your org's roles and target workflows, with realistic targets based on team size.

```bash
claude -p "$(cat personalise/prompts/learning/adoption-tracker.md)" \
  --allowedTools Read,Write,Glob,Grep \
  --max-turns 10
```

---

## Prompt inventory

| Prompt | What it generates | When to use it |
|---|---|---|
| `role-path.md` | Complete learning path for one role (8 files, including calibration exercises) | Per role — run once per role in your org config |
| `worked-example.md` | Stage 1-3 worked example for a specific role + workflow | Ad hoc — generate examples for any combination |
| `workshop.md` | 2-hour facilitated workshop plan with reinforcement schedule | Once per team — when introducing the framework |
| `champion-programme.md` | Champion selection, training, responsibilities, check-in template | Once — when setting up your adoption programme |
| `adoption-tracker.md` | Adoption metrics tracker pre-populated with your roles and targets | Once — when you want to measure progress |
| `assessment-rubric.md` | Quality rubric for evaluating completed artifacts by stage | Once — for facilitators and reviewers |
