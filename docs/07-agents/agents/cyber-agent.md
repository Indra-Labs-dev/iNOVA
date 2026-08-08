# CyberAgent

**Status:** [PLANNED] — Phase 6
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Perform authorized, defensive security analysis and produce prioritized recommendations.

## Responsibilities

- Analyze device/application/network posture within [Cybersecurity Hub](../../08-modules/cybersecurity-hub.md) boundaries.
- Classify vulnerabilities, cross-reference CVE data.
- Collaborate with `CodeAgent` on security-aware development flows.

## Inputs

An authorized target (the user's own device/project/domain), an analysis intent.

## Outputs

A security finding report with severity classification and recommendations — never an automated remediation applied without review.

## Tools

- `check_device_posture` — LOW risk.
- `lookup_cve` — LOW risk (public data).
- `analyze_dependency_vulnerabilities` — LOW risk.
- `check_url_reputation` — LOW risk (public data).
- Any tool implying active scanning of third-party systems is explicitly **out of scope** — see [cybersecurity-hub.md](../../08-modules/cybersecurity-hub.md) boundaries.

## Permissions

`security.read`, scoped to systems the user owns or is explicitly authorized on (`TODO — decision required` on how authorization is verified/recorded).

## Risks

LOW to MEDIUM — this agent is intentionally read/analysis-only; it never modifies systems it evaluates.

## Memory

Findings history per project/device, feeding [Watchlists](../../08-modules/watchlists.md) and [iNOVA Pulse](../../08-modules/nova-pulse.md).

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), CVE/NVD public API (see [integration-map.md](../../02-architecture/integration-map.md)), `CodeAgent`.

## Events

`security.finding.critical`, `security.finding.warning`, `agent.task.succeeded/failed`.

## Errors

CVE source unavailable, ambiguous ownership/authorization of target → refuse to analyze rather than guess.

## Confirmation

Not required for analysis (read-only); any future remediation tool would require confirmation per [permissions.md](../permissions.md).

## Audit

Every finding and its source logged per [audit.md](../audit.md).

## Related documentation

- [Cybersecurity Hub](../../08-modules/cybersecurity-hub.md)
- [CodeAgent](code-agent.md)
- [Threat model](../../12-security/threat-model.md)
