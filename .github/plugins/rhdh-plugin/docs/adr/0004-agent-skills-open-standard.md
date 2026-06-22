# Agent Skills open standard

All skills in this project follow the [Agent Skills specification](https://agentskills.io/specification), an open format for giving AI agents new capabilities. Skills use `SKILL.md` files with frontmatter metadata, progressive disclosure (description to instructions to references), and bundled `scripts/` and `references/` directories per the spec. This makes the skills portable across compatible agent clients. Source package manifests are an optional distribution layer and do not change the skills themselves, which remain agent-agnostic.

## Consequences

- Skill structure is constrained by the spec (frontmatter format, directory conventions, description length limits).
- New skills should be validated against the [best practices](https://agentskills.io/skill-creation/best-practices) and [description optimization](https://agentskills.io/skill-creation/optimizing-descriptions) guidance.
- The project works with compatible agents without modifying the skill content. Client-specific distribution is layered on top, not baked in.
