# [EPIC-1] Data Layer (Supabase)

## Overview

This EPIC covers the setup and definition of the data layer using Supabase, which will store the extracted and structured test questions.

## Goals

- Establish a robust and normalized database schema in Supabase to store test data, including questions, choices, passages, and associated metadata.
- Enable type-safe interactions with the database from the application.
- Prepare the necessary environment configurations for Supabase.

## Background / Why

- **PRD:**
    - [Data Model (`docs/prd.md#5-data-model`)](../prd.md#5-data-model)
    - [Bulk Save (Supabase) (`docs/prd.md#33-bulk-save-supabase`)](../prd.md#33-bulk-save-supabase)
- **Roadmap:** This work aligns with [Phase 0: Environment Setup & Design (`docs/roadmap.md#phase-0-environment-setup--design-week-1-2`)](../roadmap.md#phase-0-environment-setup--design-week-1-2) specifically tasks "2. Supabase Schema Creation" and "4. Data Model Diagram".
- **Task Breakdown:** [Phase 1 (`docs/mvp_breakdown.md#1-data-layer-supabase`)](../mvp_breakdown.md#1-data-layer-supabase)

## Scope

| Phase | Sub-scope             | Notes                                                                 |
| ----- | --------------------- | --------------------------------------------------------------------- |
| 1     | Data Layer (Supabase) | `init.sql` schema, ER diagram, Supabase type definitions, local `.env` setup. |

## Child Issues

These tasks are from `../mvp_breakdown.md#1-data-layer-supabase`:

- [ ] #<TASK_ID_INIT_SQL> **init.sql**: Create third normal form 7+2 tables (tests→…→choices / tags, question_tags)
- [ ] #<TASK_ID_ER_DIAGRAM> **Typed ER Diagram**: Auto‑generate with dbdiagram.io → `../er.png`
- [ ] #<TASK_ID_TYPES> **Supabase Type Definitions**: Generate `postgrest-js` script or `supabase gen types typescript`
- [ ] #<TASK_ID_ENV> **Local `.env`**: `SUPABASE_URL`, `SUPABASE_ANON_KEY`

## Acceptance Criteria / Definition of Done

- [ ] `init.sql` script successfully creates all 9 specified tables (test_forms, sections, parts, passage_sets, passages, questions, choices, tags, question_tags) with correct columns, data types, primary keys, foreign keys, and constraints in a local or development Supabase instance.
- [ ] The Entity Relationship Diagram (`../er.png`) is generated and accurately reflects the schema defined in `init.sql`.
- [ ] Supabase TypeScript types are successfully generated from the schema and committed to the repository.
- [ ] A template or actual `.env` file is created with `SUPABASE_URL` and `SUPABASE_ANON_KEY` variables, allowing for successful connection to the Supabase instance.
- [ ] All related documentation (e.g., notes on schema decisions) is updated if necessary.

## Reference

- PRD: `../prd.md`
- Roadmap: `../roadmap.md`
- MVP Breakdown: `../mvp_breakdown.md`
- Agent Architecture (for context on data usage): `../agents_arch.yaml`
