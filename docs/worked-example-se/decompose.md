# Worked Example: Stage 1 -- Decompose

!!! example "Worked Example"
    We're applying Stage 1 to: **a Software Engineer (SE) role**. The goal is to break this role into a structured inventory of discrete, repeatable workflows — the kind of recurring engineering work that follows a pattern, not the creative problem-solving that makes every ticket different.

## Completed Artifact: Workflow Inventory Table

| Responsibility Area | Workflow | Trigger | Frequency | Avg Time (hrs) | Systems Touched | Output/Deliverable | Automation Potential |
|---|---|---|---|---|---|---|---|
| Release Management | **Release Notes Compilation & Publishing** | Release branch cut or tag created | Per release (biweekly to monthly) | 3-4 | GitHub (PRs, commits, labels), Issue tracker (Jira/Linear), CI/CD pipeline | Published release notes (Markdown) | High |
| Release Management | Release Readiness Checklist | Release candidate tagged | Per release | 2-3 | CI/CD pipeline, Test suite, Staging environment, Deploy config | Readiness report (go/no-go + blockers) | High |
| Release Management | Hotfix Deployment Coordination | Critical bug in production | Ad hoc (1-2x/month) | 1-2 | GitHub, CI/CD pipeline, PagerDuty, Slack | Deployed hotfix + comms to stakeholders | Medium |
| Code Quality | PR Review Triage | PR opened or review requested | Daily (3-5x/day) | 0.5-1 | GitHub, CI/CD (build status), Codeowners file, Slack | Assigned reviewers + priority label | Medium |
| Code Quality | Tech Debt Assessment | Quarterly planning or sprint boundary | Quarterly | 4-6 | GitHub (code search, issue backlog), SonarQube/linters, Architecture docs | Tech debt report with prioritised recommendations | Medium |
| Code Quality | Dependency Update Review | Dependabot/Renovate PR opened | Weekly (2-4x/week) | 0.5-1 | GitHub, npm/PyPI/Maven registry, CVE databases, CI/CD | Approved or flagged dependency PRs | High |
| Incident Management | On-call Rotation Handoff | Rotation changeover (weekly) | Weekly | 1-2 | PagerDuty, Incident tracker, CI/CD (deploy history), Slack | Handoff document | Medium |
| Incident Management | Post-mortem Compilation | Incident resolved (severity P1/P2) | Ad hoc (1-3x/month) | 3-5 | Incident tracker, PagerDuty, Datadog/Grafana, Slack, Git history | Post-mortem document | Low |
| Incident Management | Incident Timeline Reconstruction | Post-mortem scheduled | Ad hoc (tied to post-mortem) | 1-2 | PagerDuty, Datadog/Grafana, Deploy logs, Slack, Git history | Annotated timeline of events | High |
| Documentation | Runbook Maintenance | Service change deployed or post-mortem action item | Ad hoc (2-3x/month) | 1-2 | Wiki/Confluence, GitHub, Monitoring dashboards, Deploy config | Updated runbook | Low |
| Documentation | API Documentation Updates | Endpoint added, changed, or deprecated | Per feature (tied to PR merge) | 1-2 | OpenAPI spec, GitHub, API gateway config, Docs site | Updated API reference docs | Medium |
| Documentation | Architecture Decision Records (ADRs) | Significant design decision made | Ad hoc (1-2x/month) | 2-3 | Confluence/GitHub, Architecture docs, Meeting notes, Slack | Published ADR | Low |

## Workflow Dependencies

### Shared data sources

- Release Notes Compilation, Release Readiness Checklist, Hotfix Deployment Coordination share GitHub data source (PRs, commits, tags, labels, CI status)
- Release Notes Compilation, Dependency Update Review share CI/CD pipeline data (build status, test results, deployment history)
- Incident Timeline Reconstruction, Post-mortem Compilation, On-call Rotation Handoff share PagerDuty and monitoring data (alerts, incident history, deploy events)

### Sequential dependencies

- Release Readiness Checklist → Release Notes Compilation (go/no-go decision gates the release that triggers notes compilation)
- Incident Timeline Reconstruction → Post-mortem Compilation (annotated timeline is a required input to the post-mortem document)
- Post-mortem Compilation → Runbook Maintenance (post-mortem action items often trigger runbook updates)

### Independent workflows

- Dependency Update Review, PR Review Triage are independent of each other and of the release cycle — both operate on their own triggers (Dependabot PRs and review requests respectively)
- API Documentation Updates operates on its own per-feature trigger, independent of the release and incident workflows

## Annotations

