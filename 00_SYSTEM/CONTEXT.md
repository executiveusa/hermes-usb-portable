# System Context

## Mode
Brownfield. Preserve verified USB portability while adding a microSD/Android sidecar.

## Outcome
One portable agent identity/workspace can run from USB on desktop hosts and from microSD on Android, work offline, journal changes, and synchronize later without making cloud state authoritative.

## Architecture

1. **ICM portable state** — identity, memory, skills, work, projects, user data, model inventory, sync journal, recovery manifests.
2. **Hermes portable core** — existing execution/tool runtime. Existing root launchers remain compatibility entry points.
3. **Resource working set** — Colibri-inspired hot/cold placement. RAM/internal flash hold active model/context/cache; removable storage holds cold models, durable memory, projects and user data.
4. **Host adapters** — USB desktop now; Android/Termux prototype beside it; future native Android APK can replace Termux without changing cartridge format.
5. **Compute routing** — local first; LAN/cloud escalation only when required or approved.

## Non-negotiable invariants

- USB functionality cannot regress.
- microSD is durable/cold storage, not fake RAM.
- No silent destructive migration of customer files.
- Original imports are copied before organization.
- Never silently overwrite sync conflicts.
- Card loss must not expose plaintext production secrets by default.
- Cloud sync is optional; cartridge remains usable offline.
- Executable/runtime-sensitive caches may live on host-local internal storage; durable state stays portable.
- Every mutation must be journalable and recoverable.

## Canonical ICM map

- `01_IDENTITY/` agent identity and policy
- `02_MEMORY/` durable memory
- `03_SKILLS/` skill catalog and packages
- `04_WORK/` intake → execute → verify → ready-to-sync
- `05_PROJECTS/` project workspaces
- `06_USER_DATA/` user-controlled imports/files
- `07_MODELS/` model manifests and optional weights
- `08_SYNC/` incoming/outgoing/conflicts/journal
- `09_HOSTS/` platform adapters
- `99_RECOVERY/` immutable snapshots/manifests

## Resource policy

**RAM:** active inference/context only.  
**Phone internal storage:** runtime, hot cache, SQLite indexes, temporary KV/cache.  
**microSD/USB:** durable models, memory, skills, projects, user files, snapshots.  
**Cloud/LAN:** large-model reasoning, builds, CI, backups and collaboration.

## Proof gate

A release is not "done" until the USB launcher baseline still works and a removable-storage Agent Max cartridge can: initialize, pass the walk test, import without modifying the source, produce a content-hash snapshot, detect changed files, and produce a deterministic sync plan.
