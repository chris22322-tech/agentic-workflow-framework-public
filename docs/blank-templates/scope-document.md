# Workflow Scope Document Template

Output artifact for [Stage 3: Scope](../stages/03-scope.md).

Map the chosen workflow in full detail, then tag each step with an automation boundary.

[:material-download: Download scope spreadsheet](../downloads/scope-document.xlsx){ .md-button .md-button--primary }

The spreadsheet has four tabs matching the sections below: Workflow Map (with boundary dropdowns), Data Inventory, Integration Requirements, and Constraints & Assumptions.

---

## 1. Step-by-Step Workflow Map

Write each step as if instructing a new hire who has never done this before. Be specific — if a step feels vague, break it down further. Aim for 8+ steps.

| # | Step | Action | Input | Output | Decision Logic | Time (est.) | Actor | Boundary |
|---|---|---|---|---|---|---|---|---|
| 1 | *e.g., Pull account data* | *What you physically do* | *What information you consume* | *What this step produces* | *Criteria for any choices made* | *e.g., 5 min* | *e.g., CSM* | *AUTOMATE / HIL / MANUAL* |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |
| 6 | | | | | | | | |
| 7 | | | | | | | | |
| 8 | | | | | | | | |

!!! tip "Actor Column"
    Include for workflows involving handoffs between roles — it reveals where approval gates, notification triggers, and data handoffs need to be specified. For single-actor workflows where one person executes every step, leave it blank or remove the column.

!!! info "Boundary Tags"
    - **AUTOMATE** — Data retrieval, data transformation, or template-based generation. The agent handles this fully.
    - **HUMAN-IN-THE-LOOP (HIL)** — The agent does 80% of the work (drafts, flags, proposes); a human reviews and approves before proceeding.
    - **MANUAL** — Stays fully human. Relationship context, political sensitivity, or high-consequence decisions the agent cannot evaluate.

    Err toward more human involvement in early versions. Push the boundary outward as trust builds.

---

## 1b. Error Path Register

