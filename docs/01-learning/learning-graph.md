# SPEC-04 — Learning Graph

**Estado:** Draft  
**Versión:** 0.1

## 1. Propósito

Representar conceptos, habilidades y relaciones para etiquetar actividades, explicar progresión y detectar oportunidades de aprendizaje.

## 2. Tipos de nodo

- Área.
- Concepto.
- Habilidad.
- Nivel funcional de una habilidad.

## 3. Tipos de relación

| Relación | Significado |
|---|---|
| `PART_OF` | El nodo pertenece a una categoría mayor. |
| `SUPPORTS` | Una habilidad facilita otra sin ser requisito. |
| `PREREQUISITE_FOR` | Conocimiento previo recomendado; incluye fuerza. |
| `OBSERVABLE_BY` | Una acción puede aportar evidencia. |
| `RELATED_TO` | Relación explicativa sin secuencia. |

## 4. Ejemplo

```text
Electricidad
├── Circuito cerrado
│   ├── identificar un camino continuo
│   └── conectar fuente y carga
├── Polaridad
├── Conductores y aislantes
├── Interruptores
└── Motores
    ├── energía eléctrica → movimiento
    └── dirección de rotación
```

## 5. Reglas

- Los prerrequisitos no bloquean automáticamente una actividad; pueden convertirla en exploración.
- Cada habilidad tiene acciones observables y ejemplos no válidos.
- Cada nodo conserva versión, estado editorial y justificación.
- El recomendador debe explicar qué camino del grafo intenta reforzar.
- El grafo no contiene puntuaciones personales; esas viven en el Learner Model.

## 6. Requisitos

- **LRN-301:** Cada actividad publicada debe enlazar al menos un concepto o habilidad.
- **LRN-302:** Cada habilidad evaluable debe tener una rúbrica observable.
- **LRN-303:** Las relaciones deben ser versionadas y auditables.
- **LRN-304:** El sistema debe admitir evidencia insuficiente en nodos no explorados.
- **LRN-305:** Un cambio del grafo no puede reinterpretar silenciosamente observaciones históricas.
