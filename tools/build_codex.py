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


def build_agents():
    (OUT / "agents").mkdir(parents=True, exist_ok=True)
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
        (OUT / "agents" / f"{cname}.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_skill():
    src = ROOT / "skills" / "departamento-marketing"
    dst = OUT / "skills" / "departamento-marketing"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

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
    OUT.mkdir(exist_ok=True)
    build_agents()
    build_skill()
    build_prompt()
    print("Versión Codex generada en", OUT)
