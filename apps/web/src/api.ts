import { demoExperience, demoExperienceFor } from "./demo";
import type { AdultGateChallenge, CatalogCard, CompanionResponse, ExperienceView, FamilyOverview, FamilyProfile, FamilySession, JourneyView, Locale } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
export const DEMO_MODE = import.meta.env.VITE_DEMO_MODE !== "false";
export const EVALUATION_MODE = import.meta.env.VITE_EVALUATION_MODE === "true";
export const DEMO_FAMILY_ID = "00000000-0000-0000-0000-000000000201";
let pendingDemoProposal: { optionId: string; kind: "adaptation" | "replacement" } | null = null;
let pendingDemoContextId: string | null = null;

function headers(): HeadersInit {
  const token = window.localStorage.getItem("kids.access_token");
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, headers: { ...headers(), ...init?.headers } });
  if (response.ok) return response.json() as Promise<T>;
  const body = await response.text();
  if (response.status === 403 && /MFA verification required/i.test(body)) {
    throw new Error("La sesión administrativa ya no tiene MFA válido. Cierra sesión y vuelve a ingresar.");
  }
  let detail = body;
  try {
    const parsed = JSON.parse(body) as { detail?: unknown };
    if (typeof parsed.detail === "string") detail = parsed.detail;
  } catch {
    // Preserve non-JSON upstream responses without hiding their status.
  }
  throw new Error(detail || `Request failed (${response.status})`);
}

export async function getExperience(contextId: string): Promise<ExperienceView> {
  if (DEMO_MODE) {
    const preview = demoPreviews.get(contextId);
    if (preview) return structuredClone(preview);
    const session = demoSessionForContext(contextId);
    if (session) return {
      contextId: session.contextId,
      activityVersionId: session.snapshot.activityVersionId,
      locale: session.snapshot.locale,
      title: session.snapshot.title,
      summary: session.snapshot.summary,
      status: session.status === "interrupted" ? "paused" : session.status,
      currentBlockId: session.currentBlockId,
      blocks: structuredClone(session.snapshot.blocks),
    };
    return demoExperienceFor(demoFamily.locale, demoExperience.activityVersionId, contextId);
  }
  return apiRequest<ExperienceView>(`/v1/experiences/${contextId}`);
}

export async function sendInteraction(contextId: string, message: string, locale: string): Promise<CompanionResponse> {
  if (DEMO_MODE) {
    const lower = message.toLowerCase();
    const spanish = locale === "es-US";
    const version = demoSessionForContext(contextId)?.snapshot.activityVersionId ?? demoPreviews.get(contextId)?.activityVersionId ?? "ACT-0001@1.0.0";
    if (/fuego|fire|enchufe|mains/.test(lower)) return {
      interactionId: crypto.randomUUID(), intent: "troubleshoot", status: "safe_stop",
      answer: spanish ? "Detén la actividad. Esa modificación no está aprobada para esta versión." : "Stop the activity. That change is not approved for this version.",
      safetyStatus: "stop", uncertainty: "low", sources: [], requiresAdultConfirmation: false
    };
    if (/otra actividad|reemplaz|replace/.test(lower)) {
      const optionId = version === "ACT-0002@1.0.0" ? "ACT-0001@1.0.0" : "ACT-0002@1.0.0";
      const card = demoCards(locale as Locale).find(item => item.activityVersionId === optionId)!;
      pendingDemoProposal = { optionId, kind: "replacement" };
      pendingDemoContextId = contextId;
      return {
        interactionId: crypto.randomUUID(), intent: "replace_planned_activity", status: "proposal",
        answer: spanish ? "Puedo preparar otra actividad publicada. La sesión actual se interrumpirá si ya comenzó." : "I can prepare another published activity. The current session will be interrupted if it already started.",
        safetyStatus: "needs_confirmation", uncertainty: "low", sources: [{ chunkId: `${optionId}-card`, activityVersionId: optionId, label: spanish ? "Alternativa publicada" : "Published alternative" }],
        proposal: { proposalId: crypto.randomUUID(), kind: "replacement", options: [{ optionId, summary: card.title, visibleChanges: [card.summary] }] },
        requiresAdultConfirmation: true
      };
    }
    if (/adapt|cambiar|menos tiempo|shorter/.test(lower)) {
      pendingDemoProposal = { optionId: "shorter-approved", kind: "adaptation" };
      pendingDemoContextId = contextId;
      return {
        interactionId: crypto.randomUUID(), intent: "adapt_current_activity", status: "proposal",
        answer: spanish ? "Puedo aplicar una versión corta ya revisada. Revisa el cambio antes de confirmarlo." : "I can apply a reviewed shorter version. Check the visible change before confirming it.",
        safetyStatus: "needs_confirmation", uncertainty: "low", sources: [{ chunkId: `${version}-step-1`, activityVersionId: version, label: spanish ? "Opción publicada" : "Published activity option" }],
        proposal: { proposalId: crypto.randomUUID(), kind: "adaptation", options: [{ optionId: "shorter-approved", summary: spanish ? "Prueba corta" : "Short test", visibleChanges: [spanish ? "Un ciclo de prueba" : "One test cycle", spanish ? "Mismas reglas de seguridad" : "Same safety rules"] }] },
        requiresAdultConfirmation: true
      };
    }
    return {
      interactionId: crypto.randomUUID(), intent: "troubleshoot", status: "answer",
      answer: spanish ? "Vuelve al paso visible, mantén los soportes a la misma distancia y prueba con una sola pieza cada vez." : "Return to the visible step, keep the supports the same distance apart, and test one piece at a time.",
      safetyStatus: "safe", uncertainty: "low", sources: [{ chunkId: `${version}-step-1`, activityVersionId: version, label: spanish ? "Paso publicado actual" : "Current published step" }], requiresAdultConfirmation: false
    };
  }
  return apiRequest<CompanionResponse>("/v1/companion/interactions", {
    method: "POST",
    body: JSON.stringify({ contextId, message, locale })
  });
}

export async function decideProposal(proposalId: string, decision: "confirm" | "reject", optionId?: string): Promise<ExperienceView> {
  if (DEMO_MODE) {
    const contextId = pendingDemoContextId;
    const pending = pendingDemoProposal;
    const record = contextId ? demoSessionForContext(contextId) : undefined;
    const preview = contextId ? demoPreviews.get(contextId) : undefined;
    let updated = contextId ? await getExperience(contextId) : demoExperienceFor(demoFamily.locale);
    if (decision === "confirm" && optionId === pending?.optionId && pending?.kind === "replacement") {
      if (record) {
        record.status = "interrupted";
        demoSessions.set(record.sessionId, record);
        const replacementContextId = crypto.randomUUID();
        updated = { ...demoExperienceFor(updated.locale, optionId, replacementContextId), status: "planned" };
        demoPreviews.set(replacementContextId, structuredClone(updated));
      } else {
        updated = { ...demoExperienceFor(updated.locale, optionId, updated.contextId), status: "planned" };
        demoPreviews.set(updated.contextId, structuredClone(updated));
      }
    } else if (decision === "confirm" && optionId === pending?.optionId) {
      updated.summary = updated.locale === "es-US" ? "Una versión corta y revisada con los mismos controles de seguridad." : "A shorter, reviewed version with the same safety controls.";
      updated.blocks = updated.blocks.slice(0, 2);
      if (record) {
        record.snapshot.summary = updated.summary;
        record.snapshot.blocks = structuredClone(updated.blocks);
        demoSessions.set(record.sessionId, record);
      }
      if (preview) demoPreviews.set(preview.contextId, structuredClone(updated));
    }
    pendingDemoProposal = null;
    pendingDemoContextId = null;
    return updated;
  }
  return apiRequest<ExperienceView>(`/v1/companion/proposals/${proposalId}/decision`, {
    method: "POST",
    headers: { "Idempotency-Key": crypto.randomUUID() },
    body: JSON.stringify({ decision, optionId })
  });
}

const demoCardsEs: CatalogCard[] = [
  { activityVersionId: "ACT-0001@1.0.0", title: "Puente de papel", summary: "Construyan, prueben y mejoren un puente de papel usando la misma carga.", minutes: 30, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0002@1.0.0", title: "Clasificador de semillas", summary: "Creen una regla para clasificar semillas y expliquen las excepciones.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0003@1.0.0", title: "Probador de conductividad", summary: "Comparen objetos aprobados en un circuito de bajo voltaje controlado por un adulto.", minutes: 30, age: [8, 10], participants: [1, 3], risk: "C", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0004@1.0.0", title: "Aerodeslizador con CD y globo", summary: "Investiguen cómo el aire que escapa cambia la fricción.", minutes: 25, age: [7, 10], participants: [1, 3], risk: "B", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0005@1.0.0", title: "Transportador de agua", summary: "Diseñen una forma de mover agua midiendo derrames y resultados.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "medium", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0006@1.0.0", title: "Torre con límite de materiales", summary: "Construyan la torre estable más alta usando una cantidad fija de materiales.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0007@1.0.0", title: "Mensaje de electricidad estática", summary: "Usen carga estática para mover piezas livianas y revelar un patrón.", minutes: 20, age: [6, 10], participants: [1, 3], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0008@1.0.0", title: "Barco de carga", summary: "Construyan un barco de aluminio y mejoren la carga que soporta sin hundirse.", minutes: 30, age: [5, 10], participants: [1, 4], risk: "A", mess: "medium", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0009@1.0.0", title: "Polea de cartón", summary: "Construyan un sistema de rueda guiada y comparen dirección y esfuerzo.", minutes: 30, age: [7, 10], participants: [1, 3], risk: "B", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0010@1.0.0", title: "Comparación de germinación", summary: "Comparen cómo una condición controlada afecta la germinación durante varios días.", minutes: 20, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0011@1.0.0", title: "Detectives de disolución", summary: "Comparen sólidos domésticos aprobados en agua usando siempre la misma prueba.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0012@1.0.0", title: "Constrúyelo con mis palabras", summary: "Practiquen comunicación precisa describiendo una construcción que otra persona no ve.", minutes: 20, age: [5, 10], participants: [2, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true },
  { activityVersionId: "ACT-0013@1.0.0", title: "Diseñadores de caminos de equilibrio", summary: "Diseñen, prueben y revisen un recorrido de movimiento seguro a nivel del suelo.", minutes: 15, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "es-US", exactVersion: true }
];
const demoCardsEn: CatalogCard[] = [
  { activityVersionId: "ACT-0001@1.0.0", title: "Paper Bridge", summary: "Build, test, and improve a paper bridge using the same load.", minutes: 30, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0002@1.0.0", title: "Seed Sorter", summary: "Create a rule for sorting seeds and explain the exceptions.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0003@1.0.0", title: "Conductivity Tester", summary: "Compare approved objects in an adult-controlled, low-voltage circuit.", minutes: 30, age: [8, 10], participants: [1, 3], risk: "C", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0004@1.0.0", title: "CD and Balloon Hovercraft", summary: "Investigate how escaping air changes friction.", minutes: 25, age: [7, 10], participants: [1, 3], risk: "B", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0005@1.0.0", title: "Water Transporter", summary: "Design a way to move water while measuring spills and results.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "medium", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0006@1.0.0", title: "Tower with a Material Limit", summary: "Build the tallest stable tower using a fixed quantity of materials.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0007@1.0.0", title: "Static Electricity Message", summary: "Use static charge to move lightweight pieces and reveal a pattern.", minutes: 20, age: [6, 10], participants: [1, 3], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0008@1.0.0", title: "Cargo Ship", summary: "Build a foil boat and improve the load it carries without sinking.", minutes: 30, age: [5, 10], participants: [1, 4], risk: "A", mess: "medium", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0009@1.0.0", title: "Cardboard Pulley", summary: "Build a guided wheel system and compare pulling direction and effort.", minutes: 30, age: [7, 10], participants: [1, 3], risk: "B", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0010@1.0.0", title: "Germination Comparison", summary: "Compare how one controlled condition affects germination over several days.", minutes: 20, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0011@1.0.0", title: "Dissolving Detective", summary: "Compare approved household solids in water using the same test each time.", minutes: 25, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0012@1.0.0", title: "Build It From My Words", summary: "Practice precise communication by describing a structure another person cannot see.", minutes: 20, age: [5, 10], participants: [2, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
  { activityVersionId: "ACT-0013@1.0.0", title: "Balance Path Designer", summary: "Design, test, and revise a safe floor-level movement path.", minutes: 15, age: [5, 10], participants: [1, 4], risk: "A", mess: "low", locale: "en-US", exactVersion: true },
];

function demoCards(locale: Locale): CatalogCard[] {
  // Family surfaces fail closed. Risk C/D versions remain visible to the
  // editorial workspace, but never enter the family demo without their gates.
  return structuredClone(locale === "es-US" ? demoCardsEs : demoCardsEn)
    .filter(card => card.risk === "A" || card.risk === "B");
}

let demoFamily: FamilyProfile = {
  familyId: DEMO_FAMILY_ID, familyName: "Familia piloto", stateCode: "FL", locale: "es-US", units: "metric", timezone: "America/New_York",
  learners: [{ learnerId: "00000000-0000-0000-0000-000000000211", alias: "Explorer 1", ageBand: "5-6" }, { learnerId: "00000000-0000-0000-0000-000000000212", alias: "Builder 2", ageBand: "7-8" }],
  preferences: { participants: 2, minutes: 30, mess: "low" }, consent: { adultLed: true, acceptedAt: new Date().toISOString() }
};
const demoSessions = new Map<string, FamilySession>();
const demoPreviews = new Map<string, ExperienceView>();

/** Rehydrates only the in-browser demo ledger after an encrypted offline reload. */
export function restoreDemoSession(record: FamilySession): void {
  if (DEMO_MODE) demoSessions.set(record.sessionId, structuredClone(record));
}

function demoSessionForContext(contextId: string): FamilySession | undefined {
  return [...demoSessions.values()].find(session => session.contextId === contextId);
}

function demoJourney(): JourneyView {
  const complete = [...demoSessions.values()].filter(session => session.status === "completed" && session.closeout);
  return {
    completed: complete.length,
    observations: complete.slice(-10).map(session => ({ sessionId: session.sessionId, activityVersionId: session.snapshot.activityVersionId, ...(session.closeout ?? {}) })),
    language: "observations_not_scores"
  };
}

function demoOverview(): FamilyOverview {
  const cards = demoCards(demoFamily.locale);
  return {
    family: structuredClone(demoFamily),
    today: cards[0], plan: cards.map((card, index) => ({ ...card, day: ["today", "next", "weekend"][index] })),
    journey: demoJourney(), explanation: demoFamily.locale === "es-US" ? ["Edad compatible", "Cabe en el tiempo elegido", "Materiales domésticos publicados"] : ["Matches the age bands", "Fits the selected time", "Published household materials"]
  };
}

export async function setupFamily(input: { familyName: string; stateCode: string; locale: Locale; units: "metric" | "us_customary"; timezone: string; learnerAliases: string[]; ageBands: Array<"5-6" | "7-8" | "9-10">; learnerIds?: Array<string | null>; removedLearnerIds?: string[]; participants: number; minutes: number; mess: "low" | "medium" | "high" }): Promise<FamilyOverview["family"]> {
  if (DEMO_MODE) {
    const current = new Map(demoFamily.learners.map(learner => [learner.learnerId, learner]));
    demoFamily = {
      familyId: DEMO_FAMILY_ID, familyName: input.familyName.trim(), stateCode: input.stateCode, locale: input.locale, units: input.units, timezone: input.timezone,
      learners: input.learnerAliases.map((alias, index) => {
        const requestedId = input.learnerIds?.[index] ?? null;
        const learnerId = requestedId && current.has(requestedId) ? requestedId : crypto.randomUUID();
        return { learnerId, alias: alias.trim(), ageBand: input.ageBands[index] };
      }),
      preferences: { participants: input.participants, minutes: input.minutes, mess: input.mess },
      consent: demoFamily.consent
    };
    return structuredClone(demoFamily);
  }
  return apiRequest<FamilyOverview["family"]>("/v1/families/setup", { method: "POST", body: JSON.stringify(input) });
}

export async function getFamilyOverview(familyId: string): Promise<FamilyOverview> {
  if (DEMO_MODE) return demoOverview();
  return apiRequest<FamilyOverview>(`/v1/families/${familyId}/overview`);
}

export async function getCatalog(locale: Locale): Promise<CatalogCard[]> {
  if (DEMO_MODE) return demoCards(locale);
  return apiRequest<CatalogCard[]>(`/v1/catalog?locale=${encodeURIComponent(locale)}`);
}

export async function createAdultGate(familyId: string, locale: Locale): Promise<AdultGateChallenge> {
  if (DEMO_MODE) return { challengeId: crypto.randomUUID(), purpose: "adult_friction_not_age_verification", prompts: locale === "es-US" ? [{ word: "cuatro", options: [3, 4, 7] }, { word: "siete", options: [6, 7, 9] }, { word: "dos", options: [2, 5, 8] }] : [{ word: "four", options: [3, 4, 7] }, { word: "seven", options: [6, 7, 9] }, { word: "two", options: [2, 5, 8] }], expiresInSeconds: 300 };
  return apiRequest<AdultGateChallenge>(`/v1/families/${familyId}/adult-gate?locale=${locale}`, { method: "POST" });
}

export async function verifyAdultGate(challengeId: string, answers: number[]): Promise<{ adultGateToken: string; expiresAt: string; legalAgeVerified: false }> {
  if (DEMO_MODE) return { adultGateToken: "demo-adult-gate-token-long-enough", expiresAt: new Date(Date.now() + 900_000).toISOString(), legalAgeVerified: false };
  return apiRequest("/v1/adult-gate/verify", { method: "POST", body: JSON.stringify({ challengeId, answers }) });
}

export async function createFamilyPreview(familyId: string, activityVersionId: string, locale: Locale, participantIds: string[], plannedActivityId?: string): Promise<ExperienceView> {
  if (DEMO_MODE) {
    const contextId = crypto.randomUUID();
    const preview = { ...demoExperienceFor(locale, activityVersionId, contextId), status: "planned" as const };
    demoPreviews.set(contextId, structuredClone(preview));
    return preview;
  }
  return apiRequest<ExperienceView>(`/v1/families/${familyId}/previews`, {
    method: "POST",
    body: JSON.stringify({ activityVersionId, locale, participantIds, plannedActivityId })
  });
}

export async function startFamilySession(familyId: string, activityVersionId: string, locale: Locale, adultGateToken: string, participantIds: string[], plannedActivityId?: string, previewContextId?: string): Promise<FamilySession> {
  if (DEMO_MODE) {
    const sessionId = crypto.randomUUID(), now = new Date().toISOString();
    const prepared = previewContextId ? demoPreviews.get(previewContextId) : undefined;
    if (previewContextId && (!prepared || prepared.activityVersionId !== activityVersionId || prepared.locale !== locale)) throw new Error("Prepared activity is unavailable");
    const view = prepared ?? demoExperienceFor(locale, activityVersionId, sessionId);
    const contextId = previewContextId ?? sessionId;
    const record = { sessionId, contextId, familyId, plannedActivityId: plannedActivityId ?? null, status: "active", currentBlockId: view.currentBlockId, snapshot: { activityVersionId, locale, title: view.title, summary: view.summary, blocks: structuredClone(view.blocks) }, participantIds, startedAt: now, updatedAt: now, closeout: null } as FamilySession;
    demoSessions.set(sessionId, record);
    if (previewContextId) demoPreviews.delete(previewContextId);
    return structuredClone(record);
  }
  return apiRequest<FamilySession>(`/v1/families/${familyId}/sessions`, { method: "POST", body: JSON.stringify({ activityVersionId, locale, adultGateToken, participantIds, plannedActivityId, previewContextId }) });
}

export async function updateSessionProgress(sessionId: string, blockId: string, status: "active" | "paused" | "completed" | "interrupted"): Promise<FamilySession> {
  if (DEMO_MODE) {
    if (!navigator.onLine) throw new TypeError("Failed to fetch");
    const record = demoSessions.get(sessionId);
    if (!record) throw new Error("Demo session not found");
    const updated = { ...record, currentBlockId: blockId, status, updatedAt: new Date().toISOString() } as FamilySession;
    demoSessions.set(sessionId, updated);
    return structuredClone(updated);
  }
  return apiRequest<FamilySession>(`/v1/sessions/${sessionId}/progress`, { method: "PUT", body: JSON.stringify({ blockId, status }) });
}

export async function closeFamilySession(sessionId: string, outcome: "worked" | "partly" | "not_today", observation: string, durationMinutes: number): Promise<FamilySession> {
  if (DEMO_MODE) {
    if (!navigator.onLine) throw new TypeError("Failed to fetch");
    const record = demoSessions.get(sessionId);
    if (!record) throw new Error("Demo session not found");
    const updated = { ...record, status: "completed", updatedAt: new Date().toISOString(), closeout: { outcome, observation, durationMinutes, recordedAt: new Date().toISOString() } } as FamilySession;
    demoSessions.set(sessionId, updated);
    return structuredClone(updated);
  }
  return apiRequest<FamilySession>(`/v1/sessions/${sessionId}/closeout`, { method: "POST", body: JSON.stringify({ outcome, observation, durationMinutes }) });
}

export async function getJourney(familyId: string): Promise<JourneyView> {
  if (DEMO_MODE) return demoJourney();
  return apiRequest<JourneyView>(`/v1/families/${familyId}/journey`);
}

export async function sendFamilyFeedback(familyId: string, input: { useful: boolean; comment: string; category: "product" | "content" | "error" | "safety" | "privacy"; activityVersionId?: string; sessionId?: string; screen: string; locale: Locale; appVersion: string; browserFamily: string; journeyState: string }): Promise<Record<string, unknown>> {
  if (DEMO_MODE) return { feedbackId: crypto.randomUUID(), rawStored: false, redactedComment: input.comment, createdAt: new Date().toISOString() };
  return apiRequest(`/v1/families/${familyId}/feedback`, { method: "POST", body: JSON.stringify(input) });
}

export async function requestPrivacyAction(familyId: string, action: "export" | "delete"): Promise<Record<string, unknown>> {
  if (DEMO_MODE) return { requestId: crypto.randomUUID(), action, state: "queued", requestedAt: new Date().toISOString() };
  return apiRequest(`/v1/families/${familyId}/privacy-requests`, { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() }, body: JSON.stringify({ action }) });
}
