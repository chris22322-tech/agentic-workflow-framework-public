# Stage 6: Evaluate

You have a working agent. Now you need to find out whether it is actually good enough to use — and where it falls short.

This stage is where you run the agent against real scenarios and compare its output to what you would have produced manually. You are looking for three things: does it get the right answer, does it handle edge cases without breaking, and is it actually faster than doing the work yourself once you account for the time spent reviewing and correcting its output. The answer to all three will probably be "not yet" on your first pass — and that is expected. The value of this stage is not a pass/fail verdict. It is a structured way to find the specific problems, diagnose their root causes, fix them, and re-test — iterating until the agent meets a quality bar you are confident in.

This is also the stage where you might discover that something upstream needs to change. A test failure might trace back to a prompt issue you can fix in minutes, or it might reveal that the flow structure needs rethinking (Stage 4) or that the scope boundary was drawn in the wrong place (Stage 3). The framework is designed for these loops — evaluation is not just the last step, it is the feedback mechanism that makes every earlier stage better.

## Inputs

!!! info "What You Need"
    - Working agent from [Stage 5: Build](05-build.md)
    - Historical examples of the manual workflow output (for comparison)

## Output Artifact

!!! info "Key Output"
    An **Evaluation Report** containing:

    1. Test case results
    2. Quality assessment
    3. Failure modes observed
    4. Iteration backlog (prioritised list of improvements)

!!! abstract "Template"

    Use the [Evaluation Report template](../blank-templates/evaluation-report.md) as you work through this stage. It includes the Test Cases table, Iteration Log, and Graduation Checklist.

!!! info "Download Templates"
    [:material-download: Download Spreadsheet](../downloads/Stage 6 - Evaluate.xlsx){ .md-button }
    [:material-download: Download Document Template](../downloads/Stage 6 - Evaluate - Template.docx){ .md-button }

    **Spreadsheet:** Import into Google Sheets for structured tables with example rows.
    **Document:** Word template with instructions, fill-in sections, and completion checklist.

---

## Evaluation Dimensions

Assess your agent across all six dimensions. Skipping any of them leaves blind spots that will surface in production.

| Dimension | What to Assess | How to Measure |
|---|---|---|
| **Correctness** | Does the agent retrieve the right data and produce accurate analysis? | Compare agent output against manually gathered data for the same account/period |
| **Completeness** | Does the agent cover all aspects the manual process covers? | Checklist comparison against a known-good manual report |
| **Quality** | Is the written output (report, summary) at professional standard? | Side-by-side blind comparison with a manually written report -- have a colleague rate both without knowing which is which |
| **Robustness** | How does the agent handle missing data, API failures, or unusual inputs? | Run against edge case accounts (new accounts with little data, accounts with unusually high ticket volume, accounts mid-escalation) |
| **Efficiency** | Is the agent actually saving time? | Measure total time (agent run time + human review/edit time) vs. manual process time |
| **HIL Effectiveness** | Are the checkpoint points at the right places? Is the surfaced information useful? | Track how often the human makes significant changes at each checkpoint. If changes are always minor, the checkpoint may be unnecessary. If changes are always major, the preceding action needs improvement. |
| **Trajectory** | Did the agent take the right path through the flow — correct action sequence, no unnecessary loops, no skipped steps? | Define expected action sequences for each test case; compare against actual execution order via traces. Flag cases where the agent reached the right output via an inefficient or incorrect path. |

Trajectory evaluation catches a class of failures invisible to output-only assessment. An agent can produce a correct report while taking an unnecessarily expensive path — re-running analysis after an unnecessary loop, skipping a data source and compensating downstream, or hitting a HIL checkpoint that should have been automated. Trace-level visibility (see [Evaluation Tooling](#evaluation-tooling) below) makes trajectory evaluation practical.

---

## Test Case Design

Create a minimum of 5 test cases representing different profiles. Don't just test the happy path -- the edge cases are where agents fail.

| Test Case | Profile | Purpose |
|---|---|---|
| **Happy path** | Normal input, all data available, no anomalies | Verify the basic flow works end to end |
| **At-risk scenario** | Declining metrics, open critical issues, upcoming deadline | Verify the agent correctly identifies and escalates risk |
| **Data gap** | One or more data sources return empty or error | Verify graceful degradation -- the agent should flag the gap, not hallucinate data |
| **Sparse data** | Limited history, few records, early-stage input | Verify the agent doesn't over-interpret sparse data |
| **Complex case** | Multiple dimensions, mixed signals, ambiguous indicators | Verify the agent handles nuance and doesn't oversimplify |

For each test case, record:

- **Input:** The initial state you provide
- **Expected behaviour:** What the agent should do at each action
- **Actual behaviour:** What the agent actually did
- **Verdict:** Pass / Fail / Partial
- **Notes:** What went wrong, or what went surprisingly well

!!! warning "Test Data Safety"
    If your [Stage 3 scope document](03-scope.md) flagged a **Data sensitivity / governance** constraint — client data, PII, or commercially sensitive information sent to an external LLM provider — that constraint applies equally to evaluation runs. Every test case you execute sends its input data through the same LLM calls your agent makes in production.

    - **Anonymised or synthetic data first.** If you can evaluate with anonymised or synthetic test data, do so — it avoids compliance review entirely and is sufficient for most correctness and robustness testing. Use real client data only when you need to assess output quality against genuine production complexity.
    - **Evaluation artifacts inherit data classification.** If your test input includes client PII (account names, financial metrics, ticket content, Slack messages), then your test case results, iteration logs, and evaluation report are PII-bearing documents. Handle and share them accordingly.
    - **Checkpoints contain test data.** Every evaluation run produces checkpoints that persist the full agent state — including whatever test data you fed in. The encryption, access control, and retention guidance from [Stage 5: Build](05-build.md#deployment-readiness) applies to your evaluation checkpoint store, not just production.

### What Good Test Results Look Like

The depth of documentation should match the verdict. A Pass needs enough detail to prove you actually checked. A Partial needs a clear diagnosis. A Fail needs enough detail that someone else could implement the fix without asking you questions.

??? example "Pass, Partial, and Fail verdicts across roles"

    **Pass — CSM: Happy path account health review**

    - **Input:** `account_id: ACME-001`, Q4 data. Healthy account, all data sources returning clean data.
    - **Expected behaviour:** Green health score, no major risks, professional report.
    - **Actual behaviour:** Agent gathered all data, scored Green with correct justification. One minor wording tweak at the report review checkpoint.
    - **Verdict:** Pass
    - **Notes:** Exec summary was slightly generic — led with "account remains healthy" rather than the 15% usage increase. Not a correctness issue, but worth noting as a prompt refinement candidate.

    A Pass is not "it worked, moving on." Record anything surprising or slightly off — these accumulate into prompt refinements over time.

    **Partial — BA: Feature request intake missed complexity estimate**

    - **Input:** Incoming feature request for a cross-system integration.
    - **Expected behaviour:** Agent logs request, checks for duplicates, estimates complexity as High (cross-system = multiple teams), drafts impact summary.
    - **Actual behaviour:** Agent correctly logged, deduplicated, and drafted the impact summary. Complexity was estimated as Medium — the prompt assessed the feature in isolation without considering cross-team coordination overhead.
    - **Verdict:** Partial
    - **Notes:** Root cause: `COMPLEXITY_ESTIMATION_PROMPT` evaluates technical effort but has no instruction to factor in coordination overhead (number of teams involved, API contract negotiations). The estimate was reasonable for a single-team feature — the prompt needs a cross-team dimension.

    A Partial requires you to name the root cause and the specific artifact that needs changing. "It got the complexity wrong" is not enough — *why* it got the complexity wrong is what drives the fix.

    **Fail — SE: Release notes missed an entire category of changes**

    - **Input:** Release branch with 23 merged PRs including 4 security patches labelled `security`.
    - **Expected behaviour:** Release notes with a dedicated Security section listing all 4 patches.
    - **Actual behaviour:** Release notes contained Features and Bug Fixes sections only. All 4 security patches were omitted entirely.
    - **Verdict:** Fail
    - **Notes:** Root cause: the `fetch_merged_prs` tool filters by labels `["feature", "bugfix", "enhancement"]`. PRs labelled `security` are not in the filter list, so they are never retrieved. This is a tool issue — the data never reached the prompt. Fix: add `"security"` and `"breaking-change"` to the label filter, and add a Security section to the release notes template.

    A Fail needs enough detail that you could hand it to someone else and they could implement the fix without asking questions. Include: what happened, what should have happened, which layer failed, and what the fix looks like.

---

## Iteration Process

After each evaluation round, follow this cycle:

1. **Categorise failures.** Is the issue in data retrieval (tool), analysis (prompt), workflow structure (flow), or scope (wrong automation boundary)?

2. **Prioritise fixes.** Use the same Impact x Feasibility framework from [Stage 2: Select](02-select.md). Fix the highest-impact, most-feasible issue first.

3. **Implement and re-evaluate.** Fix the highest priority issue, re-run the relevant test cases, confirm the fix doesn't break other cases.

4. **Track progress.** Maintain an iteration log:

    | Date | Change Made | Test Cases Affected | Result |
    |---|---|---|---|
    | *Date* | *What you changed* | *Which test cases you re-ran* | *Pass/Fail/Partial* |

!!! tip "Failure Categories"
    Most failures fall into one of four buckets:

    - **Tool issue** -- The data retrieval is wrong, incomplete, or failing. Fix the tool.
    - **Prompt issue** -- The LLM is misinterpreting data or producing poorly structured output. Fix the prompt.
    - **Flow issue** -- The workflow structure is wrong (actions in the wrong order, missing conditional routes, HIL at the wrong point). Fix the flow.
    - **Scope issue** -- You automated something that shouldn't have been automated, or left out something that should have been included. Go back to [Stage 3: Scope](03-scope.md).

### Diagnosing the Failure Category

Failures frequently present as one category but originate in another. A blended usage score looks like a prompt issue (the LLM produced a vague assessment), but it may be a scope issue (the scope assumed single-product accounts, so the schema has nowhere to store per-product results). If you default to the most accessible fix — tweaking the prompt — you waste an iteration cycle and the failure persists.

Use systematic elimination to find the actual root cause. Check each layer in order, starting from the data and working outward:

**1. Tool layer — Was the right data retrieved?**
Check whether the tool returned correct, complete data. If the raw data is wrong or missing, the failure is a tool issue regardless of what the other layers did.

**2. Prompt layer — Given the data it received, did the prompt produce the right analysis?**
Assume the data is correct (you just verified it). Read the prompt's input and output. Did the LLM do what the prompt asked? If the prompt asked for the wrong thing — missing instructions, no weighting criteria, no edge case guidance — this is a prompt issue.

**3. Flow layer — Is the action in the right position with the right inputs?**
Assume data and analysis are correct. Check whether the action receives its inputs from the right upstream actions, whether conditional routes work correctly, and whether HIL checkpoints are placed where they can catch problems. If the structure forces the right analysis into the wrong place in the workflow, this is a flow issue.

**4. Scope layer — Does the scope support what the agent needs to represent?**
Assume data, analysis, and structure are all sound for what they were designed to do. Check whether the scope — the steps, their outputs, and the memory fields they imply — can represent the distinctions this test case requires. If the memory has no field for per-product analysis, no prompt or flow change can produce per-product output. This is a scope issue.

At each layer, ask one question: **"Did this layer work correctly given what it received?"** The first layer where the answer is "no" or "it structurally cannot" is the failure category.

The ordering matters. Tool fixes are cheapest (change a query or API call) and have the smallest blast radius (only the tool's output changes). Prompt fixes are next (change instructions to the LLM, re-run the action). Flow fixes require updating the design and rebuilding affected actions. Scope fixes cascade through Stages 3 → 4 → 5. By checking in this order, you find the cheapest adequate fix first and avoid unnecessary cascading changes.

!!! example "This technique in practice"
    The [worked example's Test Case 5](../worked-example/evaluate.md#cross-stage-iteration-cycle) demonstrates full systematic elimination for a complex failure. The usage analysis returned a blended "Needs Attention" score for a multi-product account — which looks like a prompt issue. Walking the layers: the tool returned correct data for both products (tool ✓), the prompt produced a reasonable single-score assessment given the combined data it received (prompt ✓), the flow structure was a consequence of a deeper problem (flow — partial), and the scope's Step 7 described a single "Assess product engagement" step with no per-product dimension (scope ✗). The root cause was scope, not prompt. A prompt tweak would have been wasted effort.

??? example "Walking the four layers — three failures, three different root causes"

    Each example below takes a test case failure and walks through the four-layer elimination technique. Notice how each one lands on a different layer.

    **CSM — Renewal risk report understates urgency (prompt issue)**

    The agent produced a renewal brief rating risk as "Moderate" for an account 45 days from renewal with usage down 40% and two unresolved P1 tickets. The manually written brief rated the same account as "High Risk — immediate action required."

    1. **Tool layer — Was the right data retrieved?** Yes. The tool returned the usage decline (40% QoQ), the two open P1 tickets, and the renewal date. All data correct and complete. ✓
    2. **Prompt layer — Given the data, did the prompt produce the right analysis?** No. The `RENEWAL_RISK_PROMPT` assesses risk based on usage trends and ticket volume independently. Each signal alone rates "Moderate" — but the combination near a deadline should compound to "High." The prompt has no compounding logic. ✗
    3. Layers 3–4 not reached — failure identified at layer 2.

    **Fix:** Add compounding logic: "When multiple negative signals are present simultaneously and a renewal is within 60 days, escalate the overall risk rating by one level."

    **BA — Duplicate feature requests not caught (flow issue)**

    The agent processed a feature request nearly identical to an existing backlog item but did not flag the duplicate.

    1. **Tool layer — Was the right data retrieved?** Yes. The `fetch_backlog` tool returned the full backlog including the existing similar item. ✓
    2. **Prompt layer — Given the data, did the prompt produce the right analysis?** The duplicate-check prompt was never invoked for this request. ✓ (not the issue, but need to check the flow)
    3. **Flow layer — Is the action in the right position with the right inputs?** No. The duplicate-check action is placed *after* prioritisation. The conditional route from prioritisation sends low-priority items directly to the backlog, bypassing duplicate checking. This request was assessed as low priority, so it skipped the check entirely. ✗
    4. Layer 4 not reached — failure identified at layer 3.

    **Fix:** Move the duplicate-check action *before* prioritisation. Every request should be checked for duplicates regardless of priority.

    **SE — Release notes omit hotfix PRs (tool issue)**

    The agent's release notes listed 18 changes, but the manual notes had 22. The four missing items were all hotfix PRs.

    1. **Tool layer — Was the right data retrieved?** No. The `fetch_merged_prs` tool queries for PRs merged to `main` since the last release tag. The four hotfix PRs were merged to `release/2.3.x` and cherry-picked to `main` — the cherry-pick commits do not appear as merged PRs in the GitHub API response. ✗
    2. Layers 2–4 not reached — failure identified at layer 1.

    **Fix:** Update the tool query to include PRs merged to `release/*` branches, or detect cherry-pick commits and trace them back to their original PRs.

    The pattern: start at the data, work outward. The first layer that did not do its job correctly is where you fix. Do not default to prompt tweaking — it is the most tempting fix but frequently the wrong one.

### Navigating Cross-Stage Iteration

Tool and prompt failures stay within Stages 5–6: change the code or prompt, re-run test cases. Flow and scope failures are different — they require updating artifacts from earlier stages and cascading those changes forward.

| Failure Category | Go Back To | What to Update | Downstream Cascade | Evaluation Progress |
|---|---|---|---|---|
| **Flow issue** | [Stage 4: Design](04-design.md) | The affected portion of the flow structure — add, remove, or reorder actions, change routing, move HIL checkpoints. You do not redo the full Design Document. | Review and update the action implementations (Stage 5) affected by the structural change. Actions unrelated to the change stay as-is. | Re-run test cases that touch the modified actions, plus the cases that originally exposed the failure. Cases that only exercise unaffected parts of the flow do not need re-running. |
| **Scope issue** | [Stage 3: Scope](03-scope.md) | The affected steps and their boundary tags (AUTOMATE / HIL / MANUAL) in the Workflow Scope Document. You do not redo the entire scope — only the steps where the boundary was wrong. | A scope change always requires reviewing the Design Document (Stage 4), because the flow structure may need new or removed actions to reflect the updated boundary. After the design is updated, update the affected code (Stage 5). | Re-run all test cases that touch the changed steps. Cases for unaffected portions of the workflow are still valid. |

**The principle:** update only the part of each artifact that is affected by the change, then cascade forward through each downstream stage in order. Do not skip intermediate stages — a scope change that bypasses the Design Document creates drift between what the design says and what the code does, making future iterations harder to reason about.

### Iteration Cycle in Practice

Here is one complete iteration cycle. Then three brief examples show how different failure categories lead to different fix scopes.

**Full cycle: BA sprint planning prep produces stale velocity data**

The agent's sprint planning brief recommended a capacity of 42 story points. The actual recent velocity was 31 — the team had lost a developer two sprints ago and velocity had dropped. The agent used a straight 6-sprint average instead of weighting recent sprints.

**Diagnose.** The velocity data from the tool was correct — all six sprints were accurate. The prompt calculated a straight average. The brief would have over-committed the team by 35%.

**Categorise.** This is a **prompt issue**. The tool fetched the right data, the flow is structured correctly, the scope supports velocity-based recommendations. The `VELOCITY_ANALYSIS_PROMPT` says "calculate the team's average velocity" without specifying a weighting scheme — a straight average is a reasonable interpretation, but the wrong one when velocity has shifted recently.

**Fix.** Update the prompt: "Calculate velocity using a weighted average that favours recent sprints. If velocity changed by more than 20% in the most recent two sprints compared to the prior four, flag this as a trend shift and base the capacity recommendation on the recent two sprints only."

**Retest.** The agent now recommended 33 points, flagged the velocity drop, and noted the team composition change as a likely cause. Re-ran the stable-team test case — the weighted average produced the same result as the straight average when velocity was consistent. Both passed.

??? example "Different failure categories, different fix scopes"

    **Prompt fix (smallest scope) — CSM: health report tone too clinical**

    The report read like a data dump. The prompt lacked a tone instruction. Fix: add "Write in a consultative tone suitable for an executive audience — lead with insight, not data." Re-ran affected test cases. No structural changes needed.

    **Flow fix (medium scope) — SE: code review summary skips test coverage**

    The review summary action runs before the test coverage action, so it cannot include coverage data. Fix: reorder the flow so test coverage runs first and feeds into the summary. Update the summary prompt to reference coverage data. Re-run all test cases that touch either action.

    **Scope fix (largest scope) — BA: stakeholder report conflates internal and external risks**

    The scope defined one "risk assessment" step with a single risk list. Internal risks (team capacity, tech debt) and external risks (vendor delays, regulatory changes) need different escalation paths but the memory has one field. Fix: update the scope to separate internal and external risk assessment, update the design to add a field and action, update the build to implement it. Re-run all test cases.

    The fix category determines the blast radius. Prompt fixes touch one file. Flow fixes touch the design and affected actions. Scope fixes cascade through three stages. Verify you have the right category before starting — a misdiagnosed scope issue treated as a prompt fix wastes an iteration cycle.

---

## Evaluation Tooling

Manual evaluation gives you the methodology. Tooling accelerates the feedback loop and makes evaluation repeatable. Most production-grade agent platforms provide a subset of the capabilities below; check your chosen platform's documentation for the specifics.

Tracing
:   Every agent run is captured as a trace — you see exactly what each action received as input, what prompt was sent to the model, what the model returned, and what state updates were produced. The [systematic failure diagnosis](#diagnosing-the-failure-category) process (tool → prompt → flow → scope) becomes tractable when you can inspect every layer in a trace. Look for this capability in any platform you evaluate.

Evaluation Datasets
:   A set of `(input, expected_output)` pairs built from your test cases. Run the agent against the dataset programmatically instead of manually invoking each case. Each run produces a scored result you can compare across iterations. Some platforms provide dataset management and scoring built in; for others you'll build your own small harness.

Automated Scoring (LLM-as-Judge)
:   Define evaluator functions that score agent output using a language model or custom code. Common evaluators: correctness (does the output match expected?), completeness (are all required sections present?), quality (is the writing at professional standard?). Scores are tracked per test case and per iteration.

Experiment Tracking
:   Each iteration cycle produces a new experiment run. Compare scores across runs to verify that a fix actually improved performance and did not regress other cases. This replaces (or supplements) the manual iteration log.

A/B Testing
:   Deploy two versions of the agent with different instructions or tool configurations. Route evaluation inputs between them and compare output quality. Useful for validating whether a candidate improvement actually helps.

Human Evaluation Interface
:   A structured way for team members to rate agent outputs on a rubric. Track scores over time and use them to make go/no-go decisions on graduation.

!!! tip "Tooling is optional for the first few iterations"
    The manual evaluation process described above works without any tooling. But if you plan to iterate beyond 2–3 cycles or evaluate across many test inputs, the time investment in setting up your platform's evaluation features (or a simple bespoke harness) pays off quickly.

!!! tip "For non-technical participants"
    The sections below cover engineering testing — unit tests, regression suites, and CI integration. If you are a CSM, BA, or domain expert participating in evaluation, the methodology above (test case design, iteration process, failure diagnosis) is your primary guide. Skip ahead to [When to Push the Automation Boundary](#when-to-push-the-automation-boundary) for guidance on expanding the agent's scope after graduation.

### Unit Testing Individual Actions

Full end-to-end runs invoke the whole agent with real model calls. That's the right test for end-to-end correctness, but it's slow and expensive — each run costs time and API budget. Most failures originate in a single action: a tool function that mishandles an edge case, a prompt that misclassifies a signal, a routing function that picks the wrong branch. You can catch these failures in seconds with unit tests that never touch a model or external API.

The principle: isolate the action, replace its external dependencies with controlled substitutes, and assert on the output given known input. Three patterns cover the majority of cases. How you express each pattern depends on your framework's testing idioms — the examples below are pseudocode.

**Pattern 1 — Mock tool responses for data-gathering actions.**

A data-gathering action calls an external API or database and writes the result into memory. The logic you are testing is what the action does with the response — parsing, filtering, error handling — not whether the API itself works. Replace the API call with a fixture that returns a known response, then assert on the memory state the action produces.

```
// Happy-path test
test_gather_data_parses_usage_metrics:
    mock_response = {
        metrics: [
            { name: "monthly_active_users", value: 1423 },
            { name: "api_calls", value: 58210 }
        ],
        period: "Q4"
    }
    when usage_api_client.get_metrics is called, return mock_response
    result = gather_data({ account_id: "ACME-001", period: "Q4" })
    assert result.memory.usage_data.monthly_active_users == 1423
    assert result.memory.usage_data.api_calls == 58210

// Empty-result test — action should flag the gap, not crash
test_gather_data_handles_empty_response:
    when usage_api_client.get_metrics is called, return { metrics: [], period: "Q4" }
    result = gather_data({ account_id: "NEW-001", period: "Q4" })
    assert result.memory.usage_data == {}
    assert "missing_usage_data" in result.memory.warnings

// Tool-error test — action should mark the failure and continue
test_gather_data_handles_tool_error:
    when usage_api_client.get_metrics is called, raise network_error
    result = gather_data({ account_id: "ACME-001", period: "Q4" })
    assert result.memory.usage_data.ok == false
    assert result.memory.usage_data.error == "network_error"
```

Test the happy path, the empty-result case, and at least one failure mode. If your scope document's error path register has additional failure modes for this data source, add a test per mode.

**Pattern 2 — Mock model responses for analysis actions.**

An analysis action sends a prompt to the model and processes the response — parsing JSON, extracting scores, classifying risk levels. The logic you are testing is the action's handling of the model output, not the model itself. Replace the model call with a function that returns a deterministic response.

```
// Happy-path test — structured output parses correctly
test_analyse_health_parses_risk_factors:
    fake_model_response = {
        health_score: "Red",
        risk_factors: ["usage_decline", "open_p1"],
        confidence: 0.87
    }
    when call_model_for_json is called, return fake_model_response
    memory = {
        usage_data: { monthly_active_users: 300, trend: "declining" },
        support_data: { open_p1_tickets: 2 }
    }
    result = analyse_health(memory)
    assert result.memory.health_score == "Red"
    assert "usage_decline" in result.memory.risk_factors
    assert result.memory.confidence == 0.87

// Malformed-output test — action should flag the failure, not crash
test_analyse_health_handles_malformed_model_output:
    when call_model_for_json is called, return "not valid json"
    memory = { usage_data: { monthly_active_users: 300 }, support_data: {} }
    result = analyse_health(memory)
    assert result.memory.analysis_error is not null

// Missing-input test — action should flag the gap, not fabricate
test_analyse_health_handles_missing_upstream_data:
    memory = { usage_data: { ok: false, error: "timeout" }, support_data: {} }
    result = analyse_health(memory)
    assert result.memory.health_score == "Not Assessed"
    assert "usage_data unavailable" in result.memory.warnings
```

Three tests per analysis action: happy path, malformed model output, and missing upstream data. If the action has dimension-specific branching (per-dimension thresholds, per-tier scoring rules), add a test per branch to verify the decision logic.

**Pattern 3 — Test routing functions with synthetic state.**

Routing functions take the current memory state and return the name of the next action. They contain pure logic — no API calls, no model calls — so they need no mocking at all. Construct a state that represents each branch condition and assert on the return value.

```
test_routes_to_risk_assessment_when_red:
    state = { health_score: "Red", risk_factors: ["usage_decline"] }
    assert route_after_analysis(state) == "risk_assessment"

test_routes_to_report_when_green:
    state = { health_score: "Green", risk_factors: [] }
    assert route_after_analysis(state) == "generate_report"

test_routes_to_hil_review_when_amber:
    state = { health_score: "Amber", risk_factors: ["open_p1"] }
    assert route_after_analysis(state) == "human_review"

// Edge case: unknown score — the routing function should not default silently
test_routes_raises_on_unknown_score:
    state = { health_score: "Purple" }
    assert route_after_analysis(state) raises ValueError
```

One test per branch, plus at least one edge-case test where the function should explicitly reject unexpected input. Routing functions are the cheapest thing to test — treat 100% branch coverage as the minimum bar here.

These three patterns run in milliseconds, cost nothing, and catch the majority of action-level bugs. Run them on every commit. Save the full end-to-end regression tests (below) for slower CI runs where the cost of model calls is justified.

### Regression Testing in CI

Manual evaluation and experiment tracking tell you where you stand now. Regression tests tell you when something breaks later. Every time you fix a test case during iteration, that fix becomes a regression test — a test case that runs the agent end-to-end, asserts on the memory fields that matter, and fails loudly in CI if a prompt change or tool update causes a regression.

The idea is simple: record the input for a passing test case, define the memory fields you expect at the end, and run the agent programmatically. For agents with HIL checkpoints, supply predetermined feedback so the test runs unattended.

**Step 1 — Define fixtures.** Store each test case as a fixture with the input and the expected values for critical memory fields. You are not asserting on the entire output — just the fields that define correctness.

**Step 2 — Auto-resume past HIL checkpoints.** In production, the agent pauses at HIL checkpoints and waits for human input. In tests, you supply that input programmatically using your framework's pause/resume APIs (every production-grade agent framework provides these). Define a mapping of checkpoint names to the feedback you want to inject — typically an approval or a minor edit that mirrors what a human would do.

**Step 3 — Invoke the agent and assert.** Run the agent with the fixture input. When execution pauses at a HIL checkpoint, resume with the predetermined response. After the agent completes, assert on the memory fields that define whether this test case passes.

**Step 4 — Run in CI.** Add the regression suite to your CI pipeline. These tests are slow (each one invokes the model), so run them on a schedule or on PR merge rather than on every commit. Use a budget-conscious model for CI runs if cost is a concern — the regression suite catches structural failures, not subtle quality differences.

!!! tip "Keep agent construction and runtime compilation separate"
    Design your agent setup so that building the agent (wiring actions and tools) is separate from configuring its runtime (persistence, checkpointing, logging). If they are tangled, tests cannot inject a lightweight in-memory checkpointer and production cannot swap in a durable one. Your test code should be able to construct the agent, bind it to a test runtime, and run it — without duplicating production wiring.

!!! tip "Converting iteration fixes into regression tests"
    Every time you fix a test case in the [iteration process](#iteration-process), add it as a fixture. The input, the expected fields, and the HIL responses are already documented in your evaluation notes — serialising them into a fixture takes minutes. Over time, the regression suite grows to cover every failure mode you have encountered and fixed.

!!! warning "Assert on fields, not on full output text"
    Regression tests should assert on **memory fields** (scores, classifications, presence of required sections, risk flags), not on full output text. Model output varies between runs — asserting on exact text creates flaky tests. If you need to assert on output quality, use a model-as-judge evaluator rather than string matching.

### Using HIL Data as Evaluation Signal

Your human-in-the-loop checkpoints produce evaluation data as a side effect of normal operation:

- **Approvals (no changes)** — the agent got it right. Track the approval rate at each checkpoint over time. A consistently high approval rate is evidence that a checkpoint can be removed.
- **Modifications** (human edits the agent's output) — training signal. Log what was changed and why. These modifications are prompt improvement candidates — each one tells you where the agent's reasoning diverged from the human's.
- **Rejections** (human sends back for rework) — error signal. Each rejection should be added to the iteration backlog with the rework reason. Repeated rejections at the same checkpoint indicate a systemic issue in the preceding action.

This data accumulates from production use, not just test runs. Over time, it provides a richer evaluation signal than any test suite.

## When to Push the Automation Boundary

After 2-3 successful evaluation cycles with consistent results, look for opportunities to expand:

- **If the human rarely changes the output at a HIL checkpoint** -- consider removing that checkpoint and making it fully automated. The human review isn't adding value.

- **If a MANUAL step turns out to be more formulaic than expected** -- consider adding it to the flow as a HIL step. You've learned enough about the decision criteria to let the agent propose.

- **If new data sources become available** -- consider adding actions that incorporate them. More data generally means better analysis.

The boundary should move outward over time as you build trust in the agent's output. But move it incrementally -- one checkpoint at a time, with a full evaluation cycle after each change.

---

## Graduation Criteria

The agent is ready for production use when:

- [ ] All 5+ test cases pass without major human corrections
- [ ] Total time (agent + human review) is less than 50% of the manual process time
- [ ] No critical failures (wrong conclusions, missed major risks) in the last 3 evaluation rounds
- [ ] At least one colleague has reviewed and validated the output quality
- [ ] Error handling has been tested for all identified failure modes

If you can check all five, your agent graduates from prototype to production tool.

### When to Stop Iterating

Not every agent needs to reach full graduation, and not every Partial verdict needs to become a Pass.

**Diminishing returns.** If your last two iteration cycles each improved only one test case by a marginal amount — moving a Partial to a Pass with a minor quality tweak — you are past the point of productive iteration. The time spent on the next cycle is likely better spent using the agent and collecting real-world feedback.

**When Partial is acceptable.** A Partial verdict means the agent produces usable output that requires some human correction. If the agent handles 80% of the work and you spend 10 minutes correcting the rest, that may already be a significant time saving. The question is not "is it perfect" but "is agent-plus-correction meaningfully faster than doing it manually?"

**Stop iterating when:**

- Every remaining Partial has a known, documented root cause and the human correction is fast and predictable
- Total time (agent run + human review and correction) meets the 50% threshold from the graduation criteria
- Further improvements would require disproportionate effort relative to the time they save
- You have been iterating for more than 4–5 cycles without meaningful progress — this usually signals a scope issue that cannot be fixed incrementally

**Do not stop iterating when:**

- Any test case produces a Fail — a Fail means the output is unusable or misleading, which is worse than no automation
- The agent produces correct output but takes longer than doing it manually once you include review time
- You have untested edge cases that represent scenarios the agent will encounter in production

---

## What Happens After Graduation

Passing the graduation criteria means the agent works. It does not mean your team is ready to use it. Most automation initiatives fail at adoption, not at build — the agent sits idle because nobody trusts it, nobody knows what it does, or nobody changed the process to accommodate it. This section covers the transition from "working prototype" to "thing the team actually uses."

### Preparing for Production

Before shadow mode begins, you need organisational clearance. In teams of 50+, the gap between "working prototype" and "production deployment" is filled with approvals, stakeholder conversations, and compliance reviews. Skip them and your pilot stalls — not because the agent doesn't work, but because someone with authority to block it wasn't consulted.

This is not a heavyweight change management exercise. It is a checklist of conversations you need to have and a way to track who has signed off.

#### Stakeholder Map

Identify everyone who needs to approve, be informed, or could block the rollout. Map them to the RACI model your organisation already uses.

| Role | Relationship to the Agent | RACI | What They Need From You |
|---|---|---|---|
| **Workflow team** | Day-to-day operators — they run the agent and review its output | Responsible | Training on the new process, clear HIL expectations, feedback channel |
| **Team lead / manager** | Owns the process the agent is changing | Accountable | Evidence it works (your Evaluation Report), rollback plan, success metrics |
| **InfoSec** | Assesses data flow, API credentials, LLM provider risk | Consulted | Data flow diagram from [Stage 3](03-scope.md), API credential management approach from [Stage 5](05-build.md), LLM provider's security documentation |
| **Legal / Compliance** | Assesses regulatory, contractual, and IP implications | Consulted | What data is sent to which LLM provider, data residency, client contractual obligations, how outputs are reviewed before external use |
| **Procurement / Vendor management** | Manages the commercial relationship with the LLM provider | Consulted | Projected API costs, contract terms, SLA requirements |
| **Leadership / executives** | Sponsor or budget holder for the initiative | Informed | Business case summary — time saved, quality impact, cost to run |
| **Downstream consumers** | People who receive the agent's output (clients, stakeholders, other teams) | Informed | What changed, what didn't, who is accountable (covered in [Communicating the Agent's Role](#communicating-the-agents-role) below) |

Not every row applies to every organisation. A 10-person startup may not have a separate InfoSec function. A regulated financial firm will have all of these and more. Use the map to identify who is missing, not as a rigid template.

!!! tip "Start the compliance conversation early"
    If your [Stage 3 scope document](03-scope.md) flagged data sensitivity constraints, InfoSec and Legal engagement is not optional — it is a prerequisite for any production use. Start these conversations during Stage 5 (Build), not after graduation. Compliance reviews take weeks, not days, and they surface requirements (data residency, audit logging, retention policies) that may require implementation changes.

#### Compliance Engagement Checklist

When you sit down with Legal, InfoSec, or Compliance, they will ask predictable questions. Prepare the answers in advance using artifacts you have already produced.

- [ ] **What data does the agent process?** → Data sensitivity and governance section of your [Workflow Scope Document](03-scope.md)
- [ ] **Where does the data go?** → The LLM provider, any APIs the agent calls, the checkpoint store. Draw a simple data flow: input sources → agent → LLM provider → output destination
- [ ] **Is client data or PII sent to an external LLM?** → Your Stage 3 scope document already flags this. If yes, confirm the LLM provider's data processing terms and whether your client contracts permit it
- [ ] **How are API credentials managed?** → Your [Stage 5 implementation](05-build.md) should store credentials in environment variables or a secrets manager, never in code
- [ ] **Who reviews the output before it reaches clients or stakeholders?** → Your HIL checkpoint design from [Stage 4](04-design.md). Name the reviewer role and the checkpoint locations
- [ ] **What happens if the agent produces incorrect output?** → Your rollback plan (below) and the human review gate
- [ ] **Is there an audit trail?** → Tracing (via your platform's observability features) plus checkpoint history provide full execution traces. Confirm retention period meets compliance requirements
- [ ] **What is the cost model?** → Projected monthly API spend based on expected run frequency and token usage from your evaluation runs

#### Communication Plan

Different audiences need different messages at different times. Do not send a single "we're using AI now" announcement.

| Audience | When | What to Tell Them |
|---|---|---|
| **Workflow team** | Before shadow mode starts | How the process changes, what they are responsible for reviewing, where to report issues, that shadow mode is a trial not a commitment |
| **Team lead / manager** | Before shadow mode starts | Business case, success metrics, rollback criteria, their role as accountable owner |
| **InfoSec / Legal / Compliance** | During Stage 5 (before graduation) | Data flow, provider terms, credential management, audit capability — the compliance checklist above |
| **Leadership** | After shadow mode confirms production readiness | Results from shadow mode, time savings, quality comparison, plan for steady state |
| **Downstream consumers** | At supervised cutover (not before) | What changed, what didn't, who is accountable — covered in detail in [Communicating the Agent's Role](#communicating-the-agents-role) below |

!!! warning
    Do not announce to downstream consumers during shadow mode. Shadow mode is evaluation, not deployment. If the agent underperforms and you roll back, you have created anxiety for nothing.

#### Change Impact Assessment

For each role affected by the agent, document what changes and what stays the same. Derive this directly from the Future-State Summary in your [Stage 3 Workflow Scope Document](03-scope.md) — it already maps each step to AUTOMATE, HIL, or MANUAL.

| Role | What Changes | What Stays the Same | New Responsibility |
|---|---|---|---|
| *Workflow operator* | Data gathering and initial analysis are automated; they no longer do these manually | Final review, judgement calls, stakeholder communication | Reviewing agent output at HIL checkpoints; logging feedback when they make corrections |
| *Team lead* | Receives output faster; may need to adjust scheduling and review cadence | Accountability for output quality; escalation path for issues | Monitoring adoption and success metrics; deciding when to remove checkpoints |
| *Downstream consumer* | Receives the same deliverable, potentially faster and more consistent | Quality bar (maintained by human review); their existing processes and workflows | Nothing — the agent is invisible to them if the review process works |

Adapt the rows to your specific workflow. The point is to make the impact concrete and role-specific rather than abstract. "We're automating the analysis step" is vague. "You will review a draft analysis instead of writing one from scratch, which should take 10 minutes instead of 45" is actionable.

#### Rollback Plan

Define in advance what triggers a rollback and what rolling back looks like. This is not a plan you hope to use — it is the plan that makes stakeholders comfortable approving the pilot.

**Roll back if:**

- Agent output requires major corrections in more than 30% of runs during shadow mode
- A critical failure (wrong conclusion acted upon, data breach, compliance violation) occurs at any point
- The workflow team reports that review time exceeds manual process time for two consecutive weeks

**Rolling back means:**

- Return to the manual process. The agent is paused, not deleted — all code, prompts, and evaluation data are preserved
- Diagnose the failure using the [iteration process](#iteration-process) and the shadow mode data
- Re-enter evaluation with updated test cases that cover the failure mode

Having this written down before you start shadow mode gives your manager, compliance team, and workflow team confidence that the pilot is reversible.

### Pilot Rollout: Shadow, Then Cutover

Do not replace the manual process on day one. Run the agent in shadow mode alongside the existing workflow:

1. **Shadow mode (weeks 1–2).** The agent runs on real inputs and produces real output, but no one acts on it. The human continues doing the work manually. At the end of each cycle, compare the agent's output against the manual output. This is evaluation with production data — and it builds trust with the people who will rely on the output.

2. **Supervised cutover (weeks 3–4).** The agent's output becomes the starting point. The human reviews, edits, and approves before anything goes to stakeholders. This is your HIL process running in production. Track how much the human changes at each checkpoint — this is the same signal described in [Using HIL Data as Evaluation Signal](#using-hil-data-as-evaluation-signal).

3. **Steady state (week 5+).** The human reviews but rarely changes. The agent is the primary producer; the human is the quality gate. Over time, you may remove checkpoints as described in [When to Push the Automation Boundary](#when-to-push-the-automation-boundary).

!!! warning
    Do not skip shadow mode because the agent "already passed all test cases." Test fixtures are controlled inputs. Production data is messy, incomplete, and occasionally surprising. Shadow mode catches the gaps your test suite missed — without consequences.

### Communicating the Agent's Role

The people who receive the agent's output — stakeholders, leadership, clients — need to know what changed and what it means for them. Get ahead of two predictable reactions: "an AI wrote this, so I don't trust it" and "an AI wrote this, so nobody checked it."

**What to communicate:**

- What the agent does and does not do. Be specific: "The agent gathers data from four systems and drafts the initial analysis. A human reviews and approves every output before it reaches you."
- What changed for the recipient. Usually nothing — they get the same deliverable, at the same quality, faster. Say that explicitly.
- Who is accountable. The human reviewer owns the output. The agent is a tool, not a decision-maker. Make this unambiguous.

**What not to do:**

- Don't hide the agent's involvement. If stakeholders discover it later, you lose trust permanently.
- Don't over-explain the technology. Stakeholders care about reliability and accountability, not LLM architecture.

### Feedback Beyond HIL Checkpoints

HIL checkpoint data tells you about the agent's analytical quality. It does not tell you whether the output is useful, timely, or trusted by the people who consume it. Collect feedback from three additional channels:

Recipient feedback
:   Ask the people who receive the agent's output: Is this useful? Is anything missing? Is the format right? A brief monthly survey or a standing agenda item in an existing meeting is enough. You are not looking for statistical significance — you are looking for patterns.

Operator feedback
:   The human reviewer accumulates tacit knowledge about the agent's blind spots. Create a lightweight channel — a shared document, a Slack thread, a recurring 15-minute check-in — where the reviewer can log observations that don't fit neatly into "approve / modify / reject." Examples: "The agent always underweights this data source," "The tone is fine for internal reports but too casual for client-facing ones."

Process-level observation
:   Watch for behavioural signals that don't show up in structured feedback. Is the reviewer rubber-stamping approvals without reading? (Trust may have outpaced the agent's reliability.) Is the reviewer rewriting 80% of every output? (The agent is creating work, not saving it.) Are stakeholders asking the reviewer follow-up questions the agent should have answered? (Completeness gap.)

### Success Metrics: 30 / 60 / 90 Days

Define what success looks like before you deploy — not after. These metrics give you an objective basis for deciding whether to expand, adjust, or roll back.

| Timeframe | What to Measure | Target | What It Tells You |
|---|---|---|---|
| **30 days** | Adoption rate — is the agent actually being used for every eligible workflow run? | 100% of eligible runs go through the agent (shadow or supervised) | If usage is inconsistent, the process hasn't been embedded. Fix the process, not the agent. |
| **30 days** | Modification rate at HIL checkpoints | Trending downward from initial evaluation baseline | The agent is learning from prompt refinements. If flat or increasing, investigate. |
| **60 days** | Time saving — total time (agent + review) vs. manual baseline | Consistent 40–60% reduction | Confirms the efficiency case. If savings are lower than evaluation predicted, production data may be harder than test data. |
| **60 days** | Stakeholder satisfaction | No increase in complaints or follow-up questions vs. manual process | The output quality is holding in production. |
| **90 days** | HIL checkpoint removal candidates | At least one checkpoint identified as removable (>95% approval rate, minimal edits) | The trust boundary is ready to move outward. |
| **90 days** | Scope expansion candidates | At least one adjacent MANUAL step identified as a HIL or AUTOMATE candidate | The agent is generating enough confidence to justify broadening its scope. |

!!! tip
    Measure against the manual baseline you established during evaluation, not against an idealised target. The question is always "is this better than what we were doing before?" — not "is this perfect?"

If the 30-day metrics are not met, pause expansion and diagnose. The most common causes are process issues (the agent isn't integrated into the team's routine), not technical issues (the agent doesn't work). If the 60-day metrics are met, you have a production tool. If the 90-day metrics are met, you have a platform to build on — return to [Stage 2: Select](02-select.md) and pick your next workflow.

### Steady-State Operations

The 90-day metrics tell you the agent works today. They do not tell you whether it will still work in six months. Data sources change, APIs update their response formats, regulatory requirements shift, team members leave, and the business context that shaped the original scope evolves. An agent that passed graduation in Q1 can silently degrade in Q2 without anyone noticing — because the manual process it replaced is no longer being performed, so there is no human baseline to compare against.

Steady-state operations is the discipline of detecting degradation before it causes harm and maintaining agent quality as a continuous practice, not a one-time achievement.

#### Scheduled Re-Evaluation

Set a recurring re-evaluation cadence based on the agent's risk profile:

| Risk Level | Cadence | What Triggers This Classification |
|---|---|---|
| **High risk** | Monthly | Agent output goes to clients or external stakeholders; touches financial data, compliance-sensitive information, or decision inputs where errors have material consequences |
| **Standard** | Quarterly | Agent output is internal-facing; errors are inconvenient but correctable without downstream impact |
| **Low risk** | Every 6 months | Agent handles low-stakes tasks (formatting, summarisation of non-sensitive data) with a human always reviewing before use |

Each re-evaluation is a lightweight version of the original evaluation cycle:

1. **Re-run the graduation test cases** against current production data. If a test case that previously passed now returns Partial or Fail, something has changed.
2. **Review the HIL modification data** accumulated since the last re-evaluation. Rising modification rates are a leading indicator — the agent is degrading before test cases catch it.
3. **Verify data source integrity.** Confirm that every API the agent calls still returns data in the expected format and at the expected completeness. API providers do not always announce breaking changes.
4. **Check for regulatory or policy changes** that affect the agent's domain. If your compliance team has issued new guidance since the last review, assess whether the agent's prompts and scope still comply.
5. **Update the evaluation report** with the re-evaluation results. This is not a new document — append to the existing report so you have a longitudinal view of agent quality.

If a re-evaluation surfaces a failure, route it through the same [iteration process](#iteration-process) and [failure diagnosis](#diagnosing-the-failure-category) you used during the initial evaluation cycle. The fix categories are the same — tool, prompt, flow, or scope — but now you have production data and HIL history to inform the diagnosis.

#### Drift Detection

Between scheduled re-evaluations, monitor for drift signals that warrant an immediate review:

**Output quality drift**
:   The HIL modification rate at any checkpoint rises above 25% over a two-week window, or a rejection occurs for the first time in a previously stable checkpoint. Both signal that the agent's output quality has shifted — usually because an upstream data source changed, not because the agent's code changed.

**Data source drift**
:   An API the agent depends on returns errors, changes its response schema, deprecates a field, or starts returning data at different granularity. If your agent's tools do not validate response schemas, these changes propagate silently into incorrect analysis.

**Regulatory or policy triggers**
:   A compliance update, new client contract clause, or internal policy change affects the data the agent processes or the standards its output must meet. These do not degrade the agent technically — they change the definition of "correct." An agent that was compliant last month may not be this month.

**Volume or pattern shift**
:   The agent starts processing inputs that fall outside the distribution it was evaluated on — new account types, different data volumes, edge cases that were not in the test suite. Watch for inputs that trigger unexpected execution paths or produce outputs the reviewer has not seen before.

**LLM provider model updates**
:   When your LLM provider announces a model version change, deprecation, or behavioural update, treat it as a drift trigger — not a background event. Model updates can shift output tone, change how the model handles ambiguous instructions, alter JSON formatting reliability, or degrade performance on domain-specific tasks. Re-run your graduation test cases against the new model version before adopting it in production. If scores drop, treat the degradation as a prompt issue and iterate before switching. See the [prompt maintenance calendar](#prompt-maintenance-calendar) below for the full process.

!!! tip "Automate what you can"
    If your agent runs on a schedule, add a post-run check that flags anomalies: execution time significantly above baseline, memory fields that are empty when they should not be, or LLM calls that return malformed output. A simple assertion at the end of the flow that validates critical memory fields catches many drift issues before a human sees the output.

#### Operational Runbook

The sections above describe *what* to monitor and *when* to re-evaluate. This runbook consolidates the recurring operational tasks into a single reference — a checklist the agent owner follows on a fixed cadence. Print it, pin it to your project board, or add it to your team's recurring meeting agenda.

##### Monthly Maintenance Checklist

Run through this checklist once per month for high-risk agents, once per quarter for standard agents. Adapt the cadence using the [risk classification above](#scheduled-re-evaluation).

- [ ] **Re-run graduation test cases.** Compare scores to the baseline established at graduation. Flag any test case that moved from Pass to Partial or Fail.
- [ ] **Review HIL modification rates.** Pull the modification and rejection rates from the past period. If the modification rate at any checkpoint exceeds 25%, investigate before the next cycle.
- [ ] **Verify data source integrity.** For each API the agent calls: confirm the endpoint is reachable, the response schema matches what the tool expects, and no fields have been deprecated or renamed. Use the [dependency monitoring checklist](#dependency-monitoring-checklist) below.
- [ ] **Check LLM provider announcements.** Has the provider announced a model update, deprecation, or behavioural change since the last review? If yes, follow the [prompt maintenance calendar](#prompt-maintenance-calendar) below.
- [ ] **Review compliance triggers.** Has your compliance, legal, or security team issued new guidance that affects the agent's domain or data handling? If yes, re-assess the agent's scope against the updated requirements.
- [ ] **Update the evaluation report.** Append results to the existing report. Note any score changes, new failure modes, or environmental changes discovered.

##### Prompt Maintenance Calendar

LLM model updates are the single most common source of silent agent degradation. When your provider announces a model version change:

1. **Before the switch date**, run your full graduation test suite against the new model version in a staging environment. Most providers offer early access to new versions — use it.
2. **Compare scores** against your current baseline. Look for regressions in correctness, completeness, and output formatting. Subtle changes — slightly different JSON key ordering, altered verbosity, changed handling of ambiguous instructions — can break downstream parsing.
3. **If scores hold**, adopt the new version and update your baseline.
4. **If scores drop**, diagnose which prompts are affected. Common fixes: tightening ambiguous instructions that the old model happened to interpret correctly, adding explicit formatting constraints, adjusting few-shot examples. Iterate using the standard [prompt fix process](#iteration-process) before switching.
5. **Pin your model version** in production. Do not use floating version aliases (e.g., `claude-sonnet-latest`) — pin to a specific version so that updates are deliberate, not automatic.

!!! tip
    Add your LLM provider's release announcement page to your team's monitoring. When a new model version is announced, create a calendar event two weeks before the deprecation date with a link to this checklist.

##### Dependency Monitoring Checklist

Review every external dependency the agent relies on. This is not just API endpoints — it includes libraries, data sources, and internal services.

| Dependency Type | What to Check | Frequency | Action if Changed |
|---|---|---|---|
| **External APIs** (CRM, support platform, data warehouse) | Endpoint availability, response schema, deprecated fields, rate limit changes, authentication method changes | Monthly | Update tool wrapper; re-run affected test cases |
| **LLM provider** | Model version, pricing changes, API contract changes, new content policies | When announced | Follow [prompt maintenance calendar](#prompt-maintenance-calendar) |
| **Framework and SDK libraries** | Breaking changes in new releases, deprecated functions, changed default behaviours | Before upgrading | Read changelog; run full test suite against new version before merging |
| **Internal data sources** (databases, internal APIs, shared services) | Schema changes, access permission changes, data freshness guarantees | Monthly | Coordinate with the owning team; update tool wrappers |
| **Credentials and secrets** | API key expiry dates, OAuth token refresh status, certificate renewals | Monthly | Rotate before expiry; verify the agent still authenticates successfully |

##### Failure Escalation Path

When an agent fails in production, the response should be immediate and structured — not ad hoc. Define this escalation path before the first failure occurs and share it with everyone in the [stakeholder map](#stakeholder-map).

| Severity | Definition | Response Time | Who Triages | Who Fixes | Immediate Action |
|---|---|---|---|---|---|
| **Critical** | Agent produces incorrect output that was or could be acted upon; data breach; compliance violation | Within 2 hours | Agent owner | Agent owner + original builder | Disable the agent. Revert to manual process. Notify stakeholders who received affected output. |
| **High** | Agent fails to complete (crashes, timeouts, API errors) on production inputs; all runs affected | Within 1 business day | Agent owner | Agent owner or platform team (if infra-related) | Switch to manual process for affected runs. Diagnose root cause using traces. |
| **Medium** | Agent completes but output quality has degraded (rising HIL modification rates, new Partial verdicts on previously passing test cases) | Within 1 week | Agent owner | Agent owner | Continue supervised operation. Add affected scenarios to the iteration backlog. |
| **Low** | Minor quality issue noticed by reviewer; cosmetic or formatting problems; performance slower than usual | Next scheduled maintenance | Agent steward | Agent owner at next maintenance cycle | Log the issue. No process change required. |

**Post-incident process:**

1. **Document the failure** — what happened, when it was detected, what the impact was, and how it was resolved. Use the same root cause format as the [failure diagnosis technique](#diagnosing-the-failure-category).
2. **Add a regression test** — every production failure becomes a test case. The input that caused the failure, the incorrect output, and the expected output are serialised as a fixture.
3. **Review the escalation response** — was the severity classification correct? Was the response time met? Adjust the escalation path if the response was too slow or the severity was misclassified.

#### Agent Ownership Model

Every agent needs a named owner — not a team, not a channel, a specific person who is accountable for its ongoing quality. Without this, agents degrade through neglect: no one re-evaluates, no one acts on rising modification rates, and no one notices when a data source changes.

**Owner responsibilities:**

- Conduct or delegate scheduled re-evaluations
- Act on drift signals within one business week
- Maintain the agent's entry in the [agent registry](#agent-portfolio-governance) (if you have multiple agents)
- Ensure the agent's compliance sign-off is still current
- Decide when to deprecate or retire the agent

**Surviving staff turnover.** The owner will eventually change roles or leave the organisation. Protect against this:

- **Document the agent's operational context** in a brief operations runbook stored alongside the agent's code: what it does, what data sources it depends on, what the re-evaluation cadence is, what the known limitations are, and where the evaluation history lives. This is not a technical README — it is a handover document for a non-technical successor.
- **Assign a steward** in addition to the owner. The steward is a secondary contact — typically the team lead or a colleague familiar with the workflow — who can assume ownership without a cold start. The steward does not do the re-evaluations, but they know where everything is.
- **Ownership transfer is a re-evaluation trigger.** When the owner changes, the new owner conducts a re-evaluation within their first two weeks. This ensures they understand the agent's current state, not just its documented state.

#### Retirement Criteria

An agent should be retired — not just ignored — when it no longer serves its purpose. Retired means the agent is disabled, its scheduled runs are stopped, and its registry entry is marked as deprecated with a date and reason.

Retire an agent when:

- It has not been used in 60+ days and no one can articulate a reason to keep it
- The manual process it replaced has changed enough that the agent no longer reflects the current workflow
- A newer agent supersedes it and covers the same scope
- A re-evaluation reveals failures that would require a scope-level redesign (Stages 3–5), and the business case no longer justifies the investment
- The data sources it depends on have been decommissioned or restricted

!!! warning
    Do not leave unused agents running. An unmonitored agent that still has API access and scheduled runs is a liability — it consumes budget, may process stale data, and creates a false impression that a workflow is covered when it is not.

### Scaling Beyond the First Agent

The framework up to this point assumes a single team building a single agent. That model works for agents one through three. Beyond that — especially in divisions of 50+ people where multiple teams are building agents independently — you need governance layers that the single-agent pipeline does not provide. The following sections describe when each layer becomes necessary and what it should contain.

#### Agent Portfolio Governance

**When it matters:** You have three or more agents in production, or two or more teams building agents independently.

Without a lightweight review process, you get duplicate agents solving the same problem differently, agents that contradict each other's outputs, and no one with a clear view of what is running. Portfolio governance does not mean a heavyweight approval board — it means someone owns the list.

What to establish:

- **Agent registry.** A single document or system of record listing every agent: what it does, who owns it, what data it accesses, when it was last evaluated, and its current status (shadow / supervised / steady state / deprecated).
- **New agent review.** Before a team begins Stage 3, they check the registry for overlap and get sign-off from the portfolio owner. The review answers two questions: does this duplicate an existing agent, and does it introduce a new data access pattern that requires compliance review?
- **Review cadence.** Quarterly review of the registry. For each agent: Is it still in use? Has it been re-evaluated since the last review? Are its success metrics still being met? Agents that no longer meet their metrics or have no active owner get flagged for deprecation.
- **Retirement criteria.** Apply the [retirement criteria](#retirement-criteria) defined in steady-state operations. Deprecation means disabling the agent and archiving its code — not deleting it.

#### Shared Component Library

**When it matters:** Two or more agents query the same external system (CRM, support platform, data warehouse) using independently written tool wrappers.

Independent tool wrappers for the same API diverge over time. One team updates their wrapper when the API changes; the other does not. One handles pagination; the other silently truncates. Centralising shared tool wrappers eliminates this drift.

What to establish:

- **Identify shared tools.** Audit the tool functions across your agents. Any tool that calls the same external API or database from two or more agents is a centralisation candidate.
- **Extract to a shared package.** Move shared tool wrappers into a common internal package (a Python package in a shared repository or a monorepo module). Each wrapper has a single owner responsible for keeping it aligned with the external API.
- **Versioning.** Pin agent dependencies to specific versions of the shared package. When a wrapper changes, agents adopt the new version on their own release cycle — not all at once. This prevents a tool change in one agent from breaking another.
- **Testing.** Shared tools get their own integration test suite, run independently of any individual agent's tests. If a shared tool breaks, you know before any agent is affected.

#### Platform Team Model

**When it matters:** You have five or more active agents, or agent development has spread across three or more teams.

Below this threshold, each team builds and operates their own agent end-to-end. Above it, teams start duplicating infrastructure work — setting up checkpointing, configuring observability, managing API keys, building deployment pipelines. A platform team absorbs this shared work so that agent teams focus on workflow logic.

The platform team typically owns:

- **Shared infrastructure.** Checkpoint storage, secrets management, LLM provider API key rotation, and observability (tracing, logging, cost dashboards).
- **Agent template.** A starter repository with the deployment pipeline, testing scaffolding, and shared tool package pre-configured. New agents start from the template instead of from scratch.
- **Shared component library.** The tool wrappers described above migrate to the platform team's ownership once the library reaches a certain size.
- **Standards and guardrails.** Data access policies, LLM usage guidelines, evaluation requirements (minimum test cases, graduation criteria), and cost budgets per agent.

!!! tip
    The platform team is not a gatekeeper. Its job is to make building agents faster, not to approve or block them. Portfolio governance (above) handles approval. The platform team handles infrastructure.

#### Cross-Agent Monitoring

**When it matters:** You have three or more agents in steady-state production.

Individual agent monitoring — the success metrics described above — tells you whether each agent is healthy. Cross-agent monitoring tells you whether the fleet is healthy: total cost, aggregate quality, compliance posture, and operational patterns that only emerge across agents.

What to track:

| Dimension | What to Measure | Why |
|---|---|---|
| **Cost** | Total LLM spend across all agents, broken down by agent and by provider | Prevents cost surprises. Identifies agents that are disproportionately expensive relative to the value they deliver. |
| **Quality** | Aggregate HIL modification and rejection rates across agents | Surfaces agents that are degrading without their team noticing. A single agent's 5% rejection rate is fine; if the fleet average is 15%, something systemic is wrong. |
| **Compliance** | Data access patterns — which agents access which sensitive systems, and whether their access is still authorised | Catches scope creep. An agent that started querying one CRM field and now queries twelve may have drifted past its original compliance sign-off. |
| **Operational health** | Failure rates, latency, checkpoint storage growth | Identifies infrastructure issues before they become outages. Checkpoint stores that grow without retention policies are a common problem at scale. |

A lightweight dashboard that aggregates these metrics across your agent registry is sufficient. You do not need a dedicated monitoring platform — a shared spreadsheet updated during the quarterly portfolio review works at smaller scale; a Grafana board or equivalent works at larger scale.

---

??? question "Guiding Questions"
    - Are your test cases covering genuinely different scenarios, or are they variations of the same happy path?
    - When the agent fails, can you trace the failure to a specific action and root cause?
    - Is the human spending more time reviewing the agent's output than they would doing it manually? If so, which action is producing low-quality output?
    - Are your HIL checkpoints adding value, or are they just slowing the process down?
    - Have you tested with real data (not just fixtures)? Fixtures don't surface the messiness of production data.
    - Would you trust this agent's output enough to send it to a stakeholder after a quick review?
    - Have you planned how to communicate the agent's role to the people who receive its output?
    - Do you have a feedback channel beyond HIL checkpoints for the humans who review and consume the agent's output?
    - Does every production agent have a named owner and a documented re-evaluation cadence?
    - If the agent's owner left tomorrow, could someone else take over within a week using existing documentation?
    - When was the last time you verified that every API the agent calls still returns data in the expected format?
    - If this is not your first agent, do you have a registry of active agents and a clear owner for each?
    - Are multiple agents using independently maintained wrappers for the same external API?

---

!!! warning "Common Mistakes"
    **Only testing the happy path.** The agent will look great on clean data with no API failures. That's not where it breaks. Test the edge cases -- sparse data, API errors, ambiguous inputs -- because those are the conditions it will encounter in production.

    **Iterating on prompts without tracking what you changed.** Prompt tuning is empirical. If you tweak a prompt and re-run without recording the change and result, you'll lose track of what works and end up going in circles.

    **Moving too fast to remove HIL checkpoints.** It's tempting to remove human review once the agent seems reliable. Wait for 2-3 clean evaluation cycles first. Early success can be coincidence; sustained success is evidence.

!!! example "See it in practice"
    - [Customer Success Manager — Quarterly Account Health Review](../worked-example/evaluate.md)
    - [Business Analyst — New Feature Request Intake](../worked-example-ba/evaluate.md)
    - [Software Engineer — Release Notes Compilation](../worked-example-se/evaluate.md)

---

## Next Step

You've completed the methodology. From here:

- Review the [Worked Example](../worked-example/index.md) to see how all six stages come together for a concrete use case
- Use the [Templates](../blank-templates/index.md) to apply the framework to your own workflow
- Consult the [Reference](../reference/glossary.md) section for glossary, decision trees, and checklists

[Back to Stages Overview :octicons-arrow-right-24:](index.md)
