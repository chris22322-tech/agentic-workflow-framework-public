# Worked Example: Stage 2 -- Select

!!! example "Worked Example"
    We're applying Stage 2 to: **the BA Workflow Inventory Table from Stage 1**. The goal is to choose a single workflow to automate -- the one most likely to succeed and deliver value.

## Completed Artifact: Selection Decision Record

### Chosen Workflow

**New Feature Request Intake & Impact Assessment**

### Candidate Comparison

Three candidates rated High or Medium automation potential in Stage 1 were scored using the six-dimension framework. A fourth — Requirements Review Facilitation, rated Low in Stage 1 — is included to demonstrate how the disqualification criteria apply in practice:

| Candidate | Impact | Feas. | Risk Tol. | Compl. | Learn. | Org. | Composite |
|---|---|---|---|---|---|---|---|
| **New Feature Request Intake** | 4 | 5 | 5 | 3 | 4 | 4 | **4.35** |
| Sprint Planning Prep | 3 | 5 | 5 | 4 | 3 | 5 | 4.20 |
| Requirements Review Facilitation† | 3 | 4 | 3 | 3 | 2 | 3 | 3.20 |
| Gap Analysis Report | 3 | 3 | 4 | 2 | 3 | 3 | 3.10 |

**Sprint Planning Prep** scored well on Feasibility (5) and Risk Tolerance (5) — all data sources have APIs, and the output is an internal brief reviewed in the planning meeting itself. But Impact scored only 3: at 2 hours biweekly for a single team, it saves roughly 4 hours per month. There is no instance multiplier (unlike a CSM managing multiple accounts, the BA typically preps for one team's sprint). Strong on pragmatism, modest on payoff.

†**Requirements Review Facilitation** was disqualified before composite ranking. Despite scoring a respectable 3.20, it triggers the first disqualifier: the workflow's value comes from the *live facilitation* — drawing out unstated assumptions, mediating between conflicting stakeholder views, and building alignment in real time. The signed-off requirements are the artifact, but the conversation is the product. An agent could prepare the meeting (pre-populate an agenda, compile open questions, pull the latest requirements from Confluence), but that preparation is a sub-workflow of the facilitation, not the facilitation itself. Automating the meeting removes the thing that makes it valuable.

### Selection Scores

| Criterion | Weight | Score (1-5) | Rationale |
|---|---|---|---|
| **Impact** | 30% | 4 | 3-5 requests per week at 2-3 hours each. The agent handles data gathering, duplicate checking, and draft assessment — roughly 60-70% of the per-occurrence time. Estimated savings: ~1.5 hours per occurrence × ~15 occurrences/month = ~22 hours/month. Conservatively scored 4 rather than 5 because the BA still spends meaningful time reviewing the agent's output and adding contextual judgement before submission. |
| **Feasibility** | 25% | 5 | Jira has a mature REST API. Confluence has a REST API with full page and search access. The roadmap tool (whether Notion, Productboard, or a spreadsheet) has either an API or a structured export. OKR tracking lives in a system with API access or is maintained in a structured document. Every data source the workflow touches is programmatically accessible. |
| **Risk Tolerance** | 20% | 5 | The impact assessment is an internal working document reviewed by the BA before it reaches the prioritisation committee. If the agent miscategorises a request's complexity or misses a duplicate, the BA catches it during review. No external stakeholders see the output until the BA has validated it. Errors are cheap and correctable. |
| **Complexity** | 10% | 3 | Four data sources (Jira, Confluence, roadmap tool, OKR tracker) add integration complexity. The duplicate-checking step requires fuzzy matching against the existing backlog — not a simple keyword lookup. And the strategic alignment assessment asks the LLM to compare a request against current OKRs, which involves interpretation, not just data retrieval. But the overall flow is linear: receive → log → check duplicates → gather context → estimate → assess → draft → review. No conditional branching or dynamic routing. |
| **Learning Value** | 5% | 4 | The pattern — intake trigger → data gathering from multiple sources → structured assessment → human review → submission — transfers directly to Change Request Impact Assessment, Backlog Grooming Prep, and (with adaptation) Sprint Planning Prep. Building this teaches you the "triage and assess" pattern, which is the most common shape for BA automation. |
| **Organisational Readiness** | 10% | 4 | The BA owns this workflow end-to-end and has been exploring automation options. The prioritisation committee that receives the completed assessments has been consulted and is supportive — they have expressed frustration with inconsistent assessment depth and welcome a more structured approach. The automation does not change their review process; it improves the inputs they receive. |

### Weighted Score

**4.35** = (4 × 0.30) + (5 × 0.25) + (5 × 0.20) + (3 × 0.10) + (4 × 0.05) + (4 × 0.10)

### Justification

New Feature Request Intake combines high volume (3-5 per week) with a structurally repeatable process: every request follows the same assessment path through the same data sources against the same criteria. The workflow's strength is not any single dimension but its overall profile — no score below 3, and the two dimensions that matter most for a first build (Feasibility and Risk Tolerance) both score 5. Every system the agent needs to access has a documented API. Every output the agent produces is reviewed before it affects any decision. This is a workflow where the agent can fail safely while you learn what works.

### Risks

Duplicate detection is the hardest step to get right. Exact-match duplicate checking is trivial, but real duplicates rarely use the same language — a request for "batch export" and an existing ticket for "bulk download functionality" are the same thing described differently. The agent will need semantic similarity matching, which may surface false positives that waste reviewer time or miss true duplicates that defeat the purpose. Expect to iterate on the duplicate-detection prompt.

Strategic alignment assessment depends on OKRs being current and specific enough to compare against. If OKRs are vague ("improve customer satisfaction") or stale (last quarter's objectives still in the tracker), the agent's alignment score will be unreliable. This is a data quality dependency, not a technical one — the agent can only assess alignment against what's actually documented.

## Annotations

!!! note "Why Impact scored 4 and not 5"
    The raw arithmetic looks like a 5: ~15 occurrences per month × 1.5 hours saved = ~22 hours. That comfortably exceeds the 10 hrs/month threshold. But the score reflects *realised* savings, not theoretical maximum. The BA still reviews every assessment — checking the duplicate results, validating the complexity estimate against their own experience, and adding contextual nuance the agent cannot capture (e.g., "this request is politically sensitive because it came from the VP of Sales"). That review loop is not wasted time; it is the quality gate that makes the automation trustworthy. The honest estimate is closer to 8-12 hours of net savings per month once you account for review overhead. That is a strong 4.

    Compare this to the CSM's Quarterly Account Health Review, which scores Impact 5. The CSM's multiplier is structural — the same workflow repeated across 10 accounts, where the agent's output for Account A requires no adjustment before starting Account B. The BA's multiplier is frequency-based — many small occurrences — but each occurrence still requires the BA's contextual judgement layered on top. Frequency multipliers are real but less compounding than instance multipliers.

!!! note "Why Feasibility scored 5 and not 4"
    In the CSM example, Feasibility dropped to 4 because Slack sentiment analysis was a weak link — retrieving threads is easy, but interpreting conversational tone is inherently noisy. The BA workflow avoids this entirely. Every data source is structured: Jira tickets have defined fields, Confluence pages have searchable content, roadmap tools export priorities as structured data, and OKR trackers store objectives with measurable key results. The agent is not being asked to *interpret* any of these sources — it is being asked to *retrieve and compare* structured data. When all your inputs are structured and all your access paths are documented, Feasibility is 5.

    This is worth noticing as a pattern: workflows that operate on **system-of-record data** (Jira, Confluence, CRMs) tend to score higher on Feasibility than workflows that depend on **communication data** (Slack, email, meeting notes). If your workflow's critical inputs live in a ticketing system or a wiki rather than in conversations, you have a Feasibility advantage.

!!! note "Why Complexity scored 3 despite a linear flow"
    The flow is linear — no conditional branching, no dynamic routing — which would normally suggest a 4 or 5. But two steps introduce non-trivial complexity. First, duplicate detection requires semantic similarity, not just keyword matching. The agent needs to recognise that "add SSO support" and "integrate SAML authentication" are likely the same request, which is an LLM judgement call that can be wrong in both directions (false positives and false negatives). Second, strategic alignment assessment asks the agent to compare a feature request against OKR language and determine fit — this is interpretation, not retrieval. A linear flow with two LLM-judgement steps is meaningfully harder than a linear flow with purely mechanical steps. That is the difference between Complexity 3 and Complexity 4-5.

!!! note "Why Sprint Planning Prep is the runner-up, not the winner"
    Sprint Planning Prep is arguably the *safer* first build. It scores 5 on Feasibility, 5 on Risk Tolerance, and 4 on Complexity — the pragmatism dimensions are as strong or stronger than New Feature Request Intake. What holds it back is Impact: 2 hours biweekly for a single team translates to ~4 hours per month saved, firmly in the Score 3 range. There is no instance multiplier — the BA preps for one team's sprint, not ten. And Learning Value is 3 rather than 4, because the "compile metrics and summarise" pattern is simpler than the "triage, assess, and recommend" pattern and transfers to fewer workflows. Sprint Planning Prep would be a fine first build if you prioritise certainty over payoff. But New Feature Request Intake delivers more value without materially more risk.

!!! note "Why Gap Analysis Report scored lowest despite the highest per-occurrence time cost"
    At 6-8 hours, Gap Analysis is the most time-intensive workflow on the BA's inventory. The temptation is to assume that automating the most time-consuming workflow saves the most time. But time cost per occurrence is only one factor in the Impact formula — you also need frequency and instance count. Gap Analysis runs 1-2 times per quarter with no instance multiplier. Even if the agent could automate the entire data-gathering phase (roughly half the time), that saves 3-4 hours per quarter — less than 1.5 hours per month. Impact: 3 at best, and that is generous.

    The deeper problem is Complexity: 2. The annotation in Stage 1 explained why — every gap analysis defines "the gap" differently. One engagement compares a billing system against regulatory requirements; the next assesses whether an internal tool supports a new market. The interpretive framework changes each time, which means the agent cannot reuse its assessment logic from one run to the next. Low structural repeatability is the gap analysis's fundamental constraint. The [sub-workflow pattern](../stages/01-decompose.md#when-a-workflow-scores-medium-the-sub-workflow-pattern) is the right approach here: automate the data compilation (pull capabilities, extract requirements, compare feature lists) and leave the synthesis to the BA.

!!! tip "The BA selection story is different from the CSM selection story — and that's the point"
    In the CSM example, the Quarterly Account Health Review won primarily on **Impact** — the per-account multiplier turned a moderate time cost into an enormous one, and the other dimensions were strong enough to support it. The BA's winner tells a different story. New Feature Request Intake does not have the highest Impact on the table — Sprint Planning Prep ties it on most pragmatism scores, and Gap Analysis has a higher per-occurrence time cost. It wins because it has **no weak dimension**. Feasibility 5, Risk Tolerance 5, and a clean linear flow mean the first build is almost certain to succeed. Impact 4 means the payoff is real, not trivial. Learning Value 4 means the patterns transfer. The CSM example teaches "pick the highest-impact workflow that is feasible." The BA example teaches the complementary lesson: "pick the workflow with the strongest overall profile, even if it is not the most impressive on any single dimension."

---

[:octicons-arrow-left-24: Back to Stage 2: Select](../stages/02-select.md){ .md-button }
