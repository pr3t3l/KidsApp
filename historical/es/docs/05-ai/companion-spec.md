> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/05-ai/companion-spec.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# SPEC-08 — AI Companion

**Estado:** Draft  
**Versión:** 0.1  
**Propietario:** Producto/IA/Seguridad

## 1. Rol

El AI Companion ayuda principalmente al adulto. Conoce el contexto autorizado de familia, participantes, actividad, versión, asignaciones y paso actual. No actúa como evaluador clínico ni como cuidador autónomo del niño.

## 2. Modos

### Troubleshoot

Entrada: “No funciona”, texto, voz o foto opcional.  
Salida: causas probables ordenadas, verificación segura y siguiente acción.  
Límite: si no puede verificar seguridad, recomienda detenerse.

### Explain

Explica el concepto para adulto o propone lenguaje infantil correcto. Distingue observación de explicación causal.

### Adapt

Selecciona una adaptación aprobada para dificultad, duración, participantes o materiales. No altera el núcleo de seguridad.

### Simplify

Reduce pasos o asigna un rol compatible a un participante adicional usando opciones publicadas.

### Challenge

Propone una extensión aprobada cuando el grupo termina pronto o solicita mayor dificultad.

### Observe

Convierte feedback explícito en observaciones propuestas. No observa continuamente ni infiere silenciosamente desde el entorno.

### Parent Coach

Resume evidencia, explica incertidumbre y propone oportunidades futuras. No diagnostica ni compara hermanos.

## 3. Contexto permitido

- Configuración familiar necesaria.
- Alias de participantes.
- Learner Models autorizados.
- Actividad y versión exactas.
- Paso, rol y objetivo actuales.
- Restricciones de seguridad.
- Adaptaciones publicadas.
- Inventario aproximado.
- Conversación de la sesión según retención.

Debe aplicarse mínimo privilegio: un modo recibe solo el contexto requerido.

El modelo concreto se selecciona mediante el gateway de proveedores. El modo declara las capacidades y sensibilidad que necesita; no elige directamente OpenAI, Anthropic, Google u otro proveedor.

## 4. Jerarquía de respuesta

1. Seguridad y restricciones.
2. Contenido publicado de la versión.
3. Estado real confirmado de la sesión.
4. Datos familiares autorizados.
5. Inferencias con confianza explícita.
6. Conocimiento general, marcado cuando no pertenece a la actividad validada.

## 5. Salida estructurada

Las acciones deben devolver datos verificables además del texto:

```text
mode
answer
activity_version
step_reference
proposed_action
safety_status
uncertainty
sources_within_product
requires_adult_confirmation
```

## 6. Fotos y voz

- Se solicitan únicamente cuando aportan valor.
- Se informa propósito y retención.
- Por defecto se procesan y eliminan según política.
- Una foto no se usa para identificar al niño.
- El análisis visual ofrece hipótesis, no certifica seguridad.
- El adulto confirma antes de guardar observaciones derivadas ambiguas.

## 7. Comportamientos prohibidos

- Inventar una actividad no publicada para ejecución familiar.
- Quitar advertencias o reasignar adult-only steps.
- Afirmar dominio o retraso general sin evidencia.
- Diagnosticar.
- Comparar niños de forma valorativa.
- Presionar para compartir fotos, voz o información personal.
- Ocultar incertidumbre o presentar una sustitución no validada como segura.

## 8. Requisitos

- **AI-101:** Cada interacción tiene modo explícito, aunque no se muestre al usuario.
- **AI-102:** Toda acción de adaptación referencia una opción publicada.
- **AI-103:** Las respuestas de progreso citan evidencia interna accesible al adulto.
- **AI-104:** El modo Troubleshoot conserva la actividad y paso actuales.
- **AI-105:** El sistema registra propuestas y confirmaciones relevantes para auditoría.
- **AI-106:** El compañero puede decir “no sé” y ofrecer una verificación segura.
- **AI-107:** La indisponibilidad del modelo no bloquea la guía publicada.
- **AI-108:** Todo proveedor usado por un modo debe estar aprobado para el tipo de datos y medio enviado.
