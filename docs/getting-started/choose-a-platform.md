# Choose a Platform

The Agentic Workflow Framework is **platform-neutral**. It teaches you how to decompose, scope, design, build, and evaluate an agent — but it does not teach you how to use any specific framework or SDK. That's a deliberate choice: the agent ecosystem in 2026 is moving fast, vendors release new capabilities monthly, and any platform-specific content would be out of date by the time you read it.

Instead, this page points you at some of the popular options today. **This list is not exhaustive, it is not an endorsement, and it will be out of date.** Always check the vendor's current documentation for the authoritative picture.

---

## When do I need to pick?

- **Stages 1–3** (Decompose, Select, Scope): you don't need a platform. The output is a scope document that describes the workflow in human language.
- **Stage 4** (Design): you don't strictly need a platform yet. The framework's [Stage 4 methodology](../stages/04-design.md) is platform-neutral — you produce a design document that describes actions, memory, HIL checkpoints, and error handling in terms that apply to any agent framework. It helps to know roughly where you'll build (code-first vs low-code) so you can make realistic decisions about HIL implementation and state management, but you don't need to have picked a specific tool.
- **Stage 5** (Build): you need a platform. This is where the design meets a real implementation.
- **Stage 6** (Evaluate): you're testing whatever you built in Stage 5, so the platform choice is already made.

---

## Categories of platform

At the top level, agent platforms fall into three families. Pick the family first, then the specific tool within it.

### Code-first frameworks

You write the agent in code. Maximum flexibility, maximum control, and the longest learning curve. Good for production workflows that need custom tools, authenticated integrations, structured HIL, and tight testing.

Examples today (not exhaustive, not an endorsement):

- **[LangGraph](https://langchain-ai.github.io/langgraph/)** — Python/JavaScript framework for stateful, multi-step agents with explicit graph topology, typed state, and `interrupt()`/`Command` primitives for HIL. Deep integration with the broader LangChain ecosystem.
- **[CrewAI](https://www.crewai.com/)** — Python framework for multi-agent orchestration with role-based agents and task delegation.
- **[Agent Development Kit (ADK)](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview)** — Google's open-source Python/Java/Go framework, part of Vertex AI Agent Builder. Provides `FunctionTool`, `OpenAPIToolset`, `McpToolset`, and `ToolConfirmation` primitives.
- **[OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents)** — OpenAI's Python/TypeScript framework for agents built on the OpenAI API.
- **[AG2](https://github.com/ag2ai/ag2)** and **[LlamaIndex](https://docs.llamaindex.ai/)** — additional Python frameworks with different design philosophies.

### Low-code / visual builders

You configure the agent through a UI rather than writing code. Good for prototypes, for non-technical users, and for workflows that fit the builder's feature set. Usually has a "get code" export that transitions you to a code-first framework when you outgrow the UI.

Examples today:

- **[Vertex AI Agent Designer](https://docs.cloud.google.com/agent-builder/agent-designer)** — Google Cloud's low-code visual designer inside Vertex AI Agent Builder. Details panel for agent configuration, Flow tab for sub-agents, tool types include Google Search, URL context, Vertex AI Search Data Stores, and MCP servers.
- **[Dialogflow CX](https://docs.cloud.google.com/dialogflow/cx/docs/concept/agent)** — Google Cloud's older conversational agent platform with Playbooks, Flows, and data stores. Still supported and integrates with Vertex AI.
- Various other low-code agent builders from cloud providers and startups.

### Managed agent platforms

You provide the instructions and tools; the platform handles everything else — runtime, scaling, persistence, observability. Usually the fastest path to production but with less control over the runtime shape.

Examples today:

- **[Vertex AI Agent Engine](https://docs.cloud.google.com/agent-builder/agent-engine/overview)** — Google's managed runtime for agents built with ADK, LangChain, LangGraph, AG2, or LlamaIndex. Handles deployment, scaling, sessions, memory, evaluation, and code execution sandboxes.
- **[LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/)** — LangChain's managed deployment platform for LangGraph agents.
- Platform-as-a-service offerings from cloud providers (Azure, AWS, GCP) that bundle agent building and runtime.

---

## Decision rubric

Walk this list top to bottom. The first match wins:

1. **Do you have no engineers, and need to prototype fast?** → Try a low-code visual builder first. You can export to code later if you outgrow it.
2. **Does your organisation already use a specific agent platform for other projects?** → Use the same one. Consistency of tooling, observability, and skills beats theoretical best-of-breed.
3. **Do you need to self-host, avoid a specific cloud, or have strict data residency requirements?** → Code-first framework + your own runtime.
4. **Do you need maximum control over the flow, state, tool wiring, and HIL primitives?** → Code-first framework.
5. **Do you want the fastest path to production and don't mind being on a specific cloud?** → Managed agent platform on that cloud.

---

## What to evaluate when choosing

Regardless of which category you pick, check these things before committing:

- **HIL support.** Does the platform have structured pause-and-resume primitives, or do you have to enforce HIL through instructions text? Structured primitives are strictly better when your HIL checkpoints are load-bearing.
- **Tool type support.** What kinds of tools can you register — raw HTTP APIs, OpenAPI specs, MCP servers, custom functions? Does the platform support authenticated tools, or are there limits (some preview features only support unauthenticated endpoints)?
- **State persistence.** Does the platform handle durable state across pauses, across restarts, across long-running workflows? What's the persistence backend, and does it meet your compliance needs?
- **Observability and tracing.** Can you see what the agent did — every action, every tool call, every model response — after the fact? How long are traces retained?
- **Evaluation support.** Does the platform provide automated testing, LLM-as-judge evaluators, or regression tracking?
- **Model access.** Does it work with the model provider you want (Claude, GPT, Gemini, Llama, etc.), or does it lock you in?
- **Cost model.** Per-run, per-token, managed compute — which dimensions will drive your bill at your expected scale?
- **Vendor lock-in.** If you need to migrate later, how portable is your agent definition? A framework that defines your agent in standard Python is more portable than one that stores it in a proprietary visual format.

---

## What this framework does **not** teach

This framework does not cover:

- **How to install or set up any specific platform.** That's in the platform's own docs.
- **Specific SDK class names, import paths, or API shapes.** Those change faster than we can update docs.
- **Which specific MCP servers, connectors, or integrations to use.** Check your platform's current catalogue.
- **Current pricing or feature comparisons.** These are in the vendors' marketing pages and will be out of date by the time you read them.

The framework teaches *what* a good scope, design, and build look like. Any honest platform documentation will teach you *how* to implement those on their tool. The combination is what produces a working agent.

---

## Next steps

- [Stage 1: Decompose](../stages/01-decompose.md) — start the framework (you don't need a platform for this)
- [Stage 4: Design](../stages/04-design.md) — platform-neutral design methodology
- [Stage 5: Build](../stages/05-build.md) — platform-neutral build principles; consult your chosen platform's docs for implementation specifics
