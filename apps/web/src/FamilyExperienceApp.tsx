import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  closeFamilySession,
  createAdultGate,
  createFamilyPreview,
  DEMO_FAMILY_ID,
  DEMO_MODE,
  EVALUATION_MODE,
  getCatalog,
  getExperience,
  getFamilyOverview,
  requestPrivacyAction,
  restoreDemoSession,
  sendFamilyFeedback,
  setupFamily,
  startFamilySession,
  updateSessionProgress,
  verifyAdultGate,
} from "./api";
import { deferAuthStateWork, requestReauthentication, signOut, supabase } from "./auth";
import { renderBlock } from "./blocks";
import { Companion } from "./Companion";
import { familyProductCopy } from "./familyProductCopy";
import { Login } from "./Login";
import { clearActiveSession, flushOfflineEvents, isNetworkFailure, loadActiveSession, pendingOfflineEvents, queueCloseout, queueProgress, saveActiveSession } from "./offlineSession";
import type { AdultGateChallenge, CatalogCard, ExperienceView, FamilyOverview, FamilyProfile, FamilySession, JourneyView, Locale } from "./types";

type FamilyTab = "today" | "plan" | "explore" | "journey" | "family";
type SetupInput = Parameters<typeof setupFamily>[0];

const initialLocale = (): Locale => {
  const saved = localStorage.getItem("kids.locale");
  if (saved === "en-US" || saved === "es-US") return saved;
  return navigator.language.toLowerCase().startsWith("es") ? "es-US" : "en-US";
};

function Brand({ locale }: { locale: Locale }) {
  return <a className="family-brand" href="/"><span className="brand-mark" aria-hidden="true"><i/><i/><i/></span><span><strong>Kids Learning</strong><small>{familyProductCopy[locale].brandSub}</small></span></a>;
}

function ActivityCard({ card, locale, compact = false, onStart }: { card: CatalogCard; locale: Locale; compact?: boolean; onStart: (card: CatalogCard) => void }) {
  const t = familyProductCopy[locale];
  return <article className={`family-activity-card ${compact ? "compact" : ""}`}>
    <div className={`activity-art art-${Number(card.activityVersionId.replace(/\D/g, "").slice(-2)) % 4}`}><span>{card.title.split(" ").map(word => word[0]).join("").slice(0, 2)}</span><small>{card.mess} {t.mess}</small></div>
    <div className="activity-card-body"><div className="card-tags"><span>{card.minutes} min</span><span>{card.age[0]}–{card.age[1]} {t.years}</span><span>{t.risk} {card.risk}</span></div><h3>{card.title}</h3><p>{card.summary}</p><button className="button primary" onClick={() => onStart(card)}>{compact ? t.viewActivity : t.prepareActivity}</button></div>
  </article>;
}

