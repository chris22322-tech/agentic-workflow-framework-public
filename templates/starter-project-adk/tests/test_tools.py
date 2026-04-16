"""
Tool tests — Google ADK variant
================================
Unit tests for each tool. Test tools in isolation (no agent, no LLM)
before integrating into the agent.

Methodology reference:
  - Stage 6: Evaluate → Unit testing patterns
"""

import pytest

from tools.example_tool import fetch_example_data


def test_fetch_example_data_missing_key(monkeypatch):
    """Tool should return an error dict when API key is missing (not raise)."""
    monkeypatch.delenv("EXAMPLE_API_KEY", raising=False)

    result = fetch_example_data("test-001")

    assert "error" in result
    assert "EXAMPLE_API_KEY" in result["error"]


def test_fetch_example_data_success(monkeypatch):
    """Tool should return ok on success."""
    monkeypatch.setenv("EXAMPLE_API_KEY", "fake-test-key")

    result = fetch_example_data("test-002")

    assert result.get("status") == "ok"
    assert "data" in result
