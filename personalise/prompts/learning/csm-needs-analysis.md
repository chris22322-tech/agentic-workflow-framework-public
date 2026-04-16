# CSM Learning Needs Analysis Prompt

This prompt reads the entire framework and identifies what a Customer Success Manager needs to know to apply it to their work. The output is a generic needs analysis that becomes the basis for a CSM learning pathway.

---

## The Prompt

```
You are an instructional designer building a learning pathway for Customer
Success Managers who want to use the Agentic Workflow Framework.

Read the entire framework documentation in the docs/ directory. Also read the
CSM-relevant worked example (worked-example/) and the personalisation section
(personalise/).

Then produce a comprehensive learning needs analysis answering:

## 1. What does a CSM need to UNDERSTAND?

For each concept in the framework, assess:
- Is this something a CSM needs to understand deeply, understand at a surface
  level, or can safely ignore?
- WHY does a CSM need this concept? What goes wrong in their work if they
  skip it?

Organise by category:

### Concepts CSMs must understand deeply
These are the concepts a CSM will actively use in their day-to-day application
of the framework. They need to be able to explain them, apply them, and teach
them to a colleague.

### Concepts CSMs need surface-level awareness of
These are concepts a CSM will encounter but does not need to master. They need
to recognise the term, understand roughly what it means, and know when to ask
an engineer for help.

### Concepts CSMs can safely ignore
These are implementation details that belong to the engineer. A CSM who tries
to learn these will waste time and may be intimidated out of using the framework.

## 2. What does a CSM need to be able to DO?

List the specific skills — not knowledge, but capabilities — that the framework
requires from a CSM. For each skill:
- Describe the skill in action (what it looks like when someone does it well)
- Describe the common failure mode (what it looks like when someone does it badly)
- Identify where in the framework this skill is exercised (which stage, which artifact)
- Assess whether most CSMs already have this skill from their CS work, or whether
  it is genuinely new

Organise into:
- Skills CSMs already have (from their CS work) that transfer directly
- Skills CSMs already have but need to apply differently
- Genuinely new skills the framework introduces

## 3. What are the knowledge prerequisites?

What does a CSM need to know BEFORE starting the framework? Not technical
prerequisites (those are in the prerequisites page) — domain knowledge and
professional skills:
- What CS domain knowledge is assumed?
- What process documentation skills are assumed?
- What collaboration skills are needed for the Stage 3→4 handoff?
- What evaluation skills are needed for Stage 6 participation?

For each prerequisite, identify:
- Whether most CSMs with 2+ years of experience would have this
- What to do if they don't (is there a way to build it quickly?)

## 4. What are the common misconceptions?

Based on the framework content, what will CSMs most likely misunderstand or
get wrong? These are not mistakes of execution but mistakes of mental model.

For each misconception:
- State the misconception clearly ("CSMs often think X")
- Explain why it is wrong ("The framework actually requires Y because Z")
- Identify which framework page or section addresses this
- Suggest how a learning pathway should pre-empt this misconception

Think about misconceptions like:
- About what "automation" means (replacing them vs augmenting them)
- About what the agent can and cannot do (magic vs structured tool)
- About the level of detail required in scoping
- About their role during evaluation (passive reviewer vs active evaluator)
- About what happens after the agent is built (set and forget vs iterate)

## 5. What is the minimum viable knowledge?

If a CSM has exactly 4 hours to prepare, what is the absolute minimum they
need to know to complete Stages 1-3 for one workflow and hand off to an
engineer? Strip everything else away. What are the 10-15 things that, if
they understand these, they can produce a usable scope document?

List them in order of importance with one sentence each.

## 6. What does the CSM NOT need to know?

Explicitly list the framework content that a CSM should skip or skim. This is
as important as what they need to learn — the framework is 40+ pages and a CSM
who tries to read everything will either give up or waste time on irrelevant
technical content.

For each "skip this" recommendation:
- Name the specific page or section
- Explain why it is not relevant for a CSM
- Note if there is any part of that page they SHOULD read (e.g., "skip Stage 5
  entirely EXCEPT the 'If You're the Domain Expert' section")

## 7. What is the learning sequence?

Given everything above, what order should a CSM learn these concepts and skills?
Not a week-by-week plan yet — just the logical sequence:
- What must come first (foundational concepts)
- What builds on what (dependencies)
- What can be learned just-in-time (only needed when they reach that stage)
- What can be skipped on first pass and revisited later

Produce a numbered sequence of 15-20 learning items, each with:
- The concept or skill
- Why it comes at this position in the sequence
- How long it takes to learn (15 min / 30 min / 1 hour / 2+ hours)
- The framework page(s) that teach it

## 8. Assessment criteria

How would you know a CSM has learned enough to use the framework effectively?
Define 5-7 observable indicators — things you could check by looking at their
Stage 1-3 artifacts:
- What does a good Stage 1 inventory look like from a CSM? (What distinguishes
  "this person understood the methodology" from "this person just listed their
  responsibilities"?)
- What does a good Stage 2 selection look like?
- What does a good Stage 3 scope document look like?
- What does effective Stage 6 evaluation participation look like?

For each indicator, describe what "meets the bar" looks like and what
"needs more work" looks like.

## Output format

Produce the analysis as a structured markdown document with clear headers
for each of the 8 sections above. Use tables where they add clarity. Be
specific — name framework pages, sections, and concepts by name. Do not
be vague ("understand the methodology" is not useful; "understand why the
Specificity Test exists and be able to apply it to their own decision
logic entries" is useful).

Write to: personalise/output/learning/csm-needs-analysis.md
```

---

## What This Produces

A generic CSM learning needs analysis — not tailored to any individual, but
to the CSM role. It identifies:

- What CSMs need to deeply understand vs skim vs skip
- Which skills transfer from their CS work and which are genuinely new
- The minimum viable knowledge for a 4-hour time investment
- Common misconceptions to pre-empt in training
- The logical learning sequence with time estimates
- Observable assessment criteria for "this CSM is ready"

This document becomes the input for building the actual CSM learning pathway
(lessons, exercises, worked examples, assessments).
