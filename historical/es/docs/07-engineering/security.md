> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/07-engineering/security.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Seguridad del producto

**Estado:** Draft  
**Versión:** 0.1

## Activos prioritarios

- Identidad y membresía familiar.
- Datos infantiles y Learner Models.
- Fotos, audio y transcripciones.
- Contenido editorial no publicado.
- Reglas de seguridad y estado de publicación.
- Credenciales y proveedores.

## Amenazas principales

- Acceso entre familias.
- Enumeración de perfiles.
- Escalada de permisos de adulto o editor.
- Inyección de instrucciones desde contenido, voz o imagen.
- Publicación sin reviews.
- Retención accidental de medios.
- Filtración mediante logs, analítica o soporte.
- Modificación de advertencias o restricciones.
- Inferencias no autorizadas sobre niños.

## Controles

- Autorización del lado servidor para cada recurso.
- Separación lógica estricta por familia.
- Cifrado en tránsito y reposo.
- URLs de medios con vida corta y alcance limitado.
- Validación de esquema para salidas de IA.
- Herramientas de IA allowlisted por modo.
- Contenido recuperado tratado como datos, no instrucciones.
- Workflow de publicación con separación de funciones.
- Auditoría inmutable de acciones críticas.
- Secretos fuera del repositorio y rotación.
- Redacción de datos sensibles en logs.
- Jobs verificables para expiración y eliminación.

## Requisitos

- **ENG-SEC-001:** Ninguna consulta familiar confía solo en un identificador proporcionado por cliente.
- **ENG-SEC-002:** Toda operación editorial crítica registra actor, tiempo y cambio.
- **ENG-SEC-003:** Un modelo no recibe credenciales ni acceso directo amplio a almacenamiento.
- **ENG-SEC-004:** Los medios temporales expiran incluso si falla el procesamiento.
- **ENG-SEC-005:** Se prueba aislamiento entre familias antes de cada lanzamiento.
- **ENG-SEC-006:** Retirar una actividad impide nuevas sesiones con esa versión.

## Antes del lanzamiento

- Threat model formal.
- Revisión de privacidad y requisitos legales del mercado.
- Pruebas de autorización y eliminación.
- Plan de incidentes.
- Revisión de proveedores y contratos.
- Verificación de backups y borrado.
