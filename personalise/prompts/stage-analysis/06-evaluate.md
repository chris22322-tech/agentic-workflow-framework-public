# Stage 6: Evaluate — Organisation Analysis

You are analysing how a specific organisation would apply Stage 6 (Evaluate) of
the Agentic Workflow Framework.

## Inputs

1. **Organisation config**: Read `personalise/org-config.yaml`
2. **Stage documentation**: Read `docs/stages/06-evaluate.md`

## What to Produce

### Evaluation Criteria

For each role's automation candidates:
- What "good" looks like for their automated output (accuracy metrics,
  completeness checks, format requirements)
- How to compare automated vs manual output for this workflow
- Domain-specific quality criteria (industry standards, compliance requirements)

### Parallel Run Design

How to run the parallel evaluation period for this organisation:
- Duration recommendation based on workflow frequency
- Who reviews the automated output (role owner, manager, compliance)
- What constitutes a pass vs fail for each workflow
- How to handle automated output that requires client-facing review

### Organisation-Specific Evaluation Concerns

- Regulatory requirements for validating automated outputs
- Client approval requirements before switching from manual to automated
- Audit trail requirements for the evaluation period
- How to measure time savings accurately

### Go/No-Go Framework

Decision criteria for this organisation to move from parallel run to production:
- Quantitative thresholds (accuracy rate, time savings, error rate)
- Qualitative gates (stakeholder confidence, compliance sign-off)
- Rollback plan if production deployment fails

## Output

Write a structured markdown report. The team lead overseeing evaluation should
be able to use your output to design their parallel run protocol.
