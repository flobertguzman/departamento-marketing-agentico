# Instrucciones para agentes de IA (Codex / Claude Code)

Este repositorio es el **Departamento de Marketing Agéntico**: 14 agentes de marketing + un skill con un loop de trabajo.

## Si el usuario pide instalarlo («instala esto», «instálalo», «install this»)

**En Codex:**
1. Ejecuta `./codex/install.sh` desde la raíz de este repo (instalación solo en el proyecto actual: `./codex/install.sh --project`).
2. Verifica que existan `~/.agents/skills/departamento-marketing/SKILL.md` y 14 archivos `~/.codex/agents/mkt_*.toml`.
3. Informa lo instalado y que se usa con `$departamento-marketing`. Si no aparece, que reinicie Codex.

**En Claude Code:**
1. Ejecuta `./install.sh` desde la raíz (o `./install.sh --project`).
2. Verifica `~/.claude/agents/mkt-*.md` (14) y `~/.claude/skills/departamento-marketing/`.
3. Informa que se usa con `/departamento-marketing`.

No modifiques otros archivos, ni la configuración de la herramienta, ni ejecutes nada más.

## Estructura
- `agents/`, `skills/` — versión Claude Code (fuente de verdad).
- `codex/` — versión Codex, **generada** con `python3 tools/build_codex.py`. No la edites a mano.
- `PROMPT.md`, `codex/PROMPT.md` — prompts maestros para crear el departamento desde cero.
