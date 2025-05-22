## Overview

* **Purpose**
    To **one-click automate** the process of OCR, structuring, tagging, and saving PDF/image-based test question sets used internally to Supabase, thereby reducing manual work and human errors.

* **MVP Success Metrics**
    * **Error rate ≤ 10 %** after processing completion.
    * Average **processing time ≤ 3 seconds** per question (using Flash).

* **Target User**
    Only the developer (considering internal sharing in the future).

* **Prerequisite Technologies**
    * Google **Agent Development Kit (ADK)**
    * **Gemini 2.5 Flash / Pro** (Structured Output enabled)
    * **Supabase Postgres** (`upsert` + `onConflict` control)

## 1. Business Objectives and KPIs

| Item         | Content                                                 |
| :----------- | :------------------------------------------------------ |
| Success Criteria | Error rate ≤ 10% / Emphasis on reproducibility (temperature ≈ 0) |
| Scalability    | Small increase in records but flexible for **column additions** |
| Maintenance    | **Overwrite save** (history backed up separately)         |
| Future Vision  | Potential for Listening audio (MP3) OCR / Speech recognition |

## 2. Input Specifications

| Parameter     | Requirement                                   |
| :------------ | :-------------------------------------------- |
| Supported Formats | JPEG / PNG (HEIC not required)              |
| Max Size      | 10 MB / 100 pages                             |
| Processing Trigger | **Manual execution** (MVP)                    |
| PDF Splitting | Split into single pages using **PyPDF2** |

## 3. Processing Pipeline

### 3.1 OCR

| Item                | Policy                                                                                                |
| :------------------ | :---------------------------------------------------------------------------------------------------- |
| Model               | High-speed OCR with **Gemini 2.5 Flash 05-20** |
| Structured Output | Use by setting the `pydantic` model to `output_schema`                                                  |
| Timeout             | Disconnect after 60 s of call (configurable in ADK runtime)                                           |
| Retry               | **Exponential backoff 3 times** (2^n coefficient + Jitter recommended)                               |
| Rate-Limit          | Control the **API QPS** of Flash/Pro on the Runner side (different limits for each model) |

### 3.2 Text Structuring & Tagging

* Normalize extracted text to JSON using Gemini 2.5 Pro 05-06.
* Allow **variable-length** hierarchical tags (Skill → Category → Sub-category).
* Plan to add `difficulty`, `topic` → Adopt a **normalized table** in preparation for field expansion.

### 3.3 Bulk Save (Supabase)

* Third normal form with a 7-table structure:
    * tests → sections → parts → passage\_sets → passages → questions → choices
    * Auxiliary tables: tags, question\_tags
* Example of `upsert(values, onConflict= ... )`:
    * questions : `onConflict=["part_id","number"]`
    * choices : `onConflict=["question_id","label"]`
* Group by Passage-set and control JSONB metadata to be less than 8 MB row size.

## 4. ADK Agent Architecture

### 4.1 Agents

| Layer (Hierarchy) | Agent / Tool                                                                 | **Category** | Role / Reason                                      |
| :-------------- | :--------------------------------------------------------------------------- | :------------------- | :------------------------------------------------- |
| **Root** | **`question_extractor_agent`** | **Sequential Agent** | Overall orchestrator                               |
| └─Prep          | **`file_preparator_agent`**<br> `list_files`, `split_pdf_pages`              | **LlmAgent**<br>Tool | Enumerate input files / Split PDF pages               |
| └─Pipeline      | **`pipeline_loop_agent`** | **Loop Agent** | Execute the lower sequence **for each unprocessed file** |
|   └─Seq         | **`pipeline_sequential_agent`** | **Sequential Agent** | Process one file (page) in the order of **1 to 5** |
|     └─1         | `file_selector_agent` → `select_file`／`exit_loop`                           | **LlmAgent**<br>Tool | Identify the next file to process and save to artifacts. Exit loop if none. |
|     └─2         | `extractor_agent` → `load_artifact`                                        | **LlmAgent**<br>Tool | OCR with Flash                                     |
|     └─3         | `structure_agent`                                                            | **LlmAgent** | Structure to JSON with Pro                           |
|     └─4         | `tagging_agent`                                                              | **LlmAgent** | Tagging with Pro                                     |
|     └─5         | `save_agent` → `save_test_set`                                               | **LlmAgent**<br>Tool | Supabase upsert                                    |

### 4.2 Tools

