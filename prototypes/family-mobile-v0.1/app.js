const learners = [
  { id: "sofi", name: "Sofi", initials: "SO", age: "5–6 años", color: "cyan" },
  { id: "mateo", name: "Mateo", initials: "MA", age: "7–8 años", color: "yellow" },
  { id: "leo", name: "Leo", initials: "LE", age: "9–10 años", color: "coral" }
];

const learningFocuses = {
  designer: {
    title: "Diseñar y probar una forma",
    objective: "Proponer una forma, construirla y relacionar el resultado de su propia prueba con una decisión de diseño.",
    question: "¿Qué tan independientemente propuso, construyó y probó una forma usando lo que había observado?",
    contribution: "Mateo construirá y probará su propio puente; después propondrá un cambio basado en el resultado.",
    reason: "Sin evidencia previa, este reto abierto ofrece crecimiento apropiado para 7–8 años. La edad orienta la primera oportunidad, no predice su capacidad.",
    exposure: "conteo, plegado, comparación justa y explicación"
  },
  tester: {
    title: "Conteo uno a uno",
    objective: "En su propia prueba, añadir un crayón por turno, decir un número y mantener o recuperar el total después de esperar.",
    question: "¿Qué tan independientemente añadió y contó un crayón a la vez durante su propia prueba?",
    contribution: "Sofi construirá y probará su propio puente; durante su turno hará corresponder un crayón con cada número.",
    reason: "Sin evidencia previa, contar con correspondencia y espera puede consolidar el aprendizaje entre 5–6 años. No asumimos que sea fácil o difícil para ella.",
    exposure: "diseño, estructura, predicción, comparación y explicación"
  },
  coordinator: {
    title: "Comparación justa",
    objective: "Comprobar que distancia, orientación, vaso, papel y carga permanezcan iguales antes de su prueba y las demás.",
    question: "¿Qué tan independientemente comprobó que las condiciones siguieran iguales?",
    contribution: "Leo construirá y probará su propio puente; además usará el checklist de condiciones antes de cada turno.",
    reason: "Sin evidencia previa, controlar varias condiciones ofrece crecimiento posible entre 9–10 años. No se asigna por ser el mayor ni implica dominio.",
    exposure: "diseño, conteo, medición, registro, comparación y comunicación"
  }
};

const stages = [
  {
    name: "Descubrir", time: "6 min", eyebrow: "Vean el problema en acción",
    title: "Prueben primero la hoja plana",
    purpose: "Entender para qué sirven el vaso y los crayones y obtener un resultado real que dé origen al resto de la actividad.",
    entry: "El montaje está listo, pero aún no saben cómo responde una hoja plana.",
    exit: "Tienen una observación y un resultado de referencia para imaginar cambios.",
    skills: ["predicción", "conteo", "carga y flexión"],
    adultActions: [
      "Señala cada función: los libros son apoyos; la hoja es el puente; el vaso vacío irá en el centro y contendrá la carga; cada crayón será una unidad de carga.",
      "Coloca una hoja plana sobre los 15 cm. Pregunta qué creen que ocurrirá y registra una predicción por niño.",
      "Centra el vaso vacío. Tras tres segundos estables, invita a agregar un crayón por turno, decir el número y esperar tres segundos. Detén y registra la última cantidad estable."
    ],
    say: "Este vaso sirve para contener los crayones en el centro del puente. Cada crayón añade una carga igual. ¿Qué creen que hará esta hoja plana cuando el vaso empiece a llenarse?",
    actions: {
      designer: "Predice dónde se doblará; cuando llegue su turno, agrega un crayón y observa la forma.",
      tester: "Comienza el conteo: agrega un crayón, dice un número y espera la señal para el siguiente turno.",
      coordinator: "Predice y comprueba que los libros, la hoja y el vaso no cambien durante la prueba."
    },
    decision: "Cada niño elige cómo expresar su predicción: hablando, señalando o dibujando.",
    observe: "Mira si conectan un crayón con un número y si notan dónde cambia la hoja. Acertar la predicción no es el objetivo.",
    success: "Registraron qué hizo la hoja plana y qué problema deberán resolver; ya existe una razón para imaginar otras formas.",
    warning: "El adulto centra el vaso y mueve los libros. Los niños agregan crayones solo después de la señal, por turnos y sin poner manos o cara debajo.",
    helpOptions: [
      { problem: "Buscan la respuesta correcta", change: "Responde: “Todavía no lo sabemos; la prueba nos dará información”.", impact: "Conserva la predicción como exploración, no como evaluación.", resume: "Vuelve a pedir una idea por voz, gesto o dibujo.", limit: "No empujes la hoja ni hagas una prueba parcial." },
      { problem: "Un niño no quiere responder", change: "Permite que observe y vuelva a participar en otra fase.", impact: "No se registra predicción ni señal negativa.", resume: "Continúa cuando quienes quieran hayan dado su idea.", limit: "No obligar ni atribuir dificultad." }
    ]
  },
  {
    name: "Imaginar", time: "5 min", eyebrow: "Del problema a tres ideas",
    title: "Cada niño elige una forma",
    purpose: "Usar lo observado en la hoja plana, conocer posibilidades y convertir una idea de cada niño en un plan construible.",
    entry: "La hoja plana ya mostró dónde y cuándo se dobla.",
    exit: "Cada niño tiene un diseño propio y todos saben qué condiciones no cambiarán.",
    skills: ["diseño", "comparación justa", "comunicación"],
    adultActions: [
      "Retira vaso y crayones. Pregunta cómo podrían cambiar la forma de una hoja para que sea más difícil de doblar; anota todas las ideas.",
      "Con la hoja plana ya probada, muestra solo el inicio del acordeón: doblar una franja, voltear y doblar otra. Enseña también los diagramas de canal y pliegues anchos.",
      "Pide a cada niño elegir o dibujar una forma para su propia hoja. Confirmen que papel, 15 cm, vaso, crayones y procedimiento seguirán iguales."
    ],
    say: "Ya vimos lo que hizo la hoja plana. ¿Qué forma probará cada uno? Pueden usar acordeón, canal, pliegues anchos o una idea aprobada. ¿Qué debe permanecer igual para comparar?",
    actions: {
      designer: "Elige o dibuja su propia forma y explica qué característica quiere probar.",
      tester: "Elige o dibuja su propia forma y predice más, menos o igual que la hoja plana.",
      coordinator: "Elige o dibuja su propia forma y usa el checklist para nombrar qué debe permanecer igual."
    },
    decision: "Cada niño elige una forma para su propia prueba. No tienen que elegir la misma ni adivinar cuál será mejor.",
    observe: "Mira si cada niño conecta su forma con algo observado en la hoja plana y distingue su cambio de las condiciones fijas.",
    success: "Sofi, Mateo y Leo tienen cada uno un plan identificado; construir es ahora el siguiente paso lógico.",
    warning: "No añadan herramientas, fijaciones, otra hoja ni una carga diferente.",
    helpOptions: [
      { problem: "Un niño tiene demasiadas ideas", change: "Dibuja todas y pídele marcar una sola para su primera hoja.", impact: "Practica elegir sin descartar creatividad; las demás quedan como recomendaciones de mejora.", resume: "Confirma qué cambiará en su diseño y qué seguirá igual.", limit: "No combinar cambios en una misma prueba." },
      { problem: "Un niño no sabe qué forma proponer", change: "Señala dos opciones del diagrama y pídele elegir una para su hoja.", impact: "La elección sigue siendo infantil aunque el conjunto de opciones sea aprobado.", resume: "Pregunta qué cree que ocurrirá con la opción elegida.", limit: "No prometer cuál resistirá más." }
    ]
  },
  {
    name: "Construir", time: "8 min", eyebrow: "Un diseño propio por niño",
    title: "Cada niño construye su puente",
    purpose: "Convertir los tres planes en estructuras identificadas que después puedan probarse por separado.",
    entry: "Cada niño tiene una forma elegida y el grupo conoce las condiciones que seguirán iguales.",
    exit: "Hay una estructura identificada por niño, lista para una prueba individual.",
    skills: ["secuencia", "motricidad", "orientación"],
    adultActions: [
      "Entrega una hoja igual a cada niño y deja aparte la hoja plana que ya probaron. Identifica las nuevas hojas con nombre o símbolo.",
      "Pide que cada niño muestre su plan antes de doblar. Si hace falta, marca guías o estabiliza el papel; no cambies su idea para que ‘gane’.",
      "Al terminar, ordenen las estructuras según el turno de prueba y comprueben que cada una puede apoyarse sobre los dos libros."
    ],
    say: "Ahora cada uno convertirá su idea en un puente. Puede quedar diferente al dibujo; lo importante es poder reconocer qué forma quiso probar.",
    actions: {
      designer: "Construye su propia forma y señala una característica que eligió a propósito.",
      tester: "Construye su propia forma con el apoyo que necesite e identifica su hoja con nombre o símbolo.",
      coordinator: "Construye su propia forma y comprueba que la orientación coincida con el plan de prueba."
    },
    decision: "Cada niño decide cómo realizar su forma y cuándo está suficientemente lista para probarla.",
    observe: "Mira qué partes hace cada niño y qué apoyo necesita. La apariencia no se califica; registra solo acciones relacionadas con su foco.",
    success: "Sofi, Mateo y Leo tienen cada uno una estructura reconocible, identificada y apoyable sobre los libros.",
    warning: "Usen papel intacto; no usen tijeras, clips, cinta en el puente ni otras fijaciones.",
    helpOptions: [
      { problem: "A un niño le cuesta formar su diseño", change: "Estabiliza el papel, marca una guía o modela un solo gesto en la hoja de demostración; luego devuelve la acción al niño.", impact: "Conserva su autoría y hace visible el apoyo recibido.", resume: "Continúa desde la última acción que el niño pueda reconocer.", limit: "No recortar, fijar ni reemplazar silenciosamente su diseño." },
      { problem: "Una estructura quedó desigual o aplastada", change: "Pregunta si quiere probarla así o hacer un ajuste pequeño antes de declarar que está lista.", impact: "El niño decide y el resultado sigue siendo informativo.", resume: "Identifica la hoja y colócala en el orden de prueba.", limit: "No rehacerla hasta ocultar lo que ocurrió." }
    ]
  },
  {
    name: "Experimentar", time: "10 min", eyebrow: "Un turno completo por niño",
    title: "Prueben cada puente por separado",
    purpose: "Dar a cada niño una prueba propia y producir resultados comparables manteniendo iguales las demás condiciones.",
    entry: "Hay tres estructuras identificadas y un resultado de la hoja plana.",
    exit: "Cada niño hizo su prueba y tiene un resultado u observación registrada.",
    skills: ["conteo uno a uno", "control de variables", "observación"],
    adultActions: [
      "Nombra el turno. Antes de cada diseño, restablece los libros a 15 cm, coloca la estructura con apoyo parecido y centra tú el vaso vacío.",
      "Invita al niño de ese turno a añadir un crayón, decir el número y esperar tres segundos antes del siguiente. Los demás observan dónde cambia la forma.",
      "Registra la última cantidad estable o qué ocurrió. Retira vaso y crayones, restablece el montaje y repite hasta que cada niño haya probado su puente."
    ],
    say: "Ahora prueba [nombre]. Tú añadirás y contarás un crayón a la vez. Los demás miramos qué hace la forma. Después reiniciamos el montaje para el siguiente puente.",
    actions: {
      designer: "Prueba su propio diseño, cuenta la carga y relaciona dónde se dobló con una característica de su forma.",
      tester: "Prueba su propio diseño: añade un crayón, dice un número y espera la señal antes de continuar.",
      coordinator: "Comprueba la lista de condiciones y luego prueba su propio diseño con el mismo procedimiento."
    },
    decision: null,
    observe: "En Sofi observa correspondencia entre crayón y número; en Mateo, relación entre forma y resultado; en Leo, control de condiciones. Ver la prueba de otro no reemplaza la propia.",
    success: "Hay un resultado u observación de la hoja plana y de la estructura de Sofi, Mateo y Leo; las pruebas no comparables están marcadas como tales.",
    warning: "Nadie pone cara o manos bajo el montaje. Detente si se mueve un libro, se rompe algo, alguien lanza un crayón o lleva material a la boca.",
    helpOptions: [
      { problem: "El puente se dobló y el vaso cayó", change: "Espera a que el movimiento se detenga. Registra la última cantidad estable y retira las cargas.", impact: "Es un resultado de la estructura, no un error del niño.", resume: "Repite la verificación adulta completa antes del siguiente diseño.", limit: "No perseguir crayones ni añadir una carga distinta." },
      { problem: "El vaso estaba descentrado o se movió un libro", change: "Marca la prueba como NO COMPARABLE; no guardes un número.", impact: "Evita crear evidencia falsa sobre diseño o conteo.", resume: "Restablece una vez los 15 cm, apoyos y vaso vacío.", limit: "Solo el adulto mueve los libros." },
      { problem: "Perdieron el conteo", change: "Detén la prueba, retira toda la carga y vuelve a cero.", impact: "No adivina el resultado; conserva la práctica de conteo.", resume: "Comienza nuevamente con el vaso vacío y la señal adulta.", limit: "No continuar desde un total incierto." }
    ]
  },
  {
    name: "Mejorar", time: "6 min", eyebrow: "Tres recomendaciones, una prueba grupal",
    title: "Elijan y prueben una mejora",
    purpose: "Usar los resultados individuales para recomendar cambios y comprobar juntos una nueva versión.",
    entry: "Cada niño tiene el resultado de su propio diseño y puede compararlo con la hoja plana.",
    exit: "El grupo eligió una recomendación, construyó una versión nueva y registró su prueba.",
    skills: ["iteración", "toma de decisiones", "predicción"],
    adultActions: [
      "Coloca los diseños sin carga junto a sus resultados. Pide a cada niño recomendar un solo cambio y decir qué observación lo inspira.",
      "Ayúdalos a elegir una recomendación o combinar solo características compatibles sin cambiar materiales ni condiciones. Entrega la hoja grupal reservada.",
      "Distribuye acciones para que todos contribuyan a construirla y repitan una vez el procedimiento completo de Experimentar."
    ],
    say: "Cada uno ya tiene información de su puente. ¿Qué cambio recomiendas y qué viste que te hace proponerlo? Elegiremos una idea para probarla juntos.",
    actions: {
      designer: "Recomienda un cambio desde su resultado y ayuda a convertir la idea elegida en la nueva forma.",
      tester: "Recomienda un cambio desde su resultado, predice más, menos o igual y participa en la nueva prueba.",
      coordinator: "Recomienda un cambio, confirma qué permanece igual y registra la decisión y el resultado grupal."
    },
    decision: "Los tres eligen qué recomendación probar y cómo repartirse la construcción y la prueba de la hoja grupal.",
    observe: "Mira si cada recomendación nace de algo visto o contado. La nueva versión puede sostener menos y seguir siendo aprendizaje válido.",
    success: "Cada niño recomendó un cambio y el grupo construyó y probó una nueva versión conservando las condiciones.",
    warning: "No cambien distancia, peso, vaso, número de hojas ni añadan adhesivos. Máximo 20 crayones.",
    helpOptions: [
      { problem: "Quieren cambiar varias cosas", change: "Dibuja todas las ideas y deja que el grupo marque una sola.", impact: "Mantiene la prueba interpretable y conserva las otras ideas.", resume: "Nombra: “Cambiaremos esta parte; las demás condiciones seguirán iguales”.", limit: "No combinar opciones en la tercera hoja." },
      { problem: "El nuevo diseño sostuvo menos", change: "Conserva el dato y pregunta qué pudo influir.", impact: "La iteración se evalúa por decidir y probar, no por ganar.", resume: "Continúa a Explicar con los tres resultados.", limit: "No aumentar distancia o carga para forzar una diferencia." }
    ]
  },
  {
    name: "Explicar", time: "2 min", eyebrow: "Una historia de principio a fin",
    title: "Cada niño cuenta qué aprendió",
    purpose: "Conectar la forma propia, su resultado y la mejora grupal usando algo visto, contado o comparado.",
    entry: "Están visibles la hoja plana, los diseños individuales, la mejora grupal y sus resultados.",
    exit: "Cada niño explicó una conexión propia y el grupo cerró la historia de la investigación.",
    skills: ["explicación", "comparación", "reflexión"],
    adultActions: [
      "Retira todas las cargas y coloca la hoja plana, cada diseño individual y la mejora grupal junto a sus resultados.",
      "Invita a cada niño a señalar su puente, contar qué ocurrió y conectar ese resultado con la mejora elegida. Escucha antes de explicar tú."
    ],
    say: "Señala tu puente: ¿qué hiciste, qué ocurrió en tu prueba y qué recomendaste para la versión del grupo?",
    actions: {
      designer: "Explica una decisión de su forma, su resultado y qué cambiaría después.",
      tester: "Cuenta o compara su resultado usando más, menos o igual y señala la mejora grupal.",
      coordinator: "Nombra una condición que permaneció igual y conecta su prueba con la decisión grupal."
    },
    decision: "Cada niño elige si explica hablando, señalando, dibujando o escogiendo entre los resultados.",
    observe: "Busca una conexión entre diseño y algo observado. Repetir la explicación adulta no cuenta como evidencia independiente.",
    success: "Cada niño comparte una conexión entre su diseño, un resultado y la mejora; el grupo celebra decisiones y método, no el número más alto.",
    warning: "Los diseños están sin carga. Comparen diseños, nunca niños ni habilidades entre hermanos.",
    helpOptions: [
      { problem: "Les cuesta explicar", change: "Señala dos diseños y pregunta: “¿Cuál se dobló antes?” o “¿Cuál sostuvo más?”.", impact: "Acepta gesto, dibujo o elección como forma de comunicación.", resume: "Pide conectar la elección con algo visto o contado.", limit: "No completar la frase por el niño." },
      { problem: "Un niño repite tu explicación", change: "Pregunta: “¿Qué viste tú?” y ofrece señalar los resultados.", impact: "Distingue memoria verbal de observación propia.", resume: "Acepta una respuesta breve y pasa al siguiente niño.", limit: "No corregir hacia una frase científica modelo." }
    ]
  }
];

