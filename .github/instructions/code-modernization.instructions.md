---
description: "Rules for GitHub Copilot modernization work: legacy source is evidence, modernization analysis belongs under analysis/, and transformed code belongs under modernized/."
applyTo: "legacy/**,analysis/**,modernized/**"
source: "code-modernization-plugin, adapted for GitHub Copilot"
source_url: "local:.github/plugins/code-modernization-plugin"
license: "Apache-2.0"
imported_date: "2026-06-18"
last_sync: "2026-06-18"
---

# Code Modernization Rules

These rules apply when GitHub Copilot works on legacy modernization projects that use `legacy/`, `analysis/`, and `modernized/` folders.

## Boundaries

- Treat `legacy/**` as read-only evidence unless the user explicitly asks to modify it.
- Write discovery, assessment, maps, rules, and design artifacts under `analysis/**`.
- Write transformed or replacement implementation under `modernized/**`.
- Preserve behavioral evidence with file references before changing target code.
- Do not use modernization as a reason to rewrite unrelated modules.

## Evidence

- Cite source paths for technical findings.
- Mark inferred behavior as inferred.
- Separate business behavior from implementation detail.
- Capture unresolved questions for subject matter experts instead of guessing.

## Validation

- Prefer characterization tests before transformation.
- Compare legacy behavior against modernized behavior where feasible.
- Run available build, test, and static analysis commands before calling work complete.
- Report any test or runtime gap that remains.