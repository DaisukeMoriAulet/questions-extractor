"""
File selector agent for selecting unprocessed files from the input queue.

This agent is responsible for:
1. Selecting unprocessed files from the context.state["files"] queue
2. Exiting the processing loop when no more files are available
"""

from typing import List

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool

from questions_extractor_agent.tools.select_file import select_file
from questions_extractor_agent.tools.exit_loop import exit_loop


def get_agent(task_timeout: int = 60) -> LlmAgent:
    """
    Creates and returns the file_selector_agent as an LlmAgent.
    
    This agent selects unprocessed files from the input queue and determines
    when to exit the processing loop based on file availability.
    
    Args:
        task_timeout (int): Timeout in seconds for the agent task. Default is 60s for Flash model.
        
    Returns:
        LlmAgent: Configured file selector agent
    """
    # Define the tools for the agent
    tools: List[BaseTool] = [select_file, exit_loop]
    
    # Agent system instruction
    instruction = """
    You are a file selector agent responsible for selecting unprocessed files from a queue and 
    determining when to exit the processing loop.
    
    Your responsibilities:
    1. Select the next unprocessed file from the queue when requested
    2. Signal when there are no more files to process
    
    When asked to select a file:
    - Use the `select_file` tool to get the next unprocessed file from context.state["files"]
    - If a file is available, it will be marked as "in-progress" and saved as an artifact
    - If no files are available, the `select_file` tool will set escalate=True automatically
    
    When asked if processing should continue:
    - Check if there are any unprocessed files remaining
    - If no unprocessed files remain, use the `exit_loop` tool to signal the end of processing
    - The `exit_loop` tool sets context.actions.escalate=True to exit the loop
    
    Always respond clearly, stating whether a file was selected or if processing is complete.
    """
    
    # Create and return the LlmAgent instance
    return LlmAgent(
        model="gemini-2.0-flash",
        name="file_selector_agent",
        instruction=instruction,
        tools=tools,
        task_timeout=task_timeout,  # Default 60s for Flash model
    )