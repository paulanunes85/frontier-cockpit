---
name: overlay
description: "Manage the rhdh-plugin-export-overlays repository. Use for onboarding plugins to the Extensions Catalog, updating plugin versions, fixing overlay build failures, triaging or analyzing PRs, triggering publish, testing PR artifacts with rhdh-local, and managing plugin workspaces."
---

# Overlay

Use this skill for work in `redhat-developer/rhdh-plugin-export-overlays`: onboarding, updates, CI failures, PR triage, publish triggers, and local verification of PR artifacts.

## First Step

1. Resolve the RHDH orchestrator CLI. Prefer the `rhdh` skill's `$RHDH` setup. If already configured, reuse it.
2. Run `$RHDH` or `$RHDH doctor` when the task depends on local repo paths or tools.
3. Identify whether this is a plugin-owner task or a core-team task. If intent is clear, proceed; otherwise ask a concise question.

## Operating Principles

- All plugin exports go through `rhdh-plugin-export-overlays`.
- Each plugin workspace uses `source.json` plus `plugins-list.yaml`; CI performs the export from this configuration.
- `source.json` `repo-backstage-version` is upstream's actual Backstage version.
- `backstage.json` `version` is the RHDH compatibility override.
- Test PR artifacts before merge using `rhdh-local` when possible.
- OCI PR artifact format is `oci://<registry>/<image>:pr_<number>__<version>!<package-name>`.
- If blocked, compare against a similar workspace before inventing a new pattern.

## Routing

| User intent | Action |
| --- | --- |
| Onboard, add, import, new plugin | Read [workflows/onboard-plugin.md](workflows/onboard-plugin.md). |
| Update, bump, upgrade, version | Read [workflows/update-plugin.md](workflows/update-plugin.md). |
| Status, check, health | Run the inline status checks below. |
| Fix, debug, failure, CI error | Read [workflows/fix-build.md](workflows/fix-build.md). |
| Triage, prioritize, backlog | Read [workflows/triage-prs.md](workflows/triage-prs.md). |
| Analyze PR, check PR, PR number | Read [workflows/analyze-pr.md](workflows/analyze-pr.md). |
| Publish, trigger publish | Use the publish trigger guardrails below. |

## Inline Status Checks

```bash
$RHDH workspace list
$RHDH workspace status <name>
gh run list --repo redhat-developer/rhdh-plugin-export-overlays --limit 5
gh pr list --repo redhat-developer/rhdh-plugin-export-overlays --search "<name>"
```

## Publish Trigger Guardrails

Before adding `/publish` to a PR, verify:

1. The PR is open.
2. The PR has no `do-not-merge` label.
3. A publish check has not already succeeded.

Then run:

```bash
REPO="redhat-developer/rhdh-plugin-export-overlays"
gh pr comment <number> --repo "$REPO" --body "/publish"
gh pr view <number> --repo "$REPO" --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.name | contains("publish"))'
```

Read [../rhdh/references/github-reference.md](../rhdh/references/github-reference.md) before using GitHub CLI patterns that are not familiar.

## References

| File | Use when |
| --- | --- |
| [references/overlay-repo.md](references/overlay-repo.md) | Understanding workspace and overlay repository patterns. |
| [references/ci-feedback.md](references/ci-feedback.md) | Interpreting CI and publish failures. |
| [references/metadata-format.md](references/metadata-format.md) | Editing `source.json`, `plugins-list.yaml`, and metadata. |
| [references/label-priority.md](references/label-priority.md) | Prioritizing PR labels. |
| [references/rhdh-local.md](references/rhdh-local.md) | Testing PR artifacts locally. |
| [templates/workspace-files.md](templates/workspace-files.md) | Creating workspace files. |

## Success Criteria

For plugin-owner work:

- Workspace configuration is present and follows the expected structure.
- CODEOWNERS is updated when required.
- CI and publish checks pass.
- The plugin is tested locally when feasible.
- The PR is ready to merge or has clear next actions.

For core-team work:

- PRs are prioritized with actionable next steps.
- Stale or blocked PRs have owners or recommendations.
- Publish is triggered only after guardrails pass.
- Compatibility issues are flagged before merge.