# Getting Started

## What is this framework?

You have workflows you repeat every week — pulling data from three systems, compiling it into a report, sending it to someone who needs to make a decision. Each time, the steps are basically the same. The data changes, the context shifts slightly, but the *process* is the same process you ran last week and the week before that.

This framework is a step-by-step method for taking one of those repetitive workflows and building an AI agent that does most of the work for you — with you reviewing the important parts before anything goes out the door. An AI agent is a program that can take actions on its own — pulling data, analysing it, drafting outputs — but pauses for your review at the moments that matter.

It walks you through six stages: figuring out which of your workflows are worth automating, picking the best candidate, mapping exactly how that workflow works today, designing the agent, building it, and then testing it against real scenarios. Each stage produces something concrete — a document, a decision, a working tool — that feeds directly into the next stage. You do not need to be technical to start. The first three stages are pure thinking work: understanding your own job and making good decisions about what to automate. The last three stages are where the technical build happens. If your team uses a code-first agent framework, Stages 4-6 require engineering skills and you can hand them off to an engineer. If your team uses a low-code agent builder, you can complete all six stages yourself — no coding required.

The key idea is **human-in-the-loop**: the agent does the heavy lifting — gathering data, running calculations, drafting outputs — but it pauses at the moments that matter and waits for you to review before anything goes out. You stay in control of the decisions that require judgement. The agent handles the parts that are repetitive and time-consuming but do not actually need your expertise.

The goal is not to replace you. It is to give you back the hours you currently spend on work that follows the same pattern every time, so you can spend that time on the parts of your job that actually require your thinking.

Here is the process in plain language:

1. **List your workflows.** Write down every repeatable process you perform — the things with a trigger, a set of steps, and an output. Most people discover they have more than they thought.
2. **Pick the best candidate.** Score each workflow on how much time it takes, how often you do it, and how suitable it is for automation. Pick the one with the best combination.
3. **Map it in detail.** Walk through exactly how you do the workflow today, step by step. Mark which parts an agent could handle and where you need to stay in the loop.
4. **Design the agent.** Turn your workflow map into a technical specification an engineer can build from.
5. **Build it.** Implement the agent with the review checkpoints you defined.
6. **Test it.** Run the agent against real scenarios, measure how it does, and decide what to improve.

Steps 1-3 require no technical skills — just clear thinking about your own work. Steps 4-6 are where the technical build happens. With a code-first framework, you hand off to an engineer after Step 3. With a low-code builder, you can do all six steps yourself. See [Choose a Platform](choose-a-platform.md) for current options.

---

## Who is this for?

### Knowledge workers

**Customer Success Managers, Account Managers, Operations Leads** — if your role involves regularly pulling information from multiple systems, synthesising it into reports or summaries, and making recommendations, this framework was designed with you in mind.

You will use the first three stages to take the workflows that eat your week — account health reviews, renewal preparation, stakeholder reporting — and turn them into clear, scoped automation targets. The framework gives you a structured way to figure out *which* workflow to automate first (not just the one that annoys you most) and to document it clearly enough that someone else could build it. If your team uses a low-code builder, you can continue through Stages 4-6 yourself — no engineer required. Even if you never write a line of code and your team uses a code-first framework, you will leave with a document an engineer can pick up and build from.

### Business analysts

You already think in processes and systems. This framework gives you a structured method for evaluating which business processes are good automation candidates and which ones are not — using concrete scoring criteria rather than gut feel.

The decompose-select-scope stages map directly onto the kind of process analysis you already do, applied to a new question: *where should we put an AI agent?* You will find the scoring rubrics and scoping techniques familiar. If you are advising teams on automation strategy, this gives you a repeatable, defensible methodology for making those recommendations — one that produces documentation you can share with stakeholders and engineers alike.

### Software engineers

You have been asked to "build an AI agent" for a business process you half-understand. This framework gives you a way to work backward from the actual workflow to a technical design that fits.

Instead of guessing at requirements, you get a scoped workflow document that tells you exactly what the agent needs to do, where it needs human review, and what good output looks like — produced by the person who actually does the workflow today. The later stages give you a structured approach to translating that scope into architecture, building it, and evaluating whether it actually works. If you are working with a business stakeholder, you can hand them Stages 1-3 and pick up at Stage 4 with a clear spec.

---

## What kind of workflows work best?

Not every workflow is a good automation candidate. The framework helps you figure out which are which, but here is a quick filter:

**Good candidates** follow the same steps each time, pull from data sources you can access digitally, and produce an output that gets reviewed before anyone acts on it. Think: quarterly reports, data compilations, intake assessments, renewal briefs, status summaries — anything where the *process* is predictable even if the *data* changes each time.

**Poor candidates** require improvisation at every step, depend on information that only exists in your head, or produce outputs that go directly to a client with no review. Think: sensitive negotiations, novel investigations, anything where the value comes from your real-time judgement rather than from following a process.

**Most workflows land in the middle** — some steps are automatable and others are not. The framework helps you find that line and draw it in the right place.

---

## What will I have at the end?

Each stage produces a concrete deliverable. Here is what you will have after each one:

