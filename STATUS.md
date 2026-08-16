# Current Status

- **classification:** USE → pilot candidate
- **mode:** brownfield
- **usb:** preserved, existing entry points unchanged
- **microsd/android:** prototype host adapter added; physical-device proof still required
- **reference agent:** Agent Max
- **local prototype tests:** 3/3 passed
- **cross-platform CI:** configured for Windows/macOS/Linux
- **production status:** NOT RELEASED
- **rollback:** revert the MAXX Cartridge PR; legacy USB files are untouched

## Open production gates

1. Physical USB removable-media smoke test.
2. Galaxy A06 + microSD/Termux test.
3. Encryption-at-rest/key management.
4. Bidirectional conflict tests.
5. Card-removal/power-loss recovery drill.
6. Five paid pilot customers before native Android investment.
