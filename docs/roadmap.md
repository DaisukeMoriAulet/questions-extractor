## 🗺️ Roadmap Overview

| Week (Estimate) | Phase                   | Main Output                                                                 | Key Risks & Mitigation                                                                 |
| :-------------: | :---------------------- | :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
|      1-2      | **Environment Setup & Design** | Repo Initialization / CI (`act` for YAML lint) / Data Model SQL              | GitHub Actions configuration errors → Local validation with `act` ([Reddit][11])        |
|      3-4      | **File Preparation Tools** | Implement `list_files`, `split_pdf_pages` & Unit Tests                      | Large PDF splitting failure → PyPDF2 exception handling & split limit ([Stack Overflow][7], [Medium][8]) |
|      5-6      | **OCR Pipeline** | Flash OCR Tool & `extractor_agent` Prototype                                | QPS Exceeded → Runner-side 1k RPM rate limiting ([Google Developers Blog][4])          |
|      7-8      | **Structuring & Tagging** | Pro + `pydantic` output\_schema, `structure_agent` / `tagging_agent`        | JSON breakdown due to model updates → ADK regression test suite ([Google AI for Developers][3]) |
|     9-10      | **Supabase Integration** | `save_test_set` tool, 7 tables schema & upsert                               | Composite onConflict collision → Postgres constraint design ([Supabase][5], [Stack Overflow][6]) |
|     11-12     | **Reliability Enhancement** | Logger / Exponential Backoff + Jitter / Completion of `pipeline_loop_agent` | Backoff contention → Implement random Jitter ([PullRequest][12])                       |
|      13       | **Performance & QA** | 200 Questions Benchmark (≤ 3 s / question) & Error Rate Measurement          | Flash/Pro parallel optimization                                                        |
|      14       | **Documentation & Next Plan** | README / Operation Manual / Future Expansion Tickets                         | Consider sharing method (Internal Dev UI or Cloud Run)                                 |

---

## Phase Details

### Phase 0: Environment Setup & Design (Week 1-2)

1.  **ADK & Poetry Setup**

    ```bash
    pip install "google-adk[^0.4]" pydantic supabase
    ```

    Verify operation with ADK Quickstart ([Google GitHub][10])
2.  **Supabase Schema Creation** – Define 7 tables in `init.sql`.
3.  **CI / CD** – Only YAML lint with `act` and `pytest -m unit` execution ([Reddit][11]).
4.  **Data Model Diagram** – Generate ER diagram using dbdiagram.io, etc.

### Phase 1: File Preparation Tools (Week 3-4)

* Implement `list_files` and `split_pdf_pages` in Python.
* Save each page using `PdfReader` → `PdfWriter` from PyPDF2 ([Stack Overflow][7], [Medium][8]).
* Unit tests using `adk.testing.MockArtifactService` ([Google GitHub][9]).

### Phase 2: OCR Pipeline (Week 5-6)

* OCR with **Flash 05-20**. `extractor_agent` has no Structured Output.
* Rate limiting to **1000 RPM** on the Runner side ([Google Developers Blog][4]).
* 60 s timeout → `task_timeout=60` in agent config.

### Phase 3: Structuring & Tagging (Week 7-8)

* Pass **`pydantic` schema** to `structure_agent` and specify `output_schema` ([Google AI for Developers][3]).
* Normalize variable tags into a dedicated table using JSONB.

### Phase 4: Supabase I/O (Week 9-10)

* Use the `save_test_set` tool with `supabase.table("questions").upsert(..., onConflict=["part_id","number"])` ([Supabase][5], [Stack Overflow][6]).
* Bulk upsert per `passage_set` within a transaction.

### Phase 5: Reliability & Logging (Week 11-12)

* Implement **Exponential Backoff + Jitter** in the common library ([PullRequest][12]).
* Aggregate `gemini_request_id` / filenames in `context.state` for logging.
* Loop through unprocessed files with `pipeline_loop_agent`. Follow the SequentialAgent/LoopAgent pattern ([Google GitHub][2]).

### Phase 6: Performance & QA (Week 13)

