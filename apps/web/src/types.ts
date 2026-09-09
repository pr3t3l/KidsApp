export type Locale = "en-US" | "es-US";
export type ExperienceStatus = "planned" | "active" | "paused" | "completed" | "cancelled";
export type CompanionIntent = "troubleshoot" | "adapt_current_activity" | "replace_planned_activity";

export type BlockKind = "prep" | "purpose" | "safety" | "safety_notice" | "contribution" | "instruction" | "timer" | "question" | "choice" | "evidence" | "result" | "closeout";

export type LegacyContentBlock = {
  id: string;
  type: BlockKind;
  required: boolean;
  payload: Record<string, unknown>;
};

export type VersionedContentBlock = {
  id: string;
  kind: BlockKind;
  version: number;
  required: boolean;
  data: Record<string, unknown>;
};

export type ContentBlock = LegacyContentBlock | VersionedContentBlock;

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

export type CatalogCard = {
  activityVersionId: string;
  plannedActivityId?: string;
  scheduledOn?: string;
  planState?: string;
  title: string;
  summary: string;
  minutes: number;
  age: [number, number];
  participants: [number, number];
  risk: "A" | "B" | "C" | "D";
  mess: "low" | "medium" | "high";
  locale?: Locale;
  exactVersion?: boolean;
};

export type LearnerProfile = { learnerId: string; alias: string; ageBand: "5-6" | "7-8" | "9-10" };

export type FamilyProfile = {
  familyId: string;
  familyName?: string;
  stateCode?: string;
  locale: Locale;
  units: "metric" | "us_customary";
  timezone: string;
  learners: LearnerProfile[];
  preferences: { participants: number; minutes: number; mess: "low" | "medium" | "high" };
  consent: { adultLed: boolean; acceptedAt: string };
};

export type JourneyView = {
  completed: number;
  observations: Array<{ sessionId?: string; activityVersionId?: string; outcome?: string; observation?: string; durationMinutes?: number; recordedAt?: string }>;
  language: "observations_not_scores";
};

export type FamilyOverview = {
  family: FamilyProfile;
  today: CatalogCard | null;
  plan: Array<CatalogCard & { day: string }>;
  journey: JourneyView;
  explanation: string[];
};

export type AdultGateChallenge = {
  challengeId: string;
  purpose: "adult_friction_not_age_verification";
  prompts: Array<{ word: string; options: number[] }>;
  expiresInSeconds: number;
};

export type FamilySession = {
  sessionId: string;
  contextId: string;
  familyId: string;
  plannedActivityId?: string | null;
  status: ExperienceStatus | "interrupted";
  currentBlockId: string | null;
  snapshot: { activityVersionId: string; locale: Locale; title: string; summary: string; blocks: ContentBlock[] };
  participantIds?: string[];
  startedAt: string;
  updatedAt: string;
  closeout: Record<string, unknown> | null;
};
