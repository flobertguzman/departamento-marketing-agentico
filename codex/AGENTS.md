# Instrucciones para Codex

Esta carpeta contiene el **Departamento de Marketing Agéntico** para Codex: un skill (`skills/departamento-marketing`) y 14 agentes personalizados (`skills/departamento-marketing/custom-agents/*.toml`).

## Si el usuario pide instalarlo («instala esto», «instálalo», «install this»)

1. Ejecuta, desde esta carpeta, `./install.sh` (o `sh install.sh`). Para instalarlo solo en el proyecto actual: `./install.sh --project`.
2. Verifica que existan `~/.agents/skills/departamento-marketing/SKILL.md` y los 14 archivos `~/.codex/agents/mkt_*.toml`.
3. Responde al usuario con lo instalado y dile que use `$departamento-marketing`. Si Codex no muestra el skill o los agentes, que reinicie Codex.
4. No modifiques ningún otro archivo, ni la configuración de Codex, ni ejecutes nada más.

## Si el usuario pide usarlo
Invoca el skill `departamento-marketing` y sigue su `SKILL.md`.
