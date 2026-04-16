# Stage 2: Select

You have an inventory of workflows. Now you need to pick one to automate — and this is where most people make their first mistake. The temptation is to go after the workflow that is most painful, most time-consuming, or most interesting to build. But the best first automation target is rarely the most ambitious one. It is the one most likely to actually work.

This stage gives you a scoring framework to evaluate your candidates across six dimensions — impact, feasibility, risk tolerance, complexity, learning value, and organisational readiness — so the decision is grounded in evidence rather than enthusiasm. You will score each candidate, apply a weighted formula, and select the workflow with the strongest overall profile. The goal is to pick a first win: something that delivers real value, builds your confidence with the framework, and creates momentum for automating the next workflow on your list.

---

## Inputs

!!! info "What You Need"

    - Workflow Inventory Table from [Stage 1: Decompose](01-decompose.md)

## Output Artifact

!!! info "Key Output"

    A **Selection Decision Record** containing:

    - Chosen workflow name
    - Selection score (see scoring criteria below)
    - One-paragraph justification
    - Known risks or caveats

!!! abstract "Template"

    Use the [Selection Record template](../blank-templates/selection-record.md) as you work through this stage. It includes the Scoring Matrix with all six dimensions and weighted formula, plus the Selection Decision Record.

!!! info "Download Templates"
    [:material-download: Download Spreadsheet](../downloads/Stage 2 - Select.xlsx){ .md-button }

    Import into Google Sheets for a pre-formatted template with example rows.

---

## Method

### Selection Criteria

Score each candidate workflow (those rated High or Medium automation potential) from **1 to 5** on each dimension:

| Criterion | What It Measures | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 |
|---|---|---|---|---|---|---|
| **Impact** | (Time saved per occurrence) x (Frequency) | <1 hr/month saved | 1–2 hrs/month saved | 3–5 hrs/month saved | 6–10 hrs/month saved | >10 hrs/month saved |
| **Feasibility** | Can the agent access the data it needs? Are APIs/integrations available? | No programmatic access; would require screen-scraping or manual input | One critical source requires manual input; others have partial or undocumented access | Some sources have APIs, but at least one key source has no confirmed programmatic access | Most sources have clean APIs or structured exports; one requires workarounds such as LLM-assisted interpretation | Clean APIs or structured data sources readily available |
| **Risk Tolerance** | What's the blast radius if the agent gets it wrong? | Output goes directly to an external client or triggers an irreversible action | Output reaches external stakeholders or triggers actions that are difficult to reverse | Output is reviewed before external use, but errors carry commercial or reputational risk | Internal deliverable with a review step; errors are catchable before causing damage | Output is internal, reviewable, and easily corrected |
| **Complexity** | How many decision points, branches, and edge cases? | Dozens of conditional paths, high ambiguity | Many conditional paths or significant ambiguity in decision logic | Multiple data sources or processing steps, but the overall flow is linear with few branches | Straightforward flow with a small number of well-defined decision points | Linear or near-linear flow with few branches |
| **Learning Value** | Will building this teach you patterns applicable to other workflows? | One-off, niche workflow | Mostly unique; patterns may apply to one other workflow at best | Core pattern transfers to 1–2 other workflows | Core pattern transfers to 2–3 other workflows with minor adaptations | Patterns transfer to 3+ other workflows |
| **Organisational Readiness** | Will the people who run this workflow trust and use the agent's output? | Team has not been consulted; active resistance or no awareness of automation plans | Team is aware automation is being discussed but has not been involved in planning | Team has been consulted and is neutral — no enthusiasm, no resistance | Team is supportive and has contributed requirements or feedback to the automation plan | Team has requested or championed the automation; adoption is pull, not push |

### How to Score Each Dimension

The selection criteria table gives you anchor points, but knowing the anchor descriptions is not the same as knowing how to arrive at a score. This section walks through each dimension with the reasoning you need to apply.

#### Impact

Impact is arithmetic, not intuition. Use this formula:

**Monthly time saved = Time per occurrence × Monthly frequency × Number of instances**

"Number of instances" is the multiplier most people miss. A workflow that takes 2 hours and runs weekly saves 8 hours per month — but if you run it per-account or per-project, multiply again. A 2-hour weekly workflow across 5 accounts is 40 hours per month.

