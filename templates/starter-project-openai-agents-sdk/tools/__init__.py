"""Tool registry for the workflow agent.

Import each tool here so `from tools import *` gives you everything the
agent can call. Alternatively, import tools individually in agent.py.
"""

from .example_tool import fetch_example_data

__all__ = ["fetch_example_data"]
