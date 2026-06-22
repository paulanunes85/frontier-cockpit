---
name: create-plugin
description: "Create, export, package, and wire Red Hat Developer Hub dynamic plugins. Use for backend plugins, frontend plugins, Backstage plugin scaffolding, scaffolder actions, processors, pages, cards, themes, OCI or tgz packaging, npm package export, dynamic route wiring, mount points, entity tabs, frontend wiring YAML, or publishing plugin container images."
---

# Create Plugin

Use this skill for the full lifecycle of Red Hat Developer Hub dynamic plugins: scaffold, implement, export, package, publish, and configure frontend wiring.

## Prerequisites

- Node.js 22+ and Yarn.
- `podman` or `docker` for OCI packaging.
- Registry access when publishing images, for example `quay.io`.
- Target RHDH version. If not specified, consult [../rhdh/references/versions.md](../rhdh/references/versions.md) and ask for the target version only when needed.

## First Step

Infer the requested command from the user's language. If intent is clear, load the matching reference and proceed. Ask only when the plugin type, plugin ID, target RHDH version, output path, or packaging format is missing.

## Commands

| Command | Use when | Reference |
| --- | --- | --- |
| `backend` | Creating a backend plugin, API, scaffolder action, processor, or backend module. | [references/backend.md](references/backend.md) |
| `frontend` | Creating a frontend plugin, page, card, entity tab, route, or theme. | [references/frontend.md](references/frontend.md) |
| `export` | Exporting, packaging, pushing, or publishing a dynamic plugin. | [references/export.md](references/export.md) |
| `wiring` | Generating frontend wiring for mount points, routes, entity tabs, cards, search, themes, or scaffolder. | [references/wiring.md](references/wiring.md) |

## Routing

| User intent | Action |
| --- | --- |
| Backend plugin, API plugin, scaffolder action, processor | Read [references/backend.md](references/backend.md). |
| Frontend plugin, page, card, theme, entity tab | Read [references/frontend.md](references/frontend.md). |
| Export, package, OCI, tgz, npm, publish, push | Read [references/export.md](references/export.md). |
| Mount point, route, dynamic route, entity page, entity tab, frontend wiring | Read [references/wiring.md](references/wiring.md). |

## Scripts

Scaffold backend or frontend plugins:

```bash
python scripts/scaffold.py \
  --type backend \
  --rhdh-version 1.9 \
  --plugin-id my-plugin
```

Export and package plugins:

```bash
python scripts/export-plugin.py \
  --plugin-dir plugins/my-plugin \
  --tag quay.io/ns/my-plugin:v0.1.0 \
  --push --clean
```

Run `python scripts/scaffold.py --help` and `python scripts/export-plugin.py --help` for all options.

## Lifecycle

1. Scaffold with `backend` or `frontend`.
2. Implement plugin code following the selected reference.
3. Export and package with `export`.
4. Generate `dynamic-plugins.yaml` or frontend wiring with `wiring` when needed.
5. Test locally with `rhdh-local` when possible.

## Deep-Dive References

| File | Use when |
| --- | --- |
| [references/export-options.md](references/export-options.md) | Understanding shared packages, embedded packages, and dependency categories. |
| [references/packaging-formats.md](references/packaging-formats.md) | Comparing OCI, tgz, npm, bundles, and private registries. |
| [references/integrity-hashes.md](references/integrity-hashes.md) | Generating or verifying SHA-512 and SHA-256 integrity hashes. |
| [references/frontend-wiring.md](references/frontend-wiring.md) | Full frontend wiring reference. |
| [references/entity-page.md](references/entity-page.md) | Entity page tabs, cards, conditions, and grid layout. |

## Examples

| File | Contents |
| --- | --- |
| [examples/dynamic-plugins.yaml](examples/dynamic-plugins.yaml) | Backend, frontend, multi-plugin, tgz, npm, and local config patterns. |
| [examples/frontend-wiring.yaml](examples/frontend-wiring.yaml) | Tabs, cards, search, themes, and scaffolder wiring patterns. |

## Common Issues

- Backend plugin not loading: verify `createBackendPlugin` and default export.
- Frontend plugin not loading: verify `scalprum.name` matches `dynamicPlugins.frontend.<key>`.
- Build or export failure: run `yarn tsc`, clear stale `dist` and `dist-dynamic`, then rebuild.
- Missing dependency: add the package with Yarn and rerun TypeScript checks.
- MUI v5 styles missing: configure `unstable_ClassNameGenerator` in `src/index.ts` as shown in [references/frontend.md](references/frontend.md).

## Validation

- Run TypeScript checks before export.
- Run the export script in dry-run or local mode before pushing when possible.
- Verify generated wiring against [examples/frontend-wiring.yaml](examples/frontend-wiring.yaml).
- Test the plugin in local RHDH with the `rhdh-local` skill when feasible.