"""
Tool Tests — Example
====================
Test tools independently before integrating them into nodes. Each tool
test uses fixture data to verify the tool's parsing and error handling
without hitting live APIs.

Run: python -m pytest tests/test_tools.py -v

Methodology reference:
  - Stage 5: Build → Test tools independently first
  - Stage 6: Evaluate → Test Cases
"""

import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from tools.example_tool import fetch_example_data


# ── Load Fixtures ─────────────────────────────────────────────────────

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_fixture(filename: str) -> dict:
    """Load a JSON fixture file for testing."""
    with open(FIXTURES_DIR / filename) as f:
        return json.load(f)


# ── Tests ─────────────────────────────────────────────────────────────


class TestExampleTool:
    """Tests for the example tool.

    Replace these with tests for your actual tools. The pattern is:
    1. Mock the external API call
    2. Feed it fixture data (from tests/fixtures/)
    3. Assert the tool returns the expected structure
    4. Test error cases return error dicts (not exceptions)
    """

    def test_missing_api_key_returns_error(self):
        """Tool should return an error dict when API key is not set."""
        # Ensure the key is not set
        env = os.environ.copy()
        env.pop("EXAMPLE_API_KEY", None)

        with patch.dict(os.environ, env, clear=True):
            result = fetch_example_data("test-id")

        assert "error" in result
        assert result["error"] == "missing_api_key"
        assert result["source"] == "example_tool"

    @patch("tools.example_tool.requests.get")
    def test_successful_response(self, mock_get):
        """Tool should return parsed JSON on successful API call."""
        fixture_data = load_fixture("example_response.json")
        mock_response = MagicMock()
        mock_response.json.return_value = fixture_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {"EXAMPLE_API_KEY": "test-key"}):
            result = fetch_example_data("test-id", date_range="2024-Q1")

        assert "error" not in result
        assert result == fixture_data
        mock_get.assert_called_once()

    @patch("tools.example_tool.requests.get")
    def test_timeout_returns_error(self, mock_get):
        """Tool should return an error dict on timeout, not raise."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

        with patch.dict(os.environ, {"EXAMPLE_API_KEY": "test-key"}):
            result = fetch_example_data("test-id")

        assert result["error"] == "timeout"
        assert result["source"] == "example_tool"

    @patch("tools.example_tool.requests.get")
    def test_http_error_returns_error(self, mock_get):
        """Tool should return an error dict on HTTP errors, not raise."""
        import requests
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with patch.dict(os.environ, {"EXAMPLE_API_KEY": "test-key"}):
            result = fetch_example_data("test-id")

        assert result["error"] == "http_error"
        assert result["source"] == "example_tool"
