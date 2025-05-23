"""
Tests for the select_file tool.
"""

import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

from questions_extractor_agent.tools.select_file import select_file


class MockToolContext:
    """
    Mock implementation of ToolContext for testing.
    """

    def __init__(self):
        self.state: Dict[str, Any] = {}
        self.actions = MockActions()
        self.saved_artifacts = {}


class MockActions:
    """
    Mock implementation of ToolContext.actions for testing.
    """

    def __init__(self):
        self.escalate = False

    def save_artifact(self, name: str, content: Any) -> int:
        """
        Mock implementation of save_artifact.
        
        Args:
            name: The name of the artifact.
            content: The content of the artifact.
            
        Returns:
            int: A mock version number.
        """
        return 1  # Return a mock version number


def test_select_file_with_unprocessed_files():
    """
    Test select_file with unprocessed files available.
    """
    # Create a mock ToolContext
    tool_context = MockToolContext()
    
    # Set up the state with unprocessed files
    file1_path = "/path/to/file1.jpg"
    file2_path = "/path/to/file2.jpg"
    tool_context.state["files"] = {
        file1_path: "",  # Unprocessed
        file2_path: ""   # Unprocessed
    }
    
    # Create a spy on save_artifact
    original_save_artifact = tool_context.actions.save_artifact
    saved_artifacts = {}
    
    def save_artifact_spy(name, content):
        saved_artifacts[name] = content
        return original_save_artifact(name, content)
    
    tool_context.actions.save_artifact = save_artifact_spy
    
    # Call the select_file function
    result = select_file(tool_context)
    
    # Verify the result
    assert result["status"] == "success"
    assert "Successfully selected file" in result["message"]
    assert "file_metadata" in result
    assert "filename" in result["file_metadata"]
    assert "page_count" in result["file_metadata"]
    
    # Check that the file was marked as in-progress
    assert any(status == "in-progress" for status in tool_context.state["files"].values())
    
    # Check that file_to_process was set in the state
    assert "file_to_process" in tool_context.state
    
    # Check that save_artifact was called
    assert len(saved_artifacts) == 1
    
    # Verify that escalate was not set
    assert not tool_context.actions.escalate


def test_select_file_with_all_processed_files():
    """
    Test select_file when all files have been processed.
    """
    # Create a mock ToolContext
    tool_context = MockToolContext()
    
    # Set up the state with only processed files
    file1_path = "/path/to/file1.jpg"
    file2_path = "/path/to/file2.jpg"
    tool_context.state["files"] = {
        file1_path: "processed",  # Already processed
        file2_path: "in-progress"  # Currently being processed
    }
    
    # Create a spy on save_artifact
    original_save_artifact = tool_context.actions.save_artifact
    saved_artifacts = {}
    
    def save_artifact_spy(name, content):
        saved_artifacts[name] = content
        return original_save_artifact(name, content)
    
    tool_context.actions.save_artifact = save_artifact_spy
    
    # Call the select_file function
    result = select_file(tool_context)
    
    # Verify the result
    assert result["status"] == "error"
    assert "No unprocessed files available" in result["message"]
    
    # Verify that save_artifact was not called
    assert len(saved_artifacts) == 0
    
    # Verify that escalate was set to True
    assert tool_context.actions.escalate


def test_select_file_with_no_files():
    """
    Test select_file when there are no files in the state.
    """
    # Create a mock ToolContext
    tool_context = MockToolContext()
    
    # Set up the state with no files dictionary
    tool_context.state["files"] = {}
    
    # Create a spy on save_artifact
    original_save_artifact = tool_context.actions.save_artifact
    saved_artifacts = {}
    
    def save_artifact_spy(name, content):
        saved_artifacts[name] = content
        return original_save_artifact(name, content)
    
    tool_context.actions.save_artifact = save_artifact_spy
    
    # Call the select_file function
    result = select_file(tool_context)
    
    # Verify the result
    assert result["status"] == "error"
    assert "No files available for processing" in result["message"]
    
    # Verify that save_artifact was not called
    assert len(saved_artifacts) == 0
    
    # Verify that escalate was set to True
    assert tool_context.actions.escalate


def test_select_file_with_no_files_key():
    """
    Test select_file when there is no files key in the state.
    """
    # Create a mock ToolContext
    tool_context = MockToolContext()
    
    # Set up the state with no files key
    # Intentionally not setting tool_context.state["files"]
    
    # Create a spy on save_artifact
    original_save_artifact = tool_context.actions.save_artifact
    saved_artifacts = {}
    
    def save_artifact_spy(name, content):
        saved_artifacts[name] = content
        return original_save_artifact(name, content)
    
    tool_context.actions.save_artifact = save_artifact_spy
    
    # Call the select_file function
    result = select_file(tool_context)
    
    # Verify the result
    assert result["status"] == "error"
    assert "No files available for processing" in result["message"]
    
    # Verify that save_artifact was not called
    assert len(saved_artifacts) == 0
    
    # Verify that escalate was set to True
    assert tool_context.actions.escalate