const ratingScale = [
  { value: 1, label: "Todavía no", detail: "No pudo hacerlo esta vez" },
  { value: 2, label: "Mucha ayuda", detail: "Necesitó guía continua" },
  { value: 3, label: "Alguna ayuda", detail: "Lo hizo con recordatorios" },
  { value: 4, label: "Casi solo", detail: "Solo necesitó una pista" },
  { value: 5, label: "Solo y seguro", detail: "Lo hizo con independencia" }
];

const weeklyActivities = [
  {
    id: "day1", day: "DÍA 1", title: "Puentes de papel", duration: 40, color: "var(--yellow)", activityRef: "ACT-0001 · v0.3.0", status: "Draft",
    promise: "Construyan y comparen puentes hechos con una sola hoja para descubrir cómo la forma puede ayudar al papel a resistir una carga.",
    purpose: "Cambiar la forma de una hoja, hacer pruebas comparables y usar lo observado para mejorar una idea.",
    primaryArea: "Ingeniería", secondaryAreas: ["Física", "Matemáticas", "Motricidad", "Comunicación"], concepts: ["forma", "carga", "rigidez", "comparación justa"],
    focus: "Conteo uno a uno", focusDetail: "Sofi añade un crayón por turno, dice un número y espera antes de continuar.",
    materials: ["6 hojas iguales de papel", "2 libros de tapa dura", "1 vaso de papel", "20 crayones", "regla, marcador y toalla de mano"],
    flow: ["Prueben la hoja plana y registren incluso un resultado de 0.", "Sofi imagina y elige una forma después de observar.", "Construye su propio puente con una hoja igual.", "Añade y cuenta la carga una pieza a la vez.", "Cambia una sola característica y vuelve a probar.", "Explica qué hizo, qué ocurrió y qué cambiaría."],
    closeQuestion: "¿Qué tan independientemente añadió y contó un crayón a la vez durante su prueba?",
    safety: "El adulto mueve los libros y centra el vaso. Nadie pone manos o cara bajo el montaje; detener si se mueve un apoyo, se rompe algo o un material llega a la boca.",
    shopping: [
      { key: "copy-paper", name: "Papel de copia carta o A4", qty: 6, unit: "hojas", section: "Papelería", rule: "sum", detail: "Todas del mismo paquete." },
      { key: "hardcover-books", name: "Libros de tapa dura semejantes", qty: 2, unit: "libros", section: "Casa", rule: "max", detail: "Revisar primero en casa." },
      { key: "paper-cups", name: "Vasos de papel de 8–12 oz", qty: 1, unit: "vaso", section: "Supermercado", rule: "sum", detail: "Vacío, estable y sin deformaciones." },
      { key: "crayons", name: "Crayones estándar intactos", qty: 20, unit: "crayones", section: "Papelería", rule: "max", detail: "Se reutilizan en otros días." },
      { key: "ruler", name: "Regla de 30 cm / 12 in", qty: 1, unit: "regla", section: "Casa", rule: "max", detail: "Sin bordes rotos." },
      { key: "washable-marker", name: "Marcador lavable", qty: 1, unit: "marcador", section: "Papelería", rule: "max", detail: "Se reutiliza durante la semana." },
      { key: "hand-towel", name: "Toalla de mano", qty: 1, unit: "toalla", section: "Casa", rule: "max", detail: "Seca, plana y sin cordones sueltos." },
      { key: "painter-tape", name: "Cinta de pintor removible", qty: 1, unit: "rollo", section: "Papelería", rule: "max", detail: "Opcional; también sirve el día 5." }
    ]
  },
  {
    id: "day2", day: "DÍA 2", title: "Clasificar semillas", duration: 30, color: "var(--cyan)", activityRef: "ACT-0002 · v0.1.1", status: "Draft",
    promise: "Observen la misma colección y descubran que puede organizarse de distintas maneras usando reglas claras.",
    purpose: "Atender a atributos, aplicar una regla, comparar grupos y volver a organizar la misma colección.",
    primaryArea: "Matemáticas y datos", secondaryAreas: ["Naturaleza", "Lenguaje", "Motricidad"], concepts: ["atributo", "categoría", "regla", "más/menos/igual"],
    focus: "Clasificar con una regla", focusDetail: "Sofi decide dónde va cada pieza y puede explicar la regla con palabras, gesto o ejemplo.",
    materials: ["12 garbanzos", "12 frijoles negros", "12 frijoles pintos", "12 guisantes verdes secos", "bandeja, 5 recipientes, papel y marcador"],
    flow: ["Observen cuatro piezas distintas sin probarlas.", "Sofi propone una regla usando algo visible.", "Clasifica una pieza a la vez y usa ‘todavía no sé’ si hace falta.", "Prueben una pieza dudosa y aclaren la regla.", "Cuenten y comparen los grupos.", "Mezclen de nuevo y creen otra clasificación."],
    closeQuestion: "¿Qué tan independientemente usó una regla para decidir dónde iba cada pieza?",
    safety: "Manipulativos no comestibles. Ejecutar solo sin alergia conocida o sospechada y con supervisión continua. Detener ante pieza cerca de boca, nariz u oído, ingestión sospechada o reacción.",
    shopping: [
      { key: "chickpeas", name: "Garbanzos secos sellados", qty: 1, unit: "bolsa pequeña", section: "Supermercado", rule: "sum", detail: "Usar 12 piezas; no devolver a la despensa." },
      { key: "black-beans", name: "Frijoles negros secos sellados", qty: 1, unit: "bolsa pequeña", section: "Supermercado", rule: "sum", detail: "Usar 12 piezas; no devolver a la despensa." },
      { key: "pinto-beans", name: "Frijoles pintos secos sellados", qty: 1, unit: "bolsa pequeña", section: "Supermercado", rule: "sum", detail: "Usar 12 piezas; no devolver a la despensa." },
      { key: "green-peas", name: "Guisantes verdes secos sellados", qty: 1, unit: "bolsa pequeña", section: "Supermercado", rule: "sum", detail: "Usar 12 piezas; no devolver a la despensa." },
      { key: "rimmed-tray", name: "Bandeja con borde", qty: 1, unit: "bandeja", section: "Casa", rule: "max", detail: "Irrompible y fácil de limpiar." },
      { key: "small-containers", name: "Recipientes pequeños irrompibles", qty: 5, unit: "recipientes", section: "Casa", rule: "max", detail: "Para grupos y ‘todavía no sé’." },
      { key: "rigid-container", name: "Recipiente rígido con tapa", qty: 1, unit: "recipiente", section: "Casa", rule: "max", detail: "Solo para materiales de actividades." },
      { key: "washable-marker", name: "Marcador lavable", qty: 1, unit: "marcador", section: "Papelería", rule: "max", detail: "Reutilizar el de otros días." }
    ]
  },
  {
    id: "day3", day: "DÍA 3", title: "Transportar agua", duration: 30, color: "var(--mint)", activityRef: "CAND-0001 · v0.0.1", status: "Candidato",
    promise: "Prueben varias herramientas para descubrir cuál mueve más agua con el mismo número de viajes.",
    purpose: "Comparar volumen de manera visible y mejorar un procedimiento sin convertirlo en una carrera.",
    primaryArea: "Lógica y matemáticas", secondaryAreas: ["Vida práctica", "Motricidad", "Ingeniería"], concepts: ["volumen", "absorción", "derrame", "comparación justa"],
    focus: "Comparar usando niveles", focusDetail: "Sofi mantiene tres viajes por herramienta y usa las marcas de agua para elegir.",
    materials: ["2 recipientes plásticos medianos", "esponja limpia", "cuchara grande", "taza medidora plástica", "agua y toalla grande"],
    flow: ["El adulto prepara un recipiente con poca agua y otro vacío.", "Sofi predice qué herramienta dejará el nivel más alto.", "Hace tres viajes con cada herramienta.", "El adulto marca el nivel y reinicia la misma cantidad.", "Comparan las marcas y registran derrames.", "Sofi mejora una acción y repite tres viajes."],
    closeQuestion: "¿Qué tan independientemente comparó los niveles y usó el resultado para elegir una herramienta?",
    safety: "Secar derrames inmediatamente. No correr, beber el agua, acercar la cara, usar vidrio, agua caliente, jabón ni herramientas de succión oral.",
    shopping: [
      { key: "sponge", name: "Esponja nueva sin partes sueltas", qty: 1, unit: "esponja", section: "Supermercado", rule: "sum", detail: "Sin cara abrasiva desprendible." },
      { key: "medium-bowls", name: "Recipientes plásticos medianos", qty: 2, unit: "recipientes", section: "Casa", rule: "max", detail: "Irrompibles, 2–4 litros." },
      { key: "large-spoon", name: "Cuchara grande", qty: 1, unit: "cuchara", section: "Casa", rule: "max", detail: "Sin bordes dañados." },
      { key: "measuring-cup", name: "Taza medidora plástica pequeña", qty: 1, unit: "taza", section: "Casa", rule: "max", detail: "Irrompible." },
      { key: "large-towel", name: "Toalla grande", qty: 1, unit: "toalla", section: "Casa", rule: "max", detail: "Se reutiliza el día 4." }
    ]
  },
  {
    id: "day4", day: "DÍA 4", title: "Barco de aluminio", duration: 35, color: "var(--coral)", activityRef: "CAND-0002 · v0.0.1", status: "Candidato",
    promise: "Diseñen una forma que flote y comprueben cómo puede distribuir una carga.",
    purpose: "Relacionar forma y flotación mediante una primera versión y una mejora comprobable.",
    primaryArea: "Ingeniería", secondaryAreas: ["Física", "Conteo", "Motricidad"], concepts: ["flotación", "volumen interior", "carga", "distribución"],
    focus: "Elegir y probar una mejora", focusDetail: "Sofi cambia una sola característica del barco y compara qué ocurrió.",
    materials: ["3 cuadrados de papel aluminio", "recipiente ancho con poca agua", "20 palitos de madera", "toalla grande", "papel y crayón"],
    flow: ["Sofi imagina una forma con espacio seco para carga.", "Construye un primer barco con un cuadrado de aluminio.", "Añade un palito a la vez y cuenta.", "Registran la última cantidad estable.", "Elige un cambio: base, lados o distribución.", "Construye la segunda versión y compara."],
    closeQuestion: "¿Qué tan independientemente eligió una mejora y comprobó qué ocurrió?",
    safety: "El adulto llena, vacía y mueve el recipiente. Detener ante borde de aluminio cortante, agua en el piso o cara cerca del recipiente. No usar monedas, canicas, vidrio ni agua caliente.",
    shopping: [
      { key: "aluminum-foil", name: "Papel aluminio resistente", qty: 1, unit: "rollo", section: "Supermercado", rule: "max", detail: "Permite cortar tres cuadrados de 30 × 30 cm." },
      { key: "craft-sticks", name: "Palitos de madera para manualidades", qty: 20, unit: "palitos", section: "Papelería", rule: "max", detail: "Grandes, lisos y sin astillas." },
      { key: "wide-basin", name: "Recipiente plástico ancho", qty: 1, unit: "recipiente", section: "Casa", rule: "max", detail: "Irrompible y estable." },
      { key: "large-towel", name: "Toalla grande", qty: 1, unit: "toalla", section: "Casa", rule: "max", detail: "Reutilizar la del día 3." },
      { key: "crayons", name: "Crayones estándar intactos", qty: 1, unit: "crayón", section: "Papelería", rule: "max", detail: "Ya incluido en el conjunto del día 1." }
    ]
  },
  {
    id: "day5", day: "DÍA 5", title: "Torre de vasos", duration: 30, color: "var(--yellow)", activityRef: "CAND-0003 · v0.0.1", status: "Candidato",
    promise: "Construyan, prueben y mejoren una torre usando siempre el mismo conjunto de piezas.",
    purpose: "Observar dónde pierde estabilidad una estructura y usar esa información para cambiar una sola cosa.",
    primaryArea: "Ingeniería espacial", secondaryAreas: ["Medición", "Patrones", "Motricidad"], concepts: ["base", "altura", "equilibrio", "estabilidad"],
    focus: "Mejorar estabilidad", focusDetail: "Sofi identifica un cambio y prueba si la torre permanece estable durante una cuenta de diez.",
    materials: ["12 vasos de papel iguales", "6 tarjetas de cartulina o cartón", "regla", "papel y crayón", "cinta de pintor opcional"],
    flow: ["Sofi imagina qué necesita una torre para no caer.", "Elige una base y un patrón.", "Construye sin que el adulto sostenga la torre.", "Retiran las manos y cuentan hasta diez.", "Observan dónde comenzó a cambiar.", "Sofi modifica una característica y vuelve a probar."],
    closeQuestion: "¿Qué tan independientemente identificó un cambio y probó si hacía la torre más estable?",
    safety: "Construir solo dentro del alcance seguro. No subirse a muebles, lanzar piezas, usar objetos pesados como carga ni fijar la torre con cinta.",
    shopping: [
      { key: "paper-cups", name: "Vasos de papel de 8–12 oz", qty: 12, unit: "vasos", section: "Supermercado", rule: "sum", detail: "Mismo tipo que el día 1; total semanal sumado." },
      { key: "cardstock", name: "Tarjetas de cartulina o cartón fino", qty: 6, unit: "tarjetas", section: "Papelería", rule: "sum", detail: "Iguales, sin grapas ni bordes cortantes." },
      { key: "ruler", name: "Regla de 30 cm / 12 in", qty: 1, unit: "regla", section: "Casa", rule: "max", detail: "Reutilizar la del día 1." },
      { key: "painter-tape", name: "Cinta de pintor removible", qty: 1, unit: "rollo", section: "Papelería", rule: "max", detail: "Solo para marcar el área, no fijar la torre." },
      { key: "crayons", name: "Crayones estándar intactos", qty: 1, unit: "crayón", section: "Papelería", rule: "max", detail: "Ya incluido en el conjunto del día 1." }
    ]
  }
];

