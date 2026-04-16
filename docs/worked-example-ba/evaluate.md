# Worked Example: Stage 6 -- Evaluate

!!! example "Worked Example"
    We're applying Stage 6 to: **New Feature Request Intake & Impact Assessment agent**. The goal is to validate that the agent retrieves accurate context, produces sound assessments, and generates an impact summary comparable to the manual process.

## Evaluation Approach

For the feature request intake agent, evaluation focuses on three questions:

1. **Does the agent gather the right context?** Compare the agent's retrieved data — backlog duplicates, roadmap items, architecture dependencies, historical estimates, and OKR data — against what you would manually pull for the same request.
2. **Does the agent produce accurate assessments?** Compare the complexity estimate, strategic alignment score, and team impact footprint against your own judgement for requests where you know the answer.
3. **Is the impact summary at professional standard?** Have a colleague read the agent-generated assessment alongside a manually written one (without knowing which is which) and rate both on completeness, clarity, and actionability.

## Test Cases

These five test cases cover the range of feature requests a BA encounters. Each tests different aspects of the agent's behaviour.

| Test Case | Request Profile | What It Tests |
|---|---|---|
| **Happy path** | Standard feature request, all data available, clear alignment, no duplicates | The basic flow works end to end. All data sources return clean data. The agent produces a reasonable complexity estimate, alignment score, and impact summary with minor or no edits. |
| **Cross-team edge case** | Request spanning 3 teams with complex dependency chains | The agent correctly identifies cross-team coordination overhead and reflects it in the complexity estimate. Expects a higher complexity tier than a single-team request with the same component count. |
| **Cold-start data gap** | New Jira project with no estimation history (fewer than 5 completed tickets) | Graceful degradation. The agent should flag the low-confidence estimate explicitly and communicate the uncertainty clearly in the impact summary — not present it identically to a high-confidence estimate. |
| **Fuzzy duplicate detection** | Request that's similar but not identical to an existing backlog item | The agent correctly classifies a related-but-not-duplicate request. The similarity scoring should surface the related ticket at the right threshold without overclaiming it as a duplicate. |
| **Strategic ambiguity** | Request that aligns with one OKR but conflicts with another | The agent surfaces the OKR tension explicitly. The priority recommendation should acknowledge the conflict rather than resolving it into a clean P1--P4 classification. |

## What Evaluation Looks Like in Practice

### Round 1: Baseline

Run all five test cases using historical feature requests from the most recent quarter. For each test case:

1. **Run the agent** with the request's data.
2. **At each HIL checkpoint**, note what the agent surfaced and what you would change. Track the size of your edits (no changes, minor tweaks, significant corrections, complete rework).
3. **Compare the impact summary** against the assessment you manually produced for the same request. Check:
    - Were the same duplicates identified (or correctly dismissed)?
    - Did the agent reach the same complexity tier?
    - Did the agent identify the same alignment score and conflicts?
    - Were the same impacted teams and dependency paths surfaced?
    - Is the narrative quality of the impact summary comparable?

!!! note "Track the size of your edits at each HIL checkpoint"
    This is the most actionable metric in your evaluation. If you consistently make zero changes at `hil_review_assessment`, that checkpoint may be unnecessary — consider removing it in a future iteration. If you consistently make large changes, the preceding actions (`assess_complexity` or `assess_alignment`) need improvement. For this workflow, early iterations typically show more corrections at the assessment checkpoint than the summary checkpoint — because getting the assessments right is harder than writing them up.

### Round 2: Edge Cases and Failure Modes

After the baseline round, deliberately test failure scenarios:

- **Kill a data source** (return an error or empty response for Confluence, the roadmap tool, or the OKR tracker) and verify the agent flags the gap rather than proceeding with incomplete context.
- **Feed a deliberately ambiguous request** (vague description, no component specified) and check whether the agent surfaces the ambiguity at the assessment review checkpoint rather than guessing.
- **Test the revision loop** — at `hil_review_summary`, request revisions and verify the agent incorporates your feedback. Then test the rework loop — send the assessment back to `assess_complexity` with rework instructions and verify the rework instructions are consumed by both the complexity and alignment prompts.