* 200-question benchmark: **Average processing time ≤ 3 s**, error rate measurement.
* Adjust parallelism if the Flash call is the bottleneck.

### Phase 7: Documentation & Future Plans (Week 14)

* Organize operation manuals, CLI samples, and Cloud Run migration steps.
* Create PoC tickets for voice OCR (Whisper / Gemini Audio).

---

## Milestones & KPI Checkpoints

| Milestone (Week) | Verification Item    | Acceptance Criteria                           |
| :--------------- | :------------------- | :-------------------------------------------- |
| Week 4           | PDF → Image Splitting | Any 100-page PDF completed within 60 s        |
| Week 6           | Flash OCR Success Rate | ≥ 90% successful JSON extraction from 50 sample pages |
| Week 10          | Supabase Upsert      | 1k dummy questions stored without duplicates   |
| Week 13          | MVP KPI              | Error rate ≤ 10%, Average processing ≤ 3 s   |

---

## Quick Reference for Risk Mitigation

| Risk                | Impact              | Preemptive Measures                                       |
| :------------------ | :------------------ | :-------------------------------------------------------- |
| Gemini Output Issues | JSON parsing failure | Pydantic + ADK regression tests ([Google GitHub][9])      |
| API Rate Limit      | Processing Stalls   | Runner queue & Backoff                                  |
| Schema Expansion    | Data Loss           | JSONB column + Migration procedures                       |

---

### Reference Links

* ADK Docs (Agent Types, Runner, Testing) ([Google GitHub][1], [Google GitHub][2], [Google GitHub][9])
* Gemini Structured Output Guide ([Google AI for Developers][3])
* Supabase Upsert Patterns ([Supabase][5], [Stack Overflow][6])
* PyPDF2 Split Tips ([Stack Overflow][7], [Medium][8])

Updating actual values during weekly reviews based on this roadmap and further breaking down tasks will facilitate progress management towards achieving KPIs.

[1]: https://google.github.io/adk-docs/?utm_source=chatgpt.com "Agent Development Kit - Google"
[2]: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/?utm_source=chatgpt.com "Sequential agents - Agent Development Kit - Google"
[3]: https://ai.google.dev/gemini-api/docs/structured-output?utm_source=chatgpt.com "Structured output | Gemini API | Google AI for Developers"
[4]: https://developers.googleblog.com/en/gemini-15-pro-and-15-flash-now-available/?utm_source=chatgpt.com "Gemini 1.5 Pro and 1.5 Flash GA, 1.5 Flash tuning support, higher ..."
[5]: https://supabase.com/docs/reference/javascript/upsert?utm_source=chatgpt.com "JavaScript: Upsert data | Supabase Docs"
[6]: https://stackoverflow.com/questions/75247517/supabase-upsert-multiple-onconflict-constraints?utm_source=chatgpt.com "Supabase - Upsert & multiple onConflict constraints - Stack Overflow"
[7]: https://stackoverflow.com/questions/45144206/pypdf2-split-pdf-by-pages?utm_source=chatgpt.com "PyPDF2 split pdf by pages - python - Stack Overflow"
[8]: https://medium.com/%40mgkyawzayya/splitting-and-merging-pdf-files-with-python-using-pypdf2-cfce5c948c36?utm_source=chatgpt.com "Splitting and Merging PDF Files with Python using PyPDF2 - Medium"
[9]: https://google.github.io/adk-docs/get-started/testing/?utm_source=chatgpt.com "Testing - Agent Development Kit - Google"
[10]: https://google.github.io/adk-docs/get-started/quickstart/?utm_source=chatgpt.com "Quickstart - Agent Development Kit - Google"
[11]: https://www.reddit.com/r/github/comments/14x7p93/is_there_a_way_to_test_github_actions_yaml_code/?utm_source=chatgpt.com "Is there a way to test GitHub actions YAML code locally? - Reddit"
[12]: https://www.pullrequest.com/blog/retrying-and-exponential-backoff-smart-strategies-for-robust-software/?utm_source=chatgpt.com "Retrying and Exponential Backoff: Smart Strategies for Robust ..."