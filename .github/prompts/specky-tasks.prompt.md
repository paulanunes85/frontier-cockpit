---
description: Run SDD task breakdown phase
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Run the SDD task breakdown phase for feature [FEATURE NUMBER].

@task-planner , produce TASKS.md with dependency-resolved task sequence, [P] parallel markers, REQ-* traceability on every task, and complexity estimates (S/M/L/XL). Call sdd_write_tasks then sdd_checklist.

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
