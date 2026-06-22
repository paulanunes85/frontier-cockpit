# RHDH Skill

Agent skills for Red Hat Developer Hub (RHDH) plugin development, overlay management, and local testing.

## Language

**Workspace**:
A plugin's directory in the overlay repository containing `source.json` and `plugins-list.yaml`. Defines how an upstream Backstage plugin is exported for RHDH.
_Avoid_: project, package, module

**Overlay**:
The configuration layer that wraps an upstream Backstage plugin for RHDH export. Specifies the source commit, target Backstage version, and build configuration. Not a filesystem or CSS overlay.
_Avoid_: wrapper, shim, adapter

**Publish trigger**:
A `/publish` comment posted on a PR in the overlay repository to kick off the CI build workflow. Required because GitHub Actions cannot auto-trigger on bot-created PRs.

**Plugin Owner**:
An external contributor or team managing their own plugin(s) in the overlay repository. Responsible for updates, compatibility fixes, and CODEOWNERS entries.
_Avoid_: contributor (too generic), maintainer (ambiguous with repo maintainer)

**Core Team**:
The COPE/Plugins team managing overlay repository infrastructure, PR triage, and merge decisions. Distinct from Plugin Owners.
_Avoid_: maintainers, admins

### Support tiers

**Supported**:
A plugin listed in `rhdh-supported-packages.txt`. GA (generally available), fully supported by Red Hat. Workspace PRs are highest triage priority.

**Tech Preview**:
A plugin listed in `rhdh-techpreview-packages.txt`. Available but not yet GA. Workspace PRs are high triage priority.

**Community**:
A plugin listed in `community-packages.txt`. Dev Preview or community-maintained. Workspace PRs are lower triage priority.
_Avoid_: mandatory workspace, non-mandatory workspace (these are derived label concepts, not how the team talks about tiers)

## Relationships

- A **Workspace** produces one **Overlay** for one upstream plugin
- **Support tiers** (Supported, Tech Preview, Community) determine PR triage priority and are driven by productization files in the overlay repo
- **Plugin Owners** manage their own Workspaces; the **Core Team** manages repository-wide concerns (triage, merge gates, infrastructure)
- A **Publish trigger** is required before CI runs on any Workspace PR

## Example dialogue

> **Dev:** "Should I review this workspace PR?"
> **Core Team:** "Check the support tier first — if it's a Supported plugin, it's critical priority. Community plugins can wait unless they're blocking something."

**Plugin Owner:** "My PR has been open for a week."
**Core Team:** "Did you add a publish trigger? CI won't run without `/publish`."

## Flagged ambiguities

- "mandatory workspace" was used in early planning to mean a Workspace for a Supported or Tech Preview plugin — resolved: use the support tier names directly (Supported, Tech Preview, Community).
