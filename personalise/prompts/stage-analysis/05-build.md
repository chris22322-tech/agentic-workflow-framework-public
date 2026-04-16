# Stage 5: Build — Organisation Analysis

You are analysing how a specific organisation would apply Stage 5 (Build) of
the Agentic Workflow Framework.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml`
2. **Stage documentation**: Read `docs/stages/05-build.md`

## What to Produce

### Build Environment Considerations

Based on the organisation's team capability:
- Recommended development setup and tooling
- CI/CD considerations for agent deployment
- Environment management (dev, staging, production)
- Secrets and credential management for their systems

### Integration Implementation Notes

For each system in the org config:
- Specific API endpoints and patterns relevant to their workflows
- Common pitfalls when integrating with this system
- Testing strategies (sandbox environments, test accounts, mock data)
- Rate limiting and retry patterns

### Organisation-Specific Build Concerns

- How to handle client-specific configuration if multi-tenant
- Data handling during development (test data vs production data)
- Compliance requirements for the build process itself (code review,
  security scanning, change management)
- Deployment patterns appropriate for their infrastructure

### Build Sequence Recommendation

Recommended order for building agents across roles:
- Which agent to build first and why (shared integrations, lowest risk)
- Dependency graph between agents
- Estimated build effort per agent (given their team capability)

## Output

Write a structured markdown report. An engineer starting the build phase should
be able to use your output as a practical companion guide.
