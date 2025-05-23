# Overview

## Parent Epic
[Epic 3: Tool Implementation (ADK Tool Functions)](./epic-3.md)

## Background / Why

- Quote the relevant line from mvp_breakdown.md
  > - [ ] **T3** `select_file()` ― Select an unprocessed file and `save_artifact`; `exit_loop` if none

## What to do / How

0.  **Fetch and understand ADK documentation**
    *   [ ] Use MCP tool `Context7` to fetch and understand ADK documentation from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
    *   [ ] Understand ADK documentation on how to implement Tools, use `ToolContext`, `save_artifact`, and manage state (e.g., `context.state`, `context.actions.save_artifact`, `context.actions.escalate`).
1.  **Implement `select_file()` tool function**
    *   [ ] The function should be placed in `questions_extractor_agent/tools/select_file.py` (or a relevant shared tools module like `questions_extractor_agent/tools/file_tools.py`).
    *   [ ] It should access a list/queue of unprocessed files (e.g., from `context.state["files"]` or a similar agreed-upon state management key).
    *   [ ] It should select one file from this list that has not yet been processed. Define a clear mechanism for tracking processed/selected files.
2.  **Handle File Selection**
    *   [ ] If an unprocessed file is found:
        *   Mark the file as "selected" or "in-progress" to prevent reprocessing.
        *   Call `context.actions.save_artifact(name=<unique_artifact_name_for_file>, content=<file_content_or_path_as_bytes>)` to save the selected file's content or reference as an artifact. Clarify if the content itself or just a reference/path needs to be saved by this tool.
3.  **Handle No Files Remaining**
    *   [ ] If no unprocessed files are available in the list:
        *   Trigger the `exit_loop` behavior by setting `context.actions.escalate = True`.
4.  **Unit Testing**
    *   [ ] Create unit tests in `tests/tools/test_select_file.py`.
    *   [ ] Mock dependencies like `context.state`, `context.actions.save_artifact`, and `context.actions.escalate`.
    *   [ ] Test the scenario where unprocessed files are available and one is selected and `save_artifact` is called.
    *   [ ] Test the edge case where the list of unprocessed files is empty, ensuring `context.actions.escalate` is set to `True` and `save_artifact` is not called.

## Acceptance Criteria / AC

- [ ] `select_file()` correctly identifies and selects an unprocessed file from the available list when one exists.
- [ ] Upon selecting a file, `context.actions.save_artifact` is called appropriately for that file.
- [ ] If no unprocessed files are available, `select_file()` sets `context.actions.escalate = True`.
- [ ] Unit tests for `select_file()` are implemented in `tests/tools/test_select_file.py`.
- [ ] Unit tests cover:
    - [ ] Successful file selection and `save_artifact` call.
    - [ ] Empty file list and `exit_loop` (escalation) behavior.
- [ ] `ruff`, `black`, `isort` checks pass on the new code.
- [ ] Type checks (mypy | pyright) pass on the new code.
- [ ] Docstrings and comments are added to the `select_file()` function, explaining its purpose, parameters, and behavior.
- [ ] Setup instructions are added to README (if necessary, unlikely for this tool).

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort)
- [ ] Type check (mypy | pyright)
- [ ] Docstring & comments
- [ ] Test cases added
- [ ] Documentation updated (if applicable)

## Related Materials

- PRD: `../prd.md`
- Roadmap: `../roadmap.md`
- Break-down Line Number: `../mvp_breakdown.md` (Task T3 in section '3. Tool Implementation (ADK Tool Functions)')
