# MAXX Cartridge Gauntlet

## Goal
Preserve Hermes USB portability while adding an ICM-organized removable-storage cartridge and a microSD/Android sidecar that can work offline and synchronize later.

## Named bars

1. **Existing Hermes USB Portable behavior in this repository** — our change must not remove or repurpose the current Windows/macOS/Linux launchers or portable-data model.
2. **RinDig/icm-architect walk test** — a fresh agent with no prior memory must orient, act, and report status from filesystem routing/state alone.
3. **Git-style change safety** — content-addressed snapshots, explicit deltas, and no silent conflict overwrite for portable work state.

## Builder/critic gates

### Portability
- PASS: Existing USB entry points remain untouched.
- PASS: New code is stdlib-only Python and host-neutral.
- PASS: CI runs on Windows, macOS, and Linux.
- OPEN: Physical USB launch smoke test on real removable media.

### ICM
- PASS: Root router exists.
- PASS: Identity, work, sync, host, recovery layers are explicitly routed.
- PASS: Agent Max is a named reference identity.
- PASS: Prototype initialization produces a minimal fresh-agent routing structure.
- OPEN: Fresh-model walk test on a physical cartridge.

### microSD / Android
- PASS: Android is a sidecar; USB remains first-class.
- PASS: Termux adapter can discover a `MAXX` microSD mount or accept an explicit path.
- PASS: Cartridge data model does not require rooting Android.
- OPEN: Physical Galaxy A06 + microSD execution test.
- OPEN: Native Android app with scoped-storage permission UX.

### Data safety
- PASS: Import copies source data rather than moving/deleting it.
- PASS: Import refuses to overwrite an existing destination.
- PASS: SHA-256 snapshot manifests provide a recovery baseline.
- PASS: Sync plan emits changed/deleted paths rather than directly overwriting a remote.
- OPEN: Encryption-at-rest and key-management implementation.
- OPEN: Bidirectional conflict resolver and restore drill.

### Commercial
- PASS: Offer is one repeatable pilot, not custom software for each buyer.
- PASS: Cloud is optional enhancement rather than product dependency.
- PASS: 5 paid pilots are the gate before native Android investment.
- OPEN: Actual paid-customer evidence, support-cost evidence, and hardware-failure evidence.

## Current verdict

**Prototype: PASS. Production product: NOT YET.**

The repository now contains a testable cross-platform cartridge reference implementation and Android sidecar architecture. It must not be represented as a production-safe consumer product until the open physical-device, encryption, conflict, recovery, and paid-pilot gates are satisfied.