const shoppingSectionMeta = {
  Supermercado: { code: "SUP", note: "Alimentos secos, hogar y desechables" },
  Papelería: { code: "PAP", note: "Papelería y manualidades" },
  Casa: { code: "CASA", note: "Revisa primero; compra solo si falta" }
};

function aggregateShopping(activities = weeklyActivities) {
  const items = new Map();
  activities.forEach((activity) => activity.shopping.forEach((requirement) => {
    const source = { day: activity.day, title: activity.title, qty: requirement.qty, unit: requirement.unit };
    if (!items.has(requirement.key)) {
      items.set(requirement.key, { ...requirement, sources: [source] });
      return;
    }
    const aggregate = items.get(requirement.key);
    aggregate.qty = aggregate.rule === "sum" ? aggregate.qty + requirement.qty : Math.max(aggregate.qty, requirement.qty);
    aggregate.sources.push(source);
  }));
  return [...items.values()];
}

const storageKey = "kids-learning-system-founder-pilot-v1";
const persistableScreens = ["today", "focus", "prep", "session", "close", "saved", "plan", "planned-activity", "journey", "family"];
const defaultState = {
  screen: "today",
  time: 45,
  selected: ["sofi", "mateo", "leo"],
  assignments: { sofi: "tester", mateo: "designer", leo: "coordinator" },
  participation: { sofi: "active", mateo: "active", leo: "active" },
  materials: { paper: true, supports: true, crayons: true, cup: false, ruler: false, marker: false, towel: false, surface: false },
  stage: 0,
  highestStage: 0,
  offline: !navigator.onLine,
  paused: false,
  ratings: {},
  skipped: {},
  note: "",
  supportUsed: {},
  closeStartedAt: null,
  savedElapsed: null,
  planView: "activities",
  selectedPlanDay: "day1",
  shoppingChecked: {}
};

