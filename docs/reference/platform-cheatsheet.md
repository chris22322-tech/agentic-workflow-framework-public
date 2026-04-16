---
last_verified: 2026-04-15
---

# Platform Cheat Sheet

!!! warning "This is a maintainer's current reference, not framework doctrine"
    This page maps framework concepts (from [Stage 4: Design](../stages/04-design.md) and [Stage 5: Build](../stages/05-build.md)) to the corresponding primitives on current popular agent platforms. It is the **one place in the framework where platform names appear by design**, and it is **not** part of the framework's methodology.

    This content tracks a rapidly-evolving vendor ecosystem and **will go out of date**. Every row has a `last-verified` annotation. The page-level staleness is enforced by a CI check that fails the production gate if any row is more than 180 days old.

    **Use this page as a starting point, not as a source of truth.** Always verify against the vendor's current documentation before committing to an implementation choice.

---

## How to read this cheat sheet

Each row is a framework concept. Each column is a platform. Cells show:

- The platform's primitive name for the concept
- A link to the vendor's current quickstart or concept doc for that primitive
- The maintainer's last-verified date for that cell

If a cell is blank, the platform does not have a first-class equivalent for that concept — you may need to express it in a different way on that platform (e.g., instruction-based HIL when no pause primitive exists). See the [concept notes](#concept-notes) at the bottom for guidance.

---

## Concept to primitive mapping

### Code-first frameworks

| Framework concept | LangGraph | CrewAI | ADK | OpenAI Agents SDK |
|---|---|---|---|---|
| **Agent definition** | `StateGraph` with compile() <sup>[2026-04-15]</sup> | `Crew` with `Agent` members <sup>[2026-04-15]</sup> | `LlmAgent` class <sup>[2026-04-15]</sup> | `Agent` class <sup>[2026-04-15]</sup> |
| **Action** (Stage 4 concept) | Node function bound to the graph <sup>[2026-04-15]</sup> | `Task` with `Agent` assignment <sup>[2026-04-15]</sup> | Function passed to `LlmAgent` or sub-agent <sup>[2026-04-15]</sup> | Function tool or handoff to sub-agent <sup>[2026-04-15]</sup> |
| **Memory field** (Stage 4 concept) | Typed field in a `TypedDict` / Pydantic state schema <sup>[2026-04-15]</sup> | Context object fields / `Task` inputs and outputs <sup>[2026-04-15]</sup> | Session state fields managed by Agent Engine <sup>[2026-04-15]</sup> | Agent context / conversation state <sup>[2026-04-15]</sup> |
| **Tool (MCP-style connector)** | `McpToolset` via `langchain-mcp-adapters` <sup>[2026-04-15]</sup> | Custom `Tool` subclass wrapping an MCP client <sup>[2026-04-15]</sup> | `McpToolset` from `google.adk.tools.mcp_tool` <sup>[2026-04-15]</sup> | Function tool wrapping an MCP client <sup>[2026-04-15]</sup> |
| **Tool (OpenAPI-described)** | Custom `@tool` wrapping an OpenAPI client, or `OpenAPIToolset` from community packages <sup>[2026-04-15]</sup> | Custom `Tool` subclass <sup>[2026-04-15]</sup> | `OpenAPIToolset` from `google.adk.tools.openapi_tool` <sup>[2026-04-15]</sup> | Function tool with OpenAPI-derived schema <sup>[2026-04-15]</sup> |
| **Tool (custom function)** | `@tool`-decorated function <sup>[2026-04-15]</sup> | `Tool` subclass with `_run()` method <sup>[2026-04-15]</sup> | `FunctionTool` class <sup>[2026-04-15]</sup> | Function tool (`function_tool` decorator) <sup>[2026-04-15]</sup> |
| **HIL checkpoint / pause** | `interrupt()` + `Command(resume=...)` <sup>[2026-04-15]</sup> | Typically instruction-based; no first-class pause primitive <sup>[2026-04-15]</sup> | `ToolConfirmation` with boolean or structured response <sup>[2026-04-15]</sup> | Manual handoff pattern or approval function tool <sup>[2026-04-15]</sup> |
| **Error handling** (error marker and continue) | `try/except` in node function + routing function reads marker from state <sup>[2026-04-15]</sup> | `Task` error handling; retry config in `Crew` <sup>[2026-04-15]</sup> | Function-level try/except + agent-level error handlers <sup>[2026-04-15]</sup> | Function tool error returned as tool result <sup>[2026-04-15]</sup> |
| **Observability / tracing** | LangSmith (SaaS) or OpenTelemetry export <sup>[2026-04-15]</sup> | CrewAI's built-in logger + optional integrations <sup>[2026-04-15]</sup> | Agent Engine traces (Google Cloud Logging) <sup>[2026-04-15]</sup> | OpenAI trace export / external telemetry <sup>[2026-04-15]</sup> |
| **Deployment target** | LangGraph Platform or self-host <sup>[2026-04-15]</sup> | Self-host; managed options via partners <sup>[2026-04-15]</sup> | Vertex AI Agent Engine <sup>[2026-04-15]</sup> | OpenAI-hosted or self-host <sup>[2026-04-15]</sup> |

### Low-code builders

| Framework concept | Vertex AI Agent Designer | (other builders vary) |
|---|---|---|
| **Agent definition** | Main agent node on the Agent Designer canvas <sup>[2026-04-15]</sup> | — |
| **Action** (Stage 4 concept) | Sub-agent node or implicit in the Instructions field <sup>[2026-04-15]</sup> | — |
| **Memory field** (Stage 4 concept) | Implicit in conversation history; explicit via Vertex AI Search Data Store binding <sup>[2026-04-15]</sup> | — |
| **Tool (MCP-style connector)** | MCP Server tool type (**unauthenticated only in preview, early 2026**) <sup>[2026-04-15]</sup> | — |
| **Tool (OpenAPI-described)** | Not available in the Agent Designer UI; requires Get Code → ADK export <sup>[2026-04-15]</sup> | — |
| **Tool (custom function)** | Not available in the Agent Designer UI; requires Get Code → ADK export <sup>[2026-04-15]</sup> | — |
| **HIL checkpoint / pause** | Instruction-based only (no first-class pause primitive; enforced via Instructions text) <sup>[2026-04-15]</sup> | — |
| **Error handling** | Instruction-based error handling rules in the Instructions field <sup>[2026-04-15]</sup> | — |
| **Observability / tracing** | Agent Designer Preview tab + Google Cloud Logging <sup>[2026-04-15]</sup> | — |
| **Deployment target** | Export to ADK via Get Code, then deploy via Vertex AI Agent Engine <sup>[2026-04-15]</sup> | — |

!!! note "Why only one low-code platform column"
    The low-code agent builder landscape is evolving fast and each vendor's UI model is substantially different. Rather than pretend to track all of them, this cheat sheet names **Vertex AI Agent Designer** as a concrete reference point (it is the builder one of the framework's contributors is actively using) and suggests you consult your chosen builder's documentation directly. If you are maintaining this cheat sheet and want to add a column for another low-code builder, that's fine — commit to ~quarterly verification of the cells, same as any other column.

