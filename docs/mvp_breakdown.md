# MVP Breakdown

This document breaks down the minimum viable product (MVP) requirements defined in **prd.md** and **roadmap.md** into *task-level* items, assuming AI coding. Completing the checkboxes sequentially will result in the MVP.

---

## 0. Repository & Development Environment

* [x] **Repo Initialization** ― Git & GitHub / Set up main branch protection rules
* [x] **Python 3.12 & pip** ― `python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
* ~~[ ] **VSCode DevContainer (optional)** ― Python 3.12 / Supabase CLI~~
* ~~[ ] **Pre‑commit Hooks** ― `ruff`, `black`, `isort`~~
* ~~[ ] **CI (GitHub Actions)** ― YAML lint with `act` + `pytest -m unit`~~

## 1. Data Layer (Supabase)

* [ ] **init.sql** ― Create third normal form 7+2 tables (tests→…→choices / tags, question\_tags)
* [ ] **Typed ER Diagram** ― Auto‑generate with dbdiagram.io → `docs/er.png`
* [ ] **Supabase Type Definitions** ― Generate `postgrest-js` script or `supabase gen types typescript`
* [ ] **Local `.env`** ― `SUPABASE_URL`, `SUPABASE_ANON_KEY`

## 2. Common Utilities

* [ ] **logging.py** ― structured log (`filename`, `page`, `gemini_request_id`)
* [ ] **backoff.py** ― `exponential_backoff(jitter=True, retries=3)`
* [ ] **paths.py** ― Input/output directory constants `INPUT_DIR`, `TMP_DIR`, `ARTIFACT_DIR`

## 3. Tool Implementation (ADK Tool Functions)

| ID  | Tool                          | Key Points                                                              | Test                                          |
| :-- | :---------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------- |
| T1  | `list_files(dir_path)`       | Write file paths directly under the specified directory to `context.state["files"]` | `pytest tests/tools/test_list_files.py`     |
| T2  | `split_pdf_pages(file_path)` | Save each page as JPEG using PyPDF2. Append output to `state["files"]`   | Verify the number of generated files with `MockArtifactService` |
| T3  | `select_file()`              | Select an unprocessed file and `save_artifact`; `exit_loop` if none     | Edge case: empty queue                        |
| T4  | `exit_loop()`                | Set `ToolContext.actions.escalate=True`                               | -                                             |
| T5  | `load_artifact(filename)`    | Return binary image                                                     | Size limit & existence check                    |
| T6  | `save_test_set(test_set)`    | Supabase `upsert` (`onConflict=["part_id","number"]`)                  | pgBouncer limit, assert `rows_upserted`       |

> **Generated file placement** … `src/tools/**.py`

## 4. Agent Implementation

### 4.1 Workflow Agents

1.  **`question_extractor_agent` (Sequential)** ― Root orchestrator
2.  **`pipeline_loop_agent` (Loop)** ― Execute the lower sequence for each unprocessed file
3.  **`pipeline_sequential_agent` (Sequential)** ― Process one file in 1→5 steps

### 4.2 LlmAgents (Step Implementation)

| Seq | Agent                 | Model                | Input/Output           | Dependent Tools             |
| :-- | :-------------------- | :------------------- | :--------------------- | :-------------------------- |
| 1   | `file_selector_agent` | None                 | state.files → artifact | select\_file / exit\_loop   |
| 2   | `extractor_agent`     | Gemini 2.5 **Flash** | Image → raw text       | load\_artifact              |
| 3   | `structure_agent`     | Gemini 2.5 **Pro** | raw text → JSON (schema) | -                           |
| 4   | `tagging_agent`       | Gemini 2.5 **Pro** | JSON → tagged JSON     | -                           |
| 5   | `save_agent`          | None                 | tagged JSON → Supabase | save\_test\_set             |

### 4.3 Agent Config

* `task_timeout`: 60 s (Flash) / 120 s (Pro)
* `max_retries`: 3 (common backoff)
* `temperature`: ≈ 0
* 1000 RPM throttling (Runner)

> **Generated file placement** … agent YAML + python wrapper under `src/agents/**/`

## 5. Pipeline Execution CLI

* [ ] `main.py` ― `python -m app.run --input ./input_dir`
* [ ] Progress bar (`rich.progress`) & summary of successful/failed items

## 6. Testing

* [ ] **Unit Tests** ― Each tool + schema validity of each LlmAgent
* [ ] **Integration Test** ― e2e test of `pipeline_sequential_agent` with Mock images
* [ ] **Performance Benchmark** ― 200 question samples: average ≤3 s / question, error ≤10 %

## 7. Documentation

* [ ] `README.md` ― Usage / KPI / Dependent environment
* [ ] `docs/architecture.md` ― ER diagram, agent architecture diagram (Mermaid)
* [ ] `CHANGELOG.md` ― semantic‑versioning

---

### ✅ Completion Criteria

1.  Successful execution of saving **JPEG/PNG/PDF** input to Supabase with a single CLI command.
2.  `pytest` green, CI pass.
3.  Benchmark results: *error ≤10 % / avg ≤3 sec*.