### Round 3: Efficiency Measurement

Time the full process (agent execution + your review time at each checkpoint) and compare against the manual process time. The target: total time should be less than 50% of the manual process.

#### Manual Process Baseline

Timed across 5 historical feature requests from the most recent quarter:

| Phase | What You Do Manually | Time (avg per request) |
|---|---|---|
| Data gathering | Search Jira backlog for duplicates, pull Confluence architecture docs, check roadmap for related initiatives, retrieve OKR data, pull historical estimates | 25--35 min |
| Assessment | Estimate complexity using component history, assess strategic alignment against OKRs, identify impacted teams and dependency chains | 20--30 min |
| Impact summary drafting | Write the structured impact assessment: complexity rationale, alignment justification, team impact footprint, risk flags, priority recommendation | 15--25 min |
| **Total** | | **60--90 min** |

#### Agent-Assisted Process (Measured)

Timed across the same 5 historical requests:

| Phase | What Happens | Time (avg per request) |
|---|---|---|
| Agent execution | Agent runs end-to-end: `search_backlog`, `fetch_architecture`, `fetch_roadmap`, `fetch_okrs`, `fetch_estimates` → `assess_complexity` → `assess_alignment` → `generate_impact_summary` | ~3 min |
| HIL Checkpoint 1 (`hil_review_assessment`) | Review the agent's complexity tier, alignment score, and team impact identification. For 3 of 5 requests, zero changes; for 2, minor alignment score adjustments where the agent rated Indirect and the BA judged Direct based on OKR interpretation. | ~8 min |
| HIL Checkpoint 2 (`hil_review_summary`) | Read the impact summary, verify data points cited, adjust narrative framing. For 4 of 5 requests, minor wording edits; for 1 (the cold-start request), added a stronger low-confidence caveat to the complexity section. | ~5 min |
| **Total** | | **~16 min** |

#### Comparison

| Metric | Manual Process | Agent-Assisted | Improvement |
|---|---|---|---|
| Total time per request | 60--90 min | ~16 min | **~78--82% reduction** |
| Data gathering | 25--35 min | ~3 min (agent execution) | Largest single saving — the agent eliminates 25+ minutes of cross-system data retrieval |
| Assessment | 20--30 min | ~8 min (HIL checkpoint 1 review) | The agent's draft assessment is directionally correct for most requests; reviewing is faster than creating from scratch |
| Impact summary drafting | 15--25 min | ~5 min (HIL checkpoint 2 review) | Editing a well-structured draft is significantly faster than writing from a blank page |

## Sample Evaluation Results

