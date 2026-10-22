#!/usr/bin/env sh
# Instala los 14 agentes personalizados (mkt_*.toml) que acompañan a este skill.
# Uso: install-agents.sh            -> ~/.codex/agents
#      install-agents.sh --project  -> ./.codex/agents (proyecto actual)
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../custom-agents"
if [ "${1:-}" = "--project" ]; then DEST="$PWD/.codex/agents"; else DEST="$HOME/.codex/agents"; fi
mkdir -p "$DEST"
cp "$SRC"/*.toml "$DEST"/
echo "OK: $(ls "$SRC"/*.toml | wc -l | tr -d ' ') agentes instalados en $DEST"
echo "Si Codex no los lista todavía, reinícialo."