Look at your inventory table. The **Frequency** and **Avg Time** columns give you the first two factors. The third — how many parallel instances exist — comes from asking: *do I run this once, or once per [account / project / team / client]?*

!!! note "Time is the primary proxy, not the whole picture"

    The scoring anchors use hours saved because time is the easiest benefit to measure and compare across candidates. But automation often delivers value beyond time savings — **quality consistency** (reducing variance in outputs across team members), **error reduction** (fewer manual data-handling mistakes), and **timeliness** (faster turnaround enabling downstream processes to start sooner). A workflow saving only 3 hours per month but dramatically reducing error rates in a compliance-sensitive output may deserve a stronger case than its time-based score suggests.

    Do not inflate the Impact score to account for these benefits — keep the score anchored to time saved so it remains comparable across candidates. Instead, capture quality, consistency, and timeliness benefits in the **one-paragraph justification** of your Selection Decision Record. This is where you make the case that a candidate's value extends beyond the number.

#### Feasibility

Feasibility measures whether the agent can access the data it needs. You do not need to be a developer to assess this — ask three questions:

1. **Can I export the data?** If the system has a "Download CSV" or "Export" button, the data is accessible. Score at least 3.
2. **Does the vendor advertise integrations?** Check the tool's integrations page or app marketplace. If it connects to Zapier, Make, or has a documented API, score 4.
3. **Am I copy-pasting from this system?** If the only way to get data out is to manually copy it, that source scores 1–2 for feasibility. One source like this drops your overall Feasibility score.

You are scoring the *overall* data picture, not each source independently. If four out of five sources have clean APIs but the fifth requires manual input, that is a 3 or 4 depending on how critical the fifth source is to the workflow.

??? info "Feasibility scoring anchors"

    - **Score 5:** Clean APIs or structured data sources readily available; standard connectors exist in most agent frameworks
    - **Score 4:** REST APIs available but may need thin wrapper code or OpenAPI specs
    - **Score 3:** Mix of API-accessible and manually-accessed sources
    - **Score 2:** Most sources require non-standard access (web scraping, file parsing, SFTP)
    - **Score 1:** No programmatic access; data only available through manual export or screen-based workflows

#### Risk Tolerance

Risk tolerance is about blast radius — what happens when the agent gets it wrong? Think through two questions:

1. **Who sees the output before it matters?** If you review it before anyone else sees it, errors are cheap. If the output goes directly to a client or triggers an external action, errors are expensive.
2. **Is the action reversible?** Sending an internal draft you can correct is low-risk. Posting to a client-facing system or triggering a billing change is high-risk.

The combination determines your score. Internal + reviewable + reversible = 5. External + no review + irreversible = 1. Most workflows fall somewhere in between.

#### Complexity

Complexity is about the shape of the workflow, not its difficulty. Count two things:

1. **Decision points.** How many times during the workflow do you choose between different paths? Each decision point adds complexity.
2. **Data sources.** Each additional system the workflow touches adds integration complexity.

A workflow that pulls from five systems but follows the same linear path each time (gather → process → output) is less complex than a workflow that pulls from two systems but branches into different handling paths depending on what it finds.

#### Learning Value

Learning value is forward-looking. Ask: *if I built this, what would I know how to build next?*

Score high when the workflow uses a common pattern — data gathering + synthesis, triage + routing, monitoring + alerting. Score low when the workflow is a one-off with unique requirements that do not generalise.

Look at your inventory table. If you can see 2–3 other workflows that follow a similar structure (same kind of trigger, same kind of data flow, same kind of output), the pattern transfers and Learning Value is 4–5.

#### Organisational Readiness

Organisational readiness measures whether the people who perform this workflow will adopt the agent's output or resist it. A technically excellent agent that the team ignores — or shadow-processes manually — is a failed automation.

Assess this on a gradient, not as a binary pass/fail:

1. **Has the team been consulted?** If the people who currently run this workflow do not know automation is being considered, you are at a 1 or 2 regardless of their likely reaction. Consultation is a prerequisite for buy-in.
2. **Where did the idea originate?** If the team themselves asked for automation, score 5. If it came from management or an outside stakeholder with no team input, score 2–3 depending on the team's general attitude toward tooling changes.
3. **What is the team's track record with new tools?** A team that adopted their last three tool changes smoothly scores higher than a team still resisting a change from two years ago.

