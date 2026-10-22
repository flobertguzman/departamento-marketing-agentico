#!/usr/bin/env python3
"""Genera la versión Codex (codex/) a partir de la versión Claude Code (agents/ + skills/).

La versión Claude Code es la fuente de verdad. Ejecuta:  python3 tools/build_codex.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "codex"
HIGH_EFFORT = {"mkt-director", "mkt-estratega-marca", "mkt-director-creativo"}


def sub(text, old, new, where):
    if old not in text:
        sys.exit(f"[build_codex] no encontré el texto a reemplazar en {where}: {old[:70]!r}")
    return text.replace(old, new)


def parse_agent(path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    if not m:
        sys.exit(f"[build_codex] sin frontmatter: {path}")
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    return meta, m.group(2).strip()


def build_agents(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted((ROOT / "agents").glob("mkt-*.md")):
        meta, body = parse_agent(src)
        name = meta["name"]
        cname = name.replace("-", "_")
        body = body.replace("mkt-", "mkt_")
        if "'''" in body:
            sys.exit(f"[build_codex] ''' en {src}")
        lines = [
            f"name = {json.dumps(cname)}",
            f"description = {json.dumps(meta['description'], ensure_ascii=False)}",
        ]
        if name in HIGH_EFFORT:
            lines.append('model_reasoning_effort = "high"')
        lines.append("developer_instructions = '''")
        lines.append(body)
        lines.append("'''")
        (out_dir / f"{cname}.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


INSTALL_AGENTS_SH = """#!/usr/bin/env sh
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
"""

OPENAI_YAML = """interface:
  display_name: "Departamento de Marketing"
  short_description: "14 agentes de marketing que trabajan en un loop: brief, investigación, estrategia, creación, publicación, medición y aprendizaje."
  default_prompt: "Corre un ciclo del departamento de marketing para mi marca."
"""

CODEX_AGENTS_MD = """# Instrucciones para Codex

Esta carpeta contiene el **Departamento de Marketing Agéntico** para Codex: un skill (`skills/departamento-marketing`) y 14 agentes personalizados (`skills/departamento-marketing/custom-agents/*.toml`).

## Si el usuario pide instalarlo («instala esto», «instálalo», «install this»)

1. Ejecuta, desde esta carpeta, `./install.sh` (o `sh install.sh`). Para instalarlo solo en el proyecto actual: `./install.sh --project`.
2. Verifica que existan `~/.agents/skills/departamento-marketing/SKILL.md` y los 14 archivos `~/.codex/agents/mkt_*.toml`.
3. Responde al usuario con lo instalado y dile que use `$departamento-marketing`. Si Codex no muestra el skill o los agentes, que reinicie Codex.
4. No modifiques ningún otro archivo, ni la configuración de Codex, ni ejecutes nada más.

