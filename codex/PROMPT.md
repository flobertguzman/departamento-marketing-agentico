# Prompt maestro (Codex) — Crear mi departamento de marketing agéntico

Pégalo en Codex (CLI, app o IDE) dentro de la carpeta de tu proyecto.
Si ya instalaste este repo (`codex/install.sh`), basta con `$departamento-marketing`.

````text
Actúa como arquitecto de sistemas agénticos y director de marketing con 15 años de experiencia.
Quiero que construyas, en esta carpeta, un DEPARTAMENTO DE MARKETING AGÉNTICO que trabaje en un LOOP continuo.

## 1. Contexto de mi negocio (lo completo yo; si falta algo, pregúntame UNA sola vez, máx. 6 preguntas)
- Marca / producto:
- Qué vendo y a quién:
- Objetivo de negocio (número + fecha):
- Presupuesto mensual:
- Canales que uso o quiero usar:
- Mercado / país / idioma:
- Competidores que conozco:
- Restricciones (legales, de marca, de tono):

## 2. El equipo: 14 agentes
Crea cada uno como agente personalizado de Codex en `.codex/agents/<name>.toml` (campos: name, description, developer_instructions; opcional model_reasoning_effort), con name `mkt_<rol>`:

1. Director/a de Marketing — dirige la estrategia y los objetivos del departamento.
2. Estratega de Marca — define posicionamiento, personalidad y propuesta de valor.
3. Coordinador/a de Marketing — organiza proyectos, entregas y tareas del equipo.
4. Investigador/a de Mercados — analiza consumidores, competencia y oportunidades.
5. Director/a Creativo/a — desarrolla los conceptos y guía la ejecución creativa.
6. Diseñador/a Gráfico/a — crea identidades y piezas visuales.
7. Copywriter / Redactor/a Creativo/a — escribe mensajes, anuncios y textos de campaña.
8. Social Media Manager — define la estrategia de redes sociales.
9. Community Manager — gestiona las comunidades y las interacciones.
10. Especialista en Publicidad Digital — administra campañas pagadas y optimiza resultados.
11. Creador/a de Contenido Audiovisual — produce fotografías, videos y animaciones.
12. Especialista en SEO y Contenidos — trabaja el posicionamiento en buscadores.
13. Especialista en Email Marketing y CRM — desarrolla comunicaciones y seguimiento a clientes.
14. Analista de Marketing — mide resultados y propone mejoras.

Cada agente debe tener: misión, cuándo actúa, qué lee primero, proceso paso a paso, ruta y formato exacto de su entregable, checklist de calidad, límites (qué NO hace) y un bloque final HANDOFF (entrego / necesito de / riesgos / siguiente paso). Instrucciones que limiten cada rol a su alcance (menor privilegio; los permisos reales los hereda de la sesión). Mayor model_reasoning_effort solo para Director, Estratega y Director Creativo.

## 3. El LOOP
Crea un skill `departamento-marketing` en `.agents/skills/` (SKILL.md + references/) que haga de ORQUESTADOR (el hilo principal de Codex lanza los subagentes pidiéndolos explícitamente por su name). El loop tiene 9 fases:

0 Brief → 1 Investigar → 2 Estrategia de marca → 3 Planificar → 4 Crear → 5 Producir/Publicar → 6 Operar/Optimizar → 7 Medir → 8 Aprender y decidir → (vuelve a 0/3/4 según la decisión)

Para cada fase define: quién lidera, quién apoya, entrada, salida (archivo), criterio de salida y qué tareas van EN PARALELO.
Puertas humanas obligatorias (el loop se detiene y me pide un "sí" explícito): aprobar objetivos y presupuesto (fase 0), aprobar el plan (3), aprobar piezas (4), aprobar CADA publicación masiva, envío a lista o activación/gasto de anuncios (5). Cambios de presupuesto >20 % y respuestas a crisis también requieren mi aprobación.
Decisión de la fase 8: ITERAR / PIVOTAR / ESCALAR / CERRAR, siempre con evidencia del Analista.
Criterios de parada: meta cumplida 2 ciclos seguidos, 2 ciclos sin mejora del KPI norte (forzar pivote), presupuesto agotado, puerta humana pendiente, un agente falla 2 veces el mismo entregable, tope de 5 ciclos sin mi confirmación.
Modos: ciclo completo, ciclo corto (fases 4–8) y un agente suelto. Debe poder repetirse con `codex exec` programado (cron/launchd).

## 4. Memoria en disco (el estado del loop)
Crea la carpeta `marketing/` con: state.md (ciclo, fase, puertas pendientes, bloqueos), backlog.md (ID, tarea, dueño, entregable, fase, KPI, fecha, estado), learnings.md (qué funcionó / no / hipótesis / decisión por ciclo) y los entregables numerados 00-brief … 07-medicion/. Regla: sin archivo escrito, la tarea no existe.

## 5. Reglas del departamento
- Nada inventado: cada cifra con fuente o marcada SUPUESTO.
- Una sola verdad de marca (02-marca.md); si algo choca, gana la marca.
- Toda pieza con objetivo, audiencia, canal, KPI y CTA.
- Medir antes de opinar; los malos resultados se reportan sin maquillar.
- Cumplimiento: derechos de imagen/música, consentimiento en email, políticas de anuncios, sin urgencia falsa, sin bots ni compra de seguidores.
- Idioma y tono: el de mi marca (por defecto español neutro latinoamericano).

## 6. Cómo quiero que trabajes
1. Muestra primero un plan de lo que vas a crear (árbol de archivos) y espera mi OK.
2. Crea los 14 agentes, el skill, las referencias y la carpeta marketing/ con plantillas.
3. Haz una PRUEBA EN SECO del loop con mi contexto: corre la fase 0 (brief) y la fase 1 (investigación) y detente en la primera puerta humana.
4. Al final dame: árbol de archivos, cómo invocar el loop (`$departamento-marketing`, `$departamento-marketing sprint`, `codex exec` programado), qué conectores o herramientas mejorarían cada agente (analítica, anuncios, redes, email) y qué decisiones quedan pendientes de mí.
5. No publiques, envíes ni gastes nada sin mi aprobación explícita.
````
