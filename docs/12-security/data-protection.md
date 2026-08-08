# Data Protection

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how user data is protected at rest and how deletion works.

## Scope

Data lifecycle security. Entity-level structure is in [10-data/entities.md](../10-data/entities.md).

## Requirements

- Sensitive fields encrypted at rest where appropriate (`TODO — decision required` on scope — at minimum, credentials/session data).
- User-initiated data deletion must actually remove/anonymize records, not just hide them — including `Memory`, `Conversation`, and `Document` entities.
- Personalization data ([06-ai/memory.md](../06-ai/memory.md)) must be user-visible and user-deletable, per [00-overview/objectives.md](../00-overview/objectives.md) Objective 3.

## Related documentation

- [Entities](../10-data/entities.md)
- [Memory](../06-ai/memory.md)
- [Security architecture](security-architecture.md)
