"""
Agent Definition — Google ADK variant
======================================
This is the central wiring for your workflow agent. It defines an LlmAgent,
wires in function tools, and provides a main() for local testing.

Replace the placeholder tool implementations with your actual logic from
the Design Document (Stage 4) action specifications.

Methodology reference:
  - Stage 4: Design → Action Specifications, Flow Structure
  - Stage 5: Build → Platform Cheat Sheet (ADK row)
"""

import os

# NOTE: Imports are illustrative — consult
# https://docs.cloud.google.com/agent-builder/agent-development-kit/overview
# for the current ADK API. The framework does not pin to a specific ADK
# version; pin in requirements.txt based on what's stable at your build
# time.
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from prompts.instructions import MAIN_INSTRUCTIONS
from tools.example_tool import fetch_example_data


# ── Agent Definition ─────────────────────────────────────────────────
# LlmAgent bundles a model, instructions, and a list of tools. You can
# compose multiple LlmAgents into SequentialAgent or ParallelAgent for
# more complex flows — see your Design Document Section 2 (Flow Structure).
#
# For HIL checkpoints: wrap the sensitive tools in FunctionTool with
# require_confirmation=ToolConfirmation(...) — see README.md for the
# pattern.


def build_agent() -> LlmAgent:
    """Build the workflow agent.

    The tools list should include every data-source wrapper from your
    Stage 3 Data Inventory plus any LLM-backed analysis functions that
    need to be explicitly invocable.
    """
    return LlmAgent(
        name="workflow_agent",
        # Gemini is the native choice for ADK; LiteLLM bridges are available
        # for Claude / OpenAI / other providers. Pick based on your team's
        # approved model provider.
        model="gemini-2.0-flash",
        instruction=MAIN_INSTRUCTIONS,
        tools=[
            FunctionTool(fetch_example_data),
            # Add more tools here — one per data source and one per
            # LLM-backed action from your Design Document.
        ],
    )


# ── Main (local test) ────────────────────────────────────────────────

def main():
    """Run the agent with a demo input."""
    print("=" * 60)
    print("Workflow Agent — Starter Project (Google ADK)")
    print("=" * 60)
    print()
    print("Running demo with a placeholder input...")
    print("-" * 60)

    if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_GENAI_USE_VERTEXAI")):
        print("⚠ GOOGLE_API_KEY not set and Vertex AI auth not configured.")
        print("  Set GOOGLE_API_KEY in .env (AI Studio) or enable Vertex AI")
        print("  auth (gcloud auth application-default login) to run a live demo.")
        return

    agent = build_agent()

    # ADK's agent.run() drives the reasoning loop. The exact invocation
    # API depends on your ADK version — consult the official docs for the
    # current surface. Illustrative shape:
    #
    #   response = agent.run("Process input example-001")
    #   print(response.final_output)

    print("  [demo] Agent built successfully. See README.md for next steps.")
    print()
    print("=" * 60)
    print("Demo complete. Now customise this project for your workflow:")
    print("  1. Implement tools in tools/ for your data sources")
    print("  2. Add ToolConfirmation to HIL-gated tools")
    print("  3. Write instructions in prompts/instructions.py")
    print("  4. Add config in config/ for scoring rubrics and templates")
    print("  5. Compose sub-agents in agent.py if your flow has multiple")
    print("     phases (SequentialAgent / ParallelAgent)")
    print("  6. Run tool tests: python -m pytest tests/")
    print("=" * 60)


if __name__ == "__main__":
    main()
