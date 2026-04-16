# Worked Example: Stage 2 -- Select

!!! example "Worked Example"
    We're applying Stage 2 to: **the CSM Workflow Inventory Table from Stage 1**. The goal is to choose a single workflow to automate -- the one most likely to succeed and deliver value.

## Completed Artifact: Selection Decision Record

### Chosen Workflow

**Quarterly Account Health Review**

### Candidate Comparison

All workflows rated High or Medium automation potential in Stage 1 were scored. The top four candidates:

| Candidate | Impact | Feas. | Risk Tol. | Compl. | Learn. | Org. | Composite |
|---|---|---|---|---|---|---|---|
| **Quarterly Account Health Review** | 5 | 4 | 4 | 3 | 5 | 4 | **4.25** |
| Cross-team Standup Prep | 2 | 5 | 5 | 5 | 2 | 4 | 3.85 |
| Renewal Preparation | 4 | 3 | 3 | 4 | 4 | 3 | 3.45 |
| Exec Business Review Prep† | 5 | 3 | 2 | 2 | 3 | 2 | 3.20 |

**Renewal Preparation** scored Impact 4 but Feasibility 3 — the contract management system has no confirmed API, making the data-gathering step uncertain. Combined with higher commercial risk (Risk Tolerance 3), the weighting drops it below the leader despite strong Complexity and Learning Value scores.

†**Exec Business Review Prep** was disqualified before composite ranking. Despite the highest raw Impact on the inventory (5), EBR prep triggers the first disqualifier: the preparation process forces you to engage deeply with the account relationship and exec sponsor priorities. The prep *is* the relationship-building — automating it removes the thing that makes it valuable.

### Selection Scores

| Criterion | Weight | Score (1-5) | Rationale |
|---|---|---|---|
| **Impact** | 30% | 5 | 6-8 hours per account per quarter, across multiple accounts. Easily exceeds 10 hrs/month saved. |
| **Feasibility** | 25% | 4 | CRM has API, support tickets are exportable, usage data is accessible. Slack context is harder to capture programmatically -- pulling threads is straightforward, but interpreting sentiment requires LLM judgement. |
| **Risk Tolerance** | 20% | 4 | Internal deliverable, reviewed by the CSM before sharing with anyone. Agent errors are catchable before they cause damage. |
| **Complexity** | 10% | 3 | Multiple data sources and a synthesis step add complexity, but the overall pattern is consistent: gather, analyse, score, report. No branching decision trees or dynamic routing. |
| **Learning Value** | 5% | 5 | The data gathering + synthesis + report generation pattern is the same pattern used in renewal prep, EBR prep, and internal briefings. Building this teaches you a pattern you will reuse for 3-4 other workflows. |
| **Organisational Readiness** | 10% | 4 | The CSM owns this workflow and has been exploring automation. The CS leadership team that reviews health reports is supportive — they want more consistent reporting across the portfolio. Account managers who receive the reports have not been deeply consulted but are unlikely to resist, since the CSM still reviews and contextualises every report before sharing. |

### Weighted Score

**4.25** = (5 × 0.30) + (4 × 0.25) + (4 × 0.20) + (3 × 0.10) + (5 × 0.05) + (4 × 0.10)

### Justification

The quarterly account health review combines high time cost with a repeatable structure: gather data from known sources, assess against known criteria, produce a structured report. It's reviewed internally before any client exposure, so agent errors are catchable. The data-gathering and synthesis pattern is the same pattern used in 3-4 other workflows, making this a high-leverage first build.

### Risks

Product usage data may require custom extraction depending on the platform. Qualitative signals from Slack conversations are harder to capture and interpret -- the agent may need to surface relevant threads for human review rather than attempting to synthesise sentiment.

## Annotations

!!! note "Why Impact scored 5"
    The time-per-occurrence alone (6-8 hours) is significant, but the real driver is the multiplier: a CSM with a portfolio of accounts runs this workflow for *each* account every quarter. If you manage 10 accounts, that is 60-80 hours per quarter on this single workflow. The score of 5 is justified by the combination of high per-occurrence cost and quarterly frequency across multiple accounts.

!!! note "Why Feasibility scored 4 and not 5"
    A perfect 5 requires "clean APIs or structured data sources readily available" for every input. The CRM, support platform, and usage data all meet that bar. But Slack is the weak link -- while the Slack API lets you search and retrieve messages, interpreting conversational context for sentiment is inherently noisy. The agent can retrieve threads, but accurately synthesising "is this customer frustrated?" from message fragments is unreliable enough to require human validation. That gap drops Feasibility from 5 to 4.

!!! note "Why Complexity scored 3"
    A score of 3 means "moderate complexity -- not trivial, but manageable." The workflow touches four data sources, which adds integration complexity. And the synthesis step (turning raw data into a health assessment) is not purely mechanical -- it requires the LLM to interpret patterns and apply a scoring framework. But the overall flow is linear (gather, then analyse, then synthesise, then report), which keeps it tractable. There are no conditional routing decisions or dynamic branching paths.

!!! tip "The selection process is about risk management, not ambition"
    You might be tempted to pick the highest-impact workflow regardless of other factors. Resist that. A workflow that scores Impact 5 but Feasibility 2 will stall during build and erode your confidence in the framework. The weighted scoring system deliberately balances ambition (Impact, Learning Value) against pragmatism (Feasibility, Risk Tolerance, Complexity). Your first agent build should succeed -- that success unlocks everything that follows.

---

[:octicons-arrow-left-24: Back to Stage 2: Select](../stages/02-select.md){ .md-button }
