> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/03-product/module-map.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Mapa de módulos

**Estado:** Review  
**Versión:** 0.1

## Módulos de experiencia

| Módulo | Responsabilidad | Depende de |
|---|---|---|
| Accounts & Family | Identidad, familia, miembros y permisos | Privacidad, datos |
| Subscription | Mensual/anual, trial de 7 días, entitlement, cancelación y restauración | Stores, Stripe futuro, Accounts |
| Onboarding | Configuración mínima y primera actividad | Family Model, biblioteca |
| Learner Profiles | Perfil, intereses, evidencia y correcciones | Learner Model, Evidence |
| Maker Inventory | Materiales disponibles | Activity Model, Family Model |
| Activity Library | Navegación de versiones publicadas | Editorial, seguridad |
| Weekly Planner | Selección y preparación semanal | Recomendador, inventario |
| Activity Session | Guía, roles, pasos y progreso | Activity Model, UX |
| Session Close | Valoración rápida y voz opcional | Evidence Model |
| Learning Journey | Historial e inferencias explicables | Learner Model |
| AI Companion | Explain, Troubleshoot, Adapt, Coach | IA, seguridad, contexto |
| Content Operations | Crear, revisar, pilotar y publicar | Activity lifecycle |
| Privacy Center | Consentimiento, exportación, retención y borrado | Datos, seguridad |
| Offline Packs | Descargar plan, assets y registrar cambios pendientes | Sessions, sincronización |
| Private Portfolio | Medios de proyecto visibles solo a la familia | Medios, privacidad |
| Community | Galería moderada de proyectos publicados por adultos | UGC, moderación, posterior al MVP |
| Editorial Workspace | Autoría, colaboración, reviews y publicación | Activity lifecycle, permisos |

## Motores de dominio

| Motor | Entrada | Salida |
|---|---|---|
| Eligibility | Participantes, contexto, seguridad | Actividades elegibles |
| Recommendation | Elegibles, objetivos, variedad | Plan o actividad ordenada |
| Role Assignment | Actividad y Learner Models | Rol + objetivo por niño |
| Adaptation | Estado de sesión y solicitud | Variante aprobada |
| Evidence | Feedback y contexto | Observaciones/inferencias propuestas |
| Learning Graph | Taxonomía y evidencia | Próximas oportunidades |
| Media QA | ActivityVersion e imagen generada | Hallazgos y estado de revisión |
| Moderation | Publicación comunitaria | Aprobar, rechazar, retirar, reportar |

## Regla de separación

Los módulos de interfaz no implementan reglas pedagógicas o de seguridad directamente. Consumen decisiones explicables de los motores y presentan estados; las reglas centrales deben ser reutilizables y verificables fuera de la UI.
