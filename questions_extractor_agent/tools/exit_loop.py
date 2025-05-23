"""
Tool for exiting a loop in ADK.
"""

from typing import Dict

from google.adk.tools import ToolContext


def exit_loop(tool_context: ToolContext) -> Dict[str, str]:
    """
    Sets ToolContext.actions.escalate=True to exit the loop in the pipeline_loop_agent.

    Args:
        tool_context (ToolContext): ADK ToolContext for setting the escalation flag.

    Returns:
        Dict[str, str]: A dictionary containing:
            - status: "success"
            - message: A string indicating the loop escalation was requested.
    """
    # Set the escalate flag to True to exit the loop
    tool_context.actions.escalate = True

    # Return a success message
    return {"status": "success", "message": "Loop escalation requested."}
