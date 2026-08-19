> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/00-foundation/compliance-baseline.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Baseline de privacidad infantil y distribución en Estados Unidos

**Estado:** Draft — no sustituye asesoría legal  
**Versión:** 0.1  
**Revisión:** 16 de agosto de 2026

## Contexto

El producto se dirige a familias con niños de 5–10 años en Estados Unidos. Aunque el adulto controle la cuenta, la aplicación recopila información relacionada con menores y ofrece contenido dirigido a ellos. Debe diseñarse bajo COPPA y políticas de distribución infantil desde el inicio.

## COPPA

La [FTC identifica COPPA como el marco que da a los padres control sobre la información recopilada de menores de 13 años](https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy). La regla fue modificada en abril de 2025 y exige revisar la versión vigente.

Baseline de producto:

- Cuenta y consentimiento administrados por adulto.
- Aviso claro de qué se recopila, propósito, proveedores y retención.
- Consentimiento parental verificable cuando corresponda.
- Minimización y retención limitada por propósito.
- Acceso, corrección, exportación y eliminación.
- Revisión de cada SDK/proveedor; tercerizar procesamiento no elimina responsabilidad.
- Fotos, videos y voz infantiles se tratan como datos de alta sensibilidad.
- Prohibido reutilizar datos infantiles para publicidad dirigida o entrenamiento sin una base y consentimiento específicamente aprobados.

## Apple App Store

Las [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) exigen moderación para contenido generado por usuarios, incluyendo filtrado, reporte, bloqueo cuando aplique y contacto público. Las apps de Kids Category tienen restricciones adicionales sobre enlaces, compras, datos y SDKs de terceros.

Decisiones pendientes de distribución:

- Confirmar si se solicitará Kids Category.
- Diseñar parental gate para compras, enlaces y comunidad.
- Revisar todos los SDKs de analítica e IA antes de integrar.

## Google Play

Las [Families Policy Requirements](https://support.google.com/googleplay/android-developer/answer/9893335) requieren declarar audiencia, datos sensibles, cámara/micrófono y SDKs; también establecen controles para funciones sociales. La [política de UGC](https://support.google.com/googleplay/android-developer/answer/9876937) exige términos, moderación, reportes y bloqueo según la experiencia.

Baseline de producto:

- No depender de identificadores publicitarios.
- No solicitar ubicación precisa.
- Auditar SDKs para uso en servicios dirigidos a niños.
- Publicación comunitaria únicamente mediante acción adulta.
- Moderación continua, reporte y retiro.

## Estados de Estados Unidos

El contenido educativo no se fragmentará por estado, pero la ubicación de familias piloto y usuarias sí puede cambiar qué obligaciones de privacidad, consentimiento, evaluación de impacto o derechos del consumidor resultan aplicables. El volumen y alcance de legislación estatal de privacidad y protección infantil continúa cambiando; antes de ampliar el piloto se registran los estados participantes y antes del lanzamiento se completa una matriz legal vigente. El producto adopta mientras tanto un baseline nacional protector y no usa la ausencia de una regla estatal específica para reducir controles.

Referencia de seguimiento: [NCSL — Consumer Privacy 2025 Legislation](https://www.ncsl.org/technology-and-communication/consumer-privacy-2025-legislation) y las fuentes oficiales de cada estado identificado.

## Consecuencia para la comunidad

Una galería de proyectos no es “solo almacenamiento de fotos”: es UGC. Antes de habilitarla se requieren términos, normas comunitarias, moderación previa o equivalente, reporte, retirada, gestión de derechos y controles parentales. Marketing no puede reutilizar publicaciones automáticamente; necesita un consentimiento/licencia separados y explícitos.

El adulto puede decidir si una publicación incluye únicamente el proyecto/manos o muestra a un niño reconocible, pero esa elección no transfiere al adulto las obligaciones de la plataforma. El producto debe favorecer proyecto/manos por defecto, advertir sobre uniforme escolar, nombre, ubicación y metadata, pedir confirmación explícita antes de enviar una imagen reconocible, moderarla y permitir retirada. La implementación exacta requiere revisión legal vigente antes de habilitar comunidad.

## Gate antes de lanzamiento

- Asesoría legal de privacidad infantil en Estados Unidos.
- Revisión de requisitos estatales aplicables.
- Data map completo de aplicación y proveedores.
- Flujo probado de consentimiento, acceso y eliminación.
- Evaluación de App Store Kids Category y Google Play Families.
- Políticas públicas de privacidad, comunidad y retención.
