---
name: foundry-agent-blueprint
description: "Design and provision agents on Azure AI Foundry Agent Service: model catalog and deployments, connections (Azure AI Search, Azure Managed Redis, Bing, storage), threads and runs for short term memory, tools (function, OpenAPI, MCP, code interpreter, file search), evaluation, and tracing. Use when the target runtime is Azure AI Foundry, when choosing models from the Foundry catalog, when wiring agent tools and connections, or when planning Foundry evaluation and observability. Routes to the installed microsoft-foundry, azure-ai, and vscode-microsoft-foundry skills for provisioning detail. Pairs with agentic-architecture-patterns, azure-managed-redis-cache, azure-api-center, and apim-ai-gateway."
argument-hint: "what to build on Foundry, for example a RAG agent with AI Search and a Redis memory connection"
---

# Foundry Agent Blueprint

How to design an agent on **Azure AI Foundry Agent Service** and map the agentic decisions to Foundry primitives. This skill is the design layer; for hands-on provisioning, CLI, and SDK detail, load the installed `microsoft-foundry`, `azure-ai`, and `vscode-microsoft-foundry` skills, and verify against Microsoft Learn.

> Service capabilities and names evolve. Confirm the current Foundry Agent Service features, model catalog entries, and limits on Microsoft Learn before locking a recommendation. Do not quote limits or prices without a source.

## Foundry primitives, mapped to the seven decisions

| Agentic decision | Foundry primitive |
| --- | --- |
| Model routing | Model catalog deployments; a model router where available; the gateway in front (see `apim-ai-gateway`) |
| Caching | Prompt caching on supported models; semantic cache at the gateway or in app (see `azure-managed-redis-cache`) |
| Short term memory | Threads and runs (managed conversation state) |
| Long term memory | Connections to Azure AI Search or Azure Managed Redis vector store |
| Context curation | File search tool, Azure AI Search connection, your own RAG pipeline |
| Tools and MCP | Function tools, OpenAPI tools, MCP tools, code interpreter, file search |
| Identity and guardrails | Microsoft Entra Agent ID, managed identity, Content Safety, Prompt Shields |
| Evaluation and observability | Foundry evaluation framework and tracing, App Insights, OpenTelemetry |

## Blueprint steps

1. **Project and models.** Create a Foundry project. Pick models from the catalog for each routing tier (a small model for routing and extraction, a workhorse for general steps, a premium or frontier model for hard steps). Create deployments.
2. **Connections.** Add the connections the agent needs: Azure AI Search for retrieval, Azure Managed Redis for cache and memory, storage for files, and any other data source. Use managed identity on connections where supported.
   - Note from prior experience: a Foundry `AzureStorageAccount` connection target must be the Blob URI (`https://<account>.blob.core.windows.net`), not the ARM resource id.
3. **Agent definition.** Define the agent with its instructions, model, and tools. Keep the tool surface small and well described (see tools and MCP in `agentic-architecture-patterns`).
4. **Threads.** Use threads for short term memory. Add long term memory through a retrieval tool or connection, scoped by tenant and user.
5. **Guardrails and identity.** Give the agent an Entra Agent ID, use managed identity for service access, and enable Content Safety and Prompt Shields.
6. **Evaluation.** Build an eval set and run the Foundry evaluators (relevance, groundedness, coherence, safety, task success). Gate changes in CI.
7. **Observability.** Enable tracing and route telemetry to App Insights with OpenTelemetry GenAI conventions.

## Tools available in Foundry agents

- **Function tools** for your own code.
- **OpenAPI tools** to call governed HTTP APIs (register them in `azure-api-center`, front them with `apim-ai-gateway`).
- **MCP tools** to attach Model Context Protocol servers (build them with `mcp-builder`).
- **File search** for grounded retrieval over uploaded documents.
- **Code interpreter** for computation and data tasks.

## Provisioning and quotas

- For provisioning steps, identity setup, and SDK usage, route to `microsoft-foundry` and `azure-ai`.
- For model and Cognitive Services quota, the `az quota list` path can return a bad request; raise a support quota request for Cognitive Services instead. New subscriptions may need `Microsoft.ContainerRegistry` registered before creating an ACR for hosted-agent demos.

## References

- [Azure AI Foundry Agent Service](https://learn.microsoft.com/azure/ai-foundry/agents/)
- [Azure AI Foundry model catalog](https://learn.microsoft.com/azure/ai-foundry/how-to/model-catalog-overview)
- [Foundry tools](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/overview)
- [Evaluate generative AI with Azure AI Foundry](https://learn.microsoft.com/azure/ai-foundry/concepts/evaluation-approach-gen-ai)
