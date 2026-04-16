"""
Tool tests — OpenAI Agents SDK variant
=======================================
Unit tests for each tool. Test tools in isolation (no agent, no LLM)
before integrating into the agent.

Methodology reference:
  - Stage 6: Evaluate → Unit testing patterns
"""

import os
import pytest

from context import WorkflowContext
from tools.example_tool import fetch_example_data


@pytest.mark.asyncio
async def test_fetch_example_data_missing_key(monkeypatch):
    """Tool should return an error dict when API key is missing (not raise)."""
    monkeypatch.delenv("EXAMPLE_API_KEY", raising=False)
    ctx = WorkflowContext(input_id="test-001")

    result = await fetch_example_data(ctx, "test-001")

    assert "error" in result
    assert "EXAMPLE_API_KEY" in result["error"]
    assert len(ctx.data_errors) == 1


@pytest.mark.asyncio
async def test_fetch_example_data_success(monkeypatch):
    """Tool should populate context and return ok on success."""
    monkeypatch.setenv("EXAMPLE_API_KEY", "fake-test-key")
    ctx = WorkflowContext(input_id="test-002")

    result = await fetch_example_data(ctx, "test-002")

    assert result.get("status") == "ok"
    assert "example" in ctx.raw_data
    assert ctx.data_errors == []
