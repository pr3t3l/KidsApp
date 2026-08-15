# Instrucciones para agentes

## Misión

Construir un sistema de aprendizaje familiar seguro, explicable y de baja fricción, siguiendo la documentación de `docs/` como fuente de verdad.

## Lectura obligatoria

Antes de cambiar producto, datos, IA o comportamiento:

1. Leer `README.md`.
2. Leer `docs/00-foundation/product-principles.md` y `glossary.md`.
3. Para datos, medios, IA o comunidad, leer `docs/00-foundation/compliance-baseline.md`.
4. Leer el spec del dominio afectado.
5. Leer `docs/08-delivery/traceability.md`.
6. Revisar `docs/00-foundation/open-questions.md` y `docs/08-delivery/decision-log.md`.

## Precedencia

En caso de contradicción, usar este orden:

1. Seguridad física y privacidad.
2. Decisiones aprobadas en el decision log.
3. Principios del producto.
4. Specs de dominio.
5. Specs de módulo o flujo.
6. Historias y tareas de implementación.

No resolver contradicciones importantes inventando una interpretación. Documentar la contradicción y pedir una decisión.

## Reglas no negociables

- Una actividad entregada a una familia debe provenir de una versión publicada de la biblioteca.
- La IA no modifica materiales, pasos o restricciones que cambien el perfil de seguridad.
- Cada niño tiene como máximo un objetivo principal evaluado por sesión; las demás habilidades son exposiciones, salvo que el adulto elija “Evaluar más”.
- Las conclusiones sobre un niño deben ser trazables a observaciones y expresar incertidumbre.
- Nunca convertir observaciones educativas en diagnósticos clínicos, psicológicos o de inteligencia.
- No almacenar imágenes, audio o datos infantiles innecesarios por defecto.
- No usar una fecha de nacimiento completa cuando un rango de edad sea suficiente.
- El adulto conserva control para omitir, corregir y eliminar.
- El flujo de evaluación predeterminado debe poder completarse en menos de 20 segundos para tres niños.

## Cambios de documentación

- Mantener español como idioma fuente durante v0.x.
- Añadir identificadores estables a requisitos verificables.
- Actualizar enlaces y trazabilidad cuando cambie un requisito.
- Registrar decisiones arquitectónicas o de producto en `docs/08-delivery/decision-log.md`.
- No marcar un documento como `Approved` sin confirmación humana.
- Usar `TBD` solo junto con una pregunta o decisión pendiente identificable.

## Implementación futura

- Trabajar por vertical slices descritos en `docs/08-delivery/vertical-slices.md`.
- Ejecutar `npm install` una vez y `npm run validate` antes de entregar cambios de contratos, documentación o actividades piloto.
- Toda función debe enlazar requisitos y criterios de aceptación.
- Añadir pruebas para reglas de seguridad, autorización, evidencia y límites de adaptación de IA.
- Evitar incorporar servicios o frameworks no decididos en los specs.
