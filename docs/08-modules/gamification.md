# Gamification

**Status:** [PARTIAL] — XP only (Gate 3), rest introduced progressively from MVP onward
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 3 — Mission System MVP)

## Purpose

Encourage genuinely useful behavior without manipulating the user.

## Scope

Product-level module description.

## Capabilities

XP, levels, streaks, missions, achievements, unlockable visual elements, mascot customization, world evolution.

## MVP implementation (Gate 3, implemented)

Only XP exists so far: `UserProgress` (`backend/app/models/user_progress.py`), one row per user, additive-only (`UserProgressRepository.add_xp()`, rejects negative amounts, no `set_xp`). Awarded exclusively by `MissionService` on a successful mission — see [Mission System](mission-system.md). No levels, streaks, achievements, unlockable visuals, mascot customization, or world evolution yet; no leaderboard or achievements UI in the frontend.

## Principle

Gamification must reward real product engagement (completing a mission, maintaining a useful habit) — never engagement for its own sake (e.g. no streak mechanics that punish a user for a legitimate break). See [product-philosophy.md](../00-overview/product-philosophy.md).

## Dependencies

[Mission System](mission-system.md), [10-data/entities.md](../10-data/entities.md) (`Achievement`, `UserProgress`).

## Related documentation

- [Mission System](mission-system.md)
- [Learning Hub](learning-hub.md)
