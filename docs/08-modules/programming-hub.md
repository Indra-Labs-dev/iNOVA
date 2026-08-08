# Programming Hub

**Status:** [PLANNED] — Phase 6
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

An AI-assisted developer environment integrated with the rest of iNOVA.

## Scope

Product-level module description. Agent-level detail is in [CodeAgent](../07-agents/agents/code-agent.md).

## Capabilities

- Code editor (Monaco Editor), project explorer, terminal.
- Git/GitHub integration, code generation, refactoring, debugging, testing.
- Static analysis, dependency analysis, documentation, architecture assistance.
- API testing, Docker workflows, CI/CD assistance, code review.
- Security-aware development, in collaboration with [Cybersecurity Hub](cybersecurity-hub.md).

## Change safety model

Every AI-proposed code change follows: **Preview → Review → Approve → Apply → Rollback**. No change is applied without human review at MVP scope.

## Dependencies

[CodeAgent](../07-agents/agents/code-agent.md), [CyberAgent](../07-agents/agents/cyber-agent.md), GitHub API (optional), Monaco Editor.

## Security considerations

Code execution/test-running requires sandboxing (see [sandboxing.md](../07-agents/sandboxing.md)).

## Related documentation

- [CodeAgent](../07-agents/agents/code-agent.md)
- [Cybersecurity Hub](cybersecurity-hub.md)
- [Testing strategy](../14-testing/strategy.md)
