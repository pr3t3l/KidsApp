> **Copia de lectura en español.** La versión normativa es [`product-build-plan.md`](product-build-plan.md), conforme a `DEC-052`.

# Plan de construcción — Kids Learning System

**Estado:** Aprobado para implementación

**Versión:** 3.0

**Owner:** Alfredo Pretel

## Resultado y límites

Se construirá un producto bilingüe dirigido al adulto para acompañar actividades de niños de 5–10 años, junto con un workspace administrativo/editorial independiente. La primera entrega operativa será una PWA privada por invitación. Empaquetado móvil, pagos y comunidad vendrán después del piloto y de sus validaciones externas.

La actividad tendrá cuatro representaciones separadas: fuente editorial mutable, versión inmutable con hash, proyecciones mínimas para la familia e índices reconstruibles de catálogo/búsqueda. La IA ayuda a interpretar solicitudes y crear/revisar borradores; identidad, permisos, seguridad, licencias, elegibilidad, presupuestos, confirmaciones y publicación siguen siendo deterministas.

El código no equivale a autorización comercial. Revisiones profesionales, pruebas físicas, derechos, revisión legal/privacidad, credenciales, cuentas de tiendas y el piloto real son puertas humanas o externas.

## Roles

| Perfil | Facultades |
|---|---|
| `platform_owner` | Alfredo controla personas, contenido, publicación/retiro, incidentes, métricas, proveedores, modelos, rutas, secretos, tarifas y presupuestos. |
| `editorial_specialist` | Revisa y firma solo disciplinas, actividades y puertas asignadas; no maneja claves, costes, usuarios ni publicación final. |
| `support_operator` | Atiende invitaciones y pilotos con datos mínimos, seudónimos, propósito y duración auditables. |
| `family_adult` | Administra familia, perfiles, plan, sesiones, feedback, exportación y borrado. |

MFA será obligatorio para administración: correo/magic link y un código TOTP establecen la sesión Supabase `aal2`. Mientras esa sesión siga válida, ninguna acción pedirá un segundo código; cada operación seguirá exigiendo su rol exacto en API y RLS. La autorización usa membresías gestionadas por servidor/BD, nunca metadata editable del usuario. Toda mutación privilegiada y toda firma conserva actor, rol, motivo, recurso, hash y fecha. Un cambio material invalida las revisiones dependientes.

## UX administrativa

El workspace bilingüe contiene: Resumen; Cobertura; Actividades; Investigación y creación con IA; Revisiones; Pilotos; Feedback familiar; Operaciones IA; Endpoints y routing; Proveedores, modelos y conexiones; Tarifas y presupuestos; Fuentes y derechos; Incidentes; Personas y permisos; Auditoría; Configuración.

El especialista recibe una bandeja acotada: asignación → evidencia y diff exactos → comentarios → checklist por rol → aprobar o devolver. Los endpoints deterministas muestran “No usa IA”. Los dashboards indican ventana, alcance y suficiencia de datos; no muestran prompts, respuestas, nombres infantiles ni notas familiares. Acciones destructivas o de release explican consecuencias y exigen motivo.

## Proveedores, modelos, telemetría y costes

El routing usa `operation_key`, entorno y versión. Incluye: clasificación/respuesta del companion; explicación de planes; reformulación y embeddings; ideación; autoría por núcleo, materiales/seguridad, pasos, roles/adaptaciones y cierre; localización; revisiones pedagógica, técnica, seguridad, consistencia y duplicidad; síntesis; feedback opcional; visuales futuros.

Para cada operación se configura conexión y modelo primarios, fallbacks ordenados, upstream permitido en OpenRouter, parámetros, contrato, tokens, timeout, coste máximo, clases de datos, idiomas, presupuesto, canary, evaluación y estado. Un trabajo editorial conserva las versiones exactas de política, deployment, modelo, prompt, esquema y tarifa con que inició. La PWA familiar nunca elige modelo.

