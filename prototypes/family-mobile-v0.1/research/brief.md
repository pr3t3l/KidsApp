# Prototipo móvil familiar v0.1 — brief

## Resultado que debe probar

Comprobar si un adulto con atención dividida puede preparar una actividad compartida, negociar contribuciones con hasta tres niños, seguir una guía física y cerrar una observación por niño sin sentir que administra un salón de clase.

## Superficie

- **Modo:** `mobile-app`.
- **Operador:** adulto autenticado; los niños participan fuera de pantalla.
- **Clases objetivo:** teléfono compacto `360 × 800` y teléfono grande `430 × 932`.
- **Entrada:** táctil; teclado como requisito de accesibilidad del simulador.
- **Capacidades representadas:** interrupción/reanudación, estado offline, voz opcional simulada y safe areas.
- **Composición excluida:** panel editorial, tablas densas y navegación lateral de escritorio.

## Recorrido mínimo completo

1. Elegir 30, 45 o 60 minutos y los niños de hoy.
2. Revisar roles propuestos y objetivos principales.
3. Intercambiar, combinar o rechazar un rol sin penalización.
4. Preparar ACT-0001 Puente de papel `0.2.2` como fixture editorial Draft.
5. Recorrer Discover–Imagine–Build–Experiment–Improve–Explain.
6. Pausar, perder conexión y reanudar sin perder guía ni seguridad.
7. Confirmar participación real y responder una valoración verbal por niño.
8. Revisar qué se guardaría y qué no puede inferirse.

## Experiencia central

> El teléfono prepara el taller, nombra quién contribuye ahora y después se aparta para que la familia aprenda haciendo.

## Riesgos que el diseño debe revelar

- Un rol demasiado rígido puede crear conflicto o jerarquía entre hermanos.
- La escala 1–5 puede sentirse como nota si el número aparece sin palabras ni acción concreta.
- Una guía extensa puede competir con la actividad física.
- Una actividad Draft puede parecer aprobada si el estado no se repite.
- El cierre paralelo de tres niños puede producir errores de atribución.

## Dirección visual heredada

Se conserva **Pocket Workshop** como dirección de experiencia no comercial: graphite, work paper, safety yellow, blueprint cyan, coral y mint; Bahnschrift/Aptos; diagramas de taller y una acción dominante. La fuente está en `C:/Users/prett/Documents/ChatGPT/Otros/kids-system-studio/`.

## Cambios frente al artefacto fuente

- De `web-workspace` a una aplicación móvil dedicada.
- Panel editorial fuera del shell familiar.
- ACT-0001 actualizado de `0.2.1` a `0.2.2`.
- Roles presentados como propuestas negociables, no asignaciones rígidas.
- Escala con palabras visibles: todavía no, mucha ayuda, alguna ayuda, casi solo, solo y seguro.
- Guía práctica para que el adulto sugiera estructuras sin entregar la solución.

## No objetivos

- No implementa backend, autenticación, IA, audio, pagos ni persistencia.
- No aprueba ACT-0001 para uso familiar.
- No valida seguridad física ni eficacia pedagógica.
- No decide nombre comercial, stack nativo o Apple Kids Category.

## Siguiente prueba humana

Moderación con adultos usando datos sintéticos: completar el recorrido para uno y tres niños; medir comprensión de roles, cambios realizados, recordación de seguridad, tiempo de cierre y percepción de carga mental.
