"""
Agent State Schema
==================
This schema should match Section 3 of your Design Document (State Schema).

Each field is categorised by its role in the workflow. The categories below
mirror the methodology's state design guidance from Stage 4: Design.

Replace the placeholder fields with your actual state fields from the
Design Document. Keep the category comments — they help anyone reading
the code understand the data flow at a glance.

Methodology reference:
  - Stage 4: Design → State Schema section
  - Stage 5: Build → "State schema in its own file"
"""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict


class AgentState(TypedDict):
    """Workflow agent state. Replace these placeholders with your Design Document fields.

    Each field should map to a row in your Stage 4 State Schema table. The
    comments indicate which nodes read/write each field and which Stage 3
    Scope Document step it derives from.
    """

    # ── Input Fields ──────────────────────────────────────────────────
    # Provided when invoking the graph. These come from the user or the
    # system that triggers the workflow.
    # Maps to: Stage 3 Scope Document → "Trigger / Input" section

    input_id: str          # Primary identifier for the item being processed
    input_context: str     # Additional context or parameters for this run

    # ── Gathered Data ─────────────────────────────────────────────────
    # Populated by data-gathering nodes. Each tool writes its results here.
    # Maps to: Stage 3 Scope Document → data source entries
    # Written by: gather_data node | Read by: analyse node

    raw_data: dict         # Raw data retrieved from external sources
    data_errors: Annotated[list, operator.add]  # Errors from data gathering (append-only)

    # ── Analysis ──────────────────────────────────────────────────────
    # Populated by LLM analysis nodes. Structured results from prompts.
    # Maps to: Stage 3 Scope Document → analysis / decision steps
    # Written by: analyse node | Read by: hil_review, generate_output nodes

    analysis: dict         # Structured analysis output (scores, findings, etc.)

    # ── Human Feedback ────────────────────────────────────────────────
    # Populated by human-in-the-loop (HIL) review nodes.
    # Maps to: Stage 4 Design Document → HIL Interaction Design
    # Written by: hil_review node | Read by: generate_output node

    human_feedback: str    # Human reviewer's corrections or confirmation
    human_approved: bool   # Whether the human approved the analysis

    # ── Output ────────────────────────────────────────────────────────
    # Final outputs of the workflow. Consumed by downstream systems or users.
    # Maps to: Stage 3 Scope Document → output / deliverable entries
    # Written by: generate_output node

    output_text: str       # Generated text output (report, summary, etc.)
    output_metadata: dict  # Metadata about the generation (model, timestamp, etc.)
