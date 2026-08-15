# Requisitos del producto

**Estado:** Draft  
**Versión:** 0.1

## Familia y perfiles

- **PRD-001:** Un adulto puede crear una familia con configuración mínima.
- **PRD-002:** Una familia puede contener varios adultos autorizados y varios niños.
- **PRD-003:** Un niño se representa con alias y rango de edad por defecto.
- **PRD-004:** El adulto puede editar o eliminar perfiles y datos derivados.
- **PRD-005:** El sistema debe permitir comenzar sin completar inventario ni evaluación inicial extensa.
- **PRD-006:** Una familia puede autorizar varios adultos bajo una suscripción administrada por el propietario.
- **PRD-007:** El producto no impone un límite comercial pequeño de perfiles; el MVP optimiza sesiones de 1–4 participantes.
- **PRD-008:** Todo contenido y flujo principal de lanzamiento está disponible en inglés y español.

## Actividades

- **PRD-101:** Solo se muestran como recomendables versiones publicadas.
- **PRD-102:** Antes de iniciar se muestran duración, materiales, preparación, propósito y seguridad.
- **PRD-103:** El adulto confirma participantes y materiales críticos.
- **PRD-104:** Cada participante infantil recibe un rol y un objetivo principal.
- **PRD-105:** El adulto puede cambiar roles y objetivos entre opciones compatibles.
- **PRD-106:** La sesión guarda la versión exacta y asignaciones reales.

## Planificación

- **REC-000:** El adulto configura minutos disponibles por día; el sistema puede asignar una o varias actividades al bloque.
- **REC-001:** El plan considera tiempo, participantes, inventario, seguridad, evidencia, variedad e intereses.
- **REC-002:** Cada recomendación incluye una razón breve.
- **REC-003:** El adulto puede sustituir una actividad sin perder el resto del plan.
- **REC-004:** El sistema evita repetición excesiva de área, material y rol.
- **REC-005:** Si no existe actividad segura para todos, debe explicarlo y proponer alternativas.
- **REC-006:** El plan semanal descargado conserva roles, objetivos, pasos, seguridad e imágenes sin conexión.

## Ejecución y cierre

- **UX-101:** La guía permite avanzar, retroceder y reanudar.
- **UX-102:** Cada paso muestra actor, acción, resultado y advertencia relevante.
- **UX-103:** El cierre normal requiere una valoración por niño.
- **UX-104:** “Evaluar más” y nota de voz son opcionales.
- **UX-105:** El adulto puede omitir el cierre sin señal negativa.

## Evidencia y progreso

- **EVD-101:** Las exposiciones se registran automáticamente desde el rol real.
- **EVD-102:** El sistema muestra qué observación se creó desde una valoración o voz.
- **EVD-103:** Las inferencias son explicables y corregibles.
- **EVD-104:** La vista de progreso distingue explorado, observado e inferido.
- **EVD-105:** No existen puntuación global ni comparación entre niños.

## IA

- **AI-001:** El compañero conoce familia autorizada, actividad, versión, paso y sesión actuales.
- **AI-002:** La IA opera únicamente en modos y límites documentados.
- **AI-003:** Adaptaciones automáticas deben provenir de opciones aprobadas.
- **AI-004:** La IA debe expresar incertidumbre y detener recomendaciones inseguras.
- **AI-005:** Una salida de IA no puede publicar contenido sin workflow editorial.

## Privacidad y seguridad

- **PRV-001:** Recopilar solo datos necesarios para la experiencia.
- **PRV-002:** Fotos y audio se procesan temporalmente por defecto.
- **PRV-003:** Conservar medios requiere elección explícita y propósito visible.
- **PRV-004:** El adulto puede exportar y solicitar eliminación.
- **SAFE-101:** Restricciones críticas de seguridad no pueden anularse desde personalización.
- **SAFE-102:** Una versión retirada deja de ser elegible inmediatamente.

## Suscripción y offline

- **PRD-SUB-001:** El producto soporta suscripción mensual y anual.
- **PRD-SUB-002:** La pérdida temporal de conexión no interrumpe una actividad ya descargada.
- **PRD-SUB-003:** El estado de acceso usa el entitlement de la tienda/servidor y una política de gracia; no exige una verificación manual arbitraria mensual.
- **PRD-SUB-004:** La prueba comercial dura siete días y es distinta del acceso gratuito del piloto.
- **PRD-SUB-005:** La aplicación enlaza directamente a la gestión/cancelación del canal de origen.
- **PRD-SUB-006:** Cancelar no elimina datos familiares ni corta el período ya pagado.
- **PRD-OFF-001:** Recomendación, AI Companion, comunidad y sincronización requieren conexión.
- **PRD-OFF-002:** Evaluaciones realizadas offline se almacenan cifradas localmente y se sincronizan de forma idempotente.

## Comunidad y portafolio

- **PRV-COM-001:** Guardar en portafolio privado y publicar en comunidad son decisiones separadas.
- **PRV-COM-002:** Solo un adulto autorizado puede publicar contenido comunitario.
- **PRV-COM-003:** Toda publicación comunitaria pasa moderación antes de hacerse visible en la primera versión.
- **PRV-COM-004:** Marketing requiere consentimiento/licencia separados de la publicación comunitaria.
- **PRV-COM-005:** La primera comunidad no incluye mensajes directos, comentarios ni perfiles infantiles públicos.

## Operación editorial

- **PRD-OPS-001:** Autores y especialistas pueden proponer, comentar y revisar ActivityVersions según permisos.
- **PRD-OPS-002:** Pedagogía y seguridad son gates independientes antes de publicar.
- **PRD-OPS-003:** Una ActivityVersion muestra diferencias, historial, responsables y reviews pendientes.
- **PRD-OPS-004:** Ninguna sugerencia de IA se publica sin aprobación humana.
