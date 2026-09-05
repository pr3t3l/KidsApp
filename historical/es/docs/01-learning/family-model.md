> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](<../../../../docs/01-learning/SPEC-03 — Family Model.md>); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# SPEC-03 — Family Model

**Estado:** Draft  
**Versión:** 0.1

## 1. Propósito

Representar el contexto operativo necesario para que una recomendación funcione en la vida real, sin recopilar información familiar delicada que no mejore la actividad.

## 2. Componentes

### Familia

- Identificador interno.
- Idioma y unidades.
- Zona horaria aproximada para planificación.
- Preferencias de frecuencia y duración.
- Presupuesto y tolerancia de preparación opcionales.
- Tolerancia al desorden: baja, media, alta o desconocida.
- Espacios disponibles: mesa, piso, exterior, agua, taller; todos opcionales.
- Estado de suscripción y adultos autorizados, sin mezclarlo con Learner Models.

### Adultos

- Alias o nombre visible.
- Rol y permisos.
- Comodidad declarada con herramientas, ciencia y electrónica.
- Preferencias de instrucciones.
- Disponibilidad aproximada.

### Niños

- Referencias a Learner Models separados.
- Participación por sesión.
- La familia puede crear los perfiles que necesite; la experiencia de sesión inicial se optimiza para 1–4 niños.

### Inventario

- Material.
- Cantidad aproximada opcional.
- Estado: disponible, bajo, agotado, desconocido.
- Reutilizable o consumible.
- Herramienta restringida al adulto.

## 3. Contexto de una sesión

La recomendación usa un snapshot, no asume que el contexto familiar permanente aplica siempre:

- Participantes de hoy.
- Tiempo disponible hoy.
- Espacio.
- Nivel de desorden aceptable.
- Materiales disponibles.
- Energía o preferencia declarada opcional: tranquila, activa, sin preferencia.

## 4. Múltiples niños

El sistema debe:

- Recomendar un proyecto compartido cuando exista una combinación viable.
- Dar a cada niño un rol significativo y un objetivo principal.
- Evitar asignar sistemáticamente cuidado o enseñanza al niño mayor.
- Permitir colaboración y turnos.
- Señalar cuando una sola actividad no puede servir de forma segura al grupo.
- Mantener un camino completo para un solo niño, necesario para familias y piloto.

## 5. Requisitos

- **LRN-201:** El sistema debe soportar varios Learner Models por familia.
- **LRN-202:** El adulto elige participantes para cada sesión.
- **LRN-203:** Las preferencias familiares son editables y pueden anularse para una sesión.
- **LRN-204:** El inventario es aproximado; una recomendación debe confirmar materiales críticos.
- **LRN-205:** Cada rol infantil debe tener una contribución real al proyecto.
- **LRN-206:** La familia admite varios adultos autorizados y perfiles infantiles sin imponer un límite pequeño de producto.
- **LRN-207:** El MVP valida asignación simultánea para 1–4 participantes infantiles.
- **PRV-201:** No se solicitará estructura familiar, relaciones legales o ubicación precisa salvo necesidad aprobada.
