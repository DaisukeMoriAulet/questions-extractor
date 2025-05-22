# Overview

## Parent Epic
Relates to: [EPIC-3 Implement File Handling & Preprocessing Core](epic-3.md)

## Background / Why

This task is to implement the `list_files` tool, a foundational component for the `file_preparator_agent`. It enables the system to discover input files for processing.

As per `mvp_breakdown.md`:
> | T1  | `list_files(dir_path)`       | Write file paths directly under the specified directory to `context.state["files"]` | `pytest tests/tools/test_list_files.py`     |

## What to do / How

0. **Fetch and understand ADK documentation**
   * [ ] Use MCP tool `Context7` to fetch ADK documentation from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
   * [ ] Understand ADK documentation and how to use Tools and ToolContext.

1.  **Implement the `list_files` tool function.**
    *   **Location:** Create `questions_extractor_agent/tools/list_files.py` (or integrate into an existing relevant tools module under `questions_extractor_agent/tools/`).
    *   **Function Signature (from PRD):** `def list_files(dir_path: str, tool_context: ToolContext) -> dict:`
        *   The return type should be a dictionary structured as: `{"status": "success" | "error", "message": str, "files": dict}`.
    *   **Functionality:**
        *   Accepts `dir_path` (string) and `tool_context` (ADK `ToolContext`).
        *   Lists all file paths directly under the `dir_path`. It should not be recursive.
        *   Stores the discovered file paths in `tool_context.state["files"]` and `ToolContext.state["files"][{filename}] = ""`.
            *   The property {filename} shows the existence of the file.
            *   The value "" is a placeholder, meaning this file is not processed yet.
    *   **Return Value (from PRD):** A dictionary containing:
        *   `status: "success"` or `"error"`
        *   `message: str` (describing success or error)
        *   `files: dict` (a dictionary of the files found, e.g., `{filename1: "", filename2: ""}`)

2.  **Create Unit Tests.**
    *   **Location:** `tests/tools/test_list_files.py`.
    *   **Coverage:**
        *   Test with a directory containing multiple files.
        *   Test with an empty directory.
        *   Test with a directory containing various file types.
        *   Test handling of a non-existent `dir_path` (should return an error status and appropriate message).
        *   Verify that `tool_context.state["files"]` is correctly populated as per the specifications.
    *   **Mocking:** Use Python's `pathlib` and `tempfile` modules for creating test directories and files. An approach to mock the `ToolContext` might be necessary.

## Acceptance Criteria / AC

- [ ] `list_files` function is implemented in `questions_extractor_agent/tools/` as per the specifications outlined in `prd.md` and `mvp_breakdown.md`.
- [ ] The function correctly lists files from a given directory path and populates `tool_context.state["files"]` in the specified format.
- [ ] The function returns a dictionary with `status`, `message`, and `files` keys as specified.
- [ ] The function handles edge cases, such as empty or non-existent directories, gracefully by returning an appropriate error status and message.
- [ ] Comprehensive unit tests are written in `tests/tools/test_list_files.py`, covering various scenarios including edge cases, and all tests pass.
- [ ] The code adheres to project styling (ruff, black, isort) and quality standards (type hints, docstrings).

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort run and pass).
- [ ] Type hints are used, and type checks (mypy | pyright) pass.
- [ ] Docstrings and comments are clear and comprehensive, explaining the function's purpose, arguments, return value, and any non-obvious logic.
- [ ] All specified unit test cases are implemented and pass.
- [ ] Documentation (e.g., README, tool usage in agent docs) updated if necessary.

## Related Materials

- PRD: [`../prd.md`](../prd.md) (Section 4.2 Tools - `list_files`)
- Roadmap: [`../roadmap.md`](../roadmap.md) (Phase 1: File Preparation Tools)
- MVP Breakdown: [`../mvp_breakdown.md`](../mvp_breakdown.md) (Section 3. Tool Implementation, ID T1)
- Agent Architecture: [`../agents_arch.yaml`](../agents_arch.yaml)
