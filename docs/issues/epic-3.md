# Overview

## Goals
Implement all ADK tool functions required for the Questions Extractor pipeline as defined in the MVP. These tools are fundamental building blocks for the agent-based workflow, handling tasks from file input to data persistence.

## Background / Why
- **PRD:** [4.2 Tools](/docs/prd.md#42-tools)
- **Roadmap:** [Phase 1: File Preparation Tools (Week 3-4)](/docs/roadmap.md#phase-1-file-preparation-tools-week-3-4) and [Phase 4: Supabase I/O (Week 9-10)](/docs/roadmap.md#phase-4-supabase-io-week-9-10) (covering specific tools within this epic)
- **Task Breakdown:** [3. Tool Implementation (ADK Tool Functions)](/docs/mvp_breakdown.md#3-tool-implementation-adk-tool-functions)

## Scope

| Phase | Sub-scope                               | Notes                                                                                                |
| ----- | --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 3     | Tool Implementation (ADK Tool Functions) | Implement and test the 6 core ADK tools: `list_files`, `split_pdf_pages`, `select_file`, `exit_loop`, `load_artifact`, `save_test_set`. |

Details for each tool:
- **T1: `list_files(dir_path)`**: Write file paths directly under the specified directory to `context.state["files"]`.
- **T2: `split_pdf_pages(file_path)`**: Save each page as JPEG using PyPDF2. Append output to `state["files"]`.
- **T3: `select_file()`**: Select an unprocessed file and `save_artifact`; `exit_loop` if none.
- **T4: `exit_loop()`**: Set `ToolContext.actions.escalate=True`.
- **T5: `load_artifact(filename)`**: Return binary image.
- **T6: `save_test_set(test_set)`**: Supabase `upsert` (`onConflict=["part_id","number"]`).

## Child Issues (Automatic Close linked with Checkbox)

<!-- Placeholder: Task issues for T1-T6 will be linked here once created -->
- [ ] Task: Implement `list_files` (T1)
- [ ] Task: Implement `split_pdf_pages` (T2)
- [ ] Task: Implement `select_file` (T3)
- [ ] Task: Implement `exit_loop` (T4)
- [ ] Task: Implement `load_artifact` (T5)
- [ ] Task: Implement `save_test_set` (T6)

## Acceptance Criteria / Definition of Done

- [ ] All 6 ADK tool functions (T1-T6) are implemented as per `prd.md#4.2-Tools` and `mvp_breakdown.md#3-Tool-Implementation`.
- [ ] Unit tests for each tool function pass (`pytest tests/tools/test_*.py`).
- [ ] `list_files` correctly lists files and updates `context.state`.
- [ ] `split_pdf_pages` correctly splits PDFs into images and updates `context.state`.
- [ ] `select_file` correctly selects a file for processing or triggers `exit_loop`.
- [ ] `exit_loop` correctly sets the escalation action.
- [ ] `load_artifact` correctly loads image artifacts.
- [ ] `save_test_set` correctly upserts data to Supabase, handling conflicts.
- [ ] Code for tools is placed in `src/tools/`.
- [ ] `pytest` green & GitHub Actions success (related to tool tests).

## Reference

- PRD - Tool Specifications: [docs/prd.md#42-tools](/docs/prd.md#42-tools)
- MVP Breakdown - Tools: [docs/mvp_breakdown.md#3-tool-implementation-adk-tool-functions](/docs/mvp_breakdown.md#3-tool-implementation-adk-tool-functions)
- ADR / Tech Choices: `docs/architecture.md` (to be created)
