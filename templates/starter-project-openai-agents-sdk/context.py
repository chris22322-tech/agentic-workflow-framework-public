"""
Workflow Context — OpenAI Agents SDK variant
==============================================
The context object is passed to every function tool in the agent. It is
the equivalent of LangGraph's state — a shared notepad that actions can
read from and write to.

Replace the placeholder fields with your Design Document Section 3:
Memory Fields. Keep the category comments.

Methodology reference:
  - Stage 4: Design → Memory Schema
  - Stage 5: Build → Implementation Conventions
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowContext:
    """Shared state passed to every function tool.

    Pydantic dataclasses also work — pick whichever your team prefers.
    The key property: the object is mutable, so tools that write to it
    update state for subsequent tool calls within the same agent run.
    """

    # ── Input identifiers ──────────────────────────────────────────
    # What uniquely identifies the unit of work the agent is processing.
    input_id: str = ""

    # ── Raw data fields ────────────────────────────────────────────
    # Populated by data-retrieval tools. One field per data source in
    # your Stage 3 Data Inventory.
    raw_data: dict[str, Any] = field(default_factory=dict)
    data_errors: list[str] = field(default_factory=list)

    # ── Analysis fields ────────────────────────────────────────────
    # Populated by LLM-backed analysis tools. One field per analysis
    # step from your Design Document.
    analysis: dict[str, Any] = field(default_factory=dict)

    # ── HIL fields ─────────────────────────────────────────────────
    # Populated by HIL checkpoint tools.
    human_feedback: str = ""
    human_approved: bool = False

    # ── Output fields ──────────────────────────────────────────────
    # Populated by the final generation step.
    output_text: str = ""
    output_metadata: dict[str, Any] = field(default_factory=dict)
