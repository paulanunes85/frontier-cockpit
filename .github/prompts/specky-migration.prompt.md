---
description: Plan a system migration with SDD pipeline
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Plan a system migration using the Specky SDD pipeline.

**Source system:** [Current system description]
**Target system:** [Target architecture / platform]
**Data constraints:** [e.g., zero downtime, data volume, schema changes]
**Timeline:** [Migration deadline or phases]

Please:
1. Call @requirements-engineer to capture migration requirements as FRD + NFRD
2. Call @sdd-init with project_type=migration
3. Call @research-analyst to scan both source and target

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
