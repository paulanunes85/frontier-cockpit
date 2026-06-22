---
title: "Frontier Cockpit Firecrawl MCP Guide"
description: "Guide for using Firecrawl MCP to collect official documentation and validate observability references for Frontier Cockpit."
author: "Frontier Cockpit Team"
date: "2026-06-18"
version: "1.0.0"
status: "approved"
tags: ["github-copilot", "firecrawl", "mcp", "documentation", "opentelemetry"]
---

<!-- markdownlint-disable MD025 -->

# Frontier Cockpit Firecrawl MCP Guide

This guide documents how Firecrawl MCP is configured and used to support the Frontier Developer Cockpit documentation workflow.

## Change Log

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 1.0.0 | 2026-06-18 | Frontier Cockpit Team | Initial Firecrawl MCP guide. |

## Table of Contents

- [1. Purpose](#1-purpose)
- [2. Configuration](#2-configuration)
- [3. Security Model](#3-security-model)
- [4. Usage Patterns](#4-usage-patterns)
- [5. Documentation Workflow](#5-documentation-workflow)
- [6. Validation](#6-validation)
- [7. Troubleshooting](#7-troubleshooting)
- [References](#references)

## 1. Purpose

Firecrawl MCP helps collect authoritative web documentation as clean Markdown or structured data. In this implementation, it supports research and validation for:

- Aspire Dashboard documentation.
- OpenTelemetry GenAI references.
- VS Code GitHub Copilot agent documentation.
- GitHub Copilot API documentation.
- Azure Monitor and Azure Managed Grafana documentation.

Firecrawl MCP is not part of the telemetry pipeline. It is a documentation and research aid.

## 2. Configuration

The global VS Code Insiders MCP file is:

```text
~/Library/Application Support/Code - Insiders/User/mcp.json
```

The Firecrawl server is configured as a single server named:

```text
firecrawl-mcp
```

Expected configuration pattern:

```json
{
  "firecrawl-mcp": {
    "type": "stdio",
    "command": "npx",
    "args": [
      "-y",
      "firecrawl-mcp@latest"
    ],
    "env": {
      "FIRECRAWL_API_KEY": "${input:api_key}"
    },
    "gallery": "https://api.mcp.github.com",
    "version": "1.0.0"
  }
}
```

## 3. Security Model

The Firecrawl API key must not be hardcoded in `mcp.json`. It should be supplied through a secure VS Code MCP input, such as:

```json
{
  "id": "api_key",
  "type": "promptString",
  "description": "Firecrawl API key",
  "password": true
}
```

The previous hardcoded Firecrawl API key was removed from `mcp.json`. If that key was exposed in local logs or history, rotate it in the Firecrawl console.

## 4. Usage Patterns

Use Firecrawl MCP from GitHub Copilot Chat with `@firecrawl-mcp`.

### 4.1 Scrape A Documentation Page

```text
@firecrawl-mcp scrape https://aspire.dev/dashboard/explore/#genai-telemetry-visualization
```

### 4.2 Search For Official Guidance

```text
@firecrawl-mcp search "GitHub Copilot OpenTelemetry GenAI observability Aspire Dashboard"
```

### 4.3 Map Documentation Site Structure

```text
@firecrawl-mcp map https://aspire.dev/dashboard/
```

## 5. Documentation Workflow

Recommended workflow:

1. Use Firecrawl MCP to scrape or search official documentation.
2. Save or summarize the retrieved content.
3. Compare the source claims with local implementation.
4. Update Markdown documents under `frontier-cockpit/`.
5. Add references to official sources.
6. Re-run validation checks.

Firecrawl MCP should not be used to bypass source validation. Retrieved content should still be checked against official GitHub, Microsoft, Azure, Aspire, or OpenTelemetry sources.

## 6. Validation

Validate `mcp.json`:

```bash
python3 -m json.tool "$HOME/Library/Application Support/Code - Insiders/User/mcp.json" >/dev/null
```

Check Firecrawl entries:

```bash
grep -n 'firecrawl\|FIRECRAWL' "$HOME/Library/Application Support/Code - Insiders/User/mcp.json"
```

Verify the package resolves:

```bash
npm view firecrawl-mcp version
```

## 7. Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `@firecrawl-mcp` does not appear | MCP registry not reloaded | Run `Developer: Reload Window` |
| Firecrawl asks for API key | Secure input is working as designed | Paste the rotated Firecrawl API key |
| Firecrawl request fails | Invalid key, quota, or network issue | Check Firecrawl account and API usage |
| Duplicate Firecrawl servers | Old config entries remain | Keep only `firecrawl-mcp` |
| API key appears in JSON | Hardcoded secret | Replace with `${input:api_key}` and rotate the key |

## References

- [Firecrawl documentation](https://docs.firecrawl.dev/)
- [Firecrawl MCP package](https://www.npmjs.com/package/firecrawl-mcp)
- [VS Code MCP servers documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [Model Context Protocol](https://modelcontextprotocol.io/)
