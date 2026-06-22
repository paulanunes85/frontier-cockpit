# Code Modernization Plugin

A structured workflow and set of specialist agents for modernizing legacy codebases — COBOL, legacy Java/C++, monolith web apps — into current stacks while preserving behavior.

## Overview

Legacy modernization fails most often not because the target technology is wrong, but because teams skip steps: they transform code before understanding it, reimagine architecture before extracting business rules, or ship without a harness that would catch behavior drift. This plugin enforces a sequence:

```
assess → map → extract-rules → reimagine → transform → harden
```

Each step has a dedicated slash command. Specialist agents (legacy analyst, business rules extractor, architecture critic, security auditor, test engineer) are invoked from within those commands — or directly — to keep the work honest.

## Commands

The commands are designed to be run in order, but each produces a standalone artifact so you can stop, review, and resume.

### `/modernize-brief`
Capture the modernization brief: what's being modernized, why now, constraints (regulatory, data, runtime), non-goals, and success criteria. Produces `analysis/brief.md`. Run this first.

### `/modernize-assess`
Inventory the legacy codebase: languages, line counts, module boundaries, external integrations, build system, test coverage, known pain points. Produces `analysis/assessment.md`. Uses the `legacy-analyst` agent for deep reads on unfamiliar dialects.

### `/modernize-map`
Map the legacy structure onto a target architecture: which legacy modules become which target services/packages, data-flow diagrams, migration sequencing. Produces `analysis/map.md`. Uses the `architecture-critic` agent to pressure-test the design.

### `/modernize-extract-rules`
Extract business rules from the legacy code — the rules that are encoded in procedural logic, COBOL copybooks, stored procedures, or config files — into human-readable form with citations back to source. Produces `analysis/rules.md`. Uses the `business-rules-extractor` agent.

### `/modernize-reimagine`
Propose the target design: APIs, data model, runtime. Explicitly list what changes from legacy and what stays identical. Produces `analysis/design.md`. Uses the `architecture-critic` agent to challenge over-engineering.

### `/modernize-transform`
Do the actual code transformation — module by module. Writes to `modernized/`. Pairs each transformed module with a test suite that pins the pre-transform behavior.

### `/modernize-harden`
Post-transform review pass: security audit, test coverage, error handling, observability. Uses `security-auditor` and `test-engineer` agents. Produces a findings report ranked Blocker / High / Medium / Nit.

## Agents

- **`legacy-analyst`** — Reads legacy code (COBOL, legacy Java/C++, procedural PHP, classic ASP) and produces structured summaries. Good at spotting implicit dependencies, copybook inheritance, and "JOBOL" patterns (procedural code wearing a modern syntax).
- **`business-rules-extractor`** — Extracts business rules from procedural code with source citations. Each rule includes: what, where it's implemented, which conditions fire it, and any corner cases hidden in data.
- **`architecture-critic`** — Adversarial reviewer for target architectures and transformed code. Default stance is skeptical: asks "do we actually need this?" Flags microservices-for-the-resume, ceremonial error handling, abstractions with one implementation.
- **`security-auditor`** — Reviews transformed code for auth, input validation, secret handling, and dependency CVEs. Tuned for the kinds of issues that appear when translating security primitives across stacks (e.g., session handling from servlet to stateless JWT).
- **`test-engineer`** — Audits test suites for behavior-pinning vs. coverage-theater. Flags tests that exercise code paths without asserting outcomes.

## Installation

```
# For GitHub Copilot, use the converted primitives under .github/agents, .github/prompts, .github/skills, and .github/instructions.
```

## Recommended Workspace Setup

This source package ships command and agent patterns. For GitHub Copilot, enforce the "never touch legacy, freely edit modernized" rule through `.github/instructions/code-modernization.instructions.md`:

```text
legacy/**      read-only evidence unless the user explicitly asks to edit it
analysis/**    modernization assessment, rules, maps, and design artifacts
modernized/**  transformed implementation and behavior-pinning tests
```

Adjust `legacy/` and `modernized/` to match your actual layout. The key invariants: `Edit` under `legacy/` is denied, and writes are scoped to `analysis/` (for documents) and `modernized/` (for the new code).

## Typical Workflow

```bash
# 1. Write the brief — what are we modernizing and why?
/modernize-brief

# 2. Inventory the legacy code
/modernize-assess

# 3. Extract business rules before touching the code
/modernize-extract-rules

# 4. Map legacy structure to target
/modernize-map

# 5. Propose the target design and review it
/modernize-reimagine

# 6. Transform module by module
/modernize-transform

# 7. Harden: security, tests, observability
/modernize-harden
```

## License

Apache 2.0. See `LICENSE`.
