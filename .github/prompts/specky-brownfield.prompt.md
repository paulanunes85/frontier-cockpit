---
description: Add SDD pipeline to an existing codebase
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Add the Specky SDD pipeline to this existing codebase.

**Feature:** [FEATURE NAME]
**What to modernize:** [Component, module, or area to target]
**Tech stack:** [detected or stated]

Please:
1. Call @sdd-init with project_type=brownfield
2. Run @research-analyst to scan the codebase and detect the tech stack
3. Show me what was detected and suggest next steps
4. Create branch `spec/NNN-[feature]` from `develop` for all pipeline work

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
