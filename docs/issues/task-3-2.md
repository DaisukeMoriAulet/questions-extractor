# Overview

## Parent Epic
[Epic 3: Tool Implementation (ADK Tool Functions)](./epic-3.md)

## Background / Why

- This task is to implement the `split_pdf_pages` tool, a core component for processing PDF inputs as defined in the MVP.
- Relevant line from `docs/mvp_breakdown.md` (Section 3. Tool Implementation):
  > | T2  | `split_pdf_pages(file_path)` | Save each page as JPEG using PyPDF2. Append output to `state["files"]`   | Verify the number of generated files with `MockArtifactService` |

## What to do / How

0.  **Fetch and understand ADK documentation**
    *   [ ] Use MCP tool `Context7` to fetch ADK documentation from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
    *   [ ] Understand ADK documentation and how to use `Tool` classes, `ToolContext`, `context.state`, and `context.artifact_service`.

1.  **Implement `split_pdf_pages(file_path: str, tool_context: ToolContext)` function**
    *   [ ] The function should be located in `questions_extractor_agent/tools/split_pdf_pages.py` (or a new `questions_extractor_agent/tools/split_pdf_pages.py`).
    *   [ ] **Page Extraction (PyPDF2)**:
        *   [ ] Use `PyPDF2.PdfReader` to open and read the PDF specified by `file_path`.
        *   [ ] Iterate through each page of the PDF.
    *   [ ] **Page to JPEG Conversion**:
        *   [ ] For each extracted page, convert it into a JPEG image.
            *   Note: `PyPDF2` extracts pages but doesn't directly convert to JPEG. This step will likely require an additional library (e.g., `pdf2image` which often uses Poppler, or `Pillow`). Investigate and choose a suitable library.
        *   [ ] Save each JPEG image to a temporary location or a designated output directory accessible by subsequent tools/agents.
        *   [ ] Name output files systematically, e.g., `{original_filename_without_ext}-{page_number}.jpg`.
    *   [ ] **Update ToolContext**:
        *   [ ] Append the relative paths or identifiers of the generated JPEG files to `tool_context.state["files"]`. The PRD suggests the format `tool_context.state["files"]["{filename}-{index}"] = ""`. Ensure this key format is used.
    *   [ ] **Return Value**:
        *   [ ] The function should return a dictionary indicating `status` ('success' or 'error'), a `message`, and potentially the `files` dictionary (as per PRD, though updating `tool_context.state` might be the primary mechanism).

2.  **Write Unit Tests**
    *   [ ] Create/update test file: `tests/tools/test_split_pdf_pages.py`.
    *   [ ] Use `adk.testing.MockToolContext` and mock PDF files/data.
    *   [ ] **Test Case 1: Successful Splitting & Conversion**:
        *   [ ] Verify that a sample multi-page PDF is correctly split into the expected number of JPEG files.
        *   [ ] Check that `tool_context.state["files"]` is accurately updated with the paths/keys of the generated JPEGs.
    *   [ ] **Test Case 2: Single-Page PDF**:
        *   [ ] Ensure the function handles single-page PDFs correctly (produces one JPEG).
    *   [ ] **Test Case 3 (Recommended): Error Handling**:
        *   [ ] Test behavior with a non-existent `file_path`.
        *   [ ] Test behavior with a corrupted/invalid PDF file.

3.  **Dependency Management**
    *   [ ] If a new library (like `pdf2image` or `Pillow`) is required for JPEG conversion, add it to `requirements.txt` and update any relevant dependency lock files.

## Acceptance Criteria / AC

- [ ] Unit tests for `split_pdf_pages` are implemented in `tests/tools/test_split_pdf_pages.py`.
- [ ] Unit tests pass successfully (`pytest`).
- [ ] The tool correctly splits a multi-page PDF into individual JPEG files as per specifications.
- [ ] The tool updates `tool_context.state["files"]` with the paths/keys of the generated JPEGs.
- [ ] The number of generated files can be verified (e.g., using `MockArtifactService` indirectly by checking `context.state`).
- [ ] Code adheres to `ruff`, `black`, `isort` standards.
- [ ] Function includes appropriate docstrings and comments.
- [ ] Any new dependencies are added to `requirements.txt`.

## Predefined Checklist

- [ ] Docstring & comments
- [ ] Test cases added
- [ ] Documentation updated (if applicable)

## Related Materials

- PRD: [`../prd.md`](../prd.md)
- Roadmap: [`../roadmap.md`](../roadmap.md)
- MVP Breakdown Task (from `docs/mvp_breakdown.md`):
  ```
  | T2  | `split_pdf_pages(file_path)` | Save each page as JPEG using PyPDF2. Append output to `state["files"]`   | Verify the number of generated files with `MockArtifactService` |
  ```
