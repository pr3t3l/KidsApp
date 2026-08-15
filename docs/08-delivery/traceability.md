# Trazabilidad

**Estado:** Active  
**Versión:** 0.1

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
| Biblioteca publicada | P-03, ACT-002, REC-101 | Plan, Session | ActivityVersion.status | VS-01/08 | Filtro y retiro |
| Inferencias explicables | P-08, LRN-104, EVD-008 | Learning Journey | EvidenceLink, Inference | VS-04 | “¿Por qué?” y corrección |
| Medios temporales | P-09, PRV-101/102 | Troubleshoot, Voice | MediaAsset.expiry | VS-06/07 | Job de expiración |
| Adaptación segura | P-10, AI-102, SAFE-004 | Adapt | AdaptationOption | VS-06 | Evals adversariales |
| Planificación por tiempo | DEC-017, REC-000, REC-109 | Weekly Plan | WeeklyPlan, time budget | VS-05 | Casos 30/60 minutos |
| Sesión offline | DEC-019, OFF-001 | Activity Session | OfflinePack, event queue | VS-09 | Pérdida de red/sync |
| Imágenes verificadas | DEC-021, ACT-VIS-002 | Editorial Workspace | VisualAsset, QA result | VS-10 | QA + aprobación humana |
| Comunidad separada | DEC-022, COM-001/006 | Portfolio/Community | PortfolioAsset, Submission, License | VS-11/12 | Permisos y retirada |
| Gates editoriales | DEC-023, OPS-001/003 | Editorial Workspace | Review, Role, ActivityVersion | VS-08 | Workflow y auditoría |

## Regla para tareas futuras

Toda tarea de implementación debe declarar:

- Requisitos que satisface.
- Decisiones que respeta.
- Entidades o contratos modificados.
- Criterios y pruebas.
- Riesgos de privacidad/seguridad.

Si no existe requisito para una función importante, primero se actualiza el spec.
