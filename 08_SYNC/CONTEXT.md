# Offline-First Sync Contract

## Source of truth
The cartridge is authoritative for portable agent state. Cloud/LAN copies are replicas and compute partners, not mandatory dependencies.

## Journal
Every meaningful mutation should append an event containing timestamp, operation, relative path, and optional metadata. The reference implementation stores JSON Lines at `08_SYNC/journal/events.jsonl`.

## Snapshots
Content-hash manifests provide a deterministic baseline. Sync compares a new manifest with a prior manifest and emits changed/deleted paths.

## Conflict rule
Never overwrite silently. If local and remote both changed the same logical object after their shared baseline, place both candidates and a conflict record in `08_SYNC/conflicts/` for deterministic or human resolution.

## Code
Git remains the preferred transport for code/projects. The cartridge journal remains the cross-file-system audit trail and covers non-Git user data.

## Network return flow

1. Create current snapshot.
2. Build delta against last acknowledged baseline.
3. Verify mutation policy.
4. Push Git commits and/or upload changed content.
5. Receive remote results into `incoming/`.
6. Verify before applying.
7. Record acknowledged baseline.
