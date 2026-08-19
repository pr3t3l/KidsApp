> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/01-learning/evidence-model.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# SPEC-07 — Evidence Model

**Estado:** Review  
**Versión:** 0.2<br>
**Propietario:** Producto/Pedagogía/Datos

## 1. Propósito

Convertir feedback mínimo del adulto en observaciones útiles, manteniendo contexto, trazabilidad e incertidumbre.

## 2. Fuentes

1. **Automática:** actividad, versión, participantes, roles, objetivo principal y exposiciones previstas.
2. **Valoración rápida:** una respuesta por niño sobre el objetivo principal.
3. **Evaluar más:** valoraciones opcionales de objetivos secundarios.
4. **Nota de voz o texto:** observación libre del adulto.
5. **Ayuda durante la sesión:** hechos explícitos surgidos al resolver un problema, solo con confirmación apropiada.

La ausencia de feedback no es evidencia negativa.

## 3. Evaluación principal

La pregunta debe nombrar la acción y el contexto:

> Para Sofi, ¿qué tan independientemente pudo medir y marcar las piezas?

Escala:

| Valor | Ancla |
|---|---|
| 1 | No pudo hacerlo todavía, incluso con apoyo razonable. |
| 2 | Lo logró con bastante ayuda. |
| 3 | Lo logró con alguna ayuda. |
| 4 | Lo logró casi sola. |
| 5 | Lo hizo sola y con seguridad. |

La escala representa independencia contextual, no inteligencia ni valor personal.

La interfaz no muestra el número aislado como si fuera una nota. Cada opción presenta su ancla breve —por ejemplo, `3 · Con alguna ayuda`— y la pregunta nombra la acción observada. No se promedian puntuaciones entre actividades ni se crea un puntaje global del niño. Cuando una acción adulta es obligatoria por seguridad, esa ayuda no reduce la valoración; se considera únicamente la independencia dentro de las acciones permitidas al niño.

## 4. Presupuesto de interacción

- Camino normal: un toque por niño.
- Para tres niños, meta total inferior a 20 segundos.
- Nota de voz: opcional y única para la sesión; puede mencionar varios niños.
- “Evaluar más”: disponible, pero visualmente secundario.
- Se puede omitir o completar después.

## 5. Normalización de voz

La IA puede proponer observaciones estructuradas desde una nota. Debe:

- Distinguir niño, habilidad, acción, apoyo y contexto.
- Separar hechos de interpretación.
- Marcar ambigüedad.
- No inferir diagnósticos ni atributos sensibles.
- Mostrar la transcripción para edición; solo pedir confirmación adicional cuando la atribución sea ambigua o el contenido pueda cambiar materialmente un perfil.
- Respetar la política de retención del audio.

Ejemplo:

> “Mateo se frustró, pero descubrió que una base más ancha sostenía más peso.”

Observaciones propuestas:

- Persistió después de una dificultad durante ACT-X.
- Relacionó ancho de base con estabilidad durante ACT-X.

## 6. Estados

- `observed`: dato explícito del adulto o evento verificable.
- `inferred`: interpretación propuesta por IA.
- `confirmed`: adulto aceptó la interpretación.
- `corrected`: adulto modificó contexto o significado.
- `rejected`: no debe influir en el Learner Model.

## 7. Reglas de acumulación

- Una valoración aislada produce confianza inicial como máximo.
- Contextos variados aumentan la fuerza de evidencia.
- Señales contradictorias se conservan y requieren explicación.
- Evidencia reciente pesa más para recomendación, sin borrar historia.
- Exposición automática nunca se convierte en evidencia de independencia.

## 8. Requisitos

- **EVD-001:** Registrar exposiciones automáticamente sin inferir capacidad.
- **EVD-002:** Solicitar por defecto una valoración por niño y sesión.
- **EVD-003:** Usar la escala contextual de independencia 1–5.
- **EVD-004:** Permitir omitir sin penalización.
- **EVD-005:** Ofrecer “Evaluar más” de forma opcional.
- **EVD-006:** Aceptar una nota de voz o texto que cubra varios niños.
- **EVD-007:** Toda observación debe enlazar sesión, fuente y contexto.
- **EVD-008:** Toda inferencia debe enlazar evidencia y confianza.
- **EVD-009:** El adulto puede corregir o rechazar.
- **EVD-010:** La UI de cierre debe cumplir el presupuesto de 20 segundos en pruebas.
- **EVD-011:** El audio se elimina tras transcripción exitosa o expiración; la transcripción editable expira a los 30 días y las observaciones estructuradas siguen su propia retención.
- **EVD-012:** Una inferencia actualizada sin confirmación previa debe aparecer en el historial y admitir corrección posterior.
- **EVD-013:** La UI presenta cada valor 1–5 con su ancla verbal y nunca como una calificación aislada, promedio global o comparación entre niños.

## 9. Eventos mínimos

```text
SessionCompleted
ExposureRecorded
PrimaryRatingSubmitted
SecondaryRatingSubmitted
VoiceNoteProcessed
ObservationProposed
ObservationConfirmed
ObservationCorrected
InferenceUpdated
```

## 10. Casos límite

- Si el niño no participó, no crear exposición ni evaluación.
- Si cambió de rol, registrar el rol real confirmado al cierre.
- Si falló el material, permitir marcar “problema de equipo”.
- Si el adulto realizó la tarea, registrar apoyo alto sin concluir incapacidad.
- Si varios niños colaboraron inseparablemente, registrar evidencia de grupo y no atribuir desempeño individual sin confirmación.
