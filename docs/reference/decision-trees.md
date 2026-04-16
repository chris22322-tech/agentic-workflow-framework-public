# Decision Trees

Two decision trees for the most common design questions when applying the framework.

---

## Should I Automate This Step?

Use this when tagging each step in your workflow map with an automation boundary (Stage 3).

```mermaid
flowchart TD
    A{"Primarily data retrieval\nor transformation?"} -->|Yes| B["AUTOMATE"]
    A -->|No| C{"Requires judgement, but\ncriteria are articulable?"}
    C -->|Yes| D["HUMAN-IN-THE-LOOP\n(agent proposes, human approves)"]
    C -->|No| E{"Requires relationship context,\npolitical sensitivity, or\ninterpersonal reading?"}
    E -->|Yes| F["MANUAL"]
    E -->|No| G["Revisit — break the\nstep down further"]

    style B fill:#2e7d32,color:#fff
    style D fill:#f57f17,color:#fff
    style F fill:#c62828,color:#fff
    style G fill:#1565c0,color:#fff
```

---

!!! info "For engineers"
    This decision tree is for the engineer designing the agent flow in [Stage 4: Design](../stages/04-design.md). If you are a workflow owner (CSM, BA, DM), the first tree above is the one you will use.

## What Design Pattern Should I Use?

Use this when choosing a design pattern in Stage 4.

```mermaid
flowchart TD
    A{"Workflow essentially\nlinear?"} -->|Yes| B["Sequential Pipeline\nwith HIL Checkpoints"]
    A -->|No| C{"Independent steps that\ndon't depend on each other?"}
    C -->|Yes| D["Fan-out / Fan-in"]
    C -->|No| E{"Next step depends on\nclassifying output?"}
    E -->|Yes| F["Router"]
    E -->|No| G{"Output needs iterative\nrefinement?"}
    G -->|Yes| H["Refinement Loop"]

    style B fill:#1565c0,color:#fff
    style D fill:#1565c0,color:#fff
    style F fill:#1565c0,color:#fff
    style H fill:#1565c0,color:#fff
```

**→ Pattern details:** [Sequential Pipeline](../stages/04-design.md#pattern-1-sequential-pipeline-with-hil-checkpoints) · [Fan-out / Fan-in](../stages/04-design.md#pattern-2-parallel-fan-out-fan-in) · [Router](../stages/04-design.md#pattern-3-router) · [Refinement Loop](../stages/04-design.md#pattern-4-iterative-refinement-loop)

!!! note
    Most real workflows combine patterns. For example: fan-out for data gathering, sequential for analysis, router for handling different health scores differently.
