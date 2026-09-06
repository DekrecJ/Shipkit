#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
python3 -m pip install --upgrade .
python3 -m shipkit install codex
python3 -m shipkit doctor
printf '\nShipKit installation finished. Restart Codex before testing a new chat.\n'
