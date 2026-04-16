"""
Agent Definition — OpenAI Agents SDK variant
=============================================
This is the central wiring for your workflow agent. It defines the agent,
wires in function tools, and provides a main() for local testing.

Replace the placeholder tool implementations with your actual logic from
the Design Document (Stage 4) action specifications.

Methodology reference:
  - Stage 4: Design → Action Specifications, Flow Structure
  - Stage 5: Build → Platform Cheat Sheet (OpenAI Agents SDK row)

Unlike LangGraph's explicit graph, OpenAI Agents SDK lets the model's
reasoning decide which tool to call next. You influence the flow via
instruction text (see prompts/instructions.py) and via tool availability.
"""

import asyncio
import os

# NOTE: The official SDK is `openai-agents` on PyPI. Imports shown below are
# illustrative — consult https://platform.openai.com/docs/guides/agents for
# the current API surface. The framework does not pin to a specific SDK
# version because the SDK is evolving rapidly; your team should pin in
# requirements.txt based on what's stable at your build time.
from agents import Agent, Runner  # openai-agents package

from context import WorkflowContext
from prompts.instructions import MAIN_INSTRUCTIONS
from tools.example_tool import fetch_example_data


# ── Agent Definition ─────────────────────────────────────────────────
# The Agent object bundles instructions, tools, and (optionally) handoffs
# to sub-agents. This is the equivalent of a LangGraph StateGraph definition
# but expressed declaratively rather than as an explicit graph.
#
# See your Design Document Section 2 (Flow Structure) and Section 4 (Action
# Specifications). The tools list is the set of actions the agent can take;
# the instructions describe the order and conditions under which they run.


def build_agent() -> Agent:
    """Build the workflow agent.

    The agent's tools should include every data-source wrapper from your
    Stage 3 Data Inventory plus any LLM-backed analysis functions that
    need to be explicitly invocable.
    """
    return Agent(
        name="workflow_agent",
        # The model your team has approved. Use the smallest model that
        # produces acceptable output for cost control; escalate to larger
        # models only for specific nodes that need them.
        model="gpt-4o-mini",
        instructions=MAIN_INSTRUCTIONS,
        tools=[
            fetch_example_data,
            # Add more tools here — one per data source and one per
            # LLM-backed action from your Design Document.
        ],
        # handoffs=[approval_agent],  # Optional: for HIL via handoff pattern
    )


# ── Main (local test) ────────────────────────────────────────────────

async def main():
    """Run the agent with a demo input."""
    print("=" * 60)
    print("Workflow Agent — Starter Project (OpenAI Agents SDK)")
    print("=" * 60)
    print()
    print("Running demo with a placeholder input...")
    print("-" * 60)

    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠ OPENAI_API_KEY not set — cannot run live demo.")
        print("  Set it in .env and re-run to see the agent call tools.")
        return

    agent = build_agent()

    # Initial context (equivalent to initial state in LangGraph)
    context = WorkflowContext(input_id="example-001")

    # Runner.run() drives the agent's reasoning loop until it produces a
    # final response or hits a max-turns limit.
    result = await Runner.run(
        agent,
        "Please process input example-001 and report what you found.",
        context=context,
        max_turns=10,
    )

    print("-" * 60)
    print("Final response:")
    print()
    print(result.final_output)
    print()
    print("=" * 60)
    print("Demo complete. Now customise this project for your workflow:")
    print("  1. Update context.py with your Design Document memory fields")
    print("  2. Implement tools in tools/ for your data sources")
    print("  3. Write instructions in prompts/instructions.py")
    print("  4. Add config in config/ for scoring rubrics and templates")
    print("  5. Wire more tools and (optional) sub-agent handoffs in agent.py")
    print("  6. Run tool tests: python -m pytest tests/")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
