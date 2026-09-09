> **Copia de lectura y entrega en español, no normativa.** La fuente canónica es [LIDR course concept evidence](../../../../docs/08-delivery/lidr-course-concept-evidence.md). Esta traducción no introduce requisitos ni decisiones.

# Evidencia de conceptos del programa LIDR — Kids Learning System

**Estado:** Review
**Versión:** 1.0
**Alumno:** Alfredo Pretel
**Evidencia revisada:** 9 de septiembre de 2026

## Propósito y criterio de evidencia

Este informe explica, sesión por sesión, dónde se aplican los conceptos de AI Engineering en Kids Learning System, por qué se usaron y cuáles siguen siendo parciales o externos. La revisión utiliza la exportación local del curso para las sesiones 1–15 y el temario de la sesión 16 suministrado por el alumno. Por eso, la sesión 16 se contrasta con los títulos del temario compartido y no se presenta como una revisión línea por línea de un artículo local que no estaba en la exportación.

Los estados usados significan:

- **Implementado y verificado localmente:** hay código ejecutable y una prueba automatizada o de navegador.
- **Implementado con evidencia sintética:** existe el contrato con forma de producción, pero se usan fixtures en lugar de proveedores, familias o infraestructura reales.
- **Condicionado por valor o seguridad:** se evaluó el concepto y se omitió o limitó porque todavía no existe evidencia suficiente de valor o seguridad.
- **Evidencia externa pendiente:** hacen falta credenciales, infraestructura alojada, una revisión humana, una ejecución física o un piloto real.

Los resultados y gates actuales están en `docs/08-delivery/implementation-evidence.md`.

## Producto y arquitectura

Kids Learning System ayuda a un adulto a facilitar actividades prácticas bilingües para niños de 5–10 años. La guía revisada sigue siendo la fuente de verdad. La IA puede explicar, diagnosticar un problema de la actividad o proponer una adaptación/reemplazo aprobado, pero no puede cambiar la seguridad silenciosamente, publicar contenido ni diagnosticar al niño.

El sistema incluye:

- PWA familiar bilingüe y workspace administrativo/editorial bilingüe en React;
- servicio FastAPI con políticas deterministas;
- CAG de versión exacta y RAG híbrido limitado a contenido publicado;
- grafo familiar acotado en LangGraph y otro grafo multiagente editorial;
- gateway neutral con OpenRouter, OpenAI directo y Anthropic directo;
- contratos Supabase/PostgreSQL/pgvector/RLS/Vault;
- contenido compacto y versionado, evals, costos, observabilidad, Docker y CI/CD.

## Revisión sesión por sesión

### Sesión 1 — APIs de LLM y preparación del entorno

**Conceptos:** Responses API de OpenAI, Messages API de Anthropic, parámetros, estructura de respuesta, tokens, IDs de modelo/request, causas de cierre, costos y errores.

**Aplicación:** `services/ai/kids_ai/model_gateway.py` implementa tres adaptadores tras un contrato común. El adaptador directo de OpenAI usa la forma de Responses con `store: false` y captura ID de respuesta/request, modelo exacto, fecha, estado/causa de incompletitud, tokens de entrada/salida/total/caché/razonamiento, service tier y headers permitidos. El adaptador directo de Anthropic usa Messages y captura request ID HTTP, message ID, modelo, `stop_reason`, `stop_sequence`, tokens, creación/lectura de prompt cache, service tier y metadata acotada; calcula total y tiempo cuando no llegan.

`provider_models.py` normaliza ejecución, uso, facturación, ruta y metadata sin copiar prompts o respuestas completas a la telemetría. `test_provider_adapters.py` cubre respuestas, caché, razonamiento, streaming, fallback y errores.

**Estado:** implementado y verificado con fixtures; credenciales, elegibilidad de datos y conciliación real siguen pendientes.

### Sesión 2 — Primer CAG

**Conceptos:** Cache-Augmented Generation, disciplina de ventana de contexto, contexto estable/dinámico y evolución de CAG a RAG.