After running the five test cases against historical feature requests from the most recent quarter, here is what the filled-in results look like. Each follows the record format from [Stage 6](../stages/06-evaluate.md#test-case-design).

### Test Case 1: Happy Path — "Payments API Rate Limiting" (Standard Request)

- **Input:** `request_id: PROJ-1847`, submitted by an engineering lead via Jira. Request: add rate limiting to the Payments API to prevent abuse. Single component (Payments Service), well-documented in the service catalogue with clear ownership. 12 completed tickets for this component in the last 4 sprints. Aligns with "Improve Platform Reliability" OKR (active, Q1).
- **Expected behaviour:** Agent gathers all data cleanly. Complexity estimated as Medium (single component, median baseline ~8 SP, no schema change, no external dependency). Alignment scored High (Direct to the reliability OKR). One team directly impacted (Payments team), one indirectly (API Gateway team for routing changes). Impact summary matches the structure and quality of a manual assessment. Priority: P2 (High alignment, no urgency flag).
- **Actual behaviour:** Agent gathered all data without errors. Complexity estimated Medium with correct justification: 1 component, 8 SP median baseline, no schema change, no external dependency. Alignment scored High with a Direct mapping to "Improve Platform Reliability — KR3: Reduce unplanned downtime to < 2 hrs/quarter." Correctly identified the Payments team as directly impacted and the API Gateway team as indirectly impacted via the ingress routing dependency. Impact summary was well-structured with all seven template sections populated. Priority: P2, correctly justified. Zero changes at `hil_review_assessment`. One minor wording tweak at `hil_review_summary` — the Risks section listed "rate limiting configuration may require tuning post-deployment" which is generic; the manually written assessment instead flagged the specific risk of throttling legitimate high-volume API consumers.
- **Verdict:** Pass
- **Notes:** The Risks section defaulted to a generic operational risk rather than identifying the domain-specific risk (impact on legitimate high-volume API consumers). This is a quality gap between "technically accurate" and "adds the insight a human would." Worth noting as a prompt refinement candidate for a future iteration, not a blocker.

### Test Case 2: Cross-Team Edge Case — "Unified Customer Data Layer" (3 Teams, Complex Dependencies)

- **Input:** `request_id: PROJ-2103`, submitted by a product manager via Slack. Request: build a unified customer data layer so all services read from a single customer profile instead of maintaining separate copies. Affects 3 components: Customer Service (Profile team), Analytics Pipeline (Data Engineering team), and Billing Service (Billing team). Each component has 8+ completed tickets in the last 4 sprints. Architecture context shows a shared PostgreSQL database between Customer Service and Billing Service, and an event bus dependency between Customer Service and Analytics Pipeline. Roadmap context shows a related initiative ("Customer 360 view") planned for Q2. OKR alignment: Indirect to "Reduce Data Inconsistency Across Services" (Q1).
- **Expected behaviour:** Complexity estimated as Large or X-Large — 3 components maps to Medium by the component count rule, but cross-team coordination overhead (3 teams, shared database, event bus dependency) should push it higher. Alignment scored Medium (Indirect to 1 OKR). Roadmap overlap flagged as related to the Q2 Customer 360 initiative. 3 teams directly impacted, 2+ indirectly impacted. Priority: P3 or P2 (Medium alignment, higher complexity should increase urgency framing).
- **Actual behaviour:** Agent gathered all data correctly. Duplicate search found no strong matches but flagged the Q2 "Customer 360 view" roadmap item as potentially overlapping (correctly surfaced via roadmap context, not duplicate detection). Complexity estimated **Medium** — the prompt applied the four-factor tier mapping correctly: 3 components = Medium (by the "2--3 = Medium" rule), median historical baseline = 8 SP (Medium range), no schema change explicitly required, no external integration dependency. The estimate did not account for cross-team coordination overhead. The team impact identification (same action) correctly identified 3 directly impacted teams and 2 indirectly impacted teams, flagged the shared database as a coordination complexity factor, and noted the event bus dependency — but this information was not fed back into the complexity assessment.
- **Verdict:** Partial
- **Notes:** Root cause: the `COMPLEXITY_ESTIMATION_PROMPT` evaluates technical factors (component count, historical baseline, schema change, external dependency) but has no instruction to factor in organisational complexity from the team impact data. The four-factor tier mapping from [Step 6 in the Scope Document](scope.md) is faithfully implemented — the problem is that the scope's complexity model captures structural complexity but not coordination complexity. A 3-component change within one team is fundamentally different from a 3-component change across 3 teams with a shared database. The former is a Medium; the latter requires API contract negotiations, coordinated deployment sequencing, shared test environment setup, and cross-team sprint alignment. The prompt was asked to assess complexity using the four factors, and it did — it just was not asked to account for the factor that matters most for this request.

    The alignment score (Medium, Indirect to 1 OKR) and roadmap overlap ("related — Q2 Customer 360 initiative addresses a superset of this request") were both correct. The priority recommendation (P3) was wrong as a downstream consequence of the wrong complexity tier — Medium complexity produced a less urgent framing in the Risks section, which contributed to P3 rather than the P2 the manually written assessment recommended.

### Test Case 3: Cold-Start Data Gap — "Mobile Push Notification Preferences" (New Jira Project)

- **Input:** `request_id: MOB-0018`, submitted by a product manager via Jira. Request: allow users to configure push notification preferences in the mobile app. The "Mobile App" Jira project was created 3 weeks ago as part of a new mobile initiative. Only 2 completed tickets exist in the project (both setup tasks, 1 SP and 2 SP). No architecture docs in Confluence for the mobile component yet — the service catalogue has a stub entry with ownership (Mobile team) but no dependency map. OKR data and roadmap context are available and clean.
- **Expected behaviour:** Agent gathers what data exists, flags the gaps explicitly. Complexity estimation triggers the low-confidence fallback (fewer than 5 historical tickets) and uses component count alone. The impact summary should clearly communicate that the estimate is low-confidence and explain why, so the prioritisation committee knows to weight it accordingly.
- **Actual behaviour:** Agent gathered available data. Jira backlog search returned no duplicates (correct — new project, sparse backlog). Confluence returned the stub architecture entry with ownership but no dependencies. Historical estimate query returned 2 tickets (below the 5-ticket threshold). The `assess_complexity` action correctly triggered the low-confidence fallback: complexity tier set to Small (1 component, component-count-only), `confidence: "low"`, with a note: "Fewer than 5 completed tickets for component 'Mobile App'; estimate based on component count alone." Alignment scored Medium (Indirect to "Expand Mobile Presence" OKR). Team impact identified the Mobile team as directly impacted, with a flag that the dependency map is unavailable — "impact footprint may be incomplete."

    However, the impact summary presented the low-confidence complexity estimate identically to a high-confidence one. The Complexity section read: "Estimated complexity: Small (1 component, no schema change, no external dependency)." The `confidence: "low"` flag was mentioned one sentence later as "Note: estimate is low-confidence due to limited historical data." A BA reading this alongside ten other assessments — most with high-confidence estimates — would easily miss the qualification. The manually written assessment for the same request led the Complexity section with a bold caveat: "**Estimate reliability: Low** — this project has insufficient history for data-driven estimation. The Small classification is a structural lower bound, not a calibrated estimate."
- **Verdict:** Partial
- **Notes:** Root cause: the `IMPACT_SUMMARY_PROMPT` has one template for the Complexity section regardless of confidence level. It renders `complexity_estimate.tier` as the headline and `complexity_estimate.confidence` as a subordinate note. The prompt does not instruct the LLM to change the presentation format based on confidence level. The data was correct (the agent flagged low confidence), the assessment was correct (the action applied the fallback rule), and the graph structure is fine — but the *communication* of uncertainty in the final document was inadequate. The prioritisation committee does not read the raw assessment state; they read the impact summary. If the summary does not make the uncertainty unmissable, the committee will treat it as a normal estimate.

### Test Case 4: Fuzzy Duplicate Detection — "Dashboard Export to PDF" (Similar but Not Identical)

- **Input:** `request_id: PROJ-2201`, submitted by a customer success manager via email. Request: add the ability to export dashboard views as PDF files for sharing with external stakeholders. Existing backlog contains PROJ-0892 ("Report generation and export functionality" — building exportable reports from the analytics module, estimated Large, currently in the Q2 roadmap) and PROJ-1623 ("CSV export from analytics tables" — completed last sprint).
- **Expected behaviour:** Agent finds PROJ-0892 as "possibly related" (overlapping export concept but different scope — dashboards vs. reports) and PROJ-1623 as a weaker match (same feature area but different output format and source data). Neither flagged as a "likely duplicate." The BA sees both at `hil_review_assessment` with enough context to make the judgement call.
- **Actual behaviour:** Agent found PROJ-0892 with a similarity score of 0.74 ("possibly related — review recommended") and PROJ-1623 with 0.67 ("possibly related — review recommended"). Both were surfaced at `hil_review_assessment` with their ticket summaries and similarity scores. The BA confirmed PROJ-0892 as genuinely related (the dashboard export could potentially be scoped as part of the broader report export initiative) and dismissed PROJ-1623 (CSV export is a different feature). The impact summary's Duplicate Analysis section correctly presented both findings with the BA's annotations from the review checkpoint.
- **Verdict:** Pass
- **Notes:** The similarity scoring behaved well on a genuinely ambiguous case. PROJ-0892 at 0.74 is correctly in the "possibly related" band — it is related but not a duplicate, and the threshold did not overclaim. PROJ-1623 at 0.67 is right at the lower edge of the band — a reasonable match to surface given the shared "export" concept, even though the BA dismissed it. The `hil_review_assessment` checkpoint is where this ambiguity gets resolved — the agent surfaces candidates and confidence levels, the human makes the judgement call. This is the pattern working as designed.

!!! note "Why TC4 validates the duplicate detection *design*, not just the scoring"
    The interesting result here is not that the similarity scores were in the right range — it is that the workflow handled the ambiguity correctly at a system level. The `gather_context` action surfaced both candidates. The `hil_review_assessment` checkpoint presented them alongside the full assessment context (complexity, alignment, team impact), so the BA could evaluate whether the "possibly related" ticket PROJ-0892 should change the scope of this request. The BA's annotation from the review ("could be scoped as part of the broader report export initiative") flowed forward via `assessment_human_feedback` into the impact summary. This is the HIL feedback-as-context pattern from the [Design document](design.md) — the human's judgement enriches the downstream output rather than being siloed at the checkpoint.

### Test Case 5: Strategic Ambiguity — "Self-Service Analytics Portal" (Conflicting OKRs)

- **Input:** `request_id: PROJ-2250`, submitted by the VP of Product via Jira. Request: build a self-service analytics portal for enterprise clients so they can run custom queries and build dashboards without BA involvement. Active OKRs include "Expand Enterprise Self-Service Capabilities — KR2: Launch 3 self-service tools by end of Q1" (Direct alignment) and "Reduce Infrastructure Costs by 15% — KR1: Decrease compute spend by 10% by end of Q1" (Conflicting — an analytics portal with custom queries would significantly increase compute costs). No duplicates. Complexity is Medium (2 components: Analytics Pipeline and Frontend Portal). 2 teams directly impacted.
- **Expected behaviour:** Alignment scored "Conflicting" with explicit OKR mappings: Direct to the Self-Service OKR, Conflicting with the Infrastructure Cost OKR. The impact summary should surface the tension in the Strategic Alignment section. The priority recommendation should acknowledge the conflict rather than resolving it into a clean P1--P4 classification — this is a business decision the agent should not make.
- **Actual behaviour:** The `assess_alignment` action worked correctly. Alignment scored "Conflicting" with the proper OKR mappings: Direct to "Expand Enterprise Self-Service Capabilities" (request would deliver one of the three required self-service tools), Conflicting with "Reduce Infrastructure Costs by 15%" (custom query execution on enterprise datasets would increase compute costs, directly opposing KR1). The `conflicts` list was properly populated: `[{"okr": "Reduce Infrastructure Costs by 15%", "competing_initiative": "Self-service analytics portal compute requirements", "tension": "Custom query execution on large enterprise datasets will increase compute spend, directly opposing KR1"}]`.

    However, the `generate_impact_summary` action's priority recommendation was **P2** — "High strategic alignment with Expand Enterprise Self-Service Capabilities." The priority formula (High alignment without urgency = P2) was applied using the Direct mapping to one OKR while effectively ignoring the Conflicting mapping to the other. The Strategic Alignment section of the impact summary correctly rendered the conflict (pulled from `alignment_score.conflicts`), but the Recommended Priority section one page later presented a clean P2 as if the conflict did not exist. A BA reading the priority recommendation without reading the full alignment section would not know that the request has a strategic tension requiring committee deliberation.
- **Verdict:** Partial
- **Notes:** Root cause: the priority formula in the `IMPACT_SUMMARY_PROMPT` (derived from [Step 9's decision logic](scope.md)) maps alignment scores to P1--P4 using High/Medium/Low as inputs. "Conflicting" is not one of the defined alignment levels for priority mapping — the formula has no branch for it. When the LLM received an alignment score of "Conflicting," it fell through the priority rules and defaulted to using the highest individual OKR classification (Direct -> High -> P2). The alignment assessment was correct; the priority recommendation layer did not know what to do with the information the alignment layer produced.

!!! note "Why this is a prompt issue in `IMPACT_SUMMARY_PROMPT`, not a scope or design issue"
    The `assess_alignment` action faithfully implemented [Step 7's](scope.md) instruction to "surface the tension explicitly rather than averaging" — the alignment assessment is correct. The `alignment_score` state field stores conflicts separately (as designed in the [state schema](design.md)). The graph structure routes the correct data to the right action. The gap is that Step 9's priority formula has four cases (High -> P1/P2, Medium -> P2/P3, Low -> P4) but no case for "Conflicting." The `IMPACT_SUMMARY_PROMPT` implemented the formula as written — it just was not given instructions for a case the formula does not cover. The scope defined the right data model for conflicts (Step 7) but did not follow through with a corresponding decision rule in the priority logic (Step 9). This is fixable at the prompt layer by adding a "Conflicting" branch, without changing the scope or design — the data and structure already support it.

## Sample Iteration Cycle

The Partial verdict on Test Case 2 (Unified Customer Data Layer) needs to be fixed. Here is one full iteration cycle: diagnose, categorise, fix, retest.

### Diagnose

The complexity estimation returned Medium for a request that spans 3 teams, involves a shared database, and requires event bus contract changes. The manually written assessment for the same request estimated Large, citing cross-team coordination as the primary driver. The gap: the agent assessed structural complexity (components, historical baseline, schema, integrations) but not organisational complexity (teams, coordination protocols, deployment dependencies).

### Categorise

Walk through the four failure categories from [Stage 6](../stages/06-evaluate.md#diagnosing-the-failure-category):

1. **Tool layer — Was the right data retrieved?** Yes. `gather_context` returned the full architecture context including service ownership, dependency maps, and the shared database. The `assess_complexity` action's team impact prompt correctly identified 3 directly impacted teams and flagged the shared database. All data was present. ✓
2. **Prompt layer — Given the data it received, did the prompt produce the right analysis?** The complexity prompt received `architecture_context` (which includes component count and dependency data) and `historical_estimates`. It correctly applied the four-factor tier mapping and produced Medium. But the prompt's instructions do not include cross-team coordination as a complexity factor — even though the data to assess it (team count from `architecture_context.service_ownership`) was available in its input context. The prompt did what it was asked; it was not asked to factor in team coordination overhead. ✗
3. Layers 3--4 not reached — failure identified at layer 2.

This is a **prompt issue**. The data was available but the prompt did not use it.

!!! note "Why this is a prompt issue and not a scope issue"
    The scope's [Step 6](scope.md) defines a four-factor complexity model. You might argue that the missing fifth factor (cross-team coordination) makes this a scope issue — the scope's decision logic is incomplete. But the scope's Step 8 already captures team impact identification as a separate step, and the [Design document's](design.md) `assess_complexity` action combines Steps 6 and 8 into a single action with access to both data sets. The information needed to assess coordination overhead is already gathered and available within the action — `architecture_context.service_ownership` tells the complexity prompt how many teams own the affected components. The gap is that the complexity *prompt* does not reference the team ownership data for complexity assessment; it uses it only for the separate team impact output. This is fixable at the prompt layer without changing the scope, the design, or the graph structure. If the team impact data were not available to the action at all (e.g., gathered in a different action that runs later), *that* would be a graph or scope issue. But the data is right there — the prompt just does not use it.

### Fix

Add a fifth factor to the `COMPLEXITY_ESTIMATION_PROMPT` that accounts for cross-team coordination overhead. The specific change:

> **Before:** "Assess the request's complexity using four factors: (1) number of affected components, (2) historical story point baseline for those components, (3) whether a schema or data model change is required, (4) whether the request involves an external integration dependency. Apply the tier mapping and cap at X-Large."
>
> **After:** "Assess the request's complexity using five factors: (1) number of affected components, (2) historical story point baseline for those components, (3) whether a schema or data model change is required, (4) whether the request involves an external integration dependency, (5) cross-team coordination overhead — if the affected components are owned by 3 or more different teams (identifiable from the service ownership data in the architecture context), add one complexity tier. Cross-team work at this scale involves API contract negotiations, coordinated deployment sequencing, shared test environment setup, and cross-team sprint alignment — these are real effort costs not captured by component count alone. For 5+ teams, add two tiers. Apply the tier mapping and cap at X-Large."

This grounds the LLM in the distinction that matters — team count as an input to complexity, not just as a separate output — using data already present in the prompt's input context.

### Retest

Re-ran Test Case 2 (Unified Customer Data Layer) with the updated prompt. The complexity estimation now scored **Large**: Medium base (3 components) + one tier for cross-team coordination overhead (3 directly impacted teams: Profile, Data Engineering, Billing). The adjustment factors now include "cross-team coordination: 3 teams with shared database dependency." The reasoning cited API contract negotiations between the three teams and coordinated deployment requirements as the primary overhead drivers. The impact summary's Complexity section reflected the updated tier, and the priority recommendation shifted from P3 to P2 — the higher complexity tier contributed to a more urgent framing in the Risks section, which is consistent with the manually written assessment.

Re-ran Test Cases 1, 3, 4, and 5 to confirm no regression. TC1 (1 team, Payments) was unaffected — the coordination overhead factor found 1 team and added no adjustment; tier remained Medium. TC3 (1 team, Mobile) was similarly unaffected. TC4 (1 team) was unaffected. TC5 (2 teams) was unaffected — below the 3-team threshold, no adjustment applied. TC5's verdict remains Partial for the priority recommendation issue (unrelated to this change).

### Iteration Log Entry

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| 2026-03-22 | Added cross-team coordination overhead as fifth factor in `COMPLEXITY_ESTIMATION_PROMPT` (≥3 teams = +1 tier) | TC2: Partial → Pass. TC1, TC3, TC4: no regression. TC5: Partial (unchanged — priority formula issue). | 3 Pass, 2 Partial |

## Iteration Cycle: Strategic Ambiguity Fix

The Partial verdict on Test Case 5 (Self-Service Analytics Portal) is a separate prompt issue from TC2. Here is the second iteration cycle.

### Diagnose

The priority recommendation was P2, citing only the Direct alignment to one OKR while ignoring the Conflicting relationship with another. The alignment assessment itself was correct — the `conflicts` list was properly populated and the Strategic Alignment section of the impact summary rendered the tension clearly. But the Recommended Priority section one page later assigned a clean P2 as if the conflict did not exist.

### Categorise

1. **Tool layer** — data correct. ✓
2. **Prompt layer** — the priority formula in `IMPACT_SUMMARY_PROMPT` maps High/Medium/Low alignment to P1--P4 but has no rule for "Conflicting." The LLM defaulted to using the highest individual OKR classification. ✗

This is a **prompt issue** in the priority recommendation section of `IMPACT_SUMMARY_PROMPT`.

### Fix

Add a "Conflicting" branch to the priority formula instructions in `IMPACT_SUMMARY_PROMPT`:

> **Addition:** "If the alignment score is 'Conflicting,' do not assign a P1--P4 priority. Instead, set the recommended priority to 'Committee Deliberation Required' and explain the specific OKR tension. The priority decision for requests with conflicting strategic alignment is a business judgement that the prioritisation committee must make with full context — the agent should present the trade-off clearly, not resolve it."

This follows the same principle as [Step 7's](scope.md) "surface the tension explicitly rather than averaging" — extended from the alignment *assessment* to the priority *recommendation*. The agent's job is to make the conflict visible and actionable, not to choose a side.

### Retest

Re-ran Test Case 5. The priority recommendation now reads: "**Priority: Committee Deliberation Required.** This request directly advances KR2 of 'Expand Enterprise Self-Service Capabilities' but conflicts with KR1 of 'Reduce Infrastructure Costs by 15%' — custom query execution on enterprise datasets would increase compute spend. The prioritisation committee should weigh the strategic value of enterprise self-service against the cost reduction target." The Recommended Priority section now matches the Strategic Alignment section in acknowledging the tension rather than resolving it.

Re-ran Test Cases 1, 2, 3, and 4 to confirm no regression. All four were unaffected — the "Conflicting" branch only triggers when `alignment_score.score == "Conflicting"`, which none of these test cases produce.

### Iteration Log Entry

| Date | Change Made | Test Cases Affected | Result |
|---|---|---|---|
| 2026-03-23 | Added "Conflicting" branch to priority formula in `IMPACT_SUMMARY_PROMPT` — assigns "Committee Deliberation Required" instead of P1--P4 | TC5: Partial → Pass. TC1, TC2, TC3, TC4: no regression. | 4 Pass, 1 Partial |

!!! note "TC3 remains Partial — and that may be acceptable"
    After two iteration cycles, the scorecard is 4 Pass, 1 Partial (TC3: cold-start uncertainty communication). The TC3 fix is a prompt refinement in `IMPACT_SUMMARY_PROMPT` — adding conditional presentation logic for low-confidence estimates. This is a quality improvement (better communication of uncertainty), not a correctness fix (the estimate itself is right, and the low-confidence flag is present). A BA reviewing the output would catch the understated uncertainty at the `hil_review_summary` checkpoint in about 30 seconds and add a stronger caveat. The question from the [Stage 6 methodology](../stages/06-evaluate.md#when-to-stop-iterating) applies: "is agent-plus-correction meaningfully faster than doing it manually?" For TC3, it is — the agent still saved 50+ minutes of data gathering and initial analysis, and the correction is a 30-second edit to one section. This is a candidate for a third iteration cycle, not a blocker for production use.

---

## Graduation Criteria

The agent is ready for production use when:

- [x] All 5 test cases pass without major human corrections — 4 Pass after iteration; TC3 Partial requires a minor presentation correction at `hil_review_summary`, not a major rework
- [x] Total time (agent + human review) is less than 50% of the manual process time — measured at ~16 min vs 60–90 min (~78–82% reduction)
- [ ] No critical failures (wrong complexity tier leading to misallocation, missed strategic conflict, undetected strong duplicate) in the last 3 evaluation rounds
- [ ] At least one colleague has reviewed and validated the output quality
- [ ] Error handling has been tested for all identified failure modes (Jira API failure, Confluence timeout, empty backlog, insufficient historical data, malformed LLM output)

!!! tip "When to push the automation boundary"
    After 2--3 successful evaluation cycles: if the BA rarely changes the assessments at `hil_review_assessment`, consider removing that checkpoint and keeping only `hil_review_summary` (the final document review). If strategic alignment assessment proves consistently accurate — because OKRs are well-maintained and organisational context rarely changes the score — consider making Step 7's HIL component fully automated. The automation boundary is not fixed — it should expand as the agent proves itself. But remove one checkpoint at a time, with a full evaluation cycle after each change.

---

[:octicons-arrow-left-24: Back to Stage 6: Evaluate](../stages/06-evaluate.md){ .md-button }
