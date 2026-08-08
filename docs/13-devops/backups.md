# Backups

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the backup strategy for PostgreSQL and object storage.

## Scope

Data durability, not high availability.

## Requirements (once there is production data to protect)

- Regular automated PostgreSQL backups, tested restore process (an untested backup is not a backup).
- Object storage versioning/redundancy per the chosen provider's capabilities.

## Status note

No production data exists yet — this is a target requirement to implement before any real user data is stored, not before.

## Related documentation

- [Disaster recovery](disaster-recovery.md)
- [PostgreSQL](../10-data/postgresql.md)
