# Overview

## Parent Epic
[Epic 3: Tool Implementation (ADK Tool Functions)](/epic-3.md)

## Background / Why

- Quote the relevant line from mvp_breakdown.md
  > - [ ] **T5** `load_artifact(filename)` ― Return binary image

## What to do / How

- [ ] **Fetch and understand ADK documentation**
  * [ ] Use MCP tool `Context7` to fetch and understand ADK documentation from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
  * [ ] Understand ADK documentation on how to implement Tools, use `ToolContext`, and specifically how `context.actions.load_artifact(name=<artifact_name>)` works.
- [ ] **Implement `load_artifact(filename)` tool function**
  * [ ] The function should be placed in `questions_extractor_agent/tools/load_artifact.py` (or a relevant shared tools module like `questions_extractor_agent/tools/file_tools.py`).
  * [ ] The function should accept a `filename` (or artifact name) as an argument. This name corresponds to an artifact previously saved using `save_artifact`.
    *   [ ] Inside the function, call `context.actions.load_artifact(name=filename)` to retrieve the artifact content.
    *   [ ] The function should return the binary content of the loaded artifact.
- [ ] **Error Handling & Constraints**
  * [ ] Implement checks for artifact existence. What should happen if the artifact specified by `filename` does not exist? (e.g., raise an error, return None, log a warning).
  * [ ] Consider and document any size limits for artifacts being loaded. While `load_artifact` itself might handle large files, the tool's usage context (e.g., passing to an LLM) might have practical limits.
- [ ] **Unit Testing**
  * [ ] Create unit tests in `tests/tools/test_load_artifact.py`.
  * [ ] Mock `ToolContext` and `context.actions.load_artifact`.
    *   [ ] Test the successful loading of an artifact, where `context.actions.load_artifact` is called with the correct name and its return value is propagated.
    *   [ ] Test the scenario where the specified artifact does not exist (how `context.actions.load_artifact` behaves in this case and how your tool handles it).
    *   [ ] If applicable, test size limit considerations (this might be more of a note if the underlying ADK call handles it).

## Acceptance Criteria / AC

- [ ] `load_artifact(filename)` tool correctly calls `context.actions.load_artifact(name=filename)`.
- [ ] The tool returns the binary image/content retrieved by `context.actions.load_artifact`.
- [ ] The tool includes basic error handling for non-existent artifacts (e.g., logs an error or raises an exception).
- [ ] Unit tests for `load_artifact()` are implemented in `tests/tools/test_load_artifact.py`.
- [ ] Unit tests cover:
    - [ ] Successful artifact loading.
    - [ ] Attempting to load a non-existent artifact.
- [ ] `ruff`, `black`, `isort` checks pass on the new code.
- [ ] Type checks (mypy | pyright) pass on the new code.
- [ ] Docstrings and comments are added to the `load_artifact()` function.

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort)
- [ ] Type check (mypy | pyright)
- [ ] Docstring & comments
- [ ] Test cases added
- [ ] Documentation updated (if applicable)

## Related Materials

- PRD: `../prd.md`
- Roadmap: `../roadmap.md`
- Break-down Line Number: `../mvp_breakdown.md` (Task T5 in section '3. Tool Implementation (ADK Tool Functions)')
