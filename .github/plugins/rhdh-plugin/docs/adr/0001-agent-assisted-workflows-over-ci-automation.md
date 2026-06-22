# Agent-assisted workflows over CI automation

The overlay repository's plugin lifecycle (triage, onboard, update, fix) is managed through agent skill workflows rather than GitHub Actions or bots. CI automation was the obvious path — the overlay repo already has extensive GitHub Actions infrastructure — but the team chose agent-assisted workflows instead. The key reasons: plugin triage involves ambiguous judgment calls (priority assessment, compatibility evaluation, merge readiness) that don't reduce to simple boolean checks, and the team wanted to validate workflows locally before promoting anything to CI. Agent workflows can adapt through prompt changes without redeploying infrastructure.

## Considered options

- **GitHub Actions / bots**: Lower latency, always-on, but rigid. Every edge case requires code changes, and the PR backlog problem is fundamentally about prioritization and communication, not automation.
- **Agent skill workflows**: Flexible, handles ambiguity, runs locally first. Trades always-on automation for human-in-the-loop judgment with AI assistance.
