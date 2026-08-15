# SPEC-10 — Editorial Collaboration Platform

**Estado:** Draft  
**Versión:** 0.1

## 1. Propósito

Permitir que la fundadora y, posteriormente, un equipo multidisciplinario diseñen, revisen, prueben, traduzcan, ilustren, publiquen y retiren actividades con trazabilidad.

## 2. Roles

| Rol | Responsabilidad |
|---|---|
| Author | Crea el brief y ActivityVersion draft. |
| Education reviewer | Valida propósito, nivel, preguntas y evidencia. |
| Subject specialist | Valida exactitud científica/matemática/técnica según categoría. |
| Safety reviewer | Valida riesgos, controles y adult-only steps. |
| Development reviewer | Revisa adecuación infantil cuando la categoría lo requiere; no diagnostica usuarios. |
| Language reviewer | Revisa inglés/español y equivalencia conceptual. |
| Visual reviewer | Valida imágenes, pasos, alt text y consistencia. |
| Pilot coordinator | Registra ejecuciones y hallazgos. |
| Publisher | Verifica gates y publica/retira. |
| Admin | Gestiona permisos, categorías y políticas. |

Una persona puede tener varios roles en etapas tempranas, pero cada decisión conserva el rol bajo el cual se tomó. Actividades de riesgo elevado pueden requerir separación entre autor y aprobador.

## 2.1 Matriz provisional de gates

| Categoría | Gates obligatorios |
|---|---|
| Toda actividad | Author + Education + Safety + Language + Publisher |
| Física/ingeniería/electricidad | Anteriores + Subject specialist técnico |
| Química | Anteriores + profesional competente en química; C/D además revisión independiente de seguridad |
| Biología/naturaleza | Anteriores + especialista cuando existan organismos, alergias, ingestión o impacto ambiental |
| Matemáticas | Anteriores + reviewer de enseñanza de matemáticas para progresión o explicación nueva |
| Motricidad/vida práctica | Anteriores + Development/Accessibility reviewer cuando se hagan afirmaciones de desarrollo o adaptaciones sensibles |
| Actividad C/D | Anteriores + Safety reviewer independiente del autor y aprobación reforzada del Publisher |

Un psicólogo no es gate universal para todas las actividades. Se consulta cuando existen afirmaciones sobre desarrollo, conducta, accesibilidad o interacción familiar que exceden el diseño pedagógico ordinario.

## 3. Workspace

Cada ActivityVersion ofrece:

- Estado, responsable y fecha objetivo.
- Formulario basado en Activity Schema.
- Validación inmediata de campos e invariantes.
- Comentarios por campo/paso/recurso.
- Sugerencias aceptables o rechazables.
- Diff entre versiones.
- Checklist de gates.
- Registro de pilotos e incidentes.
- Generación y QA de imágenes.
- Vista previa inglés/español y modo familiar.
- Historial de decisiones y auditoría.

## 4. Workflow

```text
Draft
→ Content complete
→ Education review
→ Subject review cuando aplica
→ Safety review
→ Visual/language review
→ Ready for pilot
→ Pilot evidence complete
→ Final review
→ Published
```

Un rechazo devuelve a Draft/Revision con hallazgo obligatorio. Un incidente crítico puede retirar una versión publicada inmediatamente.

## 5. IA editorial

Puede:

- Sugerir campos faltantes.
- Detectar inconsistencias entre materiales y pasos.
- Proponer preguntas, roles, traducciones e imágenes.
- Comparar con Learning Graph y cobertura.
- Identificar posibles riesgos para revisión.

No puede:

- Aprobar gates.
- Publicar.
- Declarar una actividad segura.
- Resolver un comentario humano como si fuera el revisor.

## 6. Colaboración

- Menciones y asignación de revisores.
- Notificaciones agrupadas, no adictivas.
- Resolución de comentarios.
- Locking optimista y detección de conflicto.
- Firma de revisión con versión exacta.
- Revisión invalidada cuando cambia un campo material relacionado.

## 7. Requisitos

- **OPS-001:** Toda aprobación referencia ActivityVersion exacta y rol del aprobador.
- **OPS-002:** Cambios materiales invalidan reviews dependientes según reglas.
- **OPS-003:** El publisher no puede omitir un gate requerido.
- **OPS-004:** El retiro es inmediato para nuevas recomendaciones.
- **OPS-005:** La plataforma conserva diff, comentarios y auditoría.
- **OPS-006:** Inglés y español deben estar completos antes de publicar en ambos idiomas.
- **OPS-007:** No se prioriza importación desde spreadsheet en el MVP editorial.
- **OPS-008:** Los gates se determinan por categoría y riesgo, no por una lista idéntica para todas las actividades.
- **OPS-009:** Una persona no puede autoaprobar una actividad C/D en el rol de seguridad.
