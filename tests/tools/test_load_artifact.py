"""
Tests for the load_artifact tool.
"""

from typing import Any, Dict
import unittest
from unittest.mock import Mock, patch

# Mock the google.adk.tools module to avoid import errors
import sys
from unittest.mock import MagicMock

# Create a mock module for google.adk.tools
mock_adk_module = MagicMock()
mock_toolcontext = MagicMock()
mock_adk_module.ToolContext = mock_toolcontext
sys.modules['google.adk.tools'] = mock_adk_module

# Now import load_artifact
from questions_extractor_agent.tools.load_artifact import load_artifact


class MockActions:
    """
    Mock implementation of the actions class for testing.
    """

    def __init__(self, artifact_exists=True, content=None):
        self.artifact_exists = artifact_exists
        self.content = content or b"mock binary content"
        self.called_with = None

    def load_artifact(self, name):
        """Mock implementation of load_artifact."""
        self.called_with = name
        if not self.artifact_exists:
            raise ValueError(f"Artifact '{name}' does not exist")
        return self.content


class MockToolContext:
    """
    Mock implementation of ToolContext for testing.
    """

    def __init__(self, artifact_exists=True, content=None):
        self.state: Dict[str, Any] = {}
        self.actions = MockActions(artifact_exists, content)


def test_load_artifact_success():
    """
    Test load_artifact with an existing artifact.
    """
    # Create a mock ToolContext with a successful load_artifact implementation
    mock_content = b"test binary content"
    tool_context = MockToolContext(content=mock_content)

    # Call the load_artifact function
    result = load_artifact("test_artifact", tool_context)

    # Verify the result
    assert result["status"] == "success"
    assert "Successfully loaded artifact" in result["message"]
    assert result["content"] == mock_content
    assert result["artifact_version"] == "test_artifact"

    # Verify that the load_artifact was called with the correct name
    assert tool_context.actions.called_with == "test_artifact"


def test_load_artifact_nonexistent():
    """
    Test load_artifact with a non-existent artifact.
    """
    # Create a mock ToolContext with a failing load_artifact implementation
    tool_context = MockToolContext(artifact_exists=False)

    # Call the load_artifact function
    result = load_artifact("nonexistent_artifact", tool_context)

    # Verify the result
    assert result["status"] == "error"
    assert "Error loading artifact" in result["message"]
    assert "does not exist" in result["message"]
    assert result["content"] is None
    assert result["artifact_version"] is None

    # Verify that the load_artifact was called with the correct name
    assert tool_context.actions.called_with == "nonexistent_artifact"


# Run the tests when executed directly
if __name__ == "__main__":
    test_load_artifact_success()
    test_load_artifact_nonexistent()
    print("All tests passed!")