**Aplicación:** `docs/05-ai/cag-rag-and-agent-runtime.md` y `workflow.py` construyen un prompt pequeño y ordenado: política estable de producto/seguridad, versión inmutable exacta, idioma, bloque actual, mutaciones permitidas y luego evidencia recuperada. No se envía el snapshot editorial, ambos idiomas, toda la historia familiar ni todo el catálogo.

Este es CAG como patrón arquitectónico; no se confunde con caché de respuestas del proveedor.

**Estado:** implementado y verificado localmente.

### Sesión 3 — Wrappers, fallback, caché, streaming y observabilidad

**Conceptos:** wrapper conversacional, abstracción de proveedores, fallback, caché inteligente, streaming, logging y trazabilidad.

**Aplicación:** el companion de React es una interfaz independiente del proveedor. `ModelGateway` selecciona proveedor/modelo por `operation_key` versionada. El owner puede probar, evaluar, activar y revertir rutas; un fallback debe cumplir las mismas políticas de capacidad, datos, evaluación y presupuesto.

No se implementó una caché general de respuestas LLM: el contexto familiar, el paso y las opciones aprobadas cambian, y una respuesta insegura por estar desactualizada no compensa el ahorro. Sí se contabiliza prompt cache reportado por los proveedores. OpenRouter procesa la metadata del chunk final de streaming, pero el render token a token no se implementó porque las respuestas son cortas y la UX actual no lo necesita.

