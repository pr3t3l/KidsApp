import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const V2_LOCALES = ["en-US", "es-US"];

const valueFor = (value, locale) => {
  if (value == null) return "";
  if (typeof value === "string") return value;
  return typeof value[locale] === "string" ? value[locale] : "";
};

const nonEmpty = (value) => typeof value === "string" && value.trim().length > 0;
const compact = (value) => Object.fromEntries(Object.entries(value).filter(([, item]) => item !== undefined && item !== null && item !== ""));
const ids = (prefix, values) => values.map((_, index) => `${prefix}-${index + 1}`);

function migrateCore(v1) {
  const allStepIds = v1.steps.map((step) => step.stepId);
  return {
    schema: "activity@2",
    id: v1.activityId,
    version: v1.version,
    sourceLocale: "en-US",
    state: v1.status,
    fit: {
      age: [v1.ageRange.minimumYears, v1.ageRange.maximumYears],
      levels: v1.levels,
      group: { min: v1.participants.minimum, max: v1.participants.maximum, sizes: v1.participants.supportedCounts },
      time: {
        min: v1.timing.totalMinutesMin,
        max: v1.timing.totalMinutesMax,
        prep: v1.timing.adultPrepMinutes,
        clean: v1.timing.cleanupMinutes,
      },
      mess: v1.environment.messLevel,
      spaces: v1.environment.spaces,
      offline: v1.environment.offlineCapable,
    },
    learn: {
      primary: v1.learning.primaryArea,
      secondary: v1.learning.secondaryAreas,
      concepts: v1.learning.concepts.map((item) => item.conceptId),
      skills: v1.learning.skills.map((item) => item.skillId),
      cycle: v1.learning.cycleStages,
      guidance: v1.objectiveGuidance.map((item) => ({
        skill: item.skillId,
        age: [item.startingAgeRange.minimumYears, item.startingAgeRange.maximumYears],
        intent: item.intent,
      })),
    },
    materials: v1.materials.map((item) => ({
      id: item.materialId,
      quantity: item.quantity,
      unit: item.unit,
      required: item.required,
      reusable: !item.consumable,
      substitutes: item.approvedSubstitutions.map((substitute) => ({
        id: substitute.substitutionId,
        quantity: substitute.quantity,
        unit: substitute.unit,
        safety: substitute.safetyImpact,
      })),
    })),
    flow: {
      mode: v1.experienceNarrative.mode,
      start: v1.experienceNarrative.startingStateId,
      end: v1.experienceNarrative.endingStateId,
      states: v1.experienceNarrative.states.map((state) => state.stateId),
      materialFunctions: v1.experienceNarrative.materialFunctions.map((item) => ({ material: item.materialId, firstStep: item.introducedAtStepId })),
      participantCycle: {
        policy: v1.experienceNarrative.participantCycle.completionPolicy,
        actions: v1.experienceNarrative.participantCycle.requiredActions,
      },
      roles: v1.roleTemplates.map((role) => ({
        id: role.roleTemplateId,
        levels: role.compatibleLevels,
        primarySkills: role.eligiblePrimarySkillIds,
        skills: role.exposureSkillIds,
        concepts: role.exposureConceptIds,
        allowedSteps: role.allowedStepIds,
        restrictedSteps: role.restrictedStepIds,
      })),
      groups: v1.groupConfigurations.map((group) => ({ size: group.participantCount, roles: group.roleTemplateIds })),
      steps: v1.steps.map((step) => ({
        id: step.stepId,
        stage: step.stage,
        actor: step.actor,
        entry: step.entryStateId,
        exit: step.exitStateId,
        minutes: step.minutes,
        adultActionIds: ids(`${step.stepId}-ADULT`, step.adultActions),
        promptIds: ids(`${step.stepId}-PROMPT`, step.facilitatorPrompts),
        participantActions: step.participantActionTemplates.map((action) => ({
          id: action.actionTemplateId,
          audience: action.audience,
          roles: action.roleTemplateIds,
          turn: action.turnOrder,
        })),
        cycle: step.cycleActions,
        materialIds: step.materialUses.map((use) => use.materialId),
        hasDecision: step.childDecision != null,
        cues: step.observationCues.map((cue) => ({ id: cue.cueId, skill: cue.skillId })),
        visualIds: step.visualBriefIds,
        skills: step.exposureSkillIds,
        concepts: step.exposureConceptIds,
      })),
    },
    safety: {
      level: v1.safety.participationLevel,
      hazards: v1.safety.hazards.map((hazard) => ({
        id: hazard.hazardId,
        category: hazard.category,
        controlIds: ids(`${hazard.hazardId}-CONTROL`, hazard.controls),
        steps: allStepIds,
      })),
      adultOnlySteps: v1.safety.adultOnlyStepIds,
      stopIds: ids("STOP", v1.safety.stopConditions),
      prohibitedIds: ids("PROHIBITED", v1.safety.prohibitedAdaptations),
    },
    adaptations: v1.adaptations.map((item) => ({
      id: item.adaptationId,
      type: item.type,
      safety: item.safetyImpact,
      adultConfirm: item.requiresAdultConfirmation,
    })),
    closeout: v1.observationPrompts.map((item) => ({ skill: item.skillId })),
  };
}

