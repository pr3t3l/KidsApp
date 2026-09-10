import { useEffect, useState, type ReactNode } from "react";
import type { Locale } from "./types";

type PublicPage = "welcome" | "privacy" | "terms" | "safety";

const pageTitles: Record<PublicPage, Record<Locale, string>> = {
  welcome: { "es-US": "Aprendizaje acompañado por adultos", "en-US": "Adult-guided learning" },
  privacy: { "es-US": "Aviso de privacidad del piloto", "en-US": "Pilot privacy notice" },
  terms: { "es-US": "Términos del piloto", "en-US": "Pilot terms" },
  safety: { "es-US": "Centro de seguridad", "en-US": "Safety center" },
};

function initialLocale(): Locale {
  const requested = new URLSearchParams(window.location.search).get("lang");
  if (requested === "en-US" || requested === "es-US") return requested;
  const stored = window.localStorage.getItem("kids.public_locale");
  if (stored === "en-US" || stored === "es-US") return stored;
  return navigator.language.toLowerCase().startsWith("es") ? "es-US" : "en-US";
}

function PublicHeader({ locale, setLocale }: { locale: Locale; setLocale: (locale: Locale) => void }) {
  const es = locale === "es-US";
  return <header className="public-header">
    <a className="public-brand" href="/welcome" aria-label="Kids Learning System">
      <span className="brand-mark" aria-hidden="true"><i/><i/><i/></span>
      <span><strong>Kids Learning</strong><small>{es ? "Guiado por adultos" : "Grown-up guided"}</small></span>
    </a>
    <nav aria-label={es ? "Navegación pública" : "Public navigation"}>
      <a href="/safety">{es ? "Seguridad" : "Safety"}</a>
      <a href="/privacy">{es ? "Privacidad" : "Privacy"}</a>
      <a href="/terms">{es ? "Términos" : "Terms"}</a>
      <button onClick={() => setLocale(es ? "en-US" : "es-US")} aria-label={es ? "Read in English" : "Leer en español"}>{es ? "EN" : "ES"}</button>
      <a className="public-login" href="/">{es ? "Entrar" : "Sign in"}</a>
    </nav>
  </header>;
}

function LegalDraft({ locale }: { locale: Locale }) {
  return <aside className="legal-draft" role="note"><strong>{locale === "es-US" ? "Documento de piloto" : "Pilot document"}</strong><span>{locale === "es-US" ? "Texto operativo implementado; requiere revisión legal cualificada antes de un lanzamiento comercial." : "Implemented operational copy; qualified legal review is required before commercial launch."}</span></aside>;
}

function Welcome({ locale }: { locale: Locale }) {
  const es = locale === "es-US";
  return <>
    <section className="public-hero"><div>
      <p className="eyebrow">{es ? "Actividades de 5 a 10 años · Piloto privado" : "Ages 5–10 · Private pilot"}</p>
      <h1>{es ? "Ideas claras para aprender juntos, con un adulto siempre presente." : "Clear ideas for learning together, with an adult always present."}</h1>
      <p>{es ? "Kids Learning System ayuda al adulto a elegir, preparar y acompañar actividades prácticas. La guía publicada funciona sin IA; el asistente solo propone cambios previamente revisados y nunca los aplica sin confirmación." : "Kids Learning System helps an adult choose, prepare, and guide hands-on activities. The published guide works without AI; the companion only proposes previously reviewed changes and never applies them without confirmation."}</p>
      <div className="public-actions"><a className="button primary" href="/">{es ? "Entrar al piloto" : "Enter the pilot"}</a><a className="button secondary" href="/safety">{es ? "Cómo cuidamos la experiencia" : "How safety works"}</a></div>
    </div><aside className="public-proof"><span>01</span><strong>{es ? "El adulto decide" : "The adult decides"}</strong><p>{es ? "Antes de iniciar, revisas materiales, participantes, propósito y seguridad." : "Before starting, you review materials, participants, purpose, and safety."}</p><span>02</span><strong>{es ? "La versión queda fijada" : "The version is pinned"}</strong><p>{es ? "Una sesión conserva exactamente la actividad que aprobaste." : "A session preserves the exact activity you approved."}</p><span>03</span><strong>{es ? "Observaciones, no notas" : "Observations, not grades"}</strong><p>{es ? "El recorrido describe lo que probaron sin evaluar ni diagnosticar al niño." : "The journey describes what you tried without grading or diagnosing the child."}</p></aside></section>
    <section className="public-grid" aria-label={es ? "Principios del producto" : "Product principles"}>
      <article><b>✦</b><h2>{es ? "Hecho para acompañar" : "Built for co-use"}</h2><p>{es ? "No hay cuentas infantiles, comunidad, voz, fotografías ni publicidad en el piloto." : "The pilot has no child accounts, community, voice, photos, or advertising."}</p></article>
      <article><b>◎</b><h2>{es ? "Recomendaciones explicables" : "Explainable recommendations"}</h2><p>{es ? "Edad, tiempo, participantes, materiales y seguridad determinan qué aparece." : "Age, time, participants, materials, and safety determine what appears."}</p></article>
      <article><b>↗</b><h2>{es ? "Cambios bajo control" : "Controlled changes"}</h2><p>{es ? "El asistente no navega, publica ni inventa sustituciones. Una propuesta requiere tu confirmación." : "The companion cannot browse, publish, or invent substitutions. A proposal needs your confirmation."}</p></article>
    </section>
    <section className="public-callout"><div><p className="eyebrow">{es ? "Para familias invitadas" : "For invited families"}</p><h2>{es ? "Prueba el recorrido completo y cuéntanos dónde se traba." : "Try the full journey and tell us where it gets stuck."}</h2></div><a className="button primary" href="/?onboarding=1">{es ? "Configurar mi familia" : "Set up my family"}</a></section>
  </>;
}

