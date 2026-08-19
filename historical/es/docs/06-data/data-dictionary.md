> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/06-data/data-dictionary.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Diccionario de datos conceptual

**Estado:** Draft  
**Versión:** 0.1

| Entidad | Campos conceptuales clave | Datos sensibles |
|---|---|---|
| Family | id, locale, units, timezone, preferences | Configuración privada |
| Adult | id, display_name, auth_subject | Identidad/cuenta |
| Membership | family, adult, role, status | Autorización |
| Learner | id, family, alias, age_band, language | Datos infantiles |
| Skill | id, name, definition, graph_version | No personal |
| Activity | id, canonical_title | No personal |
| ActivityVersion | id, version, status, content_hash | No personal |
| RoleTemplate | version, responsibilities, eligible_skills | No personal |
| Session | family, activity_version, timestamps, status | Conducta familiar |
| Assignment | session, learner, role, primary_objective | Datos infantiles |
| Exposure | session, learner, skill/concept, source | Datos infantiles |
| Observation | learner, session, source, structured_fact, status | Datos infantiles |
| EvidenceLink | observation, skill, weight/context | Datos infantiles derivados |
| Inference | learner, skill, state, confidence, explanation | Perfil derivado infantil |
| InventoryItem | family, material, approximate_state | Contexto doméstico |
| MediaAsset | family, purpose, retention, expiry, owner | Potencialmente muy sensible |
| CompanionInteraction | mode, context_refs, action, safety_result | Puede contener contenido privado |
| SubscriptionEntitlement | family, billing_source, payer adult, product, trial, status, expiry/grace | Datos comerciales |
| OfflinePack | family, plan/version manifest, hashes, expiry | Datos privados locales |
| PortfolioAsset | family, adult owner, activity/session, retention | Medio de alta sensibilidad |
| CommunitySubmission | asset derivative, activity_version, adult uploader, moderation | UGC potencialmente sensible |
| ModerationDecision | submission, reviewer, reason, action | Operación interna |
| MarketingLicense | asset, adult grantor, scope, channels, expiry/revocation | Consentimiento contractual |

## Clasificación provisional

- `PUBLIC_CONTENT`: actividades publicadas y taxonomía.
- `INTERNAL_CONTENT`: borradores, revisiones y prompts.
- `FAMILY_PRIVATE`: preferencias, planes e inventario.
- `CHILD_PRIVATE`: exposiciones, observaciones e inferencias.
- `HIGH_SENSITIVITY_MEDIA`: fotos, video, audio y transcripciones asociadas.
- `COMMUNITY_UGC`: derivados destinados a visibilidad más amplia, todavía sujetos a controles.

## Reglas

- Los identificadores internos no deben contener nombres.
- Los campos libres se minimizan y se someten a controles de acceso/retención.
- Los datos derivados conservan procedencia.
- Las eliminaciones deben propagarse a índices, cachés y copias según política aprobada.
