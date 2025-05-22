# Overview

This EPIC covers the setup of the project repository and the development environment, which are foundational for the Questions Extractor project. These tasks ensure a consistent, high-quality codebase and smooth development workflow.

## Goals

- [ ] Establish a consistent and reproducible development environment for all contributors.
- [ ] Set up the project's foundational structure, including version control and dependency management.
- [ ] Integrate essential tooling for code quality, formatting, and automated checks (Continuous Integration).

## Background / Why

- **PRD:**
    - [7. Non-Functional Requirements (`../../docs/prd.md#7-non-functional-requirements`)](../../docs/prd.md#7-non-functional-requirements) (Execution Environment)
    - [8. Dependent Libraries & Versions (`../../docs/prd.md#8-dependent-libraries--versions`)](../../docs/prd.md#8-dependent-libraries--versions) (Core dependencies)
    - [6. Reliability & Testing (CI) (`../../docs/prd.md#6-reliability--testing`)](../../docs/prd.md#6-reliability--testing) (CI setup)
- **Roadmap:** [Phase 0: Environment Setup & Design (`../../docs/roadmap.md#phase-0-environment-setup--design-week-1-2`)](../../docs/roadmap.md#phase-0-environment-setup--design-week-1-2)
- **Task Breakdown:** [0. Repository & Development Environment (`../../docs/mvp_breakdown.md#0-repository--development-environment`)](../../docs/mvp_breakdown.md#0-repository--development-environment)

## Scope

| Phase | Sub-scope                     | Key Tasks & Notes                                                                 |
| ----- | ----------------------------- | --------------------------------------------------------------------------------- |
| 0     | Repository & Development Env. | Git & GitHub setup, Python 3.12 & Poetry, VSCode DevContainer (optional), Pre‑commit Hooks (`ruff`, `black`, `isort`), CI with GitHub Actions (YAML lint, `pytest`). |

## Child Issues (Tasks for this EPIC)

*Note: Replace `#TODO` with actual issue numbers once individual task issues are created.*

- [ ] **Repo Initialization** ― Git & GitHub setup, main branch protection rules. (#TODO)
- [ ] **Python 3.12 & Poetry Setup** ― Initialize with `poetry init` and add core dependencies: `google-adk`, `pydantic`, `supabase`, `PyPDF2`. (#TODO)
- [ ] **VSCode DevContainer (Optional)** ― Configure for Python 3.12, Poetry, and Supabase CLI. (#TODO)
- [ ] **Pre‑commit Hooks Setup** ― Integrate `ruff`, `black`, and `isort` for automated code quality checks before commits. (#TODO)
- [ ] **CI (GitHub Actions) Setup** ― Implement a workflow for YAML linting (e.g., using `act` for local testing) and running `pytest -m unit`. (#TODO)

## Acceptance Criteria / Definition of Done (for this EPIC)

- [ ] Project repository is successfully initialized on GitHub, including main branch protection rules.
- [ ] The development environment can be consistently and easily set up using Poetry with Python 3.12.
- [ ] (Optional) If implemented, the VSCode DevContainer configuration is available and functional for developers.
- [ ] Pre-commit hooks (for linting, formatting, and import sorting) are configured and automatically run, enforcing code style.
- [ ] A basic Continuous Integration (CI) pipeline using GitHub Actions is operational, performing YAML linting and executing unit tests (even if initially just placeholders).
- [ ] All child issues (individual tasks) linked to this EPIC are completed and verified.

## Reference

- Project Conventions & Setup: `CONTRIBUTING.md`
- Architectural Decisions (to be documented): `docs/architecture.md`
