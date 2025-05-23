"""
Tests for the list_files tool.
"""

import tempfile
from pathlib import Path
from typing import Any, Dict


from questions_extractor_agent.tools.list_files import list_files


class MockToolContext:
    """
    Mock implementation of ToolContext for testing.
    """

    def __init__(self):
        self.state: Dict[str, Any] = {}


def test_list_files_with_multiple_files():
    """
    Test list_files with a directory containing multiple files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        file1_path = Path(temp_dir) / "file1.txt"
        file2_path = Path(temp_dir) / "file2.txt"
        file1_path.write_text("content1")
        file2_path.write_text("content2")

        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the list_files function
        result = list_files(temp_dir, tool_context)

        # Verify the result
        assert result["status"] == "success"
        assert "Successfully listed 2 files" in result["message"]
        assert len(result["files"]) == 2
        assert str(file1_path.absolute()) in result["files"]
        assert str(file2_path.absolute()) in result["files"]

        # Verify tool_context.state was updated correctly
        assert "files" in tool_context.state
        assert len(tool_context.state["files"]) == 2
        assert str(file1_path.absolute()) in tool_context.state["files"]
        assert str(file2_path.absolute()) in tool_context.state["files"]
        assert tool_context.state["files"][str(file1_path.absolute())] == ""
        assert tool_context.state["files"][str(file2_path.absolute())] == ""


def test_list_files_empty_directory():
    """
    Test list_files with an empty directory.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the list_files function
        result = list_files(temp_dir, tool_context)

        # Verify the result
        assert result["status"] == "success"
        assert "Successfully listed 0 files" in result["message"]
        assert len(result["files"]) == 0

        # Verify tool_context.state was updated correctly
        assert "files" in tool_context.state
        assert len(tool_context.state["files"]) == 0


def test_list_files_various_file_types():
    """
    Test list_files with a directory containing various file types.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files with different extensions
        file1_path = Path(temp_dir) / "document.txt"
        file2_path = Path(temp_dir) / "image.jpg"
        file3_path = Path(temp_dir) / "data.csv"
        file1_path.write_text("text content")
        file2_path.write_text("image content")  # Not real image data, just for testing
        file3_path.write_text("csv content")  # Not real CSV data, just for testing

        # Create a subdirectory (should not be listed)
        subdir_path = Path(temp_dir) / "subdir"
        subdir_path.mkdir()
        (subdir_path / "subfile.txt").write_text("This file should not be listed")

        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the list_files function
        result = list_files(temp_dir, tool_context)

        # Verify the result
        assert result["status"] == "success"
        assert "Successfully listed 3 files" in result["message"]
        assert len(result["files"]) == 3

        # Check that all files are included and the subdirectory file is not
        assert str(file1_path.absolute()) in result["files"]
        assert str(file2_path.absolute()) in result["files"]
        assert str(file3_path.absolute()) in result["files"]
        assert str(Path(subdir_path) / "subfile.txt") not in str(result["files"])

        # Verify tool_context.state was updated correctly
        assert "files" in tool_context.state
        assert len(tool_context.state["files"]) == 3


def test_list_files_nonexistent_directory():
    """
    Test list_files with a non-existent directory.
    """
    # Create a path that definitely doesn't exist
    nonexistent_dir = "/path/that/definitely/does/not/exist"

    # Create a mock ToolContext
    tool_context = MockToolContext()

    # Call the list_files function
    result = list_files(nonexistent_dir, tool_context)

    # Verify the result
    assert result["status"] == "error"
    assert "does not exist" in result["message"]
    assert len(result["files"]) == 0

    # Verify tool_context.state was not updated
    assert (
        not tool_context.state
        or "files" not in tool_context.state
        or len(tool_context.state["files"]) == 0
    )


def test_list_files_not_a_directory():
    """
    Test list_files with a path that is not a directory.
    """
    with tempfile.NamedTemporaryFile() as temp_file:
        # Create a mock ToolContext
        tool_context = MockToolContext()

        # Call the list_files function with a file path
        result = list_files(temp_file.name, tool_context)

        # Verify the result
        assert result["status"] == "error"
        assert "is not a directory" in result["message"]
        assert len(result["files"]) == 0

        # Verify tool_context.state was not updated
        assert (
            not tool_context.state
            or "files" not in tool_context.state
            or len(tool_context.state["files"]) == 0
        )
