# Overview

## Parent Epic
<!-- TODO: Add Parent Epic if applicable -->

## Background / Why

- This task is part of setting up the data layer for the Questions Extractor application. Accurate type definitions are crucial for type safety and developer productivity when interacting with the Supabase database.
- Quote from `docs/mvp_breakdown.md`:
  > - [ ] **Supabase Type Definitions** ― Generate `postgrest-js` script or `supabase gen types typescript`

## What to do / How

1.  **Generate Supabase Type Definitions**:
    *   Use the Supabase CLI command: `supabase gen types typescript --project-id <your-project-id> > src/types/supabase.ts`
        *   Note: You will need to replace `<your-project-id>` with the actual project ID from your Supabase project. This ID can typically be found in your Supabase project's dashboard URL (e.g., `https://app.supabase.com/project/<your-project-id>`) or by running `supabase projects list`.
    *   Alternatively, explore generating types using a `postgrest-js` script if more customization is needed, though the CLI is generally recommended.
2.  **Save and Verify Generated Types**:
    *   Save the output to `src/types/supabase.ts` (or create this directory if it doesn't exist).
    *   Review the generated `supabase.ts` file to ensure it contains interfaces/types for all tables and columns defined in `supabase/init.sql`.
    *   Check for correctness of types (e.g., `string`, `number`, `boolean`, custom types like `jsonb` fields).
3.  **Integrate and Document**:
    *   Ensure the generated types can be imported and used within the application's TypeScript code, for example, when initializing the Supabase client or querying data.
    *   Add `src/types/supabase.ts` to `.gitignore` if it's not already covered, to prevent committing generated files if that's the project policy (though often these are committed).
    *   Document the command for generating/regenerating types in the project's `README.md` or a development setup guide.

## Acceptance Criteria / AC

- [ ] TypeScript type definitions for the Supabase database schema are successfully generated using `supabase gen types typescript --project-id <your-project-id> > src/types/supabase.ts`.
- [ ] The generated `src/types/supabase.ts` file accurately reflects all tables, columns, data types, and relationships defined in `supabase/init.sql`.
- [ ] The types can be imported and utilized in other parts of the codebase (e.g., when using the `supabase-js` client) enhancing type safety without type errors.
- [ ] The command and procedure for generating/regenerating types are documented in the project's `README.md`.

## Predefined Checklist

- [ ] Code style unified (ruff/black/isort) - N/A for generated files, but applies to scripts if created.
- [ ] Type check (mypy | pyright) - The generated types should pass type checking when used.
- [ ] Docstring & comments - N/A for generated files.
- [ ] Test cases added - N/A for type generation itself, but consuming code should be type-checked.
- [ ] Documentation updated (if applicable) - README updated with generation instructions.

## Related Materials

- PRD: [`docs/prd.md`](../../docs/prd.md) (Specifically Section 5: Data Model)
- Roadmap: [`docs/roadmap.md`](../../docs/roadmap.md) (Specifically Phase 0: Environment Setup & Design)
- MVP Breakdown: [`docs/mvp_breakdown.md`](../../docs/mvp_breakdown.md) (Line 19)
