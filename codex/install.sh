#!/usr/bin/env bash
# Instala el departamento de marketing agéntico para Codex.
# Uso: ./install.sh            -> a nivel usuario (~/.agents/skills y ~/.codex/agents)
#      ./install.sh --project  -> en el directorio actual (.agents/skills y .codex/agents)
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "${1:-}" == "--project" ]]; then
  SKILLS="$PWD/.agents/skills"
  AGENTS="$PWD/.codex/agents"
else
  SKILLS="$HOME/.agents/skills"
  AGENTS="$HOME/.codex/agents"
fi

mkdir -p "$SKILLS" "$AGENTS"
rm -rf "$SKILLS/departamento-marketing"
cp -R "$SRC/skills/departamento-marketing" "$SKILLS/"
cp "$SRC/agents/"*.toml "$AGENTS/"

echo "Instalado:"
echo "  - skill  -> $SKILLS/departamento-marketing"
echo "  - $(ls "$SRC/agents" | wc -l | tr -d ' ') agentes -> $AGENTS"
echo "Reinicia Codex y usa:  \$departamento-marketing"
