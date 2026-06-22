---
description: Check SDD pipeline status
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Check the SDD pipeline status for feature [FEATURE NUMBER or "all"].

Call sdd_get_status and show: current phase, artifacts generated, hooks active, next recommended action, and which @agent to use next.

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
