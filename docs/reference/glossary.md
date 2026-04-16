# Glossary

Key terms used throughout the framework. Organised by category. Definitions are platform-neutral — the same concept may have different names in different agent frameworks.

## Core Concepts

Action (also: Node, Step)
:   A single processing unit in the agent's workflow — for example, "pull CRM data" or "assess ticket health". Different agent frameworks call this a "node", a "step", or an "action"; the framework uses "action" throughout. *Used in: [Stage 4: Design](../stages/04-design.md), [Stage 5: Build](../stages/05-build.md)*

Tool
:   A function that connects an action to an external system — pulling data from a CRM, querying a database, calling an API, writing data back. Each tool does one specific job and can be used by any action that needs it. *Used in: [Stage 4: Design](../stages/04-design.md), [Stage 5: Build](../stages/05-build.md)*

Flow
:   The sequence and branching structure of the agent's execution — which action runs first, which run in parallel, which run conditionally, and where the agent ends. Often drawn as a directed graph. *Used in: [Stage 4: Design](../stages/04-design.md)*

Memory (also: State)
:   The shared data the agent accumulates as it works — all the fields (account ID, health score, gathered data, draft report) that get filled in as each action runs. Every framework has some way to represent this; the framework uses "memory" to emphasise the concept is platform-neutral. *Used in: [Stage 4: Design](../stages/04-design.md), [Stage 5: Build](../stages/05-build.md)*

Memory field
:   A single named slot in memory (e.g., `crm_data`, `ticket_analysis`, `health_score`). Every field should have a declared type, a single action that writes it, and one or more actions that read it. *Used in: [Stage 4: Design](../stages/04-design.md)*

Reducer
:   A rule for how a memory field gets updated when multiple actions write to it — for example, "append new items to the list" rather than "replace the whole list." Some frameworks expose this concept explicitly; others handle it implicitly. *Used in: [Stage 4: Design](../stages/04-design.md)*

Conditional routing
:   A connection where the next action depends on what happened in the previous one — for example, routing a Red-scored account to an escalation path and a Green-scored account to a standard report. Every framework expresses this differently; the design concept is the same. *Used in: [Stage 4: Design](../stages/04-design.md)*

## Execution and Persistence

Checkpoint
:   A saved snapshot of where the agent is and what data it has gathered so far. Checkpoints are what let the agent pause for human review and resume afterwards. *Used in: [Stage 4: Design](../stages/04-design.md), [Stage 5: Build](../stages/05-build.md)*

Run
:   A single execution of the agent from start to finish, usually identified by a unique ID. If the agent pauses for review and resumes later, the run keeps track of where it left off. *Used in: [Stage 5: Build](../stages/05-build.md)*

Durable execution
:   The guarantee that the agent's progress is not lost if the system restarts — it picks up from the last completed action rather than starting over. Requires a persistent checkpointing backend, which most production-grade agent frameworks provide. *Used in: [Stage 5: Build](../stages/05-build.md)*

## Human-in-the-Loop

HIL (Human-in-the-Loop)
:   The design pattern where the agent does the work but a human reviews and approves before anything is finalised or sent out. This is how you keep a human in control of quality and judgement calls. *Used in: [Stage 3: Scope](../stages/03-scope.md), [Stage 4: Design](../stages/04-design.md)*

HIL checkpoint
:   A defined point in the flow where the agent pauses, surfaces information to a human, and waits for a response before continuing. How the pause is implemented varies by framework — some have structured pause-and-resume primitives, others enforce it through the agent's instructions. *Used in: [Stage 4: Design](../stages/04-design.md), [Stage 5: Build](../stages/05-build.md)*

Feedback-as-context
:   An HIL pattern where the reviewer provides freeform feedback and the next action in the flow consumes that feedback as additional context. Useful when the reviewer is correcting or augmenting the agent's work. *Used in: [Stage 4: Design](../stages/04-design.md#which-pattern-to-choose)*

Feedback-as-control-flow
:   An HIL pattern where the reviewer's response determines which action runs next. Useful when there are distinct downstream paths (approve / revise / rework). *Used in: [Stage 4: Design](../stages/04-design.md#which-pattern-to-choose)*

## Design Patterns

Sequential Pipeline with HIL Checkpoints
:   A linear sequence of actions with one or more points where a human reviews what the agent has produced. The most common pattern for workflows adapted from human processes. *Used in: [Stage 4: Design](../stages/04-design.md#pattern-1-sequential-pipeline-with-hil-checkpoints)*

Parallel Fan-out / Fan-in
:   A pattern where multiple independent actions run concurrently and their results converge at a single downstream action — for example, pulling data from CRM, support tickets, and usage analytics simultaneously instead of one at a time. *Used in: [Stage 4: Design](../stages/04-design.md#pattern-2-parallel-fan-out-fan-in)*

Router
:   A pattern where the agent classifies input and routes to fundamentally different downstream paths, each with different logic and possibly different tools — "bug reports go through triage, feature requests go through prioritisation." *Used in: [Stage 4: Design](../stages/04-design.md#pattern-3-router)*

Iterative Refinement Loop
:   A pattern where the agent produces an output, receives feedback, revises, and repeats until the feedback is "approved" or a maximum iteration count is reached. *Used in: [Stage 4: Design](../stages/04-design.md#pattern-4-iterative-refinement-loop)*

## Error Handling

Error marker
:   A convention where an action notes in memory that a tool call failed and continues — downstream actions check for the marker and handle the gap gracefully (e.g., noting "CRM data unavailable" in the report). *Used in: [Stage 4: Design](../stages/04-design.md#error-handling-design)*

Escalate via HIL
:   An error-handling strategy where a failure that the agent can't recover from is surfaced to a human through an ad-hoc checkpoint. The human decides what to do — manually provide the missing data, skip the failing action, or abort the run. *Used in: [Stage 4: Design](../stages/04-design.md#choosing-a-response-strategy)*

Guardrails
:   Safety checks that keep the agent within acceptable bounds — validating that inputs make sense, outputs meet quality standards, and the agent does not loop forever or run past a time limit. Can be input guardrails (validating action inputs), output guardrails (validating action outputs), or structural guardrails (max iterations, timeouts). A design concept, not a single API.

## Scope Boundaries

AUTOMATE
:   A boundary tag applied to a scope step that the agent should perform — either as a tool call (data retrieval) or as a reasoning step (analysis, synthesis, generation). *Used in: [Stage 3: Scope](../stages/03-scope.md)*

HIL (boundary tag)
:   A boundary tag applied to a scope step that requires a human decision. In the design stage, HIL-tagged steps are consolidated into a smaller number of HIL checkpoints. *Used in: [Stage 3: Scope](../stages/03-scope.md), [Stage 4: Design](../stages/04-design.md#consolidating-hil-checkpoints)*

MANUAL
:   A boundary tag applied to a scope step that stays with the human — not part of the agent's work at all. MANUAL steps define the agent's boundary: the agent ends at the last action before the first MANUAL step. *Used in: [Stage 3: Scope](../stages/03-scope.md)*
