# Cross-Cutting Themes — Organisation Analysis

You are analysing cross-cutting themes that affect how a specific organisation
would apply the Agentic Workflow Framework across all six stages.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml`
2. **Framework stages**: Read all files in `docs/stages/` for full context

## What to Produce

Analyse each of the following themes for this organisation. Skip any that do not
apply based on the org config.

### Role Interactions

- How the organisation's roles collaborate through the framework stages
- Where workflow ownership is shared or ambiguous
- Cross-role dependencies that affect automation sequencing

### Client/Stakeholder Boundary

- Which workflows produce outputs visible to external parties
- What approval gates exist at the client boundary
- How automation changes the client experience (positively or negatively)

### Compliance and Regulatory

- How the organisation's regulatory environment constrains automation decisions
- Which regulations affect which stages most heavily
- Specific compliance review gates to build into the process

### Data Sensitivity

- Classification of data flowing through each system in the org config
- What data can and cannot be sent to external LLM APIs
- Anonymisation, on-premise, or alternative approaches for sensitive data
- Data residency constraints and their impact on agent architecture

### Integration Landscape

- How the organisation's systems interconnect
- Single sign-on and authentication patterns across systems
- Data flow between systems that automated workflows would need to replicate

### Multi-Team/Multi-Client Patterns

- If applicable: how to reuse agents across teams, clients, or business units
- Configuration externalisation patterns
- Shared vs isolated infrastructure decisions

## Output

Write a structured markdown report covering each applicable theme. For each
theme, provide:
1. How it affects each framework stage
2. Role-specific implications
3. Concrete recommendations for policies, guardrails, or processes
4. Risk assessment — what could go wrong if this theme is ignored
