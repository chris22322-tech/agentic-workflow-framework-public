# Worked Example: Stage 2 -- Select

!!! example "Worked Example"
    We're applying Stage 2 to: **the SE Workflow Inventory Table from Stage 1**. The goal is to choose a single workflow to automate -- the one most likely to succeed and deliver value.

## Completed Artifact: Selection Decision Record

### Chosen Workflow

**Release Notes Compilation & Publishing**

### Candidate Comparison

Three candidates rated High or Medium automation potential in Stage 1 were scored using the six-dimension framework. A fourth — Post-Mortem Compilation, rated Low in Stage 1 — is included to demonstrate how the disqualification criteria apply to engineering workflows:

| Candidate | Impact | Feas. | Risk Tol. | Compl. | Learn. | Org. | Composite |
|---|---|---|---|---|---|---|---|
| **Release Notes Compilation** | 4 | 5 | 4 | 5 | 4 | 4 | **4.35** |
| On-Call Rotation Handoff | 3 | 5 | 5 | 3 | 3 | 4 | 4.00 |
| PR Review Triage | 4 | 4 | 3 | 2 | 3 | 3 | 3.45 |
| Post-Mortem Compilation† | 3 | 3 | 3 | 2 | 2 | 3 | 2.85 |

**On-Call Rotation Handoff** scored well on Feasibility (5) and Risk Tolerance (5) — all monitoring and deployment systems have documented APIs, and the handoff document is reviewed by the incoming on-call engineer before they rely on it. But Impact scored only 3: at 1-2 hours weekly, it saves roughly 4-6 hours per month with no instance multiplier (you hand off one rotation, not ten). Strong on pragmatism, modest on payoff — the same profile as Sprint Planning Prep in the BA example.

†**Post-Mortem Compilation** was disqualified before composite ranking. Despite a non-trivial time cost (3-5 hours per post-mortem), it triggers the fourth disqualifier: the workflow changes shape significantly each time. A database outage post-mortem follows a different investigation path than a deployment rollback post-mortem. The contributing factors, the systems involved, and the remediation recommendations vary by incident. Two engineers would write meaningfully different post-mortems for the same incident because they weight different contributing factors. Low structural repeatability means the agent cannot reuse its analysis logic from one run to the next.

Note: the *data compilation* portion of post-mortem work — gathering the incident timeline from PagerDuty, Datadog, deploy logs, and Slack — was already split out as Incident Timeline Reconstruction in Stage 1, where it scored High. The disqualification applies to the interpretive layer: identifying root causes, assessing detection speed, and recommending preventive actions. Decompose before you disqualify.

### Selection Scores

| Criterion | Weight | Score (1-5) | Rationale |
|---|---|---|---|
| **Impact** | 30% | 4 | 3-4 hours per release at a biweekly cadence = ~7 hours per month for a single service. The agent handles the full compilation pipeline — fetching PRs, categorising changes, filtering to user-facing items, drafting formatted notes — leaving the engineer only the review step. No strong instance multiplier (most engineers own releases for 1-2 services), so this stays at 4 rather than reaching the >10 hrs/month threshold for a 5. |
| **Feasibility** | 25% | 5 | Every data source lives in a system with a well-documented API. GitHub provides PR metadata, commit history, labels, and milestones. The issue tracker (Jira or Linear) provides linked tickets and descriptions. CI/CD provides build status and test results. Previous release notes provide the format template. The agent is never asked to interpret unstructured communication or access a system without programmatic access. |
| **Risk Tolerance** | 20% | 4 | Release notes are reviewed by the engineering team before publishing. Errors in categorisation — miscategorising a bugfix as a feature, or missing a breaking change — are caught during that review. But the notes are published externally to users, which means an error that slips through review is visible. That external visibility keeps this at 4 rather than 5. |
| **Complexity** | 10% | 5 | The flow is entirely linear: fetch merged PRs since the last tag → categorise by type using labels → filter to user-facing changes → extract summaries → group and sort → draft formatted notes → review. No conditional branching, no dynamic routing. The categorisation step uses label-based rules with a commit-message fallback — deterministic logic, not judgement. Two engineers with the same PR list and the same rules would produce near-identical output. |
| **Learning Value** | 5% | 4 | The "data extraction → categorisation → formatted output" pattern transfers directly to changelog generation, deployment summaries, dependency update reports, and compliance documentation. Building this teaches you the core pattern: pull structured data from APIs, apply classification rules, produce a formatted deliverable. That pattern appears in at least 3-4 other workflows on the inventory. |
| **Organisational Readiness** | 10% | 4 | The engineering team views release notes as toil — necessary but tedious. The tech lead has actively encouraged automating repetitive tasks, and release notes was specifically mentioned. Users who receive release notes want better consistency, not less automation. No stakeholder has a reason to resist. |

