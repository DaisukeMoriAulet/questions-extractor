# Overview

## Parent Epic
[Epic 3: Tool Implementation (ADK Tool Functions)](/epic-3.md)

## Background / Why

- Quote the relevant line from mvp_breakdown.md
  > | T4  | `exit_loop()`                | Set `ToolContext.actions.escalate=True`                               | -                                             |
- This tool is essential for the `file_selector_agent` to signal the `pipeline_loop_agent` to terminate its execution when there are no more files to process. It enables graceful loop control as defined in `prd.md` (section 4.2 Tools: `exit_loop` - Exit the loop if there are no unprocessed files, sets `ToolContext.actions.escalate = True`).

## What to do / How

- [ ] **Fetch and understand ADK documentation**
   * [ ] Use MCP tool `Context7` to fetch and understand ADK documentation regarding `ToolContext.actions.escalate` from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
   * [ ] Understand how setting `ToolContext.actions.escalate = True` is utilized by ADK Loop Agents to control their execution flow.
- [ ] Implement the `exit_loop(tool_context: ToolContext)` function. This function will likely reside in a new file, e.g., `questions_extractor_agent/tools/exit_loop.py`, or be added to an existing common tools file if appropriate.
- [ ] Inside the function, set `tool_context.actions.escalate = True`.
- [ ] The function should return a dictionary indicating success, for example: `{"status": "success", "message": "Loop escalation requested."}`.
- [ ] Add appropriate docstrings and type hints to the function.
- [ ] Ensure the new tool is correctly registered or made available for use by agents.

## Acceptance Criteria / AC

- [ ] The `exit_loop()` tool, when called, correctly sets `tool_context.actions.escalate = True`.
- [ ] When integrated into the `file_selector_agent` and used within the `pipeline_loop_agent`, the loop agent terminates its processing iterations as expected after `exit_loop()` is invoked.
- [ ] A basic unit test is created for the `exit_loop()` tool to verify that `tool_context.actions.escalate` is set to `True` upon execution.
- [ ] Code passes `ruff`, `black`, and `isort` checks.

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort)
- [ ] Type check (mypy | pyright)
- [ ] Docstring & comments
- [ ] Test cases added
- [ ] Documentation updated (if applicable)

## Related Materials

- PRD: `docs/prd.md` (Reference Section 4.2 Tools)
- Roadmap: `docs/roadmap.md` (This tool supports Phase 5: Reliability & Logging, specifically the `pipeline_loop_agent`)
- Break-down Line Number: 28
