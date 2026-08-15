# Machine-readable domain schemas

**Estado:** Draft<br>
**Versión:** 0.1

Estos JSON Schemas convierten los specs conceptuales en contratos verificables. Los documentos Markdown siguen siendo la fuente de intención; los schemas son la fuente de forma para datos e integraciones.

## Schemas

- `v0.1/activity-version.schema.json`: versión editorial inmutable de una actividad.
- `v0.1/session.schema.json`: planificación, ejecución y cierre de una sesión familiar.
- `v0.1/learner-records.schema.json`: exposiciones, observaciones e inferencias explicables.
- `v0.1/offline-pack-manifest.schema.json`: contenido, hashes, assets, asignaciones y vencimiento de un paquete descargado.
- `v0.1/sync-event.schema.json`: envelope idempotente, revisión base, payload y resolución de conflictos para sincronización.

## Ejemplos

Los seis ejemplos de `examples/` validan contra su schema y usan datos ficticios. La actividad de puente del ejemplo es un fixture de contrato; no es la serialización canónica de la ActivityVersion editorial del Pilot Pack y nunca debe tratarse como contenido publicado.

## Validación

```bash
npm install
npm run validate
```

Capas:

1. `validate:schemas`: compila los cinco JSON Schemas con AJV en modo estricto.
2. `validate:examples`: valida seis documentos positivos, incluidos evento aceptado y conflicto offline.
3. `validate:domain`: comprueba referencias y reglas entre ActivityVersion, Session, LearnerRecords, manifest y eventos.
4. `validate:docs`: comprueba enlaces Markdown locales y señales mínimas de las tres actividades piloto.

El validador de dominio genera recorridos positivos de uno, dos y tres participantes y ejecuta además once mutaciones negativas. El comando falla si acepta rango de edad invertido, participantes contradictorios, referencia de skill inexistente, publicación sin gates/pilotos, sesión completada sin cierre, Learner duplicado, cierre duplicado, evidencia para no participante, inferencia fuerte sin evidencia, rating sin valor o EvidenceLink inexistente.

## Reglas que JSON Schema no expresa completamente

- Rangos mínimos/máximos, IDs únicos y cobertura de participantes.
- Referencias rol→skill/concept/step, step→visual/exposición y safety→adult-only step.
- `primaryObjectiveSkillId` elegible, exposiciones derivables de roles/pasos reales y un Learner por sesión.
- `family_recommendation` solo con `published`; `pilot` solo con `ready_for_pilot` o `family_pilot`; `editorial_preview` para fixtures/dry runs.
- Sesión `completed` con cierre, un resultado por participante y ninguna evidencia para quien no participó.
- Publicación con gates aprobados para la misma versión/hash y records de piloto mínimos; C/D exige safety specialist.
- Inferencias enlazadas a observaciones existentes, no rechazadas y de la misma skill.
- Manifest, sesión y eventos con alcance, hash, revisión e idempotency key coherentes.

Estas invariantes están implementadas en `scripts/domain-rules.mjs` y probadas por `scripts/validate-domain.mjs`. El backend debe reutilizar o portar las mismas reglas; validar solo JSON Schema no autoriza publicación, recomendación ni sincronización.

## Límites explícitos de v0.1

- Los ejemplos no sustituyen fixtures de las tres actividades editoriales reales.
- `LearnerRecords` cubre evidencia e inferencias; preferencias, intereses provisionales y el agregado completo del Learner Model permanecen en los specs conceptuales hasta tener un contrato propio.
- La equivalencia semántica de traducciones y la seguridad física requieren revisión humana.
- El mínimo de piloto reforzado para niveles C/D se define por ActivityVersion y especialista; el validador solo exige el gate especializado al publicar.
- Cifrado local, autorización por familia y persistencia idempotente se prueban en implementación, no mediante JSON Schema.

## Versionado

- Cambios compatibles añaden campos opcionales dentro de `v0.1`.
- Cambios incompatibles crean un nuevo directorio (`v0.2`, `v1.0`).
- ActivityVersion y Session conservan la versión de schema utilizada.
