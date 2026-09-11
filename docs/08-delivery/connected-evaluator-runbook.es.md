# Puesta en marcha del evaluador conectado desde el móvil

**Destino web:** `https://kids.alfredopretelvargas.com`

**Rama:** `finalproject-AP`

**Modo:** evaluación técnica privada con Auth, RLS, sesiones, feedback, auditoría y catálogo sintético A/B. Este modo no afirma que las actividades hayan recibido aprobación profesional o comercial.

## Regla de secretos

Los secretos se escriben únicamente en GitHub, Supabase, Vercel o en el panel owner desplegado. No se envían por chat, correo, capturas ni WhatsApp. En el móvil conviene usar el navegador en modo escritorio y un gestor de contraseñas.

## Arquitectura del despliegue

- Vercel web: proyecto `kids-learning-system`, raíz `apps/web`, rama de producción `finalproject-AP`.
- Vercel API: proyecto `kids-learning-api`, raíz `services/ai`, rama de producción `finalproject-AP`.
- Supabase: proyecto existente `declassified-shop` (`dlonzlnigwyzzetssdbx`) con PostgreSQL 17, Auth, pgvector, RLS y Vault compartidos. Todo objeto de Kids usa `kids_`; los secretos usan `kids/`.
- Cloudflare: solo el DNS de `kids.alfredopretelvargas.com`; se copia exactamente el destino que entregue Vercel.
- GitHub Environment `connected-evaluator`: aplica las migraciones, crea/invita al owner y compila el catálogo sintético.

## 1. Proyecto Supabase compartido para el piloto

Desde `supabase.com/dashboard`:

1. No crees otro proyecto para esta evaluación. Usa `declassified-shop`, ya migrado y disponible en `https://dlonzlnigwyzzetssdbx.supabase.co`.
2. No renombres ni modifiques tablas sin prefijo: pertenecen a Declassified. Las 65 tablas de este producto empiezan por `kids_`; también lo hacen tipos, funciones, índices, políticas y triggers.
3. En **Project Settings → API Keys / Connect**, copia de forma privada:
   - Project URL.
   - Publishable key.
   - Secret key; si el proyecto aún usa claves legacy, usa `service_role` solamente en backend.
   - Project reference ID.
4. Conserva la contraseña de base de datos y el Personal Access Token solo si ejecutarás futuras migraciones desde GitHub Actions.

Esta reutilización evita otro costo durante el piloto, pero no equivale a aislamiento de producción: Auth, cuotas, configuración, fallos y la autoridad de `service_role` son compartidos. El prefijo evita colisiones accidentales, no limita una clave backend comprometida. Antes del lanzamiento comercial se migrará Kids a un proyecto dedicado.

El publishable key puede ir en la web; la secret/service-role key, el access token y la contraseña de base de datos nunca pueden ir en variables `VITE_*`.

El backend acepta tanto las claves opacas nuevas `sb_publishable_*`/`sb_secret_*` como las JWT legacy. Las claves `sb_secret_*` se envían solo como `apikey`, nunca se hacen pasar por un JWT en `Authorization`. Referencia: [migración a las nuevas API keys](https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys).

## 2. Configurar Auth antes de enviar invitaciones

En **Authentication → URL Configuration**, sin reemplazar el Site URL que usa Declassified:

- Conserva el Site URL actual del proyecto compartido.
- Añade a Redirect URLs:
  - `https://kids.alfredopretelvargas.com/**`
  - la URL preview exacta de Vercel mientras se valida el dominio

Mantén desactivado el registro público. El sistema usa invitaciones y el login posterior tiene `shouldCreateUser: false`.

SMTP y las plantillas de Auth también son globales para el proyecto. Si se configuran en **Authentication → Email / SMTP**, prueba tanto Kids como Declassified antes de guardar el cambio. El envío incorporado de Supabase es limitado y no es apropiado para un piloto externo. Configura SPF, DKIM y DMARC; no publiques una invitación familiar hasta probar recepción y expiración del enlace.

