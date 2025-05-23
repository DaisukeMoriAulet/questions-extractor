"""
Sub-agents package for questions extractor.

This package contains sub-agents that are part of the questions extractor system.
"""

from questions_extractor_agent.sub_agents.file_selector_agent import get_agent as get_file_selector_agent

__all__ = ["get_file_selector_agent"]