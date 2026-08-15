# Kids Learning System

Repositorio de producto, pedagogía, contenido y arquitectura para un acompañante de aprendizaje familiar que convierte materiales cotidianos en actividades con propósito.

> **Estado:** documentación v0.1 en construcción. “Kids Learning System” es un nombre interno; el nombre comercial está pendiente.

## Propósito del repositorio

Este repositorio será la fuente de verdad para diseñar y, posteriormente, construir el producto. La documentación separa tres sistemas conectados:

1. **Sistema educativo:** habilidades, conceptos, progresión, observaciones y evidencia.
2. **Sistema de contenido:** biblioteca validada de actividades, roles, materiales, imágenes y seguridad.
3. **Producto de software:** familias, perfiles, planificación, ejecución, IA, datos e interfaz.

La IA no improvisará el núcleo de una actividad para una familia. Seleccionará una actividad publicada, asignará objetivos y roles apropiados, y podrá proponer adaptaciones dentro de límites definidos.

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

Los agentes de desarrollo deben leer también [AGENTS.md](AGENTS.md).

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

## Próximo hito

Revisar las tres actividades del [Pilot Pack v0.1](docs/08-delivery/pilot-pack-v0.1.md), completar primero dry runs adultos y gates previos, y solo después probarlas de forma controlada con niños. En paralelo puede comenzar la infraestructura y el prototipo de `VS-01` con fixtures no familiares, pero el slice no puede darse por terminado ni exponer contenido `Draft` como publicado.
