"""
Tool for loading artifacts from the tool context.
"""

from typing import Dict, Union, Optional

# Import google.adk.tools or a mock if it's not available
try:
    from google.adk.tools import ToolContext
except ImportError:
    # Creating a placeholder for ToolContext for testing/development
    class ToolContext:
        """Mock ToolContext class for development when google.adk is not available."""
        pass


def load_artifact(
    filename: str, tool_context: ToolContext
) -> Dict[str, Union[str, Optional[bytes]]]:
    """
    Load binary content of an artifact previously saved using save_artifact.

    Args:
        filename (str): Name of the artifact to load.
        tool_context (ToolContext): ADK ToolContext for accessing artifacts.

    Returns:
        Dict[str, Union[str, Optional[bytes]]]: A dictionary containing:
            - status: "success" or "error"
            - message: A string describing the success or error
            - content: The binary content of the artifact (if successful), None otherwise
            - artifact_version: A string identifier for the artifact version (if successful)
    """
    try:
        # Attempt to load the artifact using the context.actions.load_artifact method
        artifact_content = tool_context.actions.load_artifact(name=filename)
        
        return {
            "status": "success",
            "message": f"Successfully loaded artifact '{filename}'",
            "content": artifact_content,
            "artifact_version": filename  # In ADK, the artifact version is typically the name used to load it
        }
    except Exception as e:
        # Handle any errors that occur during the loading process
        return {
            "status": "error",
            "message": f"Error loading artifact '{filename}': {str(e)}",
            "content": None,
            "artifact_version": None
        }