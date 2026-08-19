> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/08-delivery/vertical-slices.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Vertical slices

**Estado:** Review  
**Versión:** 0.1

## VS-01 — Primera actividad publicada

Un adulto crea familia y dos Learners, abre una actividad publicada, revisa materiales y ve la guía.

Demuestra: identidad mínima, catálogo versionado y UI base.

## VS-02 — Roles y objetivos

La familia selecciona tres participantes; el sistema asigna roles significativos y un objetivo principal compatible a cada uno; el adulto puede intercambiarlos.

Demuestra: Family Model, Activity Schema y motor de asignación.

## VS-03 — Sesión y cierre

El adulto completa pasos, registra cambios reales y responde una valoración por niño en menos de 20 segundos.

Demuestra: sesión, exposiciones, evidencia y UX de atención dividida.

## VS-04 — Learning Journey explicable

El adulto ve observaciones e inferencias prudentes, abre “¿Por qué?” y corrige una atribución por problema de herramienta.

Demuestra: Learner Model, procedencia y corrección.

## VS-05 — Recomendación semanal

El sistema crea un plan balanceado desde biblioteca, participantes, tiempo e inventario; el adulto sustituye una actividad.

Demuestra: recomendación y planificación.

## VS-06 — Troubleshoot

Durante un paso, el adulto describe una falla; el AI Companion usa la versión y paso para proponer verificaciones seguras.

Demuestra: orquestación IA y fallback sin generación libre.

## VS-07 — Voz opcional

El adulto dicta una observación para varios niños; el sistema estructura hechos y solicita confirmación solo donde hay ambigüedad.

Demuestra: procesamiento temporal, atribución y retención.

## VS-08 — Operación editorial

Un autor crea una versión, recibe revisiones, ejecuta piloto, publica y luego retira.

Demuestra: workflow, permisos y catálogo.

## VS-09 — Paquete semanal offline

El adulto descarga el plan, pierde conexión, completa una actividad y sincroniza valoraciones después sin duplicarlas.

Demuestra: cache versionado, cifrado local, idempotencia y UX de estado.

## VS-10 — Generación y QA visual

El sistema genera candidatos para un paso, detecta inconsistencias, recibe aprobación humana y publica el asset con la ActivityVersion.

Demuestra: pipeline multimodal, trazabilidad y gate editorial.

## VS-11 — Portafolio privado

Un adulto guarda un medio del proyecto, lo ve en familia y lo elimina sin afectar observaciones educativas.

Demuestra: consentimiento, aislamiento y retención de medios.

## VS-12 — Comunidad moderada

Un adulto envía una imagen del portafolio, revisa privacidad, pasa moderación y la publica bajo una actividad; otro adulto la reporta y el equipo la retira.

Demuestra: UGC, moderación y separación de marketing.

## Definition of done por slice

- Requisitos enlazados.
- Criterios de aceptación automatizados y/o de usabilidad.
- Estados de error y permisos.
- Telemetría minimizada.
- Documentación actualizada.
- Revisión de seguridad/privacidad cuando aplique.
