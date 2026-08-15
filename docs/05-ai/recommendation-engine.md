# SPEC-06 — Recommendation and Role Assignment Engine

**Estado:** Review  
**Versión:** 0.1

## 1. Propósito

Elegir una actividad publicada que la familia pueda realizar y asignar a cada niño un rol y un objetivo principal apropiados.

## 2. Pipeline

```text
Contexto de sesión
→ filtros de elegibilidad
→ candidatos seguros
→ puntuación pedagógica y operativa
→ combinación de roles
→ objetivo principal por niño
→ explicación
→ confirmación adulta
```

## 3. Filtros duros

Una actividad se excluye si:

- No está publicada.
- Viola edad, supervisión o restricción declarada.
- No existe combinación segura de roles para participantes.
- Falta un material crítico sin sustitución aprobada.
- Excede límites explícitos de tiempo o espacio.
- Está retirada o deshabilitada.

Los filtros duros no se compensan con una puntuación alta.

## 4. Factores de ordenamiento

- Adecuación a objetivos de crecimiento.
- Variedad reciente de áreas, roles y mecanismos.
- Intereses como contexto motivador.
- Uso de materiales disponibles.
- Preparación y desorden.
- Oportunidad de recopilar evidencia útil.
- Posibilidad de participación simultánea.
- Historial de éxito y satisfacción de la actividad.

Los pesos serán configurables, auditables y probados; la primera versión puede usar reglas legibles.

## 5. Selección del objetivo principal

Para cada niño:

1. Tomar habilidades elegibles de sus roles posibles.
2. Excluir habilidades inseguras o incompatibles.
3. Preferir zona de crecimiento o consolidación.
4. Considerar metas familiares y evidencia faltante.
5. Penalizar repetición reciente.
6. Elegir exactamente una.
7. Generar una explicación breve.

Ejemplo:

> Medición fue elegida para Sofi porque ya ha contado con independencia, todavía tenemos poca evidencia de medición y el rol de Test Engineer la practica de forma natural.

## 6. Asignación de roles

La combinación debe:

- Cubrir todos los participantes.
- Respetar compatibilidad y seguridad.
- Evitar roles simbólicos.
- Reducir espera cuando sea posible.
- Rotar responsabilidades a través del tiempo.
- No convertir automáticamente al mayor en tutor.

Si no existe combinación, el motor propone otra actividad o dos bloques coordinados y explica la limitación.

## 7. Control adulto

El adulto puede:

- Cambiar participantes.
- Intercambiar roles compatibles.
- Elegir otro objetivo disponible.
- Rechazar la recomendación.
- Indicar una razón opcional.

La decisión manual se respeta y sirve como señal de producto, no como evaluación del niño.

## 8. Composición del día y la semana

El input principal es un presupuesto de minutos por día, no un número fijo de actividades. El compositor:

1. Reserva preparación y limpieza explícitas.
2. Prefiere una actividad completa que se ajuste bien al bloque.
3. Combina dos actividades solo cuando duración, transición y carga del adulto caben razonablemente.
4. No fragmenta una actividad indivisible para llenar exactamente el tiempo.
5. Mantiene balance semanal por mecanismos y áreas.
6. Permite dejar minutos libres en vez de agregar contenido sin propósito.

La semana puede proponer hasta cinco días por defecto, pero el adulto configura días y minutos independientemente.

## 9. Requisitos

- **REC-101:** Aplicar seguridad y publicación como filtros duros.
- **REC-102:** Elegir máximo un objetivo principal por niño.
- **REC-103:** Registrar todas las habilidades secundarias como exposiciones previstas.
- **REC-104:** Explicar actividad, rol y objetivo en lenguaje breve.
- **REC-105:** Permitir cambios manuales entre opciones compatibles.
- **REC-106:** Mantener variedad semanal y por niño.
- **REC-107:** Distinguir falta de evidencia de dificultad observada.
- **REC-108:** La misma entrada y configuración de reglas debe producir una decisión reproducible o registrar la aleatoriedad.
- **REC-109:** La cantidad de actividades diarias se deriva del presupuesto de tiempo y de actividades indivisibles.
- **REC-110:** Preparación, transición y limpieza forman parte de la estimación familiar.
- **REC-111:** El plan no agrega una segunda actividad solo para llenar minutos residuales.
