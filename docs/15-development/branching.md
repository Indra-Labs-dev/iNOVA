# Branching

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define branch naming and lifecycle.

## Scope

Naming convention only — process is in [git-workflow.md](git-workflow.md).

## Convention

`TODO — decision required` on exact naming scheme.

### Options

| Option | Pros | Cons |
|---|---|---|
| `type/short-description` (e.g. `feature/research-agent`, `fix/tool-validation`) | Simple, widely understood convention, low overhead | Doesn't indicate which `docs/` module/architecture area a change touches |
| `type/docs-module-short-description` (e.g. `feature/07-agents-research-agent`) | Branch name maps predictably to the documentation module it touches, useful given this repo's module-first structure | More verbose; only useful once documentation module boundaries stay stable |
| Ticket/issue-ID-based (e.g. `feature/INOVA-42-research-agent`) | Ties branches to an issue tracker for traceability | Requires an issue tracker to be in place first — none exists yet |

### Decision criteria

- **Contributor count**: with a single contributor (current state), any convention works; formalize before a second contributor joins to avoid inconsistent history.
- **Issue tracker adoption**: if GitHub Issues (or another tracker) becomes the source of task truth, the ticket-ID convention becomes more valuable — not decided yet.
- **Consistency with this documentation's module numbering** (`00-overview` … `16-roadmap`) is a reasonable tiebreaker given how this repo is already organized, but is not itself a requirement.

## Related documentation

- [Git workflow](git-workflow.md)
