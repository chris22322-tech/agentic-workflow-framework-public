"""
Agent Graph Definition
======================
This is the central wiring for your workflow agent. It imports the state
schema, defines node functions, and connects them into a LangGraph StateGraph.

Replace the placeholder node implementations with your actual logic from
the Design Document (Stage 4) node specifications.

Methodology reference:
  - Stage 4: Design → Node Specifications, Graph Structure
  - Stage 5: Build → Graph Definition, Node Functions, Implementation Conventions
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState


# ── Node Functions ────────────────────────────────────────────────────
# Each node takes the current state and returns a dict of state updates.
# Keep nodes focused — one responsibility per node.
#
# See your Design Document Section 4: Node Specifications for the full
# spec of each node (inputs, outputs, prompt pattern, error handling).


def gather_data(state: AgentState) -> dict:
    """Retrieve raw data from external sources.

    Implement this node: See your Design Document Node Specification for
    'gather_data' — it lists which tools to call, what data to retrieve,
    and how to handle source errors.

    Pattern: Call each tool, collect results into state fields.
    Each tool handles its own errors and returns an error dict on failure
    rather than raising — so downstream nodes can check for error markers.

    Methodology reference:
      - Stage 3: Scope → Data sources and integration requirements
      - Stage 5: Build → "One tool per file" and error handling conventions
    """
    # TODO: Replace with your actual tool calls
    # Example:
    #   from tools.example_tool import fetch_example_data
    #   result = fetch_example_data(state["input_id"])
    #   return {"raw_data": result, "data_errors": []}

    print(f"  [gather_data] Processing: {state.get('input_id', 'unknown')}")
    return {
        "raw_data": {"placeholder": "Replace with actual data gathering logic"},
        "data_errors": [],
    }


def analyse(state: AgentState) -> dict:
    """Run LLM analysis on gathered data.

    Implement this node: See your Design Document Node Specification for
    'analyse' — it defines the prompt pattern, expected output schema,
    scoring criteria, and error handling.

    Pattern: Load config, format prompt with state data, call LLM with
    structured output (tool_use), validate response, return analysis dict.

    Methodology reference:
      - Stage 3: Scope → Analysis steps and decision logic
      - Stage 5: Build → LLM Analysis Node pattern, call_llm_for_json helper
    """
    # TODO: Replace with your actual LLM analysis
    # Example:
    #   from prompts.analyse import ANALYSIS_PROMPT
    #   prompt = ANALYSIS_PROMPT.format(data=json.dumps(state["raw_data"]))
    #   analysis = call_llm_for_json(prompt, YourAnalysisSchema)
    #   return {"analysis": analysis}

    # Check for upstream errors before analysing
    if isinstance(state.get("raw_data"), dict) and "error" in state["raw_data"]:
        print("  [analyse] Skipping — upstream data error detected")
        return {"analysis": {"error": "Data unavailable"}}

    print("  [analyse] Analysing gathered data...")
    return {
        "analysis": {"placeholder": "Replace with actual LLM analysis logic"},
    }


def hil_review(state: AgentState) -> dict:
    """Pause for human review of analysis outputs.

    Implement this node: See your Design Document HIL Interaction Design
    for what data to present, what actions the reviewer can take, and how
    their feedback feeds back into the workflow.

    Pattern: Format analysis for human consumption, call interrupt() to
    pause, receive human feedback via Command(resume=...).

    Methodology reference:
      - Stage 4: Design → HIL Interaction Design section
      - Stage 5: Build → HIL Node pattern, interrupt() and Command(resume=...)
    """
    # TODO: Replace with actual HIL logic using interrupt()
    # Example:
    #   from langgraph.types import interrupt
    #   feedback = interrupt({
    #       "message": "Review the analysis. Confirm, correct, or add context.",
    #       "analysis": state["analysis"],
    #   })
    #   return {"human_feedback": feedback, "human_approved": True}

    print("  [hil_review] Human review checkpoint (placeholder — no interrupt in demo)")
    return {
        "human_feedback": "Auto-approved in demo mode",
        "human_approved": True,
    }


def generate_output(state: AgentState) -> dict:
    """Generate the final output (report, summary, deliverable).

    Implement this node: See your Design Document Node Specification for
    'generate_output' — it defines the prompt pattern, output format,
    and how human feedback is incorporated.

    Pattern: Format prompt with analysis and human feedback, call LLM
    for text generation (not structured JSON), return output text.

    Methodology reference:
      - Stage 3: Scope → Output / deliverable specification
      - Stage 5: Build → LLM Generation Node pattern
    """
    # TODO: Replace with actual LLM generation
    # Example:
    #   from prompts.report import REPORT_PROMPT
    #   prompt = REPORT_PROMPT.format(
    #       analysis=json.dumps(state["analysis"]),
    #       feedback=state["human_feedback"],
    #   )
    #   response = client.messages.create(model="claude-sonnet-4-20250514", ...)
    #   return {"output_text": response.content[0].text}

    print("  [generate_output] Generating output...")
    return {
        "output_text": "Placeholder output — replace with actual LLM generation.",
        "output_metadata": {"status": "demo"},
    }


# ── Routing Function ─────────────────────────────────────────────────
# Used by conditional edges to route based on state values.
# See Stage 5: Build → Conditional Edges for the pattern.

def route_after_review(state: AgentState) -> str:
    """Route based on human review decision.

    Returns the name of the next node. Used with add_conditional_edges()
    to implement approval/revision loops from your Design Document's
    graph structure.
    """
    if state.get("human_approved"):
        return "approved"
    return "revise"


# ── Graph Construction ────────────────────────────────────────────────

def build_graph():
    """Build and compile the workflow graph.

    The graph structure should match Section 2 of your Design Document
    (Graph Structure). Add/remove nodes and edges to match your design.
    """
    graph = StateGraph(AgentState)

    # Add nodes — one per node in your Design Document
    graph.add_node("gather_data", gather_data)
    graph.add_node("analyse", analyse)
    graph.add_node("hil_review", hil_review)
    graph.add_node("generate_output", generate_output)

    # Add edges — wire the graph to match your Design Document's flow
    graph.add_edge(START, "gather_data")
    graph.add_edge("gather_data", "analyse")
    graph.add_edge("analyse", "hil_review")

    # Conditional edge: route based on human review decision
    # Modify the routing map to match your Design Document's graph structure
    graph.add_conditional_edges(
        "hil_review",
        route_after_review,
        {
            "approved": "generate_output",
            "revise": "analyse",          # Loop back for revision
        },
    )

    graph.add_edge("generate_output", END)

    # MemorySaver stores checkpoints in-memory — for development only.
    # Replace with PostgresSaver for production.
    # See methodology Stage 5: Production Persistence
    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)


# ── Main ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Workflow Agent — Starter Project")
    print("=" * 60)
    print()
    print("This is a skeleton agent from the Stage 5 Starter Project.")
    print("Replace the placeholder nodes with your actual implementation")
    print("from your Design Document (Stage 4).")
    print()
    print("Running demo with placeholder data...")
    print("-" * 60)

    app = build_graph()

    # Example input — replace with your actual input fields
    initial_state = {
        "input_id": "example-001",
        "input_context": "Demo run of the starter project",
    }

    # Run the graph with a thread_id for checkpointing
    config = {"configurable": {"thread_id": "demo-thread-1"}}

    result = app.invoke(initial_state, config=config)

    print("-" * 60)
    print("Final state:")
    print()
    for key, value in result.items():
        print(f"  {key}: {value}")
    print()
    print("=" * 60)
    print("Demo complete. Now customise this project for your workflow:")
    print("  1. Update state.py with your Design Document state schema")
    print("  2. Implement tools in tools/ for your data sources")
    print("  3. Write prompts in prompts/ for your LLM nodes")
    print("  4. Add config in config/ for scoring rubrics and templates")
    print("  5. Fill in the node functions above with real logic")
    print("  6. Run tests: python -m pytest tests/")
    print("=" * 60)
