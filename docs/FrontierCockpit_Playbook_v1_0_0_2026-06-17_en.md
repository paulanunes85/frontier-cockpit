---
title: "Frontier Cockpit Playbook"
description: "Implementation playbook for Frontier Cockpit, including Frontier Developer Cockpit, Frontier FinOps Cockpit, GitHub API ingestion, governance, and workshop rollout."
author: "Frontier Cockpit Team"
date: "2026-06-17"
version: "1.0.0"
status: "approved"
tags: ["github-copilot", "opentelemetry", "aspire", "grafana", "azure", "playbook"]
---

<!-- markdownlint-disable MD025 -->

# Frontier Cockpit Playbook

This playbook explains how to implement and operate **Frontier Cockpit**, the umbrella platform for GitHub Copilot and agentic development observability. It covers **Frontier Developer Cockpit** for the local developer experience, **Frontier FinOps Cockpit** for centralized Azure leadership and cost views, daily synchronization, GitHub API enrichment, governance, dashboards, operations, and workshop delivery.

## Change Log

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0.0 | 2026-06-17 | Frontier Cockpit Team | Initial implementation playbook for local and Azure observability. |

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Playbook Map](#2-playbook-map)
- [3. Platform Layers And Fleet Overview](#3-platform-layers-and-fleet-overview)
- [4. Reference Architecture](#4-reference-architecture)
- [5. Implementation Phases](#5-implementation-phases)
- [6. Roles And Responsibilities](#6-roles-and-responsibilities)
- [7. Success Criteria](#7-success-criteria)
- [8. Data Boundaries](#8-data-boundaries)
- [9. Daily Operating Rhythm](#9-daily-operating-rhythm)
- [10. Decision Log](#10-decision-log)
- [11. Validation Gates](#11-validation-gates)
- [References](#references)

## 1. Purpose

The purpose of this playbook is to help teams deploy **Frontier Cockpit**, a complete observability model for GitHub Copilot Chat and agent work. The model gives developers a private Frontier Developer Cockpit for learning and optimization, while Azure receives sanitized and aggregated telemetry for enterprise history, FinOps, governance, and leadership insights.

The product architecture is intentionally split into two cockpit experiences on top of one platform:

| Cockpit | Purpose | Data Detail |
| --- | --- | --- |
| **Frontier Developer Cockpit** | Help developers understand and improve their own GitHub Copilot usage | Full fidelity, including content capture in trusted local environments |
| **Frontier FinOps Cockpit** | Provide central cost, ROI, governance, executive rollups, cost-center allocation, and adoption analytics | Sanitized traces, metrics, rollups, and GitHub API data |

The shared platform layers are L1 to L6, and **Fleet Overview** is the aggregate operating view that feeds leadership, FinOps, and governance workflows.

## 2. Playbook Map

| Document | Purpose |
| --- | --- |
| [Taxonomy And Platform Layers](FrontierCockpit_TaxonomyAndPlatformLayers_v1_0_0_2026-06-18_en.md) | Final naming, L1-L6 platform layers, and Fleet Overview model. |
| [Architecture Diagrams](FrontierCockpit_ArchitectureDiagrams_v1_0_0_2026-06-18_en.md) | C4, deployment, telemetry flow, and GitHub Enterprise flow diagrams. |
| [End-to-End Implementation Manual](FrontierCockpit_EndToEndImplementationManual_v1_0_0_2026-06-18_en.md) | Step-by-step implementation record for everything built so far. |
| [Python And Aspire Local Architecture](FrontierCockpit_PythonAspireLocalArchitecture_v1_0_0_2026-06-18_en.md) | Python-first local runtime guidance with Aspire, DuckDB or SQLite, Prometheus, and Grafana. |
| [Local Links Guide](FrontierCockpit_LocalLinksGuide_v1_0_0_2026-06-19_en.md) | Localhost links and explanations for Aspire, Grafana dashboards, Prometheus, Tempo, and Loki. |
| [Developer Local Guide](FrontierCockpit_DeveloperLocalGuide_v1_0_0_2026-06-17_en.md) | Install, run, and use the Frontier Developer Cockpit. |
| [Azure Enterprise Guide](FrontierCockpit_AzureEnterpriseGuide_v1_0_0_2026-06-17_en.md) | Deploy and validate Frontier FinOps Cockpit in Azure. |
| [Data Consolidation Guide](FrontierCockpit_DataConsolidationGuide_v1_0_0_2026-06-17_en.md) | Combine OTel data with GitHub APIs, usage metrics, and billing exports. |
| [Firecrawl MCP Guide](FrontierCockpit_FirecrawlMCPGuide_v1_0_0_2026-06-18_en.md) | Use Firecrawl MCP for official documentation research and validation. |
| [Operations Runbook](FrontierCockpit_OperationsRunbook_v1_0_0_2026-06-17_en.md) | Operate, validate, troubleshoot, and tear down the stack. |
| [Workshop Guide](FrontierCockpit_WorkshopGuide_v1_0_0_2026-06-17_en.md) | Run a customer or internal developer workshop. |
| [Strategy](FrontierCockpit_Strategy_v1_0_0_2026-06-17_en.md) | Explain offer, architecture, value proposition, and roadmap. |

## 3. Platform Layers And Fleet Overview

Frontier Cockpit uses six platform layers that feed both cockpit experiences.

| Layer | Name | Feeds |
| --- | --- | --- |
| L1 | Developer Signal Capture | Frontier Developer Cockpit |
| L2 | Local Observability Runtime | Frontier Developer Cockpit |
| L3 | Session Intelligence | Both cockpits |
| L4 | Secure Forwarding And Redaction | Frontier FinOps Cockpit |
| L5 | Azure Consolidation | Frontier FinOps Cockpit |
| L6 | GitHub Intelligence Layer | Frontier FinOps Cockpit |

**Fleet Overview** is the aggregate operating view across developers, repositories, organizations, cost centers, and enterprise scopes. It is part of Frontier FinOps Cockpit and is fed by all six platform layers.

For the locked taxonomy, see [FrontierCockpit_TaxonomyAndPlatformLayers_v1_0_0_2026-06-18_en.md](FrontierCockpit_TaxonomyAndPlatformLayers_v1_0_0_2026-06-18_en.md).

## 4. Reference Architecture

```text
Developer workstation
  VS Code Insiders, GitHub Copilot Chat, Agent Host, GitHub Copilot CLI
        |
        v
  Local OpenTelemetry Collector
        |
        +--> Aspire Dashboard, live trace and GenAI visualizer
        +--> Tempo, local traces
        +--> Prometheus, local metrics
        +--> Loki, local logs and content-capture records
        +--> Grafana OSS, developer dashboards
        +--> Azure Container Apps Collector, sanitized forwarding
                 |
                 +--> Application Insights
                 +--> Log Analytics
                 +--> Azure Managed Grafana
                 +--> Future GitHub API enrichment
```

The local Collector is the stable local contract. Development tools send OTLP to `localhost:4318` for HTTP and `localhost:4317` for gRPC. The Collector decides which data stays local and which data is sanitized before Azure forwarding.

## 5. Implementation Phases

### 5.1 Phase 1, Frontier Developer Cockpit

1. Configure user-level VS Code Insiders OTel settings.
2. Configure user-level shell and macOS LaunchAgents.
3. Run the full local stack in Docker Desktop.
4. Validate Aspire live GenAI traces.
5. Validate Prometheus and local Grafana dashboards.
6. Validate workspace attribution and data quality.
7. Enable daily local materialization and rollups.

### 5.2 Phase 2, Frontier FinOps Cockpit

1. Deploy Azure resources with Bicep.
2. Configure local hybrid forwarding with bearer token authentication.
3. Sanitize large or sensitive content before Azure forwarding.
4. Validate Application Insights and Log Analytics ingestion.
5. Import Azure Managed Grafana dashboards.
6. Confirm daily rollups arrive in Azure.

### 5.3 Phase 3, GitHub API Enrichment

1. Ingest GitHub Copilot usage metrics API data.
2. Ingest GitHub billing or AI Credits exports.
3. Ingest repository, organization, team, branch, and pull request metadata.
4. Add Log Analytics reference tables.
5. Join OTel rollups to GitHub adoption and billing views.

### 5.4 Phase 4, Governance And Scale

1. Define retention, redaction, and access policies.
2. Create role-based Azure dashboards.
3. Add alert rules for usage, cost, error, and context risks.
4. Package the implementation as a repeatable workshop and customer deployment kit.

## 6. Roles And Responsibilities

| Role | Responsibilities |
| --- | --- |
| Developer | Use Frontier Developer Cockpit, improve prompts, inspect sessions, validate changes. |
| Team lead | Coach developers, review usage patterns, identify enablement opportunities. |
| Platform engineer | Maintain local kit, Collector config, Azure deployment, dashboards, and automation. |
| Security or compliance | Review content capture, redaction, retention, and access policies. |
| FinOps | Reconcile AIU and official GitHub billing exports. |
| Workshop facilitator | Run guided labs and explain local vs enterprise views. |

## 7. Success Criteria

| Area | Success Criteria |
| --- | --- |
| Local setup | `~/.copilot-otel/check-otel-local.sh` reports ready. |
| Aspire | `copilot-chat` traces appear and GenAI visualizer can inspect content capture. |
| Prometheus and Grafana local | Required local metrics and dashboard layer showing real workspace usage, context, AIU, and data quality. |
| Daily rollup | `copilot_daily_workspace_*` metrics exist in Prometheus and arrive in Azure. |
| Azure | `rg-agentobs-dev-eus-001` resources are healthy and Azure Managed Grafana loads dashboards. |
| Data quality | Synthetic validation spans are separated from real usage. |
| Privacy | Raw content stays local by default, Azure receives sanitized telemetry. |

## 8. Data Boundaries

| Data | Local | Azure |
| --- | --- | --- |
| Raw prompts and responses | Allowed in trusted local environments | Redacted before forwarding |
| Tool schemas and tool results | Allowed locally | Redacted before forwarding |
| Tokens and AIU | Stored locally | Forwarded and rolled up |
| Repository and branch | Stored locally | Forwarded when emitted by GitHub Copilot |
| VS Code OS memory | Stored locally | Optional rollup only |
| GitHub usage metrics API | Planned | Enterprise source of truth for adoption |
| GitHub billing exports | Planned | Enterprise source of truth for billing reconciliation |

## 9. Daily Operating Rhythm

1. Developer works normally in VS Code Insiders.
2. Local OTel stack starts automatically through user LaunchAgents.
3. Real GitHub Copilot sessions are materialized every five minutes.
4. VS Code process memory is sampled every minute.
5. Daily rollup runs at 18:00 local time.
6. When hybrid mode is enabled, daily rollups and sanitized telemetry are forwarded to Azure.
7. Platform team reviews Azure dashboards for trends and anomalies.

## 10. Decision Log

| Decision | Rationale |
| --- | --- |
| Keep raw content local | Protect sensitive prompts, code, and tool results. |
| Send sanitized telemetry to Azure | Avoid oversized attributes and reduce data risk. |
| Use Aspire for live debugging | Aspire provides the GenAI trace visualizer and live span inspection. |
| Use Prometheus and Grafana for the local cockpit | Prometheus stores local metrics and Grafana provides the required card-based developer UX. |
| Use Tempo and Loki locally | Purpose-built stores for traces and logs. |
| Use Log Analytics and Application Insights in Azure | Enterprise query, retention, and integration surface. |
| Treat model names as telemetry labels | Emitted labels can be routed, internal, or preview labels, not always billing names. |
| Keep official billing separate | AI Credits and official spend require GitHub billing or usage exports. |

## 11. Validation Gates

### 11.1 Local Validation

```bash
~/.copilot-otel/check-otel-local.sh
~/.copilot-otel/audit-coverage.sh
~/.copilot-otel/materialize-copilot-sessions.sh
~/.copilot-otel/daily-rollup.sh
```

### 11.2 Azure Validation

```bash
az resource list -g rg-agentobs-dev-eus-001 -o table
az monitor log-analytics query \
  -w $(az monitor log-analytics workspace show -g rg-agentobs-dev-eus-001 -n log-agentobs-dev-eus-001 --query customerId -o tsv) \
  --analytics-query 'AppTraces | summarize Count=count() by AppRoleName'
```

### 11.3 Dashboard Validation

- Aspire opens at `http://localhost:18888`.
- Local Grafana opens at `http://localhost:3000`.
- Azure Managed Grafana opens at the managed endpoint.
- Coverage dashboard reports observed and not-yet-observed signals.
- Context and cost dashboard shows AIU and context-window utilization from real workspace sessions.

## References

- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/tree/main/docs/gen-ai/)
- [Inside the LLM Call: GenAI Observability with OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/)
- [Aspire Dashboard GenAI telemetry visualization](https://aspire.dev/dashboard/explore/#genai-telemetry-visualization)
- [Aspire Dashboard standalone](https://aspire.dev/dashboard/standalone/)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [GitHub REST API documentation](https://docs.github.com/en/rest)
- [Azure Monitor documentation](https://learn.microsoft.com/azure/azure-monitor/)
- [Azure Managed Grafana documentation](https://learn.microsoft.com/azure/managed-grafana/)
