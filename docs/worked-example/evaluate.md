# Worked Example: Stage 6 -- Evaluate

!!! example "Worked Example"
    We're applying Stage 6 to: **Quarterly Account Health Review agent**. The goal is to validate that the agent works correctly, handles edge cases, and produces output comparable to the manual process.

## Evaluation Approach

For the account health review agent, evaluation focuses on three questions:

1. **Does the agent retrieve the right data?** Compare the agent's gathered data against what you would manually pull for the same account and period.
2. **Does the agent produce accurate analysis?** Compare the agent's health scores, risk assessments, and trend analyses against your own judgement for accounts where you know the answer.
3. **Is the final report at professional standard?** Have a colleague read the agent-generated report alongside a manually written one (without knowing which is which) and rate both.

## Test Cases

These six test cases cover the range of account profiles a CSM encounters. Each tests different aspects of the agent's behaviour.

| Test Case | Account Profile | What It Tests |
|---|---|---|
| **Happy path** | Healthy account, all data available, no anomalies | The basic flow works end to end. All data sources return clean data. The agent produces a Green health score with no major risks flagged. |
| **At-risk account** | Declining usage, open P1 tickets, upcoming renewal | The agent correctly identifies and escalates risk. Expects an Amber or Red health score, churn risk flagged, and specific evidence cited. |
| **Data gap** | One or more data sources return empty or error | Graceful degradation. The agent should flag the gap explicitly ("no usage data available"), not silently skip it or infer from the absence. |
| **New account** | Limited history, few tickets, early in onboarding | The agent does not over-interpret sparse data. A new account with 2 tickets and 3 weeks of usage data should not get a confident health score -- the agent should note the limited data. |
| **Complex account** | Multiple products, multiple stakeholders, mixed signals | The agent handles nuance. Usage is up on one product but down on another. Sentiment is positive from the champion but negative from end users. The agent should surface the complexity, not flatten it into a single score. |
| **Champion departure** | Previously active primary contact goes silent mid-quarter, CRM contact record not yet updated | The agent distinguishes "signal loss" from "no signal." A previously vocal champion who stops communicating is a high-severity churn indicator — not neutral sentiment due to low message volume. The agent should detect the activity drop-off against the contact's own baseline and escalate it as a risk. |

## What Evaluation Looks Like in Practice

### Round 1: Baseline

Run all six test cases using historical account data from the most recent quarter. For each test case:

1. **Run the agent** with the account's data.
2. **At each HIL checkpoint**, note what the agent surfaced and what you would change. Track the size of your edits (no changes, minor wording tweaks, significant corrections, complete rewrite).
3. **Compare the final report** against the report you manually produced for the same account. Check:
    - Were the same data points surfaced?
    - Did the agent reach the same health score?
    - Were the same risks and opportunities identified?
    - Is the narrative quality comparable?

!!! note "Track the size of your edits at each HIL checkpoint"
    This is the most actionable metric in your evaluation. If you consistently make zero changes at a checkpoint, that checkpoint may be unnecessary -- consider removing it in a future iteration. If you consistently make large changes, the preceding action needs improvement (better prompt, better data, or a different approach).

### Round 2: Edge Cases and Failure Modes

After the baseline round, deliberately test failure scenarios:

- **Kill a data source** (return an error or empty response) and verify the agent handles it gracefully.
- **Feed contradictory data** (high usage but negative sentiment) and check whether the agent surfaces the contradiction rather than resolving it arbitrarily.
- **Test the revision loop** -- at the `hil_review_report` checkpoint, request revisions and verify the agent incorporates your feedback into the next draft.

### Round 3: Efficiency Measurement

Time the full process (agent execution + your review time at each checkpoint) and compare against your manual process time. The target: total time should be less than 50% of the manual process.

#### Manual Process Baseline

Timed across the same 6 accounts used in Round 1, averaged per account:

| Phase | What You Do Manually | Time (avg per account) |
|---|---|---|
| Data gathering | Open CRM, pull usage dashboards, export ticket data, read Slack threads, compile NPS scores | 2–3 hrs |
| Analysis | Compare metrics against benchmarks, identify trends, assess sentiment, cross-reference data sources, form a health judgement | 2–3 hrs |
| Report writing | Write exec summary, populate each section, draft recommended actions, format for stakeholder audience | 1–2 hrs |
| **Total** | | **6–8 hrs** |

#### Agent-Assisted Process (Measured)

Timed across the same 6 accounts, averaged per account:

| Phase | What Happens | Time (avg per account) |
|---|---|---|
| Agent execution | Agent runs end-to-end: `fetch_usage_metrics`, `fetch_tickets`, `fetch_comms`, `fetch_nps` → analysis actions → draft report | ~15 min |
| HIL Checkpoint 1 (`hil_review_analysis`) | Review the agent's health scores, risk flags, and evidence citations. Check whether the analysis matches your judgement. For 4 of 6 accounts, zero changes; for 2, minor score adjustments with rationale notes. | ~20 min |
| HIL Checkpoint 2 (`hil_review_report`) | Read the draft report. Check narrative quality, verify data points cited, adjust exec summary framing. For 5 of 6 accounts, minor wording edits only; for 1 (Globex, pre-fix), significant sentiment section rewrite. | ~15 min |
| **Total** | | **~50 min** |

#### Comparison

| Metric | Manual Process | Agent-Assisted | Improvement |
|---|---|---|---|
| Total time per account | 6–8 hrs | ~50 min | **~85–90% reduction** |
| Data gathering | 2–3 hrs | ~15 min (agent execution) | Largest single saving — the agent eliminates 2+ hours of tab-switching and data compilation |
| Analysis | 2–3 hrs | ~20 min (HIL checkpoint 1 review) | The agent's draft analysis is directionally correct for most accounts; review is faster than creation |
| Report writing | 1–2 hrs | ~15 min (HIL checkpoint 2 review) | Editing an 80%-correct draft is significantly faster than writing from scratch |
| **Time per 10-account portfolio** | **60–80 hrs** | **~8.3 hrs** | **One quarter's reviews completed in a single day instead of two weeks** |

#### Where the Savings Come From

**Data gathering is the biggest win.** The manual process requires opening 4–5 systems (CRM, usage dashboard, ticketing platform, Slack, NPS tool), navigating to each account, exporting or copying data, and compiling it into a working document. This is pure mechanical effort — no judgement required — and the agent eliminates it entirely. The ~15 minutes of agent execution time replaces 2–3 hours of human data retrieval.

