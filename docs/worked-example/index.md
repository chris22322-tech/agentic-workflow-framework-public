# Worked Example: Quarterly Account Health Review

!!! example "What you're looking at"
    This is a complete, end-to-end application of the Agentic Workflow Framework to a real workflow: the **Quarterly Account Health Review** performed by a **Customer Success Manager (CSM)**.

    Each page in this section shows the completed artifact for one stage, with annotations explaining the decisions made.

## Why this example

The Quarterly Account Health Review was chosen as the worked example for four reasons:

1. **High time cost.** A CSM typically spends 6-8 hours per account per quarter on this workflow. Across a strategic portfolio of 5-15 accounts, that is 30-120 hours per quarter -- a significant chunk of capacity.
2. **Repeatable structure.** The workflow follows the same pattern every time: gather data from known sources, assess against known criteria, produce a structured report. This predictability makes it a strong automation candidate.
3. **Good learning value.** The data gathering + synthesis + report generation pattern transfers directly to 3-4 other CSM workflows (renewal prep, EBR prep, internal briefings). Building this teaches you a pattern you will reuse.
4. **Data gathering + synthesis is a broadly reusable pattern.** Most knowledge-work automation starts here: pull data from multiple systems, make sense of it, and produce a deliverable. If you learn this pattern well, you can apply it far beyond customer success.

