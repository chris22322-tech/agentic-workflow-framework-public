"""
Node Tests — Example
====================
Test nodes by constructing a state dict and calling the node function
directly. This verifies node logic without running the full graph.

Run: python -m pytest tests/test_nodes.py -v

Methodology reference:
  - Stage 5: Build → Test nodes with constructed state
  - Stage 6: Evaluate → Test Cases
"""

import pytest

from state import AgentState
from agent import gather_data, analyse, hil_review, generate_output


# ── Helper ────────────────────────────────────────────────────────────

def make_state(**overrides) -> AgentState:
    """Construct a minimal valid state for testing.

    Provides sensible defaults for all required fields. Override any
    field by passing it as a keyword argument.

    Adapt this to your actual state schema — every field in your
    AgentState TypedDict should have a default here.
    """
    defaults: AgentState = {
        "input_id": "test-001",
        "input_context": "Unit test run",
        "raw_data": {},
        "data_errors": [],
        "analysis": {},
        "human_feedback": "",
        "human_approved": False,
        "output_text": "",
        "output_metadata": {},
    }
    defaults.update(overrides)
    return defaults


# ── Tests ─────────────────────────────────────────────────────────────


class TestGatherDataNode:
    """Tests for the gather_data node.

    Replace with tests for your actual data gathering logic. Pattern:
    1. Construct state with input fields
    2. Call the node function directly
    3. Assert it returns the expected state updates
    """

    def test_returns_raw_data(self):
        """Node should return a dict with raw_data key."""
        state = make_state(input_id="test-item")
        result = gather_data(state)

        assert "raw_data" in result
        assert isinstance(result["raw_data"], dict)

    def test_returns_data_errors_list(self):
        """Node should return data_errors as a list (for append-only state)."""
        state = make_state()
        result = gather_data(state)

        assert "data_errors" in result
        assert isinstance(result["data_errors"], list)


class TestAnalyseNode:
    """Tests for the analyse node."""

    def test_returns_analysis(self):
        """Node should return a dict with analysis key."""
        state = make_state(raw_data={"key": "value"})
        result = analyse(state)

        assert "analysis" in result
        assert isinstance(result["analysis"], dict)

    def test_handles_upstream_error(self):
        """Node should detect upstream errors and return an error analysis."""
        state = make_state(raw_data={"error": "timeout", "source": "example_tool"})
        result = analyse(state)

        assert "analysis" in result
        assert "error" in result["analysis"]


class TestHilReviewNode:
    """Tests for the hil_review node."""

    def test_returns_feedback_fields(self):
        """Node should return human_feedback and human_approved."""
        state = make_state(analysis={"score": "High"})
        result = hil_review(state)

        assert "human_feedback" in result
        assert "human_approved" in result


class TestGenerateOutputNode:
    """Tests for the generate_output node."""

    def test_returns_output_text(self):
        """Node should return output_text."""
        state = make_state(
            analysis={"score": "High", "details": "Test analysis"},
            human_feedback="Looks good",
            human_approved=True,
        )
        result = generate_output(state)

        assert "output_text" in result
        assert isinstance(result["output_text"], str)
        assert len(result["output_text"]) > 0
