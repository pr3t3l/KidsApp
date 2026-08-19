> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/08-delivery/pilot-pack-v0.1.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Pilot Pack v0.1 — guía de ejecución

**Estado:** Draft — listo para revisión humana, no para publicación familiar<br>
**Versión:** 0.1<br>
**Fecha de corte:** 15 de agosto de 2026

## Propósito

Este documento es el punto de entrada operativo para convertir los specs en el primer producto comprobable. Un agente de desarrollo debe poder usarlo para entender qué construir, en qué orden, qué contratos respetar y qué todavía requiere evidencia humana.

El paquete no declara seguras ni publicadas las actividades. Entrega tres `ActivityVersion` completas en estado `Draft`, contratos de datos ejecutables y gates explícitos para llegar a piloto.

## Lectura obligatoria antes de implementar

1. [Instrucciones para agentes](../../AGENTS.es.md).
2. [Visión del producto](../00-foundation/product-vision.md), [principios](../00-foundation/product-principles.md) y [glosario](../00-foundation/glossary.md).
3. [Baseline de privacidad infantil](../00-foundation/compliance-baseline.md).
4. [Learning Framework](../01-learning/learning-framework.md), [Learner Model](../01-learning/learner-model.md) y [Evidence Model](../01-learning/evidence-model.md).
5. [Activity Schema](../02-content/activity-schema.md), [seguridad](../02-content/safety-guidelines.md) y [ciclo editorial](../02-content/activity-lifecycle.md).
6. [Arquitectura](../07-engineering/architecture.md), [contratos API](../07-engineering/api-contracts.md) y [modelo offline](../07-engineering/mobile-offline-strategy.md).
7. [Vertical slices](vertical-slices.md), [trazabilidad](traceability.md) y este documento.

Ante una contradicción se aplica la precedencia de `AGENTS.md`; seguridad y privacidad dominan.

## Contenido del paquete

| ID y versión | Actividad | Duración | Niños | Nivel preliminar | Estado y gate distintivo |
|---|---|---:|---:|---|---|
| `ACT-0001@0.3.0` | [Puente de papel](../02-content/sample-activities/ACT-0001-puente-de-papel.md) | 30–60 min | 1–3 | A | Validar físicamente vaso/carga, estabilidad de soportes, historia causal, una prueba propia por niño, guía adulta de estructuras y reproducibilidad. |
| `ACT-0002@0.1.1` | [Clasificación con semillas](../02-content/sample-activities/ACT-0002-clasificacion-semillas.md) | 30–60 min | 1–3 | B | Revisar alergias, toxinas naturales, piezas pequeñas, ingestión, etiquetado y almacenamiento. |
| `ACT-0003@0.1.2` | [Probador de conductividad](../02-content/sample-activities/ACT-0003-probador-conductividad.md) | 35–60 min | 1–3 | C | Revisión eléctrica/mecánica reforzada, selección de una configuración, componentes exactos y gate para co-montaje infantil desenergizado. |

Las tres actividades incluyen bundles `es-US` y `en-US`, roles para uno, dos y tres niños, diferenciación funcional, un objetivo principal por niño, exposiciones secundarias, cierre 1–5, troubleshooting y briefs visuales. Ninguna puede aparecer en el catálogo familiar mientras su versión no tenga estado `published`.

## Contratos ejecutables

La [guía de schemas](../../schemas/README.es.md) describe cinco JSON Schemas 2020-12:

- `ActivityVersion`: contenido bilingüe, materiales, roles, pasos, seguridad, adaptaciones, evaluación, visuales y gates.
- `ActivitySession`: referencia exacta de versión, asignaciones, progreso, adaptaciones, cierre y sincronización offline.
- `LearnerRecords`: exposiciones, observaciones e inferencias como registros separados y trazables.
- `OfflinePackManifest`: versión/hash del paquete, contenido, assignments mínimos, assets y vencimiento.
- `SyncEvent`: evento de cliente idempotente, revisión base, payload, estado de sync y conflicto.

Los ejemplos son datos ficticios y no equivalen a aprobación editorial. Para verificar contratos y documentación:

```bash
npm install
npm run validate
```

