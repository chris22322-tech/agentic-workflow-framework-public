# Adoption Tracker Generator

You are producing a tracking template for measuring adoption progress of the
Agentic Workflow Framework across a team. The tracker is pre-populated with the
organisation's roles and target workflows, with realistic targets based on team
size and the rollout timeline from the org config.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's roles, systems, goals, team capability, and timeline.
2. **Application guide** (optional): If `personalise/output/APPLICATION-GUIDE.md`
   exists, read it for the rollout plan, quick wins, and role playbooks —
   these inform what realistic adoption targets look like.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output

Write a single markdown file to `personalise/output/learning/adoption-tracker.md`.

## Output Structure

### 1. Programme-Level Metrics

Generate a tracker table pre-populated with the org's context:

| Metric | Week 1 | Week 4 | Week 12 | Target |
|---|---|---|---|---|
| People completed Stage 1 | | | | |
| Workflows inventoried | | | | |
| Selection records completed | | | | |
| Scope documents completed | | | | |
| Agents in development | | | | |
| Agents in production | | | | |
| Hours saved/month | | | | |

**Populate the Target column** with realistic numbers based on:
- Number of roles in the org config × estimated people per role
- Number of target workflows from the goals section
- The org's timeline (e.g., "first agent in 3 months" from the goals section)
- Team capability (can they build Stages 4-6 themselves, or do they need
  engineering support?)

**Populate milestone columns** with progressive targets:
- Week 1: workshop completed, Stage 1 inventories drafted
- Week 4: Stage 1 inventories finalised, Stage 2 selections made, first Stage 3
  scope document in progress
- Week 12: first scope document handed to engineering, first agent in
  development or pilot

Be realistic about the pipeline: not every inventory leads to a selection, not
every selection leads to a scope document, not every scope document leads to a
build. Apply a funnel assumption: if 4 roles produce inventories, expect 3-4
selections, 2-3 scope documents, and 1-2 builds in the first quarter.

### 2. Per-Role Progress

For each role in the org config, generate a tracking section:

**Role: [Role Name]**

| Artifact | Status | Owner | Due Date | Notes |
|---|---|---|---|---|
| Stage 1: Workflow Inventory | Not started | | | |
| Stage 2: Selection Record | Not started | | | |
| Stage 3: Scope Document | Not started | | | |
| Handoff to engineering | Not started | | | |

Leave Owner and Due Date blank for the team to fill in. Pre-populate Notes
with relevant context from the org config (e.g., "This role's primary system
is [system] — check API availability before Stage 3").

### 3. Quick Wins Tracker

If the application guide or org config identifies target workflows or quick
wins, generate a dedicated tracking table:

| Workflow | Owning Role | Stage | Status | Blocker | Est. Hours Saved/Month |
|---|---|---|---|---|---|
| [workflow 1 from config] | [role] | Not started | | | |
| [workflow 2 from config] | [role] | Not started | | | |

Pre-populate with target workflows from the org config's goals section. If no
target workflows are specified, leave this section as a blank template with
example rows.

### 4. Health Indicators

Generate a simple RAG (Red/Amber/Green) health check the programme lead runs
monthly:

| Indicator | Green | Amber | Red |
|---|---|---|---|
| Participation | >80% of team has completed Stage 1 by Week 4 | 50-80% completed | <50% completed |
| Artifact quality | Assessment rubric scores are "done well" | Some artifacts "need improvement" | Red flags in multiple artifacts |
| Engineering pipeline | Scope documents flowing to engineering on schedule | Minor delays, pipeline not blocked | No scope documents handed off by Week 8 |
| Champion engagement | Champions running workshops and reviewing artifacts | Champions active but not running workshops | Champions disengaged or overloaded |
| Stakeholder support | Leadership aware and supportive | Leadership informed but not actively supporting | Leadership unaware or sceptical |

Adapt the thresholds to the org's size and timeline. A team of 4 has different
expectations than a team of 20.

### 5. Reporting Template

Generate a brief monthly status update template the programme lead can fill in
and share with leadership:

```
## Framework Adoption — Month [N] Update

**Overall status:** [Green/Amber/Red]

**Progress this month:**
- [X] people completed Stage 1 (target: [Y])
- [X] selection records completed
- [X] scope documents in progress
- [X] agents in development

**Wins:**
- [Concrete example of progress or time savings]

**Blockers:**
- [What is preventing progress and who owns the fix]

**Next month:**
- [Key milestone or deliverable expected]
```

## Quality Standards

- Targets must be realistic, not aspirational — a team of 4 with no prior AI
  experience and external engineering support will not have 3 agents in
  production by Week 12
- The tracker must be usable as-is — copy it into a spreadsheet or shared
  document and start filling in numbers
- Pre-populated content must reference the org's actual roles, systems, and
  target workflows from the config
- Include the funnel assumption explicitly so the programme lead understands
  that not every inventory leads to a build
