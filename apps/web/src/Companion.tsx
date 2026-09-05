import { FormEvent, useState } from "react";
import { decideProposal, sendInteraction } from "./api";
import type { CompanionResponse, ExperienceView } from "./types";
import { copy } from "./copy";

type Props = { experience: ExperienceView; onExperienceChanged: (experience: ExperienceView) => void };

export function Companion({ experience, onExperienceChanged }: Props) {
  const t = copy[experience.locale];
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [response, setResponse] = useState<CompanionResponse | null>(null);
  const [selectedOptionId, setSelectedOptionId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    const trimmed = message.trim();
    if (!trimmed || busy) return;
    setBusy(true); setError(null);
    try { const next = await sendInteraction(experience.contextId, trimmed, experience.locale); setResponse(next); setSelectedOptionId(next.proposal?.options[0]?.optionId ?? null); setMessage(""); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "The companion is unavailable. The activity guide still works."); }
    finally { setBusy(false); }
  }

  async function decide(decision: "confirm" | "reject") {
    if (!response?.proposal) return;
    setBusy(true); setError(null);
    try {
      const updated = await decideProposal(response.proposal.proposalId, decision, decision === "confirm" ? selectedOptionId ?? undefined : undefined);
      onExperienceChanged(updated);
      setResponse({ ...response, status: "answer", proposal: null, requiresAdultConfirmation: false, answer: decision === "confirm" ? t.updated : t.unchanged });
    } catch (reason) { setError(reason instanceof Error ? reason.message : "We could not apply that decision."); }
    finally { setBusy(false); }
  }

  return <>
    <button className="companion-fab" aria-expanded={open} aria-controls="companion-panel" onClick={() => setOpen((value) => !value)}><span aria-hidden="true">✦</span><span className="sr-only">{t.companion}</span></button>
    {open && <aside id="companion-panel" className="companion-panel" aria-label="Activity companion">
      <header><div><p className="eyebrow">{t.companion}</p><h2>{t.happening}</h2></div><button className="icon-button" onClick={() => setOpen(false)} aria-label={t.close}>×</button></header>
      <p className="companion-note">{t.note}</p>
      {response && <section className={`companion-response ${response.safetyStatus === "stop" ? "stop" : ""}`} aria-live="polite">
        <span className="response-status">{response.status.replace("_", " ")}</span><p>{response.answer}</p>
        {response.sources.length > 0 && <small>{t.basedOn} {response.sources.map((source) => source.label).join(", ")}</small>}
        {response.proposal && <div className="proposal"><fieldset><legend>{t.choose}</legend>{response.proposal.options.map((option) => <label className={`proposal-option ${selectedOptionId === option.optionId ? "selected" : ""}`} key={option.optionId}><input type="radio" name="proposal-option" value={option.optionId} checked={selectedOptionId === option.optionId} onChange={() => setSelectedOptionId(option.optionId)}/><span><strong>{option.summary}</strong><small>{option.visibleChanges.join(" · ")}</small></span></label>)}</fieldset><div className="proposal-actions"><button className="button primary" disabled={!selectedOptionId} onClick={() => decide("confirm")}>{t.confirm}</button><button className="button secondary" onClick={() => decide("reject")}>{t.keep}</button></div></div>}
      </section>}
      {error && <p className="error" role="alert">{error}</p>}
      <form onSubmit={submit}><label htmlFor="companion-message">{t.message}</label><textarea id="companion-message" value={message} onChange={(event) => setMessage(event.target.value)} maxLength={800} placeholder={t.placeholder} rows={3}/><button className="button primary block" disabled={!message.trim() || busy}>{busy ? t.checking : t.ask}</button></form>
    </aside>}
  </>;
}
