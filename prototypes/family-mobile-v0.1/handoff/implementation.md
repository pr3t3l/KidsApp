# Handoff de implementación móvil

## Qué valida este artefacto

El prototipo prueba el recorrido adulto `Hoy → roles → preparación → sesión → cierre → recibo → guardado` en un teléfono. Usa la identidad visual provisional **Pocket Workshop** del estudio previo, pero separa el producto familiar móvil del panel editorial web.

La actividad visible es `ACT-0001@0.2.2` y se identifica repetidamente como `Draft`. Esto permite evaluar el UI sin contradecir la regla de producción: una familia real solo recibe una `ActivityVersion` publicada.

## Límites

No hay backend, autenticación, persistencia, IA, audio real, sincronización, pagos ni datos infantiles reales. Los nombres y resultados son sintéticos. Los controles que simulan conexión, guardado o dictado explican esa condición en pantalla.

## Módulos de producto sugeridos

- `TodayPlanner`: tiempo disponible, participantes y explicación de la recomendación.
- `AssignmentReview`: roles compatibles, objetivo principal único, modo observar y cambios auditables.
- `AdultPrep`: lista de materiales, controles del adulto y guía conceptual sin revelar una “respuesta”.
- `SessionGuide`: versión inmutable, etapa/paso, actor sugerido, advertencia, ayuda, pausa y reanudación.
- `ApprovedAdaptationSheet`: solo opciones publicadas; nunca modifica materiales o seguridad.
- `SessionClose`: participación real, un rating principal por niño, `not_observed` y observación opcional.
- `EvidenceReceipt`: actividad, rol real, rating contextual, exposiciones y corrección antes de guardar.
- `OfflineQueue`: paquete verificado, eventos idempotentes, estado de sincronización y conflicto explícito.

## Estado mínimo de pantalla

```text
FamilySessionViewState
  activityRef { activityId, version, schemaVersion, contentHash, lifecycle }
  deliveryMode
  availableMinutes
  connectivity
  participants[]
    learnerAlias
    participation: active | observer | left_early
    roleTemplateId
    primaryObjectiveSkillId | null
  currentStageId
  completedStepIds[]
  appliedAdaptationIds[]
  closeOut[]
    learnerAlias
    disposition: rated | not_observed | did_not_participate
    primaryRating? { skillId, independenceRating }
  optionalObservation
  pendingSyncEvents[]
```

El cliente muestra y recopila estado, pero no decide publicación, elegibilidad, autorización ni confianza de inferencias.

## Mapeo de interacción a dominio

| Acción | Capacidad | Regla de servidor |
|---|---|---|
| Elegir tiempo/niños | Solicitar recomendación elegible | Filtrar por publicación, seguridad, edad, participantes, materiales y tiempo |
| Cambiar rol | Reasignar combinación compatible | Conservar exactamente un objetivo principal por participante activo |
| Solo observar | Actualizar participación | No crear rating ni inferir exposición por observación pasiva |
| Empezar | Crear sesión con versión inmutable | Bloquear Draft/retired en `family`; permitir Draft solo en piloto/preview autorizado |
| Pausar/reanudar | Añadir evento idempotente | Persistir localmente si está offline |
| Pedir ayuda | Consultar problema común publicado | Mostrar stop seguro si no hay solución aprobada |
| Ajustar ritmo | Aplicar `adaptationId` publicado | Rechazar cambios de materiales, mecanismo o controles |
| Valorar | Añadir rating del objetivo asignado | Aceptar 0/1 rating principal por niño; nunca convertir `not_observed` en 1 |
| Guardar | Confirmar close-out y observación | Preservar procedencia, versión, rol real y correcciones |

## Criterios de aceptación derivados

1. A 360×800 no hay scroll horizontal y los objetivos táctiles principales miden al menos 44 px.
2. La navegación inferior solo aparece en destinos; la sesión usa una pila de tarea sin distracciones.
3. Cada participante activo ve exactamente un rol y un objetivo principal antes de empezar.
4. El adulto puede cambiar un rol, elegir “solo observar” y volver a cambiar sin etiquetar al niño.
5. Preparación bloquea el inicio hasta confirmar materiales y superficie segura.
6. Cada paso comunica actor, acción, advertencia y ayuda/reanudación.
7. La ayuda esencial sigue disponible en la simulación offline.
8. El cierre de tres niños puede resolverse en tres toques; cada número incluye una frase visible.
9. `No pude observar` produce una disposición sin rating, no evidencia negativa.
10. El recibo permite revisar actividad, rol real, rating/excepción y observación antes de guardar.
11. Una sola sesión no comunica dominio, inteligencia, diagnóstico ni etiqueta estable.
12. El estado `Draft` es textual y persistente en toda vista que pueda confundirse con contenido entregable.

## Guion de prueba con adultos

1. Sin explicación previa, pedir que prepare una tarde de 45 minutos con tres niños.
2. Preguntar qué cree que significa cada rol y si un niño puede negarse o cambiar.
3. Pedir que explique el acordeón/canal a un niño sin construirlo por él.
4. Durante `Experimentar`, mover a un niño de rol y simular pérdida de conexión.
5. Pedir ayuda ante un puente que colapsa y verificar recuerdo de la regla de seguridad.
6. Al terminar, cronometrar tres observaciones y usar una vez `No pude observar`.
7. Preguntar qué información cree que quedó guardada y qué conclusión cree que hará el sistema.

Registrar tiempo, dudas, errores de atribución, carga mental, obediencia/coerción percibida de roles, comprensión de la escala y recuerdo de seguridad.

## Riesgos que siguen abiertos

- Validar con familias si tres objetivos visibles antes de la actividad se sienten útiles o excesivamente estructurados.
- Validar si los niños respetan, negocian o ignoran roles, y cómo debe responder el adulto sin forzar.
- Comparar cierre paralelo versus secuencial en una prueba real; este prototipo usa tarjetas secuenciales en una sola pantalla.
- La dirección de marca y los términos “Journey” y “taller familiar” todavía requieren decisión comercial y lingüística.
- El contenido científico y físico de ACT-0001 permanece sujeto a revisión y piloto antes de publicación.

## Verificación

```powershell
python C:\Users\prett\.codex\skills\research-design-studio\scripts\make_standalone.py C:\Users\prett\Documents\Kids System\prototypes\family-mobile-v0.1 --source design-system.html --output standalone.html
python C:\Users\prett\.codex\skills\research-design-studio\scripts\make_standalone.py C:\Users\prett\Documents\Kids System\prototypes\family-mobile-v0.1 --source index.html --output prototype-standalone.html
python C:\Users\prett\.codex\skills\research-design-studio\scripts\validate_artifact.py C:\Users\prett\Documents\Kids System\prototypes\family-mobile-v0.1
```
