---
title: "Frontier FinOps Cockpit Azure Enterprise Guide"
description: "Implementation guide for Frontier FinOps Cockpit, the Azure enterprise experience for sanitized GitHub Copilot telemetry, daily workspace rollups, GitHub Enterprise signals, cost, governance, and leadership dashboards."
author: "Frontier Cockpit Team"
date: "2026-06-17"
version: "1.0.0"
status: "approved"
tags: ["github-copilot", "azure", "application-insights", "log-analytics", "managed-grafana", "opentelemetry"]
---

<!-- markdownlint-disable MD025 -->

# Frontier FinOps Cockpit Azure Enterprise Guide

This guide explains how **Frontier FinOps Cockpit** is implemented, validated, and operated as the centralized Azure side of Frontier Cockpit.

## Change Log

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0.0 | 2026-06-17 | Frontier Cockpit Team | Initial Azure enterprise implementation guide. |

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Deployed Resources](#2-deployed-resources)
- [3. Data Flow](#3-data-flow)
- [4. Deployment Commands](#4-deployment-commands)
- [5. Hybrid Forwarding](#5-hybrid-forwarding)
- [6. Azure Data Model](#6-azure-data-model)
- [7. Dashboard Import](#7-dashboard-import)
- [8. Validation](#8-validation)
- [9. Redaction Strategy](#9-redaction-strategy)
- [10. Cost And Teardown](#10-cost-and-teardown)
- [References](#references)

## 1. Purpose

Frontier FinOps Cockpit receives sanitized GitHub Copilot telemetry and daily rollups from developer machines. It provides central history, team and platform dashboards, cost and ROI views, governance views, Fleet Overview, and GitHub API enrichment.

## 2. Deployed Resources

| Resource | Name | Purpose |
| --- | --- | --- |
| Resource group | `rg-agentobs-dev-eus-001` | Enterprise observability boundary |
| Container App | `ca-otelcol-dev-eus-001` | Cloud OpenTelemetry Collector |
| Container Apps environment | `cae-agentobs-dev-eus-001` | Runtime environment |
| Application Insights | `appi-agentobs-dev-eus-001` | Application telemetry resource |
| Log Analytics | `log-agentobs-dev-eus-001` | Workspace-backed telemetry storage |
| Azure Monitor workspace | `amw-agentobs-dev-eus-001` | Managed Prometheus integration |
| Azure Managed Grafana | `amg-agentobs-dev-eus01` | Enterprise dashboards |
| Managed identity | `id-agentobs-dev-eus-001` | Azure resource identity |

Subscription:

```text
your-subscription-name
00000000-0000-0000-0000-000000000000
```

Region:

```text
eastus
```

## 3. Data Flow

```text
Local Collector
  full local pipelines remain local
  sanitized Azure pipelines forward to cloud Collector
        |
        v
Azure Container Apps Collector
        |
        v
Application Insights and Log Analytics
        |
        v
Azure Managed Grafana
```

The Azure Collector receives OTLP/HTTP over HTTPS with bearer token authentication. It exports to Azure Monitor through the `azuremonitor` exporter.

## 4. Deployment Commands

### 4.1 Validate

```bash
~/.copilot-otel/azure/validate.sh
```

### 4.2 Deploy

```bash
az account set --subscription "your-subscription-name"
~/.copilot-otel/azure/deploy.sh
```

### 4.3 Destroy

```bash
~/.copilot-otel/azure/destroy.sh
```

The destroy script deletes `rg-agentobs-dev-eus-001` and stops the Azure cost for this environment.

## 5. Hybrid Forwarding

The local hybrid file is:

```text
~/.copilot-otel/azure/.env
```

It contains:

```text
AZURE_OTLP_ENDPOINT=https://ca-otelcol-dev-eus-001.wonderfulpebble-a02374a7.eastus.azurecontainerapps.io
AZURE_OTLP_TOKEN=<redacted>
```

Start hybrid forwarding:

```bash
~/.copilot-otel/start-full-stack.sh --hybrid
```

## 6. Azure Data Model

Workspace-based Application Insights writes to Log Analytics tables.

| Table | Contents |
| --- | --- |
| `AppTraces` | Trace logs, sanitized content-capture records, daily rollups |
| `AppMetrics` | GenAI metrics, tool metrics, token metrics, rollup metrics |
| `AppDependencies` | Dependency-style telemetry |

`AppGenAIContent` was checked and is not available in this environment. The implemented dashboards therefore use `AppTraces` and `AppMetrics`.

## 7. Dashboard Import

Azure Managed Grafana endpoint:

```text
https://your-grafana-workspace.eus.grafana.azure.com
```

Dashboard:

```text
/d/agentobs-azure-copilot-overview/github-copilot-agent-observability-azure
```

Import command:

```bash
az grafana dashboard import \
  -g rg-agentobs-dev-eus-001 \
  -n amg-agentobs-dev-eus01 \
  --folder "GitHub Copilot" \
  --definition ~/.copilot-otel/azure/agentobs-azure-grafana-dashboard.json \
  --overwrite true
```

## 8. Validation

### 8.1 Resource Validation

```bash
az resource list -g rg-agentobs-dev-eus-001 -o table
```

### 8.2 Container App Validation

```bash
az containerapp show \
  -g rg-agentobs-dev-eus-001 \
  -n ca-otelcol-dev-eus-001 \
  --query '{fqdn:properties.configuration.ingress.fqdn,runningStatus:properties.runningStatus,provisioningState:properties.provisioningState}' \
  -o json
```

### 8.3 Log Analytics Validation

```bash
az monitor log-analytics query \
  -w $(az monitor log-analytics workspace show -g rg-agentobs-dev-eus-001 -n log-agentobs-dev-eus-001 --query customerId -o tsv) \
  --analytics-query 'AppTraces | summarize Count=count() by AppRoleName | order by Count desc'
```

### 8.4 Metrics Validation

```bash
az monitor log-analytics query \
  -w $(az monitor log-analytics workspace show -g rg-agentobs-dev-eus-001 -n log-agentobs-dev-eus-001 --query customerId -o tsv) \
  --analytics-query 'AppMetrics | summarize Count=count(), Sum=sum(Sum) by Name | order by Count desc | take 20'
```

## 9. Redaction Strategy

The Azure forwarding pipeline removes large or sensitive content attributes before sending data to Azure.

Redacted attributes include:

- `gen_ai.input.messages`
- `gen_ai.output.messages`
- `gen_ai.system_instructions`
- `gen_ai.tool.definitions`
- `gen_ai.tool.call.arguments`
- `gen_ai.tool.call.result`
- `copilot_chat.user_request`
- `copilot_chat.reasoning_content`
- `github.copilot.tool.parameters.command`

Local Aspire, Tempo, and Loki retain full fidelity for trusted debugging.

## 10. Cost And Teardown

Azure resources incur cost while deployed. Delete the resource group when the environment is not needed:

```bash
~/.copilot-otel/azure/destroy.sh
```

Do not rely on local telemetry for official billing reconciliation. Official cost and AI Credits require GitHub billing or usage exports.

## References

- [Azure Monitor documentation](https://learn.microsoft.com/azure/azure-monitor/)
- [Application Insights documentation](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [Azure Managed Grafana documentation](https://learn.microsoft.com/azure/managed-grafana/)
- [Azure Container Apps documentation](https://learn.microsoft.com/azure/container-apps/)
- [OpenTelemetry Collector Azure Monitor exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/azuremonitorexporter)
