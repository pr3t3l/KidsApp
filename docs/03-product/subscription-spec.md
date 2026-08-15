# SPEC-12 — Subscription, Trial and Cancellation

**Estado:** Draft  
**Versión:** 0.1

## 1. Producto comercial

- Plan mensual.
- Plan anual.
- Mismo acceso familiar salvo decisión futura de tiers.
- Una suscripción cubre a los adultos autorizados y perfiles infantiles de la familia.
- El entitlement pertenece a la familia, aunque la compra tenga un pagador y canal de origen.

## 2. Canales

| Canal | Compra y gestión |
|---|---|
| iOS/iPadOS | App Store In-App Purchase y administración de suscripciones de Apple. |
| Android | Google Play Billing y Subscription Center. |
| Web futuro | Stripe Billing + Checkout Sessions; Customer Portal para autoservicio. |

El backend normaliza recibos y webhooks en un `SubscriptionEntitlement`. No intenta cobrar directamente una compra administrada por otra tienda.

## 3. Piloto

Durante el piloto no existe cobro ni trial comercial. Las familias reciben un `pilot entitlement` con fecha, alcance y revocación administrativa. Esto evita mezclar evaluación del producto con conversión de pago.

## 4. Prueba gratuita

- Duración: 7 días.
- Elegibilidad: una vez por familia/cuenta elegible, aplicando reglas de cada tienda.
- Beneficios: acceso completo a funciones del plan que se está probando.
- Conversión: automática al plan elegido si no se cancela, cuando el canal lo permita.
- Antes de confirmar se muestran duración, precio posterior, fecha de primer cobro, frecuencia, renovación automática y método de cancelación en inglés y español.
- Enviar recordatorio propio aproximadamente 3 días antes del final cuando el canal y consentimiento lo permitan; no depender únicamente de notificaciones de la tienda.
- Cancelar durante la prueba evita el cobro siguiente y mantiene acceso hasta el final de la prueba, sujeto al comportamiento del canal.

## 5. Política de cancelación recomendada

1. Acción visible `Administrar suscripción` en Cuenta.
2. Enlace directo a Apple, Google Play o Stripe según `billing_source`.
3. Sin llamada, correo o conversación obligatoria.
4. Mostrar fecha exacta en que termina el acceso antes de confirmar.
5. La cancelación desactiva la renovación automática.
6. El acceso continúa hasta terminar el período pagado o trial vigente, salvo cancelación inmediata exigida por ley/canal.
7. No hay reembolso prorrateado por defecto; Apple/Google administran sus reembolsos y la web sigue política publicada y ley aplicable.
8. Pregunta de motivo opcional después de confirmar; nunca bloquea.
9. El usuario puede reactivar antes de terminar el período cuando el canal lo soporte.
10. Cancelar no elimina familia, Learner Models, portafolio ni historial. La eliminación es un flujo separado.

## 6. Transparencia

El paywall muestra con igual claridad:

- “7 días gratis”.
- Precio total real de mensual o anual.
- Fecha de conversión.
- Renovación automática.
- Forma de cancelar.
- Qué ocurre con acceso y datos.
- Enlace a términos y privacidad.

No usar temporizadores falsos, botones de cierre ocultos, precios anuales presentados solo como mensualidad ni varios pasos confusos hacia compra accidental.

## 7. Fallos de pago y gracia

- Conservar acceso durante el grace period informado por la tienda/backend.
- No detener una sesión en progreso.
- Mostrar estado y acción para resolver pago únicamente al adulto pagador/Owner.
- Revocar entitlement después de expiración confirmada, manteniendo datos según política.

## 8. Restauración y familia multicanal

- Permitir `Restaurar compras`.
- Vincular la compra al Family correcto mediante cuenta adulta autenticada.
- Evitar dos suscripciones activas involuntarias; advertir si la familia ya tiene entitlement por otro canal.
- Los demás adultos autorizados consumen el mismo entitlement sin acceder a datos de pago del Owner.
- Cambio de pagador o canal requiere flujo explícito para evitar doble cobro.

## 9. Implementación web con Stripe

Cuando exista compra web:

- Usar Stripe Billing con Checkout Sessions en modo suscripción.
- Usar Customer Portal para cancelación, método de pago e invoices.
- Procesar webhooks de forma idempotente.
- Mantener claves restringidas y secretos fuera de clientes/repositorio.
- Evaluar impuestos y registros antes de activar cálculo automático.

## 10. Requisitos

- **SUB-001:** La familia tiene un entitlement normalizado independiente del canal de pago.
- **SUB-002:** La prueba comercial dura siete días y se ofrece una vez según elegibilidad.
- **SUB-003:** Términos, precio, conversión y cancelación se muestran antes de iniciar.
- **SUB-004:** La aplicación ofrece acceso directo a cancelación del canal de origen.
- **SUB-005:** Cancelar detiene renovación y conserva acceso hasta fin de período salvo excepción aplicable.
- **SUB-006:** Cancelación y eliminación de datos son flujos separados.
- **SUB-007:** La pregunta de motivo es posterior y opcional.
- **SUB-008:** La familia no debe mantener dos suscripciones activas por accidente.
- **SUB-009:** El piloto usa entitlement gratuito separado del trial comercial.
- **SUB-010:** El paywall y gestión están localizados en inglés y español.

## 11. Referencias operativas

- [Apple — introductory offers for auto-renewable subscriptions](https://developer.apple.com/help/app-store-connect/manage-subscriptions/set-up-introductory-offers-for-auto-renewable-subscriptions)
- [Google Play — subscription transparency, trials and cancellation](https://support.google.com/googleplay/android-developer/answer/9900533)
- [Stripe — Customer Portal](https://docs.stripe.com/customer-management)
- [Stripe — subscription trials](https://docs.stripe.com/billing/subscriptions/trials)
- [FTC — Negative Option Rule resources](https://www.ftc.gov/legal-library/browse/rules/negative-option-rule)

Estas fuentes son cambiantes; deben revisarse antes del lanzamiento. La especificación expresa una política de producto y no reemplaza revisión legal.
