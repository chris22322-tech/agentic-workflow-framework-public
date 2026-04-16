"""
Example Tool — Google ADK variant
==================================
Template for a data-retrieval tool. Copy this file for each data source
in your Stage 3 Data Inventory.

Methodology reference:
  - Stage 3: Scope → Data sources and integration requirements
  - Stage 5: Build → "One tool per file" and error handling conventions

ADK wraps a Python function with FunctionTool in agent.py. The function's
docstring becomes the tool's description to the model, and type
annotations become the tool's schema — so keep both precise.

The error handling pattern is critical: return an error dict on failure,
never raise. The agent's reasoning loop sees the error result and decides
what to do next.
"""

import os
from typing import Any


def fetch_example_data(input_id: str) -> dict[str, Any]:
    """Retrieve example data for the given input ID.

    Use this tool to fetch raw data from the upstream source before
    any analysis or reporting. Returns a dict with either the retrieved
    data (under "data") or an error marker (under "error"). Never raises.

    Args:
        input_id: The identifier to fetch data for.

    Returns:
        On success: {"status": "ok", "data": ...}
        On failure: {"error": "<reason>", "input_id": "<id>"}
    """
    # TODO: Replace with your actual API call
    api_url = os.environ.get("EXAMPLE_API_URL", "https://api.example.com")
    api_key = os.environ.get("EXAMPLE_API_KEY")

    if not api_key:
        return {"error": "EXAMPLE_API_KEY not configured", "input_id": input_id}

    try:
        # Example shape — replace with your actual client call:
        # import httpx
        # response = httpx.get(
        #     f"{api_url}/items/{input_id}",
        #     headers={"Authorization": f"Bearer {api_key}"},
        #     timeout=30.0,
        # )
        # response.raise_for_status()
        # data = response.json()
        data = {"placeholder": f"Example data for {input_id}"}

        return {"status": "ok", "data": data}

    except Exception as exc:
        return {
            "error": f"fetch_example_data failed: {type(exc).__name__}: {exc}",
            "input_id": input_id,
        }
