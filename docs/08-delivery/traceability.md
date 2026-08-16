# Trazabilidad

**Estado:** Active  
**Versión:** 0.2

## Cadena

```text
Principio
→ requisito de dominio
→ journey/flujo
→ entidad o regla
→ vertical slice
→ implementación
→ prueba/evaluación
```

## Matriz inicial

| Resultado | Principios/requisitos | Flujos | Datos | Slice | Verificación |
|---|---|---|---|---|---|
| Una evaluación por niño | P-06, LRN-102, EVD-002 | Session Close | Assignment, Observation | VS-03 | Tiempo y restricción de dominio |
| Exposición no es desempeño | P-07, LRN-103, EVD-001 | Session, Journey | Exposure separado | VS-03/04 | Pruebas de inferencia |
| Roles diferenciados | P-05, ACT-004, REC-105 | Activity Session | RoleTemplate, Assignment | VS-02 | Casos 1–4 niños |
| Roles flexibles y no coercitivos | DEC-036, PRD-107, US-ACT-006 | Participants and Roles | Assignment, RoleChanged, ParticipationChanged | VS-02/03 | Pruebas de aceptación, intercambio, combinación y no participación |
| Biblioteca publicada | P-03, ACT-002, REC-101 | Plan, Session | ActivityVersion.status | VS-01/08 | Filtro y retiro |
| Inferencias explicables | P-08, LRN-104, EVD-008 | Learning Journey | EvidenceLink, Inference | VS-04 | “¿Por qué?” y corrección |
| Medios temporales | P-09, PRV-101/102 | Troubleshoot, Voice | MediaAsset.expiry | VS-06/07 | Job de expiración |
| Adaptación segura | P-10, AI-102, SAFE-004 | Adapt | AdaptationOption | VS-06 | Evals adversariales |
| Planificación por tiempo | DEC-017, REC-000, REC-109 | Weekly Plan | WeeklyPlan, time budget | VS-05 | Casos 30/60 minutos |
| Sesión offline | DEC-019, OFF-001 | Activity Session | OfflinePack, event queue | VS-09 | Pérdida de red/sync |
| Imágenes verificadas | DEC-021, ACT-VIS-002 | Editorial Workspace | VisualAsset, QA result | VS-10 | QA + aprobación humana |
| Comunidad separada | DEC-022, COM-001/006 | Portfolio/Community | PortfolioAsset, Submission, License | VS-11/12 | Permisos y retirada |
| Gates editoriales | DEC-023, OPS-001/003 | Editorial Workspace | Review, Role, ActivityVersion | VS-08 | Workflow y auditoría |
| Tres actividades piloto reproducibles | ACT-001/012, SAFE-001/008 | Pilot Pack | ActivityVersion, VisualBrief, ReviewRecord | Etapa editorial previa a VS-01 | `npm run validate`, revisión cruzada y ejecución familiar |
| Contratos ejecutables de contenido y sesión | DATA-001/002, ENG-001/004, OFF-003 | Catalog, Session, Learning Journey | JSON Schemas + invariantes de dominio | VS-01–04/09 | Ejemplos positivos, fixtures negativas y referencias cruzadas |
| Semillas como manipulativos no comestibles | SAFE-001/002/006/007 | ACT-0002 | Material, Hazard, StopCondition | Piloto editorial | Revisión de toxicología, piezas pequeñas y prueba 1–3 niños |
| Circuito de baja tensión con participación infantil segura por definir | SAFE-003/004/008, DEC-040 | ACT-0003 | AdultOnlyStep, PermittedChildAction, Hazard, ReviewGate | Piloto editorial reforzado | Cálculo, números de parte, inspección física, montaje desenergizado y especialista |
| Prototipo móvil familiar de punta a punta | DEC-015/017/026/036/041, UX-201/401/501, EVD-013 | Today, Participants and Roles, Preparation, Activity Session, Session Close | Fixtures sintéticos de Assignment, Participation y Observation | Exploración UX de VS-02/03 | Smoke test interactivo, 360×800, 430×932 y prueba humana pendiente |

## Regla para tareas futuras

Toda tarea de implementación debe declarar:

- Requisitos que satisface.
- Decisiones que respeta.
- Entidades o contratos modificados.
- Criterios y pruebas.
- Riesgos de privacidad/seguridad.

Si no existe requisito para una función importante, primero se actualiza el spec.

## Evidencia del Pilot Pack v0.1

- La guía de ejecución vive en [Pilot Pack v0.1](pilot-pack-v0.1.md).
- Las actividades permanecen `Draft`; su presencia en el repositorio no satisface el gate `Published`.
- Los contratos y ejemplos viven en `schemas/`; `npm run validate` es el gate automatizado mínimo.
- La revisión cruzada por agentes detecta defectos editoriales, pero no sustituye revisión pedagógica, técnica, legal o de seguridad humana.

## Evidencia del prototipo móvil familiar v0.1

- El artefacto editable vive en [`prototypes/family-mobile-v0.1/`](../../prototypes/family-mobile-v0.1/README.md).
- La evidencia de decisiones e incertidumbres vive en `research/evidence.json`; el handoff enlaza interacción, dominio y aceptación.
- `qa/flow-smoke.mjs` recorre desde planificación hasta guardado, incluyendo observación sin evaluación.
- Las capturas verifican 360×800 y 430×932 sin overflow horizontal.
- La prueba técnica no sustituye usabilidad real con un adulto facilitando una actividad ni convierte ACT-0001 en publicada.