function loadLocalState() {
  const restored = {
    ...defaultState,
    selected: [...defaultState.selected],
    assignments: { ...defaultState.assignments },
    participation: { ...defaultState.participation },
    materials: { ...defaultState.materials },
    ratings: {},
    skipped: {},
    supportUsed: {},
    shoppingChecked: {}
  };

  try {
    const stored = JSON.parse(localStorage.getItem(storageKey) || "null");
    if (!stored || stored.version !== 1 || typeof stored.state !== "object") return restored;
    const candidate = stored.state;
    if (persistableScreens.includes(candidate.screen)) restored.screen = candidate.screen;
    if ([30, 45, 60].includes(candidate.time)) restored.time = candidate.time;
    if (Array.isArray(candidate.selected)) restored.selected = candidate.selected.filter((id) => learners.some((learner) => learner.id === id));
    if (candidate.materials && typeof candidate.materials === "object") restored.materials = { ...restored.materials, ...candidate.materials };
    if (Number.isInteger(candidate.stage) && candidate.stage >= 0 && candidate.stage < stages.length) restored.stage = candidate.stage;
    if (Number.isInteger(candidate.highestStage) && candidate.highestStage >= 0 && candidate.highestStage < stages.length) restored.highestStage = candidate.highestStage;
    if (candidate.ratings && typeof candidate.ratings === "object") restored.ratings = candidate.ratings;
    if (candidate.skipped && typeof candidate.skipped === "object") restored.skipped = candidate.skipped;
    if (typeof candidate.note === "string") restored.note = candidate.note.slice(0, 2000);
    if (candidate.supportUsed && typeof candidate.supportUsed === "object") restored.supportUsed = candidate.supportUsed;
    if (["activities", "shopping"].includes(candidate.planView)) restored.planView = candidate.planView;
    if (weeklyActivities.some((activity) => activity.id === candidate.selectedPlanDay)) restored.selectedPlanDay = candidate.selectedPlanDay;
    if (candidate.shoppingChecked && typeof candidate.shoppingChecked === "object") restored.shoppingChecked = candidate.shoppingChecked;
  } catch (error) {
    console.warn("No se pudo restaurar el avance local del prototipo.", error);
  }

  restored.offline = !navigator.onLine;
  restored.paused = false;
  restored.closeStartedAt = restored.screen === "close" ? Date.now() : null;
  return restored;
}

function persistLocalState() {
  const snapshot = {
    screen: state.screen,
    time: state.time,
    selected: state.selected,
    materials: state.materials,
    stage: state.stage,
    highestStage: state.highestStage,
    ratings: state.ratings,
    skipped: state.skipped,
    note: state.note,
    supportUsed: state.supportUsed,
    planView: state.planView,
    selectedPlanDay: state.selectedPlanDay,
    shoppingChecked: state.shoppingChecked
  };
  try {
    localStorage.setItem(storageKey, JSON.stringify({ version: 1, savedAt: new Date().toISOString(), state: snapshot }));
  } catch (error) {
    console.warn("No se pudo conservar el avance local del prototipo.", error);
  }
}

const query = new URLSearchParams(window.location.search);
if (query.get("reset") === "1") {
  try { localStorage.removeItem(storageKey); } catch (error) { console.warn("No se pudo reiniciar el estado local.", error); }
  query.delete("reset");
  const remainingQuery = query.toString();
  window.history.replaceState({}, "", `${window.location.pathname}${remainingQuery ? `?${remainingQuery}` : ""}${window.location.hash}`);
}
const state = loadLocalState();

const requestedPreview = query.get("screen");
const normalizedPreview = requestedPreview === "roles" ? "focus" : requestedPreview;
if (["today", "focus", "prep", "session", "close", "summary", "saved", "plan", "planned-activity", "journey", "family"].includes(normalizedPreview)) {
  state.screen = normalizedPreview;
  if (requestedPreview === "close") state.closeStartedAt = Date.now();
}
const requestedDay = query.get("day");
if (weeklyActivities.some((activity) => activity.id === requestedDay)) state.selectedPlanDay = requestedDay;
const requestedPlanView = query.get("view");
if (["activities", "shopping"].includes(requestedPlanView)) state.planView = requestedPlanView;
const requestedStage = Number(query.get("stage"));
if (Number.isInteger(requestedStage) && requestedStage >= 0 && requestedStage < stages.length) state.stage = requestedStage;

const view = document.querySelector("#view");
const app = document.querySelector("#app");
const appHeader = document.querySelector("#appHeader");
const bottomNav = document.querySelector("#bottomNav");
const sheet = document.querySelector("#sheet");
const sheetContent = document.querySelector("#sheetContent");
const scrim = document.querySelector("#scrim");
const toast = document.querySelector("#toast");
const connectionText = document.querySelector("#connectionText");
let lastFocus = null;
let toastTimer = null;
let deferredInstallPrompt = null;

const icon = (name) => `<svg aria-hidden="true"><use href="#i-${name}"></use></svg>`;
const learnerById = (id) => learners.find((learner) => learner.id === id);
const activeLearners = () => state.selected.map(learnerById).filter(Boolean);
const evaluableLearners = () => activeLearners().filter((learner) => state.participation[learner.id] === "active");
const focusFor = (id) => learningFocuses[state.assignments[id]];
const isTopLevel = () => ["today", "plan", "journey", "family"].includes(state.screen);

function avatar(learner) {
  return `<span class="avatar" data-color="${learner.color}" aria-hidden="true">${learner.initials}</span>`;
}

function flowHeader(title, subtitle, backTarget, action = "") {
  return `<header class="flow-header">
    <button data-action="navigate" data-target="${backTarget}" aria-label="Volver">${icon("back")}</button>
    <div><h1>${title}</h1><small>${subtitle}</small></div>
    ${action || "<span></span>"}
  </header>`;
}

function setScreen(screen, options = {}) {
  state.screen = screen;
  if (screen === "close" && !state.closeStartedAt) state.closeStartedAt = Date.now();
  closeSheet();
  render();
  if (!options.preserveScroll) view.scrollTop = 0;
  requestAnimationFrame(() => view.focus({ preventScroll: true }));
}

function render() {
  const topLevel = isTopLevel();
  appHeader.hidden = !topLevel;
  bottomNav.hidden = !topLevel;
  view.classList.toggle("no-bottom", !topLevel);
  app.classList.toggle("is-offline", state.offline);
  connectionText.textContent = state.offline ? "Sin conexión" : "En línea";
  [...bottomNav.querySelectorAll("button")].forEach((button) => button.classList.toggle("is-active", button.dataset.target === state.screen));

  const renderers = {
    today: renderToday,
    plan: renderPlan,
    "planned-activity": renderPlannedActivity,
    journey: renderJourney,
    family: renderFamily,
    focus: renderLearningPlan,
    prep: renderPrep,
    session: renderSession,
    close: renderClose,
    summary: renderSummary,
    saved: renderSaved
  };
  view.innerHTML = (renderers[state.screen] || renderToday)();
  persistLocalState();
}