!!! info "Two versions of this example — pick the one that matches your role"
    **Customer Success Manager (CSM), 5-15 strategic accounts:** The main worked example below is written for you. It assumes deep per-account engagement (6-8 hours per account per quarter), with the agent reviewing one account at a time and pausing for your input at key decision points. Start at [What each stage shows](#what-each-stage-shows) and work through each stage.

    **Customer Success Manager (CSM), 20-50 accounts:** Your workflow is fundamentally different — shallower per-account reviews (2-4 hours), portfolio-level triage as the primary weekly workflow, and templated rather than bespoke outputs. The [Portfolio Health Review](#portfolio-health-review) section below is a complete, portfolio-native walkthrough of how each framework stage adapts to your reality. You can read it directly without working through the strategic-account version above first.

## What each stage shows

| Stage | What you'll see | Key takeaway |
|---|---|---|
| [Decompose](decompose.md) | Full Workflow Inventory Table for a CSM role (8 workflows across 4 responsibility areas) | How to enumerate workflows and score automation potential |
| [Select](select.md) | Selection Decision Record with scored criteria and weighted composite | How to make a defensible, systematic choice |
| [Scope](scope.md) | 14-step workflow map with automation boundaries, data inventory, and integration requirements | How to draw the line between agent work and human work |
| [Design](design.md) | Agent architecture, data flow, step-by-step processing logic, and error handling | How to translate a scoped workflow into an agent design |
| [Build](build.md) | Working code: agent definition, processing functions, API connectors, and prompt templates *(technical -- for the engineer building it)* | How the design becomes implementation |
| [Evaluate](evaluate.md) | Test case design and evaluation approach | How to validate that the agent actually works |

## How to use this section

You have two options:

- **Read alongside the methodology.** Open the relevant worked example page in a second tab as you work through each [stage](../stages/index.md). Use it as a reference for what the completed artifact should look like.
- **Read first, then do your own.** Skim through all six pages to build a mental model of the end-to-end process before starting your own workflow.

Either way, the annotations (in coloured callout boxes) explain *why* specific decisions were made -- not just what they are. Pay attention to those.

!!! tip "See also: Portfolio variant, Business Analyst, and Software Engineer worked examples"
    This framework includes worked examples across multiple roles and workflow patterns. The **[Portfolio Health Review](#portfolio-health-review)** below covers a *triage-rank-surface* pattern for scaled account management. The **[Business Analyst — New Feature Request Intake & Impact Assessment](../worked-example-ba/index.md)** follows a *triage-analyse-recommend* pattern triggered on demand, and the **[Software Engineer — Release Notes Compilation & Publishing](../worked-example-se/index.md)** follows a *fetch-categorise-generate-publish* pattern triggered by a release event. Reading across these examples shows that the framework generalises across roles and workflow shapes.

---

## Portfolio Health Review

!!! example "What you're looking at"
    This is a complete walkthrough of the same framework applied to a **Customer Success Manager (CSM)** managing **20-50 mid-market accounts**. It covers every stage — Decompose through Evaluate — showing how each artifact changes when the fundamental workflow shape is portfolio triage, not deep single-account analysis.

The agent you need is different from the strategic-account version. A CSM managing 8 strategic accounts spends 6-8 hours per account producing bespoke, executive-facing narratives. Your value equation is inverted: 2-4 hours per account, templated outputs, and the agent's primary job is not "deep analysis of one account" but **"surface the five accounts that need me this week out of thirty."** Portfolio-level triage is your primary weekly workflow — the per-account review is a building block inside it, not the main event.

The single-account flow from the strategic-account version is the correct inner unit. But wrapping it in a for-loop is not enough. You need a **portfolio-level summary**: which accounts need immediate attention, how they rank against each other, and where to allocate limited time. Portfolio triage is a distinct analytical step with its own logic, not just iteration.

Each section below shows the completed artifact for one stage, with annotations explaining what changes from the strategic-account version and why.

### Decompose

The Workflow Inventory Table changes in three ways when moving from a CSM managing 5-15 strategic accounts to a CSM managing 20-50.

**Time estimates shrink.** A strategic-account CSM spends 6-8 hours per account because strategic accounts require deep analysis, bespoke narratives, and executive-level reporting. A CSM managing 30 accounts does not have that budget. Expect 2-4 hours per account for health reviews, 1-2 hours for renewal prep, and 30-60 minutes for standup prep. If you use the strategic-account numbers unchanged, every workflow will look like a strong automation candidate because the time cost appears enormous -- but the per-account depth is different, which changes what the agent needs to do.

**Portfolio-level workflows appear as distinct inventory entries.** A CSM treats "review my 10 accounts" as 10 runs of the same workflow. A CSM managing 30 accounts has workflows that only exist *because* of the portfolio: weekly portfolio triage, cross-account pattern detection, and resource allocation planning. These are not the same workflow run 30 times -- they are different workflows that consume the per-account outputs. Add them to the inventory as separate line items.

**Adapted Inventory Table (CSM, 30-account mid-market book):**

| Responsibility Area | Workflow | Trigger | Frequency | Avg Time (hrs) | Systems Touched | Output/Deliverable | Automation Potential |
|---|---|---|---|---|---|---|---|
| Account Health | Quarterly Account Health Review | Calendar (end of quarter) | Quarterly | **2-4** | CRM, Support tickets, Product usage data, Slack | Health report (templated, not bespoke) | High |
| Account Health | **Portfolio Triage** | Weekly or biweekly | **Weekly** | **1-2** | CRM, Support tickets, Product usage data | Ranked attention list + resource plan | **High** |
| Account Health | Escalation Triage | Incoming alert/flag | Ad hoc (5-8x/week) | 0.5-1 | CRM, Slack, Support platform | Triage assessment + action plan | Medium |
| Commercial | Renewal Preparation | 90 days before renewal | Per account cycle | **2-3** | CRM, Finance, Contract system | Renewal brief + risk flag | High |
| Commercial | Upsell Opportunity Identification | Quarterly review | Quarterly | **1-2** | Product usage data, CRM | Opportunity flag (not a full brief) | Medium |
| Delivery Coordination | Cross-team Standup Prep | Weekly standup cadence | Weekly | **0.5** | Jira, Slack | Status summary + blockers list | High |
| Stakeholder Mgmt | Exec Business Review Prep | Quarterly or semi-annual | Quarterly | **4-6** | CRM, Product data, Finance, Slides | EBR deck + talking points | Medium |
| Stakeholder Mgmt | Internal Account Briefing | Ad hoc (new stakeholder) | Ad hoc | 1-2 | CRM, Internal docs, Slack | Briefing doc | High |

!!! warning "The new entry matters"
    **Portfolio Triage** does not exist in the strategic-account inventory because a CSM with 8 accounts does triage in their head. At 30 accounts, it is a distinct weekly workflow consuming 1-2 hours — and it scores High because it is almost entirely data retrieval, ranking, and templated output. If you skip this entry, you will try to bolt portfolio triage onto the per-account health review later, which is the wrong decomposition.

Note the cascading changes: time estimates are lower across the board, Escalation Triage frequency increases (more accounts = more escalations), and output deliverables shift toward templated formats rather than bespoke narratives. The Go-live Readiness Assessment is dropped — in a mid-market book, go-lives are handled by implementation teams, not the CSM.

### Select

The Selection Decision Record scoring shifts when you multiply across a larger book. The same six criteria apply, but the numbers move.

**Adapted Candidate Comparison (CSM, 30-account book):**

| Candidate | Impact | Feas. | Risk Tol. | Compl. | Learn. | Org. | Composite |
|---|---|---|---|---|---|---|---|
| **Quarterly Account Health Review** | 5 | 4 | 4 | **2** | 5 | 4 | **4.15** |
| **Portfolio Triage** | **5** | **4** | **5** | **3** | **4** | **3** | **4.30** |
| Cross-team Standup Prep | 3 | 5 | 5 | 4 | 2 | 4 | 4.05 |
| Renewal Preparation | 4 | 3 | 3 | 4 | 4 | 3 | 3.45 |

**What changed and why:**

- **Portfolio Triage enters the comparison** and scores highest. Impact is 5 because the workflow runs weekly across all accounts — the cumulative time cost exceeds the quarterly health review. Risk Tolerance is 5 because the output is an internal prioritisation list, not a client-facing deliverable. Complexity is 3 (not 2) because cross-account comparison logic is non-trivial, but the data inputs are the same ones used by the per-account health review.
- **Health Review Complexity drops from 3 to 2** relative to the strategic-account version. The per-account analysis is shallower (templated, not bespoke), and the synthesis step is lighter because the CSM is not producing executive-facing narratives. But batch processing adds system complexity — the agent must handle 30 accounts per run without manual intervention. Net effect: the per-account flow is simpler, but the orchestration is harder.
- **Cross-team Standup Prep Impact rises from 2 to 3.** A CSM running standups for 8 accounts barely notices the prep time. A CSM covering 30 accounts across multiple pods spends more aggregate time, and the weekly frequency compounds.
- **Portfolio Triage Organisational Readiness is 3, not 4.** Unlike the Health Review (where the CSM already owns the workflow and leadership is supportive), Portfolio Triage is a *new* workflow that does not exist yet in most CSM teams. The team is aware triage is being discussed, but no one has been involved in planning how an automated portfolio ranking would fit into their weekly routine. Adoption requires the CSM to trust an agent's prioritisation of 30 accounts — a higher trust bar than reviewing a single account's health report.
- **The composite winner may differ.** In this scoring, Portfolio Triage edges out the Health Review. But the worked example still builds the Health Review first because (a) Portfolio Triage *consumes* per-account health data as an input, so you need the inner flow first, and (b) the Health Review has higher Learning Value — the data gathering + synthesis pattern transfers to more workflows. The selection rationale should note this dependency explicitly.

!!! tip "Impact scores change because the multiplier changes"
    In the strategic-account scoring, Impact for the Health Review is driven by 6-8 hours × 10 accounts = 60-80 hours/quarter. In the portfolio scoring, it is 2-4 hours × 30 accounts = 60-120 hours/quarter — similar total, but the per-account depth is different. Portfolio Triage scores Impact 5 because 1-2 hours × 52 weeks = 52-104 hours/year, and the workflow *does not exist without the agent* — most CSMs skip systematic triage because it takes too long manually.

### Scope

The scope adds two steps and three constraints when portfolio processing is a v1 requirement.

**Add Step 13: Aggregate portfolio results**

| # | Step | Action | Input | Output | Decision Logic | Boundary |
|---|---|---|---|---|---|---|
| 13 | Aggregate portfolio results | Rank all accounts by health score and urgency, produce a portfolio-level summary | All per-account health reports, CRM metadata for all accounts | Portfolio summary: ranked account list, resource allocation recommendations, immediate-attention shortlist | Rank by composite urgency: Red accounts first, then Amber, then Green. Within each tier, sort by renewal proximity. Flag any account where the health score changed from the previous quarter (trajectory matters more than static score). Identify accounts consuming disproportionate support resources relative to ARR. | AUTOMATE (ranking) / HIL (resource allocation review) |

**Add Step 14: Portfolio-level HIL review**

| # | Step | Action | Input | Output | Decision Logic | Boundary |
|---|---|---|---|---|---|---|
| 14 | Review portfolio summary | Review the ranked portfolio, adjust priorities, approve resource allocation plan | Portfolio summary from Step 13 | Approved portfolio action plan | Human judgement: does the ranking match reality? Are there political or relationship factors that change the priority order? Should any accounts be escalated to leadership? | HIL |

**Constraints and Assumptions — additions:**

- The agent processes all accounts in the portfolio per run, not one at a time. Individual account reviews happen at the portfolio level, not per-account — the CSM reviews all draft analyses as a batch and flags only accounts that need intervention.
- Portfolio triage criteria (ranking logic, attention thresholds) should be externalised as config alongside the single-account scoring rubric.
- Time budget per account drops to 2-4 hours. Scoring thresholds and report detail should reflect scaled engagement, not strategic deep-dives.

??? example "Complete Portfolio Scope: Core-tier step-by-step workflow (30-account mid-market book)"

    This is the complete, standalone workflow map for a CSM running the Quarterly Account Health Review across a 30-account mid-market portfolio. It applies the **Core** tier profile — the right default, since most of a 30-account book falls into this segment. Steps marked with **△** differ from the strategic-account version; the adaptation note explains what changed and why.

    You do not need to cross-reference the [strategic-account scope document](scope.md) to use this table. It is self-contained.

    | # | Step | Action | Output | Boundary | △ Portfolio Core Adaptation |
    |---|---|---|---|---|---|
    | 1 | Pull CRM account data | Query CRM for account record: ARR, contract dates, tier, key contacts, recent activity | Account metadata + tier classification | AUTOMATE | — Same. Tier field now drives per-account workflow shape via tier profile config |
    | 1b | Pull CS platform health score | Query CS platform for current health score, lifecycle stage, active CTAs | Platform health score + lifecycle metadata | AUTOMATE | — Same |
    | 1c | Pull prior quarter's health report | Retrieve previous quarter's report, action plan, and completion status from output store | Prior health score + action items with completion status | AUTOMATE | — Same. First-run accounts (common when inheriting a book) return null gracefully |
    | 2 | Pull support ticket history | Export tickets for the quarter by account and date range | Ticket list with status, severity, resolution time, CSAT | AUTOMATE | — Same |
    | 3 | Pull product usage metrics | Access usage dashboard or API for account-level metrics | Usage stats: active users, feature adoption, API volume, error rates | AUTOMATE | — Same. V1 aggregates at account level (blended across products) |
    | 4 | Pull recent comms context | Retrieve comms from configured channels: Slack, CRM-logged emails, call summaries, CS platform notes | Aggregated comms context across channels | AUTOMATE | — Same. Channel mix varies per account; agent queries all configured sources |
    | 5 | Review comms sentiment | Assess tone across channels, cross-reference NPS/survey data, produce per-stakeholder sentiment map | Per-stakeholder-role sentiment map with composite rollup and quantitative anchors | **△ Conditional HIL** | **Changed.** HIL triggers only when automated sentiment scores Amber or Red. Green scores auto-approve and proceed without pause. A strategic-account CSM reviews every account's sentiment because the per-account stakes justify it; at 30 accounts, pausing on every Green wastes 15-20 minutes per healthy account with near-zero correction rate. The agent still produces the full sentiment analysis — the CSM just does not review it unless there is something to review |
    | 6 | Assess ticket health | Analyse ticket volume trends, severity distribution, resolution times vs SLA benchmarks | Ticket health assessment: improving / stable / degrading + key issues | AUTOMATE / HIL (edge cases) | — Same |
    | 7 | Assess product engagement | Analyse usage trends, feature adoption, compare to **mid-market** tier benchmarks | Engagement assessment: healthy / at-risk / critical | AUTOMATE / HIL (context) | **Changed.** Benchmarks default to mid-market thresholds (DAU/MAU ≥30%, feature adoption ≥45%, API volume ≥2K/month) rather than requiring per-account tier lookup. Most of the 30-account book is mid-market; the few strategic accounts in the book use the strategic tier profile instead of this one |
    | 7b | Assess prior action follow-through | Review prior quarter's action items against completion status. Flag items unresolved for 2+ quarters as systemic | Action follow-through assessment: completion rate + unresolved items with age | AUTOMATE / HIL (context) | — Same. Skip if no prior report exists (first review cycle) |
    | 8 | Identify risks and opportunities | Synthesise Steps 5–7b findings with contract timeline. Pattern-match: declining usage + upcoming renewal = churn risk | Risk register + opportunity list | HIL | — Same |
    | 8b | Generate prioritised action items | Translate risks/opportunities into specific, time-bound actions with owner, deadline, success criterion. Cap at 5–7 items | Prioritised action plan. Carried-forward items from 7b inherit elevated priority | AUTOMATE (draft) / HIL (validation) | — Same. Actions trend toward templated interventions (adoption workshop, check-in call) rather than bespoke executive strategies |
    | 9 | Assign overall health score | Rate account Green/Amber/Red across four dimensions (tickets, usage, sentiment, contract). Reconcile against CS platform score from 1b | Health score with justification + platform reconciliation note | HIL | — Same |
    | 10 | Generate health report | Write structured report with sections for each dimension | Formatted health report | AUTOMATE (draft) / HIL (review) | **Changed.** Output is **templated**, not bespoke. The agent fills a standard template with dimension scores, key findings, and action items rather than generating a narrative tailored to each account's executive audience. Strategic accounts need bespoke framing; a 30-account book needs consistent, scannable reports that can be reviewed in batch |
    | 11 | Generate exec summary | Write 3–5 sentence summary: overall status, top risk, top action | Exec summary paragraph | AUTOMATE (draft) / HIL (tone) | **Changed.** Templated structure. Same content as the strategic-account version but tone is standardised rather than account-specific |
    | 12 | Final review and distribution | Review complete package, make edits, send to stakeholders | Distributed report | MANUAL | — Same. At 30 accounts, batch the review: scan all reports in one sitting, flag exceptions, distribute |
    | 12b | Write back to CS platform | Update platform with approved health score, dimension scores, timeline entry, and triggered playbooks/CTAs | Updated CS platform record | **△ Conditional HIL** | **Changed.** HIL triggers only when the health score changed from the prior quarter. Unchanged scores auto-write without confirmation. This saves ~30 confirmation clicks per quarter for stable accounts while still catching meaningful score transitions |
    | 13 | **Aggregate portfolio results** | Rank all accounts by health score and urgency. Produce portfolio summary: ranked list, resource allocation signals, immediate-attention shortlist, cross-account patterns | Portfolio summary (see [output format below](#portfolio-summary-output)) | AUTOMATE (ranking) / HIL (review) | **New step — not in the strategic-account scope.** Does not exist for a CSM managing 8 accounts because triage happens in their head. At 30 accounts, portfolio-level ranking is a distinct analytical step with its own logic: Red first, then Amber, then Green; within each tier, sort by renewal proximity; flag trajectory changes and disproportionate support load |
    | 14 | **Review portfolio summary** | Review ranked portfolio, adjust priorities, approve resource allocation plan | Approved portfolio action plan | HIL | **New step — not in the strategic-account scope.** The CSM's primary weekly decision point: which 5 accounts need me this week? This is where cross-account judgement happens — political factors, relationship context, and resource constraints that the ranking algorithm cannot see |

    **Reading this table:**

    - **12 of 16 steps are unchanged** from the strategic-account scope at the action level. The workflow structure is the same; the adaptations are about depth (templated vs bespoke), HIL thresholds (conditional vs always), and the two new portfolio steps.
    - **Step 5 and 12b** shift from always-on HIL to conditional HIL. This is the biggest time-saver: across 30 accounts, skipping human review on healthy sentiment scores and unchanged health scores recovers hours per quarter.
    - **Steps 13–14** are net-new. They consume the per-account outputs and produce the portfolio-level deliverable that the strategic-account version does not need.
    - **Scaled-tier accounts** in your book (if any) would skip Steps 5, 8, and 8b entirely and trigger HIL only at Step 9 when a dimension scores Red. See the [tier profile configuration](scope.md#constraints-and-assumptions) for the full tier matrix.

### Design

The portfolio wrapper adds one processing action and one HIL checkpoint after the per-account loop completes. The single-account flow runs unchanged as the inner unit.

??? note "Technical detail: memory fields and flow"

    **Additional memory fields for portfolio mode:**

    | Field | Type | Purpose |
    |---|---|---|
    | `account_ids` | list of strings | The set of accounts in the portfolio being processed |
    | `quarter` | string | Reporting period |
    | `account_results` | list of structured objects | Per-account results populated by the inner loop — each entry is the final memory state from one single-account run |
    | `portfolio_summary` | structured object | Ranked list, resource allocation signals, attention shortlist |
    | `portfolio_human_feedback` | optional string | Reviewer adjustments to portfolio priorities |

    **Portfolio flow:**

    ```mermaid
    graph TD
        START([START]) --> run_accounts[run_accounts<br/><em>loop: run single-account agent<br/>for each account in portfolio</em>]
        run_accounts --> aggregate_portfolio[aggregate_portfolio<br/><em>rank accounts, identify attention<br/>shortlist, resource allocation</em>]
        aggregate_portfolio --> hil_review_portfolio{{"`**◆ HIL: review portfolio**
        pause and surface ranked portfolio for CSM review`"}}
        hil_review_portfolio -->|approved| END([END])
        hil_review_portfolio -->|adjust| aggregate_portfolio
    ```

The `run_accounts` action runs the single-account flow for each account and collects results. The key design decision: HIL checkpoints inside the single-account flow are **removed or batched** for portfolio mode. Instead of pausing after every account's analysis, the CSM reviews all accounts together at the portfolio level. If specific accounts need deeper review, the CSM flags them during the portfolio HIL and re-runs those accounts individually with per-account HIL enabled.

**Node specification — `aggregate_portfolio`:**

- **Purpose:** Rank accounts by urgency and produce a portfolio-level action plan
- **Tools:** LLM for narrative synthesis; ranking logic can be deterministic
- **Logic:**
    1. Sort accounts into Red / Amber / Green tiers based on per-account health scores.
    2. Within each tier, sort by renewal proximity (nearest renewal first).
    3. Flag trajectory changes: accounts that moved from Green → Amber or Amber → Red since last quarter.
    4. Compute resource allocation signals: accounts consuming disproportionate support volume relative to ARR, accounts with upcoming renewals that need proactive outreach.
    5. Produce an "immediate attention" shortlist (top 5 accounts requiring action this week).
    6. LLM generates a narrative portfolio summary with cross-account patterns (e.g., "3 accounts show declining API usage after the v4 migration — this may be a product issue, not an account issue").

### Portfolio Summary Output

This is what the `aggregate_portfolio` action produces. The CSM reviews this at the portfolio HIL checkpoint.

```json
{
  "generated": "2026-Q1",
  "total_accounts": 30,
  "score_distribution": {"Red": 3, "Amber": 8, "Green": 19},

  "immediate_attention": [
    {
      "account": "Globex Inc",
      "health_score": "Red",
      "renewal_days": 58,
      "top_risk": "Usage down 30% QoQ + 3 open P1 tickets + VP expressing frustration",
      "recommended_action": "Escalation call with CS leadership this week"
    },
    {
      "account": "Initech Ltd",
      "health_score": "Red",
      "renewal_days": 45,
      "top_risk": "CSAT dropped to 3.2 after billing escalation; champion went silent on Slack",
      "recommended_action": "Executive sponsor outreach within 48 hours"
    },
    {
      "account": "Nexus Corp",
      "health_score": "Amber",
      "renewal_days": 120,
      "top_risk": "Analytics Dashboard usage critical (15% DAU/MAU) while Platform API is healthy — product-specific churn risk",
      "recommended_action": "Schedule adoption workshop for Analytics Dashboard users"
    }
  ],

  "trajectory_changes": [
    {"account": "Cyberdyne Systems", "previous": "Green", "current": "Amber", "driver": "Feature adoption dropped 18% after v4 migration"},
    {"account": "Soylent Corp", "previous": "Amber", "current": "Green", "driver": "P1 resolved, CSAT recovered to 4.3"}
  ],

  "cross_account_patterns": [
    "3 accounts (Cyberdyne, Tyrell, Weyland) show declining API usage post-v4 migration — likely a product adoption issue, not account-specific. Recommend flagging to Product team.",
    "5 of 8 Amber accounts have renewals within 90 days. Consider a dedicated renewal sprint this month."
  ],

  "resource_allocation": [
    {"account": "Globex Inc", "arr": "$420K", "support_tickets_qtd": 47, "signal": "Support load disproportionate to ARR — investigate root cause before renewal"},
    {"account": "Acme Corp", "arr": "$1.2M", "support_tickets_qtd": 3, "signal": "Healthy and low-touch — candidate for reduced cadence to free capacity for Red accounts"}
  ]
}
```

The portfolio summary answers the three questions a CSM needs every Monday morning: **Which accounts need me right now?** (immediate attention shortlist), **Where is the trend going?** (trajectory changes), and **How should I spend my time this week?** (resource allocation signals). An individual account report cannot answer any of these — they require cross-account comparison, which is why portfolio triage is a distinct analytical step, not a wrapper around the per-account loop.

### Evaluate

The evaluation suite adds one portfolio-level test case and three graduation criteria:

| Test Case | Account Profile | What It Tests |
|---|---|---|
| **Portfolio triage** | Full portfolio of 15-30 accounts with a mix of Red, Amber, and Green scores, including trajectory changes and renewal clustering | The portfolio action correctly ranks accounts, surfaces cross-account patterns, and produces actionable resource allocation signals. The immediate-attention shortlist matches what the CSM would have manually prioritised. |

**Graduation criteria addition:**

- [ ] Portfolio summary correctly ranks accounts by urgency (Red → Amber → Green, then by renewal proximity within tier)
- [ ] Cross-account patterns are surfaced when 3+ accounts share a common signal (e.g., post-migration usage decline)
- [ ] The CSM's Monday-morning triage decision takes less than 15 minutes with the portfolio summary vs. 2+ hours reviewing individual reports