### Weighted Score

**4.35** = (4 × 0.30) + (5 × 0.25) + (4 × 0.20) + (5 × 0.10) + (4 × 0.05) + (4 × 0.10)

### Justification

Release Notes Compilation combines a repeatable linear structure with universally accessible data sources and a forgiving failure mode. Every input is structured (PRs, labels, commits, linked issues), every system has a documented API, and every output is reviewed before publishing. The workflow operates entirely on metadata — reformatting and categorising data that already has structure — rather than interpreting what code changes mean. This makes it the cleanest possible target for a first build: the agent's job is data gathering and formatting, not judgement. The review-before-publish checkpoint means the engineer catches anything the agent gets wrong before users see it.

### Risks

Categorisation accuracy depends on PR labelling discipline. If the team does not consistently label PRs (feature, bugfix, breaking-change), the agent falls back to commit message parsing, which is noisier. PRs with vague titles ("misc fixes," "cleanup") and no labels will require the LLM to infer the change type from the diff description — a step that may miscategorise in both directions. Expect to iterate on the categorisation prompt, especially for edge cases like a PR that fixes a bug by adding a new feature.

Breaking change detection is the highest-stakes categorisation. A missed breaking change means users upgrade without knowing something will break. Label-based detection (`breaking-change` label) is reliable when the label is applied, but developers forget. The commit message fallback (`BREAKING:` prefix) catches some misses, but there is no substitute for the reviewer checking the breaking changes section specifically.

## Annotations

!!! note "Why Impact scored 4 and not 5"
    At 3-4 hours per release on a biweekly cadence, the arithmetic gives ~7 hours per month. That is solidly in the Score 4 range (6-10 hrs/month) but not the >10 hrs/month threshold for a 5. The difference between this and the CSM's Quarterly Account Health Review (Impact 5) is the instance multiplier. The CSM runs the same workflow for each of their 10 accounts — the per-account repetition turns 6-8 hours into 60-80 hours per quarter. The SE typically owns releases for 1-2 services, not ten. If you happen to manage releases for a microservices platform with 5+ independently versioned services, the instance multiplier would push this to a 5. For most engineers, it is a strong 4.

    This is a pattern worth noticing across the three worked examples. The CSM's Impact 5 comes from a per-account multiplier. The BA's Impact 4 comes from high frequency (3-5 per week). The SE's Impact 4 comes from moderate per-occurrence cost at moderate frequency. Same score, different arithmetic — which means different leverage points for increasing impact later.

!!! note "Why Feasibility scored 5 — and why engineering workflows have a structural advantage"
    Every data source in this workflow lives in a system designed to be programmatically accessed. GitHub's REST and GraphQL APIs expose PR metadata, commit history, labels, milestones, and linked issues. Jira and Linear have well-documented REST APIs. CI/CD systems (GitHub Actions, CircleCI, Jenkins) expose build and test results via API. This is not a coincidence — engineering tools are built by and for developers, which means API access is a first-class feature, not an afterthought.

    Compare this to the CSM's Feasibility 4, where Slack sentiment analysis was the weak link — retrieving threads is easy, but interpreting conversational tone is inherently noisy. Or the BA's Feasibility 5, which was notable because *all* business systems (Jira, Confluence, roadmap tools) happened to have APIs. For engineering workflows, API availability is closer to the default. If your workflow's data sources are Git, CI/CD, monitoring, and issue tracking, you are likely starting at Feasibility 4-5. The question is whether any step requires interpreting unstructured data (Slack conversations, meeting notes, design docs) — that is what drops the score.

