# ACT-0003 — Probador de conductividad / Conductivity Tester

**Estado:** Draft — no entregable a familias<br>
**Versión:** 0.1.1<br>
**Idioma fuente:** Español (`es-US`)<br>
**Bundles requeridos:** `es-US`, `en-US`<br>
**Autoría:** Equipo del proyecto; borrador asistido por IA<br>
**Responsable editorial propuesto:** Equipo fundador/Contenido<br>
**Revisiones registradas:** Ninguna; pendientes revisión pedagógica, eléctrica/seguridad, bilingüe y prueba familiar

## 1. Identidad editorial

| Campo | Valor |
|---|---|
| `activity_id` | `ACT-0003` |
| `version` | `0.1.1` |
| `status` | `draft` |
| `slug` | `probador-conductividad` |
| Título `es-US` | Probador de conductividad |
| Título `en-US` | Conductivity Tester |
| Resumen `es-US` | Construyan un probador de baja tensión y úselo para descubrir qué objetos secos completan un circuito. |
| Summary `en-US` | Build a low-voltage tester and use it to discover which dry objects complete a circuit. |
| Duración familiar | 35–50 minutos; hasta 60 minutos con extensión aprobada |
| Preparación adulta | 10–15 minutos antes de invitar a los niños; no cuenta dentro de la duración familiar |
| Participantes | 1–3 niños y al menos un adulto supervisor |
| Edad orientativa | 5–10 años |
| Niveles funcionales | L1–L3; extensión L4 mediante explicación y control de variables |
| Prerrequisitos infantiles | Ninguno; leer, escribir o montar componentes no es requisito. |
| Child prerequisites | None; reading, writing, and assembling components are not required. |
| Prerrequisito adulto | Poder verificar etiquetas y polaridad y seguir el montaje exacto publicado. Si no puede hacerlo, debe usar la configuración preensamblada que resulte seleccionada o elegir otra actividad. |
| Adult prerequisite | Ability to verify labels and polarity and follow the exact published setup. Otherwise, use the selected preassembled configuration or choose another activity. |
| Nivel de seguridad | C: el adulto prepara, inserta/retira pilas y mantiene las uniones fijas; los niños participan con ayuda cercana en la prueba |
| Desorden | Bajo |
| Espacio | Mesa seca, despejada y bien iluminada, lejos de cocina, baño, fregadero y enchufes |
| Dependencia externa | Ninguna durante la sesión; el paquete completo puede ejecutarse offline |

### Estado editorial y límites de uso

Esta versión es un borrador para revisión y piloto. No cumple todavía los gates de publicación de `ACT-002`, `SAFE-001` ni los criterios de ejecución familiar independiente. Ningún sistema debe recomendarla como actividad publicada.

### Registro de cambios

| Versión | Fecha | Cambio | Autor |
|---|---|---|---|
| 0.1.0 | 15 de agosto de 2026 | Primera ActivityVersion bilingüe: circuito de 2 pilas AA, LED rojo y resistencia de 330 Ω; roles para 1–3 niños; evaluación, seguridad y briefs visuales. | Equipo del proyecto; borrador asistido por IA |
| 0.1.1 | 15 de agosto de 2026 | Correcciones de revisión cruzada: retención mecánica, localización completa, tiempos, cálculo con tolerancia, evidencia justa, seguridad, campos estructurados y gates A/B. | Equipo del proyecto; revisión cruzada asistida por IA |

### Review records

| Gate | Revisor | Estado | Fecha | Hallazgos |
|---|---|---|---|---|
| Pedagogía | Por asignar | Pendiente | — | — |
| Electricidad y seguridad | Por asignar | Pendiente | — | Debe incluir montaje, componentes exactos, retención mecánica y falla segura. |
| Localización `es-US` | Por asignar | Pendiente | — | — |
| Localización `en-US` | Por asignar | Pendiente | — | — |
| Visual y accesibilidad | Por asignar | Pendiente | — | — |
| Piloto familiar | Por asignar | Pendiente | — | — |

## 2. Propósito educativo

### Pregunta central

- **es-US:** ¿Qué objetos secos dejan pasar suficiente corriente para encender nuestro LED?
- **en-US:** Which dry objects let enough current pass to light our LED?

### Decisión real del niño

Cada niño predice qué objetos completarán el circuito, decide un orden de prueba o propone una forma más consistente de hacer contacto. El resultado no está dado de antemano y una predicción diferente no se considera un error.

### Áreas y conceptos

| Tipo | Contenido |
|---|---|
| Área principal | `ELE` Electricidad |
| Áreas secundarias | `LOG` pensamiento lógico, `MAT` clasificación/registro, `COM` explicación, `PRA` organización segura |
| Conceptos principales | circuito cerrado y abierto; conductor y aislante en el contexto del probador; polaridad del LED; resistencia limitadora de corriente |
| Conceptos secundarios | prueba justa; contacto eléctrico; evidencia incierta; materiales y recubrimientos |

### Habilidades observables

| Código local | Habilidad observable | Ejemplo de evidencia contextual |
|---|---|---|
| `ELE-CLOSE-PATH` | Identificar o construir una trayectoria continua en un circuito simple. | Señala el recorrido batería → resistencia → LED → objeto → batería y encuentra una separación que impide encender el LED. |
| `ELE-SEQUENCE-TEST` | Ejecutar una secuencia de prueba segura y consistente. | Mantiene el interruptor apagado al cambiar objetos, separa las pinzas, coloca un objeto y luego enciende para observar. |
| `LOG-CLASSIFY-EVIDENCE` | Clasificar objetos según un resultado observado. | Coloca cada objeto en “encendió”, “no encendió” o “resultado incierto” después de probarlo. |
| `LOG-CONTROL-VARIABLE` | Mantener constantes las condiciones relevantes al comparar. | Usa el mismo probador, posición de contacto y tiempo de observación para cada objeto. |
| `COM-EXPLAIN-CIRCUIT` | Explicar una conclusión usando observación y mecanismo. | Dice que el metal completó la trayectoria y por eso el LED encendió, sin afirmar que todos los metales siempre producirán el mismo brillo. |
| `MAT-RECORD-RESULT` | Registrar y comparar resultados categóricos. | Marca una predicción y el resultado de cada objeto sin perder la correspondencia. |

La presencia de estas habilidades en la actividad constituye exposición. Solo la habilidad elegida como objetivo principal de cada niño se evalúa por defecto.

## 3. Resultado esperado y precisión científica

El LED debe encender cuando las dos pinzas de prueba tienen contacto limpio con un material de resistencia suficientemente baja, como la cuchara metálica o el papel aluminio. Debe permanecer apagado con los objetos secos de plástico, madera, cartón, goma/silicona y tela incluidos.

Este montaje es un **probador cualitativo**, no un medidor de conductividad. “LED apagado” significa “no pasó suficiente corriente para encender este LED en estas condiciones”; no demuestra de manera absoluta que el material sea aislante. La suciedad, pintura, óxido, un recubrimiento, contacto deficiente, pilas débiles o un LED invertido pueden producir un falso resultado. Un brillo tenue se registra como `incierto` y se repite después de comprobar el control cerrado.

## 4. Materiales estructurados

### 4.1 Circuito — exactamente una de dos configuraciones candidatas

Ninguna configuración está seleccionada como preferida en este borrador. Antes de pasar a `pedagogical_review`, el gate eléctrico y mecánico debe escoger A o B, documentar por qué es la alternativa de menor riesgo que conserva el aprendizaje y retirar la otra de las instrucciones familiares de esa versión.

#### Configuración A — componentes visibles, candidata

| ID | Cantidad | Material `es-US` | Material `en-US` | Especificación y control `es-US` | Specification and control `en-US` |
|---|---:|---|---|---|---|
| `circuit.holder-2aa` | 1 | Portapilas cerrado para 2 pilas AA, con interruptor y cables rojo/negro | Enclosed 2-AA battery holder with switch and red/black leads | Compartimento intacto; se prefiere tapa asegurada con tornillo; solo 3 V nominales; el adulto inserta y retira las pilas. | Intact compartment; a screw-secured cover is preferred; 3 V nominal only; the adult inserts and removes cells. |
| `circuit.cell-aa` | 2 | Pilas alcalinas AA | AA alkaline cells | Mismo tipo, marca y estado; nunca mezclar nuevas/usadas; nunca usar pilas dañadas, con fuga o recargables en esta versión. | Same type, brand, and condition; never mix new/used cells; never use damaged, leaking, or rechargeable cells in this version. |
| `circuit.led-red` | 1 | LED rojo de alta eficiencia, 5 mm | High-efficiency red 5 mm LED | LED discreto sin resistencia integrada; ánodo y cátodo identificables. El número de parte exacto y sus límites deben aprobarse antes de `review`; no sustituir por LED blanco/azul, tira ni bombilla. | Discrete LED without an integrated resistor; identifiable anode and cathode. The exact part number and ratings require approval before `review`; do not substitute a white/blue LED, strip, or bulb. |
| `circuit.resistor-330` | 1 | Resistencia de 330 Ω, 1/4 W, 5 % | 330 Ω, 1/4 W, 5% resistor | Obligatoria y siempre en serie. Debe venir etiquetada por el proveedor; el adulto no adivina el valor. | Required and always in series. It must be supplier-labeled; the adult does not guess its value. |
| `circuit.clip-lead` | 4 | Cables puente con pinzas cocodrilo pequeñas totalmente aisladas | Fully insulated small alligator-clip jumper leads | Fundas intactas y dientes sin bordes expuestos fuera de la mandíbula. Solo dos extremos quedan libres como pinzas de prueba. Requiere retención mecánica validada. | Intact boots and no exposed teeth outside the jaw. Only two ends remain free as test clips. Validated mechanical retention is required. |
| `circuit.insulation-tape` | 1 rollo | Cinta aislante eléctrica certificada | Listed electrical insulating tape | Solo el adulto cubre por separado las seis conexiones fijas y patas. La cinta no sustituye alivio de tensión ni repara aislamiento dañado. | The adult separately covers all six fixed joints and leads. Tape does not replace strain relief and must not repair damaged insulation. |

#### Configuración B — módulo preensamblado, candidata

Puede usarse un **módulo indicador LED rojo preensamblado (`circuit.module-led-3v`) y explícitamente especificado por su fabricante para 3 V DC, con limitación de corriente integrada**, conectado al mismo portapilas de 2 AA y a dos pinzas de prueba aisladas. El módulo debe tener polaridad marcada y conexiones cerradas, protegidas y con alivio de tensión. No se añade la resistencia externa si el módulo ya la integra. No se permite una pieza sin número de parte, ficha técnica o indicación clara de limitación de corriente.

**`en-US`:** A preassembled red LED indicator module (`circuit.module-led-3v`) explicitly manufacturer-rated for 3 V DC with integrated current limiting may connect to the same 2-AA holder and two insulated test clips. It must have marked polarity, enclosed or protected connections, and strain relief. Do not add the external resistor when current limiting is integrated. A module without a part number, datasheet, and stated current limiting is not allowed.

Las configuraciones A y B no se mezclan ni se improvisan. Esta versión no incluye soldadura, protoboard, fuente USB, pila rectangular de 9 V, batería recargable, pila tipo moneda ni conexión a corriente doméstica.

### 4.2 Objetos de prueba — secos y sueltos

| ID | Cantidad | Material `es-US` | Material `en-US` | Resultado probable | Control `es-US` / `en-US` |
|---|---:|---|---|---|---|
| `sample.spoon-steel` | 1 | Cuchara metálica de acero inoxidable, sin mango recubierto | Uncoated stainless-steel spoon | Encendió / Lit | Sin borde cortante; limpia y seca / No sharp edge; clean and dry. |
| `sample.foil` | 1 | Tira de papel aluminio, aprox. 5 × 15 cm / 2 × 6 in | Aluminum foil strip, about 5 × 15 cm / 2 × 6 in | Encendió / Lit | Doblar a cuatro capas para evitar rasgado o borde fino / Fold into four layers to prevent tearing or a thin edge. |
| `sample.ruler-plastic` | 1 | Regla plástica, aprox. 15–30 cm / 6–12 in | Plastic ruler, about 15–30 cm / 6–12 in | No encendió / Did not light | Sin partes metálicas / No metal parts. |
| `sample.stick-wood` | 1 | Palito de madera seco, sin astillas | Dry wooden craft stick with no splinters | No encendió / Did not light | El adulto inspecciona y descarta si tiene astillas / Adult inspects and discards it if splintered. |
| `sample.cardboard` | 1 | Tira de cartón seco, aprox. 5 × 15 cm / 2 × 6 in | Dry cardboard strip, about 5 × 15 cm / 2 × 6 in | No encendió / Did not light | Sin grapas, laminado metálico ni humedad / No staples, metallic laminate, or moisture. |
| `sample.spatula-silicone` | 1 | Espátula pequeña de silicona o goma, limpia y seca | Clean, dry silicone or rubber spatula | No encendió / Did not light | Sin núcleo metálico expuesto / No exposed metal core. |
| `sample.fabric-cotton` | 1 | Retazo de algodón, aprox. 10 × 10 cm / 4 × 4 in | Cotton fabric swatch, about 10 × 10 cm / 4 × 4 in | No encendió / Did not light | Totalmente seco y no deshilachado / Completely dry and not frayed. |
| `record.result-sheet` | 1 | Hoja de registro impresa o dibujada | Printed or hand-drawn result sheet | No aplica / N/A | Tres columnas: predicción, resultado, nota / Three columns: prediction, result, note. |
| `record.result-card` | 3 | Tarjetas grandes: “encendió”, “no encendió”, “incierto” | Large cards: “lit”, “did not light”, “uncertain” | No aplica / N/A | Texto e icono; no depender solo del color / Use text and icon; do not rely on color alone. |
| `record.pencil` | 1 | Lápiz o crayón | Pencil or crayon | No aplica / N/A | No se prueba como muestra / Never tested as a sample. |
| `visual.white-card` | 1 opcional | Tarjeta blanca mate | Matte white card | No aplica / N/A | Detrás del LED si cuesta verlo / Place behind the LED if visibility is poor. |

### 4.3 Estado estructurado de materiales

| Grupo/ID | Obligatorio | Ciclo | Sustituible | Preparación adulta |
|---|---|---|---|---|
| Configuración A: `circuit.holder-2aa`, `circuit.led-red`, `circuit.resistor-330`, `circuit.clip-lead` | Sí, solo si A resulta seleccionada | Reutilizable | No automático | Seleccionar número de parte, inspeccionar, montar, aislar y validar retención. |
| `circuit.cell-aa` | Sí, dos en A o B | Consumible/reemplazable | Solo dos AA alcalinas aprobadas | Insertar, retirar, contar y almacenar. |
| `circuit.insulation-tape` | Sí en A | Consumible | No | Aplicar por separado; reemplazar ante desprendimiento. |
| `circuit.module-led-3v` | Sí, solo si B resulta seleccionada | Reutilizable | No automático | Verificar ficha, polaridad, limitación y protección mecánica. |
| `sample.*` | Siete en recorrido completo; cuatro en adaptación breve | Reutilizable | Solo según 4.4 | Inspeccionar sequedad, tamaño, bordes, recubrimientos y ausencia de conexión externa. |
| `record.*` | Sí | Consumible o reutilizable según formato | Sí, por equivalente seguro | Preparar columnas, iconos e idioma. |
| `visual.white-card` | No | Reutilizable | Sí, por superficie blanca mate | Reservar si la iluminación dificulta ver el LED. |

### 4.4 Sustituciones prohibidas y aprobadas

- No sustituir la fuente, LED, valor de resistencia ni tipo de módulo sin crear una nueva revisión de seguridad.
- Un objeto de prueba puede sustituirse únicamente por otro objeto **grande, seco, suelto, no afilado, no electrónico, no conectado a nada, no alimentario y previamente aprobado por el adulto**. La sustitución se registra como exploración y no recibe resultado prometido.
- Nunca probar enchufes, tomacorrientes, interruptores de pared, cables instalados, cargadores, dispositivos, pantallas, electrodomésticos, juguetes eléctricos, baterías, vehículos, joyas valiosas, piel, personas, animales, boca, plantas, alimentos, polvos, objetos húmedos, líquidos, productos químicos ni objetos desconocidos.
- Nunca usar monedas como batería ni pilas de botón/tipo moneda como fuente o muestra.

**`en-US` non-negotiable substitutions and prohibitions:** Do not change the source, LED, resistor value, or module type without a new safety review. A sample may be replaced only by another large, dry, loose, blunt, nonelectronic, unpowered, nonfood object approved by the adult; no result is promised for a substitute. Never test an outlet, receptacle, wall switch, installed cable, charger, device, screen, appliance, powered toy, battery, vehicle, valuable jewelry, skin, person, animal, mouth, plant, food, powder, wet object, liquid, chemical, or unknown object. Never use a coin as a battery, and never use a button/coin cell as either the source or a sample.

## 5. Preparación exclusiva del adulto

Todos los puntos de esta sección son `adult-only`. Los niños pueden observar desde una distancia segura, pero no insertar pilas, seleccionar componentes al azar ni preparar uniones fijas.

1. **Preparar el espacio / Prepare the space.** Trabaje sobre una mesa seca y despejada, al menos a 1 m / 3 ft de enchufes, fregaderos, líquidos, alimentos y dispositivos. Retire cualquier objeto que no esté en la lista aprobada.
2. **Inspeccionar / Inspect.** Confirme que portapilas, cables, aislamiento, LED y resistencia no estén agrietados, calientes, corroídos, húmedos o dañados. Confirme la etiqueta `330 Ω`.
3. **Mantener sin energía / Keep power off.** Deje el interruptor en `OFF` y el portapilas vacío mientras conecta el circuito.
4. **Montar la trayectoria / Assemble the path.** Solo después de que A resulte seleccionada y exista un diagrama aprobado: cable 1 une rojo `+` a resistencia; cable 2 une resistencia a pata larga/ánodo; cable 3 une pata corta/cátodo y deja su otro extremo como pinza de prueba A; cable 4 deja un extremo como pinza de prueba B y une el otro a negro `−`. Las pinzas A/B quedan separadas. Cubra por separado las seis uniones fijas y todas las patas expuestas. Aplique el alivio de tensión exacto aprobado; la cinta sola no lo sustituye.
5. **Comprobar polaridad / Check polarity.** La pata larga del LED va hacia la resistencia y el cable rojo. La pata corta y el lado plano de la cápsula van hacia la pinza que finalmente regresa al cable negro. No energice un LED invertido para “ver qué pasa”.
6. **Insertar las pilas / Insert batteries.** Inserte dos pilas alcalinas AA siguiendo `+` y `−`; cierre y asegure la tapa. Mantenga todas las pilas sueltas fuera del alcance infantil.
7. **Prueba abierta / Open control.** Separe las pinzas, encienda durante 2 segundos y confirme que el LED permanece apagado. Apague.
8. **Prueba cerrada / Closed control.** Toque únicamente las mandíbulas de las dos pinzas de prueba entre sí, encienda durante 2 segundos y confirme que el LED enciende. Apague y vuelva a separarlas. La resistencia permanece siempre en el circuito.
9. **Revisar temperatura / Check temperature.** Nada debe sentirse caliente ni producir olor. Si el control falla o aparece calor, olor, humo, chispa, corrosión o fuga, apague solo si puede hacerlo sin acercarse ni tocar una parte peligrosa. Aleje a los niños. No abra el portapilas ni retire las pilas mientras el montaje esté caliente, humeando, chispeando o con fuga; siga la guía del fabricante y retire el montaje de servicio.
10. **Preparar objetos y registro / Set out samples and record sheet.** Confirme que todos los objetos estén secos, grandes y libres de partes peligrosas. Coloque las tres tarjetas de resultado.

### Lista de control antes de invitar a los niños

- [ ] Solo hay un portapilas de 2 AA; no hay pilas tipo moneda, fuente USB ni corriente doméstica.
- [ ] La resistencia de 330 Ω está conectada en serie y las uniones fijas están cubiertas.
- [ ] El montaje coincide con el diagrama de la configuración seleccionada; ningún componente se mueve, gira o expone metal fijo con una inspección manual suave del adulto.
- [ ] El control abierto apaga el LED y el control cerrado lo enciende.
- [ ] Los siete objetos de prueba están secos, sueltos y aprobados.
- [ ] El adulto puede alcanzar el interruptor en todo momento.
- [ ] La hoja de registro y los roles están listos.

### `en-US` adult-only preparation bundle

Every item below is `adult-only`. Children may watch from a safe distance, but they do not insert cells, select electrical components, or prepare fixed joints.

1. **Prepare the space.** Work on a dry, clear table at least 1 m / 3 ft from outlets, sinks, liquids, food, and devices. Remove every object that is not on the approved list.
2. **Inspect.** Confirm that the holder, leads, insulation, LED, and resistor are not cracked, warm, corroded, wet, or damaged. Confirm the `330 Ω` label.
3. **Keep power off.** Leave the switch `OFF` and the holder empty while assembling the circuit.
4. **Assemble the path.** Only after A is selected and an approved diagram exists: lead 1 joins red `+` to the resistor; lead 2 joins the resistor to the long LED lead/anode; lead 3 joins the short lead/cathode and leaves its other end as test clip A; lead 4 leaves one end as test clip B and joins its other end to black `−`. Keep A/B apart. Separately cover all six fixed joints and every exposed component lead. Apply the exact approved strain relief; tape alone is not strain relief.
5. **Check polarity.** The LED long lead faces the resistor and red lead. The short lead and flat side of the LED body face the clip that eventually returns to the black lead. Do not energize a reversed LED “to see what happens.”
6. **Insert the cells.** Insert two alkaline AA cells according to `+` and `−`; close and secure the cover. Keep all loose cells out of children's reach.
7. **Open control.** Keep the clips apart, switch on for 2 seconds, and confirm that the LED remains off. Switch off.
8. **Closed control.** Touch only the jaws of the two test clips together, switch on for 2 seconds, and confirm that the LED lights. Switch off and separate them. The resistor stays in the circuit at all times.
9. **Check temperature.** Nothing should feel warm or produce an odor. If a control fails or there is heat, odor, smoke, a spark, corrosion, or leakage, switch off only if this can be done without approaching or touching a hazard. Move children away. Do not open the holder or remove cells while the setup is hot, smoking, sparking, or leaking; follow the manufacturer guidance and retire the setup.
10. **Set out samples and record sheet.** Confirm that every sample is dry, large, and free of hazards. Set out all three result cards.

**Before children join:** confirm that the only source is the enclosed 2-AA holder; all fixed joints are covered and remain fixed during a gentle adult inspection; the setup matches the approved diagram; the open and closed controls work; all seven samples are dry, loose, and approved; the adult can reach the switch; and the record sheet and roles are ready.

## 6. Roles y asignación de objetivos

### 6.1 Plantillas de rol

| Rol | Contribución real | Responsabilidades | Objetivos principales elegibles | Exposiciones previstas | Pasos restringidos |
|---|---|---|---|---|---|
| **Investigador/a de materiales / Materials Investigator** | Decide qué probar y organiza la evidencia física. | Nombra, toca y observa objetos aprobados; hace predicciones; coloca cada objeto en la categoría observada. | `LOG-CLASSIFY-EVIDENCE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | materiales, conductor/aislante contextual, predicción, revisión de ideas | No inserta pilas ni toca uniones fijas; para 5–6 años el adulto opera las pinzas. |
| **Guardián/a del circuito / Circuit Keeper** | Mantiene la prueba segura y consistente. | Verifica `OFF` antes del cambio; indica la trayectoria; enciende solo cuando las pinzas están colocadas; confirma controles. | `ELE-SEQUENCE-TEST`, `ELE-CLOSE-PATH`, `LOG-CONTROL-VARIABLE` | polaridad, resistencia, circuito abierto/cerrado, turnos | No abre el portapilas, reconfigura componentes ni retira cinta. |
| **Ingeniero/a de evidencia / Evidence Engineer** | Hace comparable cada prueba y conserva resultados. | Ayuda a colocar pinzas en extremos separados; observa el LED; marca resultado; detecta contacto dudoso; pide repetir cuando corresponde. | `LOG-CONTROL-VARIABLE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | comparación, incertidumbre, registro, depuración | No prueba objetos no aprobados ni usa pinzas cerca de personas, líquidos, aparatos o enchufes. |

Todos los roles tienen agencia. Decorar la hoja no constituye un rol separado.

#### Role bundle `en-US`

| Role | Real contribution | Responsibilities | Eligible primary objectives | Expected exposures | Restricted actions |
|---|---|---|---|---|---|
| **Materials Investigator** | Chooses what to test and organizes physical evidence. | Names, handles, and observes approved samples; predicts; places each item in its observed category. | `LOG-CLASSIFY-EVIDENCE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | materials, contextual conductor/insulator, prediction, revision | Does not insert cells or touch fixed joints; the adult operates clips for ages 5–6. |
| **Circuit Keeper** | Keeps the procedure safe and consistent. | Confirms `OFF` before changes, traces the path, switches on only after clips are placed, and confirms controls. | `ELE-SEQUENCE-TEST`, `ELE-CLOSE-PATH`, `LOG-CONTROL-VARIABLE` | polarity, resistor, open/closed circuit, turns | Does not open the holder, reconfigure components, or remove insulation. |
| **Evidence Engineer** | Makes tests comparable and preserves results. | Helps direct clip placement, observes the LED, records results, flags uncertain contact, and requests a repeat when appropriate. | `LOG-CONTROL-VARIABLE`, `MAT-RECORD-RESULT`, `COM-EXPLAIN-CIRCUIT` | comparison, uncertainty, recording, troubleshooting | Does not test unapproved objects or use clips near people, liquids, devices, or outlets. |

#### Step permissions and dependencies

| Role | Permitted `step_id` | Dependency | Individual variant |
|---|---|---|---|
| Materials Investigator | `discover`, `imagine`, `build`, `experiment`, `improve`, `explain` | Adult has approved and prepared every sample; Circuit Keeper confirms `OFF` before sample change. | Child predicts, selects, observes, and classifies; adult performs any clip operation required by safety. |
| Circuit Keeper | `discover`, `build`, `experiment`, `improve`, `explain` | Adult has completed controls and retains access to switch; Evidence Engineer confirms result before change. | Child narrates and follows permitted sequence actions; adult retains all `adult-only` actions. |
| Evidence Engineer | `imagine`, `build`, `experiment`, `improve`, `explain` | Materials Investigator identifies current sample; Circuit Keeper confirms safe state. | Child observes and records one result at a time; adult maintains setup. |

No role is permitted to execute `adult-only-preparation`, open the holder, alter fixed joints, select electrical components, remove insulation, or approve new samples.

### 6.2 Configuraciones para uno, dos y tres niños

| Participantes | Asignación recomendada | Objetivo principal predeterminado cuando no hay evidencia previa | Coordinación |
|---:|---|---|---|
| 1 | El niño alterna los tres roles; el adulto maneja pinzas cuando sea necesario. | `LOG-CLASSIFY-EVIDENCE`: clasificar objetos después de observar el LED. | Complete una prueba a la vez; el adulto conserva el interruptor si el niño no sigue todavía la secuencia segura. |
| 2 | Niño A: Materials Investigator. Niño B: Circuit Keeper + Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`. B: `ELE-SEQUENCE-TEST`. | A entrega un objeto aprobado; B confirma `OFF`, coloca/ayuda a colocar y registra. Cambiar quién elige primero, no los objetivos, a mitad de la lista. |
| 3 | Niño A: Materials Investigator. Niño B: Circuit Keeper. Niño C: Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`. B: `ELE-SEQUENCE-TEST`. C: `MAT-RECORD-RESULT`. | Usar una frase de relevo: “objeto listo” → “circuito listo” → “resultado registrado”. Así todos contribuyen sin tocar simultáneamente las pinzas. |

#### Participant configurations `en-US`

| Children | Recommended assignment | Default primary objective without prior evidence | Coordination |
|---:|---|---|---|
| 1 | The child rotates through all three roles; the adult operates clips whenever required. | `LOG-CLASSIFY-EVIDENCE`. | Complete one sample at a time; the adult retains the switch if the child is not yet following the safe sequence. |
| 2 | Child A: Materials Investigator. Child B: Circuit Keeper + Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`; B: `ELE-SEQUENCE-TEST`. | A supplies one approved sample; B confirms `OFF`, directs or helps place it, and records. Switch who chooses first, not the objectives, midway. |
| 3 | Child A: Materials Investigator. Child B: Circuit Keeper. Child C: Evidence Engineer. | A: `LOG-CLASSIFY-EVIDENCE`; B: `ELE-SEQUENCE-TEST`; C: `MAT-RECORD-RESULT`. | Use “sample ready” → “circuit ready” → “result recorded” so all contribute without simultaneous clip handling. |

El recomendador puede elegir otro objetivo elegible según evidencia, independencia, interés y variedad de roles. Cada niño conserva **como máximo un objetivo principal**. Las demás habilidades son exposiciones salvo que el adulto elija “Evaluar más”. El adulto puede cambiar la asignación antes de iniciar.

### 6.3 Apoyos por edad y experiencia

- **5–6 años / Explorer–Builder:** usar cuatro objetos (cuchara, aluminio, regla plástica, cartón); el adulto fija las pinzas; el niño predice, enciende con permiso, observa y clasifica usando tarjetas con iconos.
- **7–8 años / Builder–Inventor:** usar seis o siete objetos; el niño puede operar pinzas aisladas con ayuda cercana, seguir la secuencia `OFF–colocar–ON–observar–OFF` y registrar con marcas.
- **9–10 años / Inventor:** usar todos los objetos; dibujar la trayectoria, distinguir resultado negativo de resultado incierto y justificar una repetición controlada.

La edad orienta lenguaje y control de seguridad; no determina por sí sola el objetivo.

**`en-US` age/experience supports:**

- **Ages 5–6 / Explorer–Builder:** use four samples (spoon, foil, plastic ruler, cardboard). The adult operates the clips; the child predicts, uses the switch with permission when appropriate, observes, and classifies with icon cards.
- **Ages 7–8 / Builder–Inventor:** use six or seven samples. The child may operate intact insulated clips with close help, follow `OFF–place–ON–observe–OFF`, and record with marks.
- **Ages 9–10 / Inventor:** use every sample, draw the path, distinguish a negative from an uncertain result, and justify a controlled repeat.

Age guides language and safety control; it does not determine the objective by itself.

## 7. Flujo bilingüe de la actividad

### Vista temporal

| Etapa | Tiempo base |
|---|---:|
| Discover | 5 min |
| Imagine | 5 min |
| Build | 7 min |
| Experiment | 8–10 min para 4 objetos; 14–18 min para 7 objetos |
| Improve | 4–8 min |
| Explain + cierre | 6–7 min |
| Extensión aprobada opcional | 8–10 min; total máximo 60 min |

El núcleo dura aproximadamente 35–43 minutos con cuatro objetos y 42–50 minutos con siete. Solo se añade una extensión cuando el tiempo restante mantiene la sesión en 60 minutos o menos.

### Contrato estructurado de pasos

| `step_id` | Actor y tiempo | Visual esperado | Señal de éxito | Problema frecuente y solución segura | Advertencia | Reanudación |
|---|---|---|---|---|---|---|
| `discover` | Grupo; adulto controla tester; 5 min | Control abierto/apagado y cerrado/encendido | El niño localiza la separación entre pinzas | Si “electricidad” queda abstracto, seguir físicamente la trayectoria con el tester en `OFF` | Solo el adulto ejecuta controles; no tocar uniones fijas | Adulto repite control abierto/cerrado y vuelve a apagar |
| `imagine` | Materials Investigator; 5 min | Objetos alineados con predicción atribuida | Cada objeto elegido tiene predicción o `no sé` | Si se trata como examen, recordar que la predicción no se califica | No conectar todavía objetos ni introducir muestras nuevas | Conservar hoja/tarjetas y retomar desde el primer objeto no probado |
| `build` | Niños organizan; adulto conserva montaje; 7 min | Tester intacto, `OFF`, pinzas separadas y muestras ordenadas | Roles repiten la secuencia y el adulto confirma control | Si se tira de un cable, detener y retirar el montaje hasta reinspección adulta | Niños no tocan uniones fijas, portapilas ni componentes sueltos | Adulto inspecciona, repite control y autoriza retomar |
| `experiment` | Roles coordinados; 8–18 min | Pinzas separadas sobre una muestra y LED visible | Resultado registrado; `OFF` antes de cada cambio | Ante resultado tenue, repetir control y una sola prueba; conservar `incierto` | Nadie toca metal expuesto durante `ON`; solo objetos aprobados | En pausa, adulto apaga y retira pilas; al volver, reinspecciona y repite controles |
| `improve` | Grupo; 4–8 min | Una sola variable de contacto/visibilidad cambia | El resultado se aclara o permanece honestamente `incierto` | Si cambian dos variables, volver al último estado registrado y cambiar solo una | No cambiar fuente, resistencia, LED, uniones fijas o energía | Usar la hoja para identificar la prueba elegida; repetir control antes de continuar |
| `explain` | Cada niño según rol; 6–7 min | Diagrama conceptual y hoja de resultados | Explicación oral, señalada o dibujada conecta evidencia y trayectoria | Si el lenguaje exige demasiado, permitir señalar el camino y las tarjetas | Cierre sin nuevas muestras ni conexiones | Retomar con hoja y diagrama; no reenergizar para completar la explicación |

#### Structured step contract `en-US`

| `step_id` | Actor and time | Expected visual | Success signal | Common issue and safe solution | Warning | Resume |
|---|---|---|---|---|---|---|
| `discover` | Group; adult controls tester; 5 min | Open/off and closed/lit controls | Child locates the gap between clips | If electricity feels abstract, trace the physical path with tester `OFF` | Adult alone runs controls; no fixed-joint contact | Adult repeats open/closed controls and switches off |
| `imagine` | Materials Investigator; 5 min | Samples lined up with attributed prediction | Each chosen sample has a prediction or `not sure` | If treated as a quiz, remind children predictions are not graded | Do not connect samples or add new ones yet | Keep sheet/cards and resume at first untested sample |
| `build` | Children organize; adult retains setup; 7 min | Intact tester `OFF`, clips apart, samples ordered | Roles repeat sequence and adult confirms control | If a lead is pulled, stop and retire setup until adult reinspection | Children do not touch fixed joints, holder, or loose components | Adult reinspects, repeats controls, and authorizes resume |
| `experiment` | Coordinated roles; 8–18 min | Clips separated on one sample; LED visible | Result recorded; `OFF` before every change | For dim result, repeat control and one test; keep `uncertain` | No exposed-metal contact during `ON`; approved samples only | Adult switches off/removes cells for pause; reinspects and repeats controls |
| `improve` | Group; 4–8 min | Only one contact/visibility variable changes | Result becomes clearer or honestly remains `uncertain` | If two variables change, restore last recorded state and change one | Do not alter source, resistor, LED, fixed joints, or energy | Use sheet to identify chosen test; repeat control before resuming |
| `explain` | Each child by role; 6–7 min | Concept diagram and result sheet | Spoken, pointed, or drawn explanation connects evidence and path | If language demand is high, allow pointing to path/cards | No new samples or energized connections during close | Resume with sheet/diagram; do not reenergize merely to explain |

### 7.1 Discover — encontrar la trayectoria / Find the path

**Actor:** grupo; adulto controla el tester.

**Señal visual requerida:** diagrama de circuito abierto y cerrado.

**es-US — Para el adulto**

Muestre el probador apagado y las dos pinzas separadas. Diga: “Este LED solo puede encender si existe una trayectoria completa desde una pila, a través de todas las piezas, y de regreso a la otra parte de la batería. Estas dos pinzas son la separación que intentaremos cerrar con un objeto”. Haga el control abierto y luego el control cerrado. Apague después de cada demostración.

**es-US — Pregunta para los niños**

“¿Qué cambió cuando las pinzas se tocaron? ¿Qué podría ir entre ellas para completar el camino?”

**en-US — For the adult**

Show the switched-off tester with the two test clips apart. Say: “This LED can light only when there is a complete path from one side of the battery, through every part, and back to the other side. These two clips are the gap we will try to close with an object.” Perform the open control and then the closed control. Switch off after each demonstration.

**en-US — Ask the children**

“What changed when the clips touched? What could go between them to complete the path?”

**Éxito / Success:** los niños identifican la separación entre las pinzas como parte abierta de la trayectoria. No necesitan usar todavía la palabra “conductor”.

### 7.2 Imagine — predecir sin calificar / Predict without grading

**Actor:** Materials Investigator; los demás pueden proponer razones.

**Señal visual requerida:** tablero de materiales y hoja de predicción.

**es-US**

Elijan los objetos aprobados que usarán. Para cada uno, marquen “creo que encenderá”, “creo que no” o “no estoy seguro”. Pregunte: “¿Qué observas del material que te hace pensar eso?” Acepte cambios de opinión antes de la prueba y no revele resultados.

**en-US**

Choose the approved objects you will use. For each one, mark “I think it will light,” “I think it will not,” or “I am not sure.” Ask: “What do you notice about the material that makes you think that?” Allow children to revise before testing and do not reveal results.

**Éxito / Success:** existe una predicción atribuida a cada objeto; una predicción correcta no es el objetivo principal por defecto.

### 7.3 Build — preparar la estación de prueba / Set up the test station

**Actor:** los niños organizan; el adulto conserva control de uniones fijas.

**Advertencia visible:** `OFF antes de cambiar / OFF before changing`.

**es-US**

1. Coloquen el probador en el centro sin tirar de los cables.
2. Ordenen los objetos en una fila y coloquen las tres tarjetas de resultado.
3. Sigan con un dedo el recorrido: `+ de batería → resistencia → LED → pinza → objeto → pinza → − de batería`.
4. El Circuit Keeper practica la secuencia en voz alta: “apagado, colocar, encender, observar, apagar”.
5. El adulto comprueba de nuevo el control cerrado y apaga.

**en-US**

1. Place the tester in the center without pulling on its wires.
2. Line up the samples and set out the three result cards.
3. Trace the path with a finger: `battery + → resistor → LED → clip → sample → clip → battery −`.
4. The Circuit Keeper rehearses aloud: “off, place, on, observe, off.”
5. The adult repeats the closed control and switches off.

**Resultado esperado / Expected result:** circuito intacto, pinzas separadas, interruptor apagado y materiales organizados.

### 7.4 Experiment — probar un objeto a la vez / Test one object at a time

**Actor:** roles coordinados; adulto a distancia de alcance.

**Tiempo:** 2–2.5 minutos por objeto; 8–10 minutos para cuatro objetos y 14–18 para siete.

Repita esta secuencia para cada objeto:

1. **OFF / OFF.** El Circuit Keeper confirma que el interruptor está apagado.
2. **Seleccionar / Select.** Materials Investigator entrega un solo objeto aprobado y recuerda la predicción.
3. **Conectar / Connect.** Sujete una pinza en cada extremo del mismo objeto. Las mandíbulas no deben tocarse entre sí. Para niños de 5–6 años o con dificultad motriz, lo hace el adulto siguiendo las indicaciones del niño.
4. **Encender dos segundos / Switch on for two seconds.** Nadie toca metal expuesto ni cambia el montaje durante la observación.
5. **Observar / Observe.** Evidence Engineer dice “encendió”, “no encendió” o “incierto”; coloque el objeto junto a esa tarjeta.
6. **Apagar y registrar / Switch off and record.** Marque el resultado antes de retirar el objeto.
7. **Control si hay duda / Control if uncertain.** Si el resultado fue inesperado o tenue, apague, retire el objeto, haga el control cerrado por 2 segundos y vuelva a probar una sola vez con contacto limpio. Si sigue ambiguo, conserve `incierto`; no fuerce una conclusión.

**es-US — Preguntas durante la prueba**

- “¿Están las pinzas tocando el objeto, pero no tocándose entre sí?”
- “¿Qué mantuvimos igual en esta prueba?”
- “¿El resultado nos hace cambiar alguna categoría?”

**en-US — Questions during testing**

- “Are both clips touching the object without touching each other?”
- “What did we keep the same in this test?”
- “Does the result make us change any category?”

**Señal de éxito / Success signal:** cada objeto tiene un resultado registrado y el circuito se apaga antes de cada cambio.

### 7.5 Improve — mejorar la confiabilidad / Improve reliability

**Actor:** grupo, con una decisión infantil.

**Objetivo:** distinguir fallo de contacto de propiedad del material.

**es-US**

Elijan una prueba que haya sido difícil de ver o de sujetar. Pregunte: “¿Cómo podemos hacer el contacto de la misma manera sin cambiar la fuente ni el circuito?” Elijan **una** mejora aprobada: doblar el aluminio a cuatro capas, sujetar las pinzas más lejos una de otra, colocar la tarjeta blanca detrás del LED o asignar a una sola persona el interruptor. Repitan el control cerrado y luego esa prueba una vez. Comparen si el resultado fue más claro.

**en-US**

Choose one test that was hard to see or hold. Ask: “How can we make contact in the same way without changing the power source or circuit?” Choose **one** approved improvement: fold the foil to four layers, place the clips farther apart, put the white card behind the LED, or assign only one person to the switch. Repeat the closed control and then repeat that test once. Compare whether the result became clearer.

**Límite:** mejorar no permite cambiar pilas, resistencia, LED, conexiones fijas, energía ni lista segura de objetos.

### 7.6 Explain — conectar evidencia y mecanismo / Connect evidence and mechanism

**Actor:** cada niño contribuye según su rol.

**Señal visual requerida:** diagrama conceptual, marcado “no está a escala / not to scale”.

**es-US — Explicación infantil**

“Una corriente eléctrica necesita una trayectoria completa. La cuchara y el aluminio permitieron suficiente corriente para que este LED encendiera; en este probador actuaron como conductores. El plástico, la madera seca, el cartón, la goma y la tela seca no dejaron pasar suficiente corriente para encenderlo; en este probador actuaron como aislantes. La resistencia limita la corriente para proteger el LED. La batería tiene dos lados y el LED debe mirar en la dirección correcta.”

**en-US — Child-facing explanation**

“Electric current needs a complete path. The spoon and foil allowed enough current through for this LED to light; in this tester they acted as conductors. The plastic, dry wood, cardboard, rubber, and dry fabric did not allow enough current through to light it; in this tester they acted as insulators. The resistor limits current to protect the LED. The battery has two sides, and the LED must face the correct direction.”

**Preguntas de cierre / Closing questions**

- ¿Qué resultado cambió o confirmó tu idea? / Which result changed or confirmed your idea?
- ¿Cómo sabes que el probador funcionaba? / How do you know the tester was working?
- ¿Por qué un LED apagado puede significar “incierto” y no siempre “aislante”? / Why can an unlit LED mean “uncertain” instead of always meaning “insulator”?
- ¿Dónde debe haber una trayectoria sin interrupciones? / Where must there be an unbroken path?

## 8. Explicaciones para el adulto

### Breve — `es-US`

Los metales probados suelen tener electrones que pueden moverse con facilidad, por lo que completan la trayectoria y dejan pasar suficiente corriente para encender el LED. Los objetos secos no metálicos de esta lista ofrecen mucha más resistencia. El LED solo deja pasar corriente fácilmente en una dirección, y la resistencia de 330 Ω limita la corriente.

### Brief — `en-US`

The tested metals usually contain electrons that can move readily, so they complete the path and allow enough current to light the LED. The dry nonmetal objects on this list have much higher resistance. The LED conducts readily in only one direction, and the 330 Ω resistor limits current.

### Detallada — `es-US`

Dos pilas AA en serie proporcionan aproximadamente 3 V nominales. Cuando un objeto une las pinzas, la trayectoria queda cerrada: batería, resistencia, LED, objeto y regreso a la batería. La corriente de un circuito en serie atraviesa todos esos elementos. La resistencia reduce la corriente a un rango pequeño para no sobrecargar el LED. El ánodo del LED debe quedar hacia el lado positivo y el cátodo hacia el negativo; si se invierte, normalmente no enciende.

“Conductor” y “aislante” no son etiquetas absolutas independientes de las condiciones. Todo material presenta alguna resistencia; este probador solo muestra si, con cerca de 3 V, el contacto disponible y este LED, circuló suficiente corriente para producir luz visible. Por eso se usan controles abierto/cerrado y una categoría incierta.

### Detailed — `en-US`

Two AA cells in series provide about 3 V nominally. When a sample bridges the clips, the path closes: battery, resistor, LED, sample, and back to the battery. Current in a series circuit passes through every one of those elements. The resistor limits the current to a small range so the LED is not overloaded. The LED anode must face the positive side and the cathode the negative side; when reversed, it normally will not light.

“Conductor” and “insulator” are not absolute labels independent of conditions. Every material has some resistance; this tester shows only whether, at about 3 V, with the available contact and this LED, enough current flowed to make visible light. That is why the activity uses open/closed controls and an uncertain category.

## 9. Extensiones y adaptaciones aprobadas

### 9.1 Extensión opcional: interruptor de aluminio (8–10 min)

**Material adicional:** dos cuadrados de cartón seco de 8 × 8 cm / 3 × 3 in, dos tiras de papel aluminio de 3 × 6 cm / 1 × 2.5 in y cinta adhesiva de papel. El adulto corta previamente si se requieren tijeras.

1. Peguen una tira de aluminio en cada cartón, dejando expuesta la mayor parte del metal.
2. Con `OFF`, sujeten una pinza a cada tira de aluminio.
3. Enciendan con los cartones separados: el LED debe permanecer apagado.
4. El adulto enciende. El niño sostiene únicamente los bordes de cartón y acerca un cartón al otro hasta que las caras de aluminio se toquen. Nadie toca aluminio, pinzas ni conexiones mientras está en `ON`. El LED debe encender.
5. Expliquen cómo abrir y cerrar una separación controla la trayectoria.

No se aumenta voltaje, corriente, temperatura ni velocidad. Si no funciona, vuelva al probador base; no añada pilas ni elimine la resistencia.

**`en-US` — Optional foil-switch extension:** Add two dry cardboard squares, each about 8 × 8 cm / 3 × 3 in, two foil strips about 3 × 6 cm / 1 × 2.5 in, and masking tape. The adult cuts in advance if scissors are needed. Tape one foil strip onto each square, leaving most of the metal exposed. With the tester `OFF`, the adult attaches one test clip to each strip. The adult switches on while the squares are apart; the LED should remain off. The child holds only the cardboard edges and brings the cards together until the foil faces meet. No one touches foil, clips, or connections while the tester is `ON`. The LED should light. Explain how opening and closing the gap controls the path. Do not increase voltage, current, temperature, or speed. If it does not work, return to the base tester; never add cells or remove the resistor.

### 9.2 Adaptaciones de presentación

- Leer en voz alta y usar fotos de cada material; no exigir lectura infantil.
- Usar iconos `💡`, `○` y `?` junto con palabras; no codificar resultados solo por rojo/verde.
- Permitir respuesta hablada, señalada o dibujada.
- Para atención breve, probar cuatro objetos, guardar la hoja y reanudar después; el adulto apaga y retira las pilas durante la pausa.

**`en-US`:** Read aloud and use material photos; do not require child reading. Use words and icons together rather than red/green color alone. Accept spoken, pointed, or drawn responses. For a shorter attention window, test four samples, save the sheet, and resume later; the adult switches off and removes the AA cells during the break.

### 9.3 Adaptaciones motrices

- Fijar el tester a una bandeja antideslizante sin cubrir ventilación ni interruptor.
- El adulto abre y coloca las pinzas; el niño dirige los puntos de contacto, acciona el interruptor si puede hacerlo con seguridad y clasifica el objeto.
- Usar exclusivamente objetos grandes de la lista. No reemplazar con cuentas, monedas, tornillos ni piezas pequeñas.

**`en-US`:** Secure the tester to a nonslip tray without blocking the switch. The adult opens and positions clips while the child directs contact points, operates the switch if safe, and classifies the sample. Use only the large listed objects; do not substitute beads, coins, screws, or other small parts.

### 9.4 Aumentos de reto aprobados

- Pedir un diagrama de la trayectoria y una explicación del papel de la resistencia.
- Ocultar una sola separación segura en el montaje **con el interruptor apagado y creada por el adulto**; el niño la localiza mediante inspección visual y controles, sin abrir el portapilas ni retirar aislamiento.
- Comparar la misma tira de aluminio con contacto sobre metal expuesto y con una pequeña zona cubierta por cinta de papel. Registrar que el recubrimiento bloquea el contacto en ese punto; no concluir que el aluminio dejó de conducir.

**`en-US`:** Approved challenge options are: draw the complete path and explain the resistor; locate one safe gap created by the adult while the tester is off, without opening the holder or removing insulation; or compare contact on exposed foil with contact on a small masking-tape-covered area. Record that the coating blocks contact at that point, not that the foil stopped conducting.

## 10. Troubleshooting bilingüe

Antes de cualquier diagnóstico: `OFF`, manos secas, adulto a cargo. Nunca resolver añadiendo pilas, retirando la resistencia o probando una fuente externa.

| Problema | Causa probable | Acción segura `es-US` | Safe action `en-US` |
|---|---|---|---|
| El LED no enciende en el control cerrado | Interruptor apagado, pilas invertidas/débiles, LED invertido, conexión floja | Apague. El adulto revisa polaridad y uniones cubiertas; reemplaza ambas AA juntas si están agotadas. No permita que el niño manipule el portapilas. | Switch off. The adult checks polarity and covered joints; replace both AA cells together if depleted. Do not let a child handle the holder. |
| El LED enciende con las pinzas separadas | Las mandíbulas o cables se tocan; hay un puente no previsto | Apague y separe cables. El adulto inspecciona el montaje. No continúe hasta recuperar un control abierto confiable. | Switch off and separate the leads. The adult inspects the setup. Do not continue until the open control is reliable. |
| El LED enciende con todos los objetos | Las pinzas se tocan alrededor del objeto | Apague y coloque las pinzas en extremos alejados sin contacto directo entre mandíbulas. Repita control abierto. | Switch off and place clips at separated ends without jaw-to-jaw contact. Repeat the open control. |
| Un metal no enciende | Contacto sobre pintura/recubrimiento, suciedad, pinza floja o pilas débiles | No raspe ni corte. Use la cuchara o el aluminio de control, limpios y secos; haga control cerrado. Registre `incierto` si persiste. | Do not scrape or cut. Use the clean, dry control spoon or foil; perform the closed control. Record `uncertain` if it persists. |
| El LED se ve muy tenue | Luz ambiental fuerte, contacto pobre o resistencia del objeto | Coloque tarjeta blanca detrás del LED, mejore el contacto sin cambiar circuito y repita una vez. No reduzca la resistencia. | Put the white card behind the LED, improve contact without changing the circuit, and repeat once. Do not lower the resistor value. |
| LED, resistencia, cable o pilas se calientan; hay olor, humo, fuga, corrosión o chispa | Daño o conexión incorrecta | Apague solo si puede hacerlo sin acercarse ni tocar el peligro. Aleje a los niños. No abra el portapilas ni retire pilas mientras esté caliente, humeando, chispeando o con fuga. Siga la guía del fabricante y retire el montaje de servicio. | Switch off only if this can be done without approaching or touching the hazard. Move children away. Do not open the holder or remove cells while it is hot, smoking, sparking, or leaking. Follow the manufacturer guidance and retire the setup. |
| El grupo pierde correspondencia entre objeto y resultado | Demasiados objetos o cambios simultáneos | Regrese todos los objetos a la fila y pruebe uno por vez con relevo verbal. No atribuya evidencia individual si no se sabe quién realizó la acción. | Return all objects to the row and test one at a time with the verbal handoff. Do not attribute individual evidence if the actor is unclear. |

## 11. Seguridad y limpieza

### Riesgos y controles

| Peligro | Persona/condición expuesta | Control obligatorio |
|---|---|---|
| Ingestión o uso indebido de pilas/componentes | Niños, especialmente 5–7 años | Adulto inserta, retira, cuenta y guarda; portapilas cerrado; no pilas tipo moneda; detener si un niño lleva objetos a la boca. |
| Pinchazo o pellizco de pinzas | Dedos infantiles | Pinzas pequeñas aisladas e intactas; ayuda cercana; adulto opera para 5–6 años o cuando la coordinación no sea suficiente. |
| Calentamiento por conexión incorrecta o corto fuera del circuito limitado | Todos | Resistencia obligatoria en serie; uniones fijas cubiertas; control previo; interruptor `OFF` entre muestras; adulto al alcance. |
| Unión fija floja, tirón o terminal expuesto | Niños y adulto durante manipulación | Configuración seleccionada con alivio de tensión validado; inspección adulta antes de cada uso; retirar ante cualquier movimiento, giro o metal fijo visible. |
| Contacto con energía externa | Todos | Probar solo objetos secos, sueltos y listados; mesa alejada de enchufes/dispositivos; prohibiciones explícitas repetidas antes de probar. |
| Fuga de pila | Todos | Inspección antes de uso; no usar pilas dañadas; no abrir ni retirar mientras exista calor/humo/chispa/fuga; alejar niños y seguir guía del fabricante. |
| Confusión por un resultado negativo | Aprendizaje | Control cerrado antes y después de resultado dudoso; categoría `incierto`; explicación cualitativa. |

#### Risk matrix `en-US`

| Hazard | Exposed person/condition | Mandatory control |
|---|---|---|
| Ingestion or misuse of cells/components | Children, especially ages 5–7 | Adult alone inserts, removes, counts, and stores; holder stays closed; no coin cells; stop if an item approaches the mouth. |
| Clip pinch or puncture | Children's fingers | Use intact small insulated clips with close help; adult operates for ages 5–6 or whenever coordination is insufficient. |
| Heating from incorrect connection or a short outside the limited path | Everyone | Resistor always in series; fixed joints covered; pre-check controls; `OFF` between samples; adult within reach. |
| Loose fixed joint, pull, or exposed terminal | Children and adult during handling | Selected configuration has validated strain relief; adult inspects before every use; retire upon any movement, rotation, or visible fixed metal. |
| Contact with external energy | Everyone | Test only listed dry, loose samples; keep table away from outlets/devices; repeat prohibitions before testing. |
| Cell leakage | Everyone | Inspect before use; never use damaged cells; do not open/remove while there is heat, smoke, a spark, or leakage; move children away and follow manufacturer guidance. |
| Misreading a negative result | Learning | Closed control before/after doubtful result; retain `uncertain`; use qualitative explanation. |

### Señales para detenerse

Detenga de inmediato si un niño intenta probar una persona, animal, líquido, enchufe, cable, batería o dispositivo; si alguien se lleva un componente a la boca; si se rompe el aislamiento; si una conexión no puede mantenerse cubierta; o si aparece calor, olor, humo, chispa, corrosión, fuga o comportamiento intermitente no explicado.

**`en-US` stop conditions:** Stop immediately if a child tries to test a person, animal, liquid, outlet, cable, battery, or device; if anyone puts a component in their mouth; if insulation breaks; if a fixed connection cannot remain covered; or if there is heat, odor, smoke, a spark, corrosion, leakage, or unexplained intermittent behavior.

### Limpieza y almacenamiento — solo adulto para el circuito

1. Ponga el interruptor en `OFF`.
2. Retire las dos pilas AA y guárdelas según las indicaciones del fabricante, fuera del alcance infantil. No deje pilas instaladas entre sesiones.
3. Cuente LED, resistencia, cables y pilas; no deje componentes pequeños sueltos.
4. Separe los objetos cotidianos. Recicle o guarde el aluminio sin bordes sobresalientes.
5. Guarde el tester como unidad etiquetada `3 V — ACT-0003`; retire de servicio si la cinta o aislamiento se despega.
6. Limpie la mesa en seco. No lave el circuito ni use aerosoles o líquidos sobre él.

**`en-US` cleanup and storage:** The adult switches `OFF`, removes both AA cells, and stores them according to the manufacturer, out of children's reach. Do not leave cells installed between sessions. Count the LED, resistor, leads, and cells; leave no small parts loose. Recycle or store foil without projecting edges. Store the tester as one unit labeled `3 V — ACT-0003` and retire it if tape or insulation lifts. Dry-clean the table; never wash or spray the circuit.

## 12. Observación y evaluación

### 12.1 Registro automático

Si un niño participó, registrar automáticamente:

- ActivityVersion `ACT-0003@0.1.1`.
- Rol real y configuración de participantes.
- Objetivo principal asignado.
- Exposiciones previstas según su rol.
- Adaptación utilizada y si hubo fallo de equipo.

La participación o exposición no se convierte en evidencia de independencia. Si un niño no participó, no crear exposición ni solicitar valoración.

### 12.2 Preguntas por objetivo elegible

La independencia se valora únicamente sobre las acciones permitidas para el niño. Una acción adulta obligatoria por seguridad —insertar pilas, sostener pinzas para 5–6 años, proteger uniones o detener el circuito— es una condición del entorno y **no reduce** la puntuación. Sí cuenta como ayuda cuando el adulto toma por el niño la decisión cognitiva evaluada, le indica cada respuesta o ejecuta una acción infantil permitida que el niño necesitaba practicar.

**`en-US`:** Rate independence only on actions the child is permitted to perform. Safety-required adult action—such as inserting cells, holding clips for ages 5–6, protecting fixed joints, or stopping the circuit—is an environmental control and **does not lower** the rating. Adult action counts as help when the adult makes the assessed cognitive decision, supplies each answer, or performs a permitted child action the child was meant to practice.

| Objetivo | Pregunta `es-US` | Question `en-US` | Sí cuenta como evidencia | No cuenta por sí solo | Factores externos |
|---|---|---|---|---|---|
| `LOG-CLASSIFY-EVIDENCE` | ¿Qué tan independientemente clasificó los objetos según lo que mostró el LED? | How independently did they classify the objects based on what the LED showed? | Coloca cada objeto según el resultado observado y corrige una predicción cuando corresponde. | Adivinar categorías antes de probar; copiar a otro niño. | No vio el LED, objetos mezclados, rol cambiado. |
| `ELE-SEQUENCE-TEST` | ¿Qué tan independientemente dirigió y siguió sus acciones permitidas en la secuencia apagar–colocar–encender–observar–apagar? | How independently did they direct and follow their permitted actions in the off–place–on–observe–off sequence? | Mantiene o verbaliza el orden, espera la acción adulta obligatoria y solicita ayuda antes de un cambio inseguro. | Manipulación rápida sin respetar `OFF`; el adulto decidió y anunció cada paso. | Interruptor difícil, apoyo motriz obligatorio, montaje intermitente. |
| `ELE-CLOSE-PATH` | ¿Qué tan independientemente identificó dónde debía cerrarse la trayectoria para encender el LED? | How independently did they identify where the path had to close to light the LED? | Señala la separación o describe el recorrido completo. | Repetir “circuito” sin localizar la interrupción. | Diagrama poco claro, uniones ocultas. |
| `LOG-CONTROL-VARIABLE` | ¿Qué tan independientemente mantuvo iguales las condiciones al comparar objetos? | How independently did they keep the test conditions the same across samples? | Usa mismo circuito, secuencia y contacto comparable; pide repetir un dudoso. | Obtener muchos resultados con cambios simultáneos. | Pinzas difíciles de sujetar, otro participante cambió el montaje. |
| `MAT-RECORD-RESULT` | ¿Qué tan independientemente registró cada resultado junto al objeto correcto? | How independently did they record each result with the correct object? | Conserva correspondencia y marca incierto cuando aplica. | Hoja completa escrita por otro; decorar sin registrar. | Exigencia de escritura, pérdida de hoja, turnos confusos. |
| `COM-EXPLAIN-CIRCUIT` | ¿Qué tan independientemente explicó un resultado usando la trayectoria del circuito? | How independently did they explain one result using the circuit path? | Vincula trayectoria completa con LED encendido y reconoce límites del probador. | Decir “porque sí” o “todos los metales siempre encienden” sin evidencia. | Vocabulario bilingüe, timidez, preferencia por señalar/dibujar. |

### 12.3 Escala contextual 1–5

| Valor | Ancla `es-US` | Anchor `en-US` |
|---:|---|---|
| 1 | No pudo hacerlo todavía, incluso con apoyo razonable. | Could not do it yet, even with reasonable support. |
| 2 | Lo logró con bastante ayuda. | Did it with substantial help. |
| 3 | Lo logró con alguna ayuda. | Did it with some help. |
| 4 | Lo logró casi sin ayuda. | Did it almost independently. |
| 5 | Lo hizo de forma independiente y segura. | Did it independently and safely. |

### 12.4 Flujo de cierre

- Mostrar solo a los niños que participaron.
- Solicitar una valoración de un toque por objetivo principal y niño.
- Con tres niños, la ruta normal son tres toques y debe probarse por debajo de 20 segundos.
- Ofrecer `Evaluar más / Evaluate more` de forma secundaria para habilidades adicionales.
- Ofrecer una nota de voz o texto opcional para toda la sesión.
- Permitir `Omitir / Skip`, `Problema con el equipo / Equipment issue` y corrección posterior.
- Si los niños colaboraron de forma inseparable, registrar evidencia de grupo; no atribuir desempeño individual sin confirmación.

### 12.5 Ejemplos de observación válida

- “Durante ACT-0003, Lina clasificó seis objetos según el LED y cambió la cuchara de su predicción ‘no’ a ‘encendió’ sin ayuda.”
- “Durante ACT-0003, Mateo siguió la secuencia con recordatorios para apagar antes de cambiar cada objeto.”
- “El control cerrado falló dos veces; los resultados de conductividad de esta sesión no deben alimentar inferencias.”

Estas observaciones conservan contexto y apoyo. No producen etiquetas globales sobre habilidad, inteligencia o personalidad.

## 13. Briefs de recursos visuales

Todos los recursos se vinculan a `ACT-0003@0.1.1`, pasan QA automático y aprobación humana, y contienen texto como capa programática. No mostrar rostros, marcas, enchufes, líquidos, pilas tipo moneda, fuente USB ni niños manipulando el portapilas.

### ACT-0003-VIS-01 — Materials board fotorealista

- **Tipo:** materials board, vista cenital fotorealista.
- **Contenido:** portapilas cerrado de 2 AA con interruptor, dos AA alcalinas al lado pero en zona marcada para adulto, LED rojo, resistencia etiquetada 330 Ω, cuatro cables con pinzas aisladas, cinta aislante, cuchara metálica, aluminio doblado, regla plástica, palito, cartón, espátula de silicona, tela, hoja y crayón.
- **Composición:** objetos separados, escala coherente, fondo seco neutro; componentes adultos agrupados visualmente con icono de mano adulta.
- **Excluir:** texto generado, conexiones eléctricas ambiguas, objetos adicionales, marcas, pilas instaladas, manos infantiles.
- **Alt `es-US`:** Materiales del probador separados sobre una mesa: portapilas de dos AA, LED rojo, resistencia de 330 ohmios, cables aislados y siete objetos secos para probar.
- **Alt `en-US`:** Conductivity tester materials separated on a table: a two-AA holder, red LED, 330-ohm resistor, insulated leads, and seven dry test objects.

### ACT-0003-VIS-02 — Preparación adulta fotorealista + overlay

- **Tipo:** preparation, detalle fotorealista con líneas superpuestas programáticamente.
- **Contenido:** manos adultas conectando con interruptor `OFF`; trayectoria rojo `+` → resistencia → pata larga del LED → pinza A; pinza B → negro `−`; pilas todavía fuera.
- **Momentos:** panel A antes de insertar pilas; panel B uniones fijas totalmente cubiertas; panel C solo las dos pinzas de prueba quedan libres y separadas.
- **Excluir:** soldador, protoboard, pinza infantil, metal expuesto en uniones fijas, conexión directa rojo-negro.
- **Alt `es-US`:** Manos adultas preparan con el interruptor apagado un circuito en serie y cubren las uniones fijas antes de insertar las pilas.
- **Alt `en-US`:** Adult hands prepare the series circuit with the switch off and cover fixed joints before inserting batteries.

### ACT-0003-VIS-03 — Diagrama instructivo del circuito

- **Tipo:** diagrama instructivo, no a escala.
- **Contenido:** símbolos simples y objetos reconocibles en una sola trayectoria: 2×AA, switch, 330 Ω, LED con ánodo/cátodo, dos sondas y bloque `sample/material`; flechas convencionales opcionales claramente etiquetadas como corriente convencional.
- **Estados:** lado izquierdo circuito abierto con pinzas separadas/LED apagado; lado derecho muestra metálica entre pinzas/LED encendido.
- **Accesibilidad:** `+`/`−`, formas y etiquetas además de colores; alto contraste.
- **Alt `es-US`:** Diagrama de un circuito abierto con el LED apagado y del mismo circuito cerrado por una muestra metálica con el LED encendido.
- **Alt `en-US`:** Diagram of an open circuit with the LED off and the same circuit closed by a metal sample with the LED on.

### ACT-0003-VIS-04 — Secuencia de prueba

- **Tipo:** step diagram de cinco viñetas.
- **Contenido:** `OFF` → colocar pinzas en extremos del objeto sin que se toquen → `ON 2 s` → observar → `OFF y registrar`.
- **Actor:** para contexto de 5–6 años, manos adultas colocan las pinzas mientras una mano infantil señala el punto de contacto, usa una tarjeta de resultado o acciona el interruptor con permiso; no mostrar manos infantiles operando pinzas. Para mayores con coordinación suficiente, una viñeta separada puede mostrar pinzas infantiles con supervisión adulta cercana. Nunca mostrar manipulación de pilas o uniones fijas por niños.
- **Alt `es-US`:** Cinco pasos muestran apagar, sujetar un objeto seco, encender dos segundos, observar el LED y apagar antes de registrar.
- **Alt `en-US`:** Five steps show switching off, clipping onto a dry object, switching on for two seconds, observing the LED, and switching off before recording.

### ACT-0003-VIS-05 — Resultados esperados fotorealistas

- **Tipo:** expected result, tres paneles.
- **Contenido:** cuchara con LED encendido; regla plástica con LED apagado; ejemplo de contacto dudoso marcado `?` sin afirmar resultado.
- **Control crítico:** las mandíbulas deben contactar extremos separados y no tocarse directamente.
- **Alt `es-US`:** Comparación entre una cuchara que enciende el LED, una regla plástica que no lo enciende y un contacto dudoso que debe repetirse.
- **Alt `en-US`:** Comparison of a spoon that lights the LED, a plastic ruler that does not, and uncertain contact that should be repeated.

### ACT-0003-VIS-06 — Troubleshooting de polaridad y contacto

- **Tipo:** troubleshooting diagram.
- **Contenido:** comparación correcta/incorrecta de pata larga hacia `+`; pinzas separadas sobre el objeto versus mandíbulas tocándose; símbolo `OFF` antes de corregir.
- **Excluir:** sugerir invertir con energía, retirar resistencia, añadir pilas o raspar objetos.
- **Alt `es-US`:** Diagrama de corrección con el probador apagado: polaridad correcta del LED y pinzas separadas sobre la muestra.
- **Alt `en-US`:** Switch-off correction diagram showing proper LED polarity and test clips separated across the sample.

### ACT-0003-VIS-07 — Concepto conductor/aislante

- **Tipo:** concept diagram, marcado `explicativo; no a escala / explanatory; not to scale`.
- **Contenido:** camino continuo a través de metal comparado con camino bloqueado en plástico seco; resistencia visible siempre en serie; texto cauteloso “suficiente corriente para este LED”.
- **Alt `es-US`:** Diagrama conceptual donde un metal completa la trayectoria y un plástico seco no deja pasar suficiente corriente para este LED.
- **Alt `en-US`:** Concept diagram where metal completes the path and dry plastic does not allow enough current for this LED.

## 14. Verificación eléctrica preliminar

Esta sección documenta la plausibilidad del diseño; no reemplaza la ejecución física ni la revisión de un especialista.

- Una celda alcalina AA tiene 1.5 V nominales y puede aproximarse a 1.6 V en circuito abierto cuando está fresca; dos en serie se modelan conservadoramente como hasta 3.2 V para el cálculo inicial. Fuente: [Energizer Alkaline Manganese Dioxide Handbook](https://data.energizer.com/pdfs/alkaline_appman.pdf).
- Un LED rojo de alta eficiencia de referencia tiene caída directa típica de 1.9 V a 10 mA y límite continuo de 30 mA. Fuente de referencia: [Kingbright WP1053IDT datasheet](https://www.kingbrightusa.com/images/catalog/spec/WP1053IDT.pdf). La pieza editorial final debe tener especificación igual o más restrictiva y quedar ligada a la lista aprobada.
- Estimación ilustrativa con valores nominales: `(3.0 V − 1.9 V) / 330 Ω ≈ 3.3 mA`; con 3.2 V, `≈ 3.9 mA`. La caída de 1.9 V del datasheet está especificada a 10 mA, por lo que esta cuenta no reemplaza medición a la corriente real.
- Con tolerancia de −5 %, la resistencia mínima es `330 Ω × 0.95 = 313.5 Ω`. Una cota de falla que trata la caída del LED como cero es `3.2 V / 313.5 Ω ≈ 10.2 mA`. Por tanto, esta versión **no promete** mantener el lazo por debajo de 10 mA.
- Potencia conservadora correspondiente en la resistencia: `3.2² / 313.5 ≈ 0.033 W`, todavía muy inferior a 0.25 W.
- El gate debe repetir el cálculo con tensión máxima documentada de las pilas elegidas, resistencia mínima por tolerancia y límites del LED/módulo exacto. La corriente máxima calculada debe quedar por debajo de la corriente continua permitida con el margen que apruebe el revisor eléctrico; una especificación genérica de “al menos 10 mA” no basta.
- La polaridad importa: el LED es un diodo. El diseño evita aplicar tensión inversa deliberadamente y exige verificar pata larga/ánodo hacia positivo antes de insertar pilas.
- La prueba solo se aplica a objetos aislados de cualquier otra fuente. Las prácticas profesionales de continuidad también exigen probar componentes sin energía externa; véase [Fluke — A Guide to Continuity Testing](https://www.fluke.com/en-ca/learn/blog/digital-multimeters/how-to-test-for-continuity).

**Hallazgo pendiente de piloto:** confirmar visibilidad del LED seleccionado a la corriente real bajo iluminación doméstica. Si no es suficiente, no se reduce la resistencia automáticamente: el gate evalúa otro LED rojo de alta eficiencia con número de parte o el módulo B candidato y registra una nueva revisión antes de seleccionarlo.

## 15. Gates y plan de validación antes de publicar

### Revisiones obligatorias

- [ ] Revisión pedagógica: objetivos observables, lenguaje 5–10 y roles con agencia.
- [ ] Revisión eléctrica/seguridad por profesional competente: componentes exactos, portapilas, corriente con tolerancias, aislamiento, falla segura y advertencias bilingües.
- [ ] Revisión mecánica: terminales, separación, alivio de tensión, resistencia a tirón, fatiga de cinta/cubiertas y conducta ante desprendimiento.
- [ ] Decisión A vs B: comparar riesgo residual, retención mecánica, facilidad de montaje, disponibilidad y valor pedagógico; seleccionar una sola configuración y retirarla otra del bundle familiar de la siguiente versión.
- [ ] Revisión bilingüe `es-US`/`en-US`, con atención especial a `adult-only`, prohibiciones y troubleshooting.
- [ ] QA visual automático y humano de ACT-0003-VIS-01 a ACT-0003-VIS-07.
- [ ] Revisión de accesibilidad y flujo con atención dividida.

### Ejecuciones mínimas propuestas para nivel C y gate reforzado

- [ ] Una ejecución completa del autor/editor con medición de tiempo y registro de componentes exactos.
- [ ] Al menos tres ejecuciones adicionales en dos familias, incluida una dirigida por un adulto que no redactó la actividad.
- [ ] Al menos un caso individual, uno de dos niños y uno de tres niños dentro de 5–10 años.
- [ ] Confirmar evaluación principal de tres niños en menos de 20 segundos.
- [ ] Registrar cada fallo, resultado incierto, intervención adulta, conflicto de roles y desviación de tiempo.

### Casos de prueba de seguridad

- [ ] El control abierto permanece apagado y el cerrado enciende en diez ciclos consecutivos.
- [ ] Con las pilas retiradas, cada unión/cable supera una prueba de tirón cuyo método, fuerza y duración define y registra el revisor competente; no hay desplazamiento, giro, metal fijo expuesto ni daño de aislamiento.
- [ ] El montaje supera diez ciclos completos de preparación, manipulación representativa, control abierto/cerrado, apagado e inspección sin aflojamiento, desprendimiento ni cambio intermitente.
- [ ] Las uniones fijas no quedan accesibles al manejo infantil normal y el alivio de tensión funciona sin depender únicamente de cinta adhesiva.
- [ ] El sistema/editor no acepta sustitución por 9 V, USB, pila tipo moneda, corriente doméstica, líquido o dispositivo.
- [ ] Un objeto con recubrimiento produce explicación `incierto`, no una generalización falsa.
- [ ] Un fallo de control invalida la evidencia de materiales de esa sesión.
- [ ] Ningún componente se calienta perceptiblemente durante pruebas de 2 segundos ni en un control cerrado accidental de 30 segundos; la prueba prolongada la ejecuta únicamente el revisor adulto.

## 16. Trazabilidad

| Requisito/decisión | Implementación en esta ActivityVersion |
|---|---|
| P-01, LRN-006 | Ciclo Discover–Imagine–Build–Experiment–Improve–Explain; práctica, exposición y evaluación separadas. |
| P-02 | Objetos cotidianos; solo el pequeño tester requiere componentes eléctricos definidos. |
| P-03, ACT-002 | Estado `draft`; no entregable hasta publicación y gates. |
| P-05, ACT-004, DEC-034 | Roles y configuraciones reales para 1–3 niños dentro del límite 1–4. |
| P-06, DEC-004–008, EVD-002–006 | Un objetivo y valoración por niño; “Evaluar más” y voz opcionales; cierre bajo 20 s. |
| P-07, EVD-007–009 | Observaciones contextuales, factores externos y corrección; sin etiquetas. |
| P-10, SAFE-001–009 | Riesgos estructurados, pasos adultos, 2 AA, resistencia, prohibiciones y límites de adaptación. |
| P-11 | Adulto cambia objetivos, ayuda, omite evaluación y decide detenerse. |
| ACT-001, ACT-006–012 | Identidad/versionado, bundles bilingües, troubleshooting, revisión y assets ligados a versión. |
| ACT-VIS-001–004, DEC-021, DEC-027 | Briefs fotorealistas/diagramas; QA y aprobación humana; actores correctos. |
| DEC-014 | Mercado de EE. UU., inglés/español, edades 5–10. |
| DEC-026 | La app guía al adulto; el niño participa fuera de pantalla. |

## 17. Resultado editorial requerido para avanzar

Para pasar de `draft` a `pedagogical_review`, el equipo debe decidir formalmente entre A y B, seleccionar números de parte concretos para todos los componentes de la configuración elegida, documentar el diagrama y alivio de tensión, superar la prueba de tirón y diez ciclos, ejecutar el montaje, completar la matriz de resultados con los siete objetos, medir tiempo y brillo y resolver todos los hallazgos del gate. La configuración no elegida se elimina del bundle familiar de la siguiente versión. Cualquier cambio en fuente, resistencia, componente luminoso, retención mecánica, objetos permitidos o pasos de seguridad crea una nueva versión y repite las revisiones afectadas.
