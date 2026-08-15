# Abstracción y gobernanza de proveedores de IA

**Estado:** Draft  
**Versión:** 0.1

## Objetivo

Permitir usar OpenAI, Anthropic, Google, modelos open source u otros proveedores sin acoplar producto, datos y evaluaciones a un modelo específico.

## Gateway

La aplicación llama a capacidades internas, no a nombres de modelos:

- `generate_text`
- `structured_reasoning`
- `transcribe_audio`
- `analyze_image`
- `generate_image`
- `moderate_content`
- `embed_content`

El gateway resuelve proveedor/modelo según política, disponibilidad, costo, idioma, latencia y sensibilidad.

## Registry de proveedores

Cada deployment registra:

- Proveedor, modelo y versión.
- Capacidades y límites.
- Regiones de procesamiento.
- Política de retención y entrenamiento.
- Elegibilidad para datos infantiles.
- Tipos de medio permitidos.
- Contrato/DPA y fecha de revisión.
- Evaluaciones aprobadas.
- Costo y latencia.
- Estado: candidate, approved, restricted, disabled.

## Routing

1. Clasificar caso de uso y datos.
2. Aplicar filtros de privacidad/seguridad.
3. Elegir entre deployments aprobados.
4. Ejecutar con contrato estructurado.
5. Validar salida.
6. Registrar versión, latencia y resultado sin conservar contenido innecesario.
7. Ejecutar fallback solo a otro deployment igualmente elegible.

## Portabilidad

- Prompts y schemas versionados en repositorio.
- Adapters por proveedor.
- Salidas normalizadas.
- Golden evals comunes.
- Features degradan de forma explícita si un proveedor no soporta capacidad.
- No asumir que todos los proveedores admiten fotos, voz o datos infantiles bajo iguales términos.

## Datos

- Redactar contexto no necesario antes de enviar.
- Preferir alias/IDs efímeros.
- No enviar audio o fotos a un proveedor no aprobado para ese medio.
- No usar datos de producción para entrenar modelos por defecto.
- Documentar transferencias y subprocessors.

## Requisitos

- **AI-GW-001:** Código de producto solicita capacidades, no modelos concretos.
- **AI-GW-002:** Todo deployment tiene política de elegibilidad de datos.
- **AI-GW-003:** Fallback respeta las mismas restricciones del request original.
- **AI-GW-004:** Cada salida auditable registra deployment y versiones de prompt/schema.
- **AI-GW-005:** Cambiar modelo requiere ejecutar evals aplicables.
- **AI-GW-006:** Deshabilitar un proveedor no requiere cambios en flujos de producto.
