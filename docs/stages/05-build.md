# Stage 5: Build

You have a design document that specifies the agent's architecture, data flow, human checkpoints, and error handling. Now you turn that into a working agent.

This stage is where the agent becomes real. **How** you build it depends on your platform — code-first frameworks use programming languages; low-code builders use a UI; hosted platforms use their own SDKs. The framework doesn't teach any of those — it teaches **what a good build produces** regardless of platform, and leaves the implementation specifics to your chosen tool's documentation. See [Getting Started: Choose a Platform](../getting-started/choose-a-platform.md) for current options.

**What this page covers:** the principles, conventions, and testing approaches that make a build successful. None of it is framework-specific. All of it should be true whether you build on a framework that exists today or one that ships next year.

---

## Inputs

!!! info "What You Need"
    - Design Document from [Stage 4: Design](04-design.md)
    - Credentials and access for each data source in your Data Inventory
    - Your chosen platform set up and ready (SDK installed, project created, console access, etc.)

## Output Artifact

!!! info "Key Output"
    A working agent that:

    - Implements every action defined in the design document
    - Wires the tools listed in the Data Inventory
    - Enforces the HIL checkpoints designed in Stage 4
    - Handles every failure mode from the Error Path Register
    - Has been tested end-to-end with representative inputs, including the failure paths

    Plus whatever artefacts your platform's deployment model requires (code in a repo, a configured agent in a console, a deployed service — whichever shape your platform uses).

---

## Principles for a Good Build

### 1. The design document is the contract

Stage 5 implements Stage 4. Every action, tool, memory field, HIL checkpoint, and error handler in your design should appear in the build. If the build deviates, either the design was wrong (update it) or the build is wrong (fix it). Don't let drift accumulate silently — the design document is where future readers will go to understand the system.

If you find yourself wanting to add something during build that isn't in the design, pause and ask: should this be in the design? If yes, update Stage 4 before implementing. If no, you probably shouldn't be adding it at all.

### 2. Tools handle external I/O, actions handle decisions

This is the most common structural mistake in early builds: putting decision logic inside a tool function, so the tool wrapping a CRM API also decides what to do if the CRM is down.

Keep them separated:

- **Tools** are thin wrappers around external systems. They make a single call, return a result or an error, and do nothing else. Retry logic for transient failures can live here; decision-making about what to do with a failure does not.
- **Actions** decide what to do with tool results. If the CRM tool returns an error, the action checks for the error and decides: continue with partial data, skip this dimension, or escalate to a human.

This separation is what lets Stage 4's error handling design actually work. Each action's error-handling strategy (error marker and continue, retry, escalate, abort) is enforceable in the action because the tool gave it a clean result or a clean error to work with.

### 3. Externalise everything that isn't logic

Config, prompts, thresholds, scoring rubrics, tier benchmarks, retry counts — these all change independently of the agent's logic. Put them in config files, environment variables, or a data store the agent loads at startup. The Ops team or whoever owns the business rules should be able to update them without touching the agent code.

**Pseudocode of the pattern:**

```
# At startup
config = load_config("config.json")
scoring_rubric = load_rubric("scoring_rubric.json")

// In an action
action analyse_ticket_health(memory, config, scoring_rubric):
    thresholds = scoring_rubric.sla_benchmarks
    // ... reasoning using thresholds ...
```

This is also what makes personalisation and per-org customisation tractable: when an organisation forks the framework for their own use, they change the config, not the code.

### 4. Every action's output should be inspectable

When something goes wrong in testing, you want to be able to open the memory state at every action boundary and see exactly what the action received and what it produced. If intermediate state is buried inside an action and only the final output is visible, you can't tell where the failure came from.

The design document's memory/state section should name explicit fields for every significant piece of data. The build preserves that — don't collapse the design's memory fields into local variables inside an action just because the platform would let you.

### 5. HIL checkpoints must genuinely pause

The most common HIL failure mode is an agent that presents its output and continues to the next step in the same turn, never actually waiting for the human. Some platforms have product-level primitives for this (structured confirmation APIs); others rely on the agent interpreting its own instructions literally. Both can work, but both need testing — the agent skipping a pause is the one failure that can't be caught by looking at the final output, because the final output was produced as if the pause had happened.

Your Stage 4 HIL design specified what each checkpoint surfaces and what input it expects. The build implements that. Stage 6 tests that it actually pauses — see the testing section below.

### 6. Fail loud, not silent

