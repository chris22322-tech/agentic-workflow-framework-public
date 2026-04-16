"""
Analysis Prompt Template
========================
This prompt should implement the Prompt Pattern field from your Design
Document node specification for the analysis node.

Replace the placeholder variables and instructions with your actual
analysis criteria from Stage 3: Scope → analysis steps and decision logic.

Methodology reference:
  - Stage 3: Scope → Analysis steps, decision criteria, scoring rubrics
  - Stage 4: Design → Node Spec "Prompt Pattern" field for the analyse node
  - Stage 5: Build → Prompt Management section
"""

# ── Analysis Prompt ───────────────────────────────────────────────────
# Variables filled by the analyse node at runtime:
#   {input_id}      — The item being analysed
#   {input_context} — Additional context for the analysis
#   {raw_data_json} — JSON string of gathered data from tools
#   {rubric_json}   — JSON string of scoring rubric from config/
#
# Double braces {{ }} are literal braces in the output format —
# they are NOT Python format placeholders. This is how you include
# JSON schema examples in a .format() template string.

ANALYSIS_PROMPT = """You are an expert analyst. Analyse the following data and produce
a structured assessment.

## Item
ID: {input_id}
Context: {input_context}

## Data
{raw_data_json}

## Scoring Criteria
Use the following rubric to guide your assessment:
{rubric_json}

## Instructions
1. Review all data sources for completeness and consistency
2. Apply the scoring criteria to produce an overall assessment
3. Identify key findings and any data gaps
4. Provide actionable recommendations

## Required Output Format
Return your analysis as a JSON object with this structure:
{{
    "score": "High | Medium | Low",
    "confidence": "High | Medium | Low",
    "key_findings": ["finding 1", "finding 2"],
    "data_gaps": ["gap 1", "gap 2"],
    "recommendations": ["recommendation 1", "recommendation 2"],
    "details": "Detailed narrative of the analysis"
}}
"""

# ── Conditional Feedback Section ──────────────────────────────────────
# Append this to ANALYSIS_PROMPT when re-running analysis after human
# feedback. This implements the revision loop from your Design Document's
# graph structure.
#
# Variable: {human_feedback} — The reviewer's corrections or additions

FEEDBACK_ADDENDUM = """

## Human Reviewer Feedback
The following feedback was provided by a human reviewer on a previous
version of this analysis. Incorporate their corrections and additional
context into your revised assessment:

{human_feedback}
"""
