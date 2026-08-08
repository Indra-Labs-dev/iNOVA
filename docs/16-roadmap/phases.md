# Phases

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Give the concrete deliverables of each roadmap phase.

## Scope

Detailed phase breakdown, consistent with [iNOVA_CAHIER_DES_CHARGES.md §9](../../iNOVA_CAHIER_DES_CHARGES.md).

## How MVP relates to these phases — read before starting Phase 0

The phases below describe when each module reaches its **full target scope** as documented in `08-modules/`. They are **not** a strict gate where nothing in Phase N+1 exists until Phase N is 100% complete.

[MVP](mvp.md) is a deliberate **vertical slice** that includes thin, reduced versions of several modules whose *full* version is scheduled for a later phase:

| Module | Full version phase | MVP slice |
|---|---|---|
| Agent Hub | Phase 4 | `ResearchAgent` only, no Agent Router complexity — see [research-agent.md](../07-agents/agents/research-agent.md) |
| News Intelligence | Phase 5 | Basic RSS/API ingestion + summarization, no dedup/classification/personalization pipeline — see [news-intelligence.md](../08-modules/news-intelligence.md) |
| Cybersecurity Hub | Phase 6 | Basic security posture + recommendations only, no CVE lookup/file analysis/full hub — see [cybersecurity-hub.md](../08-modules/cybersecurity-hub.md) |
| Mission System | Phase 4+ | A single linear task with XP, no multi-agent orchestration — see [mission-system.md](../08-modules/mission-system.md) |

This is intentional and mirrors the original product vision's MVP recommendation (prove AI + Agent + Data + Mascot + 2D/3D as one coherent experience) — it is not a roadmap inconsistency. Do not build the full version of any of these modules to satisfy the MVP requirement; build only the documented MVP slice, and expand to the full version only when that module's own phase is reached.

## Phase 0 — Foundation

Repository, architecture, design system, auth, core API, database, frontend shell. External dependencies activated: VPS, domain, PostgreSQL (see [13-devops/environments.md](../13-devops/environments.md)).

## Phase 1 — iNOVA Core

AI chat, memory, event system, tool system, permissions. External dependencies: Ollama local (Qwen2.5-3B, see [06-ai/ollama.md](../06-ai/ollama.md)).

## Phase 2 — Aira (Mascot)

Rive integration, state machine, emotions, contextual reactions (see [05-mascot/](../05-mascot/overview.md)).

## Phase 3 — iNOVA World

Three.js/WebGL, initial 3D scene, navigation, interactive objects, 2D/3D transitions (see [04-3d-world/](../04-3d-world/architecture.md)).

## Phase 4 — Agents

Agent runtime, Agent Router, `ResearchAgent`, `CodeAgent`, tool permissions, audit system (see [07-agents/](../07-agents/architecture.md)). External dependency note: Ollama local — tool-calling reliability at this model size should be actively monitored (see [06-ai/model-strategy.md](../06-ai/model-strategy.md)).

## Phase 5 — Intelligence

News, Research, watchlists, intelligent alerts, knowledge graph (see [08-modules/news-intelligence.md](../08-modules/news-intelligence.md) and related).

## Phase 6 — Cyber & Dev

Cybersecurity Hub, Programming Hub, security-aware coding workflows.

## Phase 7 — Ecosystem

Learning, Productivity, Cloud, Devices, advanced missions, advanced personalization.

## Related documentation

- [Roadmap](roadmap.md)
- [MVP](mvp.md)
- [Cahier des charges](../../iNOVA_CAHIER_DES_CHARGES.md)