Organisational readiness is not a permanent score — it can be improved. A team scoring 2 today can move to 4 after a pilot that demonstrates the agent's output alongside their manual process. But the score reflects *where they are now*, not where they could be after change management effort you have not yet done.

??? example "Scoring three candidates dimension by dimension"

    Walk through the scoring for three workflows — one from each role — to see how the same framework produces different scores for different candidates.

    **The candidates:**

    - **CSM — Renewal Preparation:** Trigger: 90 days before renewal. Pull usage data, assess health, compile risk factors, draft renewal brief. 4 hours per occurrence, monthly across portfolio.
    - **BA — Sprint Planning Prep:** Trigger: 2 days before sprint planning. Review backlog, check dependencies, compile velocity, draft capacity recommendation. 2 hours per occurrence, every 2 weeks.
    - **SE — Release Notes Compilation:** Trigger: release branch cut. Pull merged PRs, categorise changes, extract user-facing items, draft notes. 1.5 hours per occurrence, bi-weekly.

    **Impact — applying the formula:**

    | Candidate | Time | Frequency | Instances | Monthly hrs | Score |
    |---|---|---|---|---|---|
    | Renewal Preparation | 4 hrs | ~1/month per account | 8 accounts | ~32 hrs | 5 |
    | Sprint Planning Prep | 2 hrs | 2/month | 1 team | ~4 hrs | 3 |
    | Release Notes Compilation | 1.5 hrs | 2/month | 1 repo | ~3 hrs | 3 |

    Renewal Preparation dominates on Impact because of the instance multiplier — the per-account repetition turns a moderate time cost into a large one. The other two lack that multiplier.

    **Feasibility — checking data access:**

    | Candidate | Sources | Access Assessment | Score |
    |---|---|---|---|
    | Renewal Preparation | CRM, support platform, usage analytics, **contract system** | CRM and support have APIs. Usage analytics exportable. Contract system has no confirmed API — critical data requires manual lookup. | 3 |
    | Sprint Planning Prep | Jira, CI/CD metrics, team calendar | All three have well-documented APIs. | 5 |
    | Release Notes Compilation | Git history, PR metadata, issue tracker | All accessible via standard APIs (GitHub/GitLab). | 5 |

    Notice how Renewal Preparation's single inaccessible source — the contract system — pulls the entire Feasibility score down. The contract data is not optional; it is central to the workflow.

    **Risk Tolerance — assessing blast radius:**

    | Candidate | Who sees it? | Reversible? | Score |
    |---|---|---|---|
    | Renewal Preparation | Renewal brief informs commercial conversations with the client. Reviewed internally, but errors could affect negotiation positioning. | Errors in risk assessment could lead to under-preparing for a difficult renewal. | 3 |
    | Sprint Planning Prep | Internal team document. Reviewed in planning meeting before any commitments are made. | Easily corrected during the meeting itself. | 5 |
    | Release Notes Compilation | Published externally to users. Reviewed by team before publishing. | Errors are visible but correctable with an update. | 4 |

    Sprint Planning Prep scores highest because the output never leaves the team and gets validated in real-time during the planning session. Renewal Preparation scores lowest because errors in risk assessment have commercial consequences, even with a review step.

    **Complexity — counting decision points and data sources:**

    | Candidate | Decision Points | Data Sources | Score |
    |---|---|---|---|
    | Renewal Preparation | Risk factor weighting requires judgement at each factor. Assessment criteria may vary by account tier. | CRM, support platform, usage analytics, contract system (4 sources). | 3 |
    | Sprint Planning Prep | Capacity recommendation follows from velocity data and known constraints. Few conditional paths. | Jira, CI/CD metrics, team calendar (3 sources). | 4 |
    | Release Notes Compilation | Categorisation rules are well-defined. The flow is entirely linear: pull, categorise, draft. | Git history, PR metadata, issue tracker (3 sources). | 5 |

    Release Notes Compilation scores highest because the entire flow is linear — there are no points where the agent needs to choose between different paths. Sprint Planning Prep has a small number of decision points (how to weight capacity against priority), but they are well-defined. Renewal Preparation scores lowest because risk assessment involves weighing multiple factors against each other, with the relative importance varying by account context.

    **Learning Value — what patterns transfer:**

    | Candidate | Reusable Pattern | Other Workflows It Unlocks | Score |
    |---|---|---|---|
    | Renewal Preparation | Data gathering + risk assessment + structured brief | QBR prep, account health reviews, expansion opportunity analysis | 4 |
    | Sprint Planning Prep | Metrics compilation + capacity analysis + recommendation | Retrospective prep, resource planning, project status reports | 3 |
    | Release Notes Compilation | Data extraction + categorisation + formatted output | Changelog generation, deployment summaries, compliance reports | 3 |

    Renewal Preparation scores highest on Learning Value because the "gather from multiple sources, assess against criteria, produce a structured brief" pattern is the most common workflow shape in knowledge work. Sprint Planning Prep and Release Notes Compilation each transfer to a few similar workflows but with more role-specific patterns that generalise less broadly.

    **Organisational Readiness — assessing adoption appetite:**

    | Candidate | Consulted? | Attitude | Score |
    |---|---|---|---|
    | Renewal Preparation | CSM owns the workflow personally but has not discussed automation with the commercial team that acts on the renewal brief. | Neutral — no resistance, but no buy-in from downstream stakeholders. | 3 |
    | Sprint Planning Prep | The scrum team has raised the overhead of planning prep in retrospectives. The scrum master has asked whether parts of it can be automated. | Championed — the request came from the team. | 5 |
    | Release Notes Compilation | Engineering team is supportive. The tech lead has encouraged automation of "toil" tasks including release notes. No downstream resistance. | Actively supported by the team that runs it. | 4 |

    Sprint Planning Prep scores highest because the automation request originated from the team — the strongest possible adoption signal. Release Notes Compilation scores well because the engineering team is on board and views it as toil reduction. Renewal Preparation scores neutral because while the CSM wants it, the commercial stakeholders who depend on the renewal brief have not been consulted about an agent producing it.

    **The composite picture:**

    | Candidate | Impact | Feas. | Risk | Compl. | Learn. | Org. | Composite |
    |---|---|---|---|---|---|---|---|
    | Renewal Preparation | 5 | 3 | 3 | 3 | 4 | 3 | **3.65** |
    | Sprint Planning Prep | 3 | 5 | 5 | 4 | 3 | 5 | **4.20** |
    | Release Notes Compilation | 3 | 5 | 4 | 5 | 3 | 4 | **4.00** |

    The highest-impact workflow (Renewal Preparation) does not win. Sprint Planning Prep pulls ahead at 4.20, with Release Notes Compilation at 4.00 — both score higher than Renewal Preparation because their feasibility, risk, and organisational readiness profiles are stronger. The 0.20-point gap between the top two puts them within tiebreaker range (see [Comparing Close Candidates](#comparing-close-candidates) below). This is the framework doing its job — steering you toward the candidates most likely to succeed on your first build.

### Weighted Composite Score

Calculate the final score using these weights:

| Criterion | Weight |
|---|---|
| Impact | 30% |
| Feasibility | 25% |
| Risk Tolerance | 20% |
| Complexity | 10% |
| Learning Value | 5% |
| Organisational Readiness | 10% |

**Formula:** `(Impact x 0.30) + (Feasibility x 0.25) + (Risk Tolerance x 0.20) + (Complexity x 0.10) + (Learning Value x 0.05) + (Org Readiness x 0.10)`

Pick the workflow with the highest composite score. If two workflows score within 0.5 points of each other, see [Comparing Close Candidates](#comparing-close-candidates) below.

#### Adjusting Weights for Your Context

The default weights are not arbitrary — they encode priorities for a first build:

- **Impact (30%)** is highest because measurable time savings are what justify the effort to stakeholders and sustain your motivation through the build.
- **Feasibility (25%)** is second because inaccessible data is a hard blocker. No amount of clever design overcomes a system with no API and no export.
- **Risk Tolerance (20%)** is third because a forgiving failure mode gives you room to iterate. First builds produce imperfect output — you need space to improve without consequences.
- **Complexity (10%)**, **Organisational Readiness (10%)**, and **Learning Value (5%)** are lower because they influence success but rarely prevent it outright.

These defaults work for most teams selecting their first automation. But if your organisational context shifts one of the underlying assumptions, adjust the weights to match. Two constraints apply:

1. **Weights must sum to 100%.** Every point you add to one dimension must come from another.
2. **Impact and Feasibility should remain the two heaviest dimensions.** They represent "is it worth building?" and "can it be built?" — the two questions that matter most regardless of context.

??? example "Three scenarios where you should adjust weights"

    **Regulated environment (finance, healthcare, legal)**

    Compliance violations carry penalties that dwarf time savings. Increase Risk Tolerance to **25–30%** and reduce Learning Value to **0–5%** accordingly. The reasoning you present to stakeholders: *"In our context, the cost of a wrong output is disproportionately high, so we need to weight risk avoidance more heavily than reusable patterns."*

    | Criterion | Default | Adjusted |
    |---|---|---|
    | Impact | 30% | 30% |
    | Feasibility | 25% | 25% |
    | Risk Tolerance | 20% | **30%** |
    | Complexity | 10% | 10% |
    | Learning Value | 5% | **0%** |
    | Org Readiness | 10% | **5%** |

    **Severe resource constraints (small team, no developer support)**

    When you are building the agent yourself with no engineering help, complex workflows stall. Increase Complexity to **20%** and reduce Impact to **25%** and Learning Value to **0%**. The reasoning: *"We do not have the capacity to iterate through a complex build, so we need to weight simplicity more heavily even if it means less time saved."*

    | Criterion | Default | Adjusted |
    |---|---|---|
    | Impact | 30% | **25%** |
    | Feasibility | 25% | 25% |
    | Risk Tolerance | 20% | 20% |
    | Complexity | 10% | **20%** |
    | Learning Value | 5% | **0%** |
    | Org Readiness | 10% | 10% |

    **Change-resistant organisation (history of failed tool adoptions)**

    If your teams have a pattern of rejecting new tools, a technically perfect agent that nobody uses is worse than a mediocre one that gets adopted. Increase Organisational Readiness to **20%** and reduce Complexity to **5%** and Learning Value to **0%**. The reasoning: *"Our biggest risk is not technical failure — it is adoption failure. We need to weight team buy-in more heavily."*

    | Criterion | Default | Adjusted |
    |---|---|---|
    | Impact | 30% | 30% |
    | Feasibility | 25% | 25% |
    | Risk Tolerance | 20% | 20% |
    | Complexity | 10% | **5%** |
    | Learning Value | 5% | **0%** |
    | Org Readiness | 10% | **20%** |

Document your adjusted weights and rationale in the Selection Decision Record. If you are advising multiple teams, each team may use different weights — that is expected. The scoring framework is the constant; the weights are the variable you tune to context.

### Comparing Close Candidates

When two workflows score within 0.5 points of each other — as Sprint Planning Prep (4.20) and Release Notes Compilation (4.00) did in the scored example above, separated by 0.20 points — the composite score alone will not decide for you. Use these tiebreakers in order:

1. **Prefer higher Feasibility.** A workflow you cannot connect to is a workflow you cannot build. If one candidate has clean data access and the other has a question mark, pick the clean one.
2. **Prefer higher Risk Tolerance.** For your first build, forgiving failure modes matter more than raw impact. You want room to iterate without consequences.
3. **Prefer the workflow you run sooner.** If both candidates are still tied, pick the one with a nearer next occurrence. You will be able to test the agent against a real run sooner, which accelerates learning.

If the candidates are still tied after all three tiebreakers, it genuinely does not matter which you pick. Flip a coin and start building — the decision cost of deliberating further exceeds the difference in outcomes.

??? example "Before and After: Gut Feel vs. Framework"

    The most common selection mistake is picking the workflow that excites you rather than the one the framework recommends. Here is what that looks like.

    **The scenario:** A Business Analyst has scored four candidate workflows:

    | Candidate | Impact | Feas. | Risk | Compl. | Learn. | Org. | Composite |
    |---|---|---|---|---|---|---|---|
    | Stakeholder Progress Report | 4 | 4 | 4 | 4 | 4 | 3 | **3.90** |
    | Production Incident Analysis | 5 | 4 | 2 | 2 | 3 | 2 | **3.45** |
    | New Feature Request Intake | 3 | 5 | 5 | 5 | 3 | 4 | **4.20** |
    | Requirements Doc Generation | 4 | 3 | 4 | 3 | 5 | 3 | **3.60** |

    **:octicons-x-16: The gut-feel pick: Production Incident Analysis**

    *"This is the workflow that causes me the most pain. When a P1 hits, I spend hours pulling data from five systems while everyone is stressed. If I could automate even part of this, it would be a huge win. Plus, it would be impressive to demo."*

    The reasoning is emotionally compelling but ignores three critical scores. Risk Tolerance is 2 — incident analysis directly informs remediation decisions during an active outage, and a wrong assessment makes things worse. Complexity is 2 — each incident follows a different investigation path, meaning the agent needs to handle high ambiguity. Organisational Readiness is 2 — the on-call team has not been consulted and views their incident process as requiring human judgement. The composite score of 3.45 ranks it last.

    **:octicons-check-16: The framework pick: New Feature Request Intake**

    The framework points to the workflow with the highest composite score (4.20). It is not the most exciting candidate, but it has the strongest overall profile: all data sources have clean APIs (Feasibility 5), the output is reviewed before any decisions are made (Risk Tolerance 5), and the flow is linear with well-defined steps (Complexity 5). Impact is moderate (3) — it saves less time than the other candidates — but the near-certainty of a successful first build outweighs the time-savings gap.

    **Why this matters:** A failed first build does not just waste time — it erodes your confidence in the framework and makes you less likely to attempt the second build. The framework optimises for first-build success because success compounds. Once Feature Request Intake is working, you have a proven pattern and the confidence to tackle Stakeholder Progress Report next.

    **The same trap from a CSM perspective:** CSMs are especially prone to a variant of this mistake — picking the workflow that causes the most *client-facing pain* rather than the most feasible one. Imagine a CSM looking at Renewal Preparation (high impact from the per-account multiplier) alongside a simpler workflow like Health Report Data Gathering. The renewal workflow feels urgent — a botched renewal has real commercial consequences. But that urgency is exactly what makes it a poor first build: the stakes are higher (lower Risk Tolerance), the contract system may lack an API (lower Feasibility), and the pressure to get it right leaves no room for the iterative learning a first build requires. Start with the workflow where mistakes are cheap and data access is clean. Use that win to build toward the high-stakes workflow.

    **The same trap from an SE perspective:** Engineers tend toward the opposite variant — picking the most *technically interesting* workflow rather than the most feasible one. An engineer looking at Automated Deployment Rollback (complex branching logic, monitoring integration, real-time decision making) alongside CI Pipeline Report Generation (gather test results, build metrics, format into a summary) will gravitate toward the rollback workflow. It is a harder engineering problem, and solving it would be impressive. But the complexity score is 2 (dozens of conditional paths), the risk tolerance is 1 (a bad rollback decision during an active deploy has immediate production impact), and the monitoring integrations may require access to PagerDuty and Datadog APIs that the agent cannot reach directly. CI Pipeline Report Generation is linear, low-risk, and uses GitHub APIs that are already well-documented — it is the textbook first-build candidate. Build the boring one first; it earns you the credibility and patterns to tackle the interesting one next.

### When NOT to Automate

Before finalising your selection, check these disqualifiers:

- The workflow's value comes from the *relationship* built during the process, not the output
- Stakeholders would react negatively to knowing an agent was involved
- The data sources are locked behind systems with no API and no export
- The workflow changes shape significantly each time (low structural repeatability)
- The team that performs this workflow is actively hostile to automation **and** refuses to engage after consultation (Organisational Readiness score 1). Mild scepticism or a lack of enthusiasm (score 2–3) is not a disqualifier — it signals a need for a pilot and stakeholder engagement, not a veto. Score this gradient using the Organisational Readiness dimension above

If any of these apply to your top-scoring workflow, move to the next highest scorer.

??? example "Disqualifiers in practice — workflows that should not be automated"

    Each disqualifier targets a different structural reason. These workflows may be among the most valuable things you do — but they resist automation for reasons that no amount of engineering can overcome.

    **CSM — Executive Business Review Facilitation**

    The EBR meeting itself — presenting to the customer's leadership, reading the room, pivoting the conversation when an executive raises an unexpected concern — scores high on Impact and Learning Value. But the workflow's value comes from the *relationship* built during the process, not the output. A customer who learns their strategic review was assembled and presented by an agent will question whether their account is a priority. The deliverable is the conversation, not the deck.

    **Disqualifier:** *"The workflow's value comes from the relationship built during the process, not the output."*

    Note: the prep work leading up to the EBR — data gathering, slide generation, talking points — is a separate workflow and an excellent automation candidate. Decompose before you disqualify.

    **BA — Stakeholder Negotiation and Prioritisation Sessions**

    When competing priorities need resolution — two product managers want conflicting features in the same sprint, or a technical debt initiative conflicts with a revenue commitment — the BA facilitates a negotiation session. This involves reading political dynamics, knowing which stakeholder will compromise, and framing trade-offs in language each party accepts. An agent could gather the data inputs from Jira and Confluence (capacity, dependencies, revenue impact from the roadmap), but the facilitation itself depends on organisational context that no data source captures.

    **Disqualifier:** *"Stakeholders would react negatively to knowing an agent was involved"* and *"the workflow's value comes from the relationship built during the process."*

    **SE — Production Incident Response (Active Incident)**

    During a P1 outage, the on-call engineer is diagnosing in real time — checking Datadog dashboards, reading application logs, correlating recent deploys in the CI/CD pipeline, coordinating with other teams via PagerDuty and Slack. The workflow changes shape every time depending on symptoms. A monitoring alert that looks like a database issue may turn out to be a DNS failure. The engineer's value is in rapid hypothesis testing, not following a predetermined flow. An agent that adds processing latency between detection and response — even a few minutes — is actively harmful when the SLA clock is running.

    **Disqualifier:** *"The workflow changes shape significantly each time"* and the implicit constraint: when processing latency itself is a risk, the agent's execution time is a disqualifier even if the output would be correct.

    Note: post-incident analysis (after the incident is resolved) is a different workflow entirely — structured, repeatable, and an excellent automation candidate.

    **BA — Compliance Audit Preparation (Finance Team)**

    The BA has identified the quarterly compliance audit prep as a strong automation candidate — it scores well on Impact (20+ hours per quarter across document gathering, cross-referencing, and formatting) and Feasibility (all source systems have APIs). But the finance team was not consulted. They have performed this workflow manually for years, the senior auditor views the manual review as a quality safeguard, and the team lead has expressed scepticism about "AI touching compliance." Even with a technically sound agent, the finance team will not trust its output, will re-do the work manually as a shadow process, and the automation will quietly die.

    **Disqualifier:** Organisational Readiness score 1 — active resistance with no willingness to engage.

    Note: this is a sequencing problem, not a permanent disqualifier. The finance team's resistance places this at Organisational Readiness 1 today, but it is not fixed. If the BA runs a pilot with the finance team — showing the agent's output alongside their manual output for one cycle — and the team sees it working, resistance often dissolves. That moves the score to 3 or 4. Consult first, build second.

!!! example "See it in practice"
    - [Customer Success Manager — Quarterly Account Health Review](../worked-example/select.md)
    - [Business Analyst — New Feature Request Intake](../worked-example-ba/select.md)
    - [Software Engineer — Release Notes Compilation](../worked-example-se/select.md)

!!! tip "Need approval before proceeding?"
    Use the [Business Case template](../personalise/business-case.md) to package your Stage 1-2 findings into a one-page investment case for your manager.

---

## Guiding Questions

??? question "Guiding Questions"

    - Which workflow would save you the most time if it ran itself?
    - Which workflow has the most forgiving failure mode (internal deliverable, reviewable output)?
    - Which workflow would teach you patterns you can reuse across your other workflows?
    - Are you picking this workflow because it's genuinely the best candidate, or because it's the most interesting to build?
    - If the agent produced a mediocre output, could you fix it faster than doing the whole thing manually?
    - Has the team that currently performs this workflow been consulted? Would they use the agent, or work around it?

---

## Common Mistakes

!!! warning "Common Mistakes"

    - **Picking the most impressive workflow instead of the most feasible one.** Your first agentic workflow is a learning exercise. Optimise for success, not spectacle.
    - **Ignoring the "When NOT to Automate" list.** If the workflow's value is in the human relationship it builds, automating it destroys the thing that makes it valuable.
    - **Skipping the weighted scoring and going with gut feel.** The scoring framework exists to counteract the bias toward novelty. Use it.

---

## Next Step

With your workflow selected and justified, move to [Stage 3: Scope](03-scope.md) to map the workflow in detail and draw the automation boundary.
