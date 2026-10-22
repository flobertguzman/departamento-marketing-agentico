#!/usr/bin/env bash
# Instala el departamento de marketing agéntico para Codex.
# Uso: ./install.sh            -> a nivel usuario (~/.agents/skills y ~/.codex/agents)
#      ./install.sh --project  -> en el directorio actual (.agents/skills y .codex/agents)
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/departamento-marketing"

if [[ "${1:-}" == "--project" ]]; then
  SKILLS="$PWD/.agents/skills"
else
  SKILLS="$HOME/.agents/skills"
fi

mkdir -p "$SKILLS"
rm -rf "$SKILLS/departamento-marketing"
cp -R "$SRC" "$SKILLS/"
sh "$SKILLS/departamento-marketing/scripts/install-agents.sh" "$@"

echo "Skill instalado en $SKILLS/departamento-marketing"
echo "Reinicia Codex y usa:  \$departamento-marketing"
