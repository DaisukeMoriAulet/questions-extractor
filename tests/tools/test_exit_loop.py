"""
Tests for the exit_loop tool.
"""

from typing import Any, Dict

from questions_extractor_agent.tools.exit_loop import exit_loop


class MockToolContext:
    """
    Mock implementation of ToolContext for testing.
    """

    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.actions = MockActions()


class MockActions:
    """
    Mock implementation of ToolContext.actions for testing.
    """

    def __init__(self):
        self.escalate = False


def test_exit_loop():
    """
    Test that exit_loop correctly sets the escalate flag to True.
    """
    # Create a mock ToolContext
    tool_context = MockToolContext()

    # Verify the escalate flag is initially False
    assert tool_context.actions.escalate is False

    # Call the exit_loop function
    result = exit_loop(tool_context)

    # Verify the result
    assert result["status"] == "success"
    assert "Loop escalation requested" in result["message"]

    # Verify the escalate flag was set to True
    assert tool_context.actions.escalate is True