!!! note "Why Complexity scored 5 — the metadata advantage"
    Complexity 5 means "linear or near-linear flow with few branches." Release notes compilation is the textbook example: every run follows the same sequence, and the categorisation step uses deterministic rules (label → category) rather than judgement. The decompose stage's [annotation](decompose.md) introduced the distinction between workflows that operate on *metadata* versus *meaning*. This is where that distinction pays off in the scoring.

    Release notes categorisation asks: "Does this PR have the `bugfix` label? Then it is a bugfix." That is a metadata operation. PR review triage asks: "Is this 10-line change to the payment service risky enough to need a senior reviewer?" That is a meaning operation — it requires understanding what the change *does*, not just what labels it carries. Metadata operations are deterministic and encodable as rules. Meaning operations require context and judgement. When your workflow's hardest step is a metadata operation, Complexity stays high.

!!! note "Why On-Call Rotation Handoff is the runner-up, not the winner"
    On-Call Rotation Handoff has an impressive pragmatism profile: Feasibility 5 (all systems have APIs), Risk Tolerance 5 (internal document, reviewed before reliance). That combination — the two dimensions that matter most for a first build — is as strong as Release Notes or stronger. What holds it back is Impact: 1-2 hours weekly translates to ~4-6 hours per month saved. There is no instance multiplier and no frequency multiplier beyond weekly.

    The runner-up story here is different from the CSM and BA examples. In the CSM example, the runner-up (Cross-team Standup Prep) was held back by low Impact and low Learning Value. In the BA example, the runner-up (Sprint Planning Prep) was held back by modest Impact. Here, On-Call Rotation Handoff would be a perfectly valid first build — it would just deliver less value. If your team's biggest pain point is the weekly handoff scramble, the 0.35-point gap from the winner is small enough that team motivation could be a reasonable tiebreaker.

!!! note "Why PR Review Triage scored lowest among the viable candidates — despite the highest frequency"
    PR Review Triage runs 3-5 times per day, dwarfing the frequency of every other candidate on the table. The intuition is that high frequency equals high impact — if you can save even 15 minutes per triage, that compounds to 5-8 hours per month. And the Impact score does reflect that: at 4, it ties Release Notes for the highest on the table.

    But Impact alone does not determine the winner. PR Review Triage's composite is dragged down by the dimensions that predict whether the agent can actually *do* the work. Complexity scored 2 — the data gathering (diff size, file paths, codeowners, CI status) is straightforward, but the *decision* (who reviews, how urgently, is this blocking a release) requires engineering context that lives in people's heads, not in any API. Risk Tolerance scored 3 — assigning the wrong reviewer does not cause a catastrophe, but it wastes a senior engineer's time on a trivial PR or leaves a critical change under-reviewed, and both erode team trust in the system. Organisational Readiness scored 3 — some engineers are protective of their review process and sceptical of automated assignment.

    The lesson: frequency is an Impact multiplier, not a success predictor. A workflow that runs 80 times a month but requires judgement on every run is harder to automate than a workflow that runs 4 times a month but follows the same deterministic path each time. The composite scoring captures this — high Impact cannot compensate for low Complexity and moderate Risk Tolerance.

!!! tip "The SE selection story — metadata over meaning"
    Each worked example teaches a different selection lesson. The CSM example teaches "pick the highest-impact workflow that is feasible" — the per-account multiplier made Quarterly Account Health Review the clear winner on Impact, and the other dimensions supported it. The BA example teaches "pick the workflow with the strongest overall profile" — New Feature Request Intake won not by dominating any single dimension but by having no score below 3.

    The SE example adds a third lesson, specific to engineering workflows: **the metadata/meaning distinction is the strongest predictor of automation success.** Release Notes Compilation operates on metadata — PR labels, commit messages, version tags, linked issue IDs. The agent retrieves structured data, applies classification rules, and produces formatted output. PR Review Triage operates on meaning — "is this change risky?" requires understanding what the code does, not just what labels it carries. On-Call Rotation Handoff sits in between — the data gathering is metadata, but the valuable parts of the handoff (what to watch out for, which alerts to ignore) are meaning.

    If you are an engineer evaluating your workflow inventory, ask this question for each candidate: *is the hardest step about retrieving and reformatting structured data, or about interpreting what that data means?* The answer will often predict the composite score before you calculate it.

---

[:octicons-arrow-left-24: Back to Stage 2: Select](../stages/02-select.md){ .md-button }
