# Stage 4: Design

You have a detailed scope document describing how the workflow works and where the automation boundary sits. Now you need to turn that into a blueprint for the agent — the architectural decisions that determine how it's built, regardless of which platform or framework you use.

This stage is about making those decisions up front so you're not improvising during implementation. You'll map your workflow steps to agent actions, decide what data flows between them, design how human review checkpoints work, and plan how the agent handles failures. Think of it as the floor plan before construction: the design document does the thinking so that [Stage 5: Build](05-build.md) can focus on execution.

The framework is deliberately **platform-agnostic**. Whatever you choose to build on — a code-first framework, a low-code visual builder, a hosted agent platform, or something that doesn't exist yet — the design decisions in this stage are the same. The implementation details change; the design questions don't. See [Getting Started: Choose a Platform](../getting-started/choose-a-platform.md) for current options.

---

## Inputs

!!! info "What You Need"
    - Workflow Scope Document from [Stage 3: Scope](03-scope.md)
    - An understanding of whatever platform or framework your team will build on (or the decision, at least)

## Output Artifact

!!! info "Key Output"
    A **Design Document** containing:

    1. **Scope-to-action mapping** — which scope steps map to which agent actions, with consolidation rationale
    2. **Agent flow** — the sequence and branching structure of what the agent does
    3. **Memory / state design** — what data the agent needs to remember between steps
    4. **Node / step specifications** — what each action does, what tools it uses, what it produces
    5. **Human-in-the-loop design** — where the agent pauses for human input, what it surfaces, and what the human decides
    6. **Error handling and fallback design**

!!! info "Download Templates"
    [:material-download: Download Spreadsheet](../downloads/Stage 4 - Design.xlsx){ .md-button }
    [:material-download: Download Document Template](../downloads/Stage 4 - Design - Template.docx){ .md-button }

    **Spreadsheet:** Import into Google Sheets for structured tables with example rows.
    **Document:** Word template with instructions, fill-in sections, and completion checklist.

---

## What a Design Document Contains

Your design document answers six questions:

1. **What does the agent do at each step?** Map every scope step to an agent action (a node, a tool call, or a reasoning step within the agent's instructions — whatever your platform calls it).
2. **What data does it need and produce?** Define the inputs and outputs for each action, and how data flows from one action to the next.
3. **Where does a human review?** Identify the checkpoints where the agent pauses for human approval, what it surfaces, and what the human decides.
4. **What happens when something fails?** Define error handling for each failure mode identified in your scope document's Error Path Register.
5. **How are scope steps consolidated?** Not every scope step becomes a separate agent action — related steps are grouped for efficiency and to minimise context switches for human reviewers.
6. **What is the overall flow?** The sequence, branching, and looping structure of the agent's execution.

### How to Map Scope Steps to Agent Actions

Walk your scope document step by step. For each step, decide which kind of agent action it becomes, based on its boundary tag:

| Scope Boundary | Maps to |
|---|---|
| **AUTOMATE (data retrieval)** | A **tool** — an action that calls an external system to retrieve or write data |
| **AUTOMATE (analysis / synthesis)** | A **reasoning step** — handled by the agent's instructions and model reasoning, not by an external tool |
| **AUTOMATE (generation)** | A **reasoning step** with an explicit output format specification |
| **HUMAN-IN-THE-LOOP** | An **HIL checkpoint** — the agent pauses and surfaces information to a human, then resumes based on the response |
| **MANUAL** | **Outside the agent** — stays in the human's workflow, not part of the design at all |

This mapping is the skeleton of your design. Everything else — patterns, state, error handling — hangs off it.

!!! tip "Analysis and synthesis are reasoning, not tools"
    A common mistake at this stage is to treat every scope step as a tool call. Steps like "compare ticket volume against the prior quarter" or "synthesise the findings into a health score" are **reasoning steps**, not tool calls. The agent performs them by reasoning over data it already has, guided by its instructions. Tools are for retrieving data the agent doesn't have and for writing data back to external systems.

---

## Design Patterns

Most workflows you'll scope are variations of four patterns. Pick the one that matches your workflow's shape — or combine them — before you get into the details.

### Pattern 1: Sequential Pipeline with HIL Checkpoints

A linear sequence of actions, with one or more points where a human reviews what the agent has produced before it continues.

```
start → gather_data → analyse → [HIL: review analysis] → synthesise → generate_report → [HIL: review report] → end
```

**When to use it:** The workflow has a clear step-by-step structure, and there are defined moments where human judgement is required. This is the most common pattern for workflows adapted from human processes, because human processes tend to be sequential.

**Design decisions:**

- **Where to place HIL checkpoints.** Put them where the cost of an error is high and where the human can meaningfully catch the error. Don't put them after every step — that destroys the reviewer's flow and the efficiency gain you designed for in Stage 3.
- **Whether to consolidate related steps.** If `analyse_tickets`, `analyse_usage`, and `analyse_sentiment` all feed into a single review, make them one action that produces all three outputs, and put the review after it.

### Pattern 2: Parallel Fan-Out / Fan-In

Multiple independent actions run concurrently, and their results converge at a single downstream action.

```
start → [gather_crm || gather_support || gather_usage || gather_comms] → analyse → end
```

**When to use it:** The workflow has data-gathering steps that have no dependencies on each other. Running them in parallel reduces wall-clock time.

**Design decisions:**

- **Which actions are actually independent.** If two actions need each other's output, they're sequential, not parallel — even if your platform lets you express them in parallel.
- **How results combine.** Define the memory/state shape the downstream action consumes. If four parallel actions each produce a dict and you need one merged dict at the fan-in point, state the merge rule in the design.

### Pattern 3: Router

The agent classifies input and routes to fundamentally different downstream paths, each with different logic and possibly different tools.

```
start → classify → [if type=A: path_a → ...] / [if type=B: path_b → ...] / [if type=C: path_c → ...] → end
```

**When to use it:** The workflow has genuinely divergent paths — "bug reports go through triage, feature requests go through prioritisation, support questions go through knowledge-base lookup," for example. The scope document's Decision Logic column will show branching, not a single linear chain.

**Design decisions:**

- **Where the classification happens.** Usually as an early step that reads the input and emits a category.
- **How paths rejoin (if they do).** Sometimes paths merge at the end (all three converge on the same report-generation step); sometimes they don't (each path ends independently).

### Pattern 4: Iterative Refinement Loop

The agent produces an output, receives feedback, revises, and repeats until the feedback is "approved" or a maximum iteration count is reached.

```
start → generate → [HIL: review] → if approved: end / if revise: generate → ...
```

**When to use it:** The output is something that typically needs several rounds of editing before it's right — a draft document, a proposed plan, a piece of content. The agent can genuinely incorporate the feedback into a new version.

**Design decisions:**

- **The iteration cap.** Always set a maximum. Without one, a confused reviewer or a stubbornly-wrong agent can loop forever.
- **What "feedback" looks like.** Freeform text? A structured list of changes? Approve/reject/specific-edits? This shapes the agent's regeneration logic.

### Combining Patterns

Real workflows combine patterns. A workflow might have a Router at the top (bug vs feature vs question), then each branch is a Sequential Pipeline with its own HIL checkpoints, and the feature-request branch uses an Iterative Refinement Loop for the proposal step. The patterns are building blocks — your design names which block each part of the workflow is built from.

---

## Node / Step Specifications

For every action in the design, write a short specification that tells the implementer what it does in enough detail to build it without ambiguity.

The standard fields:

**Purpose.** One sentence stating what the action accomplishes — the result, not the activity. Derive it from the Output column of the scope steps the action consolidates. If you cannot state the purpose in a single sentence, the action is doing too much — split it.

**Tools.** Which tools the action uses to retrieve or write data. Derive them from the Data Inventory in your scope document. If a tool is not in the Data Inventory, either the inventory is incomplete or the action doesn't actually need it.

**Reasoning / Logic.** Step-by-step description of what the action does. Derive it from the Decision Logic and Output columns of the scope steps the action consolidates. A Decision Logic entry that says "compare ticket volume against the prior quarter; a >20% increase indicates degradation" becomes a reasoning step: "calculate quarter-over-quarter volume change; flag if the increase exceeds 20%." Be specific enough that the builder knows *what* to implement, but do not write framework-specific code — that belongs in Stage 5.

**Prompt pattern** *(for actions that use a language model).* Specifies two things:

1. **What context the action receives.** Name the inputs explicitly. Not "the relevant data" but "the raw ticket data, the SLA thresholds from the scoring rubric, and any human feedback from the previous review checkpoint."
2. **What output format it produces.** Structured JSON with a defined schema, plain text, or structured Markdown — and what fields or sections the output must contain. If the output is JSON, list the expected keys.

The prompt pattern is the contract between design and build. Your Stage 5 implementer uses it to determine what data to format into the prompt template and what structure to parse from the model's response. Too vague ("analyse the data and return results") and the implementer has to reverse-engineer your intent. Too specific (the exact prompt text) and you're doing Stage 5's job in Stage 4.

**Error handling.** Which failure modes this action can encounter, how it detects them, and which strategy it applies. See [Error Handling Design](#error-handling-design) below.

**Parallelism** *(for data-gathering actions).* Whether the action's tool calls are independent and can run concurrently. Your platform will express this differently, but the design decision is the same: state explicitly when actions are safe to parallelise.

### Deriving Specifications from the Scope Document

Walk your agent flow action by action and pull from three scope document sources:

1. **Output column → Purpose.** The outputs of the scope steps an action consolidates define what the action must produce.
2. **Data Inventory → Tools.** The scope document's data sources tell you which tools the action calls.
3. **Decision Logic column → Reasoning.** The Decision Logic entries contain the criteria, thresholds, and rules the action applies.

---

## Memory and State Design

The agent needs to remember information as it moves through the workflow. How that memory is implemented depends on your platform, but the design questions are the same:

**What does the agent need to remember?** Walk your design action by action and list every piece of information that gets produced and consumed downstream. These are your memory fields. Typical categories:

- **Inputs** — what the user or caller provides at the start (account ID, quarter, ticket ID, release tag)
- **Retrieved data** — raw data the tools return (CRM record, ticket list, usage metrics)
- **Derived data** — analysis outputs the agent produces (ticket health score, sentiment assessment)
- **Human feedback** — what reviewers provide at HIL checkpoints
- **Final outputs** — the artefacts the workflow produces (the health report, the release notes)

**What shape is each piece?** A single value, a list, a structured object? Name the fields explicitly. This isn't about picking a type system — it's about being clear with the implementer on what each piece of memory looks like so they can pick the right representation in their platform.

**Which actions write which fields?** Exactly one action should be responsible for each piece of memory. If two actions both write to the same field, you probably have a consolidation opportunity (merge them) or a race condition (use different field names).

**Which actions read which fields?** An action's input context lists the memory fields it reads. Trace this through the design: if an action reads a field, some earlier action must have written it.

**Design principle — everything the agent needs to act on must be in memory or retrievable via a tool.** If an action needs information to do its job, and that information is neither in memory nor retrievable by one of the action's tools, the design has a gap.

!!! tip "Design memory for observability, not just execution"
    Good memory design makes debugging tractable. If you can inspect the memory state at each action boundary, you can tell exactly what the agent had when it made a decision. If all the intermediate state lives inside a single opaque action, you can only see inputs and final outputs — everything in the middle is a black box. Lean toward explicit memory fields even when the action could hold the data internally.

---

## Human-in-the-Loop Checkpoint Design

HIL checkpoints are where the agent pauses and surfaces information to a human, waits for a response, and resumes based on what the human decides. The design decisions for each checkpoint are:

### What to surface

Everything the reviewer needs to make an informed decision, and nothing more. Include:

- **The agent's output at this point** (the analysis, the draft report, the proposed action)
- **The data the agent used to produce it** (tool responses, retrieved records)
- **Any flags or warnings** the agent raised during this stage (a metric below threshold, an ambiguous tool response, a confidence signal)

Do not surface unnecessary context. A reviewer who has to wade through the full conversation history to find what they're supposed to review will skim and miss things.

### What input to expect

Checkpoints differ in the structure of the response they take:

**Feedback-as-context.** The human provides freeform feedback, and the next action in the flow consumes that feedback as additional context. This is the pattern when the human is correcting or augmenting the agent's work — "the sentiment reading on the executive sponsor is wrong, last week's call was positive, not neutral" — and the next action re-runs with the correction incorporated.

```
hil_review_analysis:
    surface: all four analysis dimensions with scores, trends, evidence
    expect: freeform text feedback (empty string = approved)
    writes_to_memory: analysis_human_feedback
```

The downstream `synthesise` action reads `analysis_human_feedback` and injects it into its prompt as "reviewer corrections to incorporate."

**Feedback-as-control-flow.** The human's response determines which action runs next. This is the pattern when there are distinct downstream paths — "approve → proceed to report generation, reject with revise → regenerate the current output, reject with rework → go back to analysis."

```
hil_review_report:
    surface: full report and executive summary
    expect: structured decision { decision: approve | revise | rework, instructions: str }
    routes_to:
        decision == approve → end
        decision == revise → generate_report (with instructions in memory)
        decision == rework → analyse (with instructions in memory)
```

The control-flow pattern is more deterministic but requires the reviewer to choose from a fixed set of options. The context pattern is more flexible but less predictable.

### Which pattern to choose

- **Feedback-as-context** when the reviewer's job is to *correct* the agent's output and there's a single obvious downstream next step. Simpler to implement on most platforms. Works well when the agent genuinely improves on a second attempt with the feedback.
- **Feedback-as-control-flow** when the reviewer's decision *routes* to meaningfully different downstream paths. Worth the extra design effort when the difference between "tweak this draft" and "rework the analysis" is a difference in tool calls, not just prompt content.

### Consolidating HIL Checkpoints

The scope document may have ten steps tagged HIL. The design will usually have two or three checkpoints — not ten — because multiple HIL-tagged steps can be consolidated into a single review. Two patterns for consolidation:

**Pattern A: Consolidate related reviews into one checkpoint.** If the reviewer would naturally evaluate several outputs together (three analysis dimensions, for example), present them together in one checkpoint. Five context switches become one.

**Pattern B: Upstream validation converts downstream HIL to automated.** If a checkpoint earlier in the flow validates the inputs that a later HIL-tagged step depends on, the later step can often run automatically — the validation already happened. Test this carefully: it only works when the downstream step's judgement is fully derivable from data the upstream checkpoint already validated.

Be explicit about which scope-level HIL steps each design-level checkpoint covers. This makes the consolidation auditable and helps Stage 6 evaluation target the right review moments.

---

## Error Handling Design

Every action in your design can fail. If you don't design for failure modes now, you'll discover them in production when a tool times out, an API returns garbage, or the language model ignores your output format. The goal is a deliberate decision for every failure mode: what detects it, and what happens next.

### Identifying Failure Modes

For each action, walk through the failure modes:

- **Tool-call failures.** Timeout, 4xx, 5xx, malformed response, empty result. Your scope document's Error Path Register already lists these for each data source.
- **Data quality failures.** The tool responds successfully but the data is unusable — empty result sets, unexpected formats, stale records, missing fields you were counting on.
- **Model failures.** The agent returns output that doesn't match the expected format (malformed JSON, missing fields, text when you asked for structure).
- **Boundary failures.** The agent tries to do something outside its scope — attempt a MANUAL step, call a tool it shouldn't, produce an output format the downstream action can't consume.

### Choosing a Response Strategy

For each failure mode, pick one:

**Error marker and continue.** The action notes the failure in memory and continues. Downstream actions check for the marker and handle the gap gracefully (score the affected dimension as "Not Assessed", skip the dependent analysis, flag the gap in the final output). Use this for non-critical failures where partial output is still valuable.

**Retry.** The action retries the failing tool call or model invocation a small number of times before giving up. Use for transient failures (network blips, rate limits) or format failures that a stricter prompt might fix. Always cap the retry count.

**Escalate via HIL.** The action surfaces the failure to a human through an ad-hoc HIL checkpoint. The human decides what to do — manually provide the missing data, skip the failing action, abort the run. Use for failures the agent can't recover from but the human can.

**Abort.** The action stops the entire run with a clear error. Use for failures where continuing would produce a wrong or misleading output — missing critical data that the final artefact depends on.

### Design at the Action Boundary, Not the Tool Boundary

Tools report failures — they return error values or raise exceptions. **Actions** decide what to do about them. This separation matters because the same tool failure might warrant different responses in different actions. A CRM timeout during initial data gathering might be recoverable (continue with other sources); the same timeout during a critical validation step might require escalation.

Design your error handling in the action specifications, not buried inside tool implementations. Each action spec should state: what failures it can encounter, how it detects them, and which strategy it applies.

---

## Worked Example

For a concrete walkthrough of all six design questions applied to a real workflow, see the [CSM Health Review worked example](../worked-example/design.md). It translates the Stage 3 scope into a design document with all six artefacts (scope-to-action mapping, agent flow, memory, action specifications, HIL design, error handling) in platform-neutral terms you can adapt to whichever framework you're building on.

---

## Next Step

Complete your design document using the [Stage 4 Design template](../blank-templates/design-document.md), then move to [Stage 5: Build](05-build.md) to implement it.

!!! tip "Translating the design to your platform"
    When you're ready to implement, the [Platform Cheat Sheet](../reference/platform-cheatsheet.md) maps each framework concept (action, memory field, HIL checkpoint, tool type) to the equivalent primitive on several popular platforms, with links to vendor docs. It is not framework doctrine — it's a maintainer's current reference — but it's the right bridge between a platform-neutral design and a platform-specific implementation.
