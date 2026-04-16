# Application Guide Generator

You are producing a tailored application guide for an organisation adopting the
Agentic Workflow Framework. You will read the organisation's config file and the
framework's stage documentation, then produce a comprehensive guide that is
specific to this organisation — naming their systems, roles, constraints, and
workflows throughout.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml` for the
   organisation's context, roles, systems, constraints, and goals.
2. **Framework stages**: Read all files in `docs/stages/` (01-decompose.md
   through 06-evaluate.md) to understand the full methodology.
3. **Getting started**: Read `docs/getting-started/index.md` for framework
   orientation.
4. **Templates**: Read `docs/blank-templates/index.md` for the artifact
   templates each stage produces.

If running in interactive mode (no file access), the user will paste these
contents into the conversation. Work with whatever is provided.

## Output Structure

Produce a single markdown document with the following sections. Every section
must reference the organisation's actual roles, systems, and constraints — not
generic placeholders.

### 1. Executive Summary

5-8 sentences. Cover:
- What the framework offers this specific organisation
- Which roles benefit most immediately and why
- What the quickest wins are (name specific workflows)
- What the biggest risks are (name specific constraints)
- A one-sentence recommended starting point

### 2. Recommended Rollout Plan

A phased approach:
- **Phase 1 (Month 1): Foundation** — who starts, what they do each week, what
  they produce. Include specific roles from the org config.
- **Phase 2 (Months 2-3): First Agent Build** — which workflow to build first
  and why (lowest risk, highest reuse of integrations). Include a build sequence
  for 3-4 workflows.
- **Phase 3 (Months 3-6): Expansion** — expanding across roles, across
  clients/teams, into adjacent workflows.

Include a timeline table with months, milestones, active roles, and key
deliverables.

### 3. Role-Specific Playbooks

For each role in the org config, produce a playbook containing:
- **Top 3 automation candidates** — name specific workflows with a brief
  description. Score each on the five signals from Stage 2 (volume, pattern
  consistency, data availability, quality requirements, current time cost).
- **Which stages they own vs collaborate on** — some roles lead Stages 1-3,
  others lead Stages 4-6.
- **Constraints that apply to this role** — data sensitivity, client-facing
  requirements, approval gates.
- **Recommended first workflow** — the single best starting point for this role,
  with justification.

### 4. Quick Wins

3-5 workflows that could be automated in the first quarter with high confidence
and low risk. For each:
- Workflow name and owning role
- Why it's a quick win (high volume, internal-only, data readily available, etc.)
- Estimated time savings per occurrence
- Systems involved
- Composite automation score (using the five signals)

### 5. Data Sensitivity Analysis

For each system in the org config:
- What data it contains
- Sensitivity classification (public, internal, confidential, restricted)
- Whether that data can be sent to external LLM APIs
- Recommended handling (direct API access, anonymisation, on-premise model, etc.)

If the org has regulatory constraints, map them to specific automation decisions.

### 6. Guardrails and Policies

What rules the organisation should establish before anyone starts automating:
- Data classification policy for LLM inputs
- Human review requirements by output type
- Client/stakeholder approval gates
- Quality baseline requirements (parallel run protocols)
- Incident response for automated output failures

### 7. Risk Register

Top 5-8 risks of adopting the framework, specific to this organisation. For each:
- Risk description
- Likelihood (High/Medium/Low)
- Impact (High/Medium/Low)
- Mitigation strategy
- Owner (which role)

### 8. Framework Enhancement Recommendations

What should be added to the framework to serve this type of organisation better.
Prioritised by impact. Be specific — suggest concrete additions, not vague
"add more guidance."

## Output

- **CLI mode**: Write the complete guide to `personalise/output/APPLICATION-GUIDE.md`
- **Interactive mode**: Output the complete guide in the conversation

## Quality Standards

- Name the organisation's actual systems, roles, and workflows throughout — never
  use generic placeholders like "your CRM" when the config says "Salesforce"
- Workflow suggestions must be realistic for the roles described — if a role
  "writes functional specifications", suggest automating spec drafting, not
  something unrelated
- Regulatory and compliance recommendations must reference the actual
  jurisdictions and constraints from the config
- The rollout plan must be actionable — a project manager should be able to turn
  it into a project plan without further research
- Score automation candidates using the five signals from Stage 2: volume/frequency,
  pattern consistency, data availability, quality requirements, current time cost
