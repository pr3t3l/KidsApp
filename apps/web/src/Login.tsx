import { FormEvent, useState } from "react";
import { sendMagicLink } from "./auth";
import { copy } from "./copy";
import type { Locale } from "./types";

export function Login({ locale = "en-US" }: { locale?: Locale }) {
  const t = copy[locale];
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  async function submit(event: FormEvent) {
    event.preventDefault(); setError(null);
    try { await sendMagicLink(email); setSent(true); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "Unable to send sign-in link"); }
  }
  return <main className="login"><section className="login-card"><div className="brand-mark" aria-hidden="true"><i/><i/><i/></div><p className="eyebrow">Kids Learning System</p><h1>{t.signIn}</h1><p>{t.privatePilot}</p>{sent ? <p className="success" role="status">{t.sent}</p> : <form onSubmit={submit}><label htmlFor="email">{t.email}</label><input id="email" type="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)}/><button className="button primary block">{t.sendLink}</button></form>}{error && <p className="error" role="alert">{error}</p>}<nav className="login-legal" aria-label="Legal"><a href="/welcome">{locale === "es-US" ? "Acerca del piloto" : "About the pilot"}</a><a href="/privacy">{locale === "es-US" ? "Privacidad" : "Privacy"}</a><a href="/terms">{locale === "es-US" ? "Términos" : "Terms"}</a><a href="/safety">{locale === "es-US" ? "Seguridad" : "Safety"}</a></nav></section></main>;
}
