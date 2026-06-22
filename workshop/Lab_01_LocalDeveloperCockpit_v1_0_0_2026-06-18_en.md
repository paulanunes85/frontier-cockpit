---
title: "Lab 01, Local Developer Cockpit"
description: "Hands-on lab for starting and validating the local Frontier Developer Cockpit observability cockpit."
author: "Frontier Cockpit Team"
date: "2026-06-18"
version: "1.0.0"
status: "approved"
tags: ["github-copilot", "workshop", "local", "grafana", "aspire"]
---

<!-- markdownlint-disable MD025 -->

# Lab 01, Local Developer Cockpit

This lab helps participants start the Frontier Developer Cockpit and understand each local component.

## Goals

- Start the full local stack.
- Validate OpenTelemetry endpoints.
- Open Aspire, Grafana, Prometheus, Tempo, and Loki.
- Understand the difference between live debugging and historical dashboards.

## Step 1, Start The Local Stack

Run:

```bash
~/.copilot-otel/start-full-stack.sh
```

Expected local endpoints:

| Component | Endpoint |
| --- | --- |
| OpenTelemetry HTTP | `http://localhost:4318` |
| OpenTelemetry gRPC | `http://localhost:4317` |
| Aspire Dashboard | `http://localhost:18888` |
| Grafana local | `http://localhost:3000` |
| Prometheus | `http://localhost:9090` |
| Tempo | `http://localhost:3200` |
| Loki | `http://localhost:3100` |

## Step 2, Validate The Stack

Run:

```bash
~/.copilot-otel/check-otel-local.sh
```

The output should show Docker, Collector, Aspire, Grafana, Prometheus, Tempo, Loki, PostgreSQL, VS Code settings, and launchd variables as ready.

## Step 3, Open The Interfaces

```bash
open http://localhost:18888
open http://localhost:3000
open http://localhost:9090
```

Explain:

| Interface | Best For |
| --- | --- |
| Aspire | Live trace debugging and GenAI visualizer |
| Grafana | Historical and educational dashboards |
| Prometheus | Raw metric exploration |
| Tempo | Trace search and trace detail |
| Loki | Logs and content-capture metadata |

## Step 4, Register The Workspace

From the target repository folder:

```bash
~/.copilot-otel/register-workspace.sh
```

This creates a local mapping from `workspace_path_hash` to a friendly workspace, repository, and branch. It does not fabricate usage.

## Step 5, Explain Local Privacy

Local telemetry can include raw content. The local stack is intended for trusted developer machines and workshops where content capture is explicitly approved.

Azure forwarding redacts raw content before enterprise ingestion.

## Validation

Run:

```bash
curl -fsS http://localhost:9090/api/v1/label/__name__/values | python3 -m json.tool | head
```

You should see Prometheus metadata. Real GitHub Copilot metrics appear after a GitHub Copilot session runs.

## Completion Criteria

- [ ] Local stack is running.
- [ ] Aspire opens.
- [ ] Grafana opens.
- [ ] Workspace registry has a friendly entry.
- [ ] Participant can explain which tool is used for live traces vs historical dashboards.

## References

- [Developer Local Guide](../docs/FrontierCockpit_DeveloperLocalGuide_v1_0_0_2026-06-17_en.md)
- [Aspire Dashboard GenAI telemetry visualization](https://aspire.dev/dashboard/explore/#genai-telemetry-visualization)
- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/tree/main/docs/gen-ai/)
