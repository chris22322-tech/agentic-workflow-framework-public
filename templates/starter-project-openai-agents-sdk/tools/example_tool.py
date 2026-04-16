"""
Example Tool — OpenAI Agents SDK variant
=========================================
Template for a data-retrieval tool. Copy this file for each data source
in your Stage 3 Data Inventory.

Methodology reference:
  - Stage 3: Scope → Data sources and integration requirements
  - Stage 5: Build → "One tool per file" and error handling conventions

The error handling pattern is critical: return an error dict on failure,
never raise. The agent's reasoning loop sees the error result and decides
what to do next (retry, skip, escalate to a human).
"""

import os
from typing import Any

from agents import function_tool

from context import WorkflowContext


@function_tool
async def fetch_example_data(ctx: WorkflowContext, input_id: str) -> dict[str, Any]:
    """Retrieve example data for the given input ID.

    Args:
        ctx: The workflow context (shared state across all tool calls).
        input_id: The identifier to fetch data for.

    Returns:
        A dict with either the retrieved data or an error marker.
        Never raises.
    """
    # TODO: Replace with your actual API call
    api_url = os.environ.get("EXAMPLE_API_URL", "https://api.example.com")
    api_key = os.environ.get("EXAMPLE_API_KEY")

    if not api_key:
        error = {"error": "EXAMPLE_API_KEY not configured", "input_id": input_id}
        ctx.data_errors.append(error["error"])
        return error

    try:
        # Example shape — replace with your actual client call:
        # response = await httpx.AsyncClient().get(
        #     f"{api_url}/items/{input_id}",
        #     headers={"Authorization": f"Bearer {api_key}"},
        #     timeout=30.0,
        # )
        # response.raise_for_status()
        # data = response.json()
        data = {"placeholder": f"Example data for {input_id}"}

        # Write to shared context so downstream tools can read it
        ctx.raw_data["example"] = data

        return {"status": "ok", "data": data}

    except Exception as exc:
        error_msg = f"fetch_example_data failed: {type(exc).__name__}: {exc}"
        ctx.data_errors.append(error_msg)
        return {"error": error_msg, "input_id": input_id}
