# Estrategia móvil y offline

**Estado:** Draft  
**Versión:** 0.1

## Decisión

La aplicación será online-first y offline-friendly. No intentará ejecutar recomendación o IA completamente offline en el MVP, pero una actividad ya planificada debe continuar aunque se pierda conexión.

## Requiere conexión

- Crear/invitar adultos y verificar permisos.
- Generar o recalcular planes.
- AI Companion y procesamiento de voz/foto.
- Publicar o moderar comunidad.
- Sincronizar Learner Models entre dispositivos.
- Descargar contenido nuevo o retirado.
- Verificar entitlement cuando lo requiera la plataforma.

## Disponible offline después de descarga

- Agenda semanal.
- ActivityVersion asignada.
- Materiales, preparación y seguridad.
- Roles y objetivos confirmados.
- Pasos e imágenes.
- Progreso de sesión.
- Valoraciones y notas de texto pendientes de sincronizar.

La voz puede grabarse offline solo si existe consentimiento y política clara, pero se recomienda deshabilitar envío/dictado hasta recuperar conexión en el MVP para evitar audio retenido indefinidamente.

## Offline pack

Contenido:

- Manifest con versión y hash.
- Datos mínimos de participantes/assignments.
- Traducciones elegidas.
- Recursos visuales optimizados.
- Restricciones y adaptaciones previamente elegidas.
- Fecha de descarga/expiración.

No contiene todo el historial del Learner Model ni medios privados innecesarios.

## Sincronización

- Cola local cifrada.
- Eventos idempotentes con identificadores de cliente.
- Resolución explícita de conflictos de rol, cierre y corrección.
- El servidor valida permisos e invariantes al recibir.
- Una versión retirada descargada muestra bloqueo al recuperar conexión; la política de emergencia offline se definirá con seguridad.

## Suscripción

No se diseña una regla artificial de “conectarse una vez al mes”. El acceso usa recibos/entitlements de tienda y backend con un período de gracia configurable. Una actividad descargada no debe detenerse en medio de una sesión por una verificación fallida temporal.

## Requisitos

- **OFF-001:** Una sesión descargada continúa sin red.
- **OFF-002:** Los datos locales sensibles se cifran mediante capacidades seguras del dispositivo.
- **OFF-003:** La sincronización es idempotente y auditable.
- **OFF-004:** El usuario ve qué está disponible y qué está pendiente.
- **OFF-005:** La aplicación no promete IA ni comunidad offline.
- **OFF-006:** Una interrupción de entitlement no corta una sesión en progreso.
