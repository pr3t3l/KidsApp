import type { ExperienceView, Locale } from "./types";

export const DEMO_CONTEXT_ID = "00000000-0000-0000-0000-000000000101";

const activityCopy: Record<string, Record<Locale, { title: string; summary: string; instruction: string; question: string }>> = {
  "ACT-0001@1.0.0": {
    "en-US": { title: "Paper Bridge", summary: "Build, test, and improve a paper bridge using the same load each time.", instruction: "Place one sheet across two supports. Center the empty cup, then add one crayon at a time.", question: "What changed in the paper just before the bridge failed?" },
    "es-US": { title: "Puente de papel", summary: "Construyan, prueben y mejoren un puente de papel usando siempre la misma carga.", instruction: "Coloca una hoja sobre dos apoyos. Centra el vaso vacío y añade un crayón a la vez.", question: "¿Qué cambió en el papel justo antes de que fallara el puente?" },
  },
  "ACT-0002@1.0.0": {
    "en-US": { title: "Seed Sorter", summary: "Invent a sorting rule, test it, and explain what belongs together.", instruction: "Choose one visible property, sort the seeds, and test every seed against the same rule.", question: "Which seed was hardest to classify, and why?" },
    "es-US": { title: "Clasificador de semillas", summary: "Inventen una regla de clasificación, pruébenla y expliquen qué pertenece a cada grupo.", instruction: "Elige una propiedad visible, clasifica las semillas y prueba cada una con la misma regla.", question: "¿Qué semilla fue más difícil de clasificar y por qué?" },
  },
  "ACT-0005@1.0.0": {
    "en-US": { title: "Water Transporter", summary: "Test tools that move water while keeping the comparison fair.", instruction: "Move the same starting amount with one tool at a time and keep each trial the same length.", question: "Which tool moved the most water with the least spill?" },
    "es-US": { title: "Transportador de agua", summary: "Prueben herramientas para mover agua manteniendo una comparación justa.", instruction: "Mueve la misma cantidad inicial con una herramienta a la vez y usa el mismo tiempo en cada prueba.", question: "¿Qué herramienta movió más agua con menos derrame?" },
  },
};

export function demoExperienceFor(locale: Locale, activityVersionId = "ACT-0001@1.0.0", contextId = DEMO_CONTEXT_ID): ExperienceView {
  const selected = activityCopy[activityVersionId] ?? activityCopy["ACT-0001@1.0.0"];
  const content = selected[locale];
  const spanish = locale === "es-US";
  return {
    contextId,
    activityVersionId,
    locale,
    title: content.title,
    summary: content.summary,
    status: "active",
    currentBlockId: "safety-1",
    blocks: [
      { id: "safety-1", kind: "safety_notice", version: 1, required: true, data: { title: spanish ? "Revisión del adulto" : "Adult check", text: spanish ? "Usa solo los materiales indicados, mantén el área despejada y detén la actividad ante cualquier duda." : "Use only the listed materials, keep the area clear, and stop whenever safety is uncertain." } },
      { id: "instruction-1", kind: "instruction", version: 1, required: true, data: { eyebrow: spanish ? "Descubrir · 6 min" : "Discover · 6 min", title: spanish ? "Haz una prueba comparable" : "Run one comparable test", text: content.instruction } },
      { id: "question-1", kind: "question", version: 1, required: false, data: { prompt: content.question } },
    ],
  };
}

export const demoExperience = demoExperienceFor("en-US");