function renderToday() {
  const ready = state.selected.length > 0;
  return `<section class="screen">
    <p class="eyebrow">Domingo · prueba familiar</p>
    <h1>Una tarde para<br>pensar <span style="color:#0b8394">juntos.</span></h1>
    <p class="lead">Elige cuánto tiempo tienen. La actividad se adapta al grupo antes de empezar.</p>

    ${state.offline ? `<div class="offline-banner" style="margin-top:18px">${icon("signal")}<span>El plan está disponible en este dispositivo. Puedes continuar; este prototipo no sincroniza con un servidor.</span></div>` : ""}

    <div class="section-head"><h2>Tiempo disponible</h2><span class="caption">incluye cierre</span></div>
    <div class="choice-row" aria-label="Tiempo disponible">
      ${[30, 45, 60].map((minutes) => `<button class="choice ${state.time === minutes ? "is-selected" : ""}" data-action="select-time" data-value="${minutes}">${minutes} min<small>${minutes === 30 ? "versión breve" : minutes === 45 ? "recomendado" : "con extensión"}</small></button>`).join("")}
    </div>

    <div class="section-head"><h2>¿Quiénes participan?</h2><span class="caption">1–4 en producto · 3 en demo</span></div>
    <div class="participant-grid">
      ${learners.map((learner) => `<button class="participant ${state.selected.includes(learner.id) ? "is-selected" : ""}" data-action="toggle-participant" data-id="${learner.id}" aria-pressed="${state.selected.includes(learner.id)}">
        <span class="participant-check">${state.selected.includes(learner.id) ? "✓" : ""}</span>${avatar(learner)}<strong>${learner.name}</strong><small>${learner.age}</small>
      </button>`).join("")}
    </div>

    <div class="section-head"><h2>Actividad sugerida</h2><span class="tag coral">Vista previa · Draft</span></div>
    <article class="hero">
      <div><span class="tag yellow">ACT-0001 · v0.3.0</span><h2>Puentes<br>de <span>papel</span></h2><p>Construyan y comparen puentes hechos con una sola hoja para descubrir cómo la forma puede ayudar al papel a resistir una carga.</p></div>
      <div class="hero-meta"><div><strong>${state.time}</strong><small>minutos</small></div><div><strong>${state.selected.length}</strong><small>participantes</small></div><div><strong>A</strong><small>riesgo bajo</small></div></div>
    </article>
    <p class="caption" style="margin:10px 2px 0">Este prototipo usa una actividad Draft para validar la experiencia. Una familia real solo recibiría contenido publicado.</p>

    <div class="action-dock"><button class="button primary block" data-action="navigate" data-target="focus" ${ready ? "" : "disabled"}>Ver cómo aprenderán ${icon("arrow")}</button></div>
  </section>`;
}

function renderLearningPlan() {
  return `<section class="screen">
    ${flowHeader("Qué van a explorar", `${activeLearners().length} participantes · ${state.time} min`, "today")}
    <p class="eyebrow">Mapa educativo</p>
    <h2>No es solo construir un puente.</h2>
    <p class="lead">Van a cambiar la forma de una hoja, hacer pruebas comparables y usar lo observado para mejorar una idea.</p>

    <article class="learning-map" style="margin-top:18px">
      <div class="learning-primary"><span class="tag yellow">Área principal</span><h3>Ingeniería</h3><p>Estructuras, diseño e iteración.</p></div>
      <div class="learning-secondary"><p class="eyebrow">Áreas secundarias</p><div class="tag-row"><span class="tag">Física</span><span class="tag">Matemáticas</span><span class="tag">Lógica</span><span class="tag">Motricidad</span><span class="tag">Comunicación</span></div></div>
      <div class="learning-explainer"><p class="eyebrow">Por qué funciona</p><p>La forma cambia cómo el papel resiste doblarse. Mantener iguales distancia, vaso, papel y carga permite relacionar el resultado con esa forma.</p></div>
      <div class="concept-row"><span>Estructura</span><span>Carga</span><span>Rigidez</span><span>Forma</span><span>Comparación justa</span></div>
    </article>

    <article class="child-decision-card" style="margin-top:12px"><span class="decision-mark">?</span><div><p class="eyebrow">Decisiones de los niños</p><strong>Cada niño elegirá la forma de su puente; después decidirán juntos qué mejora probar.</strong><p>La seguridad y las condiciones de comparación permanecen fijas.</p></div></article>

    <div class="section-head"><h2>Foco sugerido por niño</h2><span class="caption">automático y explicable</span></div>
    <div class="stack">
      ${activeLearners().map((learner) => {
        const focus = focusFor(learner.id);
        return `<article class="focus-card" data-color="${learner.color}">
          <div class="focus-head">${avatar(learner)}<div><span class="caption">Sugerido para ${learner.name}</span><h3>${focus.title}</h3></div></div>
          <p class="focus-objective">${focus.objective}</p>
          <div class="focus-detail"><strong>Su aporte</strong><p>${focus.contribution}</p></div>
          <div class="focus-reason"><strong>¿Por qué este foco?</strong><p>${focus.reason}</p></div>
          <p class="caption"><strong>También tendrá oportunidades de:</strong> ${focus.exposure}.</p>
        </article>`;
      }).join("")}
    </div>
    <div class="action-dock"><button class="button primary block" data-action="navigate" data-target="prep">Ver preparación ${icon("arrow")}</button></div>
  </section>`;
}

function renderPrep() {
  const entries = [
    ["paper", "6 hojas iguales de papel carta o A4", "Es el puente cuya forma cambia: 1 referencia plana, 1 por niño, 1 mejora grupal y 1 para plan y resultados."],
    ["supports", "2 libros de tapa dura, planos y de igual altura", "Forman los apoyos del puente a 15 cm; no apilarlos."],
    ["cup", "1 vaso liviano de papel, 8–12 oz", "Mantiene los crayones reunidos y centrados; debe estar vacío, estable y sin deformaciones."],
    ["crayons", "20 crayones estándar intactos", "Son unidades de carga añadidas una a una; mismo tamaño aproximado y sin fragmentos."],
    ["ruler", "1 regla de 30 cm / 12 in", "Mantiene la misma distancia entre apoyos; sin bordes rotos."],
    ["marker", "1 lápiz o marcador lavable", "Registra predicciones y resultados sin depender de la memoria."],
    ["towel", "1 toalla de mano seca y plana", "Amortigua la caída y evita que los crayones rueden; nunca toca ni sostiene el puente."],
    ["surface", "Mesa firme, seca y despejada", "Mantiene el montaje estable, lejos del borde y de zonas de paso."]
  ];
  const checked = entries.filter(([id]) => state.materials[id]).length;
  const ready = checked === entries.length;
  return `<section class="screen">
    ${flowHeader("Preparación", `${checked} de ${entries.length} listos`, "focus")}
    <p class="eyebrow">5–7 minutos del adulto</p><h2>Reúne y verifica.</h2>
    <p class="lead">Los niños pueden ayudar a contar. El adulto inspecciona materiales y prepara el montaje seguro.</p>
    <div class="progress-meter" style="margin:18px 0 10px"><i style="width:${checked / entries.length * 100}%"></i></div>
    <article class="card"><ul class="checklist">
      ${entries.map(([id, label, detail]) => `<li><label class="check-label detailed"><input type="checkbox" data-action="material" data-id="${id}" ${state.materials[id] ? "checked" : ""}><span class="check-box"></span><span><strong>${label}</strong><small>${detail}</small></span></label></li>`).join("")}
    </ul></article>

    <p class="caption" style="margin:9px 3px 0">Opcional: 4 trozos de cinta de pintor para marcar la posición exterior de los libros. Nunca fijar el puente.</p>

    <div class="section-head"><h2>Prepara el montaje</h2><span class="tag yellow">Solo adulto</span></div>
    <article class="setup-card">
      <ol class="setup-list">
        <li><span>1</span><p>Extiende la toalla en una sola capa bajo el espacio: amortiguará una caída y evitará que los crayones rueden, pero no debe tocar el puente. Coloca los libros completamente planos.</p></li>
        <li><span>2</span><p>Deja exactamente <strong>15 cm / 6 in</strong> entre los bordes interiores. Marca su posición si puedes.</p></li>
        <li><span>3</span><p>Comprueba el vaso vacío sobre la mesa: debe permanecer estable durante una cuenta lenta de tres.</p></li>
        <li><span>4</span><p>Deja los 20 crayones dentro de tu alcance, lejos del borde. Solo tú moverás los libros.</p></li>
      </ol>
    </article>

    <div class="section-head"><h2>Lo que necesitas saber</h2><span class="tag cyan">guía adulta</span></div>
    <article class="adult-knowledge">
      <p class="eyebrow">Explicación breve</p>
      <h3>La forma puede hacer al papel más difícil de doblar.</h3>
      <p>Una hoja plana tiene poca altura y se flexiona fácilmente. Los pliegues crean pequeñas paredes. Eso puede aumentar la rigidez, pero no garantiza que una forma siempre gane: por eso se prueba.</p>
      <div class="guide-options">
        <div class="guide-option"><div class="shape channel"></div><strong>Canal</strong><br>Bordes levantados.</div>
        <div class="guide-option"><div class="shape accordion"><i></i><i></i><i></i><i></i></div><strong>Acordeón</strong><br>Varios pliegues.</div>
        <div class="guide-option"><div class="shape wide"><i></i><i></i><i></i></div><strong>Pliegues anchos</strong><br>Pocas crestas.</div>
        <div class="guide-option"><div class="shape guide"></div><strong>Guías rectas</strong><br>Ayuda visual.</div>
      </div>
      <blockquote>“No necesitamos saber cuál es mejor. Cada niño elige una forma, mantenemos lo demás igual y dejamos que las pruebas nos den información”.</blockquote>
    </article>
    <article class="safety-card" style="margin-top:12px"><b>${icon("alert")}</b><div><strong>Control del adulto</strong><p>Tú colocas, mides y reajustas los libros y centras el vaso antes de cada prueba. Los niños añaden los crayones por turnos. Detén la actividad si un soporte se mueve, algo se rompe, se lanza un crayón o un material llega a la boca.</p></div></article>
    <div class="action-dock"><button class="button primary block" data-action="start-session" ${ready ? "" : "disabled"}>Empezar actividad ${icon("play")}</button></div>
  </section>`;
}

function stageVisual(stageName) {
  const key = stageName.toLowerCase();
  const visuals = {
    descubrir: `<div class="mini-bridge"><i></i><b></b><i></i><span class="mini-cup">0</span></div>`,
    imaginar: `<div class="mini-shapes"><span class="mini-channel"></span><span class="mini-accordion">/\/\/</span><span class="mini-wide">/‾\</span></div>`,
    construir: `<div class="mini-build"><span>plan</span><b>→</b><span>plegar</span><b>→</b><span>listo</span></div>`,
    experimentar: `<div class="mini-turns">${activeLearners().map((learner, index) => `<span>${learner.initials}</span>${index < activeLearners().length - 1 ? "<b>→</b>" : ""}`).join("")}</div>`,
    mejorar: `<div class="mini-improve"><span>1</span><b>+ una idea</b><span>2</span></div>`,
    explicar: `<div class="mini-explain"><span>Hice…</span><span>Vi…</span><span>Cambiaría…</span></div>`
  };
  const labels = {
    descubrir: "Hoja plana entre dos apoyos con el vaso vacío como resultado cero posible",
    imaginar: "Tres formas posibles: canal, acordeón y pliegues anchos",
    construir: "Secuencia de plan, plegado y estructura lista",
    experimentar: "Un turno completo de prueba por niño",
    mejorar: "Primera versión, una sola mejora y segunda versión",
    explicar: "Explicación conectando lo que se hizo, observó y cambiaría"
  };
  return `<div class="stage-visual ${key}" role="img" aria-label="${labels[key]}">${visuals[key]}</div>`;
}

