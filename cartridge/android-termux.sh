#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

find_card() {
  if [[ -n "${MAXX_CARD_ROOT:-}" && -f "$MAXX_CARD_ROOT/cartridge.json" ]]; then printf '%s\n' "$MAXX_CARD_ROOT"; return 0; fi
  for candidate in /storage/*-*/MAXX "$HOME/storage/external-1/MAXX"; do
    [[ -f "$candidate/cartridge.json" ]] && { printf '%s\n' "$candidate"; return 0; }
  done
  return 1
}

ROOT="$(find_card || true)"
if [[ -z "$ROOT" ]]; then
  cat >&2 <<'EOF'
MAXX cartridge not found.
Run `termux-setup-storage`, place the cartridge in a folder named MAXX on the microSD card, or set MAXX_CARD_ROOT=/path/to/MAXX.
EOF
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
CLI="$ROOT/cartridge/maxx_cartridge.py"
[[ -f "$CLI" ]] || { echo "Missing $CLI" >&2; exit 2; }

if [[ $# -eq 0 ]]; then set -- status; fi
exec "$PYTHON_BIN" "$CLI" --root "$ROOT" "$@"
