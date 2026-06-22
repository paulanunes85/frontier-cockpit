# Contributing to RHDH Skill

Contributions are welcome, and they are greatly appreciated! Every little bit helps. ❤️

This project is released under the Apache 2.0 License.

## Get Started

```bash
git clone https://github.com/redhat-developer/rhdh-skill.git
cd rhdh-skill
uv sync --extra dev
git config core.hooksPath .githooks
```

That last command enables pre-commit hooks (linting, formatting, tests) automatically — no `pre-commit install` needed.

### Running Tests

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check .
uv run ruff format --check .
```

Both run automatically via the pre-commit hook.

## Adding a Skill

Use the `/skill-maker` skill — it interviews you about scope, edge cases, and architecture before drafting anything.

Before creating a new skill, check whether it belongs as a **sub-command** of an existing skill. If the new work shares prerequisites, scripts, or cross-references with an existing skill, add a sub-command and reference file instead. See `skills/create-plugin/` for an example of a sub-command router with `backend`, `frontend`, `export`, and `wiring` commands.

## Submitting a Pull Request

1. Fork the repo and create a branch from `main`.
2. Make your changes. Keep commits focused — one concern per commit.
3. Make sure `uv run pytest` and `uv run ruff check .` pass.
4. Open a pull request.

## Agent Bootstrap

`AGENTS.md` is the canonical contributor and agent guidance file. Keep platform-specific bootstrap files as thin pointers to `AGENTS.md` when a distribution requires them.
