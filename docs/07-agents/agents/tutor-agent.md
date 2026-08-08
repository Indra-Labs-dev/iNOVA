# TutorAgent

**Status:** [PLANNED] — Phase 7
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Support the user's learning within the [Learning Hub](../../08-modules/learning-hub.md): explanations, exercises, adaptive guidance.

## Responsibilities

- Explain concepts at the user's current level.
- Generate/select exercises and quizzes.
- Track progress signals to adapt difficulty.

## Inputs

A learning topic/question, the user's tracked progress.

## Outputs

Explanations, exercises, progress feedback.

## Tools

- `fetch_learning_content` — LOW risk.
- `record_progress` — LOW risk (writes to user's own progress only).
- `generate_quiz` — LOW risk.

## Permissions

`learning.read`, `learning.progress.write`.

## Risks

LOW — no system access, writes confined to the user's own learning records.

## Memory

Persistent learning progress (see [10-data/entities.md](../../10-data/entities.md) `UserProgress`).

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), [Learning Hub](../../08-modules/learning-hub.md), possibly [Aira](../../05-mascot/overview.md) as learning companion.

## Events

`learning.progress.updated`, `agent.task.succeeded/failed`.

## Errors

Content unavailable for a topic → say so rather than fabricating course material as fact.

## Confirmation

Not required.

## Audit

Progress writes logged per [audit.md](../audit.md).

## Related documentation

- [Learning Hub](../../08-modules/learning-hub.md)
- [Gamification](../../08-modules/gamification.md)
