# Departamento de Marketing Agéntico

Un skill de Claude Code que monta un **departamento de marketing de 14 agentes** y lo hace trabajar en un **loop** de mejora continua: brief → investigación → estrategia → creación → publicación → medición → aprendizaje.

## El equipo

| Agente | Rol |
|---|---|
| `mkt-director` | Director/a de Marketing — estrategia y objetivos |
| `mkt-estratega-marca` | Estratega de Marca — posicionamiento, personalidad, propuesta de valor |
| `mkt-coordinador` | Coordinador/a — proyectos, entregas y tareas |
| `mkt-investigador` | Investigador/a de Mercados — consumidores, competencia, oportunidades |
| `mkt-director-creativo` | Director/a Creativo/a — concepto y ejecución creativa |
| `mkt-disenador` | Diseñador/a Gráfico/a — identidades y piezas visuales |
| `mkt-copywriter` | Copywriter — mensajes, anuncios, textos |
| `mkt-social-media-manager` | Social Media Manager — estrategia de redes |
| `mkt-community-manager` | Community Manager — comunidades e interacciones |
| `mkt-publicidad-digital` | Publicidad Digital — campañas pagadas y optimización |
| `mkt-audiovisual` | Contenido Audiovisual — foto, video, animación |
| `mkt-seo-contenidos` | SEO y Contenidos — posicionamiento en buscadores |
| `mkt-email-crm` | Email Marketing y CRM — comunicaciones y seguimiento |
| `mkt-analista` | Analista de Marketing — medición y mejoras |

## El loop

```
 ┌─► 0 Brief ─► 1 Investigar ─► 2 Estrategia ─► 3 Planificar ─► 4 Crear ─►
 │                                                                       │
 └─ 8 Aprender ◄─ 7 Medir ◄─ 6 Operar/Optimizar ◄─ 5 Producir/Publicar ◄─┘
```

- **Orquestador:** la sesión principal (el skill) despacha a los agentes; en paralelo cuando las tareas son independientes.
- **Memoria en disco:** `marketing/state.md`, `backlog.md`, `learnings.md` y entregables numerados.
- **Puertas humanas:** objetivos/presupuesto, plan, piezas y **toda** publicación, envío o gasto requieren tu "sí".
- **Paradas:** meta cumplida, 2 ciclos sin mejora, presupuesto agotado, tope de 5 ciclos.

Detalle: [`skills/departamento-marketing/references/loop.md`](skills/departamento-marketing/references/loop.md).

## Instalación

```bash
git clone <este-repo> && cd departamento-marketing-agentico
./install.sh              # a nivel usuario (~/.claude)
# o, dentro de tu proyecto:
/ruta/al/repo/install.sh --project
```

Reinicia Claude Code.

## Uso

```text
/departamento-marketing          # ciclo completo (fases 0–8)
/departamento-marketing sprint   # ciclo corto (fases 4–8)
/departamento-marketing copy …   # un solo agente
/loop 7d /departamento-marketing sprint   # recurrente
```

## ¿Prefieres crearlo desde cero con un prompt?

[`PROMPT.md`](PROMPT.md) contiene el prompt maestro para que Claude construya el departamento en cualquier proyecto.

## Estructura

```
agents/                       # 14 subagentes
skills/departamento-marketing/
  SKILL.md                    # orquestador
  references/loop.md          # especificación del loop
  references/templates.md     # plantillas de estado
PROMPT.md                     # prompt maestro
install.sh
```
