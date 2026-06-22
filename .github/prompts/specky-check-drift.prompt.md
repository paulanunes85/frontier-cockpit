---
description: Check spec-code drift for a feature
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Check spec-code drift for feature [FEATURE NUMBER].

Call sdd_check_sync to compare SPECIFICATION.md requirements against implementation files. Report which requirements are implemented, which are missing, and the drift percentage.

Run sdd_check_sync to compare SPECIFICATION.md requirements against the current codebase. Report any REQ-IDs not found in code or tests.

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
