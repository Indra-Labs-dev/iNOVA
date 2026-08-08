# Backend Architecture

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the backend's internal layering and how it stays independent from any specific frontend.

## Scope

Backend-wide structure. Component-level detail is in [02-architecture/components.md](../02-architecture/components.md).

## Principle

The backend exposes a stable API contract; it has no knowledge of Flutter or Three.js specifics. This is what lets the frontend evolve (or be replaced) independently — see [00-overview/vision.md](../00-overview/vision.md), "keep the frontend independent from backend implementation details."

## Stack

Python + FastAPI, PostgreSQL, Redis, WebSocket for real-time, background workers for async jobs (see [background-jobs.md](background-jobs.md)).

## Related documentation

- [FastAPI](fastapi.md)
- [API design](api-design.md)
- [Components](../02-architecture/components.md)
