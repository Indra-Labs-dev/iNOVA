# Object Storage

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define where files (as opposed to structured data) are stored.

## Scope

File/asset storage strategy.

## Approach

- Local dev: local disk or MinIO.
- Production: S3-compatible provider (see [iNOVA_CAHIER_DES_CHARGES.md §5.1](../../iNOVA_CAHIER_DES_CHARGES.md) for cost notes on AWS S3 vs Cloudflare R2).

## Contents

User-uploaded documents, 3D assets (GLTF/GLB — see [04-3d-world/assets.md](../04-3d-world/assets.md)), avatar/mascot assets, generated reports.

## Related documentation

- [Data architecture](data-architecture.md)
- [3D assets](../04-3d-world/assets.md)
