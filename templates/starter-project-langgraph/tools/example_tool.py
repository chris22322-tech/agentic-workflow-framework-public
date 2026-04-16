"""
Example Tool — Template
=======================
This is a template tool function showing the standard pattern for
data-source integrations. Copy this file for each tool in your workflow.

Every tool should:
  1. Accept clear parameters (IDs, date ranges, etc.)
  2. Wrap the external call in try/except
  3. Return an error dict on failure — never raise
  4. Let the calling node decide what to do about errors

The node that calls this tool checks for an "error" key in the returned
dict to detect failures. This pattern is consistent across all tools,
making error handling predictable throughout the graph.

Methodology reference:
  - Stage 3: Scope → Data Inventory (what sources to integrate)
  - Stage 3: Scope → Integration Requirements (auth, rate limits, formats)
  - Stage 5: Build → Tool implementation conventions
"""

import os
from typing import Any

import requests


def fetch_example_data(item_id: str, date_range: str | None = None) -> dict[str, Any]:
    """Fetch data from an example external API.

    Replace this with your actual data source integration. The function
    signature, error handling pattern, and return format are the template —
    adapt the implementation to your API.

    Args:
        item_id: The identifier for the item to retrieve.
        date_range: Optional date range filter (e.g., "2024-Q1").

    Returns:
        dict: The retrieved data on success, or an error dict on failure.
              Error dict format: {"error": str, "source": str, "details": str}
    """
    # Load configuration from environment variables
    # See .env.example for required variables
    api_url = os.environ.get("EXAMPLE_API_URL", "https://api.example.com")
    api_key = os.environ.get("EXAMPLE_API_KEY")

    if not api_key:
        return {
            "error": "missing_api_key",
            "source": "example_tool",
            "details": "EXAMPLE_API_KEY not set. See .env.example for required variables.",
        }

    try:
        # Build the request — adapt URL, headers, and params to your API
        params = {"id": item_id}
        if date_range:
            params["range"] = date_range

        response = requests.get(
            f"{api_url}/data",
            headers={"Authorization": f"Bearer {api_key}"},
            params=params,
            timeout=30,  # Always set a timeout
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        return {
            "error": "timeout",
            "source": "example_tool",
            "details": f"Request timed out for item {item_id}",
        }
    except requests.exceptions.HTTPError as e:
        return {
            "error": "http_error",
            "source": "example_tool",
            "details": f"HTTP {e.response.status_code}: {e.response.text[:200]}",
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": "request_failed",
            "source": "example_tool",
            "details": str(e),
        }
