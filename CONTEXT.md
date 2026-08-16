# MAXX Portable Cartridge — Root Router

This repository remains the USB-portable Hermes runtime and now also defines the MAXX Cartridge sidecar for microSD/Android.

## Read order

1. `00_SYSTEM/CONTEXT.md` — architecture, invariants, and compatibility rules.
2. `01_IDENTITY/agent-max/IDENTITY.md` — reference test agent.
3. `04_WORK/CONTEXT.md` — work pipeline.
4. `08_SYNC/CONTEXT.md` — offline-first sync contract.
5. `09_HOSTS/CONTEXT.md` — host adapters.

## Invariant

The existing `launch.bat`, `launch.sh`, and `scripts/` USB behavior is preserved. New cartridge functionality is additive. Portable user/agent state is distinct from host-runtime state.

## Walk test

A fresh agent with no conversation history must be able to read this file, identify Agent Max, locate current work, identify the active host, and determine whether changes are local, synced, or conflicted without loading the whole repository.
