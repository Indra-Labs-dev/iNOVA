# Audit

**Status:** [TESTED] — `AuditLog` implemented (Gate 2), verified against a real PostgreSQL instance
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

## Storage — implemented

`audit_logs` table (`backend/app/models/audit_log.py`, migration `4fab2f4a1757`): `id, user_id, agent_name, tool_name, permission, risk, outcome, success, result_summary, created_at` — answers who/what/when/which agent/which tool/which permission/result/success-failure. `result_summary` is bounded to 500 characters and truncated defensively (`AuditLogRepository.record`), never carries secrets — see [12-security/secrets.md](../12-security/secrets.md).

### Outcomes covered (Gate 2)

`SUCCESS`, `PERMISSION_DENIED`, `INVALID_TOOL_CALL` (covers both malformed JSON and a hallucinated/unregistered tool name), `INVALID_ARGUMENTS`, `CONFIRMATION_REQUIRED`, `EXECUTION_FAILED` — each written for real by `ResearchAgent` (`backend/app/agents/research_agent.py`), verified in `backend/tests/test_research_agent.py` and live against a real PostgreSQL instance. A genuine "no tool needed" plain-text answer is intentionally not audited — it isn't a permissioned/tool action.

## Related documentation

- [Permissions](permissions.md)
- [Audit logging (infra-level)](../12-security/audit-logging.md)
- [Data entities](../10-data/entities.md)
- [ResearchAgent](agents/research-agent.md)