function Privacy({ locale }: { locale: Locale }) {
  const es = locale === "es-US";
  return <article className="public-document"><LegalDraft locale={locale}/><p className="eyebrow">{es ? "Vigente para el piloto privado" : "Effective for the private pilot"}</p><h1>{pageTitles.privacy[locale]}</h1><p className="lead">{es ? "Este aviso explica qué datos usa el piloto, para qué los usa y qué controles tiene el adulto responsable." : "This notice explains what data the pilot uses, why it uses it, and what controls the responsible adult has."}</p>
    <h2>{es ? "Datos que usamos" : "Data we use"}</h2><ul>
      <li>{es ? "Correo del adulto para autenticación por enlace mágico." : "Adult email for magic-link authentication."}</li>
      <li>{es ? "Estado, zona horaria, idioma, unidades y preferencias prácticas de la familia." : "State, time zone, language, units, and practical family preferences."}</li>
      <li>{es ? "Apodos y bandas de edad 5–6, 7–8 o 9–10; nunca exigimos el nombre legal ni fecha de nacimiento completa del niño." : "Aliases and age bands 5–6, 7–8, or 9–10; we never require a child's legal name or full birth date."}</li>
      <li>{es ? "Actividad y versión iniciada, avance, duración y una observación opcional del adulto." : "Activity and exact version started, progress, duration, and an optional adult observation."}</li>
      <li>{es ? "Metadatos operativos de IA como modelo, tokens, coste, latencia y resultado; no guardamos prompts ni respuestas libres por defecto." : "Operational AI metadata such as model, tokens, cost, latency, and outcome; prompts and free-form responses are not stored by default."}</li>
    </ul>
    <h2>{es ? "Lo que no pedimos en el piloto" : "What the pilot does not request"}</h2><p>{es ? "No creamos cuentas infantiles ni pedimos correo, escuela, fotografía, voz o ubicación precisa del niño. No hay publicidad ni comunidad social." : "We do not create child accounts or request a child's email, school, photo, voice, or precise location. There is no advertising or social community."}</p>
    <h2>{es ? "Comentarios y conservación" : "Feedback and retention"}</h2><p>{es ? "El comentario es opcional. Intentamos retirar correos y teléfonos antes de guardarlo; aun así, no debes incluir datos personales. El texto redactado se programa para eliminación a los 90 días. Métricas agregadas sin identificar a la familia pueden conservarse para evaluar el producto." : "Feedback is optional. We attempt to remove email addresses and phone numbers before storage; nevertheless, do not include personal information. Redacted text is scheduled for deletion after 90 days. Aggregated metrics that do not identify a family may be retained to evaluate the product."}</p>
    <h2>{es ? "Controles del adulto" : "Adult controls"}</h2><p>{es ? "Desde Familia puedes solicitar una exportación o eliminación. Estas acciones exigen autenticación reciente. Durante el piloto, las solicitudes se registran para ejecución y seguimiento por el responsable del servicio." : "From Family you can request export or deletion. These actions require recent authentication. During the pilot, requests are logged for execution and follow-up by the service owner."}</p>
    <h2>{es ? "Seguridad y proveedores" : "Security and processors"}</h2><p>{es ? "El acceso a datos familiares se aísla por familia. Los secretos de proveedores permanecen en el backend. Supabase presta autenticación y almacenamiento; proveedores de IA aprobados procesan únicamente el contexto mínimo permitido para la operación configurada." : "Family data access is isolated by family. Provider secrets remain on the backend. Supabase provides authentication and storage; approved AI providers process only the minimum context allowed for the configured operation."}</p>
    <h2>{es ? "Contacto" : "Contact"}</h2><p>{es ? "Antes del piloto externo se publicará un canal de privacidad verificable y la identidad jurídica responsable. Hasta entonces, utiliza el canal directo por el que recibiste la invitación." : "Before the external pilot, a verifiable privacy contact and responsible legal identity will be published. Until then, use the direct channel through which you received your invitation."}</p>
  </article>;
}

