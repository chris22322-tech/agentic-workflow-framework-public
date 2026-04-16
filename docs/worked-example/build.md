# Worked Example: Stage 5 — Build

!!! example "Worked Example"
    We're applying Stage 5 to: **Quarterly Account Health Review**. The goal is to take the [design document](design.md) from Stage 4 and turn it into a working agent. This worked example shows the *shape* of the implementation using platform-neutral pseudocode — it demonstrates the patterns from the [Stage 5 methodology](../stages/05-build.md) applied to this specific workflow. Your actual implementation will use whichever framework your team has chosen; see [Getting Started: Choose a Platform](../getting-started/choose-a-platform.md) for some current options.

This page does not contain runnable code. Pseudocode is deliberate — it shows the contract between the design and any platform-specific implementation without locking you into one framework's imports, class names, or syntax.

---

## Build Overview

The Stage 4 design specified:

- **6 actions**: `gather_data`, `analyse_health`, `hil_review_analysis`, `synthesise`, `generate_report`, `hil_review_report`
- **6 tools**: `get_crm_data`, `get_support_tickets`, `get_usage_metrics`, `search_comms`, `get_cs_platform_score`, `get_prior_report`
- **2 HIL checkpoints**: after analysis and after report generation
- **1 scoring rubric** loaded as config at startup
- **Memory fields** covering input, retrieved data, analysis outputs, synthesis outputs, human feedback, and final deliverables

The build implements each of these. The rest of this page walks through the shape of each component.

---

## Project Structure

Regardless of platform, the build has these conceptual pieces. How you organise them in your repo or configuration console is up to your platform's conventions.

| Component | Purpose |
|---|---|
| **Agent definition** | Wires the actions together into the flow from the design |
| **Action definitions** | One per action in the design — implements the action's logic, tool calls, reasoning, and error handling |
| **Tool definitions** | One per tool — a thin wrapper around a single external system operation |
| **Memory / state schema** | Explicit shape of every field the design specified |
| **Instructions and prompt templates** | The text that guides the model's reasoning in each action |
| **Config** | The scoring rubric, model settings, retry counts, tool timeouts |
| **Tests** | Happy-path, failure-mode, hallucination, and HIL-pause tests |

---

## Config: The Scoring Rubric

Externalise the scoring rubric so the Ops team can update thresholds without touching agent code.

**`config/scoring_rubric.json`** (excerpt — full content matches the design document):

```json
{
  "sla_benchmarks": {
    "P1": {"response_minutes": 30, "resolution_hours": 4},
    "P2": {"response_minutes": 120, "resolution_hours": 24},
    "P3": {"response_minutes": 480, "resolution_hours": 72},
    "P4": {"response_minutes": 1440, "resolution_hours": 168},
    "compliance_threshold": 0.95
  },
  "adoption_benchmarks": {
    "enterprise": {"dau_mau_floor": 0.40, "feature_adoption_floor": 0.60, "api_volume_floor": 10000},
    "mid_market": {"dau_mau_floor": 0.30, "feature_adoption_floor": 0.45, "api_volume_floor": 2000},
    "smb": {"dau_mau_floor": 0.25, "feature_adoption_floor": 0.35, "api_volume_floor": 500}
  },
  "health_scoring": {
    "green": { "rule": "All four dimensions pass thresholds" },
    "amber": { "rule": "One or more dimensions in warning band" },
    "red": { "rule": "One or more dimensions critical" },
    "assignment_rule": "Assign the most severe rating triggered by any single dimension"
  },
  "action_urgency": {
    "red_renewal_60d": "Act this week",
    "red_no_renewal": "Act within 30 days",
    "amber_renewal_90d": "Act this month",
    "amber_no_renewal": "Act this quarter",
    "green_opportunity": "Next QBR agenda item"
  }
}
```

At startup, the agent loads the rubric once:

```
scoring_rubric = load_json("config/scoring_rubric.json")
```

Every action that needs thresholds reads from `scoring_rubric`. No hardcoded numbers in the code.

---

## Tools

Each tool is a thin wrapper around one external system operation. It makes the call, returns a structured result or a structured error, and does nothing else.

### Tool: `get_crm_data`

```
function get_crm_data(account_id):
    try:
        response = http_get(crm_base_url + "/accounts/" + account_id,
                            auth=crm_credentials,
                            timeout=config.tool_timeouts.crm)
        if response.status == 200:
            return { "ok": true, "data": response.body }
        return { "ok": false, "error": "http_" + response.status }
    catch network_error:
        return { "ok": false, "error": "network_error" }
    catch timeout:
        return { "ok": false, "error": "timeout" }
```

Note what it does **not** do:

