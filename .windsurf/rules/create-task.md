---
trigger: manual
---

# GitHub Issues Task Workflow – Questions Extractor

This document describes the workflow to create GitHub Issues from the MVP breakdown.

You will be provided with the following info:

- The target mvp_breakdown task with the task id.

---

## Goals

1. **Single Source of Truth** – Every task in the MVP breakdown becomes exactly one GitHub Issue.
2. **Traceability** – Each Issue references the relevant PRD requirement _and_ Roadmap milestone so that business intent ⇆ timeline ⇆ implementation stay in sync.

---

## Source Documents

| Doc                                                 | Purpose                                         |
| --------------------------------------------------- | ----------------------------------------------- |
| [`docs/prd.md`](../docs/prd.md)                     | Functional & non-functional requirements.       |
| [`docs/roadmap.md`](../docs/roadmap.md)             | Timeline, milestones & exit criteria.           |
| [`docs/mvp_breakdown.md`](../docs/mvp_breakdown.md) | Atomised task list (ID, phase, estimate, deps). |

---

## Naming & Labelling Convention

| Element         | Rule                       | Example                 |
| --------------- | -------------------------- | ----------------------- |
| **Issue Title** | `[TASK-<ID>] <Task Title>` | `[TASK-9] <Task Title>` |
| **Labels**      | `phase/<phase>`            | `phase/0`               |

| Phase | Label     |
| ----- | --------- |
| 0     | `phase/0` |
| 1     | `phase/1` |
| 2     | `phase/2` |
| 3     | `phase/3` |
| 4     | `phase/4` |
| 5     | `phase/5` |
| 6     | `phase/6` |
| 7     | `phase/7` |

---

## Template

Get the template from the following file.

- [docs/templates/task.md](../docs/templates/task.md)