function Terms({ locale }: { locale: Locale }) {
  const es = locale === "es-US";
  return <article className="public-document"><LegalDraft locale={locale}/><p className="eyebrow">{es ? "Vigente para el piloto privado" : "Effective for the private pilot"}</p><h1>{pageTitles.terms[locale]}</h1><p className="lead">{es ? "El acceso es para adultos invitados que aceptan acompañar presencialmente cada actividad." : "Access is for invited adults who agree to be physically present for every activity."}</p>
    <h2>{es ? "Uso permitido" : "Permitted use"}</h2><p>{es ? "Puedes usar las actividades en tu hogar con los participantes de tu familia para evaluar el piloto. No puedes revender el contenido, automatizar el acceso, intentar entrar a otras familias ni usar la aplicación sin supervisión adulta." : "You may use activities at home with your family participants to evaluate the pilot. You may not resell content, automate access, attempt to access other families, or use the application without adult supervision."}</p>
    <h2>{es ? "Responsabilidad del adulto" : "Adult responsibility"}</h2><p>{es ? "Antes de empezar, comprueba materiales, alergias, espacio y capacidad de los participantes. Detén la actividad si aparece una señal de parada o una condición no prevista. La puerta matemática es solo fricción para niños; no verifica legalmente edad o identidad." : "Before starting, check materials, allergies, the environment, and participant ability. Stop if a stop signal or unexpected condition appears. The math gate is child friction only; it does not legally verify age or identity."}</p>
    <h2>{es ? "Límites del servicio" : "Service limits"}</h2><p>{es ? "El producto ofrece actividades educativas generales. No brinda consejo médico, psicológico ni diagnóstico; no sustituye a docentes, profesionales de salud, instrucciones del fabricante o servicios de emergencia. El piloto puede cambiar, pausarse o retirar una actividad por seguridad." : "The product offers general educational activities. It does not provide medical or psychological advice or diagnosis; it does not replace teachers, health professionals, manufacturer instructions, or emergency services. The pilot may change, pause, or withdraw an activity for safety."}</p>
    <h2>{es ? "IA y contenido" : "AI and content"}</h2><p>{es ? "La IA puede asistir con respuestas o borradores, pero no aprueba ni publica actividades. Las versiones disponibles para familias atraviesan controles editoriales definidos. Si el asistente falla, continúa usando la guía publicada." : "AI may assist with answers or drafts, but it does not approve or publish activities. Versions made available to families pass defined editorial controls. If the companion fails, continue with the published guide."}</p>
    <h2>{es ? "Piloto sin garantía comercial" : "Non-commercial pilot status"}</h2><p>{es ? "La disponibilidad no está garantizada y no hay pagos dentro de la aplicación durante el piloto. Comunicaremos cambios materiales a los adultos invitados antes de exigir una nueva aceptación." : "Availability is not guaranteed and there are no in-app payments during the pilot. Material changes will be communicated to invited adults before requiring renewed acceptance."}</p>
  </article>;
}

