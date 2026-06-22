# stdlib-only Python CLIs

Both CLIs (`rhdh` and `rhdh-local`) use only Python 3.9+ standard library — zero external dependencies. This means no `click`, `rich`, `typer`, or any other package. The trade-off is rougher developer ergonomics in exchange for zero-install portability. The CLIs run wherever Python exists — no `pip install`, no virtualenv, no version conflicts. For agent tooling that needs to "just work" in any environment an agent might run in, that constraint is worth the cost.

## Implementation patterns

- **`argparse`** for argument parsing (stdlib, not click/typer)
- **`OutputFormatter`** for auto-detecting TTY vs piped output (human-readable vs JSON)
- **`uv`** as the dev tool runner (`uv run pytest`) — not shipped with the CLIs, but used for development and testing

New scripts and CLI commands in this project should follow these same patterns.
