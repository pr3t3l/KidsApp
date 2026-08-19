> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/07-engineering/api-contracts.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Contratos de API conceptuales

**Estado:** Draft  
**Versión:** 0.1

Este documento define capacidades, no rutas ni tecnología finales.

## Families

- Crear/editar familia.
- Administrar miembros y permisos.
- Crear/editar/eliminar Learner.
- Administrar preferencias e inventario.
- Exportar/eliminar datos.

## Subscription

- Consultar entitlement familiar.
- Procesar recibo/webhook de tienda.
- Restaurar compra.
- Aplicar período de gracia y cambios de plan.
- Devolver deep link de gestión para Apple, Google o Stripe según origen.
- Activar/revocar pilot entitlement sin crear una prueba comercial.
- Detectar entitlement activo antes de iniciar otra compra.

## Catalog

- Buscar versiones publicadas elegibles.
- Obtener actividad/version/pasos/roles/recursos.
- Confirmar disponibilidad de materiales.
- Obtener sustituciones y adaptaciones aprobadas.

## Planning

- Solicitar recomendación con contexto.
- Obtener explicación y restricciones.
- Sustituir actividad.
- Publicar plan familiar.

## Sessions

- Crear desde una ActivityVersion.
- Confirmar participantes, roles y objetivos.
- Iniciar/pausar/reanudar/completar.
- Cambiar rol u objetivo dentro de reglas.
- Registrar paso y adaptación.
- Descargar manifest/pack semanal y sincronizar eventos offline idempotentes.

## Evidence

- Registrar evaluación principal.
- Registrar evaluación secundaria.
- Enviar observación de texto/voz.
- Revisar propuestas.
- Confirmar/corregir/rechazar.
- Consultar evidencia e inferencias explicables.

## Companion

- Iniciar interacción por modo.
- Referenciar sesión/paso.
- Solicitar upload temporal.
- Recibir acción estructurada.
- Confirmar una adaptación u observación.

## Content Operations

- Crear Activity/ActivityVersion draft.
- Validar esquema.
- Registrar review/pilot.
- Publicar/retirar.
- Comentar, sugerir, asignar y aprobar gates por rol.
- Generar candidato visual, registrar QA y aprobar asset.

## Portfolio and Community

- Crear upload privado con propósito.
- Guardar/eliminar asset de portafolio.
- Preparar derivado sin metadatos.
- Crear submission comunitaria.
- Moderar, publicar, reportar y retirar.
- Registrar consentimiento/licencia de marketing por separado.

## Convenciones futuras

- Idempotency keys para cierres, uploads y jobs.
- Versionado explícito de contratos.
- Errores de dominio legibles.
- Autorización por recurso.
- Paginación y filtros.
- ETags o control optimista para edición.
- Nunca aceptar del cliente estados derivados como confianza final o publicación.
