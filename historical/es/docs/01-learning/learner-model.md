> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/01-learning/learner-model.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# SPEC-02 — Learner Model

**Estado:** Review  
**Versión:** 0.1  
**Propietario:** Producto/Pedagogía/Datos

## 1. Propósito

Mantener una memoria educativa privada, estructurada y corregible para cada niño, suficiente para mejorar la siguiente decisión sin producir diagnósticos ni perfiles innecesarios.

## 2. Principios

- Un Learner Model pertenece a un solo niño dentro de una familia.
- Registra hechos contextuales antes que conclusiones.
- Separa habilidad, interés, independencia y preferencias observadas.
- Expresa incertidumbre.
- Permite corrección y eliminación.
- No entrena un modelo de IA independiente para cada niño; proporciona contexto estructurado a un modelo general.

## 3. Datos mínimos

### Perfil

- Alias o nickname.
- Rango de edad; edad exacta opcional cuando sea necesaria.
- Idioma preferido.
- Restricciones de participación declaradas por el adulto, con minimización.
- Intereses opcionales.
- Historial de actividades y roles.

### Estado educativo derivado

Por cada habilidad relevante:

- Exposición acumulada.
- Observaciones recientes.
- Independencia observada por contexto.
- Inferencia actual, si existe.
- Confianza.
- Fecha de última evidencia.
- Evidencia que respalda la inferencia.
- Estado: inferida, confirmada, corregida o descartada.

## 4. Lo que no almacena

- IQ o “inteligencia”.
- Diagnóstico.
- Valoración global del niño.
- Etiquetas de personalidad permanentes.
- Reconocimiento facial o biométrico.
- Dirección, escuela, apellido o ubicación precisa.
- Fecha de nacimiento completa salvo justificación aprobada.
- Comparación pública con otros niños.

## 5. Objetivo principal

Antes de una sesión, cada niño recibe como máximo un objetivo principal. La elección debe:

1. Pertenecer a las habilidades posibles de la actividad y al rol asignado.
2. Ser segura y viable para el niño.
3. Representar consolidación o crecimiento apropiado.
4. Aportar evidencia útil o cumplir un objetivo familiar.
5. Mantener variedad con respecto a sesiones recientes.

El adulto puede cambiar el objetivo antes de comenzar. El cambio se registra como decisión del adulto, no como fallo del recomendador.

## 6. Exposiciones secundarias

El sistema registra automáticamente las habilidades y conceptos presentes en el rol ejecutado. Una exposición indica solamente oportunidad; no modifica por sí sola la inferencia de capacidad.

## 7. Dimensiones separadas

### Desempeño contextual

Qué acción ocurrió en una actividad específica.

### Independencia

Cuánto apoyo fue necesario, usando la escala de EVD-003.

### Interés

Señal opcional de participación o atracción, registrada como baja, media, alta o desconocida.

### Preferencia provisional

Patrón respaldado por varias observaciones, por ejemplo “participa más cuando puede manipular antes de escuchar la explicación”. Nunca se presenta como estilo fijo.

## 8. Confianza

| Nivel | Definición |
|---|---|
| Insuficiente | No existe observación directa o solo hay exposiciones. |
| Inicial | Una observación útil o varias señales indirectas. |
| Moderada | Varias observaciones coherentes en más de una sesión. |
| Fuerte | Evidencia repetida y reciente en contextos variados, sin contradicciones relevantes. |

Los umbrales exactos serán configurables y deberán validarse; no se convertirán en una fórmula opaca.

## 9. Cambios del modelo

- Una nueva observación no sobrescribe las anteriores.
- Una contradicción reduce confianza o separa contextos; no se descarta automáticamente.
- La evidencia antigua pierde peso para recomendaciones, pero se conserva según política de retención.
- Una corrección del adulto debe tener prioridad sobre una inferencia automática y conservar trazabilidad.
- Las inferencias pueden actualizarse automáticamente desde evidencia suficiente, pero el cambio debe quedar visible, explicable y corregible. No se exige confirmar cada actualización.
- Cuando una nota de voz no permite atribuir con claridad niño, habilidad o contexto, la atribución debe confirmarse antes de afectar una inferencia.

## 10. Respuestas responsables

Ante “¿Cómo va Sofi en matemáticas?”, el sistema debe responder por subáreas y evidencia:

> Hay evidencia moderada sobre conteo y clasificación. Todavía no hay suficiente información sobre medición o geometría para resumir matemáticas en general.

Después puede sugerir actividades para observar áreas faltantes.

## 11. Requisitos

- **LRN-101:** Cada niño debe tener un Learner Model separado.
- **LRN-102:** Una sesión puede asignar como máximo un objetivo principal evaluado por niño.
- **LRN-103:** Las exposiciones no pueden interpretarse como desempeño.
- **LRN-104:** Toda inferencia debe enlazar evidencia y confianza.
- **LRN-105:** El adulto debe poder corregir o descartar inferencias.
- **LRN-106:** El sistema debe separar interés, desempeño e independencia.
- **LRN-107:** La respuesta debe indicar áreas sin evidencia suficiente.
- **LRN-108:** Una eliminación de perfil debe eliminar o anonimizar sus datos dependientes según política aprobada.

## 12. Criterios de aceptación

- Se puede explicar por qué una habilidad tiene confianza moderada.
- Una sesión omitida no produce señal negativa.
- Una exposición sin evaluación no aumenta capacidad inferida.
- Una corrección por “herramienta dañada” deja intacta la inferencia de habilidad y registra el contexto.
- El adulto puede visualizar, corregir y eliminar observaciones.
