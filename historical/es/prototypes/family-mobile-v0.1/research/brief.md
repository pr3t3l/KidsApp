> **Histórico — documentación en español.** Archivado el 18 de agosto de 2026. Se conserva para trazabilidad; toda documentación y cambios nuevos deben crearse en inglés.

# Prototipo móvil familiar v0.6 — brief

## Resultado que debe probar

Comprobar si un adulto con atención dividida puede entender el valor educativo, preparar una actividad compartida, acompañar un ciclo completo propio para hasta tres niños y cerrar una observación por niño sin sentir que administra un salón de clase.

## Superficie

- **Modo:** `mobile-app`.
- **Operador:** adulto autenticado; los niños participan fuera de pantalla.
- **Clases objetivo:** teléfono compacto `360 × 800` y teléfono grande `430 × 932`.
- **Entrada:** táctil; teclado como requisito de accesibilidad del simulador.
- **Capacidades representadas:** interrupción/reanudación, estado offline, voz opcional simulada y safe areas.
- **Composición excluida:** panel editorial, tablas densas y navegación lateral de escritorio.

## Recorrido mínimo completo

1. Elegir 30, 45 o 60 minutos y los niños de hoy.
2. Entender la promesa, propósito, áreas, conceptos, mecanismo y decisión infantil sin abrir una explicación redundante.
3. Revisar el foco principal y el aporte sugerido para cada niño, con una razón explicable.
4. Preparar ACT-0001 Puente de papel `0.3.0` como fixture editorial Draft, comprendiendo para qué sirve cada material.
5. Recorrer Discover–Imagine–Build–Experiment–Improve–Explain con una referencia visual específica, contexto breve, acción adulta prioritaria, guion, acciones nominales y resultado compacto; cada niño diseña y prueba su propio puente.
6. Pedir ayuda ante un problema concreto y aplicar un apoyo publicado sin cambiar seguridad ni mecanismo.
7. Pausar, perder conexión y reanudar sin perder guía ni seguridad.
8. Responder una valoración verbal por niño, leer qué se conservará y guardar directamente sin cronómetro visible ni pantalla redundante.
9. Abrir cualquiera de las cinco actividades del plan y volver sin perder la semana.
10. Preparar una compra semanal por sección, comprobando cantidades agregadas y procedencia por día.

## Experiencia central

> El teléfono traduce una actividad editorial rica en una guía breve y accionable: explica por qué importa, qué dice el adulto y cómo participa cada niño; después se aparta para que la familia aprenda haciendo.

## Riesgos que el diseño debe revelar

- Un foco o aporte puede sentirse como una etiqueta si no se explica como sugerencia contextual.
- La escala 1–5 puede sentirse como nota si el número aparece sin palabras ni acción concreta.
- Demasiada información simultánea puede competir con la actividad física; demasiada compresión puede volver la guía ambigua.
- Una instrucción grupal sin acciones nombradas puede dejar a uno o más niños sin una contribución clara.
- Un foco de aprendizaje puede convertirse erróneamente en un monopolio de acciones y privar a otros niños del ciclo esencial.
- Una pantalla puede parecer clara aislada y aun así no explicar qué cambió ni por qué sigue la próxima fase.
- Dividir decisión, observación, continuidad y éxito en demasiadas tarjetas puede aumentar lectura sin mejorar la acción.
- Una actividad Draft puede parecer aprobada si el estado no se repite.
- El cierre paralelo de tres niños puede producir errores de atribución.

## Dirección visual heredada

Se conserva **Pocket Workshop** como dirección de experiencia no comercial: graphite, work paper, safety yellow, blueprint cyan, coral y mint; Bahnschrift/Aptos; diagramas de taller y una acción dominante. La fuente está en `C:/Users/prett/Documents/ChatGPT/Otros/kids-system-studio/`.

## Cambios frente al artefacto fuente

- De `web-workspace` a una aplicación móvil dedicada.
- Panel editorial fuera del shell familiar.
- ACT-0001 actualizado a `0.3.0` desde un contrato narrativo causal.
- Roles editoriales internos traducidos a `foco de aprendizaje` y `aporte sugerido`; el flujo familiar no ofrece cambio de rol como acción principal.
- Los focos cambian qué observa el adulto, no quién puede imaginar, construir o probar.
- Cada fase muestra `Llegan con` y `Al terminar tendrán`; la salida de una fase coincide con la entrada de la siguiente.
- El vaso y los crayones se introducen con una función explícita antes de la primera prueba de referencia.
- Cada niño elige, construye y prueba su forma; la mejora posterior es grupal.
- Escala con palabras visibles: todavía no, mucha ayuda, alguna ayuda, casi solo, solo y seguro.
- Mapa educativo progresivo: propósito, áreas, conceptos, mecanismo, decisión infantil y focos individuales.
- Guía por fase con acciones adultas, frase exacta, tarea de cada niño, observación, criterio para avanzar, seguridad y ayuda contextual.
- Guía práctica para que el adulto sugiera estructuras sin entregar la solución.
- Promesa editorial de ACT-0001 como mensaje principal; el ciclo individual permanece como explicación operativa.
- Función y control de cada material integrados en la lista; se elimina la sección duplicada de funciones.
- Una sola señal de navegación por fases, visual específico de la fase y `Haz esto` antes de detalle secundario.
- Decisión infantil integrada en las acciones y observación/criterio de continuación agrupados.
- Cierre directo `Guardar y terminar`, sin cronómetro ni recibo obligatorio.
- Cinco tarjetas de plan navegables hacia un detalle suficiente para decidir y prepararse.
- Compra consolidada por supermercado, papelería y casa; `SUMA` para consumibles y `REUSA` para herramientas.

## No objetivos

- No implementa backend, autenticación, IA, audio, pagos ni persistencia.
- No aprueba ACT-0001 para uso familiar.
- No valida seguridad física ni eficacia pedagógica.
- No decide nombre comercial, stack nativo o Apple Kids Category.

## Siguiente prueba humana

Moderación con adultos usando datos sintéticos: completar el recorrido para uno y tres niños; pedir que narren qué existe sobre la mesa antes y después de cada fase; medir comprensión del propósito, claridad sobre qué decir y qué hace cada niño, recordación de seguridad, uso de ayuda contextual, tiempo de cierre y carga mental.
