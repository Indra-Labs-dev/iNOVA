# Background Jobs

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what runs asynchronously outside the request/response cycle.

## Scope

Job/worker architecture.

## Known use cases

- Scheduled News Intelligence ingestion (see [11-intelligence/ingestion.md](../11-intelligence/ingestion.md)).
- Long-running mission execution steps (see [08-modules/mission-system.md](../08-modules/mission-system.md)).
- Local LLM inference when queued rather than synchronous, given hardware constraints (see [06-ai/model-strategy.md](../06-ai/model-strategy.md)).

## Status note

No job runner chosen yet. `TODO — decision required` — avoid over-engineering this before real async workloads exist.

### Options

| Option | Pros | Cons |
|---|---|---|
| Simple asyncio-based scheduler (in-process, e.g. `asyncio` background tasks) | No new infrastructure dependency, matches MVP-scale simplicity | No persistence/retry across process restarts, doesn't scale past a single backend instance |
| Celery | Mature, persistent, retry/scheduling built-in, widely used with FastAPI | New infrastructure dependency (broker, worker process), meaningful operational overhead for MVP scale |
| RQ (Redis Queue) | Lighter than Celery, reuses Redis already in the stack ([10-data/redis.md](../10-data/redis.md)) | Fewer features than Celery (simpler retry/scheduling semantics) |

### Decision criteria

- **Actual async workload volume**: at MVP scale (single News Intelligence ingestion job, occasional mission steps), an in-process scheduler is likely sufficient — do not adopt Celery/RQ speculatively.
- **Persistence requirement**: if a job must survive a backend restart or run across multiple backend instances, in-process scheduling is disqualified.
- **Existing infrastructure**: RQ reuses Redis already required for the event bus ([02-architecture/event-flow.md](../02-architecture/event-flow.md)), making it the lower-cost upgrade path over Celery if/when an in-process scheduler proves insufficient.
- **Trigger to revisit**: when a job needs guaranteed retry/persistence, or when job volume causes noticeable backend request latency — not before.

## Related documentation

- [Architecture](architecture.md)
- [Ingestion](../11-intelligence/ingestion.md)