function Onboarding({ onDone, onClose, initial, defaultLocale }: { onDone: (input: SetupInput) => Promise<void>; onClose?: () => void; initial?: FamilyProfile; defaultLocale: Locale }) {
  const editing = Boolean(initial);
  const [step, setStep] = useState(editing ? 1 : 0);
  const [adultLed, setAdultLed] = useState(editing);
  const [busy, setBusy] = useState(false);
  const [aliases, setAliases] = useState(initial?.learners.map(item => item.alias) ?? ["Explorer 1", "Builder 2"]);
  const [ageBands, setAgeBands] = useState<Array<"5-6" | "7-8" | "9-10">>(initial?.learners.map(item => item.ageBand) ?? ["5-6", "7-8"]);
  const [learnerIds, setLearnerIds] = useState<Array<string | null>>(initial?.learners.map(item => item.learnerId) ?? [null, null]);
  const [removedLearnerIds, setRemovedLearnerIds] = useState<string[]>([]);
  const [minutes, setMinutes] = useState(initial?.preferences.minutes ?? 30);
  const [participants, setParticipants] = useState(initial?.preferences.participants ?? 2);
  const [mess, setMess] = useState<"low" | "medium" | "high">(initial?.preferences.mess ?? "low");
  const [familyName, setFamilyName] = useState(initial?.familyName ?? (defaultLocale === "es-US" ? "Mi familia" : "My family"));
  const [stateCode, setStateCode] = useState(initial?.stateCode ?? "FL");
  const [locale, setLocale] = useState<Locale>(initial?.locale ?? defaultLocale);
  const [units, setUnits] = useState<"metric" | "us_customary">(initial?.units ?? "metric");
  const [error, setError] = useState<string | null>(null);
  const t = familyProductCopy[locale];

  function removeLearner(index: number) {
    const id = learnerIds[index];
    if (id) setRemovedLearnerIds(old => [...old, id]);
    setAliases(old => old.filter((_, item) => item !== index));
    setAgeBands(old => old.filter((_, item) => item !== index));
    setLearnerIds(old => old.filter((_, item) => item !== index));
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true); setError(null);
    try {
      await onDone({ familyName, stateCode: stateCode.toUpperCase(), locale, units, timezone: initial?.timezone ?? (Intl.DateTimeFormat().resolvedOptions().timeZone || "America/New_York"), learnerAliases: aliases, ageBands, learnerIds, removedLearnerIds, participants, minutes, mess });
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : t.saveFamilyError);
    } finally { setBusy(false); }
  }

  return <div className="family-modal full"><section className="onboarding-card">
    {onClose && <button className="modal-close" onClick={onClose} aria-label="Close">×</button>}
    <Brand locale={locale}/><div className="onboarding-progress">{[0, 1, 2].map(index => <i className={index <= step ? "active" : ""} key={index}/>)}</div>
    {step === 0 && <div className="onboarding-step"><p className="eyebrow">{t.beforeStart}</p><h1>{t.togetherTitle}</h1><p>{t.togetherBody}</p><label className="consent-row"><input type="checkbox" checked={adultLed} onChange={event => setAdultLed(event.target.checked)}/><span><strong>{t.consentTitle}</strong><small>{t.consentBody}</small></span></label><button className="button primary block" disabled={!adultLed} onClick={() => setStep(1)}>{t.continue}</button></div>}
    {step === 1 && <div className="onboarding-step"><p className="eyebrow">{t.home}</p><h1>{editing ? t.updateHome : t.homeQuestion}</h1><div className="learner-line"><label>{t.familyName}<input value={familyName} onChange={event => setFamilyName(event.target.value)} maxLength={80}/></label><label>{t.state}<input value={stateCode} disabled={editing} onChange={event => setStateCode(event.target.value.replace(/[^A-Za-z]/g, "").slice(0, 2))} maxLength={2}/></label></div><div className="learner-line"><label>{t.language}<select value={locale} onChange={event => setLocale(event.target.value as Locale)}><option value="es-US">Español</option><option value="en-US">English</option></select></label><label>{t.units}<select value={units} onChange={event => setUnits(event.target.value as typeof units)}><option value="metric">{t.metric}</option><option value="us_customary">{t.us}</option></select></label></div><div className="choice-grid"><button className={minutes === 30 ? "selected" : ""} onClick={() => setMinutes(30)}>{t.min30}</button><button className={minutes === 20 ? "selected" : ""} onClick={() => setMinutes(20)}>{t.min20}</button><button className={mess === "low" ? "selected" : ""} onClick={() => setMess("low")}>{t.lowMess}</button><button className={mess === "medium" ? "selected" : ""} onClick={() => setMess("medium")}>{t.mediumMess}</button><button className={participants === 2 ? "selected" : ""} onClick={() => setParticipants(2)}>{t.kids12}</button><button className={participants === 4 ? "selected" : ""} onClick={() => setParticipants(4)}>{t.kids34}</button></div><p className="privacy-note">{editing ? t.stateEdit : t.stateNew}</p><button className="button primary block" disabled={stateCode.length !== 2 || !familyName.trim()} onClick={() => setStep(2)}>{t.continue}</button></div>}
    {step === 2 && <form className="onboarding-step" onSubmit={submit}><p className="eyebrow">{t.participants}</p><h1>{t.aliasesTitle}</h1>{aliases.map((alias, index) => <div className="learner-line" key={learnerIds[index] ?? `new-${index}`}><label>{t.nickname}<input value={alias} onChange={event => setAliases(old => old.map((value, item) => item === index ? event.target.value : value))} maxLength={40}/></label><label>{t.age}<select value={ageBands[index]} onChange={event => setAgeBands(old => old.map((value, item) => item === index ? event.target.value as typeof value : value))}><option>5-6</option><option>7-8</option><option>9-10</option></select></label>{aliases.length > 1 && <button type="button" className="text-button" onClick={() => removeLearner(index)}>{t.remove}</button>}</div>)}<button type="button" className="text-button" onClick={() => { if (aliases.length < 4) { setAliases(old => [...old, `Explorer ${old.length + 1}`]); setAgeBands(old => [...old, "7-8"]); setLearnerIds(old => [...old, null]); } }}>{t.addParticipant}</button>{error && <p className="error" role="alert">{error}</p>}<button className="button primary block" disabled={busy || aliases.some(alias => !alias.trim())}>{busy ? t.saving : editing ? t.saveChanges : t.firstPlan}</button><small>{t.noChildData}</small></form>}
  </section></div>;
}

