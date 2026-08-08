# Cloud / Infrastructure Hub

**Status:** [PLANNED] — Phase 7
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Help the user understand and manage infrastructure they own.

## Scope

Product-level module description. Agent-level detail is in [CloudAgent](../07-agents/agents/cloud-agent.md).

## Capabilities

Docker, servers, virtual machines, databases, APIs, logs, monitoring, backups, deployments. iNOVA can explain an infrastructure problem and suggest fixes.

## Boundaries

No destructive automation by default — every remediation action is HIGH risk and requires explicit confirmation (see [07-agents/permissions.md](../07-agents/permissions.md)).

## Dependencies

[CloudAgent](../07-agents/agents/cloud-agent.md), [DevOps tooling](../13-devops/docker.md).

## Related documentation

- [CloudAgent](../07-agents/agents/cloud-agent.md)
- [DevOps](../13-devops/environments.md)