## Si el usuario pide usarlo
Invoca el skill `departamento-marketing` y sigue su `SKILL.md`.
"""


def build_codex_extras(dst):
    (dst / "scripts").mkdir(exist_ok=True)
    sh = dst / "scripts" / "install-agents.sh"
    sh.write_text(INSTALL_AGENTS_SH, encoding="utf-8")
    sh.chmod(0o755)
    (dst / "agents").mkdir(exist_ok=True)
    (dst / "agents" / "openai.yaml").write_text(OPENAI_YAML, encoding="utf-8")
    (OUT / "AGENTS.md").write_text(CODEX_AGENTS_MD, encoding="utf-8")


def build_skill():
    src = ROOT / "skills" / "departamento-marketing"
    dst = OUT / "skills" / "departamento-marketing"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    build_agents(dst / "custom-agents")
    build_codex_extras(dst)

    p = dst / "SKILL.md"
    t = p.read_text(encoding="utf-8")
    w = "SKILL.md"
    t = sub(t, '"corre el loop de marketing", "/marketing".', '"corre el loop de marketing", "$departamento-marketing".', w)
    t = sub(
        t,
        "> Los subagentes de Claude Code no pueden lanzar otros subagentes. Por eso el orquestador eres **tú (la sesión principal)** y los 14 perfiles viven en `agents/` (se instalan en `~/.claude/agents/` o `.claude/agents/`). Si los agentes no están instalados, ejecuta `install.sh` del repo o adopta cada rol leyendo su archivo en `agents/`.",
        "> El orquestador eres **tú (el hilo principal de Codex)**. Los 14 perfiles son agentes personalizados (`~/.codex/agents/*.toml`, o `.codex/agents/` en el proyecto) y los lanzas **pidiendo explícitamente subagentes**: Codex no delega por su cuenta salvo que se lo pidas. Si no están instalados, ejecuta `codex/install.sh` del repo o adopta cada rol leyendo su archivo `.toml`.",
        w,
    )
    t = sub(
        t,
        "## El equipo\n",
        "## Paso 0 — Verifica la instalación (hazlo siempre antes de un ciclo)\n\n"
        "Comprueba que existe `~/.codex/agents/mkt_director.toml` (o `.codex/agents/` en el proyecto). Si faltan los agentes, "
        "instálalos tú mismo ejecutando `sh <carpeta de este skill>/scripts/install-agents.sh` "
        "(o con `--project` si el usuario lo quiere solo en este proyecto), avisa en una línea de lo que instalaste y, si Codex "
        "no los lista, pide reiniciar. Mientras tanto puedes adoptar cada rol leyendo `custom-agents/<name>.toml`.\n\n"
        "## El equipo\n",
        w,
    )
    t = sub(t, "| # | Agente (`subagent_type`) |", "| # | Agente personalizado (`name`) |", w)
    t = sub(
        t,
        "con la herramienta `Agent` (`subagent_type` de la tabla)",
        "lanzándolos como subagentes por su `name` de la tabla (pídelo explícito: «lanza `mkt_investigador` y `mkt_seo_contenidos` en paralelo, espera a ambos y devuélveme un resumen de cada uno»)",
        w,
    )
    t = sub(t, "van **en paralelo** en un solo mensaje", "van **en paralelo** en una sola petición de lanzamiento", w)
    t = sub(t, "(`/marketing`)", "(`$departamento-marketing`)", w)
    t = sub(t, "(`/marketing sprint`)", "(`$departamento-marketing sprint`)", w)
    t = sub(t, "(`/marketing copy …`)", "(`$departamento-marketing copy …`)", w)
    t = sub(
        t,
        "combina con `/loop 7d /marketing sprint` (o una tarea programada) para que el ciclo corto se repita sin intervención hasta la próxima puerta.",
        "programa `codex exec '$departamento-marketing sprint'` con cron o launchd para repetir el ciclo corto; el loop se detiene solo en cada puerta humana.",
        w,
    )
    t = t.replace("mkt-", "mkt_")
    p.write_text(t, encoding="utf-8")

    p = dst / "references" / "templates.md"
    p.write_text(p.read_text(encoding="utf-8").replace("mkt-", "mkt_"), encoding="utf-8")

    p = dst / "references" / "loop.md"
    t = p.read_text(encoding="utf-8")
    w = "loop.md"
    t = sub(t, "`/loop 7d /marketing sprint` → Fases 4–8 con el plan vigente.", "`codex exec '$departamento-marketing sprint'` programado cada 7 días → Fases 4–8 con el plan vigente.", w)
    t = sub(t, "`/loop 30d /marketing` → Fases 0–8;", "`codex exec '$departamento-marketing'` programado cada 30 días → Fases 0–8;", w)
    t = t.replace("mkt-", "mkt_")
    p.write_text(t, encoding="utf-8")


def build_prompt():
    t = (ROOT / "PROMPT.md").read_text(encoding="utf-8")
    m = re.search(r"````text\n(.*?)\n````", t, re.S)
    body = m.group(1)
    w = "PROMPT.md"
    body = sub(
        body,
        "Crea cada uno como subagente de Claude Code en `.claude/agents/` (frontmatter: name, description, tools, model), con nombre `mkt-<rol>`:",
        "Crea cada uno como agente personalizado de Codex en `.codex/agents/<name>.toml` (campos: name, description, developer_instructions; opcional model_reasoning_effort), con name `mkt_<rol>`:",
        w,
    )
    body = sub(
        body,
        "Herramientas mínimas necesarias por rol (principio de menor privilegio). Modelo más potente solo para Director, Estratega y Director Creativo.",
        "Instrucciones que limiten cada rol a su alcance (menor privilegio; los permisos reales los hereda de la sesión). Mayor model_reasoning_effort solo para Director, Estratega y Director Creativo.",
        w,
    )
    body = sub(
        body,
        "(la sesión principal despacha a los agentes; los subagentes no pueden lanzar subagentes)",
        "(el hilo principal de Codex lanza los subagentes pidiéndolos explícitamente por su name)",
        w,
    )
    body = sub(body, "Debe poder repetirse con `/loop 7d /marketing sprint`.", "Debe poder repetirse con `codex exec` programado (cron/launchd).", w)
    body = sub(
        body,
        "(`/marketing`, `/marketing sprint`, `/loop 7d /marketing sprint`)",
        "(`$departamento-marketing`, `$departamento-marketing sprint`, `codex exec` programado)",
        w,
    )
    body = body.replace("Crea un skill `departamento-marketing` (SKILL.md + references/)", "Crea un skill `departamento-marketing` en `.agents/skills/` (SKILL.md + references/)")
    out = (
        "# Prompt maestro (Codex) — Crear mi departamento de marketing agéntico\n\n"
        "Pégalo en Codex (CLI, app o IDE) dentro de la carpeta de tu proyecto.\n"
        "Si ya instalaste este repo (`codex/install.sh`), basta con `$departamento-marketing`.\n\n"
        "````text\n" + body + "\n````\n"
    )
    (OUT / "PROMPT.md").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT / "agents", ignore_errors=True)
    OUT.mkdir(exist_ok=True)
    build_skill()
    build_prompt()
    print("Versión Codex generada en", OUT)
