# Host Adapters

Host adapters make one cartridge usable across devices without changing portable state.

## USB desktop host
The existing root `launch.bat`, `launch.sh`, and `scripts/` remain canonical compatibility entry points for Windows/macOS/Linux. Their behavior is not replaced by the cartridge layer.

## Android microSD host
The first prototype host is Termux because it gives us a real shell, Python, Git, SSH, and removable-storage access today without requiring a custom APK. `cartridge/android-termux.sh` discovers a mounted `MAXX` cartridge and launches the same reference CLI.

A later native Android app should replace Termux as the consumer experience while preserving the cartridge format and sync contract.

## Host-local state
Runtime executables, virtual environments, hot caches, temporary KV caches, and platform-specific locks may live in internal storage. Durable identity, memory, skills, projects, user files, model inventory, journals, and recovery manifests remain portable.
