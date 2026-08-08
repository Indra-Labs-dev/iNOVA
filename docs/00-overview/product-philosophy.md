# Product Philosophy

**Document status:** Stable
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

State the non-negotiable principles that resolve ambiguity when a feature decision isn't obvious from the spec.

## Scope

Applies to every module, at every phase, regardless of how the roadmap evolves.

## The core principle

> **iNOVA should feel alive without pretending to be alive.**

The mascot can be expressive. The world can react. The AI can be conversational. The interface can evolve. But the product must remain **predictable, transparent, controllable, secure, and respectful of user privacy**. The futuristic experience must never obscure what the system is actually doing.

## Priority order when principles conflict

```text
Clean architecture → Security → Functionality → Tests → Performance → Advanced visual experience
```

3D and futuristic effects are important to iNOVA's identity, but they must never become an excuse to build a technically fragile system.

## Development principles

1. Understand before modifying.
2. Inspect existing architecture before creating new files.
3. Do not rewrite functioning systems without a clear reason.
4. Prefer small, isolated changes.
5. Avoid giant source files; keep modules cohesive.
6. Use typed models and explicit interfaces.
7. Separate UI, business logic, data access, and infrastructure.
8. Do not duplicate functionality.
9. Do not introduce dependencies without justification.
10. Never expose secrets in source code.
11. Add tests for meaningful business logic.
12. Preserve backward compatibility where reasonable.
13. Run relevant tests after changes.
14. Fix root causes rather than hiding symptoms.
15. Document important architectural decisions (see [adr/](../adr/README.md)).
16. Do not implement speculative features merely because they appear in the vision documents.
17. Treat the vision documents as context, not as a command to build the entire roadmap immediately.

## Agent principle

An AI agent must never automatically gain unrestricted access to the user's system, files, network, credentials, or external services. See [12-security/agent-security.md](../12-security/agent-security.md).

## Related documentation

- [Vision](vision.md)
- [Objectives](objectives.md)
- [Scope](scope.md)
- [Security architecture](../12-security/security-architecture.md)
