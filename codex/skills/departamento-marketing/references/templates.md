# Plantillas de archivos de estado

Crea estas al iniciar el departamento si no existen.

## marketing/state.md

```markdown
# Estado del departamento
- Proyecto / marca:
- Ciclo: 1
- Fase actual: 0 — Brief
- Última actualización: AAAA-MM-DD
- Puertas pendientes de aprobación humana:
  - [ ] (ninguna)
- Bloqueos:
  - (ninguno)
- Próxima acción:
```

## marketing/backlog.md

```markdown
# Backlog
| ID | Tarea | Dueño (agente) | Entregable | Fase | KPI | Fecha | Estado |
|----|-------|----------------|------------|------|-----|-------|--------|
| T-001 | Redactar brief | mkt_director | 00-brief.md | 0 | — | | por hacer |
```
Estados: `por hacer · en curso · en revisión · aprobado · publicado · bloqueado · cancelado`

## marketing/learnings.md

```markdown
# Aprendizajes
## Ciclo N — AAAA-MM-DD
- Funcionó: … (evidencia: …)
- No funcionó: … (evidencia: …)
- Hipótesis para probar: …
- Decisión: ITERAR | PIVOTAR | ESCALAR | CERRAR
```

## marketing/00-brief.md

```markdown
# Brief
- Marca / producto:
- Objetivo SMART:
- KPI norte (y 2–3 secundarios): línea base → meta
- Audiencia principal:
- Presupuesto (total y por canal):
- Canales habilitados:
- Plazo / hitos:
- Restricciones (legales, de marca, de tono):
- Supuestos (marcados SUPUESTO):
- Qué NO se hará:
```

## Reporte de medición (marketing/07-medicion/ciclo-N.md)

```markdown
# Ciclo N — Reporte
## Resumen en 3 líneas
## KPI vs meta
| KPI | Línea base | Meta | Real | Δ | Lectura |
## Por canal
## Qué funcionó / qué no (con evidencia)
## Recomendaciones (impacto / esfuerzo)
## Limitaciones de los datos
HANDOFF …
```