function renderSession() {
  const stage = stages[state.stage];
  const chosenSupport = state.supportUsed[state.stage] !== undefined ? stage.helpOptions[state.supportUsed[state.stage]] : null;
  return `<section class="screen">
    ${flowHeader("Puentes de papel", `${state.stage + 1} de ${stages.length} · ${stage.name}`, "prep", `<button data-action="pause" aria-label="Pausar">${icon(state.paused ? "play" : "pause")}</button>`)}
    ${state.offline ? `<div class="offline-banner">${icon("signal")}<span>Modo sin conexión. Las instrucciones, la ayuda y el avance local siguen disponibles.</span></div>` : ""}
    <div class="stage-track" aria-label="Etapas de la actividad">
      ${stages.map((item, index) => `<button class="stage-button ${index === state.stage ? "is-current" : ""}" data-action="stage" data-value="${index}"><strong>${index + 1}. ${item.name}</strong><small>${item.time}</small></button>`).join("")}
    </div>
    <article class="stage-brief">
      <div class="stage-brief-copy"><p class="eyebrow">${stage.eyebrow}</p><h2>${stage.title}</h2><p>${stage.purpose}</p><p class="stage-entry"><strong>Parten de:</strong> ${stage.entry}</p></div>
      ${stageVisual(stage.name)}
      <div class="stage-skill-line"><strong>Practican aquí</strong>${stage.skills.map((skill) => `<span>${skill}</span>`).join("")}</div>
    </article>
    <article class="facilitation-block" style="margin-top:12px">
      <header><span class="block-number">1</span><div><p class="eyebrow">Adulto</p><h3>Haz esto</h3></div></header>
      <ol class="adult-actions">${stage.adultActions.map((action) => `<li>${action}</li>`).join("")}</ol>
      <div class="say-box"><span>Diles</span><p>“${stage.say}”</p></div>
    </article>

    <article class="safety-card" style="margin-top:12px"><b>${icon("alert")}</b><div><strong>Durante este paso</strong><p>${stage.warning}</p></div></article>

    <article class="facilitation-block participant-actions" style="margin-top:12px">
      <header><span class="block-number cyan">2</span><div><p class="eyebrow">Los niños</p><h3>Ahora cada uno</h3></div></header>
      ${stage.name === "Experimentar" ? `<div class="turn-order"><strong>Un turno completo a la vez</strong><span>${activeLearners().map((learner) => learner.name).join(" → ")}</span></div>` : ""}
      ${activeLearners().map((learner) => `<div class="named-action">${avatar(learner)}<div><strong>${learner.name}</strong><p>${stage.actions[state.assignments[learner.id]]}</p></div></div>`).join("")}
      ${stage.decision ? `<div class="inline-decision"><span>?</span><p><strong>Ellos deciden</strong>${stage.decision}</p></div>` : ""}
    </article>

    <article class="step-checks" style="margin-top:12px">
      <div><span>◎</span><p><strong>Observa sin interrumpir</strong>${stage.observe}</p></div>
      <div><span>✓</span><p><strong>Continúa cuando</strong>${stage.success}</p></div>
      <p class="stage-exit"><strong>Así conecta:</strong> ${stage.exit}</p>
    </article>
    ${chosenSupport ? `<article class="applied-support" style="margin-top:12px"><strong>Apoyo elegido: ${chosenSupport.problem}</strong><p>${chosenSupport.change}</p><small>Reanuda: ${chosenSupport.resume}</small></article>` : ""}
    <button class="button secondary block" style="margin-top:12px" data-action="help">${icon("help")} ${chosenSupport ? "Revisar ayuda elegida" : "Ayuda con este paso"}</button>
    <div class="action-dock" style="display:grid;grid-template-columns:${state.stage > 0 ? "54px 1fr" : "1fr"};gap:8px">
      ${state.stage > 0 ? `<button class="button secondary" data-action="previous-stage" aria-label="Paso anterior">${icon("back")}</button>` : ""}
      <button class="button primary block" data-action="next-stage">${state.stage === stages.length - 1 ? "Cerrar actividad" : `Siguiente: ${stages[state.stage + 1].name}`} ${icon("arrow")}</button>
    </div>
  </section>`;
}

function renderClose() {
  const complete = evaluableLearners().every((learner) => state.ratings[learner.id] || state.skipped[learner.id]);
  return `<section class="screen">
    ${flowHeader("Cierre rápido", "Una observación por niño", "session", `<button data-action="close-info" aria-label="Por qué preguntamos">?</button>`)}
    <div class="close-intro"><p class="eyebrow">Objetivo principal de hoy</p><h2>¿Cuánta ayuda necesitó?</h2><p class="lead">No mide inteligencia ni califica al niño. Describe solamente lo que observaste en esta actividad.</p></div>
    <div class="stack">
      ${evaluableLearners().map((learner) => {
        const focus = focusFor(learner.id);
        const skipped = state.skipped[learner.id];
        return `<article class="card rating-card ${skipped ? "is-skipped" : ""}">
          <div class="rating-head">${avatar(learner)}<div><strong>${learner.name} · ${focus.title}</strong><small>${focus.question}</small></div></div>
          <div class="rating-options" role="group" aria-label="Independencia observada de ${learner.name}">
            ${ratingScale.map((option) => `<button class="rating-option ${state.ratings[learner.id] === option.value ? "is-selected" : ""}" data-action="rating" data-id="${learner.id}" data-value="${option.value}" aria-pressed="${state.ratings[learner.id] === option.value}"><b>${option.value}</b><span>${option.label}</span></button>`).join("")}
          </div>
          <div class="rating-exception"><span class="caption">${state.ratings[learner.id] ? ratingScale[state.ratings[learner.id] - 1].detail : skipped ? "No se guardará una conclusión" : "Elige la frase más cercana"}</span><button data-action="skip-rating" data-id="${learner.id}">${skipped ? "Sí pude observar" : "No pude observar"}</button></div>
        </article>`;
      }).join("")}
      ${activeLearners().filter((learner) => state.participation[learner.id] === "observer").map((learner) => `<article class="card cyan receipt-item">${avatar(learner)}<div><strong>${learner.name} observó hoy</strong><small>No pedimos una valoración ni inferimos desempeño.</small></div></article>`).join("")}
    </div>
    <button class="button secondary block" style="margin-top:12px" data-action="voice-note">${icon("mic")} ${state.note ? "Editar observación extra" : "Observación extra por voz o texto"}</button>
    <button class="text-button" style="width:100%;margin-top:8px" data-action="evaluate-more">Evaluar más (opcional)</button>
    <p class="save-transparency">Se guardarán la actividad, el foco y la frase elegida. Podrás corregirlos después.</p>
    <div class="action-dock"><button class="button primary block" data-action="complete-close" ${complete ? "" : "disabled"}>Guardar y terminar ${icon("check")}</button></div>
  </section>`;
}

function renderSummary() {
  return `<section class="screen">
    ${flowHeader("Antes de guardar", "Puedes corregir cualquier dato", "close")}
    <p class="eyebrow">Registro contextual</p><h2>Esto es lo que aprendimos hoy.</h2>
    <p class="lead">Se guarda la actividad, el foco observado y una respuesta contextual. No se crean etiquetas sobre los niños.</p>
    <article class="card dark" style="margin-top:18px"><div class="tag-row"><span class="tag yellow">Puentes de papel</span><span class="tag dark">ACT-0001 · v0.3.0 · Draft</span></div><h3 style="font-size:24px;margin-top:15px">${activeLearners().length} participantes · ${state.time} min</h3><p style="color:#bdc8ce;font-size:12px;line-height:1.45;margin-bottom:0">Cada participante construyó y probó una estructura; el grupo comparó resultados y probó una mejora.</p></article>
    <div class="section-head"><h2>Por niño</h2><span class="caption">editable</span></div>
    <article class="card">
      ${activeLearners().map((learner) => {
        if (state.participation[learner.id] === "observer") return `<div class="receipt-item"><span class="receipt-icon">${learner.initials}</span><div><strong>${learner.name} · Observó</strong><small>Sin objetivo evaluado ni exposición inferida.</small></div></div>`;
        const focus = focusFor(learner.id);
        const rating = state.ratings[learner.id] ? ratingScale[state.ratings[learner.id] - 1] : null;
        return `<div class="receipt-item"><span class="receipt-icon">${learner.initials}</span><div><strong>${learner.name} · ${focus.title}</strong><small>${rating ? `${rating.value}/5 · ${rating.label}. ${rating.detail}.` : "El adulto indicó que no pudo observar."}<br>Exposiciones: ${focus.exposure}.</small></div></div>`;
      }).join("")}
    </article>
    ${state.note ? `<article class="card cyan" style="margin-top:12px"><p class="eyebrow">Observación extra</p><p style="margin:0;font-size:13px;line-height:1.5">“${escapeHtml(state.note)}”</p></article>` : ""}
    <article class="card mint" style="margin-top:12px"><strong>Qué hará el sistema</strong><p style="margin:6px 0 0;font-size:12px;line-height:1.5">Usará estas observaciones, junto con evidencia futura, para variar oportunidades. Una sola sesión nunca determina una conclusión fuerte.</p></article>
    <div class="action-dock"><button class="button primary block" data-action="save-session">Guardar sesión ${icon("check")}</button></div>
  </section>`;
}

function renderSaved() {
  return `<section class="screen saved-screen"><div class="saved-mark">${icon("check")}</div><p class="eyebrow">Sesión guardada</p><h1>Listo. Sigan con su tarde.</h1><p class="lead">El cierre quedó guardado localmente en este dispositivo para el dry run. No se envió a un servidor.</p><article class="card" style="text-align:left;margin-top:24px"><strong>Próxima oportunidad</strong><p style="margin:7px 0 0;font-size:12px;line-height:1.5;color:var(--muted)">La próxima recomendación variará focos y aportes sin convertir una sola observación en una conclusión fuerte.</p></article><button class="button primary block" style="margin-top:20px" data-action="finish">Volver a Hoy ${icon("home")}</button></section>`;
}

