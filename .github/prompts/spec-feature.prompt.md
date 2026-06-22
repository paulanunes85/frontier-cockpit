---
description: "Specify a feature with the spec-driven flow: validated requirements (EARS), a design with a diagram, and a sequenced task plan with a quality gate."
agent: agent
argument-hint: "the feature to specify, for example the agent cost calculator page"
---

# Spec Feature

Produce a full specification for `${input:feature:the feature or change to specify}` before any code is written.

## First step, always

Use the `Spec Engineer` agent persona where helpful. Load `requirements-engineer` before capturing requirements, then load `sdd-spec-engineer` before generating the design and task plan. Follow the repository conventions in [../copilot-instructions.md](../copilot-instructions.md).

## Steps

1. Clarify scope, users, and constraints. Ask only for what is missing.
2. Write `REQUIREMENTS.md` with acceptance criteria in EARS notation (one requirement per sentence), plus non-functional requirements.
3. Write `DESIGN.md` with an architecture overview and a Mermaid diagram, tracing each component to requirements.
4. Write `TASKS.md` as a sequenced plan with `[P]` parallel markers and a pre-implementation gate; every task traces to a requirement.
5. Write `ANALYSIS.md` as a quality gate with a traceability matrix (requirement to design to task to test). Confirm no orphan tasks and no untraced requirements.
6. Place all four artifacts under a numbered feature folder (`001-<slug>/`, `002-<slug>/`).

## Rules

- Reuse the validated BTG building blocks rather than rewriting; for UBB math, pull formulas and canonical numbers from the `ubb-engine` skill, never invent values.
- Documentation in English; app UI copy is trilingual EN, PT-BR, ES. Write "GitHub Copilot", never "Copilot" alone. No em dashes.

## Done when

- The four artifacts exist, every acceptance criterion is in EARS notation, and the traceability matrix is complete.
- The task plan is ready to hand to the `UBB Engineer` agent for implementation.

## Output

Output concisely: return only the artifact path(s), validation status, and any critical findings or blockers. Do not narrate the process steps.
