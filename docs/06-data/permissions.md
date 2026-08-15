# Modelo conceptual de permisos

**Estado:** Draft  
**Versión:** 0.1

## Roles familiares

| Rol | Capacidades propuestas |
|---|---|
| Owner | Administrar familia, miembros, privacidad, exportación y eliminación |
| Caregiver | Planear, ejecutar, evaluar y ver Learner Models autorizados |
| Limited adult | Ejecutar actividades asignadas y registrar observaciones limitadas |

No se define inicialmente una cuenta infantil independiente.

Solo Owner o Caregiver con permiso explícito puede guardar medios o publicar en comunidad. La aplicación puede requerir una reautenticación o parental gate para publicar.

## Roles editoriales

| Rol | Capacidades |
|---|---|
| Author | Crear y editar drafts |
| Pedagogical reviewer | Aprobar propósito, objetivos y lenguaje |
| Safety reviewer | Aprobar riesgos, controles y restricciones |
| Publisher | Publicar o retirar después de gates |
| Support auditor | Acceso excepcional, limitado y auditado |
| Community moderator | Revisar publicaciones y reportes sin acceso general a Learner Models |

## Reglas

- Denegar por defecto.
- Autorizar por familia y recurso, no solo por endpoint.
- Separar datos familiares de operaciones editoriales.
- Acceso de soporte requiere propósito, tiempo limitado y auditoría.
- Un adulto removido pierde acceso inmediatamente.
- Las URLs y búsquedas no deben permitir enumerar Learners o familias.
- La IA actúa con el mismo alcance autorizado del adulto y modo actual.
- Un moderador comunitario accede al asset presentado, contexto de moderación y cuenta adulta mínima; no a observaciones educativas.