`services/ai/app.py` instrumenta FastAPI con Logfire sin capturar headers y no envía si falta el token. La [traza pública histórica](https://logfire-us.pydantic.dev/public-trace/6828aff0-bdb3-4113-b088-e56dd416fb79?spanId=a5df1c1a648534fd) prueba el ejercicio anterior, pero no se presenta como evidencia del release final.

**Estado:** wrapper, fallback y observabilidad implementados; streaming visual y caché semántica condicionados por valor.

### Sesión 4 — Productos de IA avanzados

**Conceptos:** convertir una demo de modelo en producto con interfaz, estado, restricciones, errores y límites operativos.

**Aplicación:** la IA es solo una dependencia dentro de login, onboarding, familia, plan, catálogo, preparación exacta, puerta adulta, sesión, propuesta, confirmación, cierre, trayectoria, feedback, privacidad y workspace administrativo. El software determinista conserva autorización, elegibilidad, seguridad, validación y fallback cuando la IA no está disponible.

**Estado:** implementado localmente; usabilidad con familias reales pendiente.

### Sesión 5 — Contexto dinámico, memoria, tiers, testing y Actor–Critic–Boss

**Conceptos:** contexto externo, memoria versus historial, prompts adaptativos por tier, pruebas de LLM y composición Actor–Critic–Boss.

**Aplicación:** el contexto externo entra únicamente por investigación de fuentes permitidas en la fábrica editorial y por chunks publicados en el RAG familiar. El modelo familiar no recibe navegador ni acceso libre a base de datos.

En lugar de persistir conversaciones libres, se guarda el snapshot inmutable de sesión, bloque actual, propuesta pendiente y señales estructuradas confirmadas. Las “tiers” se modelan como políticas por operación: clasificación, respuesta, autoría, crítica, localización y embeddings pueden usar deployments distintos sin exponerlo a la familia.

El golden set y las pruebas de políticas/API cubren regresión. Actor–Critic–Boss aparece en el grafo editorial: autor por etapas, críticos especialistas y supervisor/sintetizador, siempre sin autoridad de aprobación para la IA.

**Estado:** implementado y verificado, con memoria deliberadamente mínima.

### Sesión 6 — Data-driven AI, calidad e ingestión

**Conceptos:** auditoría de datos, decisiones por calidad, extracción multiformato, limpieza/normalización/validación, PII, anonimización y borrado.

**Aplicación:** la actividad se divide en core neutral, locales, fuentes/derechos/revisiones, versión compilada inmutable y chunks. `editorial_compile.py` valida referencias, unidades, materiales, controles de riesgo, idiomas, hashes y tamaños. Derechos incorrectos, gates faltantes o schemas inválidos bloquean el release.

No se implementó un extractor general de PDF/audio/Office porque los datos reales de este piloto son URLs revisadas y JSON estructurado. La familia usa alias/banda de edad, evita correo infantil, nacimiento completo, fotos y voz, redacta posible PII de feedback y dispone de exportación/eliminación.

**Estado:** calidad, normalización, validación y minimización implementadas; extracción general condicionada por valor; revisión legal externa.

### Sesión 7 — Embeddings y chunking

**Conceptos:** representación semántica, selección de modelos, chunking profesional y presupuestos específicos del dominio.

**Aplicación:** `activity_chunk` conserva modelo/versión del embedding y vector de 1.536 dimensiones. OpenAI/OpenRouter para embeddings se resuelven por `retrieval.embed`. El chunking es estructural —overview, paso, seguridad, adaptación— y no un corte arbitrario; cada resultado tiene fuente, versión exacta e idioma. Los contratos Activity V2 y las etapas de modelo fallan CI si exceden bytes/tokens.

**Estado:** implementado con evidencia sintética; generación y comparación live pendientes.

### Sesión 8 — Bases vectoriales y pgvector

**Conceptos:** cuándo usar vectores, pgvector, HNSW/IVFFlat/DiskANN, esquema, búsqueda y tuning.

**Aplicación:** `202609050001_final_project_core.sql` define columnas vector/FTS, índice HNSW coseno y función híbrida. Filtra versión publicada exacta e idioma, aplica threshold semántico `0.55` y combina rangos full-text/vector con RRF. PostgreSQL mantiene juntos autorización relacional, contenido y vectores.

Se eligió HNSW para un catálogo pequeño y de lectura frecuente. IVFFlat/DiskANN no se configuraron prematuramente. Planes de consulta, advisors y tuning necesitan el Supabase real.

**Estado:** SQL con forma de producción y parseado; rendimiento alojado pendiente.

### Sesión 9 — Fundamentos de RAG

**Conceptos:** reformulación, top-k/threshold/filtros, augmentation y retriever aislado/seguro.

**Aplicación:** el workflow clasifica intención, rechaza solicitudes inseguras o sensibles innecesarias, recupera solamente la misma actividad publicada, versión e idioma y ensambla contexto pequeño con IDs citables. Los reemplazos filtran edad, participantes, tiempo, desorden, riesgo y canal antes del ranking. El repositorio —no el LLM— tiene acceso a los datos.

`catalog.rewrite_query` existe como operación independiente, pero las preguntas simples del paso exacto no pagan siempre una llamada extra.

**Estado:** implementado localmente; ejecución vectorial de producción pendiente.

### Sesión 10 — Recuperación avanzada

**Conceptos:** reranking, medición de relevancia, búsqueda híbrida, expansión/descomposición, multiíndice y filtros contextuales/temporales.

**Aplicación:** pgvector + full-text + RRF están implementados. El golden mide Recall@5 y corrección de fuentes. El routing separa troubleshooting de actividad exacta y reemplazo de catálogo filtrado. Versión, idioma y release son filtros obligatorios.

El reranker permanece apagado hasta demostrar una mejora que justifique costo/latencia. La descomposición general y muchos índices no aportan todavía a este dominio corto. El tiempo se maneja con versiones inmutables, retiro y cohortes, no con recencia difusa.

**Estado:** búsqueda híbrida, relevancia y filtros implementados; reranking/descomposición/multiíndice condicionados por valor.

### Sesión 11 — Generación y calidad RAG avanzada

**Conceptos:** content augmentation, síntesis multifuente, citación, alucinaciones, reindexado/versionado y RAGAS.

**Aplicación:** el contexto distingue política de evidencia y etiqueta chunks exactos. La respuesta devuelve IDs de fuente; evidencia insuficiente o incompatible produce abstención segura. Versiones de actividad/localización, hashes, modelo/versión de embedding y jobs de reindexado evitan drift silencioso. Los críticos editoriales revisan fuentes y un nodo sintetiza sin aprobar.

No se afirma integración con RAGAS. `evals/run_golden.py` implementa las medidas necesarias para este caso: Recall@5, corrección de fuente y abstención segura. Utilidad y groundedness humanos quedan como gates live/piloto.

**Estado:** atribución, mitigación y versionado implementados; librería RAGAS no usada; calidad live pendiente.

### Sesión 12 — Agentes y contratos de tools

**Conceptos:** cuándo usar agente, anatomía del loop, function calling, schemas, diseño de tools y costo.

**Aplicación:** el grafo familiar decide entre resolver, adaptar o reemplazar; recupera evidencia y responde o crea una propuesta pendiente. Los contratos son tipados y estrechos. El modelo no ejecuta SQL, navega libremente, publica, baja riesgo ni modifica directamente. Preflight, límites de salida, timeout, usage y fallback acotan cada operación.

**Estado:** implementado y verificado.

### Sesión 13 — Orquestación con LangGraph

**Conceptos:** StateGraph, estado/checkpointers, paralelo, routing condicional, errores y Logfire/LangSmith.

**Aplicación:** `workflow.py` usa `StateGraph` para el companion y `editorial_agents.py` para especialistas. Los críticos independientes corren en paralelo y luego se sintetizan. Errores y límites de presupuesto/proveedor devuelven guía determinista o conservan el job en etapa recuperable.

No se usa el checkpointer de LangGraph como almacenamiento autoritativo. La durabilidad serverless vive en jobs de base de datos, propuestas pendientes y versiones inmutables con APIs de reanudación. Logfire instrumenta FastAPI.

**Estado:** grafos, paralelo, condicionales y recuperación implementados; checkpointer sustituido conscientemente por persistencia de dominio.

### Sesión 14 — Sistemas multiagente

**Conceptos:** supervisor, comunicación/handoff, human-in-the-loop, competición/síntesis, mínimo privilegio, validación y auditoría.

**Aplicación:** el grafo editorial incluye supervisor y críticos de educación, materia, seguridad, consistencia y duplicidad. Se comunican con findings tipados; corren en paralelo y el sintetizador devuelve siempre `canApprove: false`. Revisión humana, piloto y release son gates separados. Roles, MFA reciente, derechos, presupuesto y audit limitan cada acción.

El companion familiar no se convirtió innecesariamente en múltiples agentes: un grafo acotado aporta más seguridad y menos costo. Las pausas humanas viven en estado editorial/propuestas persistidas.

**Estado:** supervisión, síntesis y gates humanos implementados; agentes familiares autónomos prohibidos por diseño.

### Sesión 15 — Producción, Docker, CI/CD y cloud

**Conceptos:** criterio de producción, documentación, servicios, contenedores, CI/CD seguro y despliegue cloud.

**Aplicación:** el repo documenta arquitectura, contratos, seguridad, límites y evidencia. Web/API son deployables separados con PostgreSQL externo. Hay `docker-compose.yml`, Dockerfiles para web/API, workflow `.github/workflows/ci.yml`, auditorías de dependencias, health y configuraciones Vercel sin credenciales comprometidas.

Docker Desktop está detenido tras el reinicio del PC, así que no se afirma un nuevo build local. El [run 34418301854 de GitHub Actions](https://github.com/pr3t3l/KidsApp/actions/runs/34418301854) aprobó validación, auditorías y `docker compose build` para el commit de implementación `c63db4b`. Vercel/Supabase durables siguen pendientes.

**Estado:** artefactos y commit de implementación verificados por el CI actual; despliegue alojado pendiente.

### Sesión 16 — LLMOps, abstención, regresiones y experimentación

**Conceptos del temario suministrado:** golden set de producción, “No lo sé”, evaluación en producción, regresiones, observabilidad, costo/latencia, A/B testing y modelos locales.

**Aplicación:** 40 casos canónicos se ejecutan en ambos idiomas: 80 corridas. Las pruebas cuentan solo casos y llamadas realmente ejecutadas. Recall@5, corrección de fuentes y abstención segura son gates. Casos desconocidos, inseguros o sin evidencia no se inventan. Rutas, contenido y schemas son versionados; un candidato debe pasar golden antes de activarse de forma atómica y puede revertirse. Logfire y el ledger registran error, latencia, tokens, caché, razonamiento, fallback y costos reportados/estimados/conciliados.

Existe configuración de canary, pero no se afirma A/B sin tráfico real. No se creó adaptador local hasta que un modelo demuestre privacidad, capacidad, calidad bilingüe y costo operativo.

**Estado:** golden, regresión, abstención, costo y latencia implementados localmente; producción, A/B real y modelo local pendientes.

## Metadatos por proveedor solicitados en el programa

| Tema | OpenRouter | OpenAI directo | Anthropic directo | Destino normalizado |
|---|---|---|---|---|
| Identidad | generation/request ID, modelo solicitado/real y upstream | response/request ID y snapshot exacto | request ID HTTP, message ID y modelo exacto | `run` y `route` |
| Cierre | finish reason y router metadata | status e incomplete reason | stop reason y stop sequence | estado/causa de `run` |
| Tokens | input/output/total/caché/razonamiento | input/output/total/caché/razonamiento | input/output/total derivado/cache read-write | `usage` |
| Costos | costo reportado/upstream y conciliación | estimado por tarifa si no llega; conciliable | estimado por tarifa si no llega; conciliable | reported/estimated/reconciled + fuente |
| Routing | región, tier, BYOK, intentos, upstream | service tier y headers seguros | service tier y headers seguros | `route` + `provider_meta` acotado |
| Privacidad | metadata habilitada y upstream permitido | `store: false`; sin respuesta cruda en telemetría | sin respuesta cruda; deployment autorizado | policy + ledger redactado |

Este sidecar conserva metadata rica sin volver a inflar el contrato funcional: `ActivityCoreV2`, cada locale y los read models familiares siguen pequeños y específicos.

## Cruce con los requisitos del proyecto final

| Requisito | Evidencia | Límite honesto |
|---|---|---|
| Dominio/problema real | Aprendizaje práctico bilingüe guiado por adulto, 5–10 años | El catálogo es sintético, no aprobación comercial |
| Producto con LLM | Companion y fábrica editorial con controles deterministas | Credenciales/eval live pendientes |
| CAG y RAG | CAG de política/versión/paso y RAG híbrido publicado | Rendimiento alojado pendiente |
| Agentes | Grafo familiar acotado y grafo editorial multiagente | IA sin permiso de aprobar/publicar |
| Evaluación objetiva | 80 golden bilingües + política/API/UI/navegador | Utilidad humana y piloto pendientes |
| Arquitectura/datos | React, FastAPI, 11 migraciones, RLS, Vault, routing/costos | Entorno dedicado pendiente |
| Producción/reproducción | Docker, CI actual verde, Vercel configs, health, Logfire y runbooks | URL durable y traza de release pendientes |
| Versiones/limitaciones | Versiones y hashes de contenido/schema/ruta/tarifa/embedding, rollback | Gates humanos, legales y stores abiertos |

## Cómo reproducir

```bash
npm install
python -m pip install -r services/ai/requirements-dev.txt
npm run validate
python -m scripts.ingest_catalog --release-channel synthetic-demo --dry-run
```

Prueba real de pérdida/reload/resincronización:

```bash
npm run preview --workspace @kids/web -- --host 127.0.0.1 --port 4173
npm run test:e2e --workspace @kids/web
```

Con Docker Desktop activo:

```bash
docker compose up --build
```

## Conclusión

El proyecto aplica el programa como un sistema de ingeniería, no como una lista de librerías. CAG, RAG, metadata de proveedores, embeddings, pgvector, agentes, revisión multiagente, golden data, versionado, costos y controles de producción están implementados y pueden verificarse localmente. Los conceptos sin valor demostrado permanecen condicionados y lo que necesita infraestructura o personas reales se mantiene como evidencia externa, sin simularlo como terminado.
