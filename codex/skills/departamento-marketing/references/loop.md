# El LOOP del departamento — especificación

Un **ciclo** es una vuelta completa de 9 fases (0–8). Dura lo que dure la campaña o el sprint (normalmente 1–4 semanas). Cada ciclo deja un reporte y un aprendizaje que alimenta el siguiente.

## Contrato de cada fase

Cada fase tiene: **entrada → trabajo → salida → criterio de salida → siguiente paso**.

### Fase 0 — Brief
- **Entrada:** petición del usuario, `learnings.md` (si hay).
- **Trabajo:** `mkt_director` define objetivo SMART, KPI norte, audiencia, presupuesto, canales, plazo, restricciones. `mkt_coordinador` abre `state.md` y `backlog.md`.
- **Salida:** `00-brief.md`.
- **Salida OK si:** objetivo medible, presupuesto y plazo definidos, supuestos marcados.
- 🧑 **Puerta:** el humano aprueba objetivos y presupuesto.

### Fase 1 — Investigar
- **Trabajo:** `mkt_investigador` (consumidor, competencia, tendencias, oportunidades). En paralelo, `mkt_seo-contenidos` aporta demanda de búsqueda y `mkt_analista` aporta línea base de métricas históricas si existen.
- **Salida:** `01-investigacion.md` con hallazgos, evidencia y 3–5 oportunidades priorizadas.
- **Salida OK si:** cada hallazgo tiene fuente o `SUPUESTO`; hay un insight de consumidor accionable.

### Fase 2 — Estrategia de marca
- **Trabajo:** `mkt_estratega-marca` define posicionamiento, personalidad, propuesta de valor, pilares de mensaje, tono, qué NO somos.
- **Salida:** `02-marca.md`.
- **Salida OK si:** el posicionamiento cabe en una frase y es diferenciable frente a la competencia investigada.

### Fase 3 — Planificar
- **Trabajo:** `mkt_director` fija estrategia y reparto de presupuesto. En paralelo, `mkt_social-media-manager`, `mkt_publicidad-digital`, `mkt_seo-contenidos` y `mkt_email-crm` entregan su plan de canal. `mkt_coordinador` convierte todo en `backlog.md` con dueños y fechas.
- **Salida:** `03-plan.md`, `06-canales/*.md` (borrador), `backlog.md`.
- **Salida OK si:** cada tarea tiene dueño, entregable, fecha, KPI; el presupuesto suma 100 %.
- 🧑 **Puerta:** el humano aprueba el plan.

### Fase 4 — Crear
- **Trabajo:** `mkt_director-creativo` escribe el concepto y la guía de ejecución. Luego, **en paralelo**: `mkt_copywriter`, `mkt_disenador`, `mkt_audiovisual`. Director Creativo revisa y aprueba o devuelve (máx. 2 rondas).
- **Salida:** `04-concepto.md`, `05-copy/`, `05-diseno/`, `05-audiovisual/`.
- **Salida OK si:** todas las piezas del backlog con estado "crear" existen y pasan el checklist del Director Creativo.
- 🧑 **Puerta:** el humano aprueba piezas.

### Fase 5 — Producir y publicar
- **Trabajo:** `mkt_coordinador` verifica entregas completas. `mkt_social-media-manager` programa; `mkt_publicidad-digital` prepara campañas (en borrador, sin activar); `mkt_email-crm` arma envíos y segmentos; `mkt_seo-contenidos` publica/optimiza contenido.
- **Salida:** calendario de publicación, campañas listas, envíos listos.
- 🧑 **Puerta:** el humano aprueba **cada** publicación masiva, envío a lista y activación/gasto.

### Fase 6 — Operar y optimizar
- **Trabajo:** `mkt_community-manager` gestiona interacciones, escala crisis y resume insights de la comunidad. `mkt_publicidad-digital` optimiza (pausar perdedores, escalar ganadores dentro del presupuesto aprobado). `mkt_social-media-manager` ajusta calendario.
- **Salida:** bitácora en `06-canales/comunidad.md` y `ads.md`.
- **Regla:** cambios de presupuesto > 20 % o respuestas a crisis requieren aprobación humana.

### Fase 7 — Medir
- **Trabajo:** `mkt_analista` consolida resultados vs KPI, atribución razonable, hallazgos y 3–5 recomendaciones priorizadas por impacto/esfuerzo.
- **Salida:** `07-medicion/ciclo-N.md`.
- **Salida OK si:** cada KPI del brief tiene valor real (o "sin dato" explicado); se distingue correlación de causalidad.

### Fase 8 — Aprender y decidir
- **Trabajo:** `mkt_director` lee el reporte, escribe en `learnings.md` (qué funcionó, qué no, por qué, qué probar) y decide:
  - **ITERAR** → mismo plan con ajustes, vuelve a Fase 3 o 4.
  - **PIVOTAR** → cambia estrategia, vuelve a Fase 1 o 2.
  - **ESCALAR** → más presupuesto/canales al ganador.
  - **CERRAR** → fin de campaña, resumen final.
- `mkt_coordinador` archiva el ciclo y abre `ciclo: N+1` en `state.md`.

## Criterios de parada del loop

El orquestador **detiene** el loop y reporta si ocurre cualquiera:
1. Se cumplió el objetivo del brief (2 ciclos seguidos ≥ meta) → proponer CERRAR/ESCALAR.
2. Dos ciclos seguidos sin mejora en el KPI norte → forzar PIVOTAR y revisar el brief.
3. Presupuesto agotado.
4. Una puerta humana lleva pendiente y no hay respuesta → no avanzar, recordar.
5. Un agente falla dos veces el mismo entregable → escalar al Director y al usuario.
6. Tope duro: **máximo 5 ciclos** sin confirmación explícita del usuario para seguir.

## Paralelismo recomendado

| Momento | En paralelo |
|---|---|
| Fase 1 | investigador · seo-contenidos · analista (línea base) |
| Fase 3 | social-media-manager · publicidad-digital · seo-contenidos · email-crm |
| Fase 4 (tras el concepto) | copywriter · disenador · audiovisual |
| Fase 5 | social · ads · email · seo |

Todo lo que dependa de un entregable previo es **secuencial**.

## Formato de HANDOFF (obligatorio al final de cada entregable)

```
HANDOFF
- Entrego: <archivo(s) y qué contienen en 1 línea>
- Necesito de: <agente> → <qué exactamente>
- Riesgos / supuestos: <lista corta>
- Siguiente paso sugerido: <fase/agente>
```

## Ejecución recurrente

- **Semanal (ciclo corto):** `codex exec '$departamento-marketing sprint'` programado cada 7 días → Fases 4–8 con el plan vigente.
- **Mensual (ciclo completo):** `codex exec '$departamento-marketing'` programado cada 30 días → Fases 0–8; la Fase 0 reutiliza `learnings.md`.
- Las puertas 🧑 siempre pausan el loop; nunca se auto-aprueban.
