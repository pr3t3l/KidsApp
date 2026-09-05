export type Locale = "en-US" | "es-US";
export type ExperienceStatus = "planned" | "active" | "paused" | "completed" | "cancelled";
export type CompanionIntent = "troubleshoot" | "adapt_current_activity" | "replace_planned_activity";

export type ContentBlock = {
  id: string;
  type: "instruction" | "safety_notice" | "timer" | "question" | "choice" | "evidence" | "result";
  required: boolean;
  payload: Record<string, unknown>;
};

export type ExperienceView = {
  contextId: string;
  activityVersionId: string;
  locale: Locale;
  title: string;
  summary: string;
  status: ExperienceStatus;
  currentBlockId: string | null;
  blocks: ContentBlock[];
};

export type CompanionProposal = {
  proposalId: string;
  kind: "adaptation" | "replacement";
  options: Array<{ optionId: string; summary: string; visibleChanges: string[] }>;
};

export type CompanionResponse = {
  interactionId: string;
  intent: CompanionIntent;
  status: "answer" | "proposal" | "clarification" | "safe_stop";
  answer: string;
  safetyStatus: "safe" | "needs_confirmation" | "stop";
  uncertainty: "low" | "medium" | "high";
  sources: Array<{ chunkId: string; activityVersionId: string; label: string }>;
  proposal?: CompanionProposal | null;
  requiresAdultConfirmation: boolean;
};
