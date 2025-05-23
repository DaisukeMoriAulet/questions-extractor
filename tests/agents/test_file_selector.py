"""
Tests for the file_selector_agent.
"""

import os
from typing import Any, Dict, List, Optional
from unittest import mock

import pytest
from google.adk.testing import MockSession, MockedToolCall, MockToolHandler, mock_runner
from google.genai.types import Content, Part

from questions_extractor_agent.sub_agents.file_selector_agent import get_agent
from questions_extractor_agent.tools.select_file import FILE_STATUS_UNPROCESSED, FILE_STATUS_IN_PROGRESS


def test_agent_initialization():
    """Test that the file_selector_agent can be initialized properly."""
    agent = get_agent()
    assert agent.name == "file_selector_agent"
    assert agent.model == "gemini-2.0-flash"
    assert len(agent.tools) == 2
    
    # Verify the tool names
    tool_names = [tool.name for tool in agent.tools]
    assert "select_file" in tool_names
    assert "exit_loop" in tool_names


@pytest.mark.asyncio
async def test_file_selection_with_files_available():
    """
    Test that the agent correctly selects a file when files are available.
    """
    # Initialize the agent
    agent = get_agent()
    
    # Set up the mock session with files in the state
    mock_session = MockSession(
        state={
            "files": {
                "/path/to/file1.jpg": FILE_STATUS_UNPROCESSED,
                "/path/to/file2.jpg": FILE_STATUS_UNPROCESSED,
            }
        }
    )
    
    # Set up mock tool handlers
    mock_tool_handlers = [
        # Mock the select_file tool to return success
        MockToolHandler(
            tool_name="select_file",
            response={
                "status": "success", 
                "message": "Successfully selected file: file1.jpg",
                "file_metadata": {"filename": "file1.jpg", "page_count": 1},
            }
        )
    ]
    
    # Run the agent with a mock runner
    async with mock_runner(
        agent=agent, 
        session=mock_session,
        mock_tool_handlers=mock_tool_handlers,
    ) as runner:
        # Simulate a request to select a file
        user_message = Content(parts=[Part(text="Please select a file to process.")])
        response = await runner.run_async(user_message)
        
        # Check that the agent called the select_file tool
        assert any(call.tool.name == "select_file" for call in runner.tool_calls)
        
        # Check the response mentions the selected file
        assert "file1.jpg" in response.text.lower()
        assert "success" in response.text.lower()


@pytest.mark.asyncio
async def test_exit_loop_when_no_files():
    """
    Test that the agent correctly exits the loop when no files are available.
    """
    # Initialize the agent
    agent = get_agent()
    
    # Set up the mock session with empty files in the state
    mock_session = MockSession(
        state={
            "files": {}  # Empty file dictionary
        }
    )
    
    # Set up mock tool handlers
    mock_tool_handlers = [
        # Mock the select_file tool to return error
        MockToolHandler(
            tool_name="select_file",
            response={
                "status": "error",
                "message": "No files available for processing",
            }
        ),
        # Mock the exit_loop tool
        MockToolHandler(
            tool_name="exit_loop",
            response={
                "status": "success",
                "message": "Loop escalation requested.",
            }
        )
    ]
    
    # Run the agent with a mock runner
    async with mock_runner(
        agent=agent, 
        session=mock_session,
        mock_tool_handlers=mock_tool_handlers,
    ) as runner:
        # Simulate a request to select a file
        user_message = Content(parts=[Part(text="Please select a file to process.")])
        response = await runner.run_async(user_message)
        
        # Check that the agent called both tools in the expected order
        tool_calls = [call.tool.name for call in runner.tool_calls]
        assert "select_file" in tool_calls
        assert "exit_loop" in tool_calls
        
        # Check the response mentions no files and processing complete
        assert "no files" in response.text.lower() or "no more files" in response.text.lower()
        assert "complete" in response.text.lower() or "finished" in response.text.lower()