function migrateLocale(v1, locale) {
  const base = v1.locales[locale];
  if (!base) throw new Error(`Missing required locale ${locale}`);
  return {
    schema: "activity-locale@2",
    activityId: v1.activityId,
    version: v1.version,
    locale,
    content: {
      title: base.title,
      summary: base.summary,
      openingQuestion: base.openingQuestion,
      adultBrief: base.adultBriefExplanation,
      adultDetail: base.adultDetailedExplanation,
      childExplanation: base.childExplanation,
      reflections: base.reflectionQuestions,
    },
    learn: {
      goal: valueFor(v1.learning.experienceGoal, locale),
      method: valueFor(v1.learning.learningMechanism, locale),
      concepts: v1.learning.concepts.map((item) => ({ id: item.conceptId, name: valueFor(item.name, locale) })),
      skills: v1.learning.skills.map((item) => ({
        id: item.skillId,
        name: valueFor(item.name, locale),
        evidence: item.observableActions.map((entry) => valueFor(entry, locale)),
        nonEvidence: item.nonEvidence.map((entry) => valueFor(entry, locale)),
      })),
      decisions: v1.learning.childDecisions.map((entry) => valueFor(entry, locale)),
      lookFors: v1.learning.adultLookFors.map((entry) => valueFor(entry, locale)),
      guidance: v1.objectiveGuidance.map((item) => ({
        skill: item.skillId,
        rationale: valueFor(item.rationale, locale),
        simplify: valueFor(item.simplification, locale),
        extend: valueFor(item.extension, locale),
      })),
    },
    materials: v1.materials.map((item) => ({
      id: item.materialId,
      name: valueFor(item.name, locale),
      prep: valueFor(item.adultPreparation, locale),
      safety: valueFor(item.safetyNotes, locale),
      substitutes: item.approvedSubstitutions.map((substitute) => ({
        id: substitute.substitutionId,
        name: valueFor(substitute.name, locale),
        conditions: valueFor(substitute.conditions, locale),
        rationale: valueFor(substitute.rationale, locale),
      })),
    })),
    flow: {
      states: v1.experienceNarrative.states.map((state) => ({ id: state.stateId, text: valueFor(state.description, locale) })),
      materialFunctions: v1.experienceNarrative.materialFunctions.map((item) => ({ material: item.materialId, purpose: valueFor(item.purpose, locale) })),
      roles: v1.roleTemplates.map((role) => ({
        id: role.roleTemplateId,
        name: valueFor(role.name, locale),
        contribution: valueFor(role.contribution, locale),
        responsibilities: role.responsibilities.map((entry) => valueFor(entry, locale)),
      })),
      groups: v1.groupConfigurations.map((group) => ({ size: group.participantCount, notes: valueFor(group.notes, locale) })),
      steps: v1.steps.map((step) => compact({
        id: step.stepId,
        title: valueFor(step.title, locale),
        purpose: valueFor(step.learningPurpose, locale),
        transition: valueFor(step.transitionReason, locale),
        instruction: valueFor(step.instruction, locale),
        adultActions: step.adultActions.map((entry, index) => ({ id: `${step.stepId}-ADULT-${index + 1}`, text: valueFor(entry, locale) })),
        prompts: step.facilitatorPrompts.map((entry, index) => ({ id: `${step.stepId}-PROMPT-${index + 1}`, text: valueFor(entry, locale) })),
        participantActions: step.participantActionTemplates.map((action) => ({ id: action.actionTemplateId, text: valueFor(action.action, locale) })),
        materialUses: step.materialUses.map((use) => ({ material: use.materialId, purpose: valueFor(use.purpose, locale) })),
        decision: valueFor(step.childDecision, locale) || undefined,
        cues: step.observationCues.map((cue) => ({ id: cue.cueId, behavior: valueFor(cue.behavior, locale), doNotInfer: valueFor(cue.doNotInfer, locale) })),
        result: valueFor(step.expectedResult, locale),
        success: valueFor(step.successSignal, locale),
        problems: step.commonProblems.map((problem) => ({ problem: valueFor(problem.problem, locale), safeResponse: valueFor(problem.safeResponse, locale) })),
        warning: valueFor(step.warning, locale) || undefined,
        resume: valueFor(step.resumeInstruction, locale),
      })),
    },
    safety: {
      supervision: valueFor(v1.safety.supervision, locale),
      hazards: v1.safety.hazards.map((hazard) => ({
        id: hazard.hazardId,
        description: valueFor(hazard.description, locale),
        controls: hazard.controls.map((control, index) => ({ id: `${hazard.hazardId}-CONTROL-${index + 1}`, text: valueFor(control, locale) })),
      })),
      stops: v1.safety.stopConditions.map((entry, index) => ({ id: `STOP-${index + 1}`, text: valueFor(entry, locale) })),
      prohibited: v1.safety.prohibitedAdaptations.map((entry, index) => ({ id: `PROHIBITED-${index + 1}`, text: valueFor(entry, locale) })),
      cleanup: valueFor(v1.safety.cleanup, locale),
    },
    adaptations: v1.adaptations.map((item) => ({
      id: item.adaptationId,
      name: valueFor(item.name, locale),
      conditions: valueFor(item.conditions, locale),
      changes: valueFor(item.changes, locale),
    })),
    closeout: v1.observationPrompts.map((item) => ({
      skill: item.skillId,
      question: valueFor(item.question, locale),
      evidence: item.evidenceExamples.map((entry) => valueFor(entry, locale)),
      nonEvidence: item.nonEvidenceExamples.map((entry) => valueFor(entry, locale)),
      external: item.externalFactors.map((entry) => valueFor(entry, locale)),
    })),
    visuals: v1.visualBriefs.map((item) => ({ id: item.visualBriefId, purpose: valueFor(item.purpose, locale), altText: valueFor(item.altText, locale) })),
  };
}

