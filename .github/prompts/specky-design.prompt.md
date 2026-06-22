---
description: Run SDD design phase
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Run the SDD design phase for feature [FEATURE NUMBER].

@design-architect , produce DESIGN.md with component architecture (Mermaid C4 diagrams), API interface definitions, data models, and integration points. Call sdd_write_design then sdd_generate_all_diagrams.

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
