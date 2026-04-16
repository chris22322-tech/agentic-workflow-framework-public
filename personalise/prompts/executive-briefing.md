# Executive Briefing Generator

You are producing a 1-2 page executive summary from a completed application
guide. The audience is a director or VP who needs to understand what the team
is doing with the Agentic Workflow Framework and why — in under 5 minutes of
reading.

## Inputs

1. **Application guide**: Read `personalise/output/APPLICATION-GUIDE.md` for the
   complete analysis.
2. **Organisation config**: Read `personalise/org-config.yaml` for organisation
   context.

If running in interactive mode, the user will paste these contents into the
conversation.

## Output Structure

Produce a concise executive briefing with exactly four sections:

### What the framework does

3 sentences maximum. Plain-language explanation of the Agentic Workflow Framework
and the personalisation approach. No jargon. A non-technical executive should
understand this paragraph without any prior context.

### What we would use it for

The top 3 workflows identified as quick wins from the application guide. For
each workflow:
- Workflow name and which role owns it
- What the workflow involves today (manual steps, time cost)
- Estimated time savings per month with automation

Present as a table for easy scanning.

### What we need to start

- **Time commitment**: How many hours per role in the first month
- **System access**: Which APIs or integrations are required
- **Approvals needed**: Any compliance, legal, or stakeholder sign-offs
- **Cost**: Estimated LLM API costs for the first quarter

### What happens if we don't

The risk of ad hoc AI usage without guardrails:
- Inconsistent quality across team members using AI differently
- No governance over what data enters LLM prompts
- Duplicated effort as individuals build one-off solutions
- Shadow AI proliferation — tools adopted without security review
- Missed opportunity to capture institutional knowledge in reusable agents

Frame this as organisational risk, not fear. The point is that structured
adoption is better than unstructured adoption — and unstructured adoption is
already happening.

## Output

- **CLI mode**: Write to `personalise/output/EXECUTIVE-BRIEFING.md`
- **Interactive mode**: Output in the conversation

## Quality Standards

- Maximum 2 pages when rendered as a document
- Use the organisation's actual name, role titles, and system names throughout
- Numbers and time estimates must come from the application guide — do not
  invent figures
- Tone: professional, direct, not salesy. This is an internal document, not
  a pitch deck
