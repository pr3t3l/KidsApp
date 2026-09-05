import type { ExperienceView } from "./types";

export const DEMO_CONTEXT_ID = "00000000-0000-0000-0000-000000000101";

export const demoExperience: ExperienceView = {
  contextId: DEMO_CONTEXT_ID,
  activityVersionId: "ACT-0001@1.0.0",
  locale: "en-US",
  title: "Paper Bridge",
  summary: "Build, test, and improve a paper bridge using the same load each time.",
  status: "active",
  currentBlockId: "safety-1",
  blocks: [
    {
      id: "safety-1",
      type: "safety_notice",
      required: true,
      payload: {
        title: "Adult check",
        text: "Keep hands and faces away from beneath the bridge. The adult positions the supports and cup."
      }
    },
    {
      id: "instruction-1",
      type: "instruction",
      required: true,
      payload: {
        eyebrow: "Discover · 6 min",
        title: "Test a flat sheet first",
        text: "Place one sheet across the two supports. Center the empty cup, then add one crayon at a time and count the last stable load."
      }
    },
    {
      id: "question-1",
      type: "question",
      required: false,
      payload: {
        prompt: "What changed in the paper just before the bridge failed?"
      }
    }
  ]
};