| Tool                    | Function                                  | Args                                              | Interaction with Context                                                                                                   | Returns                                                          |
| :---------------------- | :---------------------------------------- | :------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| **`list_files`** | List file paths directly under the specified folder | `dir_path: str`<br>`tool_context: ToolContext`    | **write →**<br>`ToolContext.state["files"][{filename}] = ""`                                                             | `status: success｜error`<br>`message: str`<br>`files: dict`       |
| **`split_pdf_pages`** | Split PDF into images, one page per image    | `file_path: str`<br>`tool_context`                | **append →**<br>`ToolContext.state["files"][{filename}-{index}] = ""`                                                    | `status` / `message` / `files`                                   |
| **`select_file`** | Save unprocessed file to artifacts, set next target | `file_path: str`<br>`tool_context: ToolContext`    | **write →**<br>`ToolContext.save_artifact(filename, types.Part)`<br>`ToolContext.state["file_to_process"] = filename` | `status` / `message`<br>`file_metadata: {filename, page_count}` |
| **`exit_loop`** | Exit the loop if there are no unprocessed files | `tool_context`                                    | **write →**<br>`ToolContext.actions.escalate = True`                                                                      | `status` / `message`                                             |
| **`load_artifact`** | Load image file from artifacts              | `filename: str`<br>`tool_context: ToolContext`     | **read ←** `ToolContext.load_artifact(filename)`                                                                           | `status` / `message`<br>`artifact_version: str`                  |
| **`save_test_set`** | Upsert the structured test set to Supabase   | `test_set: dict`<br>`tool_context`                | ― (Direct write to DB)                                                                                                   | `status` / `message`<br>`rows_upserted: int`                     |

**Artifacts vs. context.state**

* Use `artifacts` for binary data like **images** and **audio** (to avoid size limitations).
* Prefer `context.state` for smaller intermediate JSON, use artifacts only if the threshold is exceeded.

## 5. Data Model

| Table             | Main Columns                                                                                                                                         | Notes / Constraints               |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| **test\_forms** | `id` PK, `name`                                                                                                                                      | Test type e.g., TOEIC, IELTS    |
| **sections** | `id` PK, `test_id` FK, `label`, `order_no`                                                                                                            | Reading / Listening …           |
| **parts** | `id` PK, `section_id` FK, `label`, `question_format`, `order_no`                                                                                       | Part 5 (short\_blank) etc.      |
| **passage\_sets** | `id` PK, `part_id` FK, `order_no`, `question_range` *int4range*, `title`, `metadata` *jsonb* | Question block (for double/triple passages) |
| **passages** | `id` PK, `passage_set_id` FK, `order_no`, `body`, `metadata` *jsonb* | Text, figures, audio scripts, etc. |
| **questions** | `id` PK, `passage_set_id` FK, `part_id` FK, `number`, `blank_index`, `stem`, `answer_explanation`, `difficulty`, `attributes` *jsonb* | Unique `(part_id, number)`      |
| **choices** | `id` PK, `question_id` FK, `label`, `content`, `is_correct`                                                                                            | Unique `(question_id, label)`   |
| **tags** | `id` PK, `level1`, `level2`, `level3`                                                                                                                  | Hierarchical tags               |
| **question\_tags**| `question_id` FK, `tag_id` FK                                                                                                                        | PK = (question\_id, tag\_id)    |

## 6. Reliability & Testing

* **Logging**: Save `filename`, `page`, `gemini_request_id` to session state.
* **Unit Testing**: Use in-memory Session & ArtifactService, mock PDF / images for **individual agent testing** (using `adk.testing` module).
* **CI**: Only YAML syntax check with GitHub Actions.

## 7. Non-Functional Requirements

| Item        | Content                                                    |
| :---------- | :--------------------------------------------------------- |
| Execution Environment | Local machine (Python 3.12 + ADK)                    |
| Security    | **No additional ACL required** due to local use           |
| Deployment  | Cloud Run also selectable in the future (ADK Engine compatible) |

## 8. Dependent Libraries & Versions

| Library       | Version | Purpose                       |
| :------------ | :------ | :---------------------------- |
| `google-adk`  | ^0.4.x  | Agent framework               |
| `PyPDF2`      | >=3.0   | PDF splitting                 |
| `supabase`    | >=2.0   | Postgres upsert               |

## 9. Risks & Future Challenges

1.  **Output degradation due to LLM model updates**
    * Continue using Structured Output with schema and detect with regression tests.
2.  **Gemini API Rate-Limit**
    * Control queue on the Runner side and use exponential backoff when exceeded.
3.  **Schema Expansion**
    * Consider a fallback strategy to add JSONB columns (leveraging Postgres flexibility).
4.  **Addition of Audio OCR**
    * Verification and Tool creation for Whisper / Gemini Audio OCR.

## 10. Reference Documents

* ADK ([ADK Documentation][1])

---

[1]: https://google.github.io/adk-docs/ "ADK Documentation"