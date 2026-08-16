# Pocket Workshop Mobile — contrato visual

## Concepto

Un instrumento de bolsillo para preparar un taller familiar. La aplicación debe sentirse precisa y confiable para el adulto, pero dejar espacio visual y mental para la actividad física.

## Tokens

- `--ink #101820`: estructura, headers y autoridad.
- `--paper #F3F1E9`: fondo cálido de trabajo.
- `--surface #FFFEF9`: tarjetas y controles.
- `--yellow #FFC928`: única acción dominante y etapa activa.
- `--cyan #52D5E6`: explicación, guía y foco.
- `--coral #FF6B56`: Draft, bloqueo o atención, siempre con texto.
- `--mint #58C79A`: listo, guardado o sincronizado.
- `--muted #68757E`: texto secundario con contraste verificado por superficie.

## Tipografía

- Display: Bahnschrift, Arial Narrow, sans-serif; 700–800.
- Interfaz: Aptos, Segoe UI, sans-serif; 400–800.
- Técnica: Cascadia Mono, Consolas, monospace.

## Composición móvil

- Canvas de aplicación centrado, máximo 430 px en preview de escritorio.
- Safe area superior e inferior mediante `env(safe-area-inset-*)`.
- Targets táctiles mínimos de 44 px; primarios de 52–56 px.
- Bottom tabs solo en navegación de nivel superior.
- Sesión y cierre son flujos full-screen con back explícito; no muestran tabs competidoras.
- Sheets inferiores para cambiar roles o registrar excepciones reversibles.
- Una decisión dominante por pantalla.

## Firma de interacción

La **Workbench Track** muestra seis etapas como un riel horizontal táctil. La **Role Baton** nombra quién actúa ahora y permite relevo sin convertir el rol en identidad fija.

## Componentes

- Activity preview con versión Draft repetida.
- Time budget selector.
- Participant tile con selección y estado real.
- Flexible role card con contribución, objetivo y acción `Cambiar`.
- Preparation checklist.
- Workbench Track.
- Child prompt card.
- Safety boundary.
- Verbal independence scale.
- Observation receipt: qué se guarda y qué no se concluye.

## Accesibilidad

- Foco visible cian de 3 px.
- Significado redundante en color + icono + texto.
- Controles operables por teclado en el simulador.
- `aria-live` para cambios de pantalla y estado offline.
- `prefers-reduced-motion` elimina desplazamiento y transiciones.
- La escala muestra palabras completas; los números son referencias secundarias.

## Motion

- Rápido 130 ms para pressed/focus.
- Estándar 220 ms para cambio de pantalla o sheet.
- Sin animaciones repetitivas, glows ni decoración cinética.

## Identidad

Pocket Workshop y su mark de tres piezas son una dirección propuesta. No constituyen nombre ni logo comercial aprobado.