When a tool errors, when a model returns malformed output, when a required memory field is missing — the agent should say so. The most dangerous failure mode is an agent that fills a gap with plausible-sounding fabrication because it has no instructions for what to do when data is absent.

Two practices that enforce this:

- **Every output the agent produces must be attributable to a tool result or a memory field.** If a metric appears in the report, it must have come from a tool response. If it doesn't, the agent fabricated it.
- **The agent's instructions must explicitly handle the "missing data" case** for every source. Not "use whatever data is available" but "if the CRM tool returned null, note that tier-specific benchmarks cannot be applied, and score that dimension as Not Assessed."

---

## Build Conventions

### Project structure

Regardless of platform, your build has a few conceptual components. Name them consistently so future readers can navigate the code or configuration:

| Component | What it is |
|---|---|
| **Agent definition** | The top-level entity that ties actions, tools, memory, and instructions together |
| **Action definitions** | One per action in the design — the code or configuration that executes an action |
| **Tool definitions** | One per tool in the Data Inventory — the thin wrappers around external systems |
| **Memory / state schema** | The explicit shape of what the agent remembers between actions |
| **Instructions** | The prompt text that guides the agent's reasoning steps |
| **Config** | Externalised thresholds, benchmarks, rubrics, and environment-dependent values |
| **Tests** | Unit tests for tools, integration tests for the end-to-end flow, scenario tests for failure modes |

How your platform names and organises these varies. What matters is that each one is identifiable and the mapping to the design document's fields is traceable.

### Tools are thin wrappers

A tool function (or tool configuration, depending on platform) wraps one external system operation. It has a single responsibility: make the call, return the result or a structured error.

**Pseudocode of a good tool:**

```
// Tool: thin wrapper around one external system operation
// Returns { ok: true, data: ... } on success, { ok: false, error: ... } on failure

function fetch_crm_data(account_id):
    try:
        response = http_get(
            url: crm_base_url + "/accounts/" + account_id,
            auth: crm_credentials,
            timeout: config.tool_timeouts.crm
        )
        if response.status == 200:
            return { ok: true, data: response.body }
        return { ok: false, error: "http_" + response.status }
    catch network_error:
        return { ok: false, error: "network_error" }
    catch timeout:
        return { ok: false, error: "timeout" }
```

Note what it does *not* do: it doesn't decide whether to retry, it doesn't fill in default data on failure, it doesn't log anything platform-specific. It returns a clean result the action can reason about.

!!! note "Pseudocode convention"
    Pseudocode in the framework is illustrative, not runnable. It uses 4-space indentation, `//` comments, `memory.field` for state access, and `if`/`else` rather than ternaries. See `MAINTAINER_GUIDE.md` at the project root for the full convention.

### Actions consume tool results

An action reads from memory, invokes the tools it needs, reasons over the results (itself or via a language-model prompt), and writes to memory:

```
action gather_data(memory):
    memory.crm = fetch_crm_data(memory.account_id)
    memory.tickets = fetch_support_tickets(memory.account_id, memory.quarter)
    memory.usage = fetch_usage_metrics(memory.account_id, memory.quarter)
    memory.comms = fetch_comms_context(memory.account_id, memory.contact_names, memory.quarter)

    // Error-handling strategy: error marker and continue.
    // Downstream actions check for .ok == false and handle gaps.

    memory.data_gaps = [
        name for (name, value) in memory.retrieved_fields
        if not value.ok
    ]
```

An action that uses a language model to reason looks similar, with the prompt construction and model invocation wrapped inside:

```
action analyse_ticket_health(memory, config, scoring_rubric):
    if not memory.tickets.ok:
        memory.ticket_analysis = { score: "Not Assessed", reason: "ticket data unavailable" }
        return

    prompt = build_prompt(
        template: TICKET_ANALYSIS_PROMPT,
        context: {
            tickets: memory.tickets.data,
            sla_benchmarks: scoring_rubric.sla_benchmarks,
            tier: memory.crm.data.tier,
        },
        output_format: "json with keys score, trend, sla_compliance, key_issues, details"
    )
    memory.ticket_analysis = invoke_model(prompt, temperature: 0.2)
```

The pseudocode isn't meant to be runnable — it's meant to show the shape. Your platform will have its own way of expressing each piece. What matters is that the shape matches.

### HIL checkpoints pause-and-resume

Your platform determines how the pause is implemented. Two families:

**Platform-level pause primitives.** Some frameworks provide explicit pause-and-resume primitives — the action halts, state is checkpointed, and the platform resumes when the human responds. This gives you a hard guarantee that the agent cannot proceed past the pause.

**Instruction-based pause.** Other platforms (especially low-code builders with no pause primitive) rely on the agent interpreting its instructions literally — "wait for the user's response before continuing." This works when the instructions are clear and the model is reliable, but it's weaker than a platform primitive because a confused or distracted model can continue anyway.

If you have a choice, use a platform primitive for any HIL checkpoint whose correctness is load-bearing — especially writes back to external systems. Instruction-based pauses are fine for review checkpoints where the downstream action can catch mistakes, and they're your only option on some platforms.

Either way, **test that the pause actually happens.** See the testing section below.

### Config externalisation

Move every value that changes independently of the code into config:

- Thresholds and benchmarks (SLA targets, DAU/MAU floors, scoring criteria)
- Model selection and generation parameters (temperature, max tokens)
- API endpoints and credentials (use environment variables or a secret manager)
- Retry counts and timeouts
- Prompt templates (pull into separate files if they're long)

**Pseudocode:**

```
// config.json (example shape)
{
    "model": "your-chosen-model",
    "temperature": 0.2,
    "max_output_tokens": 8192,
    "retry_count": 2,
    "tool_timeouts": {
        "crm": 30,
        "support": 30,
        "usage": 60,
        "comms": 90
    }
}

// At agent startup
config = load_config("config.json")
```

The agent code references `config.temperature`, `config.retry_count`, and so on. The Ops team or admin changes the JSON file; the code stays the same.

---

## Observability and Tracing

Every production agent needs structured trace data that lets you reconstruct exactly what happened on a given run. When a reviewer disputes an analysis, when a bug report mentions a specific account, when a compliance audit asks "show me every time the agent touched this customer's data" — you answer these questions by reading traces, not by guessing.

What you want from a trace:

- **Per-action inputs, outputs, and duration.** For every action the agent ran, you can see what memory state it received, what memory state it produced, and how long it took.
- **Model prompts and responses.** The exact text of every prompt sent to the language model and the exact response received. This is what lets you diagnose "the agent said something wrong" — if the prompt was wrong, fix the prompt; if the response was wrong, tighten the prompt or adjust the model; if the prompt and response were both fine but downstream logic misinterpreted, fix the downstream logic.
- **Tool calls, parameters, and responses.** Every external system interaction, with the exact arguments and the exact response. This is what lets you diagnose "the data is wrong" — you compare the tool response to what the external system actually has.
- **Error events with full context.** When an action fails, when a tool errors, when a model returns malformed output, the trace captures what happened and what state the agent was in.
- **Retention that meets your compliance requirements.** Traces contain the same data the agent processed — customer PII, financial data, whatever your workflow touches. Treat trace storage with the same security and retention rules you apply to the underlying data.

### What your platform should provide

Every production-grade agent platform provides at least basic tracing. Code-first frameworks typically support OpenTelemetry export and/or a first-party tracing service. Low-code builders typically provide built-in trace logging through their cloud provider's observability stack. Before committing to a platform, verify:

- [ ] Traces capture all of the fields listed above (inputs, outputs, prompts, responses, tool calls, errors)
- [ ] Traces persist long enough to support your debugging cycles and compliance requirements
- [ ] You can filter traces by run ID, by action name, by error type, and by time range
- [ ] You can export traces for long-term archival if your compliance regime requires it
- [ ] Trace storage is encrypted at rest and access-controlled

A platform without a trace story is not a production platform. Walk away.

### Reading a trace to diagnose a failure

The methodology from [Stage 4's error handling](04-design.md#error-handling-design) gives you four failure categories: tool failures, data quality failures, model failures, boundary failures. For each category, the trace tells you different things:

- **Tool failures** — the trace shows the tool call and the error returned. Compare against the external system's own logs to confirm. Fix: the tool's retry strategy, the tool's auth, or the upstream system.
- **Data quality failures** — the trace shows the tool call succeeded but the response was empty/malformed/partial. Fix: either the upstream data source (more work, more value) or the action's error handling to gracefully degrade.
- **Model failures** — the trace shows the exact prompt sent and the exact response received. If the response was malformed, the prompt probably didn't specify the output shape tightly enough. If the response was wrong, the prompt probably didn't give enough context, or your test coverage didn't include this case.
- **Boundary failures** — the trace shows the agent attempting something outside its scope. Fix: tighten the constraints in the agent's instructions, or add a guard action that catches the violation.

The combination of structured traces and the error-handling strategies designed in Stage 4 is what makes agents debuggable. Without traces, you're guessing.

See the [Platform Cheat Sheet — observability column](../reference/platform-cheatsheet.md#code-first-frameworks) for each platform's specific tracing primitive.

---

## Testing the Build

Testing is how you find out whether Stage 5 actually implements Stage 4. There are four categories of test you should run before declaring the build complete.

### 1. Happy-path test

Run the agent end-to-end with realistic inputs where all the tools return data and the workflow completes successfully. Check that:

- Every action in the design runs
- Every tool in the Data Inventory gets called
- The HIL checkpoints actually pause and wait for input
- The final output matches the expected format

This is the minimum bar. If the happy path doesn't work, nothing else matters.

### 2. Failure-mode tests

For each failure mode in your scope document's Error Path Register, run a test that triggers it and verify the agent's response matches the strategy designed in Stage 4:

| Failure mode | Test |
|---|---|
| Tool returns HTTP error | Point the tool at an unreachable endpoint; verify the agent reports the gap explicitly rather than fabricating data |
| Tool returns empty | Use an input that has no data (no tickets for the quarter, first review cycle with no prior report); verify the agent notes the gap and continues |
| Required field missing | Use a record with null values in required fields; verify the agent flags the gap rather than defaulting |
| Malformed model output | Run the agent with a deliberately weak prompt that produces non-JSON output; verify the retry strategy works |
| HIL reviewer unresponsive | Start a run and leave the checkpoint hanging; verify the state persists and the run can be resumed later |

Every row that corresponds to a real failure mode in your Error Path Register needs a test.

### 3. Hallucination tests

This is the most critical — and most commonly skipped — test category. Fabrication is the default failure mode for language-model-based agents, and an agent that confidently invents plausible numbers is worse than an agent that crashes.

For each metric the agent produces in its output, verify it traces to a tool response:

- Run the agent on known inputs where you know what the tool responses contain
- Compare every number in the agent's output against the raw tool responses
- Flag any number that doesn't appear in the responses — the agent fabricated it

Add explicit instructions to catch what you find: "Use only data returned by tools. Every metric you cite must appear in a tool response. If a metric is not in the tool response, state that it is unavailable."

### 4. HIL pause tests

Test that the agent actually waits at each HIL checkpoint:

- Run the agent and let it reach the first checkpoint
- Verify it stops — no further output, no further tool calls
- Wait longer than you think is reasonable (30 seconds, a minute) — the agent should still be waiting
- Provide the expected response and verify the agent continues correctly
- Test each response path: approve, reject with specific feedback, reject with vague feedback

The most common HIL failure mode is an agent that presents and continues in the same turn. You only catch this by watching for it explicitly.

---

## Deployment Readiness

Before your agent is ready to run beyond the development environment, check:

- **All tool credentials are in a secret store**, not hardcoded or committed to source control
- **Config is externalised** and can be updated without a redeploy
- **The agent handles rate limits and transient failures** gracefully (retry with backoff, not infinite retry)
- **Logs are structured enough to debug a failed run** — you can tell which action ran, what it received, what it produced
- **HIL checkpoint state persists** across restarts if your platform supports it; if not, document the constraint clearly
- **Data-handling decisions are documented** — what data flows through the model, what's retained, what compliance obligations apply
- **There is a clear rollback plan** if a new version of the agent produces worse results than the previous one

How each of these is implemented depends on the platform. The framework doesn't prescribe specific implementations — it prescribes the questions you must have answered before you deploy.

---

## Worked Example

For a concrete build walkthrough applied to the CSM Quarterly Health Review, see the [worked example build page](../worked-example/build.md). It shows every action's implementation shape, tool wiring, HIL handling, and test plan in platform-neutral terms.

---

## Next Step

After building and testing the agent, move to [Stage 6: Evaluate](06-evaluate.md) to assess quality against realistic scenarios and iterate.

!!! tip "Implementing on your platform"
    The [Platform Cheat Sheet](../reference/platform-cheatsheet.md) maps the build-time concepts on this page (action implementations, tool types, HIL primitives, observability, deployment) to the equivalent primitives on several popular platforms, with links to vendor docs. It is not framework doctrine — it's a maintainer's current reference — but it's the right place to start when you're translating the design into a specific platform's syntax.
