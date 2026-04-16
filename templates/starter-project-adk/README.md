# Workflow Agent — Starter Project (Google ADK)

A skeleton agent built on **Google's Agent Development Kit (ADK)** from the **Stage 5: Build** methodology. This project gives you a working directory structure, placeholder tools, and template files — ready to fill in with your Design Document (Stage 4) specifications.

> **This is the Google ADK variant.** Starter projects also exist for **LangGraph** (`templates/starter-project-langgraph/`) and **OpenAI Agents SDK** (`templates/starter-project-openai-agents-sdk/`). The framework itself is platform-neutral; pick the starter that matches your team's chosen platform.

> **Model flexibility:** ADK works with Gemini (native), Claude (via LiteLLM), and OpenAI models (via LiteLLM). This starter defaults to Gemini for the simplest path. Swap the model config to use a different provider.

## How Google ADK maps to the framework

| Framework concept (Stage 4) | Google ADK primitive |
|---|---|
| **Agent** | `LlmAgent` class (or `Agent` base class for custom loops) |
| **Action** | `FunctionTool` wrapping a Python function; or a sub-agent used as `AgentTool` |
| **Memory field** | Session state fields managed by Agent Engine (or in-memory for local) |
| **Flow** | `SequentialAgent`, `ParallelAgent`, or a custom composition of sub-agents |
| **HIL checkpoint** | `ToolConfirmation` — a first-class pause primitive with boolean or structured response |
| **Error handling** | Function-level `try`/`except` returning error dicts; agent-level error handlers |
| **Tool (API wrapper)** | `FunctionTool(my_python_function)` |
| **Tool (OpenAPI spec)** | `OpenAPIToolset(spec=...)` — auto-generates tools from an OpenAPI spec |
| **Tool (MCP connector)** | `McpToolset` from `google.adk.tools.mcp_tool` — first-class MCP support |

**Key paradigm strengths:** ADK has first-class primitives for every concept the framework teaches — `FunctionTool`, `OpenAPIToolset`, `McpToolset`, `ToolConfirmation` for HIL. The Stage 4 decision rubric for tool types maps almost directly onto these. If your design has an HIL checkpoint that needs strong correctness guarantees, ADK's `ToolConfirmation` is a better fit than instruction-based pauses in OpenAI Agents SDK.

## Quick Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your Google API key (or Vertex AI auth) and data source creds

# 4. Run the demo
python agent.py
```

The demo runs the agent with a placeholder tool and shows a reasoning loop.

## Project Structure

```
starter-project-adk/
├── agent.py              # Agent definition — LlmAgent, tools, sub-agents
├── tools/                # One file per data source
│   ├── __init__.py
│   └── example_tool.py   # FunctionTool template
├── prompts/              # Externalised instruction text
│   ├── __init__.py
│   └── instructions.py
├── config/               # Domain config — edit this, not code
│   ├── scoring_rubric.yaml
│   └── report_template.md
├── tests/                # Unit tests
│   ├── __init__.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Customise

### 1. Tools (`tools/`)

For each data source in your **Stage 3 Data Inventory**, copy `tools/example_tool.py`. ADK's `FunctionTool` wraps any Python function — the function's docstring becomes the tool's description, and its type annotations become the tool's schema. Keep docstrings precise; the agent uses them to decide when to call each tool.

For OpenAPI-described APIs, skip the function-tool layer entirely and use `OpenAPIToolset(spec=<your_spec>)`. For MCP-compatible services, use `McpToolset`.

### 2. Instructions (`prompts/instructions.py`)

Your Design Document's flow structure lives here as instruction text for the `LlmAgent`. Describe the action sequence, HIL checkpoints, and error handling behaviour.

### 3. Config (`config/`)

Externalise scoring rubrics, thresholds, and tier definitions from your **Stage 3 Scope Document** into `config/scoring_rubric.yaml`. Tools load from this file so values are change-able without code edits.

### 4. Agent Definition (`agent.py`)

Wire the `LlmAgent` with model, instructions, tools, and (if your design uses composition) sub-agents. The `ToolConfirmation` primitive goes on tools that require HIL approval.

### 5. HIL via ToolConfirmation

ADK has a **first-class** HIL pattern:

```python
from google.adk.tools import ToolConfirmation

@FunctionTool(
    name="send_email",
    description="Send an email to a customer",
    require_confirmation=ToolConfirmation(
        confirmation_prompt="Review the email before sending:",
    ),
)
def send_email(to: str, subject: str, body: str) -> dict:
    ...
```

When the agent calls this tool, execution pauses until the human responds with approve/reject/modify. This is stronger than instruction-based pauses — the tool **cannot execute** without confirmation.

Use `ToolConfirmation` for every tool where an incorrect call has irreversible consequences: writing to systems of record, sending messages to clients, triggering external processes.

## Testing

```bash
python -m pytest tests/ -v
```

ADK integrates with Agent Engine for deployment. Use `agent engine deploy` to push the agent to Vertex AI Agent Engine for production; see the ADK docs for deployment specifics.

## Methodology Links

- [**Stage 1: Decompose**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/01-decompose/)
- [**Stage 2: Select**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/02-select/)
- [**Stage 3: Scope**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/03-scope/)
- [**Stage 4: Design**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/04-design/)
- [**Stage 5: Build**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/05-build/) — you are here
- [**Stage 6: Evaluate**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/06-evaluate/)
