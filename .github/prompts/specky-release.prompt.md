---
description: Run SDD release phase
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Run the SDD release phase for feature [FEATURE NUMBER].

**Branch:** [current spec/NNN-* branch]
**Target:** develop (then stage → main after gates pass)

@release-engineer , verify branch, run blocking gates (security-scan + release-gate), generate documentation, create PR targeting the correct branch.

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