---

## Concept notes

### Agent definition

All code-first frameworks have a concept of "the agent" as a top-level object that wires actions, tools, memory, and model configuration together. How you instantiate it varies — some use a builder pattern, some a class, some a config file. The framework-level concept is the same.

### Action vs tool

The framework uses "action" (Stage 4) for a step in the agent's flow and "tool" (also Stage 4) for an external-system wrapper that an action uses. Different platforms blur this boundary:

- **LangGraph** makes actions first-class (nodes) and tools first-class (`@tool` functions).
- **CrewAI** puts the emphasis on tasks (actions) assigned to agents, with tools as helpers.
- **ADK** lets an agent *be* a tool (agent-as-tool pattern) and lets tools *be* agents (function tools that call sub-agents).
- **OpenAI Agents SDK** uses function tools as the primary primitive; actions are implicit in the agent's reasoning flow.

When you are designing in Stage 4, use the framework's action/tool distinction. When you translate to your chosen platform in Stage 5, consult this cheat sheet's row for the primitive your platform calls the equivalent concept.

### Memory field

Every agent framework has some way to persist information between actions. How that memory is shaped differs:

- **LangGraph** uses a typed state dict (`TypedDict` or Pydantic model) that every node reads and writes.
- **ADK** provides session state managed by Agent Engine.
- **CrewAI** uses context objects passed between tasks.
- **OpenAI Agents SDK** uses conversation state managed by the agent.

The framework's "memory field" concept — an explicit named slot written by one action and read by another — maps cleanly to all of these. Your implementation will use the platform's primitive; your design document uses the generic concept.

### HIL checkpoint

The most variable primitive across platforms. Some frameworks have structured pause-and-resume APIs that guarantee the agent cannot proceed past a checkpoint until a human responds. Others rely on instruction-based pauses where the agent interprets its instructions literally and holds at defined points.

Structured primitives are strictly better when the correctness of the pause matters (writing back to a system of record, any high-stakes approval). Instruction-based pauses work when the downstream action can catch a mistake, and when you have test coverage to verify the pause actually happens.

