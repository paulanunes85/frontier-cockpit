---
title: "Lab 00, Facilitator Setup"
description: "Preparation checklist for running the Frontier Developer Cockpit hands-on workshop."
author: "Frontier Cockpit Team"
date: "2026-06-18"
version: "1.0.0"
status: "approved"
tags: ["github-copilot", "workshop", "setup", "facilitator"]
---

<!-- markdownlint-disable MD025 -->

# Lab 00, Facilitator Setup

This lab prepares the facilitator environment and defines safety boundaries for the hands-on workshop.

## Goals

- Confirm local tools are installed.
- Confirm GitHub and Azure authentication.
- Confirm the local observability stack is available.
- Confirm whether Azure enterprise synchronization is in scope.
- Explain privacy boundaries before content capture is used.

## Prerequisites

| Requirement | Validation Command |
| --- | --- |
| VS Code Insiders | Open VS Code Insiders |
| GitHub Copilot access | Run a simple GitHub Copilot Chat prompt |
| Docker Desktop | `docker info` |
| Azure CLI | `az account show` |
| GitHub CLI | `gh auth status -h github.com` |
| Node.js and npm | `node --version && npm --version` |
| Python 3 | `python3 --version` |
| Prometheus and Grafana | Required for complete local dashboard experience |
| DuckDB or SQLite | Optional for Python-first local insight storage |
| Draw.io CLI, optional | `drawio --version` |

## Setup Validation

Run:

```bash
~/.copilot-otel/check-otel-local.sh
```

Expected result:

```text
Local OTel setup is ready.
```

If not ready, start the local stack:

```bash
~/.copilot-otel/start-full-stack.sh
```

For Azure demos, start hybrid mode:

```bash
~/.copilot-otel/start-full-stack.sh --hybrid
```

## Accounts

### GitHub

Check authentication:

```bash
gh auth status -h github.com
```

Recommended scopes for enterprise demos:

```text
admin:enterprise
admin:org
manage_billing:copilot
repo
workflow
```

### Azure

Set the expected subscription:

```bash
az account set --subscription "your-subscription-name"
```

Validate resources:

```bash
az resource list -g rg-agentobs-dev-eus-001 -o table
```

## Safety Briefing

Before a workshop, state these rules:

- Local content capture can include prompts, source code, tool arguments, and tool results.
- Raw content should stay local unless the customer explicitly approves sharing.
- Azure receives sanitized telemetry and rollups.
- Local AIU is an operational signal, not official billing.
- GitHub Copilot usage metrics and billing exports are separate official sources.
- Do not run the workshop on highly sensitive customer repositories without explicit approval.

## Instructor Checklist

- [ ] Local stack starts.
- [ ] Aspire opens at `http://localhost:18888`.
- [ ] Local Grafana opens at `http://localhost:3000`.
- [ ] Azure Managed Grafana opens if hybrid demo is planned.
- [ ] `~/.copilot-otel/audit-coverage.sh` runs.
- [ ] GitHub CLI is authenticated.
- [ ] Azure CLI is on the expected subscription.
- [ ] Firecrawl MCP uses a secure API-key input, not a hardcoded secret.

## References

- [Developer Local Guide](../docs/FrontierCockpit_DeveloperLocalGuide_v1_0_0_2026-06-17_en.md)
- [Operations Runbook](../docs/FrontierCockpit_OperationsRunbook_v1_0_0_2026-06-17_en.md)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [Aspire Dashboard standalone](https://aspire.dev/dashboard/standalone/)