La validación debe ejecutarse en CI. Incluye seis ejemplos positivos, referencias cruzadas y once mutaciones negativas de reglas centrales. Un cambio que rompa schemas, invariantes, ejemplos, enlaces locales o señales obligatorias de una actividad piloto no puede integrarse.

## Orden de construcción

### Paquete inmediato de calibración con Sofía

Para la primera semana controlada, usar el [dry run de cinco días](sofia-five-day-dry-run-v0.1.md), su [lista consolidada de compras](sofia-shopping-list-v0.1.md) y la [hoja breve de observación](founder-dry-run-observation-sheet-v0.1.md). Los días 3–5 son candidatos editoriales, no `ActivityVersion` publicadas. `ACT-0003` permanece fuera de la ejecución infantil hasta completar su gate eléctrico y mecánico.

### Etapa 1 — calibrar el contenido sin software de familia

1. Hacer un dry run de cada actividad dirigido por un adulto y sin participación infantil, comenzando por `ACT-0001` y `ACT-0002`.
2. Registrar tiempos, confusiones, sustituciones solicitadas, incidentes y casi-incidentes del dry run.
3. Corregir la `ActivityVersion`; cualquier cambio en pasos, materiales, roles u objetivos crea una nueva versión según el ciclo editorial.
4. Completar revisión pedagógica y revisión de seguridad; `ACT-0003` requiere además gates eléctrico y mecánico, componentes exactos, prueba física adulta y decisión explícita sobre qué conexiones puede realizar un niño con el circuito desenergizado.
5. Producir y revisar visuales después de estabilizar pasos y materiales; cada asset queda ligado a una versión exacta.
6. Cambiar a `ready_for_pilot` únicamente cuando los gates previos estén registrados.
7. Solo entonces ejecutar pruebas controladas con niños y cubrir configuraciones de uno, dos y tres participantes; registrar cada ejecución como pilot record.
8. Tras comenzar esas pruebas, usar `family_pilot`; una revisión posterior puede devolver la versión al estado apropiado.

Salida: cada actividad alcanza como máximo el estado sustentado por sus records; si no supera un gate, permanece en `draft` o en el estado de revisión correspondiente con causa documentada. `retired` se reserva para una versión retirada, no como sinónimo de una revisión rechazada.

### Etapa 2 — prototipo UX de baja fidelidad

Construir y probar, sin depender aún del stack final:

1. selección de participantes y tiempo disponible;
2. asignación de rol y objetivo principal por niño;
3. materiales, preparación adulta y advertencias;
4. ejecución paso a paso y recuperación de fallas;
5. cierre con una valoración por niño, `Evaluar más` opcional y una nota de voz/texto opcional;
6. explicación de observaciones e inferencias con corrección y borrado.

El criterio central es que un adulto con tres niños pueda cerrar en menos de 20 segundos sin perder contexto ni responder nueve preguntas por defecto.

### Etapa 3 — primer vertical slice funcional

Puede iniciarse la infraestructura y el prototipo de `VS-01` a `VS-03` con fixtures identificadas como `editorial_preview` o `pilot`. Implementarlos en este orden:

1. familia, adultos y Learners mínimos;
2. catálogo que solo expone versiones publicadas;
3. sesión con referencia inmutable a `ActivityVersion`;
4. asignación compatible de roles y exactamente un objetivo principal por Learner;
5. registro automático de exposición por participación real;
6. cierre y observación contextual;
7. cola offline idempotente para eventos de sesión.

La IA no es necesaria para probar este recorrido. Usar reglas deterministas y contenido aprobado primero evita que un modelo oculte defectos del dominio. `VS-01` no está terminado hasta que un adulto pueda abrir al menos una ActivityVersion realmente `published`; una fixture o actividad `Draft` solo permite avanzar el prototipo.

### Etapa 4 — Learner Model y recomendación

Después de validar que la señal del cierre es útil:

1. implementar `VS-04` con inferencias conservadoras y evidencia visible;
2. permitir corrección y eliminación adulta;
3. implementar planificación por tiempo y balance de áreas;
4. añadir selección de modelo agnóstica a proveedor solo detrás de contratos y evaluaciones;
5. habilitar primero `Explain` y `Troubleshoot` con recuperación limitada a la versión publicada.

### Etapa 5 — operación editorial