If your chosen platform only supports instruction-based pauses, plan to test rigorously (see [Stage 5: Build — principle 5](../stages/05-build.md#5-hil-checkpoints-must-genuinely-pause)).

### Observability and tracing

Every production-grade agent needs structured trace data. What you want from a trace:

- Per-action inputs, outputs, and duration
- Model prompts and responses
- Tool calls, parameters, and responses
- Error events with full context
- Retention that meets your compliance requirements

Most code-first frameworks support OpenTelemetry export or provide a first-party tracing service. Most low-code builders provide built-in trace logging through their cloud provider. Verify this before picking a platform — a framework with no observability story is not a production framework.

### Deployment target

The runtime that actually runs your agent. Options:

- **Self-hosted** — you run the agent on your own infrastructure. Maximum control, maximum operational cost.
- **Managed platform runtime** — the vendor runs the agent. Minimum operational cost, maximum vendor lock-in.
- **Framework-native managed service** — some frameworks (LangGraph Platform, Vertex AI Agent Engine, OpenAI Agents hosting) have a managed runtime specifically designed for agents.

Pick based on your org's operational maturity and data residency requirements, not on which has the flashiest features.

---

## Platform-specific caveats

### Vertex AI Agent Designer

- **Preview status:** Agent Designer is in preview (as of early 2026). Expect breaking changes.
- **MCP authentication:** The MCP Server tool type in the Agent Designer UI supports **unauthenticated MCP servers only** during preview. Most production MCP servers (BigQuery with IAM, Slack, Salesforce, etc.) require auth and must be used via ADK.
- **Tool type limits:** OpenAPI tools and Function tools are not available in Agent Designer's UI. If your design needs either, click "Get Code" to export to ADK Python and continue there.
- **Deployment:** Agent Designer prototypes should be exported to ADK before production deployment. Agent Designer-only runs are appropriate for prototyping but not for production SLA.

### LangGraph

- **Model-agnostic:** LangGraph itself does not bundle a model provider — you wire in Claude, GPT, Gemini, or whatever your team uses via LangChain model wrappers or direct SDKs.
- **Pause-and-resume is first-class:** `interrupt()` + `Command(resume=...)` provide a structured pause primitive that genuinely halts execution. Use this for any load-bearing HIL checkpoint.
- **Subgraph composition:** LangGraph has strong support for nested graphs. If your design has a multi-agent shape (router → specialised paths), subgraphs are the right primitive.
- **Deployment:** LangGraph Platform is the vendor's managed service; self-hosting is also common.

### CrewAI

- **Task-centric design:** CrewAI's mental model is "a crew of agents working on tasks" rather than "a graph of actions". Translating the framework's action/flow design to CrewAI means mapping actions to tasks and flow edges to task dependencies.
- **HIL is instruction-based:** CrewAI does not have a first-class structured pause primitive. Express HIL through the agent's instructions and test coverage.
- **Best for:** multi-agent collaboration workflows where the "crew" framing is natural; less good for single-agent linear pipelines.

### ADK (Agent Development Kit)

- **First-class tool types:** ADK has distinct classes for `FunctionTool`, `OpenAPIToolset`, `McpToolset`, and `AgentTool`. The tool type decision rubric from [Stage 4: Design](../stages/04-design.md#how-to-map-scope-steps-to-agent-actions) maps directly.
- **Structured HIL:** `ToolConfirmation` provides boolean or structured confirmation responses at the tool level. Use this for any tool call that needs human approval before execution.
- **Deployment:** ADK agents deploy to Vertex AI Agent Engine, which provides runtime, scaling, sessions, memory bank, and code execution sandboxes.

### OpenAI Agents SDK

- **Function-tool-centric:** The primary primitive is the function tool. Actions are implicit in the agent's reasoning flow rather than explicit nodes.
- **Handoffs:** The SDK's "handoff" pattern is how you compose multiple agents — one agent hands off control to another.
- **HIL:** No first-class pause primitive; implement via function tools that gate sensitive actions.

---

## Maintaining this cheat sheet

The production check enforces a 180-day staleness rule on the page-level `last_verified` frontmatter field and individual cell annotations. If you are the maintainer:

1. **Quarterly (minimum):** walk through every row for every platform. Verify the primitive name is still correct. Verify the linked docs still exist and are still the right entry point. Update the `[YYYY-MM-DD]` annotation on each cell you verify.
2. **After a vendor breaking change:** update the affected cells immediately. Bump `last_verified` in the frontmatter if you've touched a majority of cells.
3. **When a new platform becomes relevant:** add a column. Commit to maintaining it at the same cadence as the existing columns. If you cannot commit to that, do not add the column — a stale column is worse than no column.
4. **Before removing a platform:** flag it in a maintainer issue first. Removing a platform is a content change that affects readers who picked based on an earlier version of this page.

See `MAINTAINER_GUIDE.md` at the project root for broader editing rules (it lives outside the `docs/` tree because it's for contributors, not end users).