Activar una ruta exige compatibilidad, prueba sintética, golden eval aplicable y comparación de calidad/coste/latencia. La activación es atómica y la versión anterior queda disponible para rollback.

Cada adaptador devuelve un `GenerationResult<T>` con resultado validado y un sidecar de ejecución, uso, facturación, ruta y metadata permitida (máximo 16 KB). Se prohíben prompts, respuestas, secretos, headers sensibles e identificadores familiares/infantiles en telemetría.

OpenRouter enviará `HTTP-Referer`, `X-OpenRouter-Title` y `X-OpenRouter-Metadata: enabled`; leerá uso/coste y metadata de ruta, incluso el último chunk de streaming, y podrá reconciliar `gen-*`. Los adaptadores directos de OpenAI y Anthropic preservarán respuesta tipada, request ID, caché/razonamiento y demás metadata disponible. Si no hay importe monetario en la respuesta, se calcula con la tarifa vigente; no se descartan los otros metadatos.

Se guardan por separado `reportedUsd`, `estimatedUsd`, `reconciledUsd`, `costSource` y `rateVersion`; el dashboard usa reconciliado, después reportado y después estimado. Tarifas con vigencia cubren entrada, caché, escritura de caché, salida, razonamiento, embeddings, imagen, audio y tools.

Presupuestos: global, entorno, proveedor, modelo, operación y trabajo. 80% alerta, 95% pausa generación editorial masiva, 100% bloquea IA no esencial. El companion pasa a fallback aprobado barato y luego a guía determinista. Ningún presupuesto autoriza un modelo o política de datos no aprobados.

Las claves serán write-only mediante `SecretStore` y Supabase Vault: solo estado, últimos cuatro caracteres guardados aparte y fechas; nunca se devuelve el secreto. Estados de deployment: `candidate → evaluated → approved → active → restricted/disabled`.

## Cobertura y huecos

Edades: 5–6, 7–8 y 9–10. Áreas: física, ingeniería, electricidad, matemáticas, química segura, biología/naturaleza, motricidad, creatividad, pensamiento lógico, comunicación, autorregulación y vida práctica.

Dimensiones: área principal/secundaria real, L1–L4, participantes, duración, riesgo A/B/C, materiales, mecanismo, espacio, desorden, accesibilidad, idioma, estado, demanda y calidad. Una secundaria solo cuenta si está vinculada a habilidades y pasos u observaciones reales.

```text
aporte de área: principal 1; secundaria validada 0.5
aporte de estado: publicada 1; piloto autorizado 0.5; borrador 0
diversidad: primer mecanismo/material 1; repetición equivalente 0.25
cobertura efectiva = suma(área × estado × diversidad)
```

Huecos: absoluto, cobertura, diversidad, demanda, calidad, localización, editorial y seguridad. Prioridad: 50% déficit + 30% demanda + 20% calidad; seguridad crítica domina. Demanda: tres búsquedas sin resultado en piloto o ≥10% de al menos 20 solicitudes en 28 días. Calidad solo se calcula tras cinco sesiones; metas: cierre útil ≥70%, companion útil ≥80% y duración correcta ≥70%. Antes se muestra “datos insuficientes”.

Piloto: 12–15 actividades bilingües; cada área con una principal o dos secundarias significativas; cada edad con cinco opciones en cuatro áreas y dos A, de bajo desorden y materiales comunes; mínimo cuatro actividades para 1, 2 y 3/4 participantes; al menos 3 de ≤20 min, 6 de 21–40 y 2 de 41–60. C exige especialista independiente; D queda fuera. Objetivos versionados y editables.

“Cubrir hueco” muestra combinación, real/objetivo, candidatos cercanos y motivo de exclusión, demanda, repetición y riesgo máximo; crea un brief editable, nunca generación/publicación silenciosa.

## Contratos compactos V2

