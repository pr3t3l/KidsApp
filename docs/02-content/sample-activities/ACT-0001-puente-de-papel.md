# ACT-0001 — Puente de papel / Paper Bridge

**Estado / Status:** Draft — no elegible para recomendación familiar / not eligible for family recommendation

**Versión / Version:** 0.3.0

**Idioma fuente / Source language:** Español (`es-US`)

**Bundles requeridos / Required bundles:** `es-US`, `en-US`

**Propietario editorial propuesto / Proposed editorial owner:** Fundadora

**Autores de esta versión / Authors of this version:** Equipo de producto, borrador para revisión humana

**Última revisión documental / Last document review:** 2026-08-15

## 1. Control de la ActivityVersion

| Campo | Valor |
|---|---|
| `activity_id` | `ACT-0001` |
| `version` | `0.3.0` |
| `slug` | `paper-bridge` |
| `status` | `draft` |
| `age_range` | 5–10 años / ages 5–10 |
| `functional_levels` | L1 Explorer, L2 Builder, L3 Inventor, L4 Engineer; asignados por habilidad y contexto, no como nivel global del niño |
| `participant_range` | 1–3 niños y un adulto supervisor / 1–3 children and one supervising adult |
| `duration` | 30–60 minutos / minutes |
| `adult_preparation` | 5–7 minutos / minutes |
| `cleanup` | 2–4 minutos / minutes; incluido en `duration` / included in `duration` |
| `safety_level` | A — materiales de bajo riesgo bajo supervisión adulta normal |
| `mess_level` | Bajo / Low |
| `space` | Mesa firme, seca y despejada de al menos 60 × 60 cm / stable, dry, clear table at least 24 × 24 in |
| `prerequisites` | Ninguno obligatorio; contar, plegar y explicar pueden ser primera exposición con apoyo. / None required; counting, folding, and explaining may be first exposures with support. |
| `accessibility` | Respuesta por voz, gesto, dibujo o selección; estabilización adulta del papel y cambio de objetivo antes de iniciar. / Response by voice, gesture, drawing, or choice; adult paper stabilization and objective change before starting. |
| `offline_required` | Sí; instrucciones, imágenes aprobadas, roles, objetivos, seguridad y cierre deben estar en el paquete descargado |

Esta versión soporta sesiones de uno, dos o tres niños. Una sesión de cuatro niños no es elegible hasta que una configuración significativa para cuatro participantes sea probada y versionada.

### 1.1 Estado de revisión

| Gate | Estado | Condición para avanzar |
|---|---|---|
| `ACT-0001-GATE-01` Propiedad editorial | Pendiente | Una persona acepta responsabilidad editorial. |
| `ACT-0001-GATE-02` Revisión pedagógica | Pendiente | Revisión de objetivos, señales observables y lenguaje adulto/infantil. |
| `ACT-0001-GATE-03` Revisión científica/disciplinar | Pendiente | Una persona competente en estructuras o enseñanza de ciencias valida mecanismo, variables y explicaciones. |
| `ACT-0001-GATE-04` Revisión de seguridad | Pendiente | Ejecución de falla segura y validación del vaso, protocolo de carga y controles. |
| `ACT-0001-GATE-05` Revisión bilingüe | Pendiente | Verificar equivalencia científica, instrucciones y advertencias `es-US`/`en-US`. |
| `ACT-0001-GATE-06` Family pilot → Published | No iniciado | Tras `ready_for_pilot`: ejecución del autor y al menos tres ejecuciones adicionales en dos familias, incluida una dirigida por otro adulto. |
| `ACT-0001-GATE-07` Recursos visuales | Pendiente | Assets ligados a 0.3.0 con QA automático y aprobación humana. |

No hay `review_records` aprobados. Por tanto, esta ActivityVersion no puede entrar en planes ni sesiones familiares de producción.

### 1.2 Convención canónica de serialización

Este documento usa directamente los patrones del JSON Schema cuando existen:

- `stepId`: `STEP-00` a `STEP-09`; `STEP-00`, `STEP-04` y `STEP-08` conforman `adultOnlyStepIds`.
- El entero `minutes` de cada paso usa la ruta canónica de 45 minutos; `minutes_by_path` conserva las variantes 30/45/60 indicadas en la ficha. La limpieza se registra también en `timing.cleanupMinutes` y ya está incluida en el total de cada ruta.
- `visualBriefId`: `VIS-01` a `VIS-08`; el contexto `ACT-0001@0.3.0` da el namespace global.
- `adaptationId`: prefijo `ADAPT-`, por ejemplo `ADAPT-BRIDGE-PAUSE`.
- `materialId`, `roleTemplateId` y `hazardId`: prefijos `MAT-`, `ROLE-` y `HAZ-` respectivamente.
- Los `ACT-0001-OBJ-*` son identificadores editoriales locales de pregunta/rúbrica; el campo serializado `primaryObjectiveSkillId` y `eligiblePrimarySkillIds` usa el `skillId` canónico asociado en 3.2.
- `requiredReviewGates`: `publisher` (`GATE-01`), `education` (`GATE-02`), `subject` (`GATE-03`), `safety` (`GATE-04`), `language` (`GATE-05`) y `visual` (`GATE-07`); `GATE-06` se serializa en `pilotRecords`, no como tipo de review gate.

Antes de `ready_for_pilot`, una representación JSON de esta versión debe validar sin transformaciones semánticas contra `schemas/v0.1/activity-version.schema.json`. La ficha Markdown no reemplaza esa validación ni un `review_record` humano.

## 2. Promesa localizada

| Bundle | Título | Resumen |
|---|---|---|
| `es-US` | Puente de papel | Construyan y comparen puentes hechos con una sola hoja para descubrir cómo la forma puede ayudar al papel a resistir una carga. |
| `en-US` | Paper Bridge | Build and compare bridges made from one sheet to discover how shape can help paper resist a load. |

### 2.1 Resultado de la experiencia

El éxito educativo no exige que un diseño sostenga una cantidad determinada. La experiencia es exitosa cuando la familia puede ejecutar al menos dos pruebas comparables, registrar lo ocurrido y proponer una mejora basada en lo observado.

Educational success does not require a design to hold a specific amount. The experience is successful when the family can run at least two comparable tests, record what happened, and propose an improvement based on what they observed.

## 3. Propósito educativo

### 3.1 Áreas, conceptos y decisiones

- **Área principal:** `ENG` Ingeniería — estructuras, diseño e iteración.
- **Áreas secundarias:** `PHY` fuerza/carga y flexión; `MAT` conteo, medición y comparación; `MOT` plegado; `LOG` prueba controlada; `COM` explicación; `SEL` persistencia; `PRA` organización y limpieza.
- **Conceptos:** estructura, carga, rigidez a la flexión, forma, distribución de carga y comparación justa.
- **Decisión infantil real:** cómo plegar o dar forma a una hoja para la prueba de mejora.
- **Pregunta de apertura `es-US`:** “¿Cómo puede una hoja de papel convertirse en un puente que sostenga una carga?”
- **Opening question `en-US`:** “How can one sheet of paper become a bridge that holds a load?”

Una exposición a estos conceptos no demuestra comprensión. Solo una acción o explicación observada puede aportar evidencia a una habilidad.

### 3.2 Objetivos principales elegibles

Cada niño recibe exactamente uno de estos objetivos principales antes de iniciar. Los demás solo pueden registrarse como exposiciones, salvo que el adulto elija **Evaluar más / Evaluate more**.

| Objective ID | Canonical `skillId` | Habilidad observable / Observable skill | Nivel / Level | Señal observable / Observable signal |
|---|---|---|---|---|
| `ACT-0001-OBJ-01` | `MAT-SKL-ONE-TO-ONE-COUNT` | Añadir y contar una carga a la vez con correspondencia uno a uno. / Add and count one load item at a time using one-to-one correspondence. | L1–L2 | Coloca un crayón por turno y mantiene o recupera el total. / Places one crayon per turn and maintains or recovers the total. |
| `ACT-0001-OBJ-02` | `MOT-SKL-FOLD-SEQUENCE` | Seguir una secuencia de plegado y colocar la estructura. / Follow a folding sequence and place the structure. | L1–L3 | Realiza los pasos en orden con el apoyo apropiado. / Completes the steps in order with appropriate support. |
| `ACT-0001-OBJ-03` | `MAT-SKL-COMPARE-RESULTS` | Comparar resultados usando más, menos o igual. / Compare results using more, less, or the same. | L1–L3 | Usa los resultados de dos pruebas para compararlas. / Uses two test results to compare them. |
| `ACT-0001-OBJ-04` | `LOG-SKL-KEEP-CONDITIONS` | Mantener constantes las condiciones de una prueba. / Keep test conditions constant. | L2–L4 | Comprueba distancia, orientación, vaso y carga entre diseños; el adulto restablece los soportes. / Checks the gap, orientation, cup, and load between designs; the adult resets the supports. |
| `ACT-0001-OBJ-05` | `ENG-SKL-ITERATE-SHAPE` | Proponer, construir y probar una mejora de forma. / Propose, build, and test a shape improvement. | L2–L4 | Elige un cambio de forma y comprueba qué ocurrió. / Chooses a shape change and tests what happened. |
| `ACT-0001-OBJ-06` | `COM-SKL-EVIDENCE-EXPLANATION` | Explicar una afirmación usando un resultado observado. / Explain a claim using an observed result. | L2–L4 | Relaciona un diseño con evidencia de la prueba, aunque la explicación causal aún sea inicial. / Connects a design to test evidence even when the causal explanation is still emerging. |

La edad filtra lenguaje y seguridad, pero no decide por sí sola el objetivo. Si no existe evidencia previa, usar el objetivo predeterminado de la configuración como exploración o crecimiento y explicar la selección como “oportunidad para observar”, no como predicción de capacidad.

#### 3.2.1 Calibración inicial sin evidencia previa

Esta tabla orienta el fixture y la primera recomendación; no reemplaza evidencia individual.

| Rango orientativo | Foco inicial preferido | Intención | Por qué puede aportar reto | Si resulta fácil / difícil |
|---|---|---|---|---|
| 5–6 | `OBJ-01` correspondencia uno a uno durante su propia prueba | Consolidación o crecimiento | Mantener una acción por número, esperar la estabilidad y recuperar el total integra conteo con una situación física. | Fácil: comparar su total con la referencia. Difícil: contar con apoyo visual o adulto y valorar solo la correspondencia observada. |
| 7–8 | `OBJ-05` proponer, construir y probar una forma propia | Crecimiento | Convierte una idea en un diseño comprobable y exige relacionarlo con un resultado, no solo plegar. | Fácil: justificar un único cambio. Difícil: elegir entre dos formas aprobadas y construir con guías. |
| 9–10 | `OBJ-04` mantener condiciones constantes | Crecimiento | Exige controlar varias condiciones mientras cada niño prueba un diseño distinto. | Fácil: registrar y explicar por qué una prueba no fue comparable. Difícil: comprobar una condición asignada con checklist. |

En cualquier rango, evidencia reciente puede justificar otro objetivo elegible. Contar hasta 20 sin espera, correspondencia o recuperación no se usa como reto principal para un niño cuando ya existe evidencia de independencia; se selecciona comparación, diseño, control de condiciones o explicación.

### 3.3 Exposiciones secundarias previstas

Solo se registra una exposición cuando el niño participó realmente en la acción o conversación correspondiente.

| Exposición / Exposure | Se registra cuando… / Record when… | No significa… / Does not mean… |
|---|---|---|
| Estructura y rigidez / Structure and stiffness | Observó o manipuló al menos dos formas de papel. / Observed or handled at least two paper shapes. | Que comprende por qué una forma resiste mejor. / That the child understands why a shape resists bending better. |
| Carga y flexión / Load and bending | Participó en una prueba y observó deformación o estabilidad. / Took part in a test and observed bending or stability. | Que puede predecir cargas o fuerzas. / That the child can predict loads or forces. |
| Conteo / Counting | Añadió, contó o comprobó piezas de carga. / Added, counted, or checked load items. | Que contó con precisión e independencia. / That the child counted accurately and independently. |
| Medición / Measurement | Ayudó a fijar o comprobar la separación. / Helped set or check the gap. | Que mide longitudes de forma independiente. / That the child measures length independently. |
| Comparación justa / Fair comparison | Participó en mantener condiciones iguales. / Helped keep conditions the same. | Que sabe diseñar una prueba controlada en otros contextos. / That the child can design a controlled test in other contexts. |
| Diseño e iteración / Design and iteration | Propuso, eligió o construyó un cambio. / Proposed, chose, or built a change. | Que la mejora funcionó o que ya domina diseño. / That the change improved the bridge or the child has mastered design. |
| Explicación / Explanation | Compartió una predicción, observación o razón. / Shared a prediction, observation, or reason. | Que la explicación científica fue completa. / That the scientific explanation was complete. |

