# Overview

## Parent Epic
[EPIC-1] Data Layer (Supabase)

See: [docs/issues/epic-1.md](../../docs/issues/epic-1.md)

## Background / Why

This task is to create a visual representation of the database schema.
- Quoted from `docs/mvp_breakdown.md`:
  > - [ ] **Typed ER Diagram** ― Auto‑generate with dbdiagram.io → `docs/er.png`

A clear ER diagram is crucial for:
- Understanding data relationships and database structure.
- Facilitating development and debugging.
- Onboarding new team members.
- Serving as a reference for database design discussions.

## What to do / How

1.  **Review Schema**:
    *   Familiarize yourself with the database schema defined in `init.sql`.
    *   The schema consists of 7 primary tables (`test_forms`, `sections`, `parts`, `passage_sets`, `passages`, `questions`, `choices`) and 2 auxiliary tables (`tags`, `question_tags`).
2.  **Generate Diagram with dbdiagram.io**:
    *   Go to [dbdiagram.io](https://dbdiagram.io/).
    *   Use its DSL or import functionality to represent the schema. You might be able to paste the DDL from `init.sql` if the tool supports it, or define tables manually using its syntax.
    *   Ensure all 9 tables are included.
    *   Clearly define columns, data types (if possible/easy), primary keys (PK), foreign keys (FK), and relationships (e.g., one-to-many).
3.  **Export Diagram**:
    *   Once the diagram is complete and accurate, export it as a PNG image.
4.  **Save and Commit**:
    *   Save the exported image to `docs/er.png`.
    *   Commit `docs/er.png` to the repository.

## Acceptance Criteria / AC

- [ ] The file `docs/er.png` exists in the repository.
- [ ] The ER diagram in `docs/er.png` accurately and completely represents all 9 tables (`test_forms`, `sections`, `parts`, `passage_sets`, `passages`, `questions`, `choices`, `tags`, `question_tags`) as defined in `init.sql`.
- [ ] All relationships between tables (via foreign keys) are correctly depicted with appropriate cardinality (e.g., showing which field links to which table).
- [ ] Primary keys for each table are clearly indicated.
- [ ] The diagram is legible, well-organized, and easy to understand.

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort) - N/A
- [ ] Type check (mypy | pyright) - N/A
- [ ] Docstring & comments - N/A
- [ ] Test cases added - N/A (Manual verification of diagram)
- [ ] Documentation updated (if applicable) - This task *creates* documentation (`docs/er.png`).

## Related Materials

- PRD: [`docs/prd.md`](../../docs/prd.md) (See Section 5. Data Model)
- Roadmap: [`docs/roadmap.md`](../../docs/roadmap.md) (See Phase 0, Item 4. Data Model Diagram)
- MVP Breakdown: [`docs/mvp_breakdown.md#L18`](../../docs/mvp_breakdown.md#L18)