function AdultGate({ challenge, locale, onPass, onClose }: { challenge: AdultGateChallenge; locale: Locale; onPass: (token: string) => Promise<void>; onClose: () => void }) {
  const t = familyProductCopy[locale];
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reauth, setReauth] = useState(false);
  const complete = challenge.prompts.every((_, index) => answers[index] !== undefined);
  async function submit() {
    if (!complete) return;
    setBusy(true); setError(null);
    try { const result = await verifyAdultGate(challenge.challengeId, challenge.prompts.map((_, index) => answers[index])); await onPass(result.adultGateToken); }
    catch (reason) { const message = reason instanceof Error ? reason.message : t.gateMismatch; setError(message); setReauth(/reauth/i.test(message)); }
    finally { setBusy(false); }
  }
  async function sendReauth() {
    setBusy(true);
    try { await requestReauthentication(); setError(t.reauthSent); }
    catch { setError(t.reauthFailed); }
    finally { setBusy(false); }
  }
  return <div className="family-modal"><section className="gate-card" role="dialog" aria-modal="true"><button className="modal-close" onClick={onClose}>×</button><div className="gate-icon">12</div><p className="eyebrow">{t.gate}</p><h2>{t.gateTitle}</h2><p>{t.gateBody}</p>{challenge.prompts.map((question, index) => <fieldset className="gate-question" key={`${question.word}-${index}`}><legend>{question.word}</legend><div>{question.options.map(option => <label className={answers[index] === option ? "selected" : ""} key={option}><input type="radio" name={`q-${index}`} checked={answers[index] === option} onChange={() => setAnswers(old => ({ ...old, [index]: option }))}/>{option}</label>)}</div></fieldset>)}{error && <p className="error" role="alert">{error}</p>}<button className="button primary block" disabled={!complete || busy || reauth} onClick={submit}>{busy ? t.checking : t.unlock}</button>{reauth && <button className="button secondary block" disabled={busy} onClick={sendReauth}>{t.sendReauth}</button>}</section></div>;
}

function FeedbackModal({ familyId, locale, activityVersionId, sessionId, screen, onClose }: { familyId: string; locale: Locale; activityVersionId?: string; sessionId?: string; screen: string; onClose: () => void }) {
  const t = familyProductCopy[locale];
  const [sent, setSent] = useState(false);
  const [useful, setUseful] = useState<boolean | null>(null);
  const [comment, setComment] = useState("");
  const [category, setCategory] = useState<"product" | "content" | "error" | "safety" | "privacy">("product");
  const [error, setError] = useState<string | null>(null);
  async function submit(event: FormEvent) {
    event.preventDefault(); if (useful === null) return; setError(null);
    try { await sendFamilyFeedback(familyId, { useful, comment, category, activityVersionId, sessionId, screen, locale, appVersion: "web-pilot-v1", browserFamily: navigator.userAgent.slice(0, 70), journeyState: activityVersionId ? "activity" : screen }); setSent(true); }
    catch (reason) { setError(reason instanceof Error ? reason.message : t.feedbackError); }
  }
  const categories = { product: t.product, content: t.content, error: t.error, safety: t.safety, privacy: t.privacy };
  return <div className="family-modal"><section className="feedback-card" role="dialog" aria-modal="true"><button className="modal-close" onClick={onClose}>×</button><p className="eyebrow">{t.pilotFamily}</p><h2>{t.feedbackTitle}</h2>{sent ? <div className="feedback-thanks"><span>✓</span><strong>{t.thanks}</strong><p>{t.retention}</p></div> : <form onSubmit={submit}><label>{t.useful}</label><div className="useful-choice"><label className={useful === true ? "selected" : ""}><input type="radio" name="useful" onChange={() => setUseful(true)}/>{t.yes}</label><label className={useful === false ? "selected" : ""}><input type="radio" name="useful" onChange={() => setUseful(false)}/>{t.no}</label></div><label>{t.type}<select value={category} onChange={event => setCategory(event.target.value as typeof category)}>{Object.entries(categories).map(([value, label]) => <option value={value} key={value}>{label}</option>)}</select></label><label>{t.optionalComment}<textarea rows={4} maxLength={1200} value={comment} onChange={event => setComment(event.target.value)} placeholder={t.commentPlaceholder}/></label>{error && <p className="error" role="alert">{error}</p>}<button className="button primary block" disabled={useful === null}>{t.sendComment}</button></form>}</section></div>;
}

function FamilyHeader({ locale, onFeedback }: { locale: Locale; onFeedback: () => void }) {
  const t = familyProductCopy[locale];
  const modeLabel = EVALUATION_MODE ? (locale === "es-US" ? "Evaluación técnica · contenido sintético" : "Technical evaluation · synthetic content") : t.privatePilot;
  return <header className="family-header"><Brand locale={locale}/><div className="family-header-actions"><span className="pilot-badge">{modeLabel}</span><button onClick={onFeedback}>♡ <span>{t.feedback}</span></button><span className="family-avatar">A</span></div></header>;
}

