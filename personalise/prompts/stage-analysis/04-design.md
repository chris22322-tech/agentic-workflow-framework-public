# Stage 4: Design — Organisation Analysis

You are analysing how a specific organisation would apply Stage 4 (Design) of
the Agentic Workflow Framework.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml`
2. **Stage documentation**: Read `docs/stages/04-design.md`

## What to Produce

### Design Patterns

For each role's top automation candidates:

- Which of the four design patterns applies (Sequential Pipeline with HIL
  Checkpoints, Parallel Fan-out/Fan-in, Router, Iterative Refinement Loop) —
  or which combination
- Which actions handle which workflow steps
- Where HIL checkpoints are required and why
- How memory fields should be shaped for the data flowing through the agent

Describe the design in platform-neutral terms — actions, flow, memory,
checkpoints. The framework does not prescribe a specific agent framework, and
neither should this analysis. The org will translate the design into their
chosen platform's primitives in Stage 5.

### Integration Architecture

For each system in the org config:

- How the agent will reach it (available API, export/import, manual)
- Authentication approach (OAuth, API key, service account)
- Error handling patterns specific to this system
- Data transformation requirements between systems

### Organisation-Specific Design Constraints

- Multi-tenant considerations (if applicable)
- Client boundary enforcement in agent architecture
- Data residency requirements affecting where agents run
- Audit trail requirements affecting state persistence

### Shared Infrastructure

Components that multiple agents across roles can share:

- Common integration modules
- Shared memory schemas for related workflows
- Cross-cutting concerns (logging, error handling, credential management)
- Configuration externalisation patterns

## Output

Write a structured markdown report. A technical person picking up Stage 4
should be able to use your output to make informed design decisions without
additional research into the organisation's systems. The report must stay
platform-neutral — do not assume any specific agent framework or SDK.
