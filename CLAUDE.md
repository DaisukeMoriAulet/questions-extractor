# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Questions Extractor** project that uses Google's Agent Development Kit (ADK) to build a multi-agent system. The system processes image files and PDFs containing English proficiency test questions (like TOEIC), extracts and structures the information, and stores it in Supabase.

## Common Development Commands

### Running Tests
```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/tools/test_list_files.py

# Run with verbose output
pytest -v
```

### Code Formatting
```bash
# Format code with Black (required before committing)
black .
```

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

## High-Level Architecture

### Multi-Agent System Design
The system uses a hierarchical agent structure as defined in `docs/agents_arch.yaml`:

1. **Root Agent** (`question_extractor_agent`): Sequential agent that orchestrates the entire process
2. **File Preparation Agent** (`file_preparator_agent`): Lists files and splits PDFs into page images
3. **Pipeline Loop Agent** (`pipeline_loop_agent`): Processes each file through a sequential pipeline
   - File Selection Agent: Identifies next file to process
   - Extractor Agent: OCR using Gemini 2.5 Flash
   - Structure Agent: Structures text to JSON using Gemini 2.5 Pro
   - Tagging Agent: Adds tags using Gemini 2.5 Pro  
   - Save Agent: Bulk upserts to Supabase

### Database Schema (Supabase)
The system uses a normalized 7-table structure:
- `test_forms` → `sections` → `parts` → `passage_sets` → `passages` → `questions` → `choices`
- Auxiliary tables: `tags`, `question_tags`

Key constraints:
- Questions are unique by `(part_id, number)`
- Choices are unique by `(question_id, label)`
- Uses `upsert` operations with conflict resolution

### Important Technical Details

1. **ADK Context Management**:
   - Use `artifacts` for binary data (images, audio) to avoid size limitations
   - Use `context.state` for smaller JSON data
   - Tools interact with context through `ToolContext` parameter

2. **Error Handling**:
   - Exponential backoff with 3 retries for API calls
   - 60-second timeout for Gemini API calls
   - Rate limiting controlled at Runner level

3. **Testing Convention**:
   - Tests use `MockToolContext` to simulate ADK context
   - Test files follow `test_*.py` naming convention
   - Tests focus on tool functionality with realistic scenarios

## Important Notes

- **Always refer to MCP Context7** for the latest ADK documentation when in doubt
- Use **Structured Output** with Gemini models by setting `output_schema` with Pydantic models
- Environment variables are managed through GitHub Environment Variables
- The project processes JPEG/PNG images (not HEIC) with max 10MB/100 pages