**Analysis review is faster than analysis creation.** Validating someone else's health assessment (even an agent's) takes less cognitive effort than forming one from raw data. The CSM reads the agent's scores and evidence, checks them against their own intuition, and either confirms or corrects. For well-understood accounts, this takes 2–3 minutes. For complex accounts, 5–10 minutes.

**Report editing is faster than report writing.** The agent produces a structurally complete report with correct data points already populated. The CSM's edits are primarily about narrative framing — adjusting the exec summary to lead with the most important insight, softening or strengthening language for the specific stakeholder audience. This is a 15-minute polish, not a 1-hour drafting exercise.

#### What's Still Slow

**HIL checkpoints on edge cases take disproportionate time.** The averages above include 4 clean accounts (2–3 min per checkpoint) and 2 accounts requiring significant review. For the Globex account (pre-sentiment-fix), the report review took 25 minutes alone because the sentiment section needed a near-complete rewrite. After the prompt fix (see [Iteration Cycle](#sample-iteration-cycle)), this dropped to ~5 minutes. Edge-case handling improves as the agent iterates, but the first encounter with each failure mode is always expensive.

**The CSM still needs to read every report.** The ~50 minute total assumes the CSM reads and validates every output. This is appropriate for v1 — the agent has not yet earned the trust to skip review. As the agent matures and the CSM builds confidence, the graduation criteria allow for removing HIL checkpoints where edits consistently drop to zero, which would reduce the total further.

!!! note "Efficiency vs accuracy trade-off"
    The 85–90% time reduction applies to the 4 accounts where the agent's output was correct. For the 2 accounts with Partial or Fail verdicts, the CSM spent more time at the review checkpoints catching and correcting errors than they would have spent writing from scratch for those accounts. Total portfolio time still favours the agent (50 min × 6 vs 6–8 hrs × 6), but per-account ROI is strongly correlated with agent accuracy. Fixing the Partial and Fail verdicts through iteration (see below) is what makes the efficiency case sustainable.

## Sample Evaluation Results

After running the six test cases against historical Q4 data for real accounts, here is what the filled-in results look like. Each follows the record format from [Stage 6](../stages/06-evaluate.md#test-case-design).

### Test Case 1: Happy Path — Acme Corp (Healthy Account)

- **Input:** `account_id: ACME-001`, Q4 data. Healthy account: stable usage, no open P1 tickets, Green history.
- **Expected behaviour:** Agent gathers all data cleanly, produces a Green health score, flags no major risks, generates a professional report with minor or no edits at HIL checkpoints.
- **Actual behaviour:** Agent gathered all data, produced a Green health score with correct justification. Report quality was comparable to the manually written version. Zero changes made at `hil_review_analysis`; one minor wording tweak at `hil_review_report`.
- **Verdict:** Pass
- **Notes:** The exec summary was slightly generic ("account remains healthy") — not wrong, but a manually written summary would have led with the 15% usage increase as the headline. Minor quality gap, not a correctness issue.

### Test Case 2: At-Risk Account — Globex Inc (Declining, Renewal in 60 Days)

- **Input:** `account_id: GLOBEX-042`, Q4 data. Usage down 30% QoQ, 3 open P1 tickets, renewal in 60 days, negative Slack sentiment.
- **Expected behaviour:** Agent flags Amber or Red health score, identifies churn risk with specific evidence, surfaces the renewal timeline as a risk amplifier.
- **Actual behaviour:** Agent correctly scored Red, identified churn risk, and cited the usage decline and open P1s. However, the sentiment analysis scored the account as "Needs Attention" when the Slack threads contained clearly frustrated messages from the VP of Engineering — a stakeholder whose sentiment should weigh more heavily than end-user grumbles. The report did not distinguish stakeholder seniority in its sentiment assessment.
- **Verdict:** Partial
- **Notes:** Root cause is in the sentiment analysis prompt. It treats all Slack messages with equal weight — no instruction to consider the seniority or role of the person expressing the sentiment. A frustrated end user and a frustrated VP represent different risk levels, and the prompt does not encode that distinction. The health score happened to land correctly (Red) because the other signals were strong enough, but for a borderline account, this gap would produce the wrong score.

### Test Case 3: Data Gap — Initech Ltd (Slack API Failure)

- **Input:** `account_id: INITECH-007`, Q4 data. Slack API configured to return an error (simulated outage).
- **Expected behaviour:** Agent flags the missing Slack data explicitly, produces analysis from remaining sources, does not hallucinate sentiment data.
- **Actual behaviour:** Agent correctly detected the Slack error, recorded `"score": "Unknown"` for sentiment, and flagged the gap in the report. The synthesis action handled the missing dimension without crashing — health score was based on tickets and usage only, with an explicit caveat.
- **Verdict:** Pass
- **Notes:** The report included the line "Sentiment data was unavailable for this period" in the Sentiment section, which is exactly the right behaviour. No silent omission.

### Test Case 4: New Account — Waystar Ltd (Sparse Data, Early Onboarding)

- **Input:** `account_id: WAYSTAR-310`, Q4 data. Account onboarded 6 weeks ago. 3 support tickets (2 P4 onboarding questions, 1 P3 integration issue — all resolved). 5 weeks of usage data with no prior quarter for trend comparison. Minimal Slack history — one channel with 12 messages, mostly onboarding logistics. No established comms baseline.
- **Expected behaviour:** Agent gathers the available data and produces a health assessment, but clearly flags that the assessment is based on insufficient history to establish trends. A new account with 5 weeks of data and no prior quarter should not receive the same presentation as an account with two years of history. The agent should note what is missing (no trend baseline, no prior quarter comparison, no established sentiment pattern) rather than treating the absence of negative signals as positive evidence.
- **Actual behaviour:** Agent gathered all available data without errors. Usage metrics were within normal ranges for the account's tier (32% DAU/MAU, 44% feature adoption — both above onboarding benchmarks). Tickets were low severity and all resolved. Slack sentiment scored "Positive" based on the 12 available messages. The synthesis action produced an overall Green health score. The report read identically to a mature healthy account: "Waystar Ltd is in good health with strong product adoption and positive stakeholder sentiment. No risks identified." No mention of the 5-week data window, the absence of trend data, or the fact that the sentiment score was derived from 12 messages — most of which were onboarding coordination, not substantive product feedback.
- **Verdict:** Partial
- **Notes:** Root cause: neither the analysis prompts nor the report template distinguish between high-confidence and low-confidence assessments. The `USAGE_ANALYSIS_PROMPT` evaluates metrics against tier benchmarks but does not factor in the length of the observation window — 5 weeks of data that meets benchmarks is treated identically to 2 years of data that meets benchmarks. The `SYNTHESIS_PROMPT` assigns a health score based on the dimension scores it receives, with no instruction to flag when the underlying data is too sparse to establish trends. The report template has no conditional section for low-data accounts. The result is an overconfident Green score that a CSM would know to question — a 6-week-old account has no established baseline, so "healthy" really means "no red flags yet in limited data," which is a meaningfully different statement. In a fintech context, this matters: an overconfident Green on a new account could delay the early-warning escalation that a CSM's judgement would have caught. New client onboarding is exactly when close human attention is most critical, and an unqualified Green score signals that attention is not needed.

### Test Case 5: Complex Account — Nexus Corp (Multi-Product, Mixed Signals)

- **Input:** `account_id: NEXUS-200`, Q4 data. Enterprise tier, two licensed products: Platform API and Analytics Dashboard. Platform API usage is strong (48% DAU/MAU, 72% feature adoption, 18K API calls/month — all above enterprise benchmarks). Analytics Dashboard usage is declining (15% DAU/MAU, 28% feature adoption, down 22% QoQ — well below benchmarks). 2 open P3 tickets on Analytics Dashboard, no P1s. Sentiment is split: the engineering champion (Platform API power user) is positive in Slack; business analysts (Analytics Dashboard users) are frustrated about missing features and slow query performance. Renewal in 120 days.
- **Expected behaviour:** Agent surfaces per-product divergence — Platform API healthy, Analytics Dashboard critical. Report recommends product-specific actions (immediate Analytics Dashboard adoption intervention). Health score Amber, with the justification anchored to the Analytics Dashboard decline rather than a blended average.
- **Actual behaviour:** The agent produced a single usage analysis with score "Needs Attention" and trend "Declining." The details mentioned "mixed adoption signals" but did not identify which product was declining or by how much. Platform API's strong metrics pulled the blended averages up (31.5% DAU/MAU, 50% feature adoption), masking the severity of the Analytics Dashboard's 15% DAU/MAU and 28% adoption. The synthesis action scored Amber (coincidentally correct) but cited "moderate usage concerns" rather than a product-specific risk. The report's Product Engagement section contained one paragraph blending both products together. Recommended actions were generic: "monitor usage trends and schedule a check-in."
- **Verdict:** Fail
- **Notes:** The [Scope Document](scope.md) explicitly states that v1 aggregates usage metrics at the account level as a deliberate simplification (see the multi-product constraint). This test case validates whether that simplification holds — whether blended metrics still produce actionable output for multi-product accounts. The answer here is no: the manually written report for this account had separate sub-sections for each product and flagged Analytics Dashboard as an immediate retention risk requiring a dedicated adoption workshop. The agent's blended report would not trigger that action — a CSM reading it would see "Needs Attention" on usage and move on, missing the critical per-product divergence. This is not a prompt issue — the `USAGE_ANALYSIS_PROMPT` analysed the data it received and produced a reasonable single-score assessment. The problem is structural: the memory schema has one `usage_analysis` field, the `analyse_health` action makes one usage LLM call with all metrics combined, and [Step 7 in the Scope Document](scope.md) describes a single "Assess product engagement" step with no per-product dimension. The agent cannot represent per-product divergence because the schema has nowhere to put it. The aggregation constraint was known from scoping; this test case proves it needs to be revisited earlier than planned.

### Test Case 6: Champion Departure — Helios Systems (Active Contact Goes Silent)

- **Input:** `account_id: HELIOS-118`, Q4 data. Mid-market tier, renewal in 90 days. Usage metrics are stable (29% DAU/MAU, 51% feature adoption — both at or slightly above tier benchmarks). 1 open P3 ticket, nothing alarming. CRM still lists the primary champion (D. Osei, Director of Operations) as the main contact — record has not been updated. However, Slack data tells a different story: D. Osei sent 34 messages in Q3 across #helios-support and #helios-general (feature questions, feedback, coordination with the CS team). In Q4, D. Osei has sent zero messages since week 3. The last message was a routine follow-up on a feature request. No farewell, no handoff, no introduction of a successor. Other Helios users remain active but at lower volume and lower seniority — two end users asking how-to questions.
- **Expected behaviour:** The agent detects that the primary champion's communication pattern has changed dramatically — 34 messages in Q3 to 0 in the final 9 weeks of Q4. Rather than scoring sentiment as "Neutral" or "Positive" based on the remaining end-user messages, the agent should flag the champion's silence as an anomaly, note the contrast against their established baseline, and escalate it as a churn risk factor. The health score should reflect this: an account with stable usage but a silent champion near renewal is Amber at minimum, not Green.
- **Actual behaviour:** The sentiment analysis scored "Neutral" based on the Q4 Slack messages — the remaining end-user messages were transactional and low-signal. D. Osei's absence was not flagged; the analysis treated Q4's lower message volume as unremarkable. The synthesis action received a Neutral sentiment score alongside stable usage metrics and no P1 tickets, producing a Green health score. The report's Stakeholder Sentiment section noted "moderate engagement with no negative signals detected." D. Osei was not mentioned at all — a previously active champion became invisible because they stopped generating data.
- **Verdict:** Fail
- **Notes:** Root cause: the sentiment analysis prompt evaluates the messages it receives but does not compare communication patterns against prior quarters. It has no concept of "expected activity" for a contact — it scores what is in front of it. When a champion stops sending messages, the prompt sees fewer messages (scored as Neutral) rather than a pattern break (which should score as a risk). This is the difference between "no signal" (a new quiet account — TC4's territory) and "signal loss" (a previously active contact going dark). A CSM would recognise this immediately — if Sarah Okonkwo from the Acme account (TC1) suddenly went silent for 9 weeks, that would be the first thing you investigate, regardless of what the usage metrics say. Champion departure (or disengagement) is one of the strongest leading indicators of churn in mid-market and enterprise CS, precisely because it often precedes the usage decline by one or two quarters. The fix requires the sentiment analysis to receive prior-quarter communication baselines per contact and flag significant drop-offs. This is a prompt issue (the LLM can reason about pattern breaks if given the comparison data) combined with a data issue (the `fetch_comms` tool would need to return per-contact message counts for the comparison period, not just the current quarter's messages).

## Sample Iteration Cycle

The Partial verdict on Test Case 2 (Globex) needs to be fixed. Here is one full iteration cycle: diagnose, categorise, fix, retest.

### Diagnose

The sentiment analysis returned "Needs Attention" for an account where the VP of Engineering expressed clear frustration across multiple Slack threads. The manually written report for the same account rated sentiment as "Critical." The gap: the agent treated a frustrated VP and a frustrated junior user as equivalent signals.

### Categorise

This is a **prompt issue**. The `SENTIMENT_ANALYSIS_PROMPT` instructs the LLM to analyse Slack thread sentiment but gives no guidance on weighting by stakeholder role or seniority. The tool retrieved the right data (the Slack threads included the VP's messages), and the flow structure is correct (sentiment feeds into synthesis). The LLM did what the prompt asked — it just was not asked to do the right thing.

### Fix

Add stakeholder weighting instructions to `SENTIMENT_ANALYSIS_PROMPT`. The specific change:

> **Before:** "Analyse the sentiment expressed in the Slack threads below."
>
> **After:** "Analyse the sentiment expressed in the Slack threads below. Weight sentiment by the seniority and role of the person expressing it — frustration from an executive or decision-maker represents a higher risk than the same sentiment from an end user. If you can identify the role of a participant (from their Slack title or how they are addressed), factor that into your severity assessment."

This grounds the LLM in the distinction that matters without requiring a perfect org chart — it uses whatever role signals are available in the thread context.

### Retest

Re-ran Test Case 2 (Globex) with the updated prompt. The sentiment analysis now scored "Critical," citing the VP of Engineering's messages as the primary signal and noting that executive-level frustration near a renewal represents elevated churn risk. The synthesis action picked up the stronger signal and the report's sentiment section now matches the manually written version.

Re-ran Test Cases 1, 3, and 4 to confirm no regression. TC1 and TC3 remained at Pass; TC4 remained at Partial (the stakeholder weighting change is unrelated to the sparse-data presentation issue). The stakeholder weighting instruction had no negative effect on accounts where seniority signals were absent (the LLM correctly fell back to treating all messages equally). TC5 remained at Fail — a structural issue unrelated to this prompt change, addressed in the next iteration cycle.

### Iteration Log Entry

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| 2026-03-15 | Added stakeholder seniority weighting to `SENTIMENT_ANALYSIS_PROMPT` | TC2: Partial → Pass. TC1, TC3: no regression. TC4: Partial (unchanged — sparse-data issue, unrelated). TC5: Fail (unchanged — structural issue). TC6: Fail (unchanged — champion baselining issue, unrelated). | 3 Pass, 1 Partial, 2 Fail |

## Cross-Stage Iteration Cycle

The Fail verdict on Test Case 5 (Nexus Corp) cannot be fixed with a prompt tweak. The [Scope Document](scope.md) acknowledged multi-product aggregation as a deliberate v1 simplification, and this test case was designed to validate whether that simplification holds. It doesn't — blended metrics mask critical per-product divergence. The state schema has no field to hold per-product analysis, so no prompt change can produce the right output. This is the type of structural failure described in the [Stage 6 methodology's cross-stage iteration table](../stages/06-evaluate.md#navigating-cross-stage-iteration) — the symptom appears in Stage 6, but the root cause is in Stage 3. The difference between this and an unanticipated failure is that the scope document told us *where* to look; the test case told us the simplification was not acceptable for this account profile. Here is the full cycle: diagnose, categorise, fix across stages, retest.

### Diagnose

The agent produced a single usage score of "Needs Attention" for an account where one product (Platform API) is healthy and another (Analytics Dashboard) is critical. The blended metrics — 31.5% DAU/MAU, 50% feature adoption — concealed the per-product reality: Platform API at 48% DAU/MAU and 72% adoption vs Analytics Dashboard at 15% and 28%. The report mentioned "mixed adoption signals" without identifying which product was failing or recommending product-specific action. The manually written report had separate product sections and flagged Analytics Dashboard as an immediate retention risk.

### Categorise

Walk through the four failure categories from [Stage 6](../stages/06-evaluate.md):

- **Tool issue?** No. `fetch_usage_metrics` returned data for both products — the raw data was correct and complete.
- **Prompt issue?** No. The `USAGE_ANALYSIS_PROMPT` received the combined usage data and produced a reasonable single-score assessment. The prompt did what it was asked to do.
- **Flow issue?** Partially. The `analyse_health` action makes one usage LLM call and writes one `usage_analysis` dict to state. But the action structure is a consequence of a deeper problem.
- **Scope issue?** Yes. [Step 7 in the Scope Document](scope.md) describes a single "Assess product engagement" step. The decision logic references one set of metrics (DAU/MAU ratio, feature adoption percentage, API call volume) with no per-product dimension. The scope deliberately chose to aggregate at the account level as a v1 simplification (see the multi-product constraint in Constraints and Assumptions), and every downstream artifact inherited that decision. The test case validates that the simplification does not hold for accounts with divergent per-product health.

This is a **scope issue** — the most consequential failure category because it cascades through Stages 3 → 4 → 5. Because the aggregation was a stated constraint rather than an accidental omission, the fix is a planned scope expansion, not a surprise rework.

### Trace to Root Cause

The failure cascaded forward through three stages:

| Stage | Artifact | What assumed single-product |
|---|---|---|
| **Stage 3 (Scope)** | Step 7: "Assess product engagement" | Output is a single "Engagement assessment (healthy/at-risk/critical)." Decision logic evaluates one set of DAU/MAU, feature adoption, and API volume metrics against tier benchmarks. No per-product breakdown. |
| **Stage 4 (Design)** | Memory schema: `usage_data: dict`, `usage_analysis: dict` | Both fields are singular. The `analyse_health` action spec says "Calculate DAU/MAU trends, feature adoption rates" — implicitly one set. |
| **Stage 5 (Build)** | `analyse_health_node` and `USAGE_ANALYSIS_PROMPT` | One LLM call takes `{usage_data_json}` as a single block and returns one `{score, trend, feature_adoption, details}` dict. |

The fix must start at Stage 3 and cascade forward. Fixing only the code (Stage 5) without updating the Scope and Design creates drift between what the artifacts say and what the code does, making future iterations harder to reason about.

### Fix: Multi-Stage Cascade

Following the cross-stage iteration principle: update the affected part of each artifact, then cascade forward through each downstream stage in order.

**Stage 3 (Scope) — Update Step 7**

Step 7's output and decision logic need a per-product dimension. Only the output and decision logic fields change; the step's action, input, and boundary tag (AUTOMATE (quantitative) / HIL (context)) stay the same.

> **Output before:** "Engagement assessment (healthy/at-risk/critical)"
>
> **Output after:** "Per-product engagement assessments + rollup engagement summary (healthy/at-risk/critical per product, with notation of cross-product divergence)"
>
> **Decision logic addition:** "For multi-product accounts, assess each licensed product independently against tier benchmarks before computing a rollup. The rollup must surface per-product divergence — do not average metrics across products, because a healthy product can mask a failing one. Flag any product whose metrics diverge by more than two rating levels from another product on the same account."

**Stage 4 (Design) — Update Memory Schema and Action Spec**

The memory schema needs a field to hold per-product analysis. Add one field; do not restructure the existing schema.

```python
# Add to AccountHealthState
usage_analysis_by_product: dict  # {"Platform API": {score, trend, ...}, "Analytics Dashboard": {score, trend, ...}}
```

The existing `usage_analysis` field stays — it becomes the rollup that references per-product results. Downstream actions (`synthesise`, `generate_report`) that already read `usage_analysis` continue to work unchanged. Actions that need per-product detail (the synthesis prompt, for product-specific risk identification) read the new field.

Update the `analyse_health` action specification: "For multi-product accounts, make one usage LLM call per product using the same prompt template. Store per-product results in `usage_analysis_by_product`. Then compute a rollup `usage_analysis` that summarises per-product divergence instead of averaging the metrics."

**Stage 5 (Build) — Update Action and Prompt**

The usage analysis section of `analyse_health_node` changes from one LLM call to a loop over products:

```python
# --- Usage Analysis (per-product) ---
products = usage_data.get("products", {"default": usage_data})
usage_by_product = {}

for product_name, product_metrics in products.items():
    usage_prompt = USAGE_ANALYSIS_PROMPT.format(
        account_name=state["account_name"],
        product_name=product_name,
        quarter=state["quarter"],
        usage_data_json=json.dumps(product_metrics, indent=2),
        adoption_benchmarks_json=json.dumps(rubric["adoption_benchmarks"], indent=2),
    )
    try:
        usage_by_product[product_name] = call_llm_for_json(usage_prompt)
    except ValueError:
        usage_by_product[product_name] = interrupt({
            "message": f"Usage analysis for {product_name} failed after retries.",
            "raw_data": product_metrics,
        })

# Rollup: summarise per-product results into a single usage_analysis
if len(usage_by_product) == 1:
    # Single-product account — use the result directly, no rollup needed
    usage_analysis = list(usage_by_product.values())[0]
else:
    rollup_prompt = USAGE_ROLLUP_PROMPT.format(
        account_name=state["account_name"],
        per_product_json=json.dumps(usage_by_product, indent=2),
    )
    usage_analysis = call_llm_for_json(rollup_prompt)
```

Three prompt changes support this:

1. `USAGE_ANALYSIS_PROMPT` gains a `{product_name}` placeholder so the LLM knows which product it is analysing.
2. A new `USAGE_ROLLUP_PROMPT` takes the per-product results and produces a rollup that explicitly surfaces divergence between products rather than averaging scores.
3. `SYNTHESIS_PROMPT` adds a `{usage_by_product_json}` placeholder so the synthesis action can cite product-specific evidence in its risk assessment and produce product-specific recommended actions.

!!! note "The single-product path is unchanged"
    When `usage_data` contains no `products` key (single-product accounts like TC1–TC4), the fallback `{"default": usage_data}` produces one iteration of the loop. The per-product dict has one entry, so the rollup is skipped and `usage_analysis` is set directly from the single result. Existing test cases follow exactly the same code path as before.

### Retest

Re-ran Test Case 5 (Nexus Corp) with the updated scope, design, and code. The agent now produces:

- **`usage_analysis_by_product`:** Two entries — Platform API scored "Healthy" (48% DAU/MAU, 72% adoption, stable trend), Analytics Dashboard scored "Critical" (15% DAU/MAU, 28% adoption, 22% QoQ decline).
- **`usage_analysis` (rollup):** Score "Critical" with details noting significant per-product divergence — one product healthy, one critical. The rollup applied the scoring rule from `config/scoring_rubric.yaml`: assign the most severe rating triggered by any single dimension.
- **Synthesis:** The `synthesise` action cited the Analytics Dashboard decline as a high-severity risk, recommended a dedicated adoption intervention with a specific timeline (before the 120-day renewal window), and separately noted Platform API as an expansion opportunity.
- **Report:** The Product Engagement section now has sub-sections per product, matching the structure of the manually written report. Recommended actions are product-specific, not generic.
- **Health score:** Amber, with justification anchored to the Analytics Dashboard decline and the renewal window — not a vague "moderate usage concerns."

At `hil_review_analysis`, the reviewer made zero changes to the per-product usage scores (previously, this checkpoint required significant corrections to add the per-product context manually). At `hil_review_report`, one minor wording tweak.

Re-ran Test Cases 1, 2, 3, 4, and 6 to confirm no regression. TC1, TC2, and TC3 remained at Pass; TC4 remained at Partial (the per-product analysis change is unrelated to the sparse-data presentation issue); TC6 remained at Fail (the champion baselining issue is unrelated to per-product analysis). Single-product accounts took the one-iteration path through the loop and produced output identical to the previous run.

### Iteration Log Entry

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| 2026-03-17 | Per-product usage analysis — updated Scope Step 7 (per-product output and decision logic), Design memory schema (added `usage_analysis_by_product`), Build `analyse_health` action (per-product loop + rollup) and prompts (`USAGE_ANALYSIS_PROMPT`, new `USAGE_ROLLUP_PROMPT`, `SYNTHESIS_PROMPT`) | TC5: Fail → Pass. TC1, TC2, TC3: no regression. TC4: Partial (unchanged — sparse-data issue, unrelated). TC6: Fail (unchanged — champion baselining issue, unrelated). | 4 Pass, 1 Partial, 1 Fail |

!!! note "TC4 and TC6 remain unresolved — and TC4 may be acceptable"
    After two iteration cycles, the scorecard is 4 Pass, 1 Partial, 1 Fail (TC4: overconfident assessment on sparse data; TC6: champion departure not detected). The TC4 fix is a set of prompt refinements — adding observation window awareness to `USAGE_ANALYSIS_PROMPT` and `SYNTHESIS_PROMPT` so the agent distinguishes between "5 weeks of data meets benchmarks" and "2 years of data meets benchmarks," plus a conditional report template section for low-data accounts that presents findings as preliminary rather than conclusive. This is a presentation quality improvement (the underlying data gathering and analysis are correct), not a correctness fix — the agent retrieved the right data and the metrics genuinely met tier benchmarks. A CSM reviewing the output at `hil_review_analysis` or `hil_review_report` would catch the overconfident Green and add a confidence caveat ("assessment based on limited data — 6 weeks, no prior quarter for trend comparison") in under a minute. The question from the [Stage 6 methodology](../stages/06-evaluate.md#when-to-stop-iterating) applies: "is agent-plus-correction meaningfully faster than doing it manually?" For TC4, it is — the agent still saved 5–6 hours of data gathering and analysis across CRM, ticketing, usage, and Slack sources, and the correction is a brief caveat addition at one checkpoint. In a fintech context, this matters for new client onboarding: until the agent gains observation-window awareness, the CSM should treat "flag low-confidence assessments for new accounts" as a standing practice at the review checkpoint — a process mitigation, not a technical blocker. This is a candidate for a third iteration cycle, not a blocker for production use.

    TC6 is a different story. A missed champion departure is not a presentation gap — it is a missed risk. The agent scored a Green on an account where the primary champion went silent 9 weeks before a renewal. A CSM reviewing the report at `hil_review_report` might catch this if they know the account well, but the whole point of the agent is to surface risks that a CSM juggling 30 accounts might miss. The fix requires two changes: (1) the `fetch_comms` tool returns per-contact message counts for both the current and prior quarter, and (2) the `SENTIMENT_ANALYSIS_PROMPT` gains instructions to compare per-contact activity against their own baseline and flag significant drop-offs — especially for contacts tagged as champions in the CRM. Until this fix ships, the CSM should treat "check champion activity continuity" as a standing practice at the `hil_review_analysis` checkpoint. This is scoped as a **v1.1 requirement** with a concrete iteration plan below — not a backlog item.

## v1.1 Iteration Plan: Champion Departure Detection

Champion departure is the single strongest leading indicator of churn in mid-market and enterprise CS, and it is exactly the signal a CSM juggling 30 accounts is most likely to miss manually. An agent that cannot detect it is missing its highest-value detection use case. This is not deferred to a vague backlog — it is the next iteration after the TC5 multi-product fix ships.

### Diagnose

The agent scored Green on Helios Systems — an account where the primary champion (D. Osei) went from 34 Slack messages in Q3 to zero in the final 9 weeks of Q4, with renewal in 90 days. The sentiment analysis scored "Neutral" based on the remaining end-user messages. D. Osei's disappearance was not flagged because the analysis has no concept of per-contact activity baselines — it scores the messages it receives without comparing against expected communication patterns.

The core distinction: TC4 (sparse data on a new account) is "no signal" — the account never established a baseline. TC6 is "signal loss" — the champion had a clear communication pattern and broke it. A CSM would recognise this immediately. The agent cannot.

### Categorise

- **Tool issue?** Yes. `fetch_comms` returns current-quarter Slack messages but not per-contact message counts from prior quarters. The sentiment analysis LLM cannot compare against a baseline it does not have.
- **Prompt issue?** Yes. `SENTIMENT_ANALYSIS_PROMPT` evaluates the messages in front of it but has no instruction to detect activity drop-offs for known contacts.
- **Flow issue?** No. The flow structure is correct — sentiment feeds into synthesis, which feeds into the report. The plumbing works; the data and instructions are incomplete.
- **Scope issue?** Minor. The scope does not distinguish "signal loss" from "no signal" as a risk category. Step 8 (sentiment analysis) needs a decision-logic addition.

This is a **tool + prompt issue** with a supporting scope update — less invasive than the TC5 structural fix, but touching more artefact types.

### Trace to Root Cause

| Stage | Artefact | What is missing |
|---|---|---|
| **Stage 3 (Scope)** | Step 8: "Analyse stakeholder sentiment" | Decision logic evaluates sentiment polarity and volume but has no rule for detecting activity drop-offs against a contact's own baseline. No distinction between "new quiet contact" and "previously active contact who went silent." |
| **Stage 4 (Design)** | `fetch_comms` tool spec | Tool returns current-quarter messages only. No prior-quarter per-contact message counts for baseline comparison. |
| **Stage 5 (Build)** | `fetch_comms` tool + `SENTIMENT_ANALYSIS_PROMPT` | Tool does not query prior-quarter data. Prompt does not instruct the LLM to compare per-contact activity against baselines or flag significant drop-offs. |

### Fix: Scope, Tool, and Prompt Changes

**Stage 3 (Scope) — Update Step 8 Decision Logic**

Add a decision-logic rule to Step 8 ("Analyse stakeholder sentiment"):

> **Decision logic addition:** "For contacts with an established communication baseline (messages in the prior quarter), compare current-quarter message count against their prior-quarter count. Flag any contact whose activity drops by more than 70% as a potential disengagement risk. Weight this signal by the contact's role — a champion or primary contact going silent is a higher-severity indicator than an end user reducing activity. Distinguish between 'signal loss' (previously active contact goes dark) and 'no signal' (new or historically quiet contact with low volume)."

**Stage 4 (Design) — Update `fetch_comms` Tool Spec**

Extend `fetch_comms` to return per-contact message counts for both the current and prior quarter:

```python
# Updated fetch_comms return schema
{
    "current_quarter": {
        "messages": [...],  # existing: full message objects
        "per_contact_counts": {
            "D. Osei": {"messages": 0, "last_message_date": "2025-10-14"},
            "J. Park": {"messages": 8, "last_message_date": "2025-12-18"},
        }
    },
    "prior_quarter": {
        "per_contact_counts": {
            "D. Osei": {"messages": 34, "last_message_date": "2025-09-28"},
            "J. Park": {"messages": 5, "last_message_date": "2025-09-30"},
        }
    }
}
```

The prior-quarter data is counts only — no full message bodies needed. This keeps the payload small and avoids unnecessary LLM token consumption.

**Stage 5 (Build) — Update Tool and Prompt**

Three changes:

1. **`fetch_comms` tool:** Add a query for prior-quarter per-contact message counts from Slack. This is a metadata query (counts grouped by user), not a full message retrieval — the API cost and latency are minimal.

2. **`SENTIMENT_ANALYSIS_PROMPT`:** Add a contact activity comparison section:

    > **Addition:** "You are also provided with per-contact message counts for the current and prior quarter. For each contact who was active in the prior quarter, compare their current activity. If a contact's message count has dropped by more than 70%, flag this as a potential disengagement signal. If the disengaged contact is tagged as a champion or primary contact in the CRM, escalate the severity — a silent champion near a renewal is a high-severity churn indicator, not a neutral signal. Include a `contact_activity_changes` field in your response listing any contacts with significant activity drops, their role, and the magnitude of the change."

3. **`SYNTHESIS_PROMPT`:** Add an instruction to factor contact activity changes into the overall health score:

    > **Addition:** "If the sentiment analysis includes `contact_activity_changes` with champion or primary contact disengagement, this should influence the health score toward Amber or Red regardless of other positive signals. Champion silence near a renewal is a leading indicator that often precedes usage decline by 1–2 quarters."

!!! note "The quiet-account path is unchanged"
    For accounts where no contact had significant prior-quarter activity (like TC4's new account with minimal Slack history), the baseline comparison produces no flags — there is no established pattern to break. The contact activity analysis is additive: it catches signal loss without penalising accounts that never had a signal to lose.

### Expected Retest Outcome

After applying these changes, TC6 (Helios Systems) should produce:

- **Sentiment analysis:** Flags D. Osei's drop from 34 messages to 0, identifies them as the primary champion via CRM data, and escalates the silence as a high-severity churn indicator.
- **Synthesis:** Factors the champion disengagement into the health score, producing Amber despite stable usage metrics. The justification anchors to the champion's silence and the 90-day renewal window.
- **Report:** The Stakeholder Sentiment section names D. Osei's absence explicitly and recommends immediate investigation — has the champion left the company, changed roles, or disengaged?

TC1–TC5 should show no regression. TC1 (Acme Corp, where S. Okonkwo is highly active) should gain a positive signal from champion continuity, reinforcing the Green score.

### Timeline

| Week | Activity |
|---|---|
| 1 | Update Scope Step 8 decision logic. Update `fetch_comms` tool spec in Design. |
| 2 | Implement `fetch_comms` prior-quarter query. Update `SENTIMENT_ANALYSIS_PROMPT` and `SYNTHESIS_PROMPT`. |
| 3 | Run full evaluation suite (TC1–TC6). Fix regressions if any. |
| 4 | Buffer for edge cases (contacts who are legitimately seasonal, contacts who moved channels rather than going silent). |

This is a 3–4 week iteration — scoped tighter than the TC5 multi-product fix because it does not require a schema restructure or new flow actions. The changes are additive: a richer tool return, a longer prompt, and a new field in the sentiment analysis output.

---

## Graduation Criteria

The agent is ready for production use when:

- [x] All 6 test cases pass without major human corrections — 4 Pass after iteration; TC4 Partial requires the CSM to add a confidence caveat for sparse-data accounts at the review checkpoint, not a major rework; TC6 Fail requires champion activity baselining (see [v1.1 iteration plan](#v11-iteration-plan-champion-departure-detection) — scoped at 3–4 weeks)
- [x] Total time (agent + human review) is less than 50% of the manual process time — measured at ~50 min vs 6–8 hrs (~85–90% reduction)
- [ ] No critical failures (wrong health score, missed major risk) in the last 3 evaluation rounds
- [ ] At least one colleague has reviewed and validated the output quality
- [ ] Error handling has been tested for all identified failure modes

!!! tip "When to push the automation boundary"
    After 2-3 successful evaluation cycles: if you rarely change the output at a HIL checkpoint, consider removing it. If a MANUAL step turns out to be more formulaic than expected, consider adding it to the flow as a HIL step. The automation boundary is not fixed -- it should expand as the agent proves itself.

---

## Appendix: Sample Agent-Generated Report

The evaluation results above describe the agent's output in abstract terms — scores, verdicts, edit counts. But the question a reader actually needs answered is: **what does the report look like?** Below is the full agent-generated report for Test Case 1 (Acme Corp, happy path) alongside the manually written report for the same account and quarter. Both are lightly redacted — names and figures are synthetic but structurally representative.

Read both tabs, then re-read the TC1 evaluation notes. The "slightly generic exec summary" comment should become concrete.

=== "Agent-Generated Report"

    **QUARTERLY ACCOUNT HEALTH REVIEW**

    **Account:** Acme Corp · **Tier:** Growth · **Quarter:** Q4 2025 · **CSM:** J. Martinez

    ---

    **Executive Summary**

    Acme Corp remains in good health heading into Q1 2026. Product adoption is strong, support volume is low, and stakeholder sentiment is positive. No significant risks were identified. Recommend maintaining current engagement cadence and exploring expansion opportunities in the Analytics Dashboard module.

    ---

    **Health Score: :green_circle: Green**

    | Dimension | Score | Trend |
    |---|---|---|
    | Product Engagement | Healthy | Stable |
    | Support Health | Healthy | Improving |
    | Stakeholder Sentiment | Positive | Stable |
    | Overall | **Green** | **Stable** |

    ---

    **Product Engagement**

    Acme Corp's usage metrics are above Growth-tier benchmarks across all tracked indicators.

    | Metric | Value | Benchmark | Status |
    |---|---|---|---|
    | DAU/MAU Ratio | 38% | >25% | :white_check_mark: Above |
    | Feature Adoption | 64% | >50% | :white_check_mark: Above |
    | API Call Volume | 12,400/month | >8,000 | :white_check_mark: Above |
    | QoQ Usage Trend | +15% | Stable or growing | :white_check_mark: Growing |

    No product areas showed declining engagement. Feature adoption increased from 58% to 64% QoQ, driven by uptake of the batch processing workflow introduced in the September release.

    ---

    **Support Health**

    | Metric | Value |
    |---|---|
    | Open Tickets | 1 (P4 — feature request) |
    | Tickets Opened in Q4 | 4 |
    | Avg Resolution Time | 1.2 days |
    | P1/P2 Tickets in Q4 | 0 |

    Support volume is low relative to account size. All tickets opened in Q4 were P3 or P4; average resolution time improved from 1.8 days in Q3 to 1.2 days. The single open ticket is a feature request for custom report scheduling, logged as a product enhancement.

    ---

    **Stakeholder Sentiment**

    Sentiment analysis across 47 Slack messages in the #acme-support and #acme-general channels indicates consistently positive engagement.

    - **Primary champion (S. Okonkwo, Head of Data):** Actively engaged, referenced Acme's use of the platform in a positive context during a cross-team Slack discussion. Tone: enthusiastic, collaborative.
    - **End users:** Questions are task-oriented (how-to, configuration), with no frustration signals. Two users thanked the support team for quick resolution of a data export issue.

    No negative sentiment detected. No escalation language or churn indicators present.

    ---

    **Risks and Opportunities**

    | Type | Detail | Severity | Recommended Action |
    |---|---|---|---|
    | Opportunity | 15% QoQ usage growth + high feature adoption | — | Discuss expanded use cases or tier upgrade in Q1 QBR |
    | Opportunity | Champion is vocal advocate internally | — | Explore case study or referral opportunity |
    | Risk | None identified | — | — |

    ---

    **Recommended Actions**

    1. Maintain current engagement cadence (monthly check-in, quarterly QBR).
    2. Present Analytics Dashboard module in Q1 QBR as a potential expansion — usage patterns suggest the data team would benefit.
    3. Follow up on the open feature request (custom report scheduling) to confirm it is tracked in the product roadmap.

=== "Manually Written Report"

    **QUARTERLY ACCOUNT HEALTH REVIEW**

    **Account:** Acme Corp · **Tier:** Growth · **Quarter:** Q4 2025 · **CSM:** J. Martinez

    ---

    **Executive Summary**

    Acme had a strong Q4. The headline: usage grew 15% QoQ, driven almost entirely by the batch processing workflow we shipped in September — Sarah Okonkwo's team adopted it within two weeks of release and it now accounts for roughly a third of their daily API volume. Support load stayed low (zero P1/P2s), and Sarah continues to be one of our most engaged champions — she mentioned us positively in a cross-team thread without any prompting. This is an expansion-ready account: the Q1 QBR is the right venue to introduce the Analytics Dashboard module, and Sarah is the right person to pitch it to. One minor item to track: they have an open feature request for custom report scheduling. Not urgent, but worth confirming it is on the roadmap before the QBR so we are not caught off guard if she asks.

    ---

    **Health Score: :green_circle: Green**

    | Dimension | Score | Trend |
    |---|---|---|
    | Product Engagement | Healthy | Stable → Growing |
    | Support Health | Healthy | Improving |
    | Stakeholder Sentiment | Positive | Stable |
    | Overall | **Green** | **Stable** |

    ---

    **Product Engagement**

    Strong quarter. The numbers:

    | Metric | Value | Benchmark | Status |
    |---|---|---|---|
    | DAU/MAU Ratio | 38% | >25% | :white_check_mark: Above |
    | Feature Adoption | 64% (was 58%) | >50% | :white_check_mark: Above |
    | API Call Volume | 12,400/month | >8,000 | :white_check_mark: Above |
    | QoQ Usage Trend | +15% | Stable or growing | :white_check_mark: Growing |

    The 15% growth is not organic — it is almost entirely attributable to batch processing adoption. Sarah's team went from zero to ~4,100 batch API calls/month in 8 weeks. This is worth noting because it means the growth is concentrated in one feature with one team. If batch processing hits a scaling issue, the growth reverses. Not a risk today, but worth monitoring.

    The remaining usage (non-batch) was flat QoQ, which is fine for a mature Growth-tier account but means the growth story is thinner than the top-line number suggests.

    ---

    **Support Health**

    | Metric | Value |
    |---|---|
    | Open Tickets | 1 (P4 — feature request) |
    | Tickets Opened in Q4 | 4 |
    | Avg Resolution Time | 1.2 days (was 1.8) |
    | P1/P2 Tickets in Q4 | 0 |

    Nothing to flag. Resolution time improved because we resolved the recurring data export issue that generated repeat P3s in Q3 (the fix shipped in the October patch). The open ticket — custom report scheduling — is a genuine product gap. Their workaround (manual exports → internal BI tool) is clunky but functional. If this feature ships, it removes friction; if it does not, it is not a churn risk, but it will come up in the QBR.

    ---

    **Stakeholder Sentiment**

    Sarah Okonkwo remains the primary champion. She is doing our job for us — in a #data-engineering thread last month, she recommended our batch processing to a colleague in the analytics team unprompted. That is the strongest signal we have: organic internal advocacy.

    End users are low-noise. Questions in Slack are transactional (config, how-to). Two users sent thanks after the data export fix — minor, but positive signal that the support experience registers.

    No detractors. No escalation language. No signs of evaluation of competitors.

    ---

    **Risks and Opportunities**

    | Type | Detail | Severity | Recommended Action |
    |---|---|---|---|
    | Opportunity | Usage growth concentrated in batch processing — Sarah's team proved the value | — | Use this as the wedge for Analytics Dashboard pitch in Q1 QBR. Sarah's team is data-heavy; the Dashboard is the natural next step. |
    | Opportunity | Sarah is an organic advocate | — | Ask her about a case study. Timing is good — she is enthusiastic and the batch processing win is fresh. |
    | Watch item | Growth is feature-concentrated (batch processing = ~33% of API volume) | Low | Monitor batch processing reliability. If this feature has stability issues, the growth narrative flips. |
    | Watch item | Open feature request (custom report scheduling) | Low | Confirm roadmap status before Q1 QBR. |

    ---

    **Recommended Actions**

    1. **Q1 QBR prep:** Lead with the batch processing success story. Use it to frame the Analytics Dashboard pitch — "your team proved they can adopt new capabilities quickly; here is the next one."
    2. **Case study ask:** Reach out to Sarah before the QBR. Frame it as "we want to highlight what your team built" rather than a marketing request.
    3. **Feature request follow-up:** Check with Product on custom report scheduling status. Have an answer ready for the QBR.
    4. **Monitor:** Watch batch processing error rates and latency in Q1. Concentrated usage = concentrated risk if the feature has issues at scale.

!!! tip "What to notice"
    The agent and the CSM reached the same health score, surfaced the same data points, and identified the same primary opportunities. The reports diverge in three places:

    1. **Executive summary.** The agent's summary is accurate but generic — "remains in good health" could describe any green account. The manual version leads with the specific story (batch processing adoption, Sarah's advocacy) and uses that to frame actionable next steps. This is the "slightly generic exec summary" noted in the TC1 evaluation.
    2. **Analytical depth.** The agent reports the 15% usage growth as a positive signal. The CSM decomposes it: the growth is concentrated in one feature used by one team, the non-batch usage was flat, and concentrated growth creates concentrated risk. Both are correct — the agent's version is not wrong, it just lacks the second-order reasoning.
    3. **Action specificity.** The agent recommends "discuss expanded use cases in Q1 QBR." The CSM writes a QBR playbook: lead with the batch processing win, use it to frame the Dashboard pitch, prepare for the feature request question. The difference is between a recommendation and a plan.

    These are presentation quality gaps, not correctness failures — which is why TC1 earned a Pass verdict. A CSM reviewing this output at `hil_review_report` would spend 5–10 minutes sharpening the exec summary and adding specificity to the actions, versus 1–2 hours writing the report from scratch. That is the value proposition: the agent handles data gathering and first-draft generation, the human adds contextual judgement and narrative sharpness.

---

[:octicons-arrow-left-24: Back to Stage 6: Evaluate](../stages/06-evaluate.md){ .md-button }
