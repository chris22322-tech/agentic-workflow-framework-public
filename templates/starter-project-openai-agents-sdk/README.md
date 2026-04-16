# Workflow Agent — Starter Project (OpenAI Agents SDK)

A skeleton agent built on the **OpenAI Agents SDK** from the **Stage 5: Build** methodology. This project gives you a working directory structure, placeholder function tools, and template files — ready to fill in with your Design Document (Stage 4) specifications.

> **This is the OpenAI Agents SDK variant.** Starter projects also exist for **LangGraph** (`templates/starter-project-langgraph/`) and **Google ADK** (`templates/starter-project-adk/`). The framework itself is platform-neutral; pick the starter that matches your team's chosen platform.

## How OpenAI Agents SDK maps to the framework

| Framework concept (Stage 4) | OpenAI Agents SDK primitive |
|---|---|
| **Action** | Function tool (`@function_tool`-decorated function) OR handoff to a sub-agent |
| **Memory field** | Agent context object (typed dataclass / TypedDict) passed to every tool |
| **Flow** | Agent's tool-use reasoning loop; sub-agents via handoffs |
| **HIL checkpoint** | Manual: a function tool that gates sensitive actions by returning a "needs approval" result, or a handoff to a separate "approval" agent |
| **Error handling** | Tool returns an error dict; the agent's reasoning loop sees it and chooses the next action |
| **Tool (API wrapper)** | `@function_tool`-decorated async function with typed signature |
| **Tool (MCP connector)** | Function tool wrapping an MCP client call |

**Key paradigm difference from LangGraph:** there is no explicit graph. The agent's LLM reasoning drives which tool to call next. You still have a flow in your head (from Stage 4), but you express it as **instruction text + available tools** rather than as an explicit state machine. The SDK handles tool-calling turns; you handle instructions and tool implementations.

## Quick Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your OPENAI_API_KEY and any data source credentials

# 4. Run the demo
python agent.py
```

The demo runs the agent with a placeholder tool and shows the reasoning loop. You should see the agent decide to call the tool, receive a placeholder result, and produce a final response.

## Project Structure

```
starter-project-openai-agents-sdk/
├── agent.py              # Agent definition — instructions, tools, handoffs
├── context.py            # Context object (Pydantic dataclass)
├── tools/                # One function tool per data source
│   ├── __init__.py
│   └── example_tool.py   # Template with @function_tool decorator
├── prompts/              # Externalised instruction text
│   ├── __init__.py
│   └── instructions.py   # Main agent instructions with {placeholders}
├── config/               # Domain config — edit this, not code
│   ├── scoring_rubric.yaml
│   └── report_template.md
├── tests/                # Tool unit tests
│   ├── __init__.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Customise

Work through these in order.

### 1. Context Object (`context.py`)

Open your **Design Document Section 3: Memory Fields** and define the corresponding Pydantic dataclass. Every function tool receives this context — think of it as the "shared notepad" the agent's tools can read from and write to.

### 2. Tools (`tools/`)

For each data source in your **Stage 3 Data Inventory**, copy `tools/example_tool.py` and implement the API integration. Use the `@function_tool` decorator and type your parameters — the SDK uses your types to generate the tool's JSON schema automatically. Always return an error dict on failure (don't raise) so the agent's reasoning loop can handle it.

### 3. Instructions (`prompts/instructions.py`)

This is where the **Design Document's action sequence** lives. Unlike a graph framework, OpenAI Agents SDK uses natural-language instructions to tell the agent what to do in what order, when to pause for human review, and when to hand off to a sub-agent. Write these carefully — they are the equivalent of your flow structure.

### 4. Config (`config/`)

Transfer your **Stage 3 Scope Document** decision logic — scoring rubrics, thresholds, tier definitions — into `config/scoring_rubric.yaml`. The tools load from here so you can change thresholds without code changes.

### 5. Agent Definition (`agent.py`)

Wire up the `Agent` with instructions, tools, and (if your design has multiple specialised agents) handoffs. Set `model` to the OpenAI model you've chosen — o1, gpt-4o, gpt-4o-mini, etc.

### 6. HIL Pattern

The OpenAI Agents SDK has no built-in pause-and-resume primitive. Use one of:

- **Approval-gate tool pattern**: a function tool called `request_human_approval` that returns `{"status": "pending"}` on first call. The agent is instructed to call it before any irreversible action, and your runtime handles the pending state externally (queue, notify, resume).
- **Handoff pattern**: a separate "approval" sub-agent that the main agent hands off to at HIL checkpoints.
- **Instruction-only pattern**: tell the agent in its instructions "pause and ask the human before doing X" — fragile but works for low-stakes checkpoints.

See your Design Document's HIL Interaction Design section for which pattern fits your workflow.

## Testing

```bash
# Run all tests (tool unit tests, not live API calls)
python -m pytest tests/ -v
```

Test tools in isolation — the agent's reasoning loop is hard to test without live API calls. Use evaluation datasets and the SDK's tracing features for end-to-end checks.

## Methodology Links

This starter project is part of the Agentic Workflow Framework:

- [**Stage 1: Decompose**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/01-decompose/) — Break the workflow into steps
- [**Stage 2: Select**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/02-select/) — Choose the right workflow to automate
- [**Stage 3: Scope**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/03-scope/) — Define data, logic, and boundaries
- [**Stage 4: Design**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/04-design/) — Specify actions, memory, HIL, error handling
- [**Stage 5: Build**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/05-build/) — Implement the agent (you are here)
- [**Stage 6: Evaluate**](https://chris22322-tech.github.io/agentic-workflow-framework-public/stages/06-evaluate/) — Test, measure, and iterate

Each file in this project includes comments referencing the relevant methodology section.