**After Stage 1 — Decompose**
:   A complete inventory of every repeatable workflow in your role, annotated with how often you do it, how long it takes, and how automatable it is. This is the map of your work that most people have never drawn.

**After Stage 2 — Select**
:   A scored decision on which workflow to automate first — not based on gut feel, but on a structured comparison of impact, feasibility, and risk. You will know *why* this workflow is the right starting point.

**After Stage 3 — Scope**
:   A detailed, step-by-step map of how your chosen workflow actually works today. Every decision point, every data source, every handoff — documented clearly enough that someone who has never done the workflow could understand it. This is also where you draw the automation boundary: what the agent handles, where a human reviews, and what stays manual.

**After Stage 4 — Design**
:   A technical blueprint that translates your scope document into an agent architecture. This specifies what the agent does at each step, where it pauses for human review, what data it reads and writes, and how the pieces connect. This is where business requirements become engineering specifications.

**After Stage 5 — Build**
:   A working agent that executes your workflow. It gathers data, processes it, and produces draft outputs — pausing at the checkpoints you defined for your review before anything goes out. You can run it against real or sample data and see results.

**After Stage 6 — Evaluate**
:   Evidence that the agent works — tested against real or realistic scenarios — with a clear picture of where it performs well, where it falls short, and a concrete plan for what to improve next. This is not a rubber stamp; it is an honest assessment that tells you whether the agent is ready for regular use.

!!! tip "Stages 1-3 are valuable on their own"
    Even if you stop after Stage 3, you will have a thorough understanding of your own workflows and a detailed scope document that any engineer can pick up and build from. And if your team uses a low-code builder, you do not need to stop — you can continue through all six stages yourself. The thinking work has standalone value either way.

---

## How long does this take?

These are realistic estimates for your first workflow. Subsequent workflows go faster because you already understand the method. The times below represent focused work — not calendar time.

| Stages | What you are doing | Time estimate |
|---|---|---|
| **Stages 1-2** | Understanding your work and picking a target | Half a day |
| **Stage 3** | Mapping the workflow in detail — this is the hardest thinking work | 1-2 days |
| **Stage 4** | Translating to a technical design (faster if you work with an engineer) | Half a day to 1 day |
| **Stage 5** | Building the agent — depends on complexity and integrations | 1-3 days |
| **Stage 6** | Testing, evaluating, and planning improvements | 1-2 days |
| **Total** | **End to end for your first workflow** | **~1 week of focused work** |

These are not consecutive full days. Most people work through the framework alongside their normal responsibilities, spending focused blocks on each stage. A realistic calendar timeline is two to three weeks for your first workflow, with the actual work totalling roughly a week.

Stage 3 deserves special attention in your planning. It is the stage where you map your workflow in precise detail — every decision point, every data source, every place where judgement is required. This is the hardest thinking work in the framework, and it is where most of the value comes from. Do not rush it.

!!! note "Your second workflow will be faster"
    The first pass through the framework is the slowest because you are learning the method at the same time as applying it. Your second workflow typically takes half the time — you already have your inventory from Stage 1, you know how the stages connect, and you have a completed example to reference.

!!! tip "You do not have to do all six stages yourself — but you can"
    If your team uses a code-first agent framework, you can complete Stages 1-3 and hand the scope document to an engineer for Stages 4-6. If your team uses a low-code builder, you can complete all six stages yourself — no engineering skills required. If you are an engineer, you can ask a business stakeholder to work through Stages 1-3 and pick up at Stage 4. The framework is designed to support both paths.

---

## Where do I start?

**Start here: [Stage 1: Decompose](../stages/01-decompose.md).** Open Stage 1 and start listing the repeatable workflows in your role. You do not need any tools, any software setup, or any technical background — just knowledge of your own job. A blank document or a sheet of paper is enough to begin.

The most common mistake people make is skipping the early stages and jumping straight to building. The framework exists because the most frequent failure mode in automation projects is automating the wrong thing, or automating the right thing at the wrong boundary. The upfront thinking work is what makes the build stage go smoothly.

**Other starting points depending on where you are:**

- **[Quick Start Guide](quick-start.md)** — A 30-minute hands-on exercise that walks you through a compressed version of Stage 1. You will end with a draft workflow inventory and a sense of how the framework works. Good if you want a quick taste before committing.

- **[How to Use This Framework](how-to-use.md)** — A walkthrough of the six-stage structure, how the stages connect, and how to work through them. Good if you want to understand the full picture before starting.

- **[Prerequisites](prerequisites.md)** — What you need for the technical stages (4-6). You do not need any of this for Stages 1-3. Specifics depend on which platform you choose — see [Choose a Platform](choose-a-platform.md).

- **[Worked Example](../worked-example/index.md)** — A completed pass through all six stages for a real workflow (Quarterly Account Health Review for a Customer Success Manager). Good if you want to see what the end result looks like before you start.

---

!!! quote "The bottom line"
    You do not need to understand AI, agents, or automation technology to start this framework. You need to understand your own job. If you can describe what you do, you can use this framework to figure out which parts of it an agent should handle — and which parts should stay with you.

    The first step is simply writing down what you do. [Start with Stage 1.](../stages/01-decompose.md)