function renderPlan() {
  const totalMinutes = weeklyActivities.reduce((total, activity) => total + activity.duration, 0);
  return `<section class="screen secondary-screen">
    <p class="eyebrow">Dry run de fundadora</p><h1>Plan</h1>
    <p class="lead">Abre cualquier día o prepara una sola compra para toda la semana.</p>
    <div class="plan-switch" role="tablist" aria-label="Vista del plan">
      <button role="tab" aria-selected="${state.planView === "activities"}" class="${state.planView === "activities" ? "is-selected" : ""}" data-action="plan-view" data-value="activities">Actividades</button>
      <button role="tab" aria-selected="${state.planView === "shopping"}" class="${state.planView === "shopping" ? "is-selected" : ""}" data-action="plan-view" data-value="shopping">Compras</button>
    </div>
    ${state.planView === "activities" ? `
      <div class="section-head"><h2>Cinco días con Sofi</h2><span class="tag yellow">≈ ${totalMinutes} min</span></div>
      <div class="stack">${weeklyActivities.map((activity) => `<button class="plan-card" style="--activity-color:${activity.color}" data-action="open-plan-day" data-id="${activity.id}">
        <span class="day-chip">${activity.day}</span>
        <span class="plan-card-copy"><strong>${activity.title}</strong><small>${activity.duration} min · ${activity.primaryArea}</small><em>${activity.promise}</em></span>
        <span class="plan-card-end"><span class="plan-state">${activity.status}</span>${icon("arrow")}</span>
      </button>`).join("")}</div>
      <button class="button secondary block" style="margin-top:14px" data-action="plan-view" data-value="shopping">Ver compra consolidada ${icon("arrow")}</button>
      <p class="caption" style="margin-top:14px">El probador eléctrico permanece fuera de esta semana hasta completar la revisión técnica y seleccionar componentes exactos.</p>
    ` : renderShoppingList()}
  </section>`;
}

function formatUnit(quantity, unit) {
  if (quantity === 1) return unit;
  const plurals = { vaso: "vasos", hoja: "hojas", libro: "libros", crayón: "crayones", regla: "reglas", marcador: "marcadores", toalla: "toallas", rollo: "rollos", bandeja: "bandejas", recipiente: "recipientes", cuchara: "cucharas", taza: "tazas", esponja: "esponjas", palito: "palitos", tarjeta: "tarjetas", "bolsa pequeña": "bolsas pequeñas" };
  return plurals[unit] || unit;
}

function formatQuantity(quantity, unit) {
  return `${quantity} ${formatUnit(quantity, unit)}`;
}

function shoppingProvenance(item) {
  if (item.sources.length === 1) return `${item.sources[0].day} · ${item.sources[0].title}`;
  if (item.rule === "sum") return item.sources.map((source) => `${source.day}: ${formatQuantity(source.qty, source.unit)}`).join(" + ");
  return `${item.sources.map((source) => source.day).join(" + ")} · se reutiliza; compra la cantidad mayor`;
}

function renderShoppingList() {
  const items = aggregateShopping();
  const checked = items.filter((item) => state.shoppingChecked[item.key]).length;
  return `<div class="shopping-view">
    <article class="shopping-summary">
      <div><p class="eyebrow">Compra semanal</p><h2>${checked} de ${items.length} listos</h2><p>Los consumibles se suman. Las herramientas reutilizables cuentan una sola vez.</p></div>
      <span>${Math.round(checked / items.length * 100)}%</span>
    </article>
    ${Object.entries(shoppingSectionMeta).map(([section, meta]) => {
      const sectionItems = items.filter((item) => item.section === section);
      return `<section class="store-section">
        <header><span>${meta.code}</span><div><h2>${section}</h2><p>${meta.note}</p></div><b>${sectionItems.length}</b></header>
        <div class="shopping-items">${sectionItems.map((item) => `<label class="shopping-item ${state.shoppingChecked[item.key] ? "is-checked" : ""}">
          <input type="checkbox" data-action="shopping-item" data-id="${item.key}" ${state.shoppingChecked[item.key] ? "checked" : ""}>
          <span class="shopping-check"></span>
          <span class="shopping-copy"><strong>${formatQuantity(item.qty, item.unit)} · ${item.name}</strong><small>${item.detail}</small><em>${shoppingProvenance(item)}</em></span>
          <span class="aggregation-rule">${item.rule === "sum" ? "SUMA" : "REUSA"}</span>
        </label>`).join("")}</div>
      </section>`;
    }).join("")}
    <article class="card coral shopping-hold"><strong>Probador eléctrico: no comprar todavía</strong><p>La configuración y los números de parte siguen pendientes del gate técnico.</p></article>
  </div>`;
}

function renderPlannedActivity() {
  const activity = weeklyActivities.find((item) => item.id === state.selectedPlanDay) || weeklyActivities[0];
  return `<section class="screen">
    ${flowHeader(activity.title, `${activity.day} · ${activity.duration} min`, "plan")}
    <article class="planned-hero" style="--activity-color:${activity.color}">
      <div class="tag-row"><span class="tag yellow">${activity.activityRef}</span><span class="tag coral">${activity.status}</span></div>
      <p class="eyebrow">Promesa de la actividad</p><h1>${activity.promise}</h1>
    </article>
    <article class="detail-purpose">
      <p class="eyebrow">Propósito educativo</p><h2>${activity.primaryArea}</h2><p>${activity.purpose}</p>
      <div class="tag-row">${activity.secondaryAreas.map((area) => `<span class="tag">${area}</span>`).join("")}</div>
      <div class="concept-row">${activity.concepts.map((concept) => `<span>${concept}</span>`).join("")}</div>
    </article>
    <article class="focus-card" data-color="cyan">
      <div class="focus-head">${avatar(learners[0])}<div><span class="caption">Foco sugerido para Sofi</span><h3>${activity.focus}</h3></div></div>
      <p class="focus-objective">${activity.focusDetail}</p>
    </article>
    <div class="section-head"><h2>Materiales</h2><span class="caption">para este día</span></div>
    <article class="card"><ul class="plain-list material-detail-list">${activity.materials.map((material) => `<li>${material}</li>`).join("")}</ul></article>
    <div class="section-head"><h2>Cómo ocurre</h2><span class="caption">historia completa</span></div>
    <article class="card"><ol class="planned-flow">${activity.flow.map((step, index) => `<li><span>${index + 1}</span><p>${step}</p></li>`).join("")}</ol></article>
    <article class="card cyan close-question"><p class="eyebrow">Una pregunta al cerrar</p><strong>${activity.closeQuestion}</strong></article>
    <article class="safety-card" style="margin-top:12px"><b>${icon("alert")}</b><div><strong>Seguridad y detención</strong><p>${activity.safety}</p></div></article>
    <p class="caption" style="margin:12px 3px 0">Esta actividad forma parte de un founder pilot controlado. ${activity.status === "Draft" ? "Aún no es contenido publicado." : "Debe convertirse en ActivityVersion y superar revisión antes de publicarse."}</p>
    <div class="activity-detail-actions">
      <button class="button secondary" data-action="view-shopping">Compras</button>
      ${activity.id === "day1" ? `<button class="button primary" data-action="prepare-planned">Preparar actividad ${icon("arrow")}</button>` : `<button class="button primary" data-action="navigate" data-target="plan">Volver al plan</button>`}
    </div>
  </section>`;
}

function renderJourney() {
  return `<section class="screen secondary-screen"><p class="eyebrow">Observaciones, no etiquetas</p><h1>Journey</h1><p class="lead">Una vista del recorrido y de las oportunidades vividas, siempre con contexto.</p><div class="section-head"><h2>Últimas experiencias</h2><span class="caption">familia completa</span></div><article class="card"><div class="receipt-item"><span class="receipt-icon">SO</span><div><strong>Sofi · Construcción</strong><small>Tuvo oportunidades de plegar, comparar y explicar. Evidencia todavía limitada.</small></div></div><div class="receipt-item"><span class="receipt-icon">MA</span><div><strong>Mateo · Medición</strong><small>Dos observaciones recientes muestran mayor independencia; no es un diagnóstico.</small></div></div><div class="receipt-item"><span class="receipt-icon">LE</span><div><strong>Leo · Comunicación</strong><small>Una exposición registrada. Hace falta observar en otros contextos.</small></div></div></article><article class="card yellow" style="margin-top:12px"><strong>Diseño pendiente de validar</strong><p style="font-size:12px;line-height:1.5;margin-bottom:0">Esta pantalla prueba cómo comunicar incertidumbre a familias sin convertirla en un tablero de notas.</p></article></section>`;
}

function renderFamily() {
  const installed = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
  return `<section class="screen secondary-screen"><p class="eyebrow">Cuenta del adulto</p><h1>Familia</h1><p class="lead">Perfiles mínimos para adaptar oportunidades y compartir acceso entre cuidadores.</p>
    <article class="card mint install-card">
      <div><p class="eyebrow">Este dispositivo</p><strong>${installed ? "La abriste como aplicación" : "Puedes instalar este piloto"}</strong><p>${installed ? "El plan y tu avance operativo quedan disponibles desde este icono." : "Añádelo a la pantalla de inicio para abrirlo sin buscar el enlace."}</p></div>
      <button class="button secondary" data-action="install-app">${installed ? "Ver instrucciones" : "Instalar"}</button>
    </article>
    <div class="section-head"><h2>Niños</h2><span class="caption">datos sintéticos</span></div><div class="stack">${learners.map((learner) => `<article class="card actor-card">${avatar(learner)}<div><strong>${learner.name}</strong><small>${learner.age} · sin fecha de nacimiento completa</small></div><button class="inline-button" data-action="not-built">•••</button></article>`).join("")}</div><div class="section-head"><h2>Adultos con acceso</h2></div><article class="card"><div class="receipt-item"><span class="receipt-icon">AM</span><div><strong>Adulto principal</strong><small>Gestiona suscripción, privacidad y permisos.</small></div></div><div class="receipt-item"><span class="receipt-icon">AP</span><div><strong>Adulto invitado</strong><small>Puede planear y realizar actividades.</small></div></div></article>
    <button class="text-button reset-local" data-action="reset-prototype">Reiniciar el avance guardado en este dispositivo</button>
  </section>`;
}

