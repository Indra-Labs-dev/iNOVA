# Glossary

**Document status:** Living document
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Shared vocabulary so that documents, code, and conversations about iNOVA use the same words for the same concepts.

| Term | Meaning |
|---|---|
| **iNOVA** | The overall product — the intelligent digital universe. |
| **iNOVA Core** | The shared backend substrate (identity, events, data) all hubs build on. See [system-context.md](../02-architecture/system-context.md). |
| **Hub** | A functional domain module (e.g. Cybersecurity Hub, News Intelligence). See [08-modules/ai-hub.md](../08-modules/ai-hub.md) onward. |
| **Aira** | The AI mascot / digital companion — part of the iNOVA ecosystem, not an alternate product name. See [05-mascot/](../05-mascot/overview.md). |
| **Agent** | A specialized, permissioned AI worker with a defined purpose and toolset. See [07-agents/architecture.md](../07-agents/architecture.md). |
| **Agent Router** | The component that routes a user intent to the right agent(s). See [agent-router.md](../07-agents/agent-router.md). |
| **Tool** | A discrete, permissioned capability an agent or the AI Hub can invoke (e.g. `create_task`). See [tools.md](../07-agents/tools.md). |
| **Permission** | An explicit scope (e.g. `productivity.tasks.write`) required before a tool can execute. See [12-security/authorization.md](../12-security/authorization.md). |
| **Mission** | A user-given high-level goal broken into a structured, inspectable multi-step plan. See [mission-system.md](../08-modules/mission-system.md). |
| **LLMProvider** | The abstraction interface between AI Core and any specific model backend (Ollama today, cloud APIs potentially later). See [llm-provider.md](../06-ai/llm-provider.md). |
| **ADR** | Architecture Decision Record — a short document capturing one significant, hard-to-reverse technical decision. See [adr/README.md](../adr/README.md). |
| **Watchlist** | A user-defined set of topics iNOVA monitors and aggregates alerts for. See [watchlists.md](../08-modules/watchlists.md). |
| **Knowledge Graph** | The semantic layer connecting entities, documents, events, and user interests. See [knowledge-graph.md](../08-modules/knowledge-graph.md). |
| **iNOVA World** | The 3D/WebGL environment layer. See [04-3d-world/](../04-3d-world/architecture.md). |
| **iNOVA Pulse** | The real-time visual intelligence center aggregating activity across hubs. See [nova-pulse.md](../08-modules/nova-pulse.md). |

## Related documentation

- [Scope](scope.md)
- [Feature matrix](../01-product/feature-matrix.md)