- `ActivityCoreV2`: identidad, adecuación, aprendizaje, materiales, flujo causal, seguridad, adaptaciones y referencias de cierre, sin texto duplicado por idioma.
- `ActivityLocaleV2`: un idioma exacto con títulos, explicaciones, guiones, materiales, pasos, advertencias, soluciones y alt text.
- Entidades aparte: fuentes, derechos, asignaciones, comentarios, revisiones, gates, pilotos, incidentes, QA visual, publicación e historial.
- Read models mínimos: `ActivityCard`, `ActivityPrep`, `SessionStep`, `SessionCloseout`, `JourneySummary` y `CompanionContext` interno.

JSON externo usa `camelCase` inglés y BD usa `snake_case`. Se aprovecha el anidamiento (`fit.time.min`) y solo se admiten abreviaturas claras (`id`, `min`, `max`, `ms`, `usd`, `url`). Lo no aplicable se omite.

La UI recibe bloques `{kind, version, data}` con registro de renderers. Un nuevo ejercicio añade esquema/renderer, no rehace la BD. Un bloque obligatorio desconocido bloquea el inicio; uno opcional se omite con telemetría.

Reglas condicionales: cada acción infantil tiene propósito y señal observable; cada riesgo tiene control, parada y pasos; grupos tienen configuraciones coherentes; una adaptación que cambie seguridad no es automática; visual obligatorio referencia asset.

Generación en etapas: idea (~600 tokens), núcleo (~1.500), materiales/seguridad, grupos pequeños de pasos, roles/adaptaciones cuando apliquen, cierre, un idioma/sección por vez, validación determinista y compilación/hash del servidor. Nunca se genera el snapshot bilingüe/editorial entero en una llamada.

Límites ejecutables: esquema al modelo ≤2.000 tokens estimados; solicitud editorial ≤8.000; respuesta de etapa ≤2.000; contexto companion <2.000; respuesta companion ≤350; card <2 KB; preparación <12 KB; paso <8 KB. Migración V1→V2 determinista y no destructiva; sesiones históricas conservan snapshot/hash; V1 se retira solo tras evidencia de equivalencia semántica.

## Fábrica editorial con IA

Owner elige/edita hueco → búsqueda en dominios permitidos → resultados transitorios → verificación de página/licencia → ideas → selección humana → autoría V2 por etapas → validadores → críticos especialistas → síntesis sin aprobación → localización → compilación → revisión humana → piloto → release humano.

Pasan automáticamente solo CC0, dominio público y CC BY verificable. CC BY-SA/licencias especiales requieren revisión manual/legal. NC, ND, desconocidas o contradictorias quedan bloqueadas. Encontrar una URL no concede derechos.

La IA no puede firmar, publicar, bajar seguridad, quitar advertencias, inventar sustituciones aprobadas, decir que se probó, aprobar derechos ni simular un profesional.

Estados: `idea → draft → review → ready_for_pilot → family_pilot → revision → published → retired`. Canales: `founder_internal`, `family_pilot`, `production`. Alfredo puede aprobar A/B internamente para piloto, siempre marcado como no independiente; publicación comercial exige gates configurados. Retirar elimina de nuevas recomendaciones inmediatamente y conserva sesiones históricas.

## PWA familiar

Navegación: Hoy, Plan, Explorar, Trayectoria y Familia. Onboarding: invitación/magic link → consentimiento adulto → idioma/unidades/zona → alias y banda de edad → participantes/tiempo/espacio/desorden/materiales → primera actividad elegible. No se pide nombre completo, email infantil, escuela, fecha completa, foto ni cuenta infantil.

Actividad: preparación, propósito, seguridad, foco/contribución por participante, puerta adulta, pasos causales, pausa/reanudación, un botón flotante del companion, adaptación confirmada, cierre rápido y trayectoria. Antes de iniciar, una adaptación confirmada cambia la actividad visible; durante sesión solo cambia pasos pendientes; reemplazar cierra la actual como interrumpida.

