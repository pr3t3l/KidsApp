# SPEC-05A — Contrato narrativo de la experiencia

**Estado:** Review
**Versión:** 0.1
**Propietario:** Contenido/Pedagogía/UX/Seguridad

## 1. Propósito

Evitar que una actividad sea una colección de pantallas correctas pero una experiencia física incoherente. Antes de redactar copy de interfaz, cada `ActivityVersion` describe la historia causal de lo que ocurrirá sobre la mesa: estado inicial, problema, acciones, cambios físicos, información obtenida y razón para pasar al momento siguiente.

El contrato no es una historia decorativa. Es la secuencia operativa que permite a otro adulto ejecutar la actividad sin completar mentalmente pasos omitidos.

## 2. Unidad de experiencia

Toda actividad declara uno de estos modos:

| Modo | Uso |
|---|---|
| `individual_cycles` | Cada niño crea o manipula un artefacto propio y completa el ciclo esencial. |
| `shared_artifact` | El resultado solo puede construirse colectivamente; la actividad justifica qué acción significativa realiza cada participante. |
| `hybrid` | Cada niño completa acciones esenciales y el grupo comparte una comparación, integración o mejora. |

El modo no se infiere desde el número de roles. Se elige desde la naturaleza física y educativa de la experiencia.

## 3. Ciclo esencial por participante

La actividad declara las acciones esenciales que todo participante activo debe experimentar cuando sean físicamente viables:

1. `encounter_problem`: observar o experimentar el fenómeno/problema.
2. `propose`: formular una idea, elección o predicción.
3. `build_or_do`: construir, manipular o ejecutar.
4. `test_or_check`: probar o comprobar el resultado.
5. `observe_result`: observar, contar, medir o describir qué ocurrió.
6. `improve_or_recommend`: realizar una mejora o proponerla usando lo observado.
7. `explain`: comunicar una relación entre acción y resultado.

Un foco principal cambia qué se observa con mayor atención; no retira al niño del ciclo esencial. Dividir el proyecto en tareas exclusivas solo es válido cuando la actividad documenta por qué cada niño conserva una experiencia educativa completa.

## 4. Estados y transiciones

La narrativa declara estados identificables, por ejemplo:

```text
STATE-READY
→ STEP-01 prueba de referencia
→ STATE-BASELINE-OBSERVED
→ STEP-02 propuestas individuales
→ STATE-DESIGNS-CHOSEN
```

Cada paso referencia:

- `entryStateId`: estado físico/informativo que debe existir antes;
- `exitStateId`: estado que queda al terminar;
- `transitionReason`: por qué ese resultado habilita el siguiente paso;
- `materialUses`: objetos utilizados y función concreta;
- `cycleActions`: acción del ciclo y audiencia que la completa.

La salida de un paso debe coincidir con la entrada del siguiente. Una fase no puede pedir mejorar antes de obtener un resultado, comparar antes de producir datos o explicar un objeto cuya función nunca se presentó.

## 5. Función de los materiales

Cada material requerido declara:

- función dentro de la experiencia;
- primer paso donde aparece;
- quién puede manipularlo;
- qué cambio físico o dato produce;
- límites de seguridad y sustitución.

La guía introduce la función antes o al mismo tiempo que el objeto. Ejemplo: `El vaso es el recipiente de carga; los crayones son unidades iguales que se agregan de uno en uno`.

## 6. Foco y calibración

Cada objetivo elegible incluye orientación específica para esta actividad:

- rango de edad orientativo;
- intención: exploración, crecimiento o consolidación;
- prerrequisitos recomendados, nunca asumidos;
- razón de adecuación;
- simplificación aprobada;
- extensión que evita una tarea trivial.

La edad es una señal inicial cuando no existe evidencia, no una conclusión sobre capacidad. Si el foco base probablemente resulta trivial para el rango, la ActivityVersion ofrece una extensión observable o selecciona otro objetivo.

## 7. Plantilla de beat

| Campo | Pregunta editorial |
|---|---|
| `entryStateId` | ¿Qué existe físicamente y qué sabe el grupo al entrar? |
| Propósito | ¿Qué información o capacidad produce este momento? |
| Acción adulta | ¿Qué prepara, muestra, controla o retira? |
| Guion | ¿Qué necesita decir exactamente? |
| Acción infantil | ¿Qué hace cada participante, no solo qué observa? |
| Decisión | ¿Qué puede elegir y qué permanece fijo? |
| Materiales | ¿Qué se usa y para qué? |
| Resultado | ¿Qué objeto, registro u observación queda? |
| `exitStateId` | ¿Cómo se identifica el nuevo estado? |
| Transición | ¿Por qué ahora tiene sentido continuar? |
| Contingencia | ¿Cómo se recupera una falla sin inventar datos? |

## 8. Revisión de mesa

Antes de revisión visual, una persona distinta al autor realiza un walkthrough narrado:

1. Coloca los materiales reales o representaciones a escala.
2. Lee la instrucción sin conocimiento previo.
3. Dice dónde está cada objeto y quién lo toca.
4. Comprueba qué recibe cada paso del anterior.
5. Recorre la experiencia de cada niño por separado.
6. Marca toda referencia a un objeto, dato o resultado que todavía no existe.
7. Cronometra esperas y turnos con el máximo de participantes soportado.

Un documento no pasa a revisión pedagógica si el walkthrough requiere que el revisor invente una acción o transición.

## 9. Gates automáticos y humanos

- **ACT-NAR-001:** Toda ActivityVersion declara modo, estado inicial, estado final, estados intermedios y ciclo esencial.
- **ACT-NAR-002:** El primer paso entra desde el estado inicial y el último termina en el estado final.
- **ACT-NAR-003:** La salida de cada paso coincide con la entrada del siguiente.
- **ACT-NAR-004:** Todo material requerido tiene función y paso de introducción válidos.
- **ACT-NAR-005:** Un paso solo puede usar materiales definidos e introducidos.
- **ACT-NAR-006:** `improve_or_recommend` requiere al menos un `observe_result` anterior.
- **ACT-NAR-007:** `explain` requiere un resultado o registro producido anteriormente.
- **ACT-NAR-008:** En `individual_cycles` y en la parte individual de `hybrid`, cada participante activo completa las acciones esenciales declaradas.
- **ACT-NAR-009:** Un foco principal no puede convertir las demás acciones esenciales del niño en mera observación pasiva.
- **ACT-NAR-010:** Cada objetivo elegible declara orientación de reto por edad/evidencia y una extensión cuando pueda resultar trivial.
- **ACT-NAR-011:** El walkthrough de mesa con el máximo de participantes se registra antes de `ready_for_pilot`.
- **ACT-NAR-012:** Las pantallas se derivan del contrato narrativo; no crean ni reordenan procedimientos por conveniencia visual.

## 10. Criterios de aceptación

1. Un revisor puede narrar minuto a minuto qué ocurre y dónde queda cada objeto.
2. Puede seguirse la trayectoria de un participante desde el problema hasta su explicación.
3. Ningún material aparece sin función previamente visible.
4. El mapa de estados permite detectar saltos causales sin ejecutar la interfaz.
5. Clasificación, circuitos, naturaleza y vida práctica pueden usar el mismo contrato aunque cambien acciones y materiales.