function migrateEditorial(v1) {
  return {
    schema: "activity-editorial@2",
    activityId: v1.activityId,
    version: v1.version,
    legacyHash: v1.contentHash,
    authors: v1.editorial.authors,
    requiredGates: v1.editorial.requiredReviewGates,
    reviews: v1.editorial.reviewRecords,
    pilots: v1.editorial.pilotRecords,
    changes: v1.editorial.changeLog,
    sources: [],
    visuals: v1.visualBriefs.map((item) => ({
      id: item.visualBriefId,
      assetVersion: item.assetVersion,
      type: item.type,
      style: item.style,
      mustShow: item.mustShow,
      mustNotShow: item.mustNotShow,
      source: item.source,
      rightsClaim: item.rights,
      linkedSteps: item.linkedStepIds,
      approvalState: "review_required",
    })),
  };
}

export function migrateActivityV1ToV2(v1) {
  if (v1.schemaVersion !== "0.1") throw new Error(`Unsupported source schema ${v1.schemaVersion}`);
  const core = migrateCore(v1);
  const locales = Object.fromEntries(V2_LOCALES.map((locale) => [locale, migrateLocale(v1, locale)]));
  const editorial = migrateEditorial(v1);
  const canonical = JSON.stringify({ core, locales });
  const contentHash = `sha256:${createHash("sha256").update(canonical).digest("hex")}`;
  const missingText = V2_LOCALES.flatMap((locale) => {
    const text = JSON.stringify(locales[locale]);
    return nonEmpty(text) ? [] : [locale];
  });
  return {
    core,
    locales,
    editorial,
    report: {
      sourceSchema: "0.1",
      targetSchema: "2.0",
      sourceHash: v1.contentHash,
      contentHash,
      semanticChecks: {
        identity: core.id === v1.activityId && core.version === v1.version,
        ageRange: core.fit.age[0] === v1.ageRange.minimumYears && core.fit.age[1] === v1.ageRange.maximumYears,
        participantRange: core.fit.group.min === v1.participants.minimum && core.fit.group.max === v1.participants.maximum,
        stepOrder: core.flow.steps.map((step) => step.id).join("|") === v1.steps.map((step) => step.stepId).join("|"),
        materialCount: core.materials.length === v1.materials.length,
        roleCount: core.flow.roles.length === v1.roleTemplates.length,
        safetyLevel: core.safety.level === v1.safety.participationLevel,
        requiredLocales: missingText.length === 0,
      },
      reviewRequired: [
        "V1 hazards do not identify affected steps; migration conservatively binds each hazard to every step until human review.",
        "Legacy visual rights claims require conversion to structured evidence before publication.",
        "The target content hash must be stored by the compiler, outside the authored core document.",
      ],
    },
  };
}

function writeBundle(inputPath, outputDir) {
  const source = JSON.parse(readFileSync(inputPath, "utf8"));
  const bundle = migrateActivityV1ToV2(source);
  mkdirSync(outputDir, { recursive: true });
  writeFileSync(path.join(outputDir, "activity-core.v2.example.json"), `${JSON.stringify(bundle.core, null, 2)}\n`);
  for (const locale of V2_LOCALES) {
    writeFileSync(path.join(outputDir, `activity-locale.${locale}.v2.example.json`), `${JSON.stringify(bundle.locales[locale], null, 2)}\n`);
  }
  writeFileSync(path.join(outputDir, "activity-editorial.v2.example.json"), `${JSON.stringify(bundle.editorial, null, 2)}\n`);
  writeFileSync(path.join(outputDir, "activity-migration-report.v2.example.json"), `${JSON.stringify(bundle.report, null, 2)}\n`);
  return bundle.report;
}

const isMain = process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isMain) {
  const inputPath = process.argv[2] ?? "schemas/examples/activity-version.example.json";
  const outputDir = process.argv[3] ?? "schemas/examples/v2";
  const report = writeBundle(inputPath, outputDir);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (Object.values(report.semanticChecks).some((value) => value !== true)) process.exitCode = 1;
}
