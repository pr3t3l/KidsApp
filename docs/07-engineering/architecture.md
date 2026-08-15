# Arquitectura conceptual

**Estado:** Draft  
**Versión:** 0.1

## Objetivo

Definir fronteras antes de elegir stack. La arquitectura técnica final se decidirá después de confirmar mercado, plataforma y requisitos de operación.

## Contextos delimitados

```text
Family & Identity
       │
       ├──────────────┐
       ▼              ▼
Planning        Learner Records
       │              ▲
       ▼              │
Activity Sessions ─ Evidence
       │
       ├── Activity Catalog
       ├── Recommendation & Roles
       └── AI Companion

Content Operations ──publishes──> Activity Catalog
Safety & Privacy ──govern──> todos los contextos
```

## Componentes lógicos

### Aplicación familiar

Onboarding, plan, guía de sesión, cierre, journey y privacidad.

### Aplicación editorial

Autoría, revisiones, pilotos, publicación, retiro y recursos visuales.

### API de dominio

Expone operaciones de familia, catálogo, planes, sesiones, evidencia y medios con autorización consistente.

### Motores deterministas

Elegibilidad, filtros de seguridad, asignaciones compatibles, invariantes de evidencia y publicación. Deben funcionar y probarse sin depender de generación de IA.

### Capa de IA

Orquesta modelos generales con contexto estructurado, herramientas limitadas y salidas validadas. No es fuente de verdad.

La capa usa un gateway propio y un registro de proveedores/capacidades. Ningún proveedor recibe datos infantiles por el solo hecho de estar disponible; debe estar aprobado para el tipo de dato, región, retención y caso de uso.

### Persistencia

Datos transaccionales, contenido versionado, medios temporales y auditoría separados según sensibilidad.

## Regla fundamental

Las decisiones críticas no dependen únicamente de texto generado:

- Publicación y seguridad: reglas/estado verificable.
- Autorización: políticas de servidor.
- Un objetivo principal: restricción de dominio/datos.
- Retención: jobs y metadatos verificables.
- Adaptaciones: identificadores de opciones publicadas.

## Enfoque inicial

Para el piloto, se recomienda un monolito modular con una base transaccional y almacenamiento de objetos separado. Reduce complejidad operativa y conserva fronteras de dominio. Microservicios solo se justifican por escala, seguridad u organización demostradas.

El cliente será una aplicación móvil. El framework nativo o multiplataforma queda por decidir después de prototipos y requisitos de background sync, cámara, audio, compras y accesibilidad.

## Resiliencia

- La guía publicada debe estar disponible sin IA.
- Una sesión guarda progreso local o recuperable.
- El paquete semanal descargado contiene una versión inmutable de las actividades asignadas y no depende del modelo de IA para ejecutarse.
- Los jobs de voz/foto son idempotentes.
- Publicar o retirar invalida cachés de elegibilidad.
- Una falla de analítica no bloquea producto.

## Observabilidad

- Eventos de dominio sin contenido infantil innecesario.
- Auditoría de acceso, publicación, corrección y eliminación.
- Métricas de latencia y error por modo de IA.
- Trazas con referencias internas, no prompts completos por defecto.

## Decisiones pendientes

- Plataforma cliente.
- Lenguaje/framework.
- Base de datos.
- Autenticación.
- Proveedores de IA, voz, imágenes y almacenamiento.
- Región y despliegue.
- Estrategia offline.
- Integración de suscripciones en App Store/Google Play y posible compra web.
