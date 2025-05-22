---
description: This document describes the workflow to create GitHub Issues Epic from the MVP breakdown.
---

# GitHub Issue Epic Workflow – Questions Extractor

This document describes the workflow to create GitHub Issues Epic from the MVP breakdown.

You will be provided with the following info:

- The target mvp_breakdown epic with the epic id.

---

## Workflow

### 1. Generate Epic file

Generate an epic file based on the documents below.

- [`docs/prd.md`](../docs/prd.md)
- [`docs/roadmap.md`](../docs/roadmap.md)
- [`docs/mvp_breakdown.md`](../docs/mvp_breakdown.md)
- Epic template

---

### 2. Save Epic file

Save the epic file to `docs/issues/` directory.

File naming convention:

- `docs/issues/epic-<phase>.md`

### 3. GitHub CLI Command

Generate gh issue create command.

```bash
gh issue create \
--title "[EPIC-<phase>] <Phase Title>" \
--body-file "docs/issues/epic-<phase>.md" \
--label "phase/<phase>" \
```