function Today({ card, explanation, locale, onStart }: { card: CatalogCard | null; explanation: string[]; locale: Locale; onStart: (card: CatalogCard) => void }) {
  const t = familyProductCopy[locale];
  return <div className="family-page"><section className="today-intro"><div><p className="eyebrow">{t.familyPlan}</p><h1>{t.todayTitle}</h1><p>{t.todayBody}</p></div><div className="why-card"><span>◎</span><div><strong>{t.why}</strong><small>{explanation.join(" · ").replaceAll("_", " ") || t.publishedRules}</small></div></div></section>{card ? <ActivityCard card={card} locale={locale} onStart={onStart}/> : <section className="journey-empty"><span>○</span><h2>{t.noMatch}</h2><p>{t.noDrafts}</p></section>}<section className="family-tip"><span>✦</span><div><strong>{t.guideWorks}</strong><p>{t.companionPurpose}</p></div></section></div>;
}

function Plan({ cards, locale, onStart, onBrowse }: { cards: CatalogCard[]; locale: Locale; onStart: (card: CatalogCard) => void; onBrowse: () => void }) {
  const t = familyProductCopy[locale];
  const days = [t.today, t.next, t.weekend];
  return <div className="family-page"><div className="page-heading"><p className="eyebrow">{t.yourWeek}</p><h1>{t.flexiblePlan}</h1><p>{t.planBody}</p><button className="button secondary" onClick={onBrowse}>{t.browseAlternatives}</button></div><div className="plan-list">{cards.map((card, index) => <article key={`${card.plannedActivityId ?? card.activityVersionId}-${index}`}><div className="plan-day"><strong>{days[index] ?? t.later}</strong><small>{index ? t.suggested : t.ready}</small></div><ActivityCard card={card} locale={locale} compact onStart={onStart}/></article>)}</div></div>;
}

function Explore({ cards, locale, onStart }: { cards: CatalogCard[]; locale: Locale; onStart: (card: CatalogCard) => void }) {
  const t = familyProductCopy[locale];
  const filters = [t.all, "20 min", t.littleMess, t.oneChild, t.riskA];
  const [filter, setFilter] = useState(filters[0]);
  const filtered = cards.filter(card => filter === t.all || filter === "20 min" && card.minutes <= 20 || filter === t.littleMess && card.mess === "low" || filter === t.oneChild && card.participants[0] === 1 || filter === t.riskA && card.risk === "A");
  return <div className="family-page wide"><div className="page-heading"><p className="eyebrow">{t.publishedCatalog}</p><h1>{t.explore}</h1><p>{t.exploreBody}</p></div><div className="filter-row">{filters.map(item => <button className={filter === item ? "active" : ""} onClick={() => setFilter(item)} key={item}>{item}</button>)}</div>{filtered.length ? <div className="catalog-grid">{filtered.map(card => <ActivityCard key={card.activityVersionId} card={card} locale={locale} compact onStart={onStart}/>)}</div> : <section className="journey-empty"><h2>{t.noResults}</h2><p>{t.tryFilter}</p></section>}</div>;
}

function Journey({ journey, locale }: { journey: JourneyView; locale: Locale }) {
  const t = familyProductCopy[locale];
  return <div className="family-page"><div className="page-heading"><p className="eyebrow">{t.observationsNotScores}</p><h1>{t.journey}</h1><p>{t.journeyBody}</p></div><section className="journey-summary"><div><strong>{journey.completed}</strong><span>{t.activitiesClosed}</span></div><div><strong>{journey.completed ? t.inProgress : "—"}</strong><span>{journey.completed ? t.explainableHistory : t.noTrend}</span></div></section>{journey.observations.length ? <section className="family-settings"><h2>{t.recentObservations}</h2>{journey.observations.map((item, index) => <article key={item.sessionId ?? index}><span className="learner-avatar">{item.outcome === "worked" ? "✓" : "≈"}</span><div><strong>{item.observation || t.noComment}</strong><small>{item.durationMinutes ?? 0} min · {item.activityVersionId}</small></div></article>)}</section> : <section className="journey-empty"><span>○</span><h2>{t.firstObservation}</h2><p>{t.afterActivity}</p></section>}</div>;
}

