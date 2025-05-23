# Overview

## Parent Epic

Epic 4: Agent Implementation - Building the core agent architecture for the questions extractor system.

## Background / Why

Quote the relevant line from mvp_breakdown.md:
> - [ ] **file_selector_agent** <br>└─ `select_file` / `exit_loop` | Select unprocessed file / Exit loop judgment | `tests/agents/test_file_selector.py` |

The file_selector_agent is the first agent in our processing pipeline. It's responsible for selecting unprocessed files from the input queue and determining when to exit the processing loop. This agent is critical for orchestrating the file processing workflow and ensuring all files are processed exactly once.

## What to do / How

- [ ] **Fetch and understand ADK documentation**
  * [ ] Use MCP tool `Context7` to fetch and understand ADK documentation from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
  * [ ] Understand ADK documentation and how to use Tools, ToolContext, and LlmAgent.
- [ ] **Implement file_selector_agent**
  * [ ] Create `questions_extractor_agent/sub_agents/file_selector_agent.py`
  * [ ] Implement LlmAgent with appropriate system instructions for file selection logic
  * [ ] Configure agent to use `select_file` and `exit_loop` tools
  * [ ] Add proper error handling and timeout configuration (60s for Flash model)
  * [ ] Ensure agent can access and modify context state for file tracking
- [ ] **Verify tool dependencies**
  * [ ] Ensure `select_file` tool is implemented in `questions_extractor_agent/tools/select_file.py`
  * [ ] Ensure `exit_loop` tool is implemented in `questions_extractor_agent/tools/exit_loop.py`
  * [ ] Verify tools can properly interact with `context.state["files"]` queue
- [ ] **Create comprehensive unit tests**
  * [ ] Create `tests/agents/test_file_selector.py`
  * [ ] Test file selection from non-empty queue
  * [ ] Test exit loop behavior when queue is empty
  * [ ] Test edge cases (corrupted files, permission issues)
  * [ ] Mock ToolContext and state management
  * [ ] Verify proper tool calling behavior
- [ ] **Integration with agent development UI**
  * [ ] Test individual operation with `adk web sub_agents/file_selector_agent`
  * [ ] Verify agent responds correctly to different file queue states

## Acceptance Criteria / AC

- [ ] `file_selector_agent.py` is implemented as an LlmAgent with proper configuration
- [ ] Agent successfully selects unprocessed files from `context.state["files"]`
- [ ] Agent calls `exit_loop` tool when no more files to process
- [ ] Unit tests pass with >90% code coverage
- [ ] Agent works correctly in ADK web interface for manual testing
- [ ] Error handling works for edge cases (empty queue, file access issues)
- [ ] Agent timeout is properly configured (60s for Flash model)
- [ ] Documentation includes clear system instructions and tool usage

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort)
- [ ] Type check (mypy | pyright)
- [ ] Docstring & comments
- [ ] Test cases added
- [ ] Documentation updated (if applicable)

## Related Materials

- PRD: `docs/prd.md`
- Roadmap: `docs/roadmap.md`
- Break-down Line Number: MVP Breakdown Phase 4.1 - file_selector_agent
- ADK Documentation: https://google.github.io/adk-docs/agents/llm-agents/
- Tools Documentation: https://google.github.io/adk-docs/tools/function-tools/