@pytest.mark.asyncio
async def test_file_selection_with_all_processed_files():
    """
    Test that the agent correctly handles the case when all files are processed.
    """
    # Initialize the agent
    agent = get_agent()
    
    # Set up the mock session with only processed files in the state
    mock_session = MockSession(
        state={
            "files": {
                "/path/to/file1.jpg": FILE_STATUS_IN_PROGRESS,
                "/path/to/file2.jpg": "processed",
            }
        }
    )
    
    # Set up mock tool handlers
    mock_tool_handlers = [
        # Mock the select_file tool to return error
        MockToolHandler(
            tool_name="select_file",
            response={
                "status": "error",
                "message": "No unprocessed files available",
            }
        ),
        # Mock the exit_loop tool
        MockToolHandler(
            tool_name="exit_loop",
            response={
                "status": "success",
                "message": "Loop escalation requested.",
            }
        )
    ]
    
    # Run the agent with a mock runner
    async with mock_runner(
        agent=agent, 
        session=mock_session,
        mock_tool_handlers=mock_tool_handlers,
    ) as runner:
        # Simulate a request to select a file
        user_message = Content(parts=[Part(text="Please select a file to process.")])
        response = await runner.run_async(user_message)
        
        # Check that the agent called the select_file tool
        assert any(call.tool.name == "select_file" for call in runner.tool_calls)
        
        # Check that the agent called the exit_loop tool
        assert any(call.tool.name == "exit_loop" for call in runner.tool_calls)
        
        # Check the response mentions no unprocessed files
        assert "no unprocessed files" in response.text.lower() or "all files processed" in response.text.lower()


@pytest.mark.asyncio
async def test_error_handling_with_corrupted_file():
    """
    Test that the agent handles errors when there's a corrupted file.
    """
    # Initialize the agent
    agent = get_agent()
    
    # Set up the mock session with files in the state
    mock_session = MockSession(
        state={
            "files": {
                "/path/to/corrupted_file.jpg": FILE_STATUS_UNPROCESSED,
            }
        }
    )
    
    # Set up mock tool handlers
    mock_tool_handlers = [
        # Mock the select_file tool to simulate a corrupted file error
        MockToolHandler(
            tool_name="select_file",
            response={
                "status": "error",
                "message": "File access error: The file appears to be corrupted",
            }
        ),
        # Mock the exit_loop tool
        MockToolHandler(
            tool_name="exit_loop",
            response={
                "status": "success",
                "message": "Loop escalation requested.",
            }
        )
    ]
    
    # Run the agent with a mock runner
    async with mock_runner(
        agent=agent, 
        session=mock_session,
        mock_tool_handlers=mock_tool_handlers,
    ) as runner:
        # Simulate a request to select a file
        user_message = Content(parts=[Part(text="Please select a file to process.")])
        response = await runner.run_async(user_message)
        
        # Check that the agent called the select_file tool
        assert any(call.tool.name == "select_file" for call in runner.tool_calls)
        
        # Check the response mentions the error
        assert "error" in response.text.lower()
        assert "corrupted" in response.text.lower()


@pytest.mark.asyncio
async def test_permission_error_handling():
    """
    Test that the agent handles permission errors when accessing files.
    """
    # Initialize the agent
    agent = get_agent()
    
    # Set up the mock session with files in the state
    mock_session = MockSession(
        state={
            "files": {
                "/path/to/restricted_file.jpg": FILE_STATUS_UNPROCESSED,
            }
        }
    )
    
    # Set up mock tool handlers
    mock_tool_handlers = [
        # Mock the select_file tool to simulate a permission error
        MockToolHandler(
            tool_name="select_file",
            response={
                "status": "error",
                "message": "Permission denied: Cannot access the file",
            }
        ),
        # Mock the exit_loop tool
        MockToolHandler(
            tool_name="exit_loop",
            response={
                "status": "success",
                "message": "Loop escalation requested.",
            }
        )
    ]
    
    # Run the agent with a mock runner
    async with mock_runner(
        agent=agent, 
        session=mock_session,
        mock_tool_handlers=mock_tool_handlers,
    ) as runner:
        # Simulate a request to select a file
        user_message = Content(parts=[Part(text="Please select a file to process.")])
        response = await runner.run_async(user_message)
        
        # Check that the agent called the select_file tool
        assert any(call.tool.name == "select_file" for call in runner.tool_calls)
        
        # Check the response mentions the permission error
        assert "permission" in response.text.lower() or "access" in response.text.lower()
        assert "denied" in response.text.lower() or "error" in response.text.lower()


def test_agent_timeout_configuration():
    """Test that the file_selector_agent respects the task_timeout parameter."""
    # Test with default timeout
    agent_default = get_agent()
    assert agent_default.task_timeout == 60
    
    # Test with custom timeout
    custom_timeout = 30
    agent_custom = get_agent(task_timeout=custom_timeout)
    assert agent_custom.task_timeout == custom_timeout