function installHelpSheet() {
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const steps = isIOS
    ? ["Abre este enlace en Safari.", "Toca Compartir.", "Elige “Añadir a pantalla de inicio” y luego “Agregar”."]
    : ["Abre este enlace en Chrome.", "Toca el menú de tres puntos.", "Elige “Agregar a pantalla principal” o “Instalar aplicación”."];
  openSheet(`<header><div><p class="eyebrow">Instalar en el celular</p><h2 id="sheetTitle">Déjalo como un icono</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>
    <ol class="setup-list install-steps">${steps.map((step, index) => `<li><span>${index + 1}</span><p>${step}</p></li>`).join("")}</ol>
    <article class="card cyan"><strong>Tu avance es local</strong><p>Las compras y el punto de la actividad se conservan en este dispositivo. Este prototipo no crea cuentas ni sincroniza con otro teléfono.</p></article>`);
}

async function requestInstall() {
  if (!deferredInstallPrompt) return installHelpSheet();
  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  render();
}

function learningDetailsSheet() {
  openSheet(`<header><div><p class="eyebrow">Entender la actividad</p><h2 id="sheetTitle">Qué aprendizaje sostiene el puente</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>
    <article class="card dark"><span class="tag yellow">Éxito educativo</span><p style="font-size:13px;line-height:1.55;margin-bottom:0">Cada niño imagina, construye y prueba su propia forma; registra lo ocurrido y recomienda una mejora usando una observación. No importa cuántos crayones sostenga.</p></article>
    <div class="sheet-section"><p class="eyebrow">Conceptos</p><div class="tag-row"><span class="tag">Estructura</span><span class="tag">Carga</span><span class="tag">Rigidez a la flexión</span><span class="tag">Distribución de carga</span><span class="tag">Prueba justa</span></div></div>
    <div class="sheet-section"><p class="eyebrow">Habilidades practicables</p><ul class="plain-list"><li>Predecir y hacer una pregunta comprobable.</li><li>Seguir una secuencia de plegado.</li><li>Añadir y contar una carga a la vez.</li><li>Mantener condiciones constantes.</li><li>Comparar resultados usando más, menos o igual.</li><li>Elegir una mejora y explicar con evidencia.</li></ul></div>
    <article class="card cyan"><strong>Importante</strong><p style="font-size:12px;line-height:1.5;margin-bottom:0">Una oportunidad de practicar no demuestra capacidad. Solo el foco principal recibe la pregunta final; las demás habilidades se registran como exposición cuando el niño realmente participa.</p></article>
    <button class="button primary block" style="margin-top:16px" data-action="close-sheet">Entendido</button>`);
}

function helpSheet() {
  const stage = stages[state.stage];
  openSheet(`<header><div><p class="eyebrow">${stage.name}</p><h2 id="sheetTitle">¿Qué está pasando?</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>
    ${stage.helpOptions.map((option, index) => `<button class="support-option ${state.supportUsed[state.stage] === index ? "is-current" : ""}" data-action="use-support" data-value="${index}"><span class="support-problem">${option.problem}</span><span class="support-change">${option.change}</span><span class="support-meta"><b>Impacto</b> ${option.impact}</span><span class="support-meta"><b>Reanuda</b> ${option.resume}</span><span class="support-limit">${icon("alert")} ${option.limit}</span></button>`).join("")}
    <p class="caption">Estas respuestas pertenecen a la versión revisada de la actividad. La IA puede explicarlas, pero no cambiar materiales, carga, distancia ni controles.</p>`);
}

function pauseSheet() {
  openSheet(`<header><div><p class="eyebrow">Actividad en pausa</p><h2 id="sheetTitle">Tómense el tiempo que necesiten.</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header><button class="button primary block" data-action="resume">${icon("play")} Continuar</button><button class="button secondary block" style="margin-top:9px" data-action="finish-early">Terminar y cerrar ahora</button><button class="button danger block" style="margin-top:9px" data-action="abandon">Salir sin guardar</button>`);
}

function noteSheet() {
  openSheet(`<header><div><p class="eyebrow">Opcional</p><h2 id="sheetTitle">Observación extra</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header><p class="caption">En el producto real, el adulto podrá dictar, revisar la transcripción y corregirla antes de guardar. Ejemplo: “Cambiaron el diseño cuando vieron que el vaso se inclinaba”.</p><textarea id="noteInput" aria-label="Observación extra">${escapeHtml(state.note)}</textarea><button class="button primary block" style="margin-top:12px" data-action="save-note">Guardar observación</button>`);
  requestAnimationFrame(() => document.querySelector("#noteInput")?.focus());
}

function openSheet(content) {
  lastFocus = document.activeElement;
  sheetContent.innerHTML = content;
  scrim.hidden = false;
  sheet.classList.add("is-open");
  sheet.setAttribute("aria-hidden", "false");
  requestAnimationFrame(() => sheet.querySelector("button, textarea")?.focus());
}

function closeSheet() {
  if (!sheet.classList.contains("is-open")) return;
  sheet.classList.remove("is-open");
  sheet.setAttribute("aria-hidden", "true");
  scrim.hidden = true;
  setTimeout(() => { sheetContent.innerHTML = ""; lastFocus?.focus?.(); }, 230);
}

function showToast(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.add("is-visible");
  toastTimer = setTimeout(() => toast.classList.remove("is-visible"), 2600);
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"]/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[character]);
}

document.addEventListener("click", (event) => {
  const control = event.target.closest("[data-action]");
  if (!control || control.disabled) return;
  const { action, target, id, value } = control.dataset;

  if (action === "tab" || action === "navigate") return setScreen(target);
  if (action === "home") return setScreen("today");
  if (action === "select-time") { state.time = Number(value); return render(); }
  if (action === "plan-view") { state.planView = value; return render(); }
  if (action === "open-plan-day") { state.selectedPlanDay = id; return setScreen("planned-activity"); }
  if (action === "view-shopping") { state.planView = "shopping"; return setScreen("plan"); }
  if (action === "prepare-planned") return setScreen("focus");
  if (action === "toggle-participant") {
    state.selected = state.selected.includes(id) ? state.selected.filter((item) => item !== id) : [...state.selected, id];
    return render();
  }
  if (action === "learning-details") return learningDetailsSheet();
  if (action === "start-session") return setScreen("session");
  if (action === "stage") { state.stage = Number(value); state.highestStage = Math.max(state.highestStage, state.stage); return render(); }
  if (action === "previous-stage") { state.stage = Math.max(0, state.stage - 1); return render(); }
  if (action === "next-stage") {
    if (state.stage === stages.length - 1) return setScreen("close");
    state.stage += 1; state.highestStage = Math.max(state.highestStage, state.stage); return render();
  }
  if (action === "help") return helpSheet();
  if (action === "use-support") { state.supportUsed[state.stage] = Number(value); const selectedSupport = stages[state.stage].helpOptions[Number(value)]; closeSheet(); render(); showToast(`Apoyo seleccionado. ${selectedSupport.resume}`); return; }
  if (action === "pause") { state.paused = true; return pauseSheet(); }
  if (action === "resume") { state.paused = false; closeSheet(); return render(); }
  if (action === "finish-early") { state.paused = false; closeSheet(); return setScreen("close"); }
  if (action === "abandon") { state.paused = false; closeSheet(); return setScreen("today"); }
  if (action === "rating") { state.ratings[id] = Number(value); state.skipped[id] = false; return render(); }
  if (action === "skip-rating") { state.skipped[id] = !state.skipped[id]; delete state.ratings[id]; return render(); }
  if (action === "voice-note") return noteSheet();
  if (action === "save-note") { state.note = document.querySelector("#noteInput")?.value.trim() || ""; closeSheet(); render(); return; }
  if (action === "evaluate-more") return showToast("Flujo opcional documentado; no se abre por defecto.");
  if (action === "complete-close") { state.savedElapsed = Date.now() - state.closeStartedAt; return setScreen("saved"); }
  if (action === "save-session") return setScreen("saved");
  if (action === "finish") return setScreen("today");
  if (action === "connection-info") return openSheet(`<header><div><p class="eyebrow">Estado de conexión</p><h2 id="sheetTitle">${state.offline ? "Sin conexión" : "En línea"}</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header><article class="card ${state.offline ? "yellow" : "mint"}"><strong>${state.offline ? "Puedes continuar" : "El contenido está listo"}</strong><p>${state.offline ? "La aplicación, el plan y el avance local siguen disponibles. No hay sincronización con un servidor en este prototipo." : "El dispositivo conservará localmente tus compras y el punto de la actividad."}</p></article>`);
  if (action === "install-app") return requestInstall();
  if (action === "reset-prototype") {
    if (!window.confirm("¿Reiniciar compras, preparación y avance de la actividad en este dispositivo?")) return;
    try { localStorage.removeItem(storageKey); } catch (error) { console.warn("No se pudo reiniciar el estado local.", error); }
    window.location.assign(`${window.location.pathname}?reset=1`);
    return;
  }
  if (action === "close-info") return openSheet(`<header><div><p class="eyebrow">Escala de independencia</p><h2 id="sheetTitle">Describe esta ocasión, no al niño.</h2></div><button class="sheet-close" data-action="close-sheet" aria-label="Cerrar">${icon("close")}</button></header>${ratingScale.map((item) => `<div class="receipt-item"><span class="receipt-icon">${item.value}</span><div><strong>${item.label}</strong><small>${item.detail}</small></div></div>`).join("")}`);
  if (action === "not-built") return showToast("Este control está fuera del recorrido que estamos validando.");
  if (action === "close-sheet") return closeSheet();
});

document.addEventListener("change", (event) => {
  const materialControl = event.target.closest('[data-action="material"]');
  if (materialControl) {
    state.materials[materialControl.dataset.id] = materialControl.checked;
    return render();
  }
  const shoppingControl = event.target.closest('[data-action="shopping-item"]');
  if (shoppingControl) {
    state.shoppingChecked[shoppingControl.dataset.id] = shoppingControl.checked;
    return render();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeSheet();
});

window.addEventListener("online", () => { state.offline = false; render(); showToast("Conexión restaurada."); });
window.addEventListener("offline", () => { state.offline = true; render(); showToast("Sin conexión: el contenido sigue disponible."); });
window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  if (state.screen === "family") render();
});
window.addEventListener("appinstalled", () => {
  deferredInstallPrompt = null;
  showToast("Aplicación añadida a este celular.");
  if (state.screen === "family") render();
});
window.addEventListener("load", () => {
  if ("serviceWorker" in navigator && ["http:", "https:"].includes(window.location.protocol)) {
    navigator.serviceWorker.register("./sw.js").catch((error) => console.warn("No se pudo activar el modo instalable.", error));
  }
});

render();
