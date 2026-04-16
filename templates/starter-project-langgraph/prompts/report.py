"""
Report Generation Prompt Template
==================================
This prompt should implement the Prompt Pattern field from your Design
Document node specification for the output generation node.

This is a text-generation prompt — it produces human-readable output
(report, summary, email, etc.), NOT structured JSON. The output goes
to a human via a HIL checkpoint or to a downstream consumer.

Methodology reference:
  - Stage 3: Scope → Output / deliverable specification
  - Stage 4: Design → Node Spec "Prompt Pattern" field for generate_output
  - Stage 5: Build → LLM Generation Node pattern
"""

# ── Report Prompt ─────────────────────────────────────────────────────
# Variables filled by the generate_output node at runtime:
#   {input_id}       — The item this report covers
#   {input_context}  — Additional context
#   {analysis_json}  — JSON string of the analysis output
#   {human_feedback} — Human reviewer's feedback (if any)
#   {report_template}— Report structure from config/report_template.md

REPORT_PROMPT = """You are a report writer. Generate a clear, professional report
based on the analysis below.

## Item
ID: {input_id}
Context: {input_context}

## Analysis
{analysis_json}

## Human Reviewer Notes
{human_feedback}

## Report Structure
Follow this template:
{report_template}

## Instructions
- Write in clear, professional language appropriate for the target audience
- Reference specific data points from the analysis
- Incorporate the human reviewer's feedback where applicable
- Be concise but thorough — every section should add value
"""

# ── Summary Prompt ────────────────────────────────────────────────────
# Used for a second LLM call to summarise the generated report.
# The summary prompt receives the full report as input so the LLM
# summarises the actual document rather than trying to summarise
# and generate simultaneously.
#
# Variable: {report_text} — The full report text from the first LLM call

SUMMARY_PROMPT = """Summarise the following report in 2-3 sentences. Focus on the
key findings, overall assessment, and most important recommendation.

## Report
{report_text}

## Instructions
- Keep the summary under 100 words
- Lead with the most important finding
- Include the overall assessment score or rating if present
"""
