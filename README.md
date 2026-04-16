# Agentic Workflow Framework

A structured, platform-neutral methodology for identifying, designing, and building agentic workflows for knowledge workers.

**Live site:** https://chris22322-tech.github.io/agentic-workflow-framework/ *(enabled on first successful deploy)*

---

## What this is

Six stages — **Decompose**, **Select**, **Scope**, **Design**, **Build**, **Evaluate** — that take a knowledge worker from "I have a repetitive job" to "I have a production AI agent doing the repetitive parts, and I'm reviewing what matters."

Deliberately **platform-neutral**: the framework teaches you *what* to design and build (actions, memory fields, HIL checkpoints, flow structure), not *which* agent framework or LLM provider to use. When you reach the build stage, you pick your own stack.

## Who it's for

- **Knowledge workers** — CSMs, Account Managers, Operations leads. You know your job has repeatable shapes; this framework gives you a systematic way to turn one into an agent. You can complete Stages 1-3 with nothing more than a text editor.
- **Business Analysts** — process-mapping is what you already do. Apply it to automation candidates. See the BA worked example.
- **Software Engineers** — pick up at Stage 4 with a scoped workflow and build from there. The platform cheat sheet maps framework concepts to the primitives in common agent frameworks (LangGraph, CrewAI, ADK, OpenAI Agents SDK, Vertex AI Agent Designer).

## Run the site locally

```bash
git clone https://github.com/chris22322-tech/agentic-workflow-framework.git
cd agentic-workflow-framework
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000/>.

## Personalise for your organisation

Under `personalise/` there are three single-file prompts that let you generate a tailored Application Guide, Training Materials, or a full branded site fork for your own org. Each file contains both the organisation config (you fill in the top) and the LLM instructions (the AI reads and executes) in one document.

Runnable from any capable LLM CLI — Claude Code, Gemini CLI, OpenAI, or pasted into a web chat. See `docs/personalise/` for walkthroughs of each layer.

## Repository layout

```
docs/              # The published framework (six stages, worked examples, reference)
  stages/          # The six-stage methodology
  worked-example*/ # Three complete walkthroughs (CSM, BA, SE)
  reference/       # Glossary, decision trees, checklist, platform cheat sheet
  personalise/     # User-facing docs for the personalise feature
personalise/       # The personalise tooling itself
  PERSONALISE-L1-APPLICATION-GUIDE.md
  PERSONALISE-L2-TRAINING-MATERIALS.md
  PERSONALISE-L3-CUSTOM-SITE.md
  fork.py          # Layer 3 automation (runs via Claude Code or Gemini CLI)
  prompts/         # Prompt library for generated content
  org-config-template.yaml
templates/         # Blank templates for each stage's artifacts (CSV + XLSX + DOCX)
scripts/           # Production-check script (mkdocs build + link integrity)
mkdocs.yml         # Site config
```

## Contributing

PRs welcome. Keep the framework platform-neutral (no code-first primitives in the methodology pages), follow the vocabulary conventions (`action` / `memory` / `flow` — not `node` / `state` / `graph`), and run `python scripts/production_check.py` before submitting. The script enforces strict mkdocs build, link integrity, template-methodology sync, and nav resolution.

## Licence

See [LICENSE](LICENSE). MIT.
