# iNOVA Documentation

**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

This is the entry point into iNOVA's complete technical and product documentation. Start here, then follow links into the section you need.

## Read this first

- [PROJECT_STATUS.md](PROJECT_STATUS.md) — what actually exists in the repository right now. Everything else in this folder describes target vision or target architecture; this file is the only one that describes reality.
- [ARCHITECTURE_FREEZE.md](ARCHITECTURE_FREEZE.md) — the 2026-08-08 architecture freeze: confirmed decisions, open decisions, constraints, boundaries, forbidden shortcuts, and the next implementation step (Phase 0). Read this before writing any code.
- [00-overview/scope.md](00-overview/scope.md) — explains the three-layer distinction (Product Vision / Architecture Target / Current Implementation) used throughout this documentation, and the status labels (`[PLANNED]`, `[IMPLEMENTED]`, etc.) every document uses.

## Navigation

1. **[iNOVA](00-overview/vision.md)** — what iNOVA is and why it exists → [objectives](00-overview/objectives.md), [philosophy](00-overview/product-philosophy.md), [scope](00-overview/scope.md), [glossary](00-overview/glossary.md), [authorship](00-overview/authorship.md)
2. **[Product](01-product/product-overview.md)** — personas, journeys, requirements, feature matrix
3. **[Architecture](02-architecture/overview.md)** — system context, containers, components, data/event flow, integration map, ADR process
4. **[Frontend](03-frontend/architecture.md)** — Flutter, Riverpod, design system, navigation, accessibility
5. **[3D World](04-3d-world/architecture.md)** — Three.js, WebGL, scene architecture, assets, performance, 2D/3D integration
6. **[Mascotte (Aira)](05-mascot/overview.md)** — character, states, Rive, state machine, events
7. **[IA](06-ai/architecture.md)** — LLMProvider, Ollama, model strategy, memory, retrieval, tool use
8. **[Agents](07-agents/architecture.md)** — lifecycle, router, orchestration, permissions, tools, sandboxing, audit, and [individual agent fiches, starting with ResearchAgent](07-agents/agents/research-agent.md)
9. **[Cybersecurity](08-modules/cybersecurity-hub.md)** — see also [Programming Hub](08-modules/programming-hub.md)
10. **[Programming](08-modules/programming-hub.md)** — Monaco, Git/GitHub, CodeAgent workflow
11. **[3D](04-3d-world/architecture.md)** — see section 5 above
12. **[Data](10-data/data-architecture.md)** — PostgreSQL, Redis, object storage, entities, schema, migrations
13. **[Security](12-security/security-architecture.md)** — threat model, auth, agent security, secrets, audit logging
14. **[DevOps](13-devops/environments.md)** — environments, Docker, CI/CD, monitoring, backups
15. **[Testing](14-testing/strategy.md)** — unit through E2E, agent-specific and security-specific tests
16. **[Roadmap](16-roadmap/roadmap.md)** — phases, MVP, v1/v2, future
17. **[ADR](adr/README.md)** — every significant architecture decision, with rationale

## Full module index

All 15 functional hubs (AI Hub, Cybersecurity Hub, Programming Hub, Research Hub, News Intelligence, OSINT Hub, Knowledge Graph, Watchlists, Learning Hub, Productivity Hub, Device Hub, Cloud Hub, Mission System, iNOVA Pulse, Gamification) are documented individually starting from [08-modules/ai-hub.md](08-modules/ai-hub.md).

Every one of iNOVA's 9 planned agents (ResearchAgent, CodeAgent, CyberAgent, OSINTAgent, TutorAgent, DataAgent, CloudAgent, WriterAgent, ProductivityAgent) has its own fiche starting from [07-agents/agents/research-agent.md](07-agents/agents/research-agent.md).

## Development

- [Setup](15-development/setup.md) — get a local environment running (currently `[PARTIAL]` — see the file for what's actionable today vs. still `TODO`).
- [Conventions](15-development/conventions.md), [Git workflow](15-development/git-workflow.md), [Code review](15-development/code-review.md), [Dependency policy](15-development/dependency-policy.md).

## Source-of-truth documents outside `docs/`

- [`iNOVA_MASTER_CONTEXT.md`](../iNOVA_MASTER_CONTEXT.md) — the original product vision brief.
- [`iNOVA_CAHIER_DES_CHARGES.md`](../iNOVA_CAHIER_DES_CHARGES.md) — specifications derived from it, including external dependencies and budget.
- [`iNOVA_OBJECTIFS_FONCTIONNALITES_STACK.md`](../iNOVA_OBJECTIFS_FONCTIONNALITES_STACK.md) — detailed objective/feature/stack reference.

This `docs/` folder is the technical elaboration of those three documents — it does not replace them, and cross-links back to them where relevant.
