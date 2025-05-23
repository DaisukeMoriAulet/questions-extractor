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

* [x] **init.sql** ― Create third normal form 7+2 tables (test_forms→…→choices / tags, question\_tags)
* ~~[ ] **Typed ER Diagram** ― Auto‑generate with dbdiagram.io → `docs/er.png`~~
* ~~[ ] **Supabase Type Definitions** ― Generate `postgrest-js` script or `supabase gen types typescript`~~
* [x] **Local `.env`** ― `SUPABASE_URL`, `SUPABASE_API_KEY`

## 2. Common Utilities

* [x] **logging.py** ― structured log (`filename`, `page`, `gemini_request_id`)
* [x] **backoff.py** ― `exponential_backoff(jitter=True, retries=3)`
* [x] **paths.py** ― Input/output directory constants `INPUT_DIR`

## 3. Tool Implementation (ADK Tool Functions)

| ID  | Tool                          | Key Points                                                              | Test                                          |
| :-- | :---------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------- |
| [x] T1  | `list_files(dir_path)`       | Write file paths directly under the specified directory to `context.state["files"]` | `pytest tests/tools/test_list_files.py`     |
| [x] T2  | `split_pdf_pages(file_path)` | Save each page as JPEG using PyPDF2. Append output to `state["files"]`   | Verify the number of generated files with `MockArtifactService` |
| [x] T3  | `select_file()`              | Select an unprocessed file and `save_artifact`; `exit_loop` if none     | Edge case: empty queue                        |
| [x] T4  | `exit_loop()`                | Set `ToolContext.actions.escalate=True`                               | -                                             |
| [x] T5  | `load_artifact(filename)`    | Return binary image                                                     | Size limit & existence check                    |
| [x] T6  | `save_test_set(test_set)`    | Supabase `upsert` (`onConflict=["part_id","number"]`)                  | pgBouncer limit, assert `rows_upserted`       |

> **Generated file placement** … `questions_extractor_agent/tools/**.py`

## 4. Agent Implementation

### 4.0 Phase Goals at a Glance
| Phase | Planned Weeks | Completion Criteria                                            |
| :---: | :------------: | :------------------------------------------------------------- |
| 2     | 5-6            | **5 LlmAgents** pass all unit tests                          |
| 3     | 7-8            | **pipeline_sequential_agent** successful on 1-page e2e       |
| 4     | 9-10           | **question_extractor_agent** → multi-page e2e success        |

---

### 4.1 Phase 2 – LlmAgent Individual Implementation & Testing
The checklist is **each Agent + dependent tools + unit tests** as one set.

| ✅ | Agent / Tool                     | Key Implementation Points         | Example Test File              |
| :- | -------------------------------- | ------------------------------- | ------------------------------ |
| [ ] | **file_selector_agent** <br>└─ `select_file` / `exit_loop` | Select unprocessed file / Exit loop judgment | `tests/agents/test_file_selector.py` |
| [ ] | **extractor_agent** <br>└─ `load_artifact` | Flash 05-20 OCR (unstructured)  | `tests/agents/test_extractor.py` |
| [ ] | **structure_agent** | Pro 05-06 + JSON schema with `pydantic` | `tests/agents/test_structure.py` |
| [ ] | **tagging_agent** | Tagging with Pro 05-06          | `tests/agents/test_tagging.py` |
| [ ] | **save_agent** <br>└─ `save_test_set` | Supabase upsert logic only      | `tests/agents/test_save.py`    |

> **Development UI** – Check individual operation with `adk web agents/<agent_name>`. :contentReference[oaicite:1]{index=1}

---

### 4.2 Phase 3 – Building pipeline_sequential_agent
1.  **Generate SequentialAgent**
    Connect the 5 stages: `file_selector` → `extractor` → `structure` → `tagging` → `save`.
2.  **Integration Test**
    - e2e with 1 mock image.
    - Verify data flow / error propagation.
3.  **Supabase Stub**
    Replace `save_test_set` with a dummy implementation targeting local sqlite to enable testing in CI. :contentReference[oaicite:2]{index=2}

---

### 4.3 Phase 4 – Loop & Orchestration
| ✅ | Workflow Agent             | Role                                          | Completion Criteria                |
| :- | -------------------------- | --------------------------------------------- | ---------------------------------- |
| [ ] | **pipeline_loop_agent** (Loop) | Sequentially input unprocessed files to `pipeline_sequential_agent` | Process all pages in a 10-page PDF |
| [ ] | **question_extractor_agent** (Sequential) | Manage `file_preparator_agent` → `pipeline_loop_agent` | Upsert 1k rows to Supabase end-to-end |

> **End-to-end Integration Test** – `tests/e2e/test_full_pipeline.py`. Matches the achievement criteria of Roadmap Phase 4. :contentReference[oaicite:3]{index=3}

---

### 4.4 Common Agent Settings
* `task_timeout`: Flash 60 s / Pro 120 s
* `max_retries`: 3 (exponential backoff + jitter)
* Runner-side **1000 RPM** throttling
* Generated file placement: `questions_extractor_agent/agents/**/`

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