### 3.4 Instancia del contrato narrativo

- **Modo:** `hybrid`.
- **Parte individual obligatoria:** cada participante activo encuentra el problema, propone una forma, construye una hoja propia, realiza su prueba por turnos, observa/registra su resultado y propone una mejora.
- **Parte compartida:** el grupo selecciona un único cambio basado en los resultados, construye una hoja de mejora y vuelve a probarla.
- **Regla de foco:** el objetivo principal determina qué señal observa el adulto; no reserva diseño, construcción o prueba para un solo niño.

#### Función de materiales

| Material | Función visible antes del primer uso | Introducción |
|---|---|---|
| Libros | Crear dos apoyos iguales separados 15 cm / 6 in. | `STEP-00` |
| Papel | Convertirse en el puente; una hoja por diseño. | `STEP-01` |
| Vaso | Recipiente de carga colocado en el centro; siempre vacío al iniciar una prueba. | `STEP-01` |
| Crayones | Unidades de carga iguales que se agregan de una en una dentro del vaso. | `STEP-01` |
| Regla/marcas | Comprobar que la separación permanece igual. | `STEP-00` |
| Hoja de registro | Conservar idea, diseño, resultado y comparabilidad de cada prueba. | `STEP-01` |

#### Estados y continuidad

| Paso | Estado de entrada | Acción causal | Estado de salida | Por qué habilita el siguiente momento |
|---|---|---|---|---|
| `STEP-01` Discover | `STATE-READY` | Presentar función de materiales y probar una hoja plana. | `STATE-BASELINE-OBSERVED` | Ya existe un problema visto y un resultado de referencia sobre el cual imaginar. |
| `STEP-02` Imagine | `STATE-BASELINE-OBSERVED` | Proponer formas, ver una demostración adulta y elegir una forma por niño. | `STATE-DESIGNS-CHOSEN` | Cada niño tiene una intención concreta que puede construir. |
| `STEP-03` Build | `STATE-DESIGNS-CHOSEN` | Cada niño construye y etiqueta su propia hoja. | `STATE-CHILD-DESIGNS-READY` | Hay artefactos identificables listos para probar uno por uno. |
| `STEP-04/05` Experiment | `STATE-CHILD-DESIGNS-READY` | Cada niño realiza su prueba en el mismo montaje y registra el resultado. | `STATE-CHILD-RESULTS-RECORDED` | Existen varios resultados comparables que permiten escoger una mejora. |
| `STEP-06` Improve | `STATE-CHILD-RESULTS-RECORDED` | Todos proponen; el grupo construye y prueba un único cambio. | `STATE-IMPROVEMENT-TESTED` | Hay una iteración vinculada a evidencia anterior. |
| `STEP-07` Explain | `STATE-IMPROVEMENT-TESTED` | Cada niño conecta su diseño o la mejora con algo visto o contado. | `STATE-EXPLANATION-SHARED` | La experiencia termina con evidencia expresada, no solo con un objeto. |

Una pantalla no puede cambiar este orden, omitir la prueba plana de referencia ni volver exclusivas para un solo niño las acciones individuales obligatorias.

## 4. Parámetros canónicos de la prueba

Estos parámetros forman parte del núcleo y se mantienen iguales entre diseños:

1. Una sola hoja intacta por diseño, del mismo tamaño y paquete.
2. El borde largo de la hoja cruza un espacio de `15 cm / 6 in` entre los bordes interiores de los soportes.
3. La hoja descansa sobre ambos soportes sin cinta, pegamento, clips ni otra fijación.
4. El mismo vaso liviano se coloca con su base aproximadamente en el centro del espacio y sin tocar los soportes.
5. La única carga aprobada es el mismo set de 20 crayones canónicos. En su propia prueba, cada niño baja un crayón suavemente hasta dejarlo completamente dentro del vaso; no lo deja caer. Alterna el lado del centro donde lo coloca para no concentrar toda la carga en un borde.
6. Antes de añadir el primer crayón, el adulto confirma soportes inmóviles, hoja apoyada y vaso centrado. El vaso vacío debe permanecer estable durante una cuenta lenta de tres.
7. La puntuación es la última cantidad de crayones que permaneció estable durante una cuenta lenta de tres bajo un montaje válido.
8. Si sostiene los 20, se registra `20+`; no se añaden objetos ni se sustituye la carga.

**Canonical parameters `en-US`:**

1. Use one intact sheet per design, with every sheet from the same size and package.
2. The sheet's long edge spans a `15 cm / 6 in` gap between the inner edges of the supports.
3. The sheet rests on both supports without tape, glue, clips, or other attachment.
4. Place the same lightweight cup with its base near the center of the gap and without touching the supports.
5. The only approved load is the same canonical set of 20 crayons. The child whose turn it is gently lowers one crayon fully into the cup and alternates the side of center to avoid concentrating the load on one edge.
6. Before the first crayon, the adult confirms stationary supports, sheet overlap, and a centered cup. The empty cup remains stable for a slow count of three.
7. The score is the last number of crayons that remained stable for a slow count of three under a valid setup.
8. If the bridge holds all 20, record `20+`; do not add or substitute objects.

### 4.1 Clasificación de fallas de prueba

| Estado | Definición `es-US` | Definition `en-US` | Acción / Action |
|---|---|---|---|
| `invalid_setup` | Una condición externa cambia antes de poder atribuir la falla al papel: soporte movido, hoja colocada con apoyo desigual, vaso inicialmente descentrado, carga soltada o concentrada en un borde, golpe o contacto de una persona. | An external condition changes before failure can be attributed to the paper: shifted support, uneven sheet overlap, initially off-center cup, dropped or edge-loaded crayons, bump, or participant contact. | No producir puntuación. El adulto restablece una vez desde cero. Si vuelve a ocurrir o la causa es incierta, marcar **No comparable / No comparable** y detener ese diseño. / Produce no score. The adult resets once from zero. If it happens again or the cause is uncertain, mark **No comparable** and stop that design. |
| `bridge_deformation` | Con montaje válido, el papel se curva, aplasta o pierde apoyo y entonces el centro toca la toalla o el vaso se inclina o desliza. Si falla al colocar el vaso vacío correctamente, el resultado es 0. | With a valid setup, the paper bends, flattens, or loses support and then its center touches the towel or the cup tips or slides. If it fails when the empty cup is placed correctly, the result is 0. | Terminar la prueba y registrar la última cantidad estable; no reiniciar para buscar un número mayor. / End the test and record the last stable amount; do not restart to seek a higher number. |
| `safe_stop` | Un objeto se rompe, alguien acerca la cara o la mano bajo el montaje, lleva material a la boca, lanza la carga o el adulto no puede confirmar seguridad. | An item breaks; someone puts a face or hand under the setup, mouths material, throws the load, or the adult cannot confirm safety. | Detener la actividad. No producir puntuación para la prueba interrumpida. / Stop the activity. Produce no score for the interrupted test. |

La inclinación del vaso no se reinicia automáticamente. El adulto usa las definiciones anteriores; ante duda el resultado es `invalid_setup`, nunca evidencia negativa sobre un niño. El protocolo de vaso y carga permanece sujeto al gate físico de la sección 19.

Cup tipping does not trigger an automatic restart. The adult uses the definitions above; when uncertain, the result is `invalid_setup`, never negative evidence about a child. The cup-and-load protocol remains subject to the physical gate in section 19.

La comparación es válida dentro de la sesión. No se comparan números entre familias, tipos de papel o sets de carga diferentes. / The comparison is valid within the session. Do not compare numbers across families, paper types, or different load sets.

## 5. Materiales

### 5.1 Lista canónica

| ID | Cantidad / unidad | Required | Consumable | Nombre `es-US` / `en-US` | Preparación adulta / Adult preparation | Nota de seguridad / Safety note | Sustitución aprobada / Approved substitution |
|---|---|---:|---:|---|---|---|---|
| `MAT-PAPER-COPY` | 6 `sheet` | Sí / Yes | Sí / Yes | Papel común de impresora/copia, carta o A4, del mismo paquete / Standard printer/copy paper, Letter or A4, from the same package | Reservar 1 para referencia plana y demostración adulta, hasta 3 para un diseño por niño, 1 para mejora grupal y 1 para planificación/resultados; inspeccionar sequedad e integridad. / Reserve 1 for the flat baseline and adult demonstration, up to 3 for one child design each, 1 for the group improvement, and 1 for planning/results; inspect for dryness and intact edges. | Retirar hojas húmedas, rasgadas o con bordes que puedan cortar. / Remove damp or torn sheets and any edge that could cut. | Carta o A4; elegir uno y no mezclar tamaños. / Letter or A4; choose one and do not mix sizes. |
| `MAT-SUPPORT-BOOK` | 2 `item` | Sí / Yes | No | Libros de tapa dura estables, cada uno de al menos 15 × 20 cm y 3–6 cm de grosor; diferencia de grosor ≤0.5 cm / Stable hardcover books, each at least 6 × 8 in and about 1.2–2.4 in thick; thickness difference ≤3/16 in | El adulto comprueba que estén secos, planos, sin piezas sueltas y que no se deslicen. / The adult checks that they are dry, flat, have no loose parts, and do not slide. | Solo el adulto coloca, mueve y guarda los soportes. / Only the adult places, moves, and stores the supports. | Dos cajas rectangulares cerradas, firmes, secas, no frágiles y de igual altura, tras validación adulta. / Two closed, sturdy, dry, nonbreakable rectangular boxes of equal height after adult validation. |
| `MAT-CUP-LIGHT` | 1 `item` | Sí / Yes | No | Vaso liviano de papel, vacío, de 8–12 oz, con base plana de 5–7 cm / 2–2.75 in / Empty lightweight 8–12 oz paper cup with a flat 2–2.75 in / 5–7 cm base | Inspeccionar que no esté aplastado, húmedo ni deformado; usar el mismo en todas las pruebas. Su función es contener la carga en el centro del puente. / Check that it is not crushed, damp, or warped; use the same cup in every test. Its function is to hold the load at the bridge center. | No usar con líquido ni si se tambalea sobre una mesa plana. / Do not use with liquid or if it rocks on a flat table. | Ninguna en 0.3.0; otra forma o material requiere validación física y nueva versión. / None in 0.3.0; another shape or material requires physical validation and a new version. |
| `MAT-CRAYON-LOAD` | 20 `item` | Sí / Yes | No | Veinte crayones estándar, no jumbo, intactos y de tamaño semejante, aproximadamente 8–10 cm / 3–4 in de largo / Twenty standard, non-jumbo, intact, similarly sized crayons, approximately 3–4 in / 8–10 cm long | Contar 20, retirar fragmentos y conservar exactamente el mismo set durante la sesión. Cada crayón es una unidad de carga agregada de una en una. / Count 20, remove fragments, and keep exactly the same set throughout the session. Each crayon is one load unit added one at a time. | Mantener fuera de la boca; bajar cada crayón dentro del vaso, no lanzarlo. / Keep out of mouths; lower each crayon into the cup rather than dropping it. | Ninguna en 0.3.0; marcadores, bloques, monedas y otras cargas no están validados. / None in 0.3.0; markers, blocks, coins, and other loads are not validated. |
| `MAT-RULER` | 1 `item` | Sí / Yes | No | Regla de 30 cm / 12 in sin bordes rotos / 30 cm / 12 in ruler with no broken edges | Inspeccionar; el niño puede leerla o señalar mientras el adulto mueve soportes. / Inspect it; the child may read or point while the adult moves supports. | Retirar una regla quebrada o con borde afilado. / Remove a cracked ruler or one with a sharp edge. | Cinta métrica flexible intacta bajo control adulto. / Intact flexible measuring tape under adult control. |
| `MAT-MARKER` | 1 `item` | Sí / Yes | No | Lápiz o marcador lavable / Pencil or washable marker | Comprobar que sea no tóxico y apropiado para la edad. / Check that it is nontoxic and age-appropriate. | Tapar el marcador al terminar; retirar puntas rotas. / Cap the marker after use; remove broken tips. | Otro utensilio de escritura no tóxico y apropiado para la edad. / Another nontoxic, age-appropriate writing tool. |
| `MAT-TAPE-MARK` | 4 `piece`, 2–3 cm / 1 in | No | Sí / Yes | Cinta de pintor removible opcional / Optional removable painter's tape | El adulto corta o rasga cuatro trozos y los usa solo para marcar la posición exterior de los libros. / The adult tears or cuts four pieces and uses them only to mark the books' outer positions. | Nunca fijar el puente ni pegar cinta a piel o cabello. / Never attach the bridge or put tape on skin or hair. | Omitir y comprobar la posición con la regla antes de cada prueba. / Omit it and check position with the ruler before each test. |
| `MAT-TOWEL` | 1 `item` | Sí / Yes | No | Toalla de mano en una sola capa / Hand towel in one layer | Extender bajo el espacio sin que sostenga el puente o el vaso al inicio. / Lay it under the gap without supporting the bridge or cup at the start. | Debe estar seca, plana y sin bucles o cordones sueltos. / It must be dry, flat, and free of loose loops or cords. | Tapete delgado, blando, limpio y antideslizante. / Thin, soft, clean, nonslip mat. |

### 5.2 Materiales no aprobados en esta versión

No sustituir la carga por marcadores, bloques, monedas, canicas, baterías, piedras, latas, vidrio, herramientas, alimentos, recipientes con líquido ni otros objetos. No sustituir el vaso en esta versión. No usar tijeras, grapas, alfileres, ligas tensadas ni pistola de pegamento. No fijar el puente a los soportes durante las pruebas núcleo.

Do not replace the load with markers, blocks, coins, marbles, batteries, rocks, cans, glass, tools, food, liquid-filled containers, or any other objects. Do not replace the cup in this version. Do not use scissors, staples, pins, stretched rubber bands, or a hot glue gun. Do not attach the bridge to the supports during the core tests.

## 6. Preparación adulta y seguridad

### 6.1 `STEP-00` — Preparación adulta / Adult preparation

- **Stage:** `build_or_do`; **actor:** `adult`; **minutes:** 5 en todas las rutas / 5 on every path.
- **Visual brief IDs:** `VIS-01`, `VIS-02`.
- **Expected result / Resultado esperado:** dos soportes planos e inmóviles, espacio de 15 cm / 6 in, materiales inspeccionados y configuración asignada. / Two flat, stationary supports, a 15 cm / 6 in gap, inspected materials, and an assigned configuration.
- **Success signal / Señal de éxito:** el adulto confirma checklist, vaso estable en una mesa plana y ningún material roto. / The adult confirms the checklist, a cup that is stable on a flat table, and no broken material.
- **Resume / Reanudación:** volver a inspeccionar estabilidad, separación, integridad y conteo antes de continuar. / Recheck stability, gap, integrity, and count before continuing.
- **Warning / Advertencia:** solo el adulto mueve los soportes; no iniciar si el vaso se tambalea sobre la mesa o el montaje está cerca de un borde o zona de paso. / Only the adult moves supports; do not begin if the cup rocks on the table or the setup is near an edge or walkway.
- **Common problem / Problema común:** soportes de distinta altura; reemplazarlos por un par que cumpla la tolerancia, sin compensar apilando. / Supports differ in height; replace them with a pair within tolerance rather than compensating by stacking.

#### Instrucciones `es-US`

1. Despeja una mesa firme, seca y lejos del borde de una escalera o zona de paso.
2. Inspecciona los libros, el vaso, la regla y los crayones. Retira cualquier objeto roto, afilado o frágil.
3. Extiende la toalla en una sola capa sobre la mesa. Coloca un libro a cada lado, completamente plano; la toalla no debe tocar el puente ni el vaso al inicio.
4. Deja exactamente `15 cm / 6 in` entre los bordes interiores. Marca la posición exterior con cinta removible, si la tienes.
5. Separa seis hojas del mismo paquete: referencia/demostración, una por niño (máximo tres), mejora grupal y registro.
6. Carga la configuración de participantes. Confirma un solo objetivo principal por niño; todos completarán su propio diseño y prueba.
7. Mantén los 20 crayones dentro de tu alcance y fuera del borde de la mesa.

#### Instructions `en-US`

1. Clear a stable, dry table away from stairs and walkways.
2. Inspect the books, cup, ruler, and crayons. Remove anything broken, sharp, or fragile.
3. Lay the towel flat in one layer on the table. Place one book on each side, fully flat; the towel must not touch the bridge or cup at the start.
4. Leave exactly `15 cm / 6 in` between the inner edges. Mark each outer position with removable tape, if available.
5. Set aside six sheets from the same paper package: baseline/demonstration, one per child (up to three), group improvement, and recording.
6. Load the participant configuration. Confirm exactly one primary objective per child; everyone will complete a design and test of their own.
7. Keep the 20 crayons within adult reach and away from the table edge.

### 6.3 Registro de riesgos y controles

**Nivel / Level:** A para la lista canónica exclusivamente: los niños manipulan papel, vaso y crayones de bajo riesgo bajo supervisión adulta normal. / A for the canonical list only: children handle low-risk paper, cup, and crayons under normal adult supervision.

**Supervisión / Supervision:** el adulto permanece presente, controla los soportes y puede detener la prueba inmediatamente. / The adult remains present, controls the supports, and can stop the test immediately.

| Hazard ID / category | Peligro `es-US` / Hazard `en-US` | Persona o condición / Person or condition | Control `es-US` / Control `en-US` | Step IDs |
|---|---|---|---|---|
| `HAZ-FALLING-LOAD` / `other` | Soporte, vaso o carga que cae / Falling support, cup, or load | Cualquier participante si los libros se apilan, se mueven o están cerca del borde / Any participant if books are stacked, shifted, or near the edge | Libros planos, montaje bajo, toalla debajo, mesa despejada y máximo 20 crayones; detener al moverse un soporte. / Flat books, low setup, towel below, clear table, and no more than 20 crayons; stop if a support moves. | `STEP-00`, `STEP-04`, `STEP-05`, `STEP-06`, `STEP-08` |
| `HAZ-SHARP-DAMAGE` / `cut` | Papel o regla dañados pueden cortar o pinchar / Damaged paper or ruler may cut or poke | Niño al plegar o medir / Child while folding or measuring | Inspección adulta, movimientos lentos y retiro de papel rasgado o regla quebrada. / Adult inspection, slow movements, and removal of torn paper or a cracked ruler. | `STEP-00`, `STEP-03` |
| `HAZ-MOUTHING` / `ingestion` | Crayón o fragmento llevado a la boca / Crayon or fragment placed in the mouth | Niño, especialmente si suele llevar objetos a la boca / Child, especially one who tends to mouth objects | Solo crayones intactos, supervisión continua y retiro inmediato de fragmentos; detener si ocurre. / Intact crayons only, continuous supervision, and immediate fragment removal; stop if it occurs. | `STEP-00`, `STEP-05`, `STEP-09` |
| `HAZ-THROWN-SPILL` / `spill` | Crayones lanzados o caídos pueden crear tropiezo / Thrown or dropped crayons may create a trip hazard | Grupo durante una falla / Group during a failure | Bajar uno a la vez, esperar a que todo se detenga, recoger antes de continuar y no perseguir objetos durante la prueba. / Lower one at a time, wait until everything stops, collect before continuing, and do not chase items during the test. | `STEP-05`, `STEP-09` |
| `HAZ-PINCHED-FINGER` / `other` | Dedos bajo un soporte / Fingers under a support | Niño si intenta mover un libro o caja / Child attempting to move a book or box | Colocar, reajustar y guardar soportes son acciones exclusivas del adulto; ninguna mano permanece bajo el montaje. / Placing, resetting, and storing supports are adult-only actions; no hand remains under the setup. | `STEP-00`, `STEP-04`, `STEP-08` |
| `HAZ-COMPETITION` / `other` | Frustración o competencia si el resultado se presenta como puntuación personal / Frustration or competition if the result is framed as a personal score | Niño durante prueba o explicación / Child during testing or explanation | Comparar diseños, no niños; permitir pausa y celebrar observaciones y datos inesperados. / Compare designs, not children; allow a pause and celebrate observations and unexpected data. | `STEP-05`, `STEP-07` |

### 6.4 Advertencia crítica bilingüe

> **Adulto / Adult:** Coloca y reajusta los libros. Mantén la prueba sobre una mesa baja y estable. Detén la actividad si un soporte se mueve, un objeto se rompe, un niño lleva materiales a la boca o alguien empieza a lanzar la carga. / Place and reset the books. Keep the test on a low, stable table. Stop if a support moves, an item breaks, a child mouths materials, or anyone begins throwing the load.

### 6.5 Pasos exclusivos del adulto

`adultOnlyStepIds = [STEP-00, STEP-04, STEP-08]`.

- **`es-US`:** El adulto elige y despeja el lugar; inspecciona materiales; coloca, mide y reajusta los libros; coloca/centra el vaso vacío al inicio de cada prueba; clasifica una falla como `invalid_setup`, `bridge_deformation` o `safe_stop`; retira el vaso entre pruebas; y guarda los soportes. Un niño puede leer la regla o indicar la posición, pero no mueve los soportes.
- **`en-US`:** The adult chooses and clears the location; inspects materials; places, measures, and resets the books; places/centers the empty cup at the start of every test; classifies a failure as `invalid_setup`, `bridge_deformation`, or `safe_stop`; removes the cup between tests; and stores the supports. A child may read the ruler or indicate position but does not move the supports.

La IA no puede reasignar estos pasos a un niño ni eliminar la advertencia.

AI may not reassign these steps to a child or remove the warning.

## 7. Roles y configuraciones

### 7.1 Plantillas de rol

| ID / nombre bilingüe | Compatible levels | Contribución / Contribution | Responsabilidades / Responsibilities | Objetivos elegibles / Eligible objectives | Allowed step IDs | Restricted step IDs | Dependencias / Dependencies |
|---|---|---|---|---|---|---|---|
| `ROLE-CHILD-INVESTIGATOR` Investigador/a de puente / Bridge Investigator | L1–L4 según objetivo / by objective | Completa un ciclo propio dentro del reto compartido. / Completes an individual cycle within the shared challenge. | Observa la referencia, propone, construye una hoja, realiza su prueba, registra/observa, recomienda una mejora y explica. / Observes the baseline, proposes, builds one sheet, runs an individual test, records/observes, recommends an improvement, and explains. | Cualquiera de `OBJ-01` a `OBJ-06`, exactamente uno por sesión / Any of `OBJ-01` through `OBJ-06`, exactly one per session | `STEP-01`, `STEP-02`, `STEP-03`, `STEP-05`, `STEP-06`, `STEP-07`, `STEP-09` | `STEP-00`, `STEP-04`, `STEP-08` | El adulto prepara/restablece el montaje y todos esperan el turno de prueba. / The adult prepares/resets the setup and everyone waits for the testing turn. |

Todos los niños usan la misma plantilla interna porque todos viven el ciclo completo. El objetivo principal personaliza observación, lenguaje y apoyo; no asigna monopolios sobre diseñar, contar o probar. La UI familiar no muestra el nombre técnico del rol.

### 7.2 Configuración de un niño

| Participante / Participant | Rol / Role | Objetivo predeterminado sin evidencia / Default objective without evidence | Exposiciones secundarias / Secondary exposures |
|---|---|---|---|
| Niño 1 / Child 1 | `ROLE-CHILD-INVESTIGATOR` | Según 3.2.1 y evidencia; sin evidencia, `OBJ-01` para 5–6, `OBJ-05` para 7–8 u `OBJ-04` para 9–10 / Per 3.2.1 and evidence | Estructura, carga, conteo, plegado, comparación y explicación, solo según participación real / Structure, load, counting, folding, comparison, and explanation only when actually performed |

El adulto sigue haciendo los pasos exclusivos. El niño realiza su diseño y su prueba con el apoyo apropiado. / The adult still performs adult-only steps. The child completes an individual design and test with appropriate support.

### 7.3 Configuración de dos niños

| Participante / Participant | Rol / Role | Objetivo predeterminado sin evidencia / Default objective without evidence | Exposiciones secundarias / Secondary exposures |
|---|---|---|---|
| Niño 1 / Child 1 | `ROLE-CHILD-INVESTIGATOR` | Según 3.2.1 y evidencia / Per 3.2.1 and evidence | Ciclo completo en su hoja / Full cycle on an individual sheet |
| Niño 2 / Child 2 | `ROLE-CHILD-INVESTIGATOR` | Según 3.2.1 y evidencia / Per 3.2.1 and evidence | Ciclo completo en su hoja / Full cycle on an individual sheet |

Ambos proponen, construyen y prueban una hoja por turnos. Comparten la mejora final. / Both propose, build, and test one sheet in turn. They share the final improvement.

### 7.4 Configuración de tres niños

| Participante / Participant | Rol / Role | Objetivo predeterminado sin evidencia / Default objective without evidence | Exposiciones secundarias / Secondary exposures |
|---|---|---|---|
| Niño 1 / Child 1 | `ROLE-CHILD-INVESTIGATOR` | Según 3.2.1 y evidencia / Per 3.2.1 and evidence | Ciclo completo en su hoja / Full cycle on an individual sheet |
| Niño 2 / Child 2 | `ROLE-CHILD-INVESTIGATOR` | Según 3.2.1 y evidencia / Per 3.2.1 and evidence | Ciclo completo en su hoja / Full cycle on an individual sheet |
| Niño 3 / Child 3 | `ROLE-CHILD-INVESTIGATOR` | Según 3.2.1 y evidencia / Per 3.2.1 and evidence | Ciclo completo en su hoja / Full cycle on an individual sheet |

Los tres proponen, construyen y prueban su propia hoja en orden visible. Mientras uno prueba, los demás observan y comparan; observar la prueba ajena no sustituye la prueba propia. Los tres proponen la mejora compartida. / All three propose, build, and test their own sheet in a visible order. While one tests, the others observe and compare; watching another test does not replace one's own test. All three propose the shared improvement.

### 7.5 Regla de asignación

- Antes de iniciar: exactamente un `primary_objective_id` por participante.
- Durante la sesión: cada niño conserva acceso al ciclo completo; el objetivo puede recibir apoyo, pero no se reemplaza silenciosamente.
- Al cerrar: confirmar quién participó y si realizó su prueba propia.
- Si un niño no participó: no crear exposición ni pedir valoración.
- Si el adulto hizo la acción objetivo: ofrecer “No se pudo observar / Could not observe”; no asignar un 1.

En la serialización, `eligiblePrimarySkillIds` usa los `skillId` canónicos de la sección 3.2; los `OBJ-*` identifican la pregunta/rúbrica local de esta ActivityVersion. / In serialization, `eligiblePrimarySkillIds` uses the canonical `skillId` values in section 3.2; `OBJ-*` identifies this ActivityVersion's local question/rubric.

## 8. Duraciones y rutas

| Fase / Stage | Ruta / Path 30 min | Ruta / Path 45 min | Ruta / Path 60 min |
|---|---:|---:|---:|
| Preparación adulta / Adult preparation | 5 min | 5 min | 5 min |
| Discover | 4 min | 6 min | 7 min |
| Imagine | 3 min | 5 min | 7 min |
| Build | 5 min | 8 min | 10 min |
| Experiment | 7 min | 10 min | 14 min |
| Improve | 3 min | 6 min | 11 min |
| Explain y cierre / Explain and close | 1 min | 2 min | 3 min |
| Cleanup / Limpieza | 2 min | 3 min | 3 min |

La ruta corta conserva las seis fases y una prueba por niño. La ruta de 60 minutos amplía planificación, construcción y comparación; solo repite la mejora cuando el número de participantes deja una hoja canónica sin usar. Con tres niños no añade una séptima hoja en esta versión. / The short path keeps all six stages and one test per child. The 60-minute path expands planning, building, and comparison; it repeats the improvement only when participant count leaves one canonical sheet unused. With three children, this version does not add a seventh sheet.

Los totales incluyen preparación, cierre y limpieza; no se añade tiempo oculto al bloque familiar. / Totals include preparation, close, and cleanup; no hidden time is added to the family's block.

## 9. Ejecución localizada

### 9.1 `STEP-01` — Discover / Descubrir (4–7 min)

**Stage:** `discover`. **Actor:** `group`; el adulto facilita / adult-facilitated. **Minutes:** 6 canónicos; 4/6/7 en rutas 30/45/60 / canonical; 4/6/7 on 30/45/60 paths.

**Visual brief IDs:** `VIS-02`.

**Entry / Entrada:** `STATE-READY`. **Exit / Salida:** `STATE-BASELINE-OBSERVED`.

**Expected result / Resultado esperado:** el grupo entiende para qué sirven vaso y crayones, observa una prueba real de la hoja plana y registra un resultado de referencia. / The group understands the purpose of the cup and crayons, observes a real flat-sheet test, and records a baseline result.

**Resume / Reanudación:** puede pausarse después de registrar el resultado de referencia; al volver, el adulto repite `STEP-04` antes de cualquier prueba. / Pause after recording the baseline result; on return, the adult repeats `STEP-04` before any test.

**Warning / Advertencia:** el adulto centra el vaso y corrige los soportes; los niños solo agregan crayones después de la señal y por turnos. / The adult centers the cup and adjusts supports; children add crayons only after the signal and in turn.

**`es-US`**

1. Señala los materiales: “Los libros son los apoyos. Esta hoja será el puente. El vaso irá vacío en el centro y guardará los crayones. Cada crayón será una unidad de carga”.
2. Coloca la hoja plana sobre los apoyos y pregunta: “¿Qué creen que ocurrirá cuando el vaso empiece a llenarse? ¿Dónde podría doblarse?” Cada niño predice hablando, señalando o dibujando.
3. Da la señal. El adulto centra el vaso vacío. Si permanece estable durante tres segundos, los niños agregan un crayón por turno, dicen el número y esperan tres segundos.
4. Detén la prueba cuando el papel falle o llegue a 20. Registra `PLANA`, el último número estable y si la prueba fue comparable.
5. Pregunta: “¿Qué vieron que ahora necesitamos cambiar?” No expliques todavía qué forma será mejor.

**`en-US`**

1. Point to the materials: “The books are supports. This sheet will be the bridge. The empty cup will sit in the center and hold the crayons. Each crayon is one load unit.”
2. Place the flat sheet on the supports and ask: “What do you think will happen as the cup fills? Where might it bend?” Each child predicts by speaking, pointing, or drawing.
3. Give the signal. The adult centers the empty cup. If it stays stable for three seconds, children add one crayon in turn, say the number, and wait three seconds.
4. Stop when the paper fails or reaches 20. Record `FLAT`, the last stable number, and whether the test was comparable.
5. Ask: “What did you see that we now need to change?” Do not explain which shape will work best.

**Señal de éxito / Success signal:** todos observaron el problema físico y existe un resultado de referencia; ahora tiene sentido imaginar formas. / Everyone observed the physical problem and a baseline result exists; imagining shapes now has a reason.

**Problema común / Common issue:** si el niño busca la “respuesta correcta”, responde: “Todavía no lo sabemos; la prueba nos dará información”. / If the child seeks the “right answer,” respond: “We do not know yet; the test will give us information.”

### 9.2 `STEP-02` — Imagine / Imaginar (3–7 min)

**Stage:** `imagine`. **Actor:** `group`; todos los niños proponen y el adulto facilita / all children propose, with adult facilitation. **Minutes:** 5 canónicos; 3/5/7 por ruta / canonical; 3/5/7 by path.

**Visual brief IDs:** `VIS-03`.

**Entry / Entrada:** `STATE-BASELINE-OBSERVED`. **Exit / Salida:** `STATE-DESIGNS-CHOSEN`.

**Expected result / Resultado esperado:** cada niño elige o dibuja una forma propia después de observar la referencia; el grupo identifica las condiciones que permanecerán iguales. / Each child chooses or draws an individual shape after observing the baseline; the group identifies the conditions that will stay the same.

**Resume / Reanudación:** guardar cada dibujo con el nombre del niño; al volver, confirmar una forma por participante. / Save each drawing with the child's name; on return, confirm one shape per participant.

**Warning / Advertencia:** solo elegir formas de papel aprobadas; no añadir herramientas, fijaciones, otra hoja ni una carga diferente. / Choose only approved paper shapes; do not add tools, fasteners, another sheet, or a different load.

**`es-US`**

1. Retira vaso y carga. Coloca a la vista el resultado `PLANA` y pregunta: “¿Cómo podríamos cambiar la forma de una hoja para que sea más difícil de doblar?” Registra todas las ideas.
2. Usa la hoja de referencia ya probada para mostrar solo el inicio de un acordeón: doblar una franja, voltear y doblar otra. Muestra también los diagramas de canal y pliegues anchos; no construyas los diseños infantiles.
3. Entrega a cada niño un espacio de planificación. Cada uno elige o dibuja una forma aprobada para su propia hoja y predice qué ocurrirá.
4. Pregunta: “¿Qué debe permanecer igual aunque cada puente tenga otra forma?” Confirmen papel, 15 cm, vaso, 20 crayones y procedimiento.
5. Ordenen los turnos de construcción y prueba. Ninguna idea se elimina por parecer menos resistente.

**`en-US`**

1. Remove the cup and load. Keep the `FLAT` result visible and ask: “How could we change one sheet's shape so it is harder to bend?” Record every idea.
2. Use the tested baseline sheet to demonstrate only the start of an accordion: fold one strip, turn, and fold again. Also show channel and wide-fold diagrams; do not build the children's designs.
3. Give each child planning space. Each chooses or draws one approved shape for an individual sheet and predicts what will happen.
4. Ask: “What must stay the same even when each bridge has a different shape?” Confirm paper, 6 in, cup, 20 crayons, and procedure.
5. Set the build and test order. Do not remove an idea because it seems less strong.

**Señal de éxito / Success signal:** existe una forma identificada por niño y una lista común de condiciones fijas; ahora cada idea puede construirse. / One identified shape exists per child and there is a shared list of fixed conditions; each idea can now be built.

**Problema común / Common issue:** múltiples ideas incompatibles. Registra todas y elige una por turno; no las combines en la misma prueba. / If there are several incompatible ideas, record all of them and choose one per turn; do not combine them in one test.

### 9.3 `STEP-03` — Build / Construir (5–10 min)

**Stage:** `build_or_do`. **Actor:** `group`; cada participante construye una hoja propia con apoyo / each participant builds an individual sheet with support. **Minutes:** 8 canónicos; 5/8/10 por ruta / canonical; 5/8/10 by path.

**Visual brief IDs:** `VIS-03`.

**Advertencia / Warning:** usar solo papel intacto; no usar tijeras ni fijaciones. / Use only intact paper; do not use scissors or fasteners.

**Entry / Entrada:** `STATE-DESIGNS-CHOSEN`. **Exit / Salida:** `STATE-CHILD-DESIGNS-READY`.

**Expected result / Resultado esperado:** hay una estructura de una hoja por niño, identificada con nombre/diseño y orientación de prueba. / There is one single-sheet structure per child, identified by child/design and test orientation.

**Resume / Reanudación:** conservar cada estructura junto a su dibujo y nombre; no apilarlas ni cambiar su orientación. / Keep each structure beside its drawing and name; do not stack it or change its orientation.

**`es-US`**

1. Entrega una hoja igual a cada niño. Mantén la hoja de referencia/demostración separada.
2. Uno por uno, pide que muestre su plan y diga o señale qué forma intentará. El adulto puede marcar guías o sostener el papel.
3. Cada niño construye su forma. Para acordeón: doblar una franja de aproximadamente `2.5 cm / 1 in`, voltear y repetir. Para canal: levantar ambos bordes largos. Para pliegues anchos: repetir la secuencia con menos franjas.
4. El niño coloca su nombre o símbolo en la hoja de registro, no sobre la zona de prueba del puente.
5. Abre y orienta cada estructura para que cruce el espacio. El adulto comprueba integridad, pero no corrige el diseño para hacerlo “ganar”.
6. Ordena las estructuras según el turno acordado.

**`en-US`**

1. Give one equal sheet to each child. Keep the baseline/demonstration sheet separate.
2. One at a time, ask each child to show the plan and say or point to the intended shape. The adult may mark guides or hold the paper.
3. Each child builds the chosen shape. For an accordion: fold a strip about `1 in`, turn, and repeat. For a channel: lift both long edges. For wide folds: repeat the sequence with fewer strips.
4. The child adds a name or symbol to the recording sheet, not to the bridge test area.
5. Open and orient every structure so it can span the gap. The adult checks integrity but does not correct a design to make it “win.”
6. Place structures in the agreed test order.

**Señal de éxito / Success signal:** cada niño puede identificar su estructura y cómo se colocará; ahora existen artefactos propios listos para probar. / Each child can identify an individual structure and its orientation; individual artifacts are now ready to test.

**Problemas comunes / Common issues:**

- Pliegues diagonales: continuar y registrar; para la mejora se pueden marcar guías rectas. / Diagonal folds: continue and record it; straight guidelines may be marked for the improvement.
- Acordeón aplastado: abrirlo suavemente sin tirar de los extremos. / Flattened accordion: open it gently without pulling the ends.
- Motricidad difícil: el adulto sostiene el papel o marca líneas; si crea los pliegues, no se evalúa `OBJ-02`. / Folding is physically difficult: the adult holds the paper or marks lines; if the adult makes the folds, do not assess `OBJ-02`.

### 9.4 Experiment / Experimentar (7–12 min)

#### `STEP-04` — Verificar y restablecer / Verify and reset

**Stage:** `experiment`. **Actor:** `adult`. **Minutes:** 2 canónicos; 1/2/2 minutos totales por ruta, repartidos entre las verificaciones repetidas / canonical; 1/2/2 total minutes by path, shared across repeated checks.

**Visual brief IDs:** `VIS-02`, `VIS-07`.

**Expected result / Resultado esperado:** soportes inmóviles, espacio de 15 cm / 6 in, toalla sin contacto inicial y hoja con apoyo semejante en ambos lados. / Stationary supports, a 15 cm / 6 in gap, no initial towel contact, and similar sheet overlap on both sides.

**Success signal / Señal de éxito:** el adulto y el niño cuyo turno comienza confirman las condiciones; solo el adulto ha movido los soportes. / The adult and the child whose turn begins confirm the conditions; only the adult has moved the supports.

**Resume / Reanudación:** repetir todo `STEP-04` después de una pausa y antes de cada diseño. / Repeat all of `STEP-04` after a pause and before every design.

**Warning / Advertencia:** solo el adulto coloca y reajusta soportes; no apilar, elevar ni sostener un libro con la mano durante la carga. / Only the adult places and resets supports; do not stack, raise, or hold a book by hand during loading.

**Common problem / Problema común:** si las marcas no coinciden o los soportes difieren en altura, no compensar con objetos; corregir el par o marcar `invalid_setup`. / If marks do not align or supports differ in height, do not compensate with objects; correct the pair or mark `invalid_setup`.

- **`es-US`:** El adulto confirma el espacio y la toalla, coloca el diseño con apoyo semejante y da la señal de listo. Entre pruebas retira vaso y carga, restablece los soportes y repite la verificación.
- **`en-US`:** The adult confirms the gap and towel, places the design with similar overlap, and gives the ready signal. Between tests, the adult removes the cup and load, resets the supports, and repeats the check.

#### `STEP-05` — Cargar, observar y registrar / Load, observe, and record

**Stage:** `experiment`. **Actor:** `group`; cada niño prueba por turno / each child tests in turn. **Minutes:** 8 canónicos; 6/8/12 por ruta / canonical; 6/8/12 by path.

**Visual brief IDs:** `VIS-04`, `VIS-05`, `VIS-07`.

**Entry / Entrada:** `STATE-CHILD-DESIGNS-READY`. **Exit / Salida:** `STATE-CHILD-RESULTS-RECORDED`.

**Expected result / Resultado esperado:** la hoja de referencia y cada diseño infantil producen un resultado `0–20+` bajo montaje válido o `No comparable` con causa; cada niño realizó su propia prueba. / The baseline and every child design produce a `0–20+` result under a valid setup or `Not comparable` with a cause; every child ran an individual test.

**Resume / Reanudación:** registrar diseño, resultado y estado antes de pausar; al volver, comenzar desde `STEP-04`, no desde una carga parcial. / Record design, result, and status before pausing; on return, restart from `STEP-04`, not from a partial load.

**Warning / Advertencia:** nadie acerca cara o manos debajo del montaje; bajar, no soltar, un crayón a la vez; aplicar `safe_stop` ante una condición de detención. / No one puts a face or hands under the setup; lower rather than drop one crayon at a time; apply `safe_stop` for any stop condition.

**`es-US`**

1. Mantén visible el resultado `PLANA`. Toma la primera estructura infantil y nombra el turno: diseño de [niño].
2. El adulto completa `STEP-04`, coloca la estructura y centra el vaso vacío. El niño del turno confirma su forma y espera la señal.
3. El niño baja un crayón completamente dentro del vaso, dice el número y espera tres segundos. Alterna el lado del centro; no lo deja caer. Los demás observan dónde se dobla y si cambia una condición.
4. Cuando ocurra una falla, el adulto aplica 4.1. En `bridge_deformation`, registra la última cantidad estable; en `invalid_setup`, no registra número y restablece una sola vez.
5. El niño del turno dice o señala qué observó en su puente. Registra diseño, resultado, comparabilidad y observación antes de retirar la hoja.
6. Repite desde `STEP-04` para cada participante. Observar la prueba de otro no sustituye realizar la propia.
7. Cuando todos hayan probado, comparen resultados válidos con `más`, `menos` o `igual`; si un diseño sostiene 20, registra `20+`.

**`en-US`**

1. Keep the `FLAT` result visible. Take the first child structure and name the turn: [child]'s design.
2. The adult completes `STEP-04`, places the structure, and centers the empty cup. The child confirms the shape and waits for the signal.
3. The child lowers one crayon fully into the cup, says the number, and waits three seconds. Alternate sides of center; do not drop it. Others watch where it bends and whether a condition changes.
4. When a failure occurs, the adult applies 4.1. For `bridge_deformation`, record the last stable amount; for `invalid_setup`, record no number and reset only once.
5. The child says or points to what happened to the bridge. Record design, result, comparability, and observation before removing the sheet.
6. Repeat from `STEP-04` for every participant. Watching another test does not replace running one's own.
7. After everyone tests, compare valid results using `more`, `less`, or `the same`; if a design holds 20, record `20+`.

**Success signal / Señal de éxito:** existe un resultado u observación honesta por participante y al menos dos resultados pueden compararse; ahora la mejora puede basarse en evidencia real. / A result or honest observation exists for every participant and at least two results can be compared; improvement can now use real evidence.

**Common problem / Problema común:** si el vaso se inclina entre crestas, no reiniciar automáticamente; el adulto decide entre `invalid_setup` y `bridge_deformation` según 4.1. / If the cup tips between ridges, do not automatically restart; the adult chooses `invalid_setup` or `bridge_deformation` under 4.1.

### 9.5 `STEP-06` — Improve / Mejorar (3–11 min)

**Stage:** `improve`. **Actor:** `group`; todos proponen y comparten construcción/prueba / everyone proposes and shares building/testing. **Minutes:** 6 canónicos; 3/6/11 por ruta / canonical; 3/6/11 by path.

**Visual brief IDs:** `VIS-08`.

**Entry / Entrada:** `STATE-CHILD-RESULTS-RECORDED`. **Exit / Salida:** `STATE-IMPROVEMENT-TESTED`.

**Expected result / Resultado esperado:** una hoja grupal incorpora exactamente un cambio basado en los resultados infantiles y produce un resultado válido o `No comparable` documentado. / One group sheet incorporates exactly one change based on the children's results and produces a valid result or a documented `Not comparable` state.

**Resume / Reanudación:** dibujar la mejora elegida y guardar la hoja sin carga; al volver, repetir `STEP-04`. / Draw the chosen improvement and store the unloaded sheet; on return, repeat `STEP-04`.

**Warning / Advertencia:** no combinar cambios ni aumentar peso, altura o separación; el adulto conserva control de soportes y clasificación de fallas. / Do not combine changes or increase weight, height, or gap; the adult retains control of supports and failure classification.

**`es-US`**

1. Coloca juntos la tabla de resultados y los diseños sin carga. Cada niño responde: “¿Qué cambiarías después de ver tu prueba y por qué?”
2. Registra las tres recomendaciones. El grupo elige un solo cambio aprobado: ancho, cantidad o rectitud de pliegues, o bordes longitudinales levantados.
3. Usa la hoja reservada para mejora. Cada niño realiza una parte compatible: marcar/indicar el cambio, plegar con apoyo y comprobar que coincide con la decisión.
4. Todos predicen si sostendrá más, menos o igual que un resultado anterior y nombran con cuál lo compararán.
5. Repitan `STEP-04/05`: por turnos, uno confirma el cambio, otro agrega/contabiliza carga y otro vigila condiciones; estas funciones rotan y no reemplazan las pruebas propias ya realizadas.
6. Registren el resultado aunque sostenga menos o no sea comparable. En 60 minutos, repitan la mejora solo si el número de participantes dejó una hoja canónica sin usar; con tres niños profundicen la comparación sin añadir papel.

**`en-US`**

1. Place the result table and unloaded designs together. Each child answers: “After seeing your test, what would you change and why?”
2. Record all recommendations. The group chooses one approved change: fold width, number, or straightness, or raised long edges.
3. Use the reserved improvement sheet. Each child performs a compatible part: mark/name the change, fold with support, and verify that it matches the decision.
4. Everyone predicts whether it will hold more, less, or the same as one prior result and names the comparison.
5. Repeat `STEP-04/05`: in turn, one confirms the change, one adds/counts load, and one watches conditions; these functions rotate and do not replace the individual tests already completed.
6. Record the result even if it holds less or is not comparable. On a 60-minute path, repeat the improvement only when participant count left one canonical sheet unused; with three children, deepen comparison without adding paper.

**Señal de éxito / Success signal:** el grupo cambia una variable de forma, prueba y conserva el resultado sin llamarlo éxito o fracaso personal. / The group changes one shape variable, tests it, and keeps the result without framing it as personal success or failure.

**Problema común / Common issue:** si quieren cambiar varias cosas, dibuja las ideas y elige una; las demás quedan para otra hoja o sesión. / If the group wants to change several things, draw the ideas and choose one; save the others for another sheet or session.

### 9.6 `STEP-07` — Explain / Explicar (1–3 min)

**Stage:** `explain`. **Actor:** `group`; el adulto escucha y hace una pregunta de evidencia / the adult listens and asks an evidence question. **Minutes:** 2 canónicos; 1/2/3 por ruta / canonical; 1/2/3 by path.

**Visual brief IDs:** `VIS-05`, `VIS-06`.

**Entry / Entrada:** `STATE-IMPROVEMENT-TESTED`. **Exit / Salida:** `STATE-EXPLANATION-SHARED`.

**Expected result / Resultado esperado:** cada niño conecta su propia prueba o la mejora grupal con algo visto o contado; la familia conserva resultados inesperados. / Every child connects an individual test or the group improvement to something seen or counted; the family keeps unexpected results.

**Resume / Reanudación:** puede completarse después usando la hoja de resultados; indicar que la explicación fue diferida. / It may be completed later using the results sheet; mark that explanation was deferred.

**Warning / Advertencia:** los diseños están sin carga y los soportes ya no se manipulan; no presentar el número como puntuación del niño. / Designs are unloaded and supports are no longer handled; do not frame the number as a child's score.

**`es-US`**

1. Coloquen juntos los diseños sin carga, cada uno junto a su resultado, y la mejora grupal al final.
2. Por turnos pregunta a cada niño: “En tu puente, ¿qué hiciste y qué viste o contaste?” Acepta señalar, dibujar o elegir.
3. Pregunta: “¿Qué recomendaste cambiar después de tu prueba? ¿Dónde aparece esa idea en la mejora grupal?”
4. Pregunta al grupo: “¿Qué mantuvimos igual para poder comparar?”
5. Conecta sus palabras con forma, carga y flexión sin declarar que más pliegues siempre son mejores. Celebren haber completado pregunta, diseño, prueba y mejora, no el número más alto.

**`en-US`**

1. Put the unloaded designs beside their results, with the group improvement last.
2. In turn ask each child: “In your bridge, what did you do and what did you see or count?” Accept pointing, drawing, or choosing.
3. Ask: “What change did you recommend after your test? Where can we see that idea in the group improvement?”
4. Ask the group: “What did we keep the same so we could compare?”
5. Connect their words to shape, load, and bending without claiming that more folds are always better. Celebrate completing the question, design, test, and improvement—not the highest number.

**Señal de éxito / Success signal:** cada niño identifica una acción propia y un resultado; la explicación cierra el ciclo que comenzó con la hoja plana. No se exige vocabulario científico. / Every child identifies an individual action and result; the explanation closes the cycle that began with the flat sheet. Scientific vocabulary is not required.

**Common problem / Problema común:** un niño repite la explicación adulta; volver a “¿qué viste o contaste?” y aceptar gesto, dibujo o elección sin corregir hacia una frase modelo. / A child repeats the adult explanation; return to “what did you see or count?” and accept a gesture, drawing, or choice without correcting toward a model sentence.

## 10. Explicaciones

### 10.1 Explicación adulta breve

**`es-US`:** La forma cambia cómo se dobla el papel. Una hoja plana se flexiona con facilidad; los pliegues crean crestas y pequeñas paredes que pueden ayudar a la hoja a conservar su forma y distribuir la carga. La prueba debe mantener iguales el papel, la separación, el vaso y la carga para atribuir la diferencia principalmente a la forma.

**`en-US`:** Shape changes how paper bends. A flat sheet flexes easily; folds create ridges and small walls that can help the sheet keep its shape and distribute the load. The test must keep the paper, gap, cup, and load the same so the difference can be attributed mainly to shape.

### 10.2 Explicación adulta detallada

**`es-US`:** La rigidez a la flexión depende del material y de la geometría de la sección. Como las hojas provienen del mismo paquete, la variable que buscamos cambiar es la geometría. Al plegar, parte del papel queda más lejos de la zona central donde la estructura se curva y aparecen paredes que resisten la deformación. Esto puede aumentar la rigidez del conjunto sin cambiar el material. El resultado también depende de la dirección, uniformidad y daño de los pliegues; del lugar donde se aplica la carga; del espacio; y de la estabilidad de los apoyos. Por eso un acordeón no tiene garantizado superar a la hoja plana. Un dato inesperado invita a comprobar el montaje y repetir, no a reemplazarlo por el resultado esperado.

**`en-US`:** Bending stiffness depends on both the material and the geometry of its cross-section. Because the sheets come from the same package, geometry is the variable we intend to change. Folding moves some paper farther from the central region where the structure bends and creates walls that resist deformation. This can increase the stiffness of the structure without changing the material. The result also depends on fold direction, uniformity, and damage; load placement; gap width; and support stability. An accordion is therefore not guaranteed to outperform the flat sheet. An unexpected result is a reason to check the setup and repeat—not to replace the data with the expected result.

### 10.2.1 Guía práctica para que el adulto acompañe el diseño

Esta guía ayuda al adulto a hacer preguntas y mostrar posibilidades sin diseñar el puente por el niño.

**`es-US`:**

1. Empieza con la hoja plana y pregunta: “¿Dónde se está doblando?” y “¿Cómo podríamos hacer que una parte del papel quede de pie en vez de completamente acostada?”.
2. Si el niño no tiene una idea, usa la hoja de planificación para mostrar **un solo pliegue de ejemplo**, no el puente completo. Después devuelve la decisión: “¿Quieres repetirlo, hacerlo más ancho o probar otra forma?”.
3. Ofrece como posibilidades, no como respuestas: un acordeón con montañas y valles repetidos; bordes largos levantados como un canal; pliegues más anchos o más estrechos; o guías para que los pliegues queden rectos.
4. Antes de probar, pregunta: “¿Las crestas van de un libro al otro?” Las crestas que cruzan el espacio pueden funcionar como pequeñas paredes; si van de lado a lado del puente, quizá no ayuden de la misma manera.
5. Ayuda a hacer pliegues definidos y uniformes sin romper el papel. No digas que “más pliegues siempre es mejor”: demasiados pliegues pequeños pueden aplastarse o quedar desiguales.
6. Después de la prueba, vuelve a la evidencia: “¿Qué cambiaste?”, “¿Dónde se dobló?” y “¿Qué intentarías ahora?”. El objetivo es iterar, no adivinar el diseño ganador.

**`en-US`:**

1. Begin with the flat sheet and ask, “Where is it bending?” and “How could we make part of the paper stand up instead of lying completely flat?”
2. If the child has no idea, use the planning sheet to demonstrate **one sample fold**, not the complete bridge. Return the choice: “Would you like to repeat it, make it wider, or try another shape?”
3. Offer possibilities rather than answers: an accordion with repeating peaks and valleys; raised long edges forming a channel; wider or narrower folds; or guidelines that help keep folds straight.
4. Before testing, ask, “Do the ridges run from one book to the other?” Ridges that span the gap can act like small walls; ridges running across the bridge may not help in the same way.
5. Support crisp, even folds without tearing the paper. Do not say “more folds are always better”: too many small folds may flatten or become uneven.
6. After the test, return to evidence: “What did you change?”, “Where did it bend?” and “What would you try next?” The goal is iteration, not guessing the winning design.

### 10.3 Explicación infantil

**`es-US`:** “El papel sigue siendo papel, pero su forma cambió. Las crestas son como muchas paredes pequeñas que pueden ayudarlo a no doblarse tan rápido. La prueba nos dice qué ocurrió con nuestras formas.”

**`en-US`:** “The paper is still paper, but its shape changed. The ridges are like many small walls that can help it keep from bending as quickly. The test tells us what happened with our shapes.”

### 10.4 Observaciones físicas esperadas, sin garantía

**`es-US`:** Es común que la hoja plana se hunda o pierda estabilidad con poca carga y que un acordeón bien orientado permanezca estable con más crayones. También es posible obtener un empate o que el acordeón sostenga menos por pliegues aplastados, diagonales o desiguales, por una carga descentrada o por movimiento de los soportes. Más pliegues no siempre significa mejor desempeño. La observación real de la familia prevalece sobre este patrón común.

**`en-US`:** It is common for the flat sheet to sag or lose stability with a small load and for a well-oriented accordion to remain stable with more crayons. A tie is also possible, or the accordion may hold less because folds are flattened, diagonal, or uneven, the load is off-center, or the supports move. More folds do not always mean better performance. The family's actual observation takes precedence over this common pattern.

### 10.5 Hoja mínima de registro / Minimum recording sheet

| Diseño / Design | Predicción / Prediction | Crayones estables / Stable crayons | Qué observamos / What we observed |
|---|---|---:|---|
| Plano / Flat | Más / Menos / Igual / More / Less / Same | 0–20+ | Curvatura, deslizamiento o estabilidad / Bending, slipping, or stability |
| Acordeón / Accordion | Más / Menos / Igual / More / Less / Same | 0–20+ | Dirección y uniformidad de pliegues / Fold direction and evenness |
| Mejora / Improvement | Más / Menos / Igual / More / Less / Same | 0–20+ | Cambio elegido y resultado / Chosen change and result |

## 11. Solución de problemas / Troubleshooting

| Situación / Situation | `es-US` | `en-US` | Impacto en evidencia / Evidence impact |
|---|---|---|---|
| Los libros se mueven / Books move | Detén la prueba. El adulto devuelve los libros a las marcas, comprueba 15 cm / 6 in y reinicia ese diseño desde cero. | Stop the test. The adult returns the books to their marks, checks 15 cm / 6 in, and restarts that design from zero. | No usar el resultado interrumpido para comparar. / Do not use the interrupted result for comparison. |
| El vaso se inclina / Cup tips | No reinicies automáticamente. El adulto aplica 4.1: si hubo montaje o carga externa desigual, `invalid_setup`; si el papel se deformó bajo un montaje válido, `bridge_deformation`. | Do not restart automatically. The adult applies 4.1: external setup or uneven loading means `invalid_setup`; paper deformation under a valid setup means `bridge_deformation`. | `invalid_setup` no produce puntuación ni evidencia negativa; `bridge_deformation` conserva la última carga estable. / `invalid_setup` produces no score or negative evidence; `bridge_deformation` keeps the last stable load. |
| Los crayones ruedan o caen / Crayons roll or fall | Espera a que todo se detenga y clasifica la causa: caída después de deformación válida = `bridge_deformation`; crayón soltado fuera del vaso o golpe = `invalid_setup`; lanzamiento, rotura o material en boca = `safe_stop`. | Wait until everything stops and classify the cause: a fall after valid paper deformation = `bridge_deformation`; a crayon dropped outside the cup or a bump = `invalid_setup`; throwing, breakage, or mouthing = `safe_stop`. | Solo `bridge_deformation` conserva la última carga estable; nunca adivinar el total ni atribuir la falla al niño. / Only `bridge_deformation` keeps the last stable load; never guess the count or attribute the failure to the child. |
| La hoja plana sostiene los 20 / Flat sheet holds 20 | Registra `20+`. No añadas peso. Aumentar el espacio no está aprobado como adaptación automática de esta versión. Compara deformación visible o repite en otra sesión versionada. | Record `20+`. Do not add weight. Increasing the gap is not approved as an automatic adaptation in this version. Compare visible bending or repeat in another versioned session. | No inferir que no hubo aprendizaje. / Do not infer that no learning occurred. |
| Ambos diseños dan el mismo resultado / Both designs match | Comprueba condiciones y acepta el empate. Pregunta qué nueva prueba ayudaría a saber más. | Check the conditions and accept the tie. Ask what new test would help you learn more. | Un empate es evidencia válida de esta prueba. / A tie is valid evidence from this test. |
| El acordeón sostiene menos / Accordion holds less | Revisa orientación, daño y uniformidad. Si la prueba fue justa, conserva el dato y explora una mejora. | Check orientation, damage, and evenness. If the test was fair, keep the result and explore an improvement. | No sustituir por una expectativa editorial. / Do not replace it with an editorial expectation. |
| Plegar resulta difícil / Folding is difficult | Marca guías, estabiliza el papel o permite que el niño dirija al adulto. Cambia el objetivo si todavía no inició; si ya inició, registra el apoyo real. | Mark guidelines, stabilize the paper, or let the child direct the adult. Change the objective if the session has not started; otherwise record the actual support. | No valorar precisión si el adulto creó los pliegues. / Do not rate folding accuracy if the adult made the folds. |
| Un niño no quiere participar / A child does not want to participate | Ofrece observar, dibujar o retirarse. Confirma no participación al cierre. | Offer observing, drawing, or opting out. Confirm nonparticipation at close. | No exposición ni valoración principal si no participó. / No exposure or primary rating when the child did not participate. |
| Los niños compiten por la carga / Children compete for the load | Recuerda que se comparan formas y que cada niño tendrá su propia prueba. Mantén el orden visible; solo el niño del turno añade carga. | Remind them that shapes are compared and every child will run an individual test. Keep the order visible; only the child whose turn it is adds load. | No interpretar conflicto como habilidad o interés. / Do not interpret conflict as skill or interest. |

## 12. Adaptaciones y extensiones aprobadas

Cuando esta versión llegue a `published`, la IA podrá elegir únicamente estas opciones sin crear una nueva versión. No puede combinar opciones que cambien simultáneamente más de una variable de prueba. Mientras permanezca `draft`, ninguna opción está disponible para recomendación familiar.

Once this version reaches `published`, AI may choose only these options without creating a new version. It may not combine options that change more than one test variable at the same time. While it remains `draft`, no option is available for family recommendation.

| ID / type | Condición / Condition | Cambio / Change | Límite / Limit | `safetyImpact` | Adult confirmation |
|---|---|---|---|---|---:|
| `ADAPT-BRIDGE-NARRATIVE` / `presentation` | Interés narrativo / Narrative interest | Presentar que el puente cruza un río imaginario. / Frame the bridge as crossing an imaginary river. | No añadir juguetes, cambiar materiales, puntuación ni seguridad. / Do not add toys or change materials, scoring, or safety. | `none` | No |
| `ADAPT-BRIDGE-VISUAL-SEQUENCE` / `simplification` | L1 o dificultad para secuenciar / L1 or sequencing difficulty | Usar diagrama y marcar guías cada 2.5 cm / 1 in. / Use the diagram and mark guides every 2.5 cm / 1 in. | Si el adulto pliega, `OBJ-02` deja de ser evaluable. / If the adult folds, `OBJ-02` is no longer assessable. | `none` | Sí / Yes |
| `ADAPT-BRIDGE-MOTOR-ACCESS` / `role` | Fatiga o acceso motor / Fatigue or motor access | El adulto estabiliza el papel; el niño presiona con la palma o dirige hablando o señalando. / The adult stabilizes the paper; the child presses with a palm or directs by speaking or pointing. | Registrar apoyo y reasignar el objetivo antes de iniciar si hace falta. / Record support and reassign the objective before starting if needed. | `reduced` | Sí / Yes |
| `ADAPT-BRIDGE-LANGUAGE-ACCESS` / `presentation` | Lenguaje expresivo emergente / Emerging expressive language | Permitir señalar, usar tarjetas más/menos/igual o responder con gesto. / Allow pointing, more/less/same cards, or gestures. | `OBJ-06` requiere una afirmación comunicada por cualquier modalidad, no una frase hablada. / `OBJ-06` requires a communicated claim in any mode, not a spoken sentence. | `none` | No |
| `ADAPT-BRIDGE-COUNT-GROUPS` / `simplification` | Se pierde el total / Count is lost | Alinear fuera del vaso los crayones ya retirados en grupos visuales de cinco después de cada prueba. / After each test, align removed crayons outside the cup in visual groups of five. | Durante la prueba entra uno por vez; registrar el apoyo y nunca retirar una carga parcial para agrupar. / During a test, one enters at a time; record support and never remove a partial load to group it. | `none` | No |
| `ADAPT-BRIDGE-DIFFICULTY` / `difficulty` | Evidencia inicial o fuerte / Initial or strong evidence | Medir ancho de pliegue, justificar una variable controlada o repetir el mejor diseño. / Measure fold width, justify a controlled variable, or repeat the best design. | No añadir peso, altura, adhesivos, separación ni riesgo. / Do not add weight, height, adhesives, gap, or risk. | `none` | Sí / Yes |
| `ADAPT-BRIDGE-PAUSE` / `duration` | Necesidad de pausa / A pause is needed | Pausar después de una fase, fotografiar solo el montaje si el adulto elige o anotar resultados, y etiquetar materiales. / Pause after a stage, photograph only the setup if the adult chooses or write results, and label materials. | Al volver repetir `STEP-04`; la foto no se guarda por defecto. / On return repeat `STEP-04`; the photo is not saved by default. | `none` | Sí / Yes |
| `ADAPT-BRIDGE-MATERIAL` / `material` | Falta papel, soporte, regla, utensilio de escritura, cinta o toalla canónicos / Canonical paper, support, ruler, writing tool, tape, or towel is unavailable | Usar solo la sustitución expresa de la fila correspondiente en 5.1. / Use only the explicit substitute in that material's row in 5.1. | No sustituir vaso ni carga; usar un solo tipo de papel y soporte durante la sesión. / Do not replace cup or load; use one paper and support type throughout the session. | `reviewed_equivalent` | Sí / Yes |
| `ADAPT-BRIDGE-REPEAT` / `extension` | Ruta de 60 min y una o dos participantes / 60-minute path with one or two participants | Usar una hoja canónica no asignada para repetir la mejora y explorar repetibilidad. / Use an unassigned canonical sheet to repeat the improvement and explore repeatability. | No añadir una séptima hoja con tres participantes; máximo 20 crayones por prueba. / Do not add a seventh sheet with three participants; no more than 20 crayons per test. | `none` | Sí / Yes |

### 12.1 Adaptaciones prohibidas

- Aumentar la carga por encima de los 20 crayones canónicos o usar otro objeto. / Increase the load beyond the 20 canonical crayons or use another object.
- Elevar soportes, apilar libros o probar sobre un espacio abierto. / Raise supports, stack books, or test over an open space.
- Aumentar el espacio como respuesta automática a “demasiado fácil”. / Increase the gap as an automatic response to “too easy.”
- Mojar, calentar, cortar o perforar el papel. / Wet, heat, cut, or puncture the paper.
- Añadir cinta, pegamento, grapas, clips, cuerda o una segunda hoja a un diseño núcleo. / Add tape, glue, staples, clips, string, or a second sheet to a core design.
- Reemplazar vaso, soportes o carga fuera de las sustituciones expresas y gates aprobados. / Replace the cup, supports, or load outside explicit substitutions and approved gates.
- Pedir al niño que mueva libros o sostenga un soporte durante la carga. / Ask a child to move books or hold a support during loading.

## 13. Limpieza y almacenamiento / Cleanup and storage

### `STEP-08` — Desmontaje adulto / Adult teardown

- **Stage:** `cleanup`; **actor:** `adult`; **minutes:** 1 canónico; incluido en el presupuesto 2/3/4 de limpieza / canonical; included in the 2/3/4 cleanup budget.
- **Visual brief IDs:** ninguno / none.
- **Expected result / Resultado esperado:** vaso y crayones quedan sobre una zona despejada; los soportes se guardan sin intervención infantil. / The cup and crayons are on a clear area; supports are stored without child handling.
- **Success signal / Señal de éxito:** ningún niño mueve soportes ni permanece bajo el montaje. / No child moves supports or remains under the setup.
- **Resume / Reanudación:** si se interrumpe, dejar todo inmóvil hasta que vuelva el adulto. / If interrupted, leave everything stationary until the adult returns.
- **Warning / Advertencia:** el adulto retira primero vaso y carga, comprueba que no haya manos cerca y solo entonces mueve los soportes. / The adult first removes the cup and load, checks that no hands are nearby, and only then moves the supports.
- **Common problem / Problema común:** un crayón cae; detener el desmontaje, esperar que todo quede quieto y recogerlo antes de mover libros. / A crayon falls; stop teardown, wait until everything is still, and collect it before moving books.
- **`es-US`:** Retira el vaso, vacía los crayones sobre una zona despejada y guarda los dos soportes.
- **`en-US`:** Remove the cup, empty the crayons onto a clear area, and store both supports.

### `STEP-09` — Limpieza grupal / Group cleanup

- **Stage:** `cleanup`; **actor:** `group`; **minutes:** 2 canónicos; 1/2/3 por ruta / canonical; 1/2/3 by path.
- **Visual brief IDs:** ninguno / none.
- **Expected result / Resultado esperado:** los 20 crayones están contabilizados y el área queda seca y despejada. / All 20 crayons are accounted for and the area is dry and clear.
- **Success signal / Señal de éxito:** no quedan piezas, marcas húmedas ni obstáculos en mesa o zona de paso. / No pieces, wet marks, or obstacles remain on the table or walkway.
- **Resume / Reanudación:** comenzar de nuevo por contar los 20 crayones. / Resume by recounting all 20 crayons.
- **Warning / Advertencia:** el adulto recoge y desecha fragmentos; los niños manipulan solo materiales intactos. / The adult collects and discards fragments; children handle intact materials only.
- **Common problem / Problema común:** falta un crayón; revisar vaso, toalla y suelo con los niños quietos. / A crayon is missing; check the cup, towel, and floor while children stay still.

**`es-US`**

1. Cuenten los 20 crayones y guárdenlos.
2. Los niños pueden apilar hojas y guardar materiales intactos; el adulto retira fragmentos.
3. Reciclen papel limpio según las reglas locales o conserven un diseño para explicarlo más tarde.
4. Limpien marcas lavables y dejen la zona de paso despejada.

**`en-US`**

1. Count and store all 20 crayons.
2. Children may stack sheets and store intact materials; the adult removes fragments.
3. Recycle clean paper according to local rules or keep one design to explain later.
4. Wipe away washable marks and leave the walkway clear.

## 14. Cierre y evidencia

### 14.1 Camino predeterminado

Al cerrar, mostrar solo a los niños que participaron. Para cada uno, formular la pregunta correspondiente a su único objetivo principal y ofrecer un toque 1–5. El camino predeterminado no evalúa todas las exposiciones. **Evaluar más / Evaluate more** permanece secundario. Una sola nota de voz o texto para toda la sesión es opcional.

Si el objetivo no pudo observarse, usar **No se pudo observar / Could not observe**. Esto no equivale a 1. Un problema de montaje se registra como contexto, no como dificultad del niño.

El adulto puede omitir el cierre, completarlo después, corregir una respuesta o eliminar la observación. Omitir no crea evidencia negativa. / The adult may skip the close, complete it later, correct an answer, or delete the observation. Skipping does not create negative evidence.

### 14.2 Anclas 1–5 bilingües

| Valor | `es-US` | `en-US` |
|---:|---|---|
| 1 | No pudo hacerlo todavía, incluso con apoyo razonable. | Could not do it yet, even with reasonable support. |
| 2 | Lo logró con bastante ayuda. | Did it with substantial help. |
| 3 | Lo logró con alguna ayuda. | Did it with some help. |
| 4 | Lo logró casi sin ayuda. | Did it almost independently. |
| 5 | Lo hizo sin ayuda y de forma segura. | Did it independently and safely. |

La escala describe independencia en esta acción y contexto; no mide inteligencia, valor ni un nivel global.

### 14.3 Rúbricas por objetivo

#### `ACT-0001-OBJ-01` — Correspondencia uno a uno

- **Pregunta `es-US`:** “¿Qué tan independientemente pudo [nombre] añadir un crayón a la vez y mantener el conteo?”
- **Question `en-US`:** “How independently could [name] add one crayon at a time and keep track of the count?”
- **Cuenta como evidencia / Counts as evidence:** una pieza por turno, total contado o recuperado, resultado comunicado. / One item per turn, a count maintained or recovered, and a communicated result.
- **No cuenta / Does not count:** recitar números sin corresponderlos a piezas; el adulto añade y cuenta; exposición pasiva. / Reciting numbers without matching them to items; the adult adding and counting; passive exposure.
- **Factores externos / External factors:** piezas que caen, interrupción de otro niño, reinicio no señalado, dificultad auditiva o de habla no acomodada. / Falling items, another child's interruption, an unmarked restart, or unaccommodated hearing or speech access.

#### `ACT-0001-OBJ-02` — Secuencia de plegado

- **Pregunta `es-US`:** “¿Qué tan independientemente pudo [nombre] seguir la secuencia de pliegues y colocar la estructura?”
- **Question `en-US`:** “How independently could [name] follow the folding sequence and place the structure?”
- **Cuenta como evidencia / Counts as evidence:** alterna orientación, continúa la secuencia y coloca crestas en dirección del espacio con el apoyo registrado. / Alternates orientation, continues the sequence, and places ridges toward the gap with recorded support.
- **No cuenta / Does not count:** el adulto completa los pliegues; valorar solo la apariencia final; confundir precisión motora con comprensión de la secuencia. / The adult completes the folds; rating only final appearance; confusing motor precision with sequence understanding.
- **Factores externos / External factors:** papel dañado, líneas poco visibles, fatiga o adaptación motora. / Damaged paper, hard-to-see lines, fatigue, or a motor adaptation.

#### `ACT-0001-OBJ-03` — Comparar resultados

- **Pregunta `es-US`:** “¿Qué tan independientemente pudo [nombre] usar los resultados para decir qué diseño sostuvo más, menos o lo mismo?”
- **Question `en-US`:** “How independently could [name] use the results to say which design held more, less, or the same?”
- **Cuenta como evidencia / Counts as evidence:** compara los dos números, colecciones o marcas mediante palabra, gesto o selección visual. / Compares two numbers, collections, or marks using words, gestures, or a visual choice.
- **No cuenta / Does not count:** elegir el diseño preferido sin usar resultados; repetir la respuesta de otra persona sin indicio de comparación. / Choosing a preferred design without results; repeating another person's answer without evidence of comparison.
- **Factores externos / External factors:** resultado perdido, pruebas no comparables, símbolos de registro inaccesibles. / A lost result, noncomparable tests, or inaccessible recording symbols.

#### `ACT-0001-OBJ-04` — Prueba justa

- **Pregunta `es-US`:** “¿Qué tan independientemente pudo [nombre] ayudar a mantener iguales la separación, el vaso y la forma de añadir la carga?”
- **Question `en-US`:** “How independently could [name] help keep the gap, cup, and loading method the same?”
- **Cuenta como evidencia / Counts as evidence:** recuerda o comprueba al menos dos condiciones y solicita corregir una que cambió. / Remembers or checks at least two conditions and asks to correct one that changed.
- **No cuenta / Does not count:** observar al adulto preparar todo; afirmar que fue justo sin identificar condiciones. / Watching the adult prepare everything; saying it was fair without identifying conditions.
- **Factores externos / External factors:** el adulto reinicia sin involucrar al niño, marcas ausentes, cambio accidental de material. / The adult resets without involving the child, position marks are absent, or material changes accidentally.

#### `ACT-0001-OBJ-05` — Diseñar una mejora

- **Pregunta `es-US`:** “¿Qué tan independientemente pudo [nombre] proponer un cambio de forma, construirlo y probarlo?”
- **Question `en-US`:** “How independently could [name] propose a shape change, build it, and test it?”
- **Cuenta como evidencia / Counts as evidence:** elige un cambio específico, participa en construirlo y usa la prueba para saber qué ocurrió. / Chooses a specific change, participates in building it, and uses the test to learn what happened.
- **No cuenta / Does not count:** decorar sin cambiar estructura; el adulto elige y construye; exigir que el resultado supere al anterior. / Decorating without structural change; the adult choosing and building; requiring the result to beat the prior one.
- **Factores externos / External factors:** falta de hoja, tiempo insuficiente, dificultad motora no acomodada, conflicto de turno. / Missing paper, insufficient time, unaccommodated motor access, or a turn conflict.

#### `ACT-0001-OBJ-06` — Explicar con evidencia

- **Pregunta `es-US`:** “¿Qué tan independientemente pudo [nombre] usar algo que vio o contó para explicar una idea sobre el puente?”
- **Question `en-US`:** “How independently could [name] use something they saw or counted to explain an idea about the bridge?”
- **Cuenta como evidencia / Counts as evidence:** comunica una afirmación y la relaciona con una observación o resultado, por voz, gesto, dibujo o selección accesible. / Communicates a claim and links it to an observation or result through voice, gesture, drawing, or an accessible choice.
- **No cuenta / Does not count:** memorizar la explicación adulta; nombrar el diseño sin evidencia; exigir causalidad científica completa. / Memorizing the adult explanation; naming a design without evidence; requiring complete scientific causality.
- **Factores externos / External factors:** pregunta dirigida, falta de tiempo, lenguaje no acomodado, otro niño responde primero. / A leading question, lack of time, unaccommodated language access, or another child answering first.

### 14.4 Nota opcional y normalización

Ejemplo de nota `es-US`: “A Maya se le hacía difícil plegar, pero señaló que debíamos poner el vaso en el mismo lugar. Leo contó solo hasta doce y después pidió ayuda”.

Example note `en-US`: “Folding was difficult for Maya, but she pointed out that we should put the cup in the same place. Leo counted independently to twelve and then asked for help.”

La normalización puede proponer dos observaciones separadas y contextuales. No debe convertirlas en “Maya es lógica” o “Leo tiene nivel bajo”. La transcripción se puede editar; la atribución ambigua requiere confirmación. El audio se elimina tras transcripción exitosa o al vencer su máximo operativo, y la transcripción editable expira según la política vigente.

Normalization may propose two separate contextual observations. It must not turn them into “Maya is logical” or “Leo is low level.” The transcript is editable; ambiguous attribution requires confirmation. Audio is deleted after successful transcription or its operational maximum, and the editable transcript expires under the current policy.

## 15. Recursos visuales requeridos

Todos los assets permanecen en estado `planned` hasta generación, QA automático y aprobación humana. El texto y las cifras se renderizan como capas controladas; no forman parte de la imagen generada. Ningún asset muestra rostros, marcas comerciales ni información identificable.

| Asset ID | Tipo/estilo | Paso/propósito | Brief canónico | Requerido / prohibido | Alt text `es-US` | Alt text `en-US` |
|---|---|---|---|---|---|---|
| `VIS-01` | Materials board fotorealista | Lista de materiales | Vista cenital sobre fondo neutro: seis hojas carta o A4 apiladas, dos libros de tapa dura separados, vaso de papel vacío, 20 crayones intactos ordenados, regla, lápiz, toalla extendida y, en un recuadro separado, cuatro trozos de cinta removible con overlay “Opcional / Optional” | Mostrar cantidades comprobables y solo materiales de esta versión; distinguir la cinta opcional; sin texto generado dentro de la imagen, sustituciones de carga, tijeras, vidrio o manos infantiles | Materiales requeridos del puente de papel y cinta opcional ordenados desde arriba. | Required paper bridge materials and optional tape arranged from above. |
| `VIS-02` | Preparación fotorealista | Preparación/Discover | Mesa baja y firme; toalla bajo un espacio entre dos libros planos; regla mostrando la separación; hoja plana apoyada sobre ambos; manos adultas ajustando un libro | Mostrar 15 cm / 6 in mediante overlay; actor adulto; sin libros apilados ni vaso cargado | Un adulto ajusta dos libros planos separados por 15 centímetros, con una toalla debajo y una hoja cruzando el espacio. | An adult adjusts two flat books 6 inches apart, with a towel underneath and a sheet crossing the gap. |
| `VIS-03` | Diagrama instructivo, 6 paneles | Imagine/Build | Tres opciones aprobadas —acordeón, canal y pliegues anchos— seguidas por la secuencia del acordeón: primer pliegue de 2.5 cm / 1 in, voltear/repetir y abrir con crestas longitudinales | Presentar opciones, no una respuesta correcta; flechas y números como overlays; sin tijeras, cinta o manos adult-only falsas | Opciones de forma y pasos para doblar una hoja en acordeón con crestas a lo largo. | Shape options and steps for accordion-folding a sheet with lengthwise ridges. |
| `VIS-04` | Diagrama instructivo | Experiment | Vaso centrado sobre puente bajo; una mano infantil baja suavemente un crayón dentro del vaso; 19 restantes en una fila; toalla bajo el espacio; libros planos | Mostrar solo acción infantil permitida; el crayón no cae; sin caras, cargas sustitutas o manos bajo soportes | Una mano baja un crayón dentro del vaso centrado sobre el puente, con una toalla debajo. | A hand lowers one crayon into the cup centered on the bridge, with a towel underneath. |
| `VIS-05` | Resultado esperado fotorealista, secuencia de 4 paneles | Experiment/Explain | El mismo montaje, cámara y vaso muestran referencia plana y tres formas infantiles distintas, una por vez; cada panel tiene espacio externo para símbolo/nombre y resultado, sin número generado dentro de la imagen | Overlay “Mismo montaje; un turno por diseño; los resultados pueden variar / Same setup; one turn per design; results may vary”; no duplicar soportes, prometer superioridad ni mostrar física imposible | Cuatro turnos del mismo montaje muestran una referencia plana y tres diseños infantiles probados por separado. | Four turns on the same setup show a flat baseline and three child designs tested separately. |
| `VIS-06` | Diagrama conceptual, no a escala | Explicación | Cortes transversales: hoja plana y hoja con crestas; flechas de carga hacia abajo; pequeñas paredes verticales resaltadas | Marcar “diagrama, no a escala”; overlays bilingües separados; sin ecuaciones requeridas | Diagrama no a escala compara una hoja plana con crestas que forman pequeñas paredes bajo una carga. | Not-to-scale diagram compares a flat sheet with ridges that form small walls under a load. |
| `VIS-07` | Troubleshooting, diagrama comparativo | Fallas | Tres paneles: montaje válido; `invalid_setup` con soporte desplazado o vaso inicialmente descentrado; `bridge_deformation` con papel curvado antes de inclinarse el vaso | Cruz/check y etiquetas como overlays controlados; no mostrar caída cerca de un niño ni sugerir reinicio automático | Comparación entre montaje válido, montaje inválido y deformación del puente. | Comparison of a valid setup, an invalid setup, and bridge deformation. |
| `VIS-08` | Diagrama instructivo | Improve | Cuatro opciones separadas: pliegues más anchos, más estrechos, guías rectas y bordes largos elevados; cada una usa una sola hoja | Presentar como opciones, no como resultados garantizados; sin combinarlas en un diseño | Cuatro cambios de forma aprobados para probar una mejora con una sola hoja. | Four approved shape changes for testing an improvement with one sheet. |

### 15.1 Checklist de QA visual específico

- El conteo automático confirma seis hojas y 20 crayones en `VIS-01`.
- Los libros están planos y el espacio está sobre una mesa en todos los montajes.
- Las crestas cruzan de un soporte al otro; no atraviesan lateralmente el espacio.
- El vaso aparece vacío al inicio y recibe solo la carga aprobada.
- Ninguna imagen añade adhesivos, clips, monedas, vidrio o peso no permitido.
- `VIS-05` se valida como resultado posible, no como garantía.
- Los bundles usan el mismo asset físico cuando corresponde y overlays/alt text revisados por idioma.
- `VIS-05` se interpreta como dos momentos secuenciales del mismo set de materiales, nunca como dos montajes simultáneos.
- `VIS-07` diferencia visualmente `invalid_setup` de `bridge_deformation` sin atribuir una causa que la imagen no permita verificar.
- Se registra modelo/proveedor, brief, resultado de QA, aprobador, fecha y vínculo a `ACT-0001@0.3.0`.

## 16. Criterios de aceptación de la versión

- Un adulto puede preparar el montaje únicamente con la lista y `VIS-01`/`VIS-02`.
- Las rutas de 30, 45 y 60 minutos conservan Discover–Imagine–Build–Experiment–Improve–Explain.
- Las configuraciones de uno, dos y tres niños asignan exactamente un objetivo principal y permiten que cada participante proponga, construya, pruebe, observe y recomiende una mejora.
- El flujo de cierre necesita un toque por participante y puede completarse en menos de 20 segundos para tres niños en prueba de usabilidad.
- Se pueden registrar exposiciones sin convertirlas en evidencia de independencia.
- `invalid_setup`, `bridge_deformation` y `safe_stop` producen estados distintos; solo una prueba válida produce puntuación y ninguno produce por sí mismo una valoración negativa del niño.
- La actividad se puede ejecutar sin tijeras, monedas, adhesivos en el puente ni conexión de red.
- El vaso y la carga no tienen sustituciones en 0.3.0; cualquier alternativa se rechaza o crea una nueva versión después de validación.
- Ninguna adaptación aprobada aumenta altura, energía, peso, temperatura, presión, toxicidad o velocidad.
- Los bundles `es-US` y `en-US` comunican el mismo mecanismo y controles de seguridad.
- Cada `STEP-00`–`STEP-09` declara actor, stage, tiempo, estado de entrada/salida, resultado esperado, señal de éxito, reanudación, advertencia y problema común; las referencias cumplen el mapping de 1.2.
- La salida de cada fase coincide con la entrada de la siguiente y el walkthrough de mesa confirma la función de vaso/crayones y una prueba propia por niño.
- Una instancia JSON de 0.3.0 valida contra el schema vigente antes de `ready_for_pilot`.
- Un resultado igual o contrario a la expectativa sigue siendo válido y no se reemplaza por una conclusión garantizada.

## 17. Trazabilidad

| Regla de esta ActivityVersion | Principios y requisitos fuente | Verificación prevista |
|---|---|---|
| Biblioteca versionada y no publicable sin gates | P-03, P-14, ACT-001, ACT-002, ACT-006, ACT-007 | Estado, review records y referencia exacta de sesión |
| Una hoja, misma separación y misma carga | P-01, LRN-001, ACT-003 | Ejecución observada y checklist de prueba justa |
| Roles significativos 1–3 niños | P-05, ACT-004, ACT-008 | Pilotos individual, dos niños y tres niños |
| Un objetivo por niño; otras habilidades como exposición | P-06, LRN-006, EVD-001, EVD-002 | Restricción de asignación y cierre cronometrado |
| Escala contextual y omisión | P-07, EVD-003, EVD-004, EVD-010 | Prueba de UI y auditoría de observaciones |
| Sustituciones y extensiones cerradas | P-10, ACT-005, SAFE-004 | Pruebas de adaptación y rechazo de opciones prohibidas |
| Pasos adultos inmutables | P-11, SAFE-003, SAFE-006 | Render bilingüe y prueba de recomendador |
| Falla de prueba clasificada sin inferencia infantil | P-07, EVD-004, SAFE-002, SAFE-006 | Casos `invalid_setup`, `bridge_deformation` y `safe_stop` |
| Imágenes versionadas y revisadas | ACT-010, ACT-VIS-001 a ACT-VIS-004 | QA automático + revisión humana |
| Localización completa | ACT-011, ACT-012 | Revisión bilingüe específica |

## 18. Registro de cambios

| Versión | Estado | Cambios |
|---|---|---|
| 0.1.0 | Draft histórico | Esqueleto inicial para validar el esquema. |
| 0.2.0 | Draft histórico | Amplía a ActivityVersion editorial bilingüe; fija materiales y prueba; documenta rutas de 30–60 minutos, configuraciones 1–3, roles, objetivos/rúbricas, seguridad, adaptaciones, troubleshooting, cierre y briefs visuales. Cambia la carga de monedas/bloques ambiguos a crayones intactos en vaso liviano y limita esta versión a tres niños hasta validación. |
| 0.2.1 | Draft histórico | Retira sustituciones no validadas de vaso y carga; distingue `invalid_setup`, `bridge_deformation` y `safe_stop`; estructura `STEP-00`–`STEP-09`; completa campos bilingües de materiales, roles, peligros y adaptaciones; alinea IDs con el schema; corrige tolerancias y briefs visuales; añade gate científico y gate físico de vaso/carga. |
| 0.2.2 | Draft histórico | Añade una guía bilingüe y práctica para que el adulto pueda proponer pliegues, canales y preguntas de diseño sin entregar la solución ni prometer que una forma será superior. |
| 0.3.0 | Draft actual | Reescribe la actividad desde un contrato narrativo causal: prueba de referencia real en Discover, función explícita del vaso y los crayones, diseño y prueba propios por niño, mejora grupal, transiciones verificables y focos calibrados por edad/evidencia. |

## 19. Evidencia requerida antes de cambiar a `ready_for_pilot`

1. **Gate físico de vaso y carga:** ejecutar al menos diez ciclos adultos completos con el mismo tipo de vaso y set canónico de 20 crayones; registrar masa aproximada, dimensiones del vaso, estabilidad vacía, estabilidad progresiva, forma de colocación y causa de cada falla. El protocolo solo avanza si dos revisores pueden distinguir consistentemente `invalid_setup` de `bridge_deformation`; si no, se cambia recipiente/protocolo y se crea otra versión.
2. Probar explícitamente carga descentrada, crayón soltado, soporte movido, apoyo desigual, inclinación por deformación y colapso sobre la toalla; confirmar que cada caso llega al estado correcto sin producir evidencia infantil.
3. Ejecutar con papel carta y A4 comunes y documentar si 15 cm / 6 in produce al menos dos pruebas comparables sin carga sustituta ni aumento del espacio.
4. Verificar que vaso y 20 crayones permanecen dentro del perfil de falla segura sobre la mesa baja; cualquier rotura, rebote fuera de la mesa o necesidad de mayor carga bloquea la versión.
5. Cronometrar rutas y preparación con un adulto distinto al autor, y cronometrar limpieza por separado.
6. Ejecutar walkthrough de mesa y validar continuidad, espera y una prueba propia completa con uno, dos y tres niños; ningún paso puede requerir inventar la función de un material o la transición.
7. Confirmar que las preguntas de cierre distinguen apoyo, `invalid_setup`, `bridge_deformation`, `safe_stop` y no observación.
8. Serializar `ACT-0001@0.3.0` y validar todos sus IDs, campos localizados, narrativa y referencias contra el schema vigente.
9. Completar y registrar revisión científica, pedagógica, de seguridad y bilingüe.
10. Generar los ocho assets y completar QA; no usar imágenes familiares sin consentimiento separado.

Las pruebas familiares adicionales pertenecen al estado `family_pilot` y son requisito posterior para `published`; no se confunden con la evidencia anterior necesaria para entrar a `ready_for_pilot`.
