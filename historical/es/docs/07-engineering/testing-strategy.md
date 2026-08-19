> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/07-engineering/testing-strategy.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Estrategia de pruebas

**Estado:** Draft  
**Versión:** 0.1

## Pirámide

### Dominio

- Invariantes de objetivo principal.
- Exposición versus evidencia.
- Elegibilidad y seguridad.
- Versionado y publicación.
- Permisos.

### Integración

- Plan → sesión → cierre → Learner Model.
- Upload temporal → procesamiento → expiración.
- Publicación/retiro → catálogo.
- Corrección adulta → recálculo de inferencia.

### Contrato

- Cliente/API.
- Proveedores de IA, voz y almacenamiento.
- Esquemas de salida estructurada.

### End-to-end

- Primera actividad.
- Tres niños con objetivos distintos.
- Actividad sin evaluación.
- Troubleshooting sin IA disponible.
- Eliminación de perfil.
- Descarga offline, cierre sin red y sincronización sin duplicados.
- Suscripción en gracia sin interrumpir sesión.
- Publicación comunitaria moderada y retirada.

### UX y usabilidad

- Cierre bajo 20 segundos.
- Preparación con atención dividida.
- Errores de atribución entre niños.
- Comprensión de confianza e inferencias.
- Accesibilidad.

### Contenido

- Ejecución literal independiente.
- Materiales completos.
- Resultados esperados.
- Riesgos y adult-only steps.
- Recursos visuales por versión.

### IA

Usar la suite de `docs/05-ai/evaluations.md`, golden cases y evaluación humana. Ningún modelo se despliega solo porque mejora una métrica promedio si introduce una violación crítica.

### Imágenes y comunidad

- QA detecta materiales extra, pasos físicamente incoherentes y actor incorrecto.
- Ningún asset draft aparece en actividad publicada.
- Se eliminan metadatos de ubicación en derivados públicos.
- Guardar privado no crea submission.
- Publicar comunidad no crea licencia de marketing.
- Reporte y retirada dejan de servir el asset público.

## Datos de prueba

- Perfiles completamente sintéticos.
- Familias de 1–4 niños con edades y experiencia variadas.
- Casos con evidencia contradictoria.
- No copiar fotos, voz o nombres reales de pilotos a entornos de desarrollo.

## Gates iniciales

- Cero fallos de seguridad/autorización conocidos de severidad crítica o alta.
- Cero recomendaciones de actividades no publicadas.
- Cero asignaciones de más de un objetivo principal por niño/sesión.
- Pruebas de retención y eliminación exitosas.
- Suite de IA crítica aprobada.
