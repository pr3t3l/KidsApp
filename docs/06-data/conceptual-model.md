# Modelo conceptual de datos

**Estado:** Draft  
**Versión:** 0.1

## Dominios

```text
Family ─┬─ AdultMembership
        ├─ Learner
        ├─ InventoryItem
        ├─ SubscriptionEntitlement
        ├─ WeeklyPlan ─ OfflinePack
        └─ PortfolioAsset ─ CommunitySubmission

Activity ─ ActivityVersion ─┬─ MaterialRequirement
                            ├─ Step
                            ├─ RoleTemplate
                            ├─ SkillMapping
                            ├─ AdaptationOption
                            └─ SafetyConstraint

Session ─┬─ ParticipantAssignment ─ PrimaryObjective
         ├─ Exposure
         ├─ Observation ─ EvidenceLink ─ Inference
         └─ CompanionInteraction
```

## Límites de agregados

### Family

Controla membresía, permisos, preferencias e inventario. No contiene directamente observaciones; las autoriza.

### ActivityVersion

Snapshot inmutable publicado. Pasos, materiales, roles, seguridad y adaptaciones se versionan juntos o mediante referencias inmutables.

### Session

Registra la ejecución real: versión, contexto, participantes, asignaciones, cambios, exposiciones y cierre.

### Learner Model

Compone observaciones e inferencias vinculadas a un Learner. Las inferencias son derivadas y reconstruibles.

### Media and Community

Separa asset privado, derivado comunitario, submission, decisión de moderación y licencia de marketing. Ninguna relación se deduce automáticamente de otra.

## Invariantes

- Una Session apunta a una ActivityVersion exacta.
- Un ParticipantAssignment apunta a un solo Learner y RoleTemplate compatible.
- Máximo un PrimaryObjective activo por participante y sesión.
- Exposure no tiene campo de desempeño.
- Observation conserva fuente y contexto.
- Inference enlaza una o más observaciones/evidencias.
- Medios se almacenan separados con propósito y expiración.
- Una versión retirada no se elimina si existen sesiones históricas; se vuelve inelegible.
- Un CommunitySubmission requiere uploader adulto autorizado y estado de moderación.
- Una licencia de marketing es independiente del permiso de comunidad.

## Eventos de dominio

- FamilyCreated
- LearnerAdded
- ActivityVersionPublished
- WeeklyPlanGenerated
- SessionStarted
- RoleChanged
- SessionCompleted
- ObservationRecorded
- InferenceProposed
- InferenceCorrected
- MediaExpired
- ActivityVersionRetired
- OfflinePackDownloaded
- SubscriptionEntitlementChanged
- CommunitySubmissionCreated
- CommunitySubmissionModerated
- CommunityPostRetired

## Pendiente para esquema físico

- Motor de base de datos.
- Estrategia de multi-tenancy.
- Proveedor de autenticación.
- Almacenamiento de medios.
- Cifrado y región.
- Analítica y aislamiento.
