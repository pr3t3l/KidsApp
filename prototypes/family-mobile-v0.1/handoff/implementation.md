# Handoff de implementación móvil

## Qué valida este artefacto

El prototipo prueba el recorrido adulto `Hoy → mapa educativo y focos → preparación → facilitación → cierre → guardado` en un teléfono. Usa la identidad visual provisional **Pocket Workshop** del estudio previo, pero separa el producto familiar móvil del panel editorial web. La revisión v0.4 elimina el recibo obligatorio; la transparencia aparece junto a la acción de guardar y la corrección queda disponible después.

La actividad visible es `ACT-0001@0.3.0` y se identifica repetidamente como `Draft`. Esto permite evaluar el UI sin contradecir la regla de producción: una familia real solo recibe una `ActivityVersion` publicada.

## Límites

No hay backend, autenticación, cifrado de aplicación, IA, audio real, sincronización, pagos ni datos infantiles reales. Los nombres y resultados son sintéticos. La PWA conserva únicamente estado local del prototipo mediante almacenamiento del navegador; detecta la conectividad real y cachea el shell, pero no afirma sincronización. El dictado sigue siendo una simulación explicada en pantalla.

## Módulos de producto sugeridos

- `TodayPlanner`: tiempo disponible, participantes y explicación de la recomendación.
- `LearningMap`: propósito, áreas, conceptos, mecanismo, decisión infantil y divulgación progresiva.
- `ChildFocusReview`: objetivo principal único, aporte sugerido, razón explicable y exposiciones para cada participante.
- `AdultPrep`: lista completa de materiales, montaje seguro y conocimiento conceptual para guiar sin revelar una “respuesta”.
- `SessionGuide`: versión inmutable derivada del contrato narrativo; usa una referencia visual específica y jerarquía por fase: contexto breve, acción adulta, guion, seguridad, acciones de todos los niños, decisión integrada, observación/continuación y ayuda.
- `ContextualHelpSheet`: opciones publicadas ligadas a un problema; explica cambio, impacto, reanudación y límite de seguridad.
- `SessionClose`: participación real, un rating principal por niño, `not_observed` y observación opcional.
- `EvidenceReceipt`: vista opcional posterior de actividad, foco evaluado, rating contextual, exposiciones y corrección; no bloquea el guardado normal.
- `OfflineQueue`: paquete verificado, eventos idempotentes, estado de sincronización y conflicto explícito.
- `WeeklyPlan`: cinco objetos planificados navegables, cada uno con referencia editorial, promesa, foco y preparación.
- `ShoppingAggregator`: agrupa `MaterialRequirement` por sección y clave canónica; aplica `sum` a consumibles y `max` a reutilizables y conserva fuentes por actividad.

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
    roleTemplateId        # interno; no se presenta como identidad familiar
    primaryObjectiveSkillId | null
    suggestedContribution
  currentStageId
  currentEntryStateId
  expectedExitStateId
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
| Solo observar | Actualizar participación | No crear rating ni inferir exposición por observación pasiva |
| Empezar | Crear sesión con versión inmutable | Bloquear Draft/retired en `family`; permitir Draft solo en piloto/preview autorizado |
| Pausar/reanudar | Añadir evento idempotente | Persistir localmente si está offline |
| Pedir ayuda | Consultar problema común publicado | Devolver problema, cambio, impacto, reanudación y límite; mostrar stop seguro si no hay solución aprobada |
| Aplicar apoyo | Aplicar `adaptationId` publicado | Rechazar cambios de materiales, mecanismo o controles |
| Valorar | Añadir rating del objetivo asignado | Aceptar 0/1 rating principal por niño; nunca convertir `not_observed` en 1 |
| Guardar | Confirmar close-out y observación | Preservar procedencia, versión, foco evaluado, asignación interna y correcciones |

## Criterios de aceptación derivados

1. A 360×800 no hay scroll horizontal y los objetivos táctiles principales miden al menos 44 px.
2. La navegación inferior solo aparece en destinos; la sesión usa una pila de tarea sin distracciones.
3. Antes de empezar se explican propósito, áreas principal/secundarias, conceptos, mecanismo y decisión infantil sin trasladar el documento editorial completo.
4. Cada participante activo aparece por nombre con exactamente un foco principal, aporte sugerido, razón y exposiciones; no aparece un control normal de cambio de rol.
5. Preparación incluye la lista canónica y bloquea el inicio hasta confirmar materiales y superficie segura.
6. Cada fase comunica estado de entrada, estado de salida, acciones del adulto, frase literal, acción nombrada de todos los participantes, decisión cuando existe, qué observar, cuándo avanzar, seguridad y ayuda/reanudación; `Haz esto` precede al detalle secundario y el visual representa la fase actual.
7. En actividades `individual_cycles` o `hybrid`, cada participante activo completa las acciones esenciales declaradas; un foco cambia la observación o el apoyo, no reserva construir o probar a un solo niño.
8. La ayuda esencial sigue disponible después de perder la conexión cuando el shell ya fue cacheado.
9. El cierre de tres niños puede resolverse en tres toques; cada número incluye una frase visible y el tiempo se mide solo durante la prueba, sin cronómetro o cuenta regresiva en la UI.
10. `No pude observar` produce una disposición sin rating, no evidencia negativa.
11. La UI explica en una línea qué conservará y permite `Guardar y terminar` directamente; la corrección posterior y un recibo opcional preservan el control adulto.
12. Una sola sesión no comunica dominio, inteligencia, diagnóstico ni etiqueta estable.
13. El estado `Draft` es textual y persistente en toda vista que pueda confundirse con contenido entregable.
14. Las cinco actividades del plan abren un detalle con promesa, propósito, foco, materiales, recorrido, cierre y seguridad.
15. La compra muestra secciones, total y procedencia; `1 vaso del día 1 + 12 vasos del día 5 = 13 vasos`, mientras una herramienta reutilizable se cuenta una sola vez.
16. Servido por HTTPS, el prototipo declara un manifest instalable, registra un service worker y vuelve a abrir plan, compras y actividad sin depender de red después de la primera carga.
17. Recargar conserva checklist de compras, preparación y punto actual; `Reiniciar el avance` borra únicamente ese estado local.
18. El despliegue temporal no solicita permisos de cámara, micrófono o ubicación y no presenta una sincronización inexistente.

## Guion de prueba con adultos

1. Sin explicación previa, pedir que prepare una tarde de 45 minutos con tres niños.
2. Preguntar qué cree que aprenderá cada niño y por qué el sistema sugirió cada aporte.
3. Pedir que explique la función del vaso y los crayones y que narre qué resultado debe dejar Discover.
4. Durante `Imaginar`, pedir que indique qué debe hacer y decir el adulto y cómo cada niño llegará a su propio diseño.
5. Durante `Experimentar`, comprobar que entiende que cada niño prueba su puente; cortar la conexión y pedir ayuda ante un resultado no comparable.
6. Al terminar, cronometrar externamente tres observaciones y usar una vez `No pude observar`; confirmar que la UI no comunica presión temporal.
7. Después de `Guardar y terminar`, preguntar qué información cree que quedó guardada y qué conclusión cree que hará el sistema.

Registrar tiempo, dudas, errores de atribución, carga mental, claridad del guion, comprensión de la escala y recuerdo de seguridad.

## Riesgos que siguen abiertos

- Validar con familias si tres objetivos visibles antes de la actividad se sienten útiles o excesivamente estructurados.
- Validar si los niños aceptan, negocian o ignoran los aportes sugeridos, y cómo debe responder el adulto sin forzar.
- Validar si la escalera de facilitación contiene suficiente información sin obligar al adulto a leer demasiado durante la actividad.
- Validar si el contexto inicial y el resultado compacto conservan continuidad con menos lectura que dos tarjetas independientes.
- Comparar cierre paralelo versus secuencial en una prueba real; este prototipo usa tarjetas secuenciales en una sola pantalla.
- La dirección de marca y los términos “Journey” y “taller familiar” todavía requieren decisión comercial y lingüística.
- El contenido científico y físico de ACT-0001 permanece sujeto a revisión y piloto antes de publicación.

## Verificación

```powershell
python C:\Users\prett\.codex\skills\research-design-studio\scripts\make_standalone.py C:\Users\prett\Documents\Kids System\prototypes\family-mobile-v0.1 --source design-system.html --output standalone.html
python C:\Users\prett\.codex\skills\research-design-studio\scripts\make_standalone.py C:\Users\prett\Documents\Kids System\prototypes\family-mobile-v0.1 --source index.html --output prototype-standalone.html
python C:\Users\prett\.codex\skills\research-design-studio\scripts\validate_artifact.py C:\Users\prett\Documents\Kids System\prototypes\family-mobile-v0.1
```