!!! note "Why Release Notes Compilation scored High — and why we chose it"
    This workflow checks every box for High automation potential. (1) **Structurally repeatable** — every release follows the same sequence: pull merged PRs since the last tag, categorise by type (feature, bugfix, breaking change), filter to user-facing changes, draft formatted notes, get sign-off. The steps don't change; only the PRs do. (2) **Deterministic** — two engineers pulling the same PR list and applying the same label-based categorisation rules would produce near-identical output. There's no "it depends on how the sprint went" factor. (3) **Data available** — Git history, PR metadata, labels, linked issues, and CI status are all queryable via GitHub's API. Everything the workflow needs lives in structured, API-accessible systems. (4) **Errors recoverable** — the draft is reviewed by the team before publishing. A miscategorised PR gets caught in review, not in production. At 3-4 hours per release and a biweekly-to-monthly cadence, the individual time savings are meaningful but not the primary reason this scored High. The real value is consistency — release notes generated from PR metadata are more reliable than notes compiled by an engineer skimming a Git log at 5pm on release day. This is the workflow we carry through the remaining stages.

!!! note "Why Incident Timeline Reconstruction scored High but Post-mortem Compilation scored Low"
    These two workflows are often lumped together as "post-mortem work," but they have very different automation profiles. Timeline reconstruction is almost entirely data retrieval: pull alerts from PagerDuty in chronological order, correlate with deploy events from CI/CD, extract relevant Slack messages from the incident channel, and stitch them into an annotated timeline. Two engineers with the same data would produce the same timeline. Post-mortem compilation, by contrast, requires interpreting *why* things happened — identifying contributing factors, assessing whether the detection was fast enough, and recommending preventive actions. That interpretive work depends on system knowledge and engineering judgement that varies by engineer. Splitting the post-mortem process into these two workflows is an example of the [sub-workflow pattern](../stages/01-decompose.md#when-a-workflow-scores-medium-the-sub-workflow-pattern) — the High-scoring data compilation feeds into the Low-scoring analysis.

!!! note "Why PR Review Triage scored Medium, not High"
    PR review triage has strong structural repeatability — check the diff size, identify affected services from file paths, look up codeowners, check CI status, assign reviewers, set a priority label. That sounds mechanical. But the judgement layer is real: a 10-line change to the payment service needs a senior reviewer and fast turnaround; a 500-line refactor in a test utility can wait. Deciding *who* should review and *how urgently* depends on understanding which parts of the codebase are high-risk, who has context on the relevant module, and whether the PR is blocking a release. An agent could handle the data gathering and suggest reviewers based on codeowners, but the priority call requires engineering context that's hard to encode as rules.

!!! note "Why Dependency Update Review scored High despite being security-sensitive"
    At 30-60 minutes per occurrence, each individual dependency update is small. But at 2-4 updates per week, it compounds. The workflow scores High because it's almost entirely rule-based: check whether the update is a major/minor/patch version bump, scan the changelog for breaking changes, verify CI passes with the new version, check CVE databases for known vulnerabilities in the current version, and approve or flag. The decision criteria are explicit and documentable — "approve patch updates with passing CI," "flag major bumps for manual review," "reject any version with a known CVE above CVSS 7.0." The security sensitivity actually *supports* automation here: a rules-based check is more consistent than an engineer scanning changelogs at varying levels of attention across the week.

!!! note "Why ADRs scored Low despite being documentation"
    Not all documentation workflows are equal. Release notes (High) are about reformatting structured data that already exists. ADRs are about articulating *why* a design decision was made — capturing the alternatives considered, the trade-offs weighed, and the context that made one option preferable. Two engineers might write the same ADR very differently because they weight different trade-offs. The value of an ADR is in the reasoning, not the format. An agent could scaffold the template and pull in relevant context (related ADRs, linked tickets, architecture diagrams), but the core intellectual work — "we chose X over Y because Z" — is irreducibly human.

!!! tip "Pattern to notice"
    In engineering workflows, the line between High and Medium often comes down to **whether the workflow operates on metadata or on meaning**. Release notes compilation, dependency update review, and incident timeline reconstruction all operate on metadata — PR labels, version numbers, alert timestamps. They reorganise and reformat data that already has structure. PR review triage, tech debt assessment, and on-call handoffs require interpreting what the data *means* in context — which changes are risky, which debt is urgent, which alerts are worth worrying about. If the workflow is about moving structured data between systems, it's probably High. If it's about making a judgement call that depends on engineering context, it's probably Medium or Low.

---

[:octicons-arrow-left-24: Back to Stage 1: Decompose](../stages/01-decompose.md){ .md-button }
