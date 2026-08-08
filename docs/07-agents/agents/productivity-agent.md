# ProductivityAgent

**Status:** [PLANNED] — Phase 7
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Help organize tasks, calendar, and planning within [Productivity Hub](../../08-modules/productivity-hub.md).

## Responsibilities

- Propose schedules/plans from available context.
- Create/update tasks and reminders — with confirmation for anything that modifies existing important records.

## Inputs

A planning intent (e.g. "organize my day"), permitted calendar/task context.

## Outputs

A proposed plan or created/updated records.

## Tools

- `create_task` — LOW risk, confirmation optional.
- `update_task` — LOW to MEDIUM risk depending on whether it's a new or existing important record.
- `propose_schedule` — LOW risk (proposal only, no writes).

## Permissions

`productivity.tasks.read`, `productivity.tasks.write`, `productivity.calendar.read`.

## Risks

LOW to MEDIUM — creating new items is low risk; modifying/deleting existing important records requires confirmation.

## Memory

User's productivity patterns/preferences, within the personalization boundaries of [06-ai/memory.md](../../06-ai/memory.md).

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), [Productivity Hub](../../08-modules/productivity-hub.md) data.

## Events

`agent.task.succeeded/failed`, `mission.step.completed` when part of a mission.

## Errors

Conflicting calendar data → surface the conflict, do not silently pick a resolution.

## Confirmation

Required before creating/modifying important records (per the product vision's productivity example).

## Audit

Every task/record change logged per [audit.md](../audit.md).

## Related documentation

- [Productivity Hub](../../08-modules/productivity-hub.md)
- [Gamification](../../08-modules/gamification.md)