function FamilySettings({ family, onEdit, onPrivacy }: { family: FamilyProfile; onEdit: () => void; onPrivacy: (action: "export" | "delete") => Promise<void> }) {
  const t = familyProductCopy[family.locale];
  const [message, setMessage] = useState<string | null>(null);
  const [needsReauth, setNeedsReauth] = useState(false);
  async function privacy(action: "export" | "delete") { setMessage(t.processing); try { await onPrivacy(action); setMessage(action === "export" ? t.exportQueued : t.deleteQueued); } catch { setNeedsReauth(true); setMessage(t.reauthNeeded); } }
  async function reauthenticate() { try { await requestReauthentication(); setMessage(t.reauthSent); setNeedsReauth(false); } catch { setMessage(t.reauthFailed); } }
  return <div className="family-page"><div className="page-heading"><p className="eyebrow">{t.adultControl}</p><h1>{t.family}</h1><p>{t.familyBody}</p></div><section className="family-settings"><h2>{t.people}</h2>{family.learners.map((learner, index) => <article key={learner.learnerId}><span className={`learner-avatar ${index % 2 ? "alt" : ""}`}>{learner.alias.split(" ").map(word => word[0]).join("").slice(0, 2)}</span><div><strong>{learner.alias}</strong><small>{learner.ageBand} {t.years} · {t.nickname.toLowerCase()}</small></div></article>)}<button className="text-button" onClick={onEdit}>{t.editPreferences}</button></section><section className="family-settings"><h2>{t.preferences}</h2><dl><div><dt>{t.usualTime}</dt><dd>{family.preferences.minutes} min</dd></div><div><dt>{t.mess}</dt><dd>{family.preferences.mess}</dd></div><div><dt>{t.locale}</dt><dd>{family.locale}</dd></div></dl></section><section className="family-settings privacy"><h2>{t.privacyData}</h2><button onClick={() => privacy("export")}>{t.exportData} <b>→</b></button><button onClick={() => privacy("delete")}>{t.requestDelete} <b>→</b></button>{needsReauth && <button className="button secondary" onClick={reauthenticate}>{t.sendReauth}</button>}<small>{t.recentAuth} {message}</small><nav className="family-policy-links" aria-label="Policies"><a href={`/privacy?lang=${family.locale}`}>{t.policyPrivacy}</a><a href={`/terms?lang=${family.locale}`}>{t.policyTerms}</a><a href={`/safety?lang=${family.locale}`}>{t.policySafety}</a></nav><button className="text-button" onClick={() => signOut()}>{t.signOut}</button></section></div>;
}

function Preparation({ experience, family, onBack, onStart, onExperienceChanged }: { experience: ExperienceView; family: FamilyProfile; onBack: () => void; onStart: () => Promise<void>; onExperienceChanged: (value: ExperienceView) => void }) {
  const t = familyProductCopy[experience.locale];
  const participantCount = Math.min(4, Math.max(1, family.preferences.participants));
  const participants = family.learners.slice(0, participantCount);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  async function start() {
    setBusy(true); setError(null);
    try { await onStart(); }
    catch (reason) { setError(reason instanceof Error ? reason.message : t.gateError); setBusy(false); }
  }
  return <div className="preparation-shell">
    <header className="preparation-header"><button className="text-button" onClick={onBack}>← {t.backToCatalog}</button><Brand locale={experience.locale}/></header>
    <main className="preparation-main">
      <section className="preparation-intro"><p className="eyebrow">{t.preparationKicker}</p><h1>{t.preparationTitle}</h1><p>{t.preparationBody}</p><div className="preparation-version"><strong>{experience.title}</strong><small>{t.exactVersion} · {experience.activityVersionId}</small><p>{experience.summary}</p></div><div className="preparation-people"><strong>{t.selectedPeople}</strong>{participants.map(person => <span key={person.learnerId}>{person.alias}</span>)}</div></section>
      <section className="preparation-guide" aria-label={experience.title}>{experience.blocks.map(block => <article className="preparation-block" data-block-id={block.id} key={block.id}>{renderBlock(block, experience.locale)}</article>)}</section>
      <section className="preparation-ready"><div><strong>{t.readyToStart}</strong><small>{t.gateBody}</small></div><button className="button primary" disabled={busy} onClick={start}>{busy ? t.preparing : t.openAdultGate}</button>{error && <p className="error" role="alert">{error}</p>}</section>
    </main>
    <Companion experience={experience} onExperienceChanged={onExperienceChanged}/>
  </div>;
}

function Session({ record, experience, onExperienceChanged, onRecordChanged, onOfflineQueued, onFinish }: { record: FamilySession; experience: ExperienceView; onExperienceChanged: (value: ExperienceView) => void; onRecordChanged: (value: FamilySession) => void; onOfflineQueued: () => void; onFinish: () => Promise<void> }) {
  const t = familyProductCopy[experience.locale];
  const initial = Math.max(0, experience.blocks.findIndex(block => block.id === experience.currentBlockId));
  const [index, setIndex] = useState(initial);
  const [closeout, setCloseout] = useState(false);
  const [observation, setObservation] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const block = experience.blocks[Math.min(index, experience.blocks.length - 1)];
  const atEnd = index === experience.blocks.length - 1;
  async function move(next: number) {
    const nextBlock = experience.blocks[next]; if (!nextBlock) return;
    const nextExperience = { ...experience, currentBlockId: nextBlock.id };
    const localRecord = { ...record, currentBlockId: nextBlock.id, updatedAt: new Date().toISOString() };
    setBusy(true); setError(null);
    try {
      const saved = await updateSessionProgress(record.sessionId, nextBlock.id, "active");
      onRecordChanged(saved); onExperienceChanged(nextExperience); await saveActiveSession(saved, nextExperience); setIndex(next);
    } catch (reason) {
      if (!isNetworkFailure(reason)) { setError(reason instanceof Error ? reason.message : t.stepSaveError); return; }
      await queueProgress(record.sessionId, nextBlock.id, "active");
      await saveActiveSession(localRecord, nextExperience);
      onRecordChanged(localRecord); onExperienceChanged(nextExperience); onOfflineQueued(); setIndex(next); setError(t.offlineQueued);
    } finally { setBusy(false); }
  }
  async function exitInterrupted() {
    setBusy(true); setError(null);
    try { await updateSessionProgress(record.sessionId, block.id, "interrupted"); await clearActiveSession(); await onFinish(); }
    catch (reason) {
      if (!isNetworkFailure(reason)) { setError(reason instanceof Error ? reason.message : t.stepSaveError); setBusy(false); return; }
      await queueProgress(record.sessionId, block.id, "interrupted"); await clearActiveSession(); onOfflineQueued(); await onFinish();
    }
  }
  async function finish(outcome: "worked" | "partly" | "not_today") {
    setBusy(true); setError(null);
    const elapsed = Math.max(0, Math.min(180, Math.round((Date.now() - new Date(record.startedAt).getTime()) / 60_000)));
    try { await closeFamilySession(record.sessionId, outcome, observation, elapsed); await clearActiveSession(); await onFinish(); }
    catch (reason) {
      if (!isNetworkFailure(reason)) { setError(reason instanceof Error ? reason.message : t.closeSaveError); setBusy(false); return; }
      await queueCloseout(record.sessionId, outcome, observation, elapsed); await clearActiveSession(); onOfflineQueued(); await onFinish();
    }
  }
  if (!block) return <main className="fatal"><h1>{t.noBlocks}</h1><button onClick={onFinish}>{t.back}</button></main>;
  return <div className="session-shell">{EVALUATION_MODE && <div className="offline-banner" role="status">{experience.locale === "es-US" ? "Evaluación técnica: contenido sintético, no aprobado para publicación comercial." : "Technical evaluation: synthetic content, not approved for commercial publication."}</div>}<header className="session-header"><button disabled={busy} onClick={exitInterrupted}>← <span>{t.exit}</span></button><div><strong>{experience.title}</strong><small>{t.exactVersion} · {experience.activityVersionId}</small></div><span>{index + 1}/{experience.blocks.length}</span></header><div className="session-progress"><i style={{ width: `${(index + 1) / experience.blocks.length * 100}%` }}/></div><main className="session-main"><div className="session-context"><p className="eyebrow">{t.currentStep}</p><h1>{experience.title}</h1><p>{experience.summary}</p></div><section className="current-block" data-block-id={block.id}>{renderBlock(block, experience.locale)}</section>{error && <p className="error">{error}</p>}<div className="session-actions"><button className="button secondary" disabled={index === 0 || busy} onClick={() => move(index - 1)}>{t.previous}</button><button className="button primary" disabled={busy} onClick={() => atEnd ? setCloseout(true) : move(index + 1)}>{atEnd ? t.closeActivity : t.nextStep}</button></div></main><Companion experience={experience} onExperienceChanged={next => { onExperienceChanged(next); void saveActiveSession(record, next); }}/>{closeout && <div className="family-modal"><section className="closeout-card"><button className="modal-close" onClick={() => setCloseout(false)}>×</button><p className="eyebrow">{t.closeoutKicker}</p><h2>{t.closeoutTitle}</h2><div className="outcome-grid"><button disabled={busy} onClick={() => finish("worked")}><span>✓</span>{t.worked}</button><button disabled={busy} onClick={() => finish("partly")}><span>≈</span>{t.partly}</button><button disabled={busy} onClick={() => finish("not_today")}><span>○</span>{t.notToday}</button></div><label>{t.optionalObservation}<textarea maxLength={300} rows={2} value={observation} onChange={event => setObservation(event.target.value)} placeholder={t.noticed}/></label>{error && <p className="error">{error}</p>}<small>{t.exportDeleteNote}</small></section></div>}</div>;
}

