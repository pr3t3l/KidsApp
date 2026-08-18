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
- Sheets inferiores para ampliar el fundamento educativo, resolver un problema concreto o registrar excepciones reversibles.
- Una decisión dominante por pantalla.

## Firma de interacción

La **Workbench Track** es la única señal de progreso y muestra seis etapas como un riel horizontal táctil. El **Stage Brief** combina la entrada causal con un visual específico de la fase. La **Facilitation Ladder** prioriza `Haz esto` y el guion; después presenta seguridad, acciones nominales, decisión integrada y un bloque compacto de observación/continuación. Antes de empezar, el **Learning Map** explica el propósito y convierte los roles editoriales internos en focos de observación, sin reservar el ciclo esencial a un solo niño.

## Componentes

- Activity preview con versión Draft repetida.
- Time budget selector.
- Participant tile con selección y estado real.
- Learning Map con propósito, áreas, conceptos, mecanismo y decisión infantil.
- Child Focus Card con nombre, foco observable, aporte sugerido, razón y exposiciones.
- Preparation checklist.
- Workbench Track.
- Stage Brief con contexto inicial, visual de fase y habilidades practicadas.
- Adult Action Block con pasos y guion literal.
- Named Child Action List para todos los participantes activos.
- Child Decision integrada en las acciones; Observation/Continue Check combinado.
- Safety boundary.
- Contextual Help Sheet con problema, cambio, impacto, reanudación y límite de seguridad.
- Verbal independence scale.
- Direct Save Transparency: qué se guarda y cómo corregirlo, sin recibo obligatorio.
- Planned Activity Card: día, estado, promesa breve y affordance de navegación táctil.
- Shopping Aggregate Row: total, detalle, días de origen y regla textual `SUMA` o `REUSA`.

## Accesibilidad

- Foco visible cian de 3 px.
- Significado redundante en color + icono + texto.
- Controles operables por teclado en el simulador.
- `aria-live` para cambios de pantalla y estado offline.
- `prefers-reduced-motion` elimina desplazamiento y transiciones.
- La escala muestra palabras completas; los números son referencias secundarias.
- Los tiempos de usabilidad se miden fuera de la interfaz; el cierre no muestra cronómetros ni cuentas regresivas.

## Motion

- Rápido 130 ms para pressed/focus.
- Estándar 220 ms para cambio de pantalla o sheet.
- Sin animaciones repetitivas, glows ni decoración cinética.

## Identidad

Pocket Workshop y su mark de tres piezas son una dirección propuesta. No constituyen nombre ni logo comercial aprobado.
