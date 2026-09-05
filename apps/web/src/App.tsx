import { useEffect, useState } from "react";
import { getExperience } from "./api";
import { renderBlock } from "./blocks";
import { Companion } from "./Companion";
import { DEMO_CONTEXT_ID } from "./demo";
import type { ExperienceView } from "./types";
import { copy } from "./copy";
import { supabase } from "./auth";
import { Login } from "./Login";

const demoMode = import.meta.env.VITE_DEMO_MODE !== "false";

export default function App() {
  const [experience, setExperience] = useState<ExperienceView | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [authenticated, setAuthenticated] = useState(demoMode);
  useEffect(() => {
    let active = true;
    async function initialize() {
      if (!demoMode) {
        if (!supabase) { setError("Supabase authentication is not configured."); return; }
        const { data } = await supabase.auth.getSession();
        if (!data.session) { setAuthenticated(false); return; }
        window.localStorage.setItem("kids.access_token", data.session.access_token); setAuthenticated(true);
      }
      const params = new URLSearchParams(window.location.search);
      const contextId = params.get("context") ?? import.meta.env.VITE_DEFAULT_CONTEXT_ID ?? import.meta.env.VITE_DEMO_CONTEXT_ID ?? DEMO_CONTEXT_ID;
      getExperience(contextId).then((value) => { if (active) { document.documentElement.lang = value.locale; setExperience(value); } }).catch((reason) => { if (active) setError(reason instanceof Error ? reason.message : "Unable to load activity"); });
    }
    initialize();
    const listener = supabase?.auth.onAuthStateChange((_event, session) => { if (session) { window.localStorage.setItem("kids.access_token", session.access_token); setAuthenticated(true); initialize(); } else { window.localStorage.removeItem("kids.access_token"); setAuthenticated(false); } });
    return () => { active = false; listener?.data.subscription.unsubscribe(); };
  }, []);
  if (!authenticated) return <Login/>;
  if (error) return <main className="fatal"><h1>{copy["en-US"].unavailable}</h1><p>{error}</p></main>;
  if (!experience) return <main className="loading">{copy["en-US"].loading}</main>;
  const t = copy[experience.locale];
  return <div className="prototype-frame"><aside className="prototype-label"><strong>Pocket Workshop</strong><span>Production-shaped pilot · adult-led family learning</span></aside><main className="app-shell"><header className="app-header"><div className="brand-mark" aria-hidden="true"><i/><i/><i/></div><div><strong>Kids Learning System</strong><small>{experience.status} · {experience.locale}</small></div><span className="secure-badge">{t.privatePilot}</span></header><div className="activity-view"><section className="hero"><p className="eyebrow">{t.today}</p><h1>{experience.title}</h1><p>{experience.summary}</p><div className="hero-meta"><span><strong>30</strong><small>{t.minutes}</small></span><span><strong>1–4</strong><small>{t.children}</small></span><span><strong>A</strong><small>{t.safety}</small></span></div></section><section className="block-stack" aria-label="Activity guide">{experience.blocks.map((block) => <div key={block.id} data-block-id={block.id}>{renderBlock(block)}</div>)}</section></div><Companion experience={experience} onExperienceChanged={setExperience}/></main></div>;
}