- It does not retry — that's the action's decision, not the tool's.
- It does not log anything platform-specific — logging happens at the action boundary.
- It does not fill in default data on failure — it returns a clean error the action can reason about.
- It does not know about the scoring rubric or any downstream consumer — it just retrieves account data.

This shape repeats for every tool in the design:

```
function get_support_tickets(account_id, start_date, end_date):
    // ... same pattern: call, return {ok, data} or {ok: false, error} ...

function get_usage_metrics(account_id, start_date, end_date):
    // ... same pattern ...

function search_comms(account_id, account_name, contact_names, start_date, end_date):
    // ... same pattern ...

function get_cs_platform_score(account_id):
    // ... same pattern, but may return null data if no CS platform is configured ...

function get_prior_report(account_id):
    // ... same pattern, but may return null data if first review cycle ...
```

### Adapting the tools to your systems

The tools above are named after the **capabilities** the agent needs, not specific vendors. In your implementation:

- `get_crm_data` wraps whatever CRM your organisation uses — it might call a specific vendor's API, an internal service, or a database view. The agent doesn't care which.
- `get_support_tickets` wraps your ticketing platform.
- `get_usage_metrics` wraps your product analytics store — a data warehouse, an analytics API, or a product-analytics tool.
- `search_comms` wraps whichever communications channels your team uses for customer conversations. Often this is an aggregator across multiple sources (chat, email, call recordings, CS platform timelines), returning a single normalised response.

This is the main personalisation point. When an org forks the framework for their own use, the personalisation engine fills in the actual systems. The action code that calls `get_crm_data(account_id)` doesn't change.

---

## Actions

Each action reads from memory, invokes tools, reasons (directly or through a model prompt), and writes back to memory.

### Action: `gather_data`

```
action gather_data(memory):
    // The six tool calls are independent and can run concurrently.
    // Your platform will have its own pattern for parallel execution.
    memory.crm_data = get_crm_data(memory.account_id)
    memory.cs_platform_data = get_cs_platform_score(memory.account_id)
    memory.prior_report = get_prior_report(memory.account_id)
    memory.tickets = get_support_tickets(memory.account_id,
                                          memory.quarter_start_date,
                                          memory.quarter_end_date)
    memory.usage_data = get_usage_metrics(memory.account_id,
                                           memory.quarter_start_date,
                                           memory.quarter_end_date)
    memory.comms = search_comms(memory.account_id,
                                 memory.account_name,
                                 memory.contact_names,
                                 memory.quarter_start_date,
                                 memory.quarter_end_date)

    // Error-handling strategy: error marker and continue.
    // Downstream actions check for .ok == false and handle gaps.
    memory.data_gaps = [name for (name, value) in retrieved_fields(memory)
                        if not value.ok]
```

### Action: `analyse_health`

```
action analyse_health(memory, scoring_rubric):
    // Each analysis dimension runs independently.
    // If a dimension's data is unavailable, it's scored "Not Assessed"
    // and the other dimensions still run.

    if memory.tickets.ok:
        memory.ticket_analysis = run_ticket_analysis(
            tickets=memory.tickets.data,
            sla_benchmarks=scoring_rubric.sla_benchmarks,
            tier=memory.crm_data.data.tier if memory.crm_data.ok else null
        )
    else:
        memory.ticket_analysis = { score: "Not Assessed",
                                    reason: memory.tickets.error }

    if memory.usage_data.ok:
        memory.usage_analysis = run_usage_analysis(
            usage=memory.usage_data.data,
            adoption_benchmarks=scoring_rubric.adoption_benchmarks,
            tier=memory.crm_data.data.tier if memory.crm_data.ok else null
        )
    else:
        memory.usage_analysis = { score: "Not Assessed",
                                   reason: memory.usage_data.error }

    if memory.comms.ok:
        memory.sentiment_analysis = run_sentiment_analysis(
            comms=memory.comms.data
        )
    else:
        memory.sentiment_analysis = { score: "Not Assessed",
                                       reason: memory.comms.error }

    // Action follow-through runs only if we have a prior report
    if memory.prior_report.ok and memory.prior_report.data is not null:
        memory.action_followthrough = run_action_followthrough_analysis(
            prior_report=memory.prior_report.data,
            current_crm=memory.crm_data.data,
            current_tickets=memory.tickets.data,
            current_usage=memory.usage_data.data
        )
    else:
        memory.action_followthrough = null  // First review cycle or prior report unavailable
```

Each `run_*_analysis` helper constructs a prompt, invokes the model, parses the response, and returns the structured dimension output. The prompt template for ticket analysis looks like:

```
TICKET_ANALYSIS_PROMPT = """
You are analysing support tickets for a customer account health review.

Account: {account_name} ({tier} tier)
Quarter: {quarter}

Raw ticket data:
{tickets_json}

SLA thresholds for this tier:
{sla_benchmarks_json}

Analyse the tickets against the SLA thresholds. Produce structured JSON with:
- score: "Green" | "Amber" | "Red"
- trend: "improving" | "stable" | "degrading"
- volume_vs_previous_quarter: string describing the comparison
- key_issues: list of strings, the most significant issues
- sla_compliance: string with the compliance percentage
- details: narrative explanation

Rules:
- Only cite data that appears in the raw ticket data above.
- If a metric cannot be calculated from the data, say so explicitly.
- Never infer from absence of data.
"""
```

The prompt encodes the same rules the [design document's prompt pattern](design.md#action-analyse_health) specified. The language model invocation is a single call per dimension; the retry logic for malformed output wraps that call.

### Action: `hil_review_analysis`

```
action hil_review_analysis(memory):
    // Present all analysis dimensions as a single review package
    surfaced = format_for_review(
        memory.ticket_analysis,
        memory.usage_analysis,
        memory.sentiment_analysis,
        memory.action_followthrough  // may be null
    )

    // Pause and wait for the reviewer
    reviewer_response = pause_for_human(surfaced)

    // Store the reviewer's feedback for the synthesise action to consume
    memory.analysis_human_feedback = reviewer_response.text
```

The `pause_for_human` operation is where the platform-specific behaviour matters most. If your platform has a structured pause-and-resume primitive, use it — it gives you a hard guarantee that the agent cannot proceed until the reviewer responds. If your platform only supports instruction-based pauses (the agent's instructions tell it to wait, and the agent interprets them), that's your only option on that platform — but see the [Stage 5 methodology's note on HIL implementation](../stages/05-build.md#5-hil-checkpoints-must-genuinely-pause) for the testing implications.

### Action: `synthesise`

```
action synthesise(memory, scoring_rubric):
    feedback_section = (
        "Reviewer corrections to incorporate:\n" + memory.analysis_human_feedback
        if memory.analysis_human_feedback else ""
    )

    synthesis_prompt = SYNTHESIS_PROMPT.format(
        ticket_analysis=memory.ticket_analysis,
        usage_analysis=memory.usage_analysis,
        sentiment_analysis=memory.sentiment_analysis,
        action_followthrough=memory.action_followthrough,
        feedback_section=feedback_section,
        contract_context=extract_contract_context(memory.crm_data),
        health_scoring=scoring_rubric.health_scoring,
        action_urgency=scoring_rubric.action_urgency,
    )

    result = invoke_model(synthesis_prompt, temperature=0.2, expect_json=true)

    memory.risks = result.risks
    memory.opportunities = result.opportunities
    memory.health_score = result.health_score
    memory.health_justification = result.health_justification
    memory.action_items = result.action_items
    memory.platform_reconciliation = result.platform_reconciliation  // may be null
```

### Action: `generate_report`

```
action generate_report(memory):
    report_prompt = REPORT_PROMPT.format(
        analyses=[memory.ticket_analysis, memory.usage_analysis,
                  memory.sentiment_analysis, memory.action_followthrough],
        synthesis={
            risks: memory.risks,
            opportunities: memory.opportunities,
            health_score: memory.health_score,
            health_justification: memory.health_justification,
            action_items: memory.action_items,
        },
        contract_context=extract_contract_context(memory.crm_data),
        revision_feedback=memory.report_human_feedback  // may be null on first pass
    )

    memory.report_markdown = invoke_model(report_prompt, temperature=0.4)

    summary_prompt = EXEC_SUMMARY_PROMPT.format(report=memory.report_markdown)
    memory.exec_summary = invoke_model(summary_prompt, temperature=0.3)
```

### Action: `hil_review_report`

```
action hil_review_report(memory):
    surfaced = {
        report: memory.report_markdown,
        exec_summary: memory.exec_summary,
    }

    reviewer_response = pause_for_human(surfaced,
                                         expected_structure="decision_and_instructions")

    memory.report_review_decision = reviewer_response.decision  // "approve" | "revise" | "rework"

    if reviewer_response.decision == "revise":
        memory.report_human_feedback = reviewer_response.instructions
    else if reviewer_response.decision == "rework":
        memory.rework_instructions = reviewer_response.instructions

    // The agent framework's routing logic reads memory.report_review_decision
    // and decides the next action: end, generate_report, or analyse_health
```

This action uses the feedback-as-control-flow pattern from the [Stage 4 HIL design](../stages/04-design.md#which-pattern-to-choose) — the reviewer's structured decision determines which action runs next.

---

## Agent Flow Wiring

The agent definition ties the actions together into the flow from the design:

```
agent = Agent(
    actions=[
        gather_data,
        analyse_health,
        hil_review_analysis,
        synthesise,
        generate_report,
        hil_review_report,
    ],
    flow=[
        start → gather_data,
        gather_data → analyse_health,
        analyse_health → hil_review_analysis,
        hil_review_analysis → synthesise,
        synthesise → generate_report,
        generate_report → hil_review_report,
        hil_review_report → (
            if decision == "approved" → end
            if decision == "revise"   → generate_report
            if decision == "rework"   → analyse_health
        ),
    ],
    memory_schema=AccountHealthMemory,
    config=scoring_rubric,
)
```

Your platform expresses this differently — a graph definition, a sequence of steps, an orchestrator function, or a config file. What matters is that the flow matches the design.

---

## Testing the Build

Run the four test categories from the [Stage 5 methodology](../stages/05-build.md#testing-the-build):

### 1. Happy-path test

Run the agent end-to-end with a test account that has complete data. Verify:

- All six actions execute in order
- Each tool is called exactly once (with the expected arguments)
- `hil_review_analysis` pauses after `analyse_health` — no further activity until a reviewer responds
- `hil_review_report` pauses after `generate_report`
- The final report contains all eight sections (seven if first review cycle)

### 2. Failure-mode tests

| Scenario | Setup | Expected behaviour |
|---|---|---|
| CRM tool unavailable | Disconnect the CRM tool / point at a bad endpoint | `data_gaps` contains "crm_data"; analysis scores the affected dimensions as "Not Assessed"; report notes the gap explicitly |
| First review cycle | Use an account with no prior report | `prior_report` is null; `action_followthrough` dimension is skipped; report has seven sections instead of eight |
| Missing critical CRM fields | Use an account where `tier` is null | Analysis skips tier-specific benchmarks; notes the gap rather than defaulting to a tier |
| Empty communications data | Use an account with no recent comms | Sentiment dimension is scored "Not Assessed"; report notes "insufficient data for sentiment" |
| Malformed model output | Deliberately weaken a prompt template | Retry up to 2 times; on persistent failure, escalate via ad-hoc HIL checkpoint |
| Reviewer unresponsive at checkpoint 1 | Start a run and leave the first checkpoint hanging | State persists; run can be resumed later when the reviewer returns |

### 3. Hallucination tests

For each metric in the final report, verify it traces back to a tool response:

- SLA compliance percentages → from `get_support_tickets`
- DAU/MAU ratios → from `get_usage_metrics`
- Sentiment quotes → from `search_comms`
- Action item status → from `get_prior_report`

Run the agent on a known-state test account where you know what the tools return. Every number in the output should be verifiable against the raw tool responses. If a number appears that isn't in any tool response, the agent fabricated it — tighten the prompt constraints ("every metric you cite must appear in a tool response") and re-test.

### 4. HIL pause tests

Test that each checkpoint actually pauses:

- Run to `hil_review_analysis` and verify the agent stops — no further tool calls, no further output
- Wait longer than you'd expect (30+ seconds) — the agent should still be waiting
- Provide a reviewer response and verify the agent continues with the next action
- Test each response path at `hil_review_report`: approve (ends the run), revise (loops back to `generate_report` with instructions), rework (loops back to `analyse_health` with instructions)
- Verify that a reviewer providing an empty/approval response at `hil_review_analysis` doesn't corrupt state for `synthesise`

---

## Adapting This to Your Organisation

The six actions, six tools, scoring rubric structure, HIL checkpoint placement, and error handling strategy are **framework-level decisions**. The parts that change per organisation are:

- **Which systems the tools wrap.** Your CRM is whatever CRM your org uses. Your ticketing platform, your analytics warehouse, your comms channels — whatever you actually have. The tool names (`get_crm_data`, `get_support_tickets`, etc.) stay the same; the implementation behind each name is what gets personalised.
- **The scoring rubric's thresholds.** SLA targets, DAU/MAU floors, CSAT minimums, risk urgency timelines — these reflect your business's definition of health. The structure of the rubric is generic; the values are yours.
- **Tier definitions.** "Enterprise / mid-market / SMB" may not match your org's tiering. Rename and reshape the tiers in the rubric; the analysis logic consumes whatever tiers you define.
- **Report sections.** Your report template may have different sections than the eight shown here. Add or remove sections in the `generate_report` prompt; the rest of the build is unchanged.
- **Your chosen platform.** Everything above adapts to whatever you're building on. See [Getting Started: Choose a Platform](../getting-started/choose-a-platform.md).

See the [Personalise section](../personalise/index.md) for tooling that automates org-specific personalisation.

---

## Next Step

With the agent built and tested, move to [Stage 6: Evaluate](evaluate.md) to run structured test cases against real scenarios and iterate on quality.

[:octicons-arrow-left-24: Stage 5: Build](../stages/05-build.md){ .md-button }
[:octicons-arrow-right-24: Next: Stage 6 Evaluate](evaluate.md){ .md-button .md-button--primary }
