# QA del prototipo móvil

**Fecha:** 2026-08-16  
**Resultado:** Pass

## Viewports inspeccionados

| Vista | Viewport | Ancho de documento | Resultado |
|---|---:|---:|---|
| Hoy | 360×800 | 360 | Sin overflow horizontal |
| Roles | 430×932 | 430 | Tarjetas y acción sticky legibles |
| Sesión | 360×800 | 360 | Track horizontal intencional; contenido principal contenido |
| Cierre | 430×932 | 430 | Cinco anclas verbales visibles por niño |
| Sistema visual | 1280×900 | 1280 | Navegación, hero y primera sección sin overflow |

Capturas:

- `today-360.png`
- `roles-430.png`
- `session-360.png`
- `close-430.png`
- `design-system-1280.png`

## Smoke test interactivo

`flow-smoke.mjs` valida:

1. selección inicial de tres participantes;
2. apertura del plan de roles;
3. cambio a observador sin objetivo evaluado;
4. restauración de un rol activo;
5. bloqueo de preparación incompleta;
6. inicio después de confirmar materiales;
7. sesión desde Descubrir;
8. ayuda contextual;
9. cierre con tres ratings;
10. recibo con incertidumbre explícita;
11. estado final guardado;
12. ausencia de excepciones de JavaScript.

## Resultado visual

- Acción primaria y advertencias permanecen visibles bajo atención dividida.
- Roles y objetivo principal se leen como asignaciones de la sesión, no como perfiles.
- En sesión no aparecen destinos de navegación; volver, pausar y ayuda permanecen disponibles.
- La escala 1–5 conserva una frase visible en cada opción.
- `Draft` es textual en la recomendación y el recibo.

## Pendiente de prueba humana

- Carga mental real con 1–3 niños presentes.
- Respuesta infantil a roles propuestos y cambios en vivo.
- Cierre paralelo actual frente a una alternativa secuencial.
- Comprensión espontánea de “exposición” y de la incertidumbre del Journey.