La puerta adulta usa tres asociaciones localizadas entre número escrito y valor; dura la sesión o 15 minutos inactivo y tres fallos llevan a reautenticación real. Es fricción infantil, no prueba legal de edad. Privacidad, borrado, invitaciones, enlaces y pagos siempre exigen autenticación real. Se declara supervisión adulta obligatoria.

Feedback desde cualquier recorrido: útil sí/no + comentario opcional; adjunta pantalla, versión, actividad, navegador, idioma y estado. Sin screenshot, voz ni ambiente. Advierte contra PII; texto cifrado/redactado y borrado a 90 días; agregados pueden permanecer. Seguridad crea incidente y puede retirar contenido.

## Datos, API, CAG/RAG y agentes

Dominios de datos: familia/perfiles/planes/sesiones/trayectoria/privacidad; núcleo/idioma/bloques/materiales/fuentes/derechos/revisiones/pilotos/visuales/incidentes; cobertura; operaciones/conexiones/deployments/routing/uso/tarifas/reconciliación/presupuestos/salud/evals; auditoría append-only.

APIs administrativas cubren operación IA, rutas, test/activar/rollback, uso/costes/tarifas/presupuestos/conexiones/deployments/evals, cobertura/huecos y flujo editorial. APIs familiares cubren perfiles, preferencias, hoy/plan/catálogo, sesión, companion, decisiones, trayectoria, feedback, exportación y borrado.

Toda tabla expuesta tiene RLS, grants y políticas explícitas. Tablas sensibles son server-only o quedan fuera del API expuesto. El navegador solo usa clave publicable; secretos se quedan en backend. Mutaciones reintentables son idempotentes.

CAG contiene política, contrato, versión exacta, idioma, bloque actual y evidencia necesaria. RAG solo indexa contenido publicado por idioma; autorización, versión y seguridad filtran antes del ranking. Full-text y pgvector devuelven hasta ocho cada uno y RRF hasta cinco. Los reemplazos pasan filtros deterministas. Evidencia insuficiente produce abstención o `safe_stop`.

El companion sigue siendo un grafo acotado sin SQL, navegador, archivos ni publicación general. Los agentes editoriales trabajan bajo supervisor, costes/reintentos y human-in-the-loop; sus hallazgos nunca equivalen a firmas.

## Orden y aceptación

1. Plan, evaluación, decisiones, estado y trazabilidad.
2. Contratos V2, ejemplos, migrador y límites.
3. RBAC, esquema operacional/editorial, grants, RLS y auditoría.
4. Registro de operaciones, routing versionado y secretos.
5. Gateway neutral, tres adaptadores y telemetría.
6. Costes, tarifas, reconciliación, presupuestos y métricas.
7. Cobertura, derechos y fábrica por etapas.
8. Workspace owner/especialista/soporte.
9. PWA familiar completa y offline.
10. CAG/RAG y agentes editoriales.
11. Golden set, E2E, seguridad, build, contenedores y docs.
12. Crear y probar físicamente 12–15 actividades.
13. Desplegar y ejecutar piloto de 14 días con 12 adultos.
14. Corregir, completar puertas comerciales, web/políticas/suscripción y luego Capacitor Android e iOS.

Aceptación: 100% de gates duros de autorización/aislamiento/seguridad/esquema/confirmación; ≥80 ejecuciones bilingües; recall@5 ≥90%; abstención ≥95%; cero recuperación de borrador/retirado/versión/idioma incorrectos; metadata/coste correctos sin PII ni conversación cruda; 12–15 actividades con derechos y gates; C independiente y D ausente; cierre útil ≥70%, companion útil ≥80%, duración ≥70%; cero críticos; PWA accesible y guía útil sin IA.

La entrega académica sigue en `finalproject-AP`, con README reproducible, arquitectura, CAG/RAG/agentes/evals/despliegue, limitaciones honestas, URL o video y tag recomendado `v1.0-final-AP`.
