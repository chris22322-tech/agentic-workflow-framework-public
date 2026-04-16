# Prerequisites

What you need before working through the framework.

The framework has two phases with very different requirements. **Stages 1–3 are thinking work** — analysing your workflows, picking the right one to automate, and scoping it in detail. **Stages 4–6 are building work** — designing, implementing, and evaluating the agent. The framework is platform-neutral, so the specific tools you need in Stages 4–6 depend on the platform your team picks.

---

## Stages 1–3: Thinking Stages

### What you need

**Nothing technical.** Stages 1–3 require knowledge of your own workflows and the framework templates. That's it.

- A text editor (Google Docs, Word, Notion, even pen and paper)
- The downloadable templates for Stages 1–3
- Knowledge of the workflows you perform in your role
- Access to colleagues who can validate your workflow descriptions (helpful, not required)

These stages produce documentation — a workflow inventory, a prioritisation scorecard, and a detailed scope document. The output is structured thinking, not code.

!!! info "Non-technical users"
    If you're a knowledge worker doing Stages 1–3 and handing off to an engineer for Stages 4–6, you only need a text editor and the templates. The scope document you produce in Stage 3 is designed to be a complete handoff artifact — an engineer can pick it up and move straight to Stage 4 without needing you to explain what the agent should do. If your team uses a low-code builder instead, you may be able to complete all six stages yourself. See [Choose a Platform](choose-a-platform.md) for pointers.

---

## Stages 4–6: Building Stages

Everything below is needed only when you reach Stage 4 (Design) and begin building the agent. The framework itself is platform-neutral — it tells you **what** to design and build, not **which** platform to use. Your team's prerequisites depend on the platform you choose.

See [Choose a Platform](choose-a-platform.md) for an overview of current popular options.

### If you haven't picked a platform yet

You don't have to decide before Stage 4. The design work in Stage 4 is platform-neutral — you produce a design document that describes actions, memory, HIL checkpoints, and error handling in terms that apply to any agent framework. The design document is then the contract that any platform's build process implements.

What you **do** need before Stage 5 (Build):

- **A platform choice**, and access to it (an account on the platform, or the SDK installed locally)
- **A model provider**, and access to it (API key or managed-service access to whichever language model your platform supports)
- **API credentials for your data sources**, scoped narrowly to the tables/endpoints the agent needs
- **A place for the agent to run** once built — whether that's the platform's managed runtime, your own infrastructure, or a local dev environment during prototyping

### Common requirements regardless of platform

These apply whether you're using a code-first framework, a low-code builder, or a hosted agent platform:

**Access to your data sources.** Every tool the agent calls needs read (and possibly write) access to a real system. Before you reach Stage 5, verify that the data sources you identified in Stage 3 (Scope) actually have usable APIs or connectors. If a critical data source has no programmatic access, you'll need to revisit your scope.

Typical access needs:

- CRM API token or service account
- Support platform API key
- Analytics / warehouse read access
- Communications platform credentials (chat, email, call recording, etc.)
- Write-back credentials if the agent updates systems of record

**A model provider account.** Every platform uses a language model for the reasoning steps. You'll need API access to whichever model your chosen platform supports — this may be built into the platform (some managed services bundle model access) or require a separate provider account.

**A secrets store.** Production agents should never have credentials hardcoded. Use whatever secret manager your platform or cloud provides.

**Persistence for HIL checkpoints.** Any workflow with a human-in-the-loop checkpoint needs durable state persistence so that a reviewer who takes hours (or days) to respond doesn't cause the run to fail. Most production-grade agent frameworks provide this; verify your chosen platform does before relying on HIL in production.

**An evaluation plan.** Stage 6 is where you test the agent. Plan the test data, success criteria, and environment before you build — evaluating against real production data is a compliance question, not just a technical one.

---

## Next steps

- [Choose a Platform](choose-a-platform.md) — pointers to current popular agent frameworks
- [How to Use This Framework](how-to-use.md) — understand the stage-based structure
- [Stage 1: Decompose](../stages/01-decompose.md) — start the framework
