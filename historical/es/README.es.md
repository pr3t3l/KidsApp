# Kids Learning System

> **Histórico — documentación en español.** Archivado el 18 de agosto de 2026. Para trabajo vigente y toda documentación nueva, usar el [README en inglés](../../README.md) y la especificación canónica en [`docs/`](../../docs/README.md).

Repositorio de producto, pedagogía, contenido y arquitectura para un acompañante de aprendizaje familiar que convierte materiales cotidianos en actividades con propósito.

> **Estado:** documentación v0.1 en construcción. “Kids Learning System” es un nombre interno; el nombre comercial está pendiente.

## Propósito del repositorio

Este repositorio será la fuente de verdad para diseñar y, posteriormente, construir el producto. La documentación separa tres sistemas conectados:

1. **Sistema educativo:** habilidades, conceptos, progresión, observaciones y evidencia.
2. **Sistema de contenido:** biblioteca validada de actividades, focos de aprendizaje, aportes sugeridos, materiales, imágenes y seguridad.
3. **Producto de software:** familias, perfiles, planificación, ejecución, IA, datos e interfaz.

La IA no improvisará el núcleo de una actividad para una familia. Seleccionará una actividad publicada, sugerirá un foco y un aporte apropiado para cada niño, y podrá proponer adaptaciones dentro de límites definidos.

## Orden de lectura

1. [Visión del producto](docs/00-foundation/product-vision.md)
2. [Principios del producto](docs/00-foundation/product-principles.md)
3. [Glosario](docs/00-foundation/glossary.md)
4. [Alcance y versiones](docs/00-foundation/scope-and-releases.md)
5. [Baseline de privacidad infantil](docs/00-foundation/compliance-baseline.md)
6. [Marco de aprendizaje](docs/01-learning/learning-framework.md)
7. [Learner Model](docs/01-learning/learner-model.md)
8. [Modelo de actividades](docs/02-content/activity-schema.md)
9. [Estrategia de biblioteca](docs/02-content/library-strategy.md)
10. [Mapa de módulos](docs/03-product/module-map.md)
11. [User stories](docs/03-product/user-stories.md)
12. [Suscripción, trial y cancelación](docs/03-product/subscription-spec.md)
13. [Arquitectura conceptual](docs/07-engineering/architecture.md)
14. [Pilot Pack v0.1](docs/08-delivery/pilot-pack-v0.1.md)
15. [Roadmap](docs/08-delivery/roadmap.md)
16. [Prototipo móvil familiar v0.1](prototypes/family-mobile-v0.1/README.es.md)

Los agentes de desarrollo deben leer también [AGENTS.md](AGENTS.es.md).

## Arquitectura documental

```text
docs/
├── 00-foundation/   Visión, principios, alcance, vocabulario y preguntas
├── 01-learning/     Marco pedagógico, Learner Model y evidencia
├── 02-content/      Esquema, producción y seguridad de actividades
├── 03-product/      Personas, journeys, módulos y requisitos
├── 04-ux/           Arquitectura de información, interacción y flujos
├── 05-ai/           Compañero de IA, recomendación y evaluaciones
├── 06-data/         Modelo conceptual, diccionario y gobernanza
├── 07-engineering/  Arquitectura, contratos, seguridad y pruebas
└── 08-delivery/     Roadmap, vertical slices, decisiones y trazabilidad
schemas/             Contratos JSON Schema y ejemplos ficticios
scripts/             Validaciones ejecutables de contratos y documentación
prototypes/          Artefactos interactivos para validar UX antes de implementar
```

## Método de construcción

El trabajo se realizará en este orden:

1. Fundamentos y lenguaje común.
2. Modelos educativos y editoriales.
3. Journeys y reglas funcionales.
4. Modelo conceptual de datos.
5. UX y contratos técnicos.
6. Implementación por recorridos verticales.
7. Pilotos familiares y revisión.
8. Escalamiento de la biblioteca y funciones comerciales.

No se construirá toda la base de datos, todo el backend y toda la interfaz como fases aisladas. Cada vertical slice debe entregar un flujo pequeño de extremo a extremo.

## Estado de los documentos

Cada documento debe indicar uno de estos estados:

- `Draft`: incompleto o sujeto a decisiones centrales.
- `Review`: suficientemente desarrollado para discusión.
- `Approved`: aceptado como fuente de verdad.
- `Superseded`: reemplazado por otro documento o decisión.

La versión v0.1 captura las decisiones de la conversación inicial. Las decisiones pendientes están consolidadas en [Preguntas abiertas](docs/00-foundation/open-questions.md).

## Identificadores

| Prefijo | Dominio |
|---|---|
| `PRD` | Producto general |
| `LRN` | Aprendizaje |
| `ACT` | Actividades y contenido |
| `EVD` | Observación y evidencia |
| `REC` | Recomendaciones |
| `UX` | Experiencia de usuario |
| `AI` | Inteligencia artificial |
| `PRV` | Privacidad |
| `SAFE` | Seguridad física |
| `DATA` | Datos |
| `ENG` | Ingeniería |

## Prototipo de experiencia

El [prototipo móvil familiar v0.6](../../prototypes/family-mobile-v0.1/index.html) permite recorrer planificación por tiempo, un plan de cinco actividades navegables, compras consolidadas, mapa educativo, focos sugeridos por niño, preparación, facilitación de seis etapas y cierre contextual. La compra agrupa por supermercado, papelería y casa, suma consumibles y reutiliza herramientas con procedencia visible por día. Puede servirse por HTTPS como PWA instalable y conserva localmente el avance operativo para el dry run. Incluye un [sistema visual](../../prototypes/family-mobile-v0.1/design-system.html), copias standalone y evidencia de QA a 360×800 y 430×932. Usa datos sintéticos y contenido `Draft`/candidato; no constituye entrega familiar ni implementación de producción.

## Próximo hito

Ejecutar el [dry run de cinco días con Sofía](docs/08-delivery/sofia-five-day-dry-run-v0.1.md) usando la [lista consolidada de compras](docs/08-delivery/sofia-shopping-list-v0.1.md) y la [hoja breve de observación](docs/08-delivery/founder-dry-run-observation-sheet-v0.1.md). Después se ajustan lenguaje, carga mental, materiales y secuencia, y se decide qué candidatos convertir primero en `ActivityVersion`. En paralelo deben completarse los gates humanos del [Pilot Pack v0.1](docs/08-delivery/pilot-pack-v0.1.md). `VS-01` todavía requiere una actividad publicada y backend real; el prototipo no satisface ese gate.