Referencias: [usuarios e invitaciones](https://supabase.com/docs/guides/auth/users), [redirect URLs](https://supabase.com/docs/guides/auth/redirect-urls) y [SMTP](https://supabase.com/docs/guides/auth/auth-smtp).

## 3. Cargar secretos de aprovisionamiento en GitHub desde el móvil

Abre `github.com/pr3t3l/KidsApp/settings/environments`, crea el environment `connected-evaluator` y añade estos **Environment secrets**:

| Nombre | Procedencia |
|---|---|
| `SUPABASE_ACCESS_TOKEN` | Token personal de Supabase |
| `SUPABASE_DB_PASSWORD` | Contraseña del proyecto Supabase |
| `SUPABASE_PROJECT_ID` | Reference ID del proyecto |
| `SUPABASE_URL` | Project URL |
| `SUPABASE_SECRET_KEY` | Secret key o legacy service-role, solo backend |
| `OWNER_EMAIL` | Correo adulto de Alfredo |
| `OPENROUTER_API_KEY` | Opcional; si falta, el catálogo usa full-text y el acompañante falla de forma segura |

Las migraciones iniciales ya fueron aplicadas de forma transaccional el 10 de septiembre de 2026. Los once archivos `shop_*` del repositorio son marcadores vacíos que alinean el ledger remoto compartido; nunca recrean ni alteran Declassified. Para una migración futura, abre **Actions → Provision connected evaluator → Run workflow**, selecciona `finalproject-AP` y ejecútalo. El job:

1. valida que estén los valores obligatorios;
2. enlaza el proyecto;
3. ejecuta `supabase db push --dry-run`;
4. solo si ese paso pasa, aplica las migraciones;
5. reutiliza o invita la identidad owner y asigna `platform_owner`;
6. carga 13 actividades bilingües sintéticas, pero solo A/B quedan disponibles para evaluación;
7. crea 28 chunks RAG; si no hay clave de embeddings, quedan en full-text sin impedir el despliegue.

La acción no imprime correos completos ni valores secretos. Referencia: [migraciones Supabase](https://supabase.com/docs/guides/deployment/database-migrations).

## 4. Variables del proyecto API en Vercel

En el proyecto con raíz `services/ai`, configura Production y Preview de forma separada:

```text
APP_ENV=production
DEMO_MODE=false
EVALUATION_CATALOG=true
ALLOWED_ORIGINS=https://kids.alfredopretelvargas.com
PUBLIC_SITE_URL=https://kids.alfredopretelvargas.com
OPENROUTER_SITE_URL=https://kids.alfredopretelvargas.com
OPENROUTER_APP_NAME=Kids Learning System
SUPABASE_URL=<Project URL>
SUPABASE_PUBLISHABLE_KEY=<Publishable key>
SUPABASE_SECRET_KEY=<Secret key; backend only>
SUPABASE_OBJECT_PREFIX=kids_
TELEMETRY_HASH_SALT=<valor aleatorio independiente de 48+ caracteres>
ADULT_GATE_SIGNING_SECRET=<otro valor aleatorio independiente de 48+ caracteres>
MONTHLY_INFERENCE_BUDGET_USD=15
LEGAL_MATRIX_VERSION=pilot-us-v1
```

`LOGFIRE_TOKEN` es opcional para arrancar, pero necesario para la evidencia de observabilidad final. Las claves OpenRouter/OpenAI/Anthropic no necesitan quedar como variables permanentes de Vercel: después del primer acceso owner se introducen desde el panel administrativo y quedan write-only en Supabase Vault.

## 5. Variables del proyecto web en Vercel

En el proyecto con raíz `apps/web`:

```text
VITE_API_URL=https://<url-del-proyecto-api>.vercel.app
VITE_DEMO_MODE=false
VITE_EVALUATION_MODE=true
VITE_SUPABASE_URL=<Project URL>
VITE_SUPABASE_PUBLISHABLE_KEY=<Publishable key>
```

No coloques secretos en variables que empiecen por `VITE_`: Vite las incorpora al JavaScript público.

## 6. Dominio

1. En Vercel añade `kids.alfredopretelvargas.com` al proyecto web.
2. Vercel mostrará el registro DNS exacto requerido.
3. Desde Cloudflare móvil crea ese CNAME/A exacto. Durante la verificación usa **DNS only** si Vercel lo solicita; no inventes el destino.
4. Espera que Vercel confirme dominio y certificado antes de usarlo como Site URL definitivo.

Referencias: [dominio personalizado de Vercel](https://vercel.com/docs/domains/working-with-domains/add-a-domain) y [subdominios en Cloudflare](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-subdomain/).

## 7. Primer acceso owner y proveedor IA

**Estado verificado el 11 de septiembre de 2026:** Alfredo completó el enlace
mágico originado desde Kids, registró y confirmó TOTP MFA, y accedió al
workspace owner alojado. Las consultas administrativas de identidad, cobertura,
catálogo, costes, personas, revisiones, pilotos, incidencias y auditoría
respondieron correctamente. Lo siguiente en esta sección es configurar y probar
la primera ruta de proveedor IA real.

1. Abre la invitación owner en el móvil.
2. En `/admin`, registra TOTP y vuelve a autenticarte; las acciones sensibles exigen MFA reciente.
3. En **IA → Proveedores**, crea la conexión OpenRouter, OpenAI o Anthropic. La clave se muestra solo al escribirla y nunca vuelve al navegador.
4. Prueba la conexión, crea el deployment, registra la tarifa, configura la ruta por `operation_key`, ejecuta su golden eval y solo entonces actívala.
5. Confirma que uso, tokens, metadatos, costo y fallback aparecen sin prompts ni datos infantiles.

Hasta activar una ruta aprobada, las actividades, sesiones y feedback funcionan; el RAG conserva búsqueda full-text y el acompañante responde con abstención segura cuando no existe proveedor.

## 8. Invitación de familias y aceptación

Desde **Admin → Pilotos**:

1. envía una invitación a un correo adulto de prueba;
2. confirma que el correo llega y abre `/?onboarding=1`;
3. crea familia y perfiles solo con alias y banda de edad;
4. verifica aislamiento usando dos familias distintas;
5. prueba onboarding, plan, actividad, puerta adulta, acompañante, confirmación de adaptación, cierre, recorrido, feedback y privacidad.

La franja visible “Evaluación técnica · contenido sintético” debe permanecer durante esta fase. Retirarla exige contenido exacto con derechos, ejecución física y gates humanos/profesionales.

## 9. Gate antes de compartir con Lía

- Workflow de aprovisionamiento verde.
- Las 65 tablas `kids_*` siguen con RLS y el smoke test de Declassified conserva catálogo, compras y descargas.
- API `/health` responde y web carga desde el dominio final.
- Owner y familia real pueden autenticarse; MFA owner activo.
- RLS comprobado con dos familias.
- Riesgo C/D ausente de superficies familiares.
- Ningún secreto aparece en HTML, bundle, logs o capturas.
- SMTP, Logfire y al menos una ruta IA real probados.
- Capturas/presentación muestran claramente qué es evidencia técnica y qué sigue pendiente de piloto humano.
