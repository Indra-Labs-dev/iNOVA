# Audit

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what gets logged for every agent action, so any action can be reconstructed after the fact.

## Scope

Agent-specific audit trail. General audit logging infrastructure is in [12-security/audit-logging.md](../12-security/audit-logging.md).

## Trail contents

```text
User request
   |
Agent decision
   |
Tool selected
   |
Permission check (result)
   |
Confirmation (if applicable, and outcome)
   |
Execution
   |
Result
   |
Audit log entry
```

Every step in this chain is logged, not just the final result — this is what makes agent actions transparent and reviewable per the product philosophy (see [00-overview/product-philosophy.md](../00-overview/product-philosophy.md)).

## Storage

Audit entries persist in PostgreSQL as their own entity (`AuditLog`, see [10-data/entities.md](../10-data/entities.md)), never only in application logs — logs can rotate away; audit records must not.

## Related documentation

- [Permissions](permissions.md)
- [Audit logging (infra-level)](../12-security/audit-logging.md)
- [Data entities](../10-data/entities.md)
