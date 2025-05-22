# Overview

## Parent Epic
[epic-1.md](./epic-1.md)

## Background / Why

- Quote the relevant line from mvp_breakdown.md
  > - [ ] **init.sql** ― Create third normal form 7+2 tables (tests→…→choices / tags, question_tags)

## What to do / How

1. Define the schema for the 7 main tables as specified in `prd.md` (Section 5. Data Model): `test_forms`, `sections`, `parts`, `passage_sets`, `passages`, `questions`, `choices`.
2. Define the schema for the 2 auxiliary tables: `tags`, `question_tags`.
3. Ensure all tables are designed in third normal form (3NF) to minimize data redundancy and improve data integrity.
4. Implement primary keys, foreign keys, constraints (e.g., `UNIQUE`, `NOT NULL`), and appropriate data types for all columns based on `prd.md`.
5. Save the complete SQL script as `init.sql` in the appropriate directory (e.g., `supabase/migrations/` or a similar standard location for database migrations).

## Acceptance Criteria / AC

- [x] The `init.sql` script can be executed successfully against a Supabase Postgres database without errors.
- [x] All 9 tables (`test_forms`, `sections`, `parts`, `passage_sets`, `passages`, `questions`, `choices`, `tags`, `question_tags`) are created with the correct columns, data types, and constraints as defined in `prd.md` (Section 5. Data Model).
- [x] Relationships between tables (foreign keys) are correctly established and enforced.
- [x] The schema adheres to third normal form principles.

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort)
- [ ] Type check (mypy | pyright)
- [ ] Docstring & comments
- [ ] Test cases added
- [ ] Documentation updated (if applicable)

## Related Materials

- PRD: `../../docs/prd.md`
- Roadmap: `../../docs/roadmap.md`
- Break-down Line Number: `16`
