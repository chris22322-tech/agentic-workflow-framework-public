# Champion Programme Generator

You are producing a champion programme for driving adoption of the Agentic
Workflow Framework across a team. Champions are the people who bridge the gap
between "the team was trained" and "the team actually uses it." This prompt
generates the selection criteria, training path, responsibilities, and ongoing
cadence for a champion programme tailored to the organisation.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's roles, systems, constraints, team size, and goals.
2. **Framework stages**: Read `docs/stages/01-decompose.md` through
   `docs/stages/06-evaluate.md` for the full methodology (champions need to
   understand all six stages, not just the first three).
3. **Application guide** (optional): If `personalise/output/APPLICATION-GUIDE.md`
   exists, read it for the rollout plan and role playbooks — the champion
   programme should align with the rollout timeline.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output

Write a single markdown file to `personalise/output/learning/champion-programme.md`.

## Output Structure

### 1. Champion Selection Criteria

What makes a good champion. Generate criteria adapted to the org's context:

- **Curiosity about AI** — not expertise. Champions do not need to be technical;
  they need to be interested in how AI can change their work
- **Respected by peers** — their endorsement carries weight. Other team members
  ask them for advice or follow their lead
- **Comfortable with ambiguity** — early adoption involves rough edges. Champions
  cannot be people who need everything polished before they engage
- **Willing to dedicate 2-3 hours/week** — this is not a side project with zero
  time commitment. Be honest about what it requires
- **Span of roles** — at least one champion per role in the org config. A
  champion programme staffed entirely by one role type will not drive adoption
  across the team

Include anti-patterns: who should NOT be a champion (the most senior person by
default, someone voluntold by management, someone who views AI as a threat to
their role).

### 2. Champion Training Path

A structured onboarding for champions that covers:

**Week 1-2: Framework foundations**
- Complete all three non-technical stages (Decompose, Select, Scope) for their
  own role — using the learning path materials from the role-path prompt
- Review the worked examples to understand the target depth and quality

**Week 3-4: Technical orientation**
- Read Stages 4-6 (Design, Build, Evaluate) — not to become a builder, but to
  understand what happens after scoping so they can answer questions and set
  realistic expectations
- If the org has engineering support, meet with the engineering partner to
  understand the build process and timeline
- Complete a basic prompt engineering exercise: run one of the personalisation
  prompts (e.g., the worked-example prompt) and evaluate the output quality

**Week 5-6: Facilitation skills**
- Run a practice workshop session with 2-3 colleagues (using the workshop prompt
  output)
- Debrief with the programme lead: what worked, what did not, what questions
  came up that the materials do not cover

**Ongoing: Peer support**
- Review colleagues' Stage 1 inventories and provide feedback
- Be the first point of contact for questions about the framework
- Escalate blockers that require engineering support or management decisions

### 3. Champion Responsibilities

What a champion does on an ongoing basis:

- **Run team workshops** — facilitate the introductory workshop for their role
  group, using the workshop plan from the workshop prompt
- **Review colleagues' artifacts** — review Stage 1 inventories and Stage 2
  selections for quality and completeness, using the assessment rubric
- **Escalate blockers** — when someone is stuck because a system has no API, or
  a workflow is too complex to scope, or organisational readiness is blocking
  progress, the champion raises it
- **Share wins** — when an agent is working and saving time, the champion makes
  it visible to the team and leadership. Concrete numbers, not vague praise
- **Maintain the application guide** — as the team learns more about their
  workflows and systems, the application guide should be updated. The champion
  owns this maintenance
- **Attend monthly check-ins** — structured sync with other champions and the
  programme lead

### 4. Monthly Check-in Template

A structured agenda for champion check-ins. Generate a template with:

**Adoption metrics review** (10 min)
- How many people have completed Stage 1? Stage 2? Stage 3?
- How many scope documents have been handed to engineering?
- How many agents are in development? In production?
- Hours saved this month (if measurable)

**Blockers and escalations** (15 min)
- What is preventing progress? Categorise: technical (no API, data quality),
  organisational (no engineering capacity, no management support), knowledge
  (people stuck on a concept)
- For each blocker: who owns the resolution, what is the next action, when is
  the deadline

**New workflow candidates** (10 min)
- Has anyone identified a new workflow since the last check-in?
- Should the application guide's quick wins list be updated?

**Lessons learned** (10 min)
- What worked well this month? (Share across champions)
- What did not work? (Adjust approach)
- Any materials that need updating based on feedback?

**Next month's focus** (5 min)
- What is the priority for the next 4 weeks?
- Any workshops to schedule? Artifacts to review?

## Adaptation Requirements

- Use the org's role names and team structure throughout
- Scale the champion count recommendation to team size: 1 champion per 5-8
  people is a reasonable ratio
- If the org config shows engineering support is external or shared, adjust the
  champion's technical orientation to account for limited engineering access
- If the org has regulatory constraints, include a responsibility for the
  champion to verify that automation candidates comply with relevant policies

## Quality Standards

- The programme must be realistic — do not propose a champion training path
  that requires 40 hours of preparation before someone can start helping
  their colleagues
- The check-in template must be usable as-is — copy it into a meeting agenda
  and run it
- Responsibilities must be specific enough that a champion knows what "done"
  looks like for each one