function Safety({ locale }: { locale: Locale }) {
  const es = locale === "es-US";
  return <article className="public-document safety-document"><p className="eyebrow">{es ? "La seguridad es una puerta, no una etiqueta" : "Safety is a gate, not a label"}</p><h1>{pageTitles.safety[locale]}</h1><p className="lead">{es ? "El adulto mantiene el control antes, durante y después de cada actividad." : "The adult remains in control before, during, and after every activity."}</p>
    <div className="safety-steps"><section><span>1</span><h2>{es ? "Antes" : "Before"}</h2><p>{es ? "Lee propósito, materiales, riesgo y advertencias. Sustituye la actividad —no una regla de seguridad— si no encaja." : "Read the purpose, materials, risk, and warnings. Replace the activity—not a safety rule—if it does not fit."}</p></section><section><span>2</span><h2>{es ? "Durante" : "During"}</h2><p>{es ? "Permanece presente. La IA puede orientar o proponer opciones publicadas; tú confirmas cualquier cambio." : "Stay present. AI may guide or propose published options; you confirm every change."}</p></section><section><span>3</span><h2>{es ? "Si algo cambia" : "If conditions change"}</h2><p>{es ? "Detén la actividad, aleja a los participantes del peligro y sigue las indicaciones de emergencia locales cuando corresponda." : "Stop the activity, move participants away from danger, and follow local emergency guidance when appropriate."}</p></section></div>
    <h2>{es ? "Niveles editoriales" : "Editorial levels"}</h2><dl className="risk-list"><div><dt>A</dt><dd>{es ? "Riesgo cotidiano bajo con presencia adulta." : "Low everyday risk with an adult present."}</dd></div><div><dt>B</dt><dd>{es ? "Controles adultos específicos y señales de parada visibles." : "Specific adult controls and visible stop signals."}</dd></div><div><dt>C</dt><dd>{es ? "Requiere revisión profesional independiente antes de asignarse a familias." : "Requires independent professional review before family assignment."}</dd></div><div><dt>D</dt><dd>{es ? "Bloqueado; no se ofrece a familias." : "Blocked; never offered to families."}</dd></div></dl>
    <h2>{es ? "Reportar un problema" : "Report a concern"}</h2><p>{es ? "Usa Feedback desde cualquier pantalla y selecciona Seguridad. Un reporte alto o crítico retira automáticamente esa versión de nuevas recomendaciones mientras se investiga. Para una emergencia, utiliza los servicios locales; la aplicación no es un canal de emergencia." : "Use Feedback from any screen and choose Safety. A high or critical report automatically removes that version from new recommendations while it is investigated. For an emergency, use local services; the application is not an emergency channel."}</p>
  </article>;
}

function PublicFooter({ locale }: { locale: Locale }) {
  const es = locale === "es-US";
  return <footer className="public-footer"><p>Kids Learning System · {es ? "piloto privado dirigido a adultos" : "adult-directed private pilot"}</p><nav><a href="/privacy">{es ? "Privacidad" : "Privacy"}</a><a href="/terms">{es ? "Términos" : "Terms"}</a><a href="/safety">{es ? "Seguridad" : "Safety"}</a></nav></footer>;
}

export default function PublicSite({ page }: { page: PublicPage }) {
  const [locale, setLocaleState] = useState<Locale>(initialLocale);
  useEffect(() => { document.documentElement.lang = locale; document.title = `${pageTitles[page][locale]} · Kids Learning System`; }, [locale, page]);
  function setLocale(value: Locale) { window.localStorage.setItem("kids.public_locale", value); setLocaleState(value); }
  const content: Record<PublicPage, ReactNode> = { welcome: <Welcome locale={locale}/>, privacy: <Privacy locale={locale}/>, terms: <Terms locale={locale}/>, safety: <Safety locale={locale}/> };
  const evaluation = import.meta.env.VITE_EVALUATION_MODE === "true";
  return <div className="public-shell"><a className="skip-link" href="#main">{locale === "es-US" ? "Saltar al contenido" : "Skip to content"}</a>{evaluation&&<aside className="legal-draft" role="note"><strong>{locale === "es-US" ? "Entorno de evaluación" : "Evaluation environment"}</strong><span>{locale === "es-US" ? "El catálogo visible es sintético y no representa una aprobación comercial o profesional." : "Visible catalog content is synthetic and does not represent commercial or professional approval."}</span></aside>}<PublicHeader locale={locale} setLocale={setLocale}/><main id="main">{content[page]}</main><PublicFooter locale={locale}/></div>;
}
