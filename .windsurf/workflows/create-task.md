---
description: This document describes the workflow to create GitHub Issues from the MVP breakdown.
---

# GitHub Issues Task Workflow – Questions Extractor

This document describes the workflow to create GitHub Issues from the MVP breakdown.

You will be provided with the following info:

- The target mvp_breakdown task with the task id.

---

## Workflow

### 1. Generate Issue file

Generate an issue file based on the documents below.

- [`docs/prd.md`](../docs/prd.md)
- [`docs/roadmap.md`](../docs/roadmap.md)
- [`docs/mvp_breakdown.md`](../docs/mvp_breakdown.md)
- Task template

---

### 2. Save Issue file

Save the issue file to `docs/issues/` directory.

File naming convention:

- `docs/issues/task-<id>.md`

### 3. GitHub CLI Command

Generate gh issue create command.

```bash
gh issue create \
--title "[TASK-<id>] <Task Title>" \
--body-file "docs/issues/task-<id>.md" \
--label "phase/<phase>" \
```
