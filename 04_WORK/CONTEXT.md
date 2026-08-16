# Work Pipeline

The portable work state is intentionally small and inspectable.

## Stages

- `00_INTAKE/` — requests and events not yet accepted.
- `01_EXECUTE/` — active local work and tool outputs.
- `02_VERIFY/` — independent checks, diffs, tests, and evidence.
- `03_READY_TO_SYNC/` — verified local changes waiting for network or explicit sync.
- `04_COMPLETE/` — synchronized or intentionally local completed work.

## Contract

A builder cannot approve its own work. Any change that can affect user data, code, credentials, messaging, money, or system configuration must carry evidence appropriate to its risk before moving to `03_READY_TO_SYNC/`.

Offline is not an error state. Work may stop at `03_READY_TO_SYNC/` indefinitely and resume when connectivity returns.
