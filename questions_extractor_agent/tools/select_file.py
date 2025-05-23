"""
Tool for selecting an unprocessed file and saving it as an artifact.
"""

import os
from typing import Dict, Union

from google.adk.tools import ToolContext
from google.genai import types

FILE_STATUS_UNPROCESSED = ""
FILE_STATUS_IN_PROGRESS = "in-progress"


def select_file(
    tool_context: ToolContext,
) -> Dict[str, Union[str, Dict[str, Union[str, int]]]]:
    """
    Selects an unprocessed file from context.state["files"] and saves it as an artifact.
    If no unprocessed files are available, sets context.actions.escalate=True to exit the loop.

    Args:
        tool_context (ToolContext): ADK ToolContext for accessing state and actions.

    Returns:
        Dict[str, Union[str, Dict[str, Union[str, int]]]]: A dictionary containing:
            - status: "success" or "error"
            - message: A string describing the success or error
            - file_metadata: Dictionary with filename and page_count (if success)
    """
    # Check if files exist in the state
    if "files" not in tool_context.state or not tool_context.state["files"]:
        # No files are available, set escalate to True to exit the loop
        tool_context.actions.escalate = True
        return {
            "status": "error",
            "message": "No files available for processing",
        }

    # Look for the first unprocessed file
    unprocessed_file = None
    for file_path, status in tool_context.state["files"].items():
        if status == FILE_STATUS_UNPROCESSED:  # Empty string indicates unprocessed file
            unprocessed_file = file_path
            break

    # If no unprocessed files are found, set escalate to True to exit the loop
    if unprocessed_file is None:
        tool_context.actions.escalate = True
        return {
            "status": "error",
            "message": "No unprocessed files available",
        }

    # Mark the file as in-progress to prevent reprocessing
    tool_context.state["files"][unprocessed_file] = FILE_STATUS_IN_PROGRESS

    # Set the file to process in the state
    file_name = os.path.basename(unprocessed_file)
    tool_context.state["file_to_process"] = file_name

    # Create an artifact representing the file path
    # This is just storing the path as text, not the actual file content
    file_path_part = types.Part(text=unprocessed_file)

    # Save the artifact
    tool_context.actions.save_artifact(name=file_name, content=file_path_part)

    # Get page count (assume 1 for non-PDF files)
    page_count = 1
    # For actual implementation, you might want to determine page count for PDFs, etc.

    # Return success with file metadata
    return {
        "status": "success",
        "message": f"Successfully selected file: {file_name}",
        "file_metadata": {"filename": file_name, "page_count": page_count},
    }
