#!/usr/bin/env bash
# Instala el departamento de marketing agéntico.
# Uso: ./install.sh            -> instala a nivel usuario (~/.claude)
#      ./install.sh --project  -> instala en ./.claude del directorio actual
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${1:-}" == "--project" ]]; then
  DEST="$PWD/.claude"
else
  DEST="$HOME/.claude"
fi

mkdir -p "$DEST/agents" "$DEST/skills"
cp -R "$SRC/agents/." "$DEST/agents/"
cp -R "$SRC/skills/departamento-marketing" "$DEST/skills/"

echo "Instalado en $DEST"
echo "  - $(ls "$SRC/agents" | wc -l | tr -d ' ') agentes en $DEST/agents"
echo "  - skill departamento-marketing en $DEST/skills"
echo "Reinicia Claude Code y usa:  /departamento-marketing"