For each step where failure changes what downstream steps see, skip, or produce, document the failure mode here. One row per failure condition — a single step may have multiple. See [Mapping Error and Edge Case Paths](../stages/03-scope.md#mapping-error-and-edge-case-paths) for guidance.

| Step | Failure Category | Error Condition | Downstream Impact | Fallback Behaviour |
|---|---|---|---|---|
| *e.g., 2 — Pull support tickets* | *Data unavailable* | *API returns 503 after 3 retries* | *Steps 3, 7 lack ticket data* | *Flag gap, continue with other sources* |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

!!! tip "When to add rows"
    Focus on steps where failure changes downstream behaviour — cascading impacts, degraded outputs, or skipped steps. Pure data transformations with validated inputs can usually be omitted. Expect 5–8 rows for a typical 10-step workflow.

---

## 1c. Decision Point Register

Extract every step from the Workflow Map that has a non-trivial Decision Logic entry (criteria-based or contextual judgement — skip the "None" entries). This consolidates decision criteria for stakeholder review, boundary validation, and traceability into Design and Build. See [Decision Point Register](../stages/03-scope.md#decision-point-register) for guidance.

| Step | Decision Type | Criteria | Boundary Tag | Downstream Impact |
|---|---|---|---|---|
| *e.g., 3 — Calculate ticket health metrics* | *Criteria-based* | *The specific criteria, thresholds, or reasoning framework from the Decision Logic column* | *AUTOMATE / HIL / MANUAL* | *Which downstream steps, design decisions, or config rules depend on this decision* |
| | | | | |
| | | | | |
| | | | | |

!!! tip "Filling in the Boundary Tag column"
    Leave the Boundary Tag column blank until you have completed boundary tagging in the Workflow Map. Then fill in each row to link the decision to its automation boundary. The register makes review efficient — a stakeholder can validate all decision criteria in one table without reading the full workflow map.

---

## 1d. Future-State Summary *(optional)*

A two-column comparison showing what the human's workflow looks like after the agent is deployed. Derived from your boundary tags. See [Future-State Summary](../stages/03-scope.md#future-state-summary) for guidance.

| What the human does today | What the human does with the agent |
|---|---|
| *Describe current step(s) from the human's perspective* | *What changes — removed, reduced to review, or unchanged* |
| | |
| | |
| | |
| | |

Derive each row from your boundary tags:

- **AUTOMATE** steps → the agent handles this; the human no longer does it
- **HUMAN-IN-THE-LOOP** steps → the agent prepares; the human reviews or approves
- **MANUAL** steps → unchanged; the human still owns this step

!!! tip "Include time estimates"
    Add time estimates to the "with the agent" column where possible. "Review agent-drafted summary (5 min)" versus "Write summary from scratch (30 min)" communicates value immediately. Include a net-effect line at the bottom summarising total time saved.

---

## 2. Data Inventory

Every input the workflow consumes.

| Data Source | Access Method | Format | Auth Required | Notes |
|---|---|---|---|---|
| *e.g., CRM (Salesforce)* | *e.g., REST API* | *e.g., JSON* | *e.g., OAuth token* | *e.g., Need account read permissions* |
| | | | | |
| | | | | |
| | | | | |

---

## 3. Integration Requirements

What is needed to connect the agent to the systems and data sources listed above.

- **Agent framework or platform:** *whichever your team has chosen — see [Choose a Platform](../getting-started/choose-a-platform.md) for current options*
- **Language model provider:** *whichever model provider your platform supports*
- **Tool wrappers needed:** ___
- **Credentials management:** ___
- **Output format:** ___

### 3b. Downstream Integration

What processes does this workflow's output feed into? What systems need to be updated with the results? See [Downstream Integration](../stages/03-scope.md#downstream-integration) for guidance.

| Workflow Output | Downstream Process | Target System | Integration Method | Trigger Condition |
|---|---|---|---|---|
| *e.g., Health score (Red/Yellow/Green)* | *e.g., Risk escalation playbook* | *e.g., Gainsight* | *e.g., API — update healthScore field* | *e.g., Score is Red or dropped 2 levels* |
| | | | | |
| | | | | |
| | | | | |

!!! tip "Not just APIs"
    If the downstream handoff is currently manual (you read the report and create a CTA by hand), document it anyway. It tells you whether to automate the handoff or keep it as a manual step in your agent design.

---

## 4. Constraints and Assumptions

What must be true for this workflow to work as designed. Walk your workflow map against each category below — if a diagnostic question reveals a dependency, state the specific value you are assuming.

**Entity cardinality:** Does any step operate on a single entity that could, in production, be multiple? (e.g., one product per account, one contact per deal)

:   ___

**Temporal / frequency:** Does any step assume data is current as of a specific window, or that the workflow runs at a specific cadence?

:   ___

**Access / permissions:** Does any step assume the agent can read or write data that might require elevated permissions, user consent, or manual export?

:   ___

**Stability / change rate:** Does any step depend on a schema, scoring framework, or business rule that could change mid-quarter?

:   ___

**Processing model:** Does any step assume sequential processing that could encounter parallel, batched, or out-of-order inputs?

:   ___

**Data sensitivity / governance:** Does any step send client data, PII, or commercially sensitive information to an external service — including the LLM provider? Has the organisation's AI data processing policy been reviewed and approved for this data category?

:   ___

---

## 5. Stakeholders and Approvals

Who commissioned this analysis, who owns the workflow being automated, and who needs to sign off before build begins.

**Sponsor / Requestor:** ___

**Workflow Owner(s):** ___

| Name | Role | Consulted | Date | Outcome / Notes |
|---|---|---|---|---|
| *e.g., J. Smith* | *e.g., CS Team Lead* | *Y* | *e.g., 2025-03-15* | *Agreed boundary tags for steps 4–6* |
| | | | | |
| | | | | |
| | | | | |

**Sign-off:**

- [ ] Sponsor confirms automation scope and boundary decisions
- [ ] Workflow owner confirms step-by-step map is accurate
- [ ] Impacted teams have been consulted (rows above)
- [ ] Ready for handoff to engineering / agent build

!!! tip "Keep it lightweight"
    This is not a governance exercise — it is a record that the right people saw the scope before you started building. If a boundary decision gets challenged later, you can point here.

---

## 6. Compliance Readiness

!!! warning "Start these conversations at Stage 1"
    Compliance and legal review is the longest lead-time item in regulated industries (8–12 weeks in financial services). Do not wait until your scope is complete. Initiate the conversations below during [Stage 1: Decompose](../stages/01-decompose.md) so that legal, compliance, and third-party risk reviews run in parallel with your scoping work — not after it.

### Pre-flight checklist

- [ ] **AI usage policy.** Does the organisation have an approved policy for using external LLM services? If not, who owns creating one, and what is their timeline?
- [ ] **Data classification for LLM processing.** What data categories will the agent send to the LLM provider? Map each to your organisation's data classification scheme (e.g., public, internal, confidential, restricted). Know which classifications are permitted for external processing *before* you finalise your data inventory.
- [ ] **Third-party risk assessment for the model provider.** Most regulated organisations require a vendor risk assessment before sending data to a new third-party service. Initiate this for the LLM provider (e.g., Anthropic, OpenAI) as early as possible — it typically requires security questionnaires, data processing agreements, and procurement review.
- [ ] **Model risk management (MRM) applicability.** Determine whether your organisation's MRM framework applies to agentic workflows. If the agent produces outputs that inform business decisions — risk scores, health ratings, recommendations — it may fall under model governance even though it is not a traditional statistical model. Engage your model risk team early to clarify scope.
- [ ] **Data processing impact assessment (DPIA).** If the workflow processes personal data or PII, determine whether a DPIA is required under your regulatory framework (GDPR, CCPA, or sector-specific rules). Start the assessment process before the agent design is finalised.
- [ ] **Regulator notification.** In some jurisdictions and sectors, deploying AI in customer-facing or decision-supporting processes requires notifying the regulator. Check whether this applies and what the lead time is.

### Status tracker

Record who owns each conversation, when it was initiated, and its current status. Update this table as conversations progress.

| Pre-flight Item | Status | Owner | Date Initiated | Target Completion | Notes |
|---|---|---|---|---|---|
| AI usage policy | *Not started / In progress / Complete* | | | | |
| Data classification for LLM processing | | | | | |
| Third-party risk assessment (model provider) | | | | | |
| Model risk management (MRM) applicability | | | | | |
| Data processing impact assessment (DPIA) | | | | | |
| Regulator notification | | | | | |

### Compliance artifacts — mapped to framework stages

The table below shows which framework stage produces the artifacts your compliance and legal teams will need to review. Use it to set expectations with those teams about when each artifact will be available.

| Compliance Artifact | What They Need | Which Stage Produces It |
|---|---|---|
| Data inventory with classification | Every data element the agent processes, its source, and its sensitivity classification | Stage 3 — [Data Inventory](#2-data-inventory) |
| Automation boundary documentation | Which decisions are automated vs. human-reviewed, and the criteria for each | Stage 3 — [Workflow Map](#1-step-by-step-workflow-map) and [Decision Point Register](#1c-decision-point-register) |
| Error handling and fallback behaviour | How the agent degrades gracefully and when it escalates to a human | Stage 3 — [Error Path Register](#1b-error-path-register), refined in Stage 4 |
| Agent architecture and data flow | How data moves through the system, where it is stored, and what is sent externally | Stage 4: Design |
