# SPEC-05 — Activity Content Model

**Estado:** Review  
**Versión:** 0.1  
**Propietario:** Contenido/Pedagogía/Seguridad

## 1. Propósito

Definir la unidad versionada que alimenta la biblioteca, el recomendador, la interfaz, las imágenes y las evaluaciones.

## 2. Identidad y ciclo editorial

| Campo | Requerido | Descripción |
|---|---:|---|
| `activity_id` | Sí | Identificador estable, por ejemplo `ACT-0001`. |
| `version` | Sí | Versión semántica del contenido. |
| `status` | Sí | Draft, review, pilot, published, retired. |
| `title` | Sí | Título breve para la familia. |
| `slug` | Sí | Referencia técnica legible. |
| `summary` | Sí | Promesa de una oración. |
| `authors` | Sí | Responsables editoriales. |
| `review_records` | Sí para publicar | Revisiones pedagógica y de seguridad. |
| `change_log` | Sí | Cambios entre versiones. |

## 2.1 Localización

Los identificadores, relaciones y reglas son neutrales al idioma. Cada ActivityVersion publica bundles `en-US` y `es-US` con:

- Título, resumen e instrucciones.
- Explicación adulta breve y detallada.
- Lenguaje sugerido para el niño.
- Materiales y nombres regionales alternativos.
- Advertencias y troubleshooting.
- Preguntas de apertura/cierre.
- Alt text y capas de texto visual.

Cantidades y unidades se representan de forma estructurada para renderizar sistema métrico y estadounidense cuando corresponda. Una traducción no puede cambiar el significado científico ni de seguridad.

## 3. Adecuación

- Rango de edad orientativo.
- Niveles funcionales soportados.
- Número mínimo y máximo de niños.
- Duración total y por etapa.
- Preparación del adulto.
- Nivel de desorden.
- Espacio necesario.
- Accesibilidad y adaptaciones conocidas.
- Prerrequisitos recomendados, no asumidos.

## 4. Propósito educativo

- Área principal y áreas secundarias.
- Conceptos explicados.
- Habilidades practicables.
- Ciclo Discover–Imagine–Build–Experiment–Improve–Explain.
- Pregunta de apertura.
- Predicción esperada, sin exigir respuesta correcta.
- Señales observables por habilidad.
- Explicación para el adulto.
- Explicación con lenguaje infantil.
- Preguntas de reflexión.

## 5. Materiales

Cada material incluye:

- Identidad normalizada.
- Nombre visible y alternativas.
- Cantidad/unidad.
- Consumible o reutilizable.
- Obligatorio u opcional.
- Puede sustituirse y por qué.
- Restricciones de seguridad.
- Preparación del adulto.

El recomendador no puede proponer una sustitución no aprobada que cambie el riesgo o el mecanismo esencial.

## 6. Pasos

Cada paso contiene:

- Número y título.
- Actor: adulto, niño, grupo o rol.
- Instrucción breve.
- Resultado visual esperado.
- Tiempo aproximado.
- Imagen o diagrama requerido.
- Señal de éxito.
- Problemas comunes y soluciones.
- Advertencia localizada.
- Posibilidad de reanudar.

## 7. Roles

La actividad define `role_templates`. Cada rol incluye:

- Nombre y contribución real.
- Responsabilidades.
- Habilidades posibles como objetivo principal.
- Niveles compatibles.
- Pasos permitidos y restringidos.
- Dependencias con otros roles.
- Variantes para trabajo individual.

Ejemplo para un puente:

| Rol | Responsabilidad | Objetivos posibles |
|---|---|---|
| Materials Explorer | contar y clasificar piezas | conteo, clasificación, patrones |
| Builder | unir y montar estructura | motricidad, secuenciación, ensamblaje |
| Test Engineer | medir y probar carga | medición, comparación, registro |
| Design Engineer | dibujar e iterar | planificación, estabilidad, explicación |

## 8. Variaciones y extensiones

Se distinguen:

- **Presentación:** historia, vocabulario, soporte visual.
- **Dificultad:** número de pasos, precisión, independencia.
- **Rol:** responsabilidad del participante.
- **Material:** sustitución aprobada.
- **Extensión:** reto adicional publicado.

Cada adaptación declara condiciones y límites. La IA selecciona entre opciones aprobadas; una propuesta nueva permanece como borrador editorial.

## 9. Seguridad

- Nivel de supervisión.
- Riesgos por material, herramienta y paso.
- Pasos solo para adultos.
- Preparación y limpieza.
- Señales para detenerse.
- Restricciones por edad o capacidad.
- Equipo de protección cuando aplique.
- Prohibiciones de adaptación.
- Instrucciones ante falla segura; no instrucciones médicas.

## 10. Recursos visuales

Paquete recomendado:

1. Materiales identificados.
2. Preparación del adulto.
3. Secuencia visual de construcción.
4. Resultado esperado.
5. Explicación visual del concepto.

Cada recurso incluye alt text, versión, fuente, derechos y nodos/pasos asociados.

## 11. Observación

Para cada objetivo elegible:

- Pregunta final específica.
- Anclas de independencia aplicables.
- Qué cuenta como evidencia.
- Qué no cuenta como evidencia.
- Factores externos frecuentes.

## 12. Criterios de publicación

- Todos los materiales y cantidades fueron verificados.
- Un adulto distinto al autor ejecutó las instrucciones.
- Se documentaron resultado esperado y fallas frecuentes.
- Las reglas de seguridad están revisadas.
- Los objetivos tienen señales observables.
- Los roles producen un proyecto coherente.
- Las imágenes coinciden con la versión.
- Se registró tiempo real de al menos una prueba.

## 13. Requisitos

- **ACT-001:** Cada actividad y versión tiene identidad inmutable.
- **ACT-002:** Solo una versión publicada puede recomendarse a una familia.
- **ACT-003:** Toda habilidad evaluable incluye rúbrica observable.
- **ACT-004:** Cada rol declara pasos permitidos y objetivos posibles.
- **ACT-005:** Las sustituciones y extensiones deben estar previamente aprobadas para entrega automática.
- **ACT-006:** Cambios de seguridad requieren nueva versión y revisión.
- **ACT-007:** Una sesión conserva referencia a la versión exacta utilizada.
- **ACT-008:** Una actividad debe funcionar individualmente o declarar que requiere grupo.
- **ACT-009:** Cada actividad publicada tiene instrucciones de solución de problemas.
- **ACT-010:** Las imágenes deben estar versionadas con el contenido.
- **ACT-011:** Una versión lanzada en Estados Unidos requiere bundles completos y revisados en inglés y español.
- **ACT-012:** Advertencias y adult-only steps reciben revisión bilingüe específica.