Implementar `VS-08` antes de escalar la biblioteca: autoría, revisiones independientes, gates por categoría, piloto, publicación, retiro y auditoría. La fundadora puede acumular roles al inicio, pero el sistema conserva roles separados para el equipo futuro.

## Reglas de implementación no negociables

- Cada asignación tiene exactamente un `primaryObjectiveSkillId`; otras habilidades son exposiciones.
- Participación no prueba desempeño y exposición no crea automáticamente una inferencia.
- Una valoración 1–5 mide independencia contextual, no inteligencia ni identidad del niño.
- Las inferencias muestran confianza, evidencia y explicación, y son corregibles.
- La IA selecciona o adapta dentro de opciones aprobadas; no inventa el núcleo ni sustituye materiales libremente.
- Los pasos adultos, advertencias y límites de seguridad no pueden degradarse por adaptación o traducción.
- La app está dirigida al adulto en v1; el niño participa en la actividad física, no administra cuenta, consentimiento ni evaluación.
- Medios, audio y transcripciones son opcionales y temporales salvo que el adulto elija guardar un proyecto en el portafolio.
- La comunidad futura permanece separada del Learner Model y visible solo a adultos autenticados en su primera versión.

## Gates para estas tres actividades

### Gate común

- esquema completo y dos idiomas revisados;
- ejecución del autor o propietaria editorial;
- revisión pedagógica y de seguridad registrada;
- pasos, materiales y troubleshooting reproducibles por otro adulto;
- prueba explícita con 1, 2 y 3 niños;
- visuales coherentes con materiales, cantidades, actores y riesgos;
- tres ejecuciones satisfactorias adicionales en al menos dos familias para nivel A/B;
- cambios posteriores vuelven a los gates afectados.

### Gate reforzado de `ACT-0003`

- especialista apropiado aprueba fuente, resistencia, LED, conexiones, aislamiento y modos de falla;
- especialista apropiado define y aprueba —o rechaza con causa— una ruta de co-montaje infantil desenergizado, con acciones permitidas por edad;
- números de parte exactos y ficha técnica archivada;
- prueba de control abierto/cerrado, polaridad, falso negativo y cortocircuito evitado;
- verificación de ausencia de calor, olor, fuga, chispa o acceso infantil a pilas;
- el adulto inserta, retira, cuenta y guarda las pilas;
- exclusión comprobable de 9 V, USB, pilas tipo moneda, red doméstica, líquidos, personas, animales y dispositivos;
- mínimo de ejecuciones reforzadas definido y aprobado antes de `family_pilot`.

## Evidencia mínima del piloto

Por sesión se conserva solo:

- actividad y versión exacta;
- número de participantes, rol y objetivo principal;
- duración aproximada y estado de finalización;
- exposiciones realmente ocurridas;
- una valoración principal opcional por niño;
- nota opcional corregible;
- adaptación aplicada;
- falla, abandono, incidente o casi-incidente.

No se requiere foto, video, audio persistente ni informe largo. El plan completo de ocho semanas está en [Plan de piloto familiar](pilot-plan.md).

## Definición de listo para comenzar implementación

El repositorio está listo para iniciar prototipos y `VS-01` cuando:

- `npm run validate` termina sin errores;
- las decisiones abiertas que afecten el slice están resueltas o explícitamente excluidas;
- el equipo elige solo el mínimo stack necesario para ese slice;
- existen criterios de aceptación y pruebas para autorización, seguridad, evidencia y offline;
- ningún contenido `Draft` se presenta como recomendación publicada.

Esto no equivale a estar listo para una familia. Una actividad necesita completar sus gates, y el producto necesita revisión de privacidad, seguridad, accesibilidad y cumplimiento para Estados Unidos antes de distribución.

## Entrega esperada de cada tarea a otro Codex

Cada tarea debe declarar antes de editar:

1. vertical slice y recorrido adulto que completa;
2. requisitos y decisiones respetados;
3. schemas, entidades y endpoints afectados;
4. estados de error, permisos y comportamiento offline;
5. pruebas de aceptación y regresión;
6. riesgos de seguridad y privacidad;
7. qué queda fuera de alcance.

Al terminar debe actualizar implementación, pruebas, documentación, trazabilidad y decision log si tomó una decisión nueva. No debe rellenar una ambigüedad de seguridad, privacidad o producto con una suposición silenciosa.
