"""
Prompts Package
===============
Externalised prompt templates for LLM nodes. Never hardcode prompts
inside node functions — put them here as template strings so you can
iterate on wording without touching graph logic.

Each prompt module contains format-string templates with {placeholder}
variables that nodes fill in at runtime.

Methodology reference:
  - Stage 4: Design → Prompt Pattern field in Node Specifications
  - Stage 5: Build → Prompt Management, "Prompts externalised" convention
"""
