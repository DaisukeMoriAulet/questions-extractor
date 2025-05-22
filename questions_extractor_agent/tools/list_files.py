"""
Tool for listing files in a directory.
"""

from pathlib import Path
from typing import Dict, Union

from google.adk.tools import ToolContext


def list_files(
    dir_path: str, tool_context: ToolContext
) -> Dict[str, Union[str, Dict[str, str]]]:
    """
    Lists all file paths directly under the specified directory (non-recursively).

    Args:
        dir_path (str): Path to the directory to list files from.
        tool_context (ToolContext): ADK ToolContext for storing the file information.

    Returns:
        Dict[str, Union[str, Dict[str, str]]]: A dictionary containing:
            - status: "success" or "error"
            - message: A string describing the success or error
            - files: A dictionary of the files found (filename as key, "" as value)
    """
    directory = Path(dir_path)

    # Check if directory exists
    if not directory.exists():
        return {
            "status": "error",
            "message": f"Directory '{dir_path}' does not exist",
            "files": {},
        }

    # Check if path is a directory
    if not directory.is_dir():
        return {
            "status": "error",
            "message": f"'{dir_path}' is not a directory",
            "files": {},
        }

    # List files (non-recursively)
    found_files = {}
    try:
        # Get only files, not directories
        for item in directory.iterdir():
            if item.is_file():
                # Use absolute path for the key
                found_files[str(item.absolute())] = ""
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error listing files in directory '{dir_path}': {str(e)}",
            "files": {},
        }

    # Initialize files dict in tool_context if it doesn't exist
    if "files" not in tool_context.state:
        tool_context.state["files"] = {}

    # Store the files in the tool_context.state
    for file_path, value in found_files.items():
        tool_context.state["files"][file_path] = value

    # Return the result
    return {
        "status": "success",
        "message": f"Successfully listed {len(found_files)} files in '{dir_path}'",
        "files": found_files,
    }
