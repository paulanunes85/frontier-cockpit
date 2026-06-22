---
description: Run the full SDD pipeline end-to-end
agent: agent
argument-hint: "feature number, task details, or source artifact"
---
Run the full SDD pipeline for feature [FEATURE NUMBER or NAME].

@specky-orchestrator , coordinate all 10 phases (Init → Discover → Specify → Clarify → Design → Tasks → Analyze → Implement → Verify → Release), validate artifacts between phases, enforce LGTM gates at Phases 2/4/5, and route to the correct agent per phase.

## Output

Output concisely: return only the artifact path(s), validation status, next required action, and any critical findings or blockers. Do not narrate the process steps.
