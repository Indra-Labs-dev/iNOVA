# CloudAgent

**Status:** [PLANNED] — Phase 7
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Help the user understand and troubleshoot infrastructure within [Cloud / Infrastructure Hub](../../08-modules/cloud-hub.md).

## Responsibilities

- Inspect Docker/server/database/deployment status.
- Explain infrastructure problems and suggest fixes.

## Inputs

An infrastructure question or problem description, read access to the relevant systems.

## Outputs

Diagnosis and suggested remediation — presented for review, not auto-applied.

## Tools

- `inspect_container_status` — LOW risk.
- `read_logs` — LOW risk.
- `suggest_fix` — LOW risk (produces text, no execution).
- Any tool that would restart/modify infrastructure is HIGH risk and out of MVP scope — see [12-security/agent-security.md](../../12-security/agent-security.md).

## Permissions

`cloud.read`, scoped per-resource.

## Risks

LOW for read/diagnostic tools; explicitly **no destructive automation by default** per the product vision.

## Memory

Infrastructure state snapshots, not persistent beyond diagnostic session unless explicitly retained.

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), Docker/infra tooling (see [13-devops/docker.md](../../13-devops/docker.md)).

## Events

`agent.task.succeeded/failed`.

## Errors

Inaccessible resource → report clearly; never assume a default/fallback infra target.

## Confirmation

Not required for read-only diagnosis; any future remediation action would be HIGH risk with mandatory confirmation.

## Audit

All inspected resources logged per [audit.md](../audit.md).

## Related documentation

- [Cloud / Infrastructure Hub](../../08-modules/cloud-hub.md)
- [DevOps](../../13-devops/docker.md)
