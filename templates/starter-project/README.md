# Workflow Agent — Starter Project

A skeleton LangGraph agent from the **Stage 5: Build** methodology. This project gives you a working directory structure, placeholder nodes, and template files — ready to fill in with your Design Document (Stage 4) specifications.

## Quick Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env with your actual API keys

# 4. Run the demo
python agent.py
```

The demo runs the graph with placeholder logic. You should see each node execute and print the final state — no crashes, no real API calls.

## Project Structure

```
starter-project/
├── agent.py              # Graph definition — nodes, edges, compilation
├── state.py              # State schema (TypedDict)
├── tools/                # One file per data source
│   └── example_tool.py   # Template with error handling pattern
├── prompts/              # Externalised prompt templates
│   ├── analyse.py        # Analysis prompt with {placeholders}
│   └── report.py         # Report generation prompt
├── config/               # Domain config — edit this, not code
│   ├── scoring_rubric.yaml
│   └── report_template.md
├── tests/                # Tool tests, node tests, fixtures
│   ├── test_tools.py
│   ├── test_nodes.py
│   └── fixtures/
├── .env.example          # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Customise

Work through these in order — each step builds on the previous one.

### 1. State Schema (`state.py`)
Open your **Design Document Section 3: State Schema** and replace the placeholder fields with your actual state fields. Keep the category comments.

### 2. Tools (`tools/`)
For each data source in your **Stage 3 Data Inventory**, copy `tools/example_tool.py` and implement the API integration. Follow the error handling pattern: `try`/`except` → return error dict, never raise.

### 3. Prompts (`prompts/`)
Open your **Design Document Node Specifications** and look at the "Prompt Pattern" field for each LLM node. Write the actual prompts in `prompts/analyse.py` and `prompts/report.py` using `{placeholder}` variables.

### 4. Config (`config/`)
Transfer your **Stage 3 Scope Document** decision logic — scoring rubrics, thresholds, tier definitions — into `config/scoring_rubric.yaml`. Edit `config/report_template.md` to match your output format.

### 5. Node Functions (`agent.py`)
Now fill in the node implementations. Each node has a `TODO` comment pointing you to the relevant Design Document section. Follow the patterns documented in Stage 5: Build (LLM Analysis Node, LLM Generation Node, HIL Node).

### 6. Graph Wiring (`agent.py`)
Adjust the `build_graph()` function to match your Design Document's graph structure — add/remove nodes, change edge routing, modify conditional logic.

## Testing

Test incrementally — tools first, then nodes, then the full graph.

```bash
# Run all tests
python -m pytest tests/ -v

# Run just tool tests
python -m pytest tests/test_tools.py -v

# Run just node tests
python -m pytest tests/test_nodes.py -v
```

## Methodology Links

This starter project is part of the workflow agent methodology:

- [**Stage 1: Decompose**](https://chris-the-ai-guy.github.io/Workflow_Framework/stages/01-decompose/) — Break the workflow into steps
- [**Stage 2: Select**](https://chris-the-ai-guy.github.io/Workflow_Framework/stages/02-select/) — Choose the right workflow to automate
- [**Stage 3: Scope**](https://chris-the-ai-guy.github.io/Workflow_Framework/stages/03-scope/) — Define data, logic, and boundaries
- [**Stage 4: Design**](https://chris-the-ai-guy.github.io/Workflow_Framework/stages/04-design/) — Specify graph, state, nodes, and prompts
- [**Stage 5: Build**](https://chris-the-ai-guy.github.io/Workflow_Framework/stages/05-build/) — Implement the agent (you are here)
- [**Stage 6: Evaluate**](https://chris-the-ai-guy.github.io/Workflow_Framework/stages/06-evaluate/) — Test, measure, and iterate

Each file in this project includes comments referencing the relevant methodology section. Follow them to connect your Design Document to working code.
