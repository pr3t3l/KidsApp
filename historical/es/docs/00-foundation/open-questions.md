> **Histórico — documento en español.** Archivado el 18 de agosto de 2026. La especificación vigente está en [English canonical document](../../../../docs/00-foundation/open-questions.md); no agregar requisitos, decisiones ni cambios nuevos a este registro.

# Preguntas y decisiones de definición

**Estado:** Review  
**Versión:** 0.4

## Decisiones confirmadas por la fundadora

| Tema | Decisión |
|---|---|
| Mercado | Estados Unidos. |
| Idiomas | Inglés y español desde el lanzamiento. |
| Plataforma | Aplicación móvil iOS/Android y dos experiencias web previstas: aplicación familiar y portal administrativo/editorial. El orden de construcción web se decide en el roadmap. |
| Interfaz inicial | Dirigida al adulto. El niño participa fuera de pantalla; puede recibir preguntas e imágenes presentadas por el adulto. |
| Cuenta | Un adulto paga; varios adultos autorizados pueden usar la familia. |
| Perfiles | La familia puede crear los perfiles infantiles que necesite. |
| Sesiones | Límite operativo inicial aprobado: 1–4 niños. |
| Edad inicial | 5–10 años. |
| Planificación | Basada en minutos disponibles por día; una o varias actividades pueden llenar el bloque. |
| Semana | Hasta cinco días propuestos por defecto, configurable. |
| Duración | Configurable, con opciones iniciales de 30 y 60 minutos. |
| Contenido | Balanceado entre STEM, matemáticas, motricidad, creatividad, naturaleza y vida práctica, con énfasis transversal en invención. |
| Materiales | Objetos cotidianos y reutilizables; evitar kits que conviertan la solución en ensamblaje predeterminado. |
| Imágenes | Fotorealismo para materiales/resultados, diagramas para pasos/conceptos e ilustración infantil como recurso terciario. |
| IA | Arquitectura agnóstica de proveedor mediante router y registro de capacidades. |
| Explicaciones | Versión breve y versión detallada para el adulto. |
| Inferencias | Pueden actualizarse sin confirmación individual; deben ser visibles y corregibles. Atribuciones ambiguas desde voz requieren confirmación. |
| Voz | Audio temporal; transcripción editable; conservar el dato estructurado útil, no el audio indefinidamente. |
| Negocio | Suscripción mensual o anual. Piloto actual sin costo. |
| Compra móvil | App Store y Google Play. |
| Compra web futura | Stripe Billing + Checkout y Customer Portal. |
| Prueba comercial | Siete días gratuitos para una familia elegible, antes de conversión automática claramente informada. |
| Cancelación | Autoservicio, desde la aplicación, mediante la tienda de origen o Stripe; detiene renovación y conserva acceso hasta terminar el período vigente. |
| Comunidad | Visible únicamente para adultos autenticados dentro de la aplicación. |
| Fotografías comunitarias | El adulto decide si publica solo el proyecto/manos o si incluye a un niño reconocible. La opción segura por defecto favorece proyecto/manos; una imagen reconocible requiere confirmación explícita, revisión de privacidad y moderación. La elección parental no elimina las responsabilidades de la plataforma. |
| Marketing social | Un tag externo puede iniciar una solicitud de permiso; no autoriza reutilización automática. |
| Edición | Comienza con la fundadora y evoluciona a equipo especializado colaborativo. |
| Importación masiva | No se prioriza importación/exportación de actividades por spreadsheet. |
| Piloto | Ocho semanas con la hija de la fundadora como caso de un solo niño y familias amigas con dos o tres niños cada una. |
| Actividades de calibración | La fundadora acepta conceptualmente puente de papel, clasificación con semillas y probador de conductividad. Siguen siendo borradores sujetos a gates. |
| Estrategia estatal | No crear variantes educativas por estado. Diseñar con un baseline nacional protector, registrar los estados donde ocurran pilotos y completar una matriz legal de aplicabilidad antes del lanzamiento. |

## Recomendaciones adoptadas provisionalmente

1. **Offline:** recomendación, IA, comunidad, sincronización y pagos requieren conexión; el paquete semanal descargado funciona offline.
2. **Comunidad:** portafolio privado y comunidad son permisos separados; moderación previa y sin comentarios ni mensajes directos inicialmente.
3. **Medios de voz:** borrar audio tras transcripción o máximo operativo; conservar transcripción editable hasta 30 días y luego solo observaciones estructuradas.
4. **Llama, vidrio o presión:** categoría adulta especial posterior al piloto básico, con revisión experta y controles específicos.
5. **Publicación A/B:** ejecución del autor y al menos tres ejecuciones adicionales en dos familias; C/D requiere gate reforzado.
6. **Prueba gratuita:** una sola prueba de siete días por familia elegible, con recordatorio antes de finalizar y sin mecanismos de cancelación obstructivos.

## Preguntas todavía abiertas

1. ¿Cuál será el precio mensual y anual después de validar el piloto?
2. ¿Qué experiencia web se construye primero: la familiar o el portal administrativo/editorial?
3. ¿Se solicitará inclusión en Apple Kids Category o se distribuirá como aplicación para adultos que acompañan niños? Esta decisión sí cambia metadata, parental gates, SDKs, analítica y revisión de tienda; requiere revisión legal y de App Store.
4. ¿Qué configuración eléctrica exacta permite que los niños participen materialmente en el montaje desenergizado sin acceder a pilas, uniones fijas peligrosas o componentes no aprobados?
5. ¿Qué mecanismo de consentimiento, revisión de privacidad y retirada se usará cuando un adulto elija publicar una imagen con un niño reconocible?
