> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/02-content/visual-content-pipeline.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Pipeline de imágenes instructivas

**Estado:** Draft  
**Versión:** 0.1

## Propósito

Producir imágenes bilingües, coherentes y versionadas para actividades aunque las primeras no sean fotografiadas en un estudio. La IA puede generar borradores; ninguna imagen entra en una actividad publicada sin QA y aprobación humana.

## Tipos de recurso

1. **Materials board:** objetos requeridos, cantidades y etiquetas.
2. **Preparation:** montaje previo y pasos exclusivos del adulto.
3. **Step diagram:** una acción y resultado esperado.
4. **Expected result:** apariencia correcta y variaciones normales.
5. **Concept diagram:** explicación científica, marcada como diagrama cuando no está a escala.
6. **Troubleshooting:** comparación entre estado correcto y error frecuente.

## Jerarquía visual aprobada

1. **Fotorealismo:** materiales, montaje y resultado esperado cuando la fidelidad física ayuda a ejecutar.
2. **Diagrama instructivo:** pasos, conexiones, fuerzas, secuencias y conceptos que necesitan simplificación visual.
3. **Ilustración infantil:** narrativa, ambientación o motivación; no sustituye una referencia física importante.

Una actividad puede combinar los tres estilos con reglas consistentes. La seguridad y claridad determinan el estilo, no una preferencia estética aislada.

## Pipeline

```text
ActivityVersion estructurada
→ shot list por paso
→ prompt/brief generado
→ generación de candidatos
→ QA automático multimodal
→ revisión editorial humana
→ ajustes o regeneración
→ aprobación
→ publicación ligada a la versión
```

## QA automático

El verificador compara cada candidato contra datos estructurados:

- Materiales correctos y sin objetos extra peligrosos.
- Cantidades y componentes esenciales visibles.
- Orientación física coherente con el paso.
- Actor correcto: no mostrar al niño realizando adult-only steps.
- Resultado posible, sin piezas flotantes o conexiones falsas.
- Ausencia de texto deformado; las etiquetas se superponen programáticamente.
- Consistencia visual entre pasos.
- Ausencia de marcas, rostros reales o información identificable no autorizada.

El QA automático produce hallazgos; no aprueba por sí solo.

## Revisión humana

Requiere confirmar:

- Fidelidad a la versión y seguridad.
- Claridad para un adulto que no leyó la actividad.
- Coherencia entre inglés y español.
- Accesibilidad, alt text y contraste.
- Derechos y trazabilidad del proveedor/modelo.

## Versionado

Cada asset conserva:

- ActivityVersion y step_id.
- Tipo de recurso.
- Prompt/brief y modelo/proveedor.
- Candidatos y resultado de QA según retención editorial.
- Aprobador y fecha.
- Idioma y alt text.
- Estado: draft, review, approved, retired.

Un cambio material de pasos invalida los assets afectados.

## Producción futura

Las fotos reales de pilotos pueden servir para comprender fallas, pero no se convierten automáticamente en material editorial o marketing. Su uso requiere consentimiento/licencia separados, revisión de privacidad y ausencia de información infantil no necesaria.

## Requisitos

- **ACT-VIS-001:** Toda imagen publicada referencia una ActivityVersion y propósito.
- **ACT-VIS-002:** La imagen pasa QA automático y aprobación humana.
- **ACT-VIS-003:** El texto visible se renderiza como capa controlada, no generado dentro de la imagen.
- **ACT-VIS-004:** Los adult-only steps no muestran manipulación infantil.
- **ACT-VIS-005:** Marketing no reutiliza medios familiares sin consentimiento específico separado.
