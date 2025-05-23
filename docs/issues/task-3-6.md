# Overview

## Parent Epic
[Epic 3: Tool Implementation (ADK Tool Functions)](/epic-3.md)

## Background / Why

This task involves implementing the `save_test_set` ADK tool, which is responsible for persisting the extracted, structured, and tagged test question data into the Supabase database. This is a critical step in the data processing pipeline, enabling the storage and future retrieval of question sets.

- Quote the relevant line from `mvp_breakdown.md` (line 33):
  > - [ ] **T6 `save_test_set(test_set)`** ― Supabase `upsert` (`onConflict=["part_id","number"]`)

As per `prd.md` (Section 3.3 Bulk Save and Section 4.2 Tools), this tool handles the final stage of the pipeline: saving processed data.

## What to do / How

- [ ] **Fetch and understand ADK documentation**
  * [ ] Use MCP tool `Context7` to fetch and understand ADK documentation from [Agent Development Kit (ADK) Documentation](https://google.github.io/adk-docs/).
  * [ ] Understand ADK documentation and how to use Tools and ToolContext, particularly for interacting with external services like Supabase.

- [ ] **Implement `save_test_set` Tool:**
  * [ ] Create/update the Python file for the tool (e.g., `questions_extractor_agent/tools/database_tools.py` or `questions_extractor_agent/tools/save_tool.py`, following `tools/**.py` convention from `mvp_breakdown.md`).
    *   [ ] Define the `save_test_set(test_set: dict, tool_context: ToolContext)` function signature as specified in `prd.md` (Section 4.2).
        *   Input: `test_set` (a dictionary containing the structured question data ready for DB insertion, conforming to the 7+2 table structure).
        *   Input: `tool_context` (ADK ToolContext).

- [ ] **Supabase Integration:**
  * [ ] Utilize the `supabase` library to connect to the Supabase instance (credentials should be loaded from `.env`).
  * [ ] Implement `upsert` logic for each of the tables defined in `prd.md` (Section 5. Data Model):
    *   `test_forms`
    *   `sections`
    *   `parts`
        *   `passage_sets`
        *   `passages`
        *   `questions` (implement `onConflict=["part_id","number"]`)
        *   `choices` (implement `onConflict=["question_id","label"]`)
        *   `tags`
        *   `question_tags`
    *   [ ] Ensure data is inserted/updated in the correct order to satisfy foreign key constraints. Consider the relationships between tables (e.g., a `question` belongs to a `part` and `passage_set`).
    *   [ ] Group database operations logically, potentially by `passage_set`, and perform bulk upserts within database transactions for efficiency and atomicity.
    *   [ ] Adhere to the JSONB metadata size limit (less than 8MB per row) for tables like `passage_sets` and `passages` as noted in `prd.md`.

- [ ] **Return Values:**
  * [ ] The tool must return a dictionary as specified in `prd.md` (Section 4.2): `{"status": "success" | "error", "message": "Descriptive message", "rows_upserted": integer_count}`.

- [ ] **Unit Testing:**
  * [ ] Create unit tests in `tests/tools/test_save_test_set.py` (or similar, matching the tool's file location).
  * [ ] Mock Supabase client interactions using `unittest.mock` or a similar library.
    *   [ ] Test successful data insertion for all tables.
    *   [ ] Test successful data updates (idempotency) due to `onConflict` clauses for `questions` and `choices`.
    *   [ ] Test correct handling of relationships and foreign keys.
    *   [ ] Test error handling (e.g., database errors, malformed `test_set` data).
    *   [ ] Verify the structure and content of the return values (`status`, `message`, `rows_upserted`).

## Acceptance Criteria / AC

- [ ] The `save_test_set` tool is implemented as an ADK Tool function.
- [ ] The tool correctly upserts structured test data into all 9 Supabase tables (`test_forms`, `sections`, `parts`, `passage_sets`, `passages`, `questions`, `choices`, `tags`, `question_tags`).
- [ ] `onConflict` constraints for `questions` (`part_id`, `number`) and `choices` (`question_id`, `label`) are correctly implemented and prevent duplicate entries while allowing updates.
- [ ] The tool handles bulk operations efficiently, ideally grouped by `passage_set` and within transactions.
- [ ] The tool returns the specified status, message, and `rows_upserted` count.
- [ ] Unit tests for `save_test_set` are comprehensive and pass, covering successful operations, `onConflict` behavior, and error handling.
- [ ] As per `roadmap.md` (Milestone Week 10), the implementation should support storing 1k dummy questions without duplicates, demonstrating robust `onConflict` and bulk handling.
- [ ] Consider and test for pgBouncer connection limits if applicable during integration testing (as noted in `mvp_breakdown.md` for T6 tests).

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort)
- [ ] Type check (mypy | pyright)
- [ ] Docstring & comments added, explaining the logic, especially for data mapping and Supabase interactions.
- [ ] Test cases added (as detailed in "What to do / How" and "Acceptance Criteria").
- [ ] Documentation updated (if applicable, e.g., notes on data structure expectations for `test_set`).

## Related Materials

- PRD: `docs/prd.md` (especially Sections 3.3, 4.2, 5)
- Roadmap: `docs/roadmap.md` (Phase 4: Supabase I/O, Milestone Week 10)
- MVP Breakdown: `docs/mvp_breakdown.md` (Task T6, line 33)