export default function FamilyExperienceApp() {
  const [locale, setLocale] = useState<Locale>(initialLocale);
  const [authenticated, setAuthenticated] = useState(DEMO_MODE);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [overview, setOverview] = useState<FamilyOverview | null>(null);
  const [catalog, setCatalog] = useState<CatalogCard[]>([]);
  const [tab, setTab] = useState<FamilyTab>("today");
  const [challenge, setChallenge] = useState<AdultGateChallenge | null>(null);
  const [selected, setSelected] = useState<CatalogCard | null>(null);
  const [preview, setPreview] = useState<ExperienceView | null>(null);
  const [sessionRecord, setSessionRecord] = useState<FamilySession | null>(null);
  const [lastSessionId, setLastSessionId] = useState<string | undefined>();
  const [experience, setExperience] = useState<ExperienceView | null>(null);
  const [feedback, setFeedback] = useState(false);
  const [onboarding, setOnboarding] = useState(() => new URLSearchParams(location.search).get("onboarding") === "1");
  const [online, setOnline] = useState(() => navigator.onLine);
  const [pendingSync, setPendingSync] = useState(0);
  const t = familyProductCopy[locale];
  const familyId = overview?.family.familyId ?? localStorage.getItem("kids.family_id") ?? (DEMO_MODE ? DEMO_FAMILY_ID : null);

  async function loadFamily(id: string) {
    const next = await getFamilyOverview(id);
    const cards = await getCatalog(next.family.locale);
    setLocale(next.family.locale); setOverview(next); setCatalog(cards);
    document.documentElement.lang = next.family.locale;
    localStorage.setItem("kids.locale", next.family.locale);
    localStorage.setItem("kids.family_id", next.family.familyId);
  }

  useEffect(() => {
    let active = true;
    async function initialize() {
      setLoading(true); setError(null);
      try {
        if (!DEMO_MODE) {
          if (!supabase) throw new Error("Supabase authentication is not configured.");
          const { data } = await supabase.auth.getSession();
          if (!data.session) { if (active) setAuthenticated(false); return; }
          localStorage.setItem("kids.access_token", data.session.access_token);
          if (active) setAuthenticated(true);
        }
        const stored = localStorage.getItem("kids.family_id") ?? (DEMO_MODE ? DEMO_FAMILY_ID : null);
        if (stored) await loadFamily(stored); else if (active) setOnboarding(true);
      } catch (reason) {
        if (active) {
          const message = reason instanceof Error ? reason.message : familyProductCopy[locale].loadTitle;
          if (!DEMO_MODE && /family|404|not found/i.test(message)) setOnboarding(true); else setError(message);
        }
      } finally { if (active) setLoading(false); }
    }
    void initialize();
    const listener = supabase?.auth.onAuthStateChange((_event, value) => {
      if (value) { localStorage.setItem("kids.access_token", value.access_token); setAuthenticated(true); deferAuthStateWork(initialize); }
      else { localStorage.removeItem("kids.access_token"); localStorage.removeItem("kids.family_id"); setAuthenticated(false); setOverview(null); }
    });
    return () => { active = false; listener?.data.subscription.unsubscribe(); };
  }, []);

  useEffect(() => {
    let active = true;
    async function restore() {
      const saved = await loadActiveSession();
      if (active && saved && ["active", "paused"].includes(saved.record.status)) {
        restoreDemoSession(saved.record);
        setSessionRecord(saved.record); setExperience(saved.experience); setLocale(saved.experience.locale);
        document.documentElement.lang = saved.experience.locale;
      }
      if (active) setPendingSync(await pendingOfflineEvents());
    }
    async function becameOnline() {
      setOnline(true);
      const result = await flushOfflineEvents();
      if (active) setPendingSync(result.remaining);
      if (result.synced && familyId) { try { await loadFamily(familyId); } catch { /* retry on the next online event */ } }
    }
    const becameOffline = () => setOnline(false);
    restore();
    window.addEventListener("online", becameOnline);
    window.addEventListener("offline", becameOffline);
    return () => { active = false; window.removeEventListener("online", becameOnline); window.removeEventListener("offline", becameOffline); };
  }, [familyId]);

  const planCards = useMemo(() => overview?.plan?.length ? overview.plan : catalog.slice(0, 3), [overview, catalog]);
  if (!authenticated) return <Login locale={locale}/>;
  if (loading && !overview) return <main className="loading">{t.preparing}</main>;
  if (error && !overview && !onboarding) return <main className="fatal"><h1>{t.loadTitle}</h1><p>{error}</p><button onClick={() => location.reload()}>{t.retry}</button></main>;
  const syncNotice = !online ? t.offlineActive : pendingSync ? `${pendingSync} ${pendingSync === 1 ? t.syncPending : t.syncPendingPlural}` : null;
  async function offlineQueued() { setPendingSync(await pendingOfflineEvents()); }
  if (sessionRecord && experience) return <>{syncNotice && <div className="offline-banner" role="status">{syncNotice}</div>}<Session record={sessionRecord} experience={experience} onRecordChanged={setSessionRecord} onOfflineQueued={offlineQueued} onExperienceChanged={next => {
    if (next.status === "planned") {
      const match = catalog.find(card => card.activityVersionId === next.activityVersionId);
      setSelected(match ? { ...match, plannedActivityId: selected?.plannedActivityId } : null);
      setSessionRecord(null); setExperience(null); setPreview(next);
    } else setExperience(next);
  }} onFinish={async () => { setLastSessionId(sessionRecord.sessionId); setSessionRecord(null); setExperience(null); setTab("journey"); setFeedback(true); if (familyId && navigator.onLine) { try { await loadFamily(familyId); } catch { /* queued state remains visible */ } } }}/></>;
  if (preview && overview) return <>
    <Preparation experience={preview} family={overview.family} onBack={() => { setPreview(null); setSelected(null); setChallenge(null); }} onStart={async () => { if (!familyId) return; setChallenge(await createAdultGate(familyId, overview.family.locale)); }} onExperienceChanged={next => {
      const match = catalog.find(card => card.activityVersionId === next.activityVersionId);
      setSelected(match ? { ...match, plannedActivityId: selected?.plannedActivityId } : selected);
      setPreview(next);
    }}/>
    {challenge && <AdultGate challenge={challenge} locale={locale} onPass={passGate} onClose={() => setChallenge(null)}/>}
  </>;

  async function completeOnboarding(input: SetupInput) { const family = await setupFamily(input); localStorage.setItem("kids.family_id", family.familyId); localStorage.setItem("kids.locale", family.locale); await loadFamily(family.familyId); setOnboarding(false); }
  async function begin(card: CatalogCard) { if (!familyId || !overview) return; setError(null); try { const participants = overview.family.learners.slice(0, Math.min(4, Math.max(1, overview.family.preferences.participants))).map(item => item.learnerId); setSelected(card); setPreview(await createFamilyPreview(familyId, card.activityVersionId, overview.family.locale, participants, card.plannedActivityId)); } catch (reason) { setError(reason instanceof Error ? reason.message : t.previewError); } }
  async function passGate(token: string) { if (!selected || !preview || !overview || !familyId) return; try { const participants = overview.family.learners.slice(0, Math.min(4, Math.max(1, overview.family.preferences.participants))).map(item => item.learnerId); const record = await startFamilySession(familyId, preview.activityVersionId, overview.family.locale, token, participants, selected.plannedActivityId, preview.contextId); const view = await getExperience(record.contextId); await saveActiveSession(record, view); setSessionRecord(record); setExperience(view); setPreview(null); setChallenge(null); } catch (reason) { setError(reason instanceof Error ? reason.message : t.gateError); } }
  const page = !overview ? <div className="family-page"><section className="journey-empty"><h2>{t.completeProfile}</h2></section></div> : tab === "today" ? <Today card={overview.today} explanation={overview.explanation} locale={locale} onStart={begin}/> : tab === "plan" ? <Plan cards={planCards} locale={locale} onStart={begin} onBrowse={() => setTab("explore")}/> : tab === "explore" ? <Explore cards={catalog} locale={locale} onStart={begin}/> : tab === "journey" ? <Journey journey={overview.journey} locale={locale}/> : <FamilySettings family={overview.family} onEdit={() => setOnboarding(true)} onPrivacy={action => requestPrivacyAction(overview.family.familyId, action).then(() => undefined)}/>;
  const nav: Array<[FamilyTab, string, string]> = [["today", "⌂", t.todayNav], ["plan", "▤", t.planNav], ["explore", "◇", t.exploreNav], ["journey", "↗", t.journeyNav], ["family", "○", t.familyNav]];
  return <div className="family-shell">{EVALUATION_MODE && <div className="offline-banner" role="status">{locale === "es-US" ? "Entorno conectado de evaluación: usa datos ficticios y no realices las actividades como guía profesional." : "Connected evaluation environment: use fictional data and do not treat activities as professional guidance."}</div>}{syncNotice && <div className="offline-banner" role="status">{syncNotice}</div>}<FamilyHeader locale={locale} onFeedback={() => setFeedback(true)}/>{error && <div className="app-alert error" role="alert">{error}<button onClick={() => setError(null)}>×</button></div>}<main>{page}</main><nav className="family-nav">{nav.map(([id, icon, label]) => <button className={tab === id ? "active" : ""} key={id} onClick={() => setTab(id)}><i>{icon}</i><span>{label}</span></button>)}</nav>{challenge && <AdultGate challenge={challenge} locale={locale} onPass={passGate} onClose={() => setChallenge(null)}/>} {feedback && familyId && <FeedbackModal familyId={familyId} locale={locale} activityVersionId={selected?.activityVersionId} sessionId={lastSessionId} screen={tab} onClose={() => { setFeedback(false); setLastSessionId(undefined); }}/>} {onboarding && <Onboarding initial={overview?.family} defaultLocale={locale} onDone={completeOnboarding} onClose={overview ? () => setOnboarding(false) : undefined}/>}</div>;
}
