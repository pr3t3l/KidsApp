# QA del prototipo móvil

**Fecha:** 2026-08-18
**Resultado:** Pass v0.6

## Viewports inspeccionados

| Vista | Viewport | Ancho de documento | Resultado |
|---|---:|---:|---|
| Hoy | 360×800 | 360 | Sin overflow horizontal |
| Plan | 430×932 | 430 | Cinco actividades táctiles y estados editoriales visibles |
| Detalle planificado | 430×932 | 430 | Propósito, foco, materiales, recorrido y seguridad |
| Compras | 430×932 | 430 | Secciones, totales, procedencia y reglas SUMA/REUSA |
| Mapa educativo | 430×932 | 430 | Propósito, áreas, mecanismo y decisión legibles |
| Preparación | 430×932 | 430 | Función integrada en materiales, progreso y bloqueo visibles |
| Imaginar | 430×932 | 430 | Parte de la referencia observada; cada niño elige una forma propia |
| Construir | 430×932 | 430 | Contexto, visual específico y una estructura propia por niño visibles |
| Experimentar | 430×932 | 430 | Un turno completo por niño, protocolo comparable y guion nombrado visibles |
| Sesión compacta | 360×800 | 360 | Sin overflow horizontal; riel de fases contenido |
| Cierre | 430×932 | 430 | Cinco anclas verbales, sin cronómetro y con guardado directo |
| Sistema visual | 1280×900 | 1280 | Navegación, hero y primera sección sin overflow |

Capturas:

- `today-360.png`
- `plan-430.png`
- `planned-activity-430.png`
- `planned-activity-flow-430.png`
- `shopping-430.png`
- `shopping-paper-430.png`
- `shopping-360.png`
- `focus-430.png`
- `focus-children-430.png`
- `prep-430.png`
- `prep-guide-430.png`
- `imagine-430.png`
- `imagine-children-430.png`
- `build-430.png`
- `build-actions-430.png`
- `experiment-430.png`
- `experiment-actions-430.png`
- `session-360.png`
- `close-430.png`
- `design-system-1280.png`

## Smoke test interactivo

`flow-smoke.mjs` valida:

1. selección inicial de tres participantes;
2. apertura de los cinco días del plan y retorno sin perder la semana;
3. consolidación de compras por sección, suma `1 + 12 = 13` y reutilización con procedencia;
4. apertura del mapa educativo y presencia de tres focos explicados;
5. asignación inicial de conteo a Sofi y diseño a Mateo, sin convertir edad en conclusión;
6. ausencia de controles normales de cambio de rol y del copy innecesario de configuración;
7. ausencia de un detalle educativo redundante;
8. función integrada en materiales y bloqueo de preparación incompleta;
9. Discover con prueba plana real, visual específico y transición visible;
10. Build con una estructura propia por niño;
11. Experiment con turno completo y prueba propia por niño;
12. ayuda contextual con impacto y punto de reanudación;
13. confirmación visible del apoyo aplicado;
14. cierre con tres ratings y sin temporizador visible;
15. guardado directo sin recibo obligatorio;
16. persistencia local del checklist y el punto de cierre después de recargar;
17. estado final guardado y ausencia de excepciones de JavaScript.

## PWA y uso desde celular

Con el prototipo servido por HTTP(S) y Chrome iniciado con depuración remota:

```powershell
node qa/pwa-smoke.mjs http://127.0.0.1:4173/index.html
```

La prueba verifica manifest e iconos, control del service worker, cache del shell y recarga completa sin red. La protección/autenticación del hosting no forma parte del prototipo estático y debe configurarse antes de invitar familias externas.

## Resultado visual

- Acción primaria y advertencias permanecen visibles bajo atención dividida.
- `Haz esto` aparece en el primer viewport a 360×800 y el resumen de fase no usa el plano genérico del puente.
- Cada tarjeta semanal comunica que se puede abrir; la compra explica el cálculo sin ocultar los días de origen.
- Focos y aportes se leen como sugerencias de la sesión, no como perfiles ni identidades.
- La sesión separa visualmente lo que hace/dice el adulto y la acción de cada niño.
- El contexto inicial y el bloque compacto de resultado conservan la continuidad causal con menos tarjetas.
- El foco modifica el lenguaje y lo que se observa; no impide que Sofi, Mateo o Leo diseñen, construyan y prueben.
- En sesión no aparecen destinos de navegación; volver, pausar y ayuda permanecen disponibles.
- La escala 1–5 conserva una frase visible en cada opción.
- El cierre no muestra tiempo, no exige recibo y comunica `Guardar y terminar` como acción dominante.
- `Draft` es textual en la recomendación y preparación.

## Pendiente de prueba humana

- Carga mental real con 1–3 niños presentes.
- Respuesta infantil a los aportes sugeridos, especialmente si un niño decide hacer otra contribución.
- Cantidad de lectura que el adulto tolera en cada fase mientras facilita físicamente.
- Cierre paralelo actual frente a una alternativa secuencial.
- Comprensión espontánea de “exposición” y de la incertidumbre del Journey.
