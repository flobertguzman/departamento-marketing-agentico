# Instalación

Elige la forma que prefieras. Las tres dejan lo mismo: el skill `departamento-marketing` y los 14 agentes.

## 1. Pídeselo a Codex (la más fácil)

Pega esto en Codex:

```text
Instala el skill departamento-marketing desde https://github.com/flobertguzman/departamento-marketing-agentico (ruta codex/skills/departamento-marketing) con $skill-installer. Luego ejecuta su script scripts/install-agents.sh y confírmame qué quedó instalado.
```

> Requiere que el repositorio sea público. Si es privado, usa la opción 2.

Aunque solo se instale el skill, **se completa solo**: la primera vez que lo uses, el skill comprueba si faltan los agentes y ejecuta su propio `scripts/install-agents.sh`.

## 2. Descarga el zip y dáselo a Codex

1. En GitHub: **Code → Download ZIP** (o el zip de la sección *Releases*).
2. Descomprímelo y abre Codex **dentro de esa carpeta**.
3. Escribe: `Instala esto.`

Codex lee el `AGENTS.md` de la carpeta, ejecuta el instalador y verifica el resultado. No hace falta explicarle nada más.

## 3. Desde la terminal

```bash
git clone https://github.com/flobertguzman/departamento-marketing-agentico.git
cd departamento-marketing-agentico
./codex/install.sh      # Codex
./install.sh            # Claude Code
```

## Después de instalar

- **Codex:** reinicia y escribe `$departamento-marketing`.
- **Claude Code:** reinicia y escribe `/departamento-marketing`.

Las instalaciones **por proyecto** (solo en la carpeta actual) usan `--project`.

## Desinstalar

```bash
rm -rf ~/.agents/skills/departamento-marketing ~/.codex/agents/mkt_*.toml      # Codex
rm -rf ~/.claude/skills/departamento-marketing ~/.claude/agents/mkt-*.md       # Claude Code
```
