# Logging

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define application logging conventions, distinct from the audit log (which is a data record, not a log stream).

## Scope

Operational/debug logging.

## Rules

- Structured logging (not free-text) once implemented, to support later monitoring integration.
- Never log secrets, tokens, or full user message content at INFO level or above — see [secrets.md](../12-security/secrets.md).
- Logs are for operational debugging; they are not a substitute for the [audit log](../12-security/audit-logging.md), which is the compliance/security record of truth.

## Related documentation

- [Monitoring](monitoring.md)
- [Audit logging](../12-security/audit-logging.md)
