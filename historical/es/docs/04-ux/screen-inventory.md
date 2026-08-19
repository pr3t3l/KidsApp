> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/04-ux/screen-inventory.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Inventario inicial de pantallas

**Estado:** Draft  
**Versión:** 0.1

## Aplicación familiar

| ID | Pantalla | Propósito | Slice |
|---|---|---|---|
| SCR-001 | Bienvenida/acceso | Iniciar cuenta adulta | VS-01 |
| SCR-002 | Crear familia | Idioma, unidades y configuración mínima | VS-01 |
| SCR-003 | Añadir niño | Alias y rango de edad | VS-01 |
| SCR-004 | Hoy | Próxima actividad y preparación | VS-01 |
| SCR-005 | Entender y preparar actividad | Propósito, áreas, conceptos, decisión infantil, tiempo, materiales y seguridad | VS-01 |
| SCR-006 | Focos por participante | Mostrar aporte sugerido, foco principal, razón y exposiciones por niño | VS-02 |
| SCR-007 | Facilitación paso a paso | Guiar acciones adultas, guion, acciones nominales, observación y seguridad | VS-03 |
| SCR-008 | Ayuda con este paso | Resolver un problema concreto mediante troubleshooting/adaptación publicada | VS-06 |
| SCR-009 | Cierre | Una valoración por niño | VS-03 |
| SCR-010 | Evaluar más | Habilidades secundarias opcionales | VS-03 |
| SCR-011 | Observación por voz | Grabar, transcribir y confirmar | VS-07 |
| SCR-012 | Resumen de sesión | Mostrar qué se guardó | VS-03 |
| SCR-013 | Plan semanal | Revisar y abrir cada actividad de la semana | VS-05 |
| SCR-014 | Lista de compras | Consolidar cantidades por sección, mostrar procedencia y marcar lo conseguido | VS-05 |
| SCR-014A | Detalle de actividad planificada | Promesa, propósito, foco, materiales, recorrido, cierre, seguridad y estado editorial | VS-05/01 |
| SCR-015 | Explorar biblioteca | Buscar actividad publicada | Posterior |
| SCR-016 | Learning Journey | Proyectos, conceptos y oportunidades | VS-04 |
| SCR-017 | Detalle de habilidad | Evidencia, confianza y “¿Por qué?” | VS-04 |
| SCR-018 | Corregir observación | Confirmar, editar, rechazar | VS-04 |
| SCR-019 | Familia | Miembros, preferencias e inventario | VS-01/05 |
| SCR-020 | Centro de privacidad | Medios, exportación y eliminación | Piloto/MVP |
| SCR-021 | Descargas | Estado del paquete semanal y sincronización pendiente | MVP |
| SCR-022 | Portafolio privado | Fotos/videos familiares por proyecto | Posterior |
| SCR-023 | Preparar publicación | Privacidad, recorte, actividad y normas | Comunidad |
| SCR-024 | Comunidad de actividad | Resultados moderados vinculados a una actividad | Comunidad |
| SCR-025 | Reportar publicación | Motivo y seguimiento | Comunidad |
| SCR-026 | Paywall | Trial, mensual/anual, precio y conversión | MVP comercial |
| SCR-027 | Administrar suscripción | Canal, renovación, trial, cancelación y restauración | MVP comercial |
| SCR-028 | Suscripción cancelada | Fecha final de acceso y opción de reactivar | MVP comercial |

## Estados obligatorios por pantalla

- Cargando.
- Vacío.
- Error recuperable.
- Sin conexión cuando aplique.
- Sin permiso.
- Contenido retirado o actualizado.
- IA no disponible.

## Aplicación editorial

| ID | Pantalla | Propósito |
|---|---|---|
| OPS-001 | Cola de actividades | Estado y propietario |
| OPS-002 | Editor de ActivityVersion | Esquema completo y validación |
| OPS-003 | Revisión pedagógica | Comentarios y gate |
| OPS-004 | Revisión de seguridad | Riesgos, controles y aprobación |
| OPS-005 | Registro de piloto | Resultado, duración y observaciones |
| OPS-006 | Publicar/retirar | Acción protegida y auditoría |
| OPS-007 | Recursos visuales | Versionar imágenes y alt text |
| OPS-008 | Cola de moderación | Revisar y retirar UGC |
| OPS-009 | Equipo y permisos | Especialidades, roles y acceso |

## Wireframes pendientes

Primero se diseñarán SCR-005 a SCR-012 porque concentran el recorrido que diferencia al producto. Los wireframes no deben comenzar hasta validar requisitos y casos límite del vertical slice correspondiente.
