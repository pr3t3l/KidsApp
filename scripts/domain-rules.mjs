function addError(errors, code, message) {
  errors.push({ code, message });
}

function duplicateValues(items, selector) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of items) {
    const value = selector(item);
    if (seen.has(value)) duplicates.add(value);
    seen.add(value);
  }
  return [...duplicates];
}

function setOf(items, selector = (value) => value) {
  return new Set(items.map(selector));
}

function isBeforeOrEqual(first, second) {
  if (!first || !second) return true;
  return Date.parse(first) <= Date.parse(second);
}

function validateActivity(activity, errors) {
  if (activity.ageRange.minimumYears > activity.ageRange.maximumYears) {
    addError(errors, "ACT_AGE_RANGE", "ageRange.minimumYears must not exceed maximumYears");
  }
  if (activity.participants.minimum > activity.participants.maximum) {
    addError(errors, "ACT_PARTICIPANT_RANGE", "participants.minimum must not exceed maximum");
  }
  if (activity.timing.totalMinutesMin > activity.timing.totalMinutesMax) {
    addError(errors, "ACT_TIMING_RANGE", "timing.totalMinutesMin must not exceed totalMinutesMax");
  }

  for (const count of activity.participants.supportedCounts) {
    if (count < activity.participants.minimum || count > activity.participants.maximum) {
      addError(errors, "ACT_SUPPORTED_COUNT", `supported participant count ${count} is outside the declared range`);
    }
  }

  const collections = [
    ["concept", activity.learning.concepts, (item) => item.conceptId],
    ["skill", activity.learning.skills, (item) => item.skillId],
    ["material", activity.materials, (item) => item.materialId],
    ["role", activity.roleTemplates, (item) => item.roleTemplateId],
    ["step", activity.steps, (item) => item.stepId],
    ["adaptation", activity.adaptations, (item) => item.adaptationId],
    ["visual brief", activity.visualBriefs, (item) => item.visualBriefId],
    ["review", activity.editorial.reviewRecords, (item) => item.reviewId],
    ["pilot record", activity.editorial.pilotRecords, (item) => item.pilotRecordId],
  ];
  for (const [label, items, selector] of collections) {
    for (const duplicate of duplicateValues(items, selector)) {
      addError(errors, "ACT_DUPLICATE_ID", `duplicate ${label} identifier ${duplicate}`);
    }
  }

  const skillIds = setOf(activity.learning.skills, (item) => item.skillId);
  const conceptIds = setOf(activity.learning.concepts, (item) => item.conceptId);
  const roleIds = setOf(activity.roleTemplates, (item) => item.roleTemplateId);
  const stepIds = setOf(activity.steps, (item) => item.stepId);
  const adaptationIds = setOf(activity.adaptations, (item) => item.adaptationId);
  const visualIds = setOf(activity.visualBriefs, (item) => item.visualBriefId);

  const checkRefs = (refs, validIds, code, context) => {
    for (const ref of refs) {
      if (!validIds.has(ref)) addError(errors, code, `${context} references unknown identifier ${ref}`);
    }
  };

  for (const role of activity.roleTemplates) {
    checkRefs(role.eligiblePrimarySkillIds, skillIds, "ACT_ROLE_SKILL_REF", role.roleTemplateId);
    checkRefs(role.exposureSkillIds, skillIds, "ACT_ROLE_SKILL_REF", role.roleTemplateId);
    checkRefs(role.exposureConceptIds, conceptIds, "ACT_ROLE_CONCEPT_REF", role.roleTemplateId);
    checkRefs(role.allowedStepIds, stepIds, "ACT_ROLE_STEP_REF", role.roleTemplateId);
    checkRefs(role.restrictedStepIds, stepIds, "ACT_ROLE_STEP_REF", role.roleTemplateId);
    const restricted = setOf(role.restrictedStepIds);
    for (const stepId of role.allowedStepIds) {
      if (restricted.has(stepId)) addError(errors, "ACT_ROLE_STEP_OVERLAP", `${role.roleTemplateId} both allows and restricts ${stepId}`);
    }
  }

  for (const config of activity.groupConfigurations) {
    checkRefs(config.roleTemplateIds, roleIds, "ACT_GROUP_ROLE_REF", `group configuration ${config.participantCount}`);
    if (config.roleTemplateIds.length > config.participantCount) {
      addError(errors, "ACT_GROUP_ROLE_COUNT", `configuration ${config.participantCount} has more roles than participants`);
    }
  }
  const configuredCounts = setOf(activity.groupConfigurations, (item) => item.participantCount);
  for (const count of activity.participants.supportedCounts) {
    if (!configuredCounts.has(count)) addError(errors, "ACT_GROUP_COVERAGE", `supported participant count ${count} has no group configuration`);
  }

  for (const step of activity.steps) {
    checkRefs(step.visualBriefIds, visualIds, "ACT_STEP_VISUAL_REF", step.stepId);
    checkRefs(step.exposureSkillIds, skillIds, "ACT_STEP_SKILL_REF", step.stepId);
    checkRefs(step.exposureConceptIds, conceptIds, "ACT_STEP_CONCEPT_REF", step.stepId);
  }
  for (const stage of activity.learning.cycleStages) {
    if (!activity.steps.some((step) => step.stage === stage)) {
      addError(errors, "ACT_CYCLE_COVERAGE", `cycle stage ${stage} has no step`);
    }
  }
  checkRefs(activity.safety.adultOnlyStepIds, stepIds, "ACT_ADULT_STEP_REF", "safety.adultOnlyStepIds");
  for (const prompt of activity.observationPrompts) {
    checkRefs([prompt.skillId], skillIds, "ACT_PROMPT_SKILL_REF", "observation prompt");
  }
  for (const visual of activity.visualBriefs) {
    checkRefs(visual.linkedStepIds, stepIds, "ACT_VISUAL_STEP_REF", visual.visualBriefId);
  }

  if (activity.status === "published") {
    const approvals = activity.editorial.reviewRecords.filter(
      (record) => record.decision === "approved" && record.reviewedVersion === activity.version && record.contentHash === activity.contentHash,
    );
    const approvedGates = setOf(approvals, (record) => record.gate);
    for (const gate of activity.editorial.requiredReviewGates) {
      if (!approvedGates.has(gate)) addError(errors, "ACT_PUBLISH_GATE", `published version lacks an approved ${gate} review for its version and hash`);
    }
    const pilots = activity.editorial.pilotRecords;
    if (pilots.length < 4 || setOf(pilots, (record) => record.familyPilotId).size < 2 || !pilots.some((record) => record.facilitatorKind === "other_adult")) {
      addError(errors, "ACT_PUBLISH_PILOT", "published content requires at least four records across two families, including another adult; C/D may require more");
    }
    if (["C", "D"].includes(activity.safety.participationLevel) && !approvals.some((record) => record.gate === "safety" && record.reviewerRole === "safety_specialist")) {
      addError(errors, "ACT_PUBLISH_REINFORCED_GATE", "published C/D content requires an approved safety-specialist record");
    }
  }

  return { skillIds, conceptIds, roleIds, stepIds, adaptationIds };
}

function validateSession(activity, session, refs, errors) {
  if (
    session.activityRef.activityId !== activity.activityId ||
    session.activityRef.version !== activity.version ||
    session.activityRef.contentHash !== activity.contentHash
  ) {
    addError(errors, "SES_ACTIVITY_REF", "session must reference the exact activity id, version, and content hash");
  }
  if (session.deliveryMode === "family_recommendation" && activity.status !== "published") {
    addError(errors, "SES_DELIVERY_STATUS", "family_recommendation requires a published ActivityVersion");
  }
  if (session.deliveryMode === "pilot" && !["ready_for_pilot", "family_pilot"].includes(activity.status)) {
    addError(errors, "SES_DELIVERY_STATUS", "pilot delivery requires ready_for_pilot or family_pilot content");
  }
  if (activity.status === "retired" && session.status === "planned") {
    addError(errors, "SES_RETIRED_CONTENT", "a new planned session cannot use retired content");
  }

  if (!activity.participants.supportedCounts.includes(session.assignments.length)) {
    addError(errors, "SES_PARTICIPANT_COUNT", "assignment count is not supported by the ActivityVersion");
  }
  for (const duplicate of duplicateValues(session.assignments, (item) => item.learnerId)) {
    addError(errors, "SES_DUPLICATE_LEARNER", `learner ${duplicate} appears more than once in assignments`);
  }
  for (const duplicate of duplicateValues(session.assignments, (item) => item.assignmentId)) {
    addError(errors, "SES_DUPLICATE_ASSIGNMENT", `assignment ${duplicate} appears more than once`);
  }
  for (const duplicate of duplicateValues(session.stepProgress, (item) => item.stepId)) {
    addError(errors, "SES_DUPLICATE_STEP", `step ${duplicate} appears more than once in progress`);
  }

  const roleById = new Map(activity.roleTemplates.map((role) => [role.roleTemplateId, role]));
  const assignmentByLearner = new Map(session.assignments.map((assignment) => [assignment.learnerId, assignment]));
  for (const assignment of session.assignments) {
    const plannedRole = roleById.get(assignment.plannedRoleTemplateId);
    if (!plannedRole) {
      addError(errors, "SES_ROLE_REF", `unknown planned role ${assignment.plannedRoleTemplateId}`);
      continue;
    }
    for (const roleId of assignment.actualRoleTemplateIds) {
      if (!roleById.has(roleId)) addError(errors, "SES_ROLE_REF", `unknown actual role ${roleId}`);
    }
    if (!plannedRole.eligiblePrimarySkillIds.includes(assignment.primaryObjectiveSkillId)) {
      addError(errors, "SES_PRIMARY_OBJECTIVE", `${assignment.primaryObjectiveSkillId} is not eligible for ${plannedRole.roleTemplateId}`);
    }
    for (const stepId of assignment.participatedStepIds) {
      if (!refs.stepIds.has(stepId)) addError(errors, "SES_STEP_REF", `assignment references unknown step ${stepId}`);
    }

    const actualRoles = assignment.actualRoleTemplateIds.map((id) => roleById.get(id)).filter(Boolean);
    const participatedSteps = activity.steps.filter((step) => assignment.participatedStepIds.includes(step.stepId));
    const allowedSkills = new Set(actualRoles.flatMap((role) => role.exposureSkillIds).concat(participatedSteps.flatMap((step) => step.exposureSkillIds)));
    const allowedConcepts = new Set(actualRoles.flatMap((role) => role.exposureConceptIds).concat(participatedSteps.flatMap((step) => step.exposureConceptIds)));
    for (const skillId of assignment.actualExposureSkillIds) {
      if (!allowedSkills.has(skillId)) addError(errors, "SES_DERIVED_EXPOSURE", `actual skill exposure ${skillId} is not derivable from actual roles or steps`);
    }
    for (const conceptId of assignment.actualExposureConceptIds) {
      if (!allowedConcepts.has(conceptId)) addError(errors, "SES_DERIVED_EXPOSURE", `actual concept exposure ${conceptId} is not derivable from actual roles or steps`);
    }
    if (assignment.participationStatus === "did_not_participate") {
      if (assignment.actualRoleTemplateIds.length || assignment.actualExposureSkillIds.length || assignment.actualExposureConceptIds.length || assignment.participatedStepIds.length) {
        addError(errors, "SES_NONPARTICIPANT_DATA", `nonparticipant ${assignment.learnerId} cannot have actual roles, steps, or exposures`);
      }
    }
  }

  for (const progress of session.stepProgress) {
    if (!refs.stepIds.has(progress.stepId)) addError(errors, "SES_STEP_REF", `progress references unknown step ${progress.stepId}`);
  }
  for (const adaptation of session.appliedAdaptations) {
    if (!refs.adaptationIds.has(adaptation.adaptationId)) addError(errors, "SES_ADAPTATION_REF", `unknown adaptation ${adaptation.adaptationId}`);
    const definition = activity.adaptations.find((item) => item.adaptationId === adaptation.adaptationId);
    if (definition?.requiresAdultConfirmation && !adaptation.appliedByAdultId) {
      addError(errors, "SES_ADAPTATION_CONFIRMATION", `${adaptation.adaptationId} requires an adult id`);
    }
  }
  for (const event of session.assignmentEvents) {
    const assignment = session.assignments.find((item) => item.assignmentId === event.assignmentId);
    if (!assignment || assignment.learnerId !== event.learnerId) addError(errors, "SES_ASSIGNMENT_EVENT_REF", `${event.eventId} does not match an assignment and learner`);
  }

  if (session.status === "completed" && (!session.closeOut || !session.completedAt)) {
    addError(errors, "SES_COMPLETED_CLOSEOUT", "completed sessions require completedAt and closeOut");
  }
  if (!isBeforeOrEqual(session.scheduledAt, session.startedAt) || !isBeforeOrEqual(session.startedAt, session.completedAt)) {
    addError(errors, "SES_TIMESTAMP_ORDER", "session timestamps are not chronological");
  }

  if (session.closeOut) {
    for (const duplicate of duplicateValues(session.closeOut.participantResults, (item) => item.learnerId)) {
      addError(errors, "SES_DUPLICATE_PRIMARY_RESULT", `close-out has duplicate result for ${duplicate}`);
    }
    const resultLearners = setOf(session.closeOut.participantResults, (item) => item.learnerId);
    for (const assignment of session.assignments) {
      if (!resultLearners.has(assignment.learnerId)) addError(errors, "SES_CLOSEOUT_COVERAGE", `close-out lacks ${assignment.learnerId}`);
    }
    for (const result of session.closeOut.participantResults) {
      const assignment = assignmentByLearner.get(result.learnerId);
      if (!assignment) {
        addError(errors, "SES_CLOSEOUT_LEARNER", `close-out references unknown learner ${result.learnerId}`);
        continue;
      }
      if (result.disposition === "rated" && result.primaryRating?.skillId !== assignment.primaryObjectiveSkillId) {
        addError(errors, "SES_PRIMARY_RATING_SKILL", `primary rating for ${result.learnerId} must match the assigned objective`);
      }
      if (assignment.participationStatus === "did_not_participate" && (result.disposition !== "did_not_participate" || result.primaryRating || result.secondaryRatings.length)) {
        addError(errors, "SES_NONPARTICIPANT_RATING", `nonparticipant ${result.learnerId} cannot be rated`);
      }
      const ratedSkills = [result.primaryRating?.skillId, ...result.secondaryRatings.map((rating) => rating.skillId)].filter(Boolean);
      for (const duplicate of duplicateValues(ratedSkills, (value) => value)) {
        addError(errors, "SES_DUPLICATE_RATING_SKILL", `${result.learnerId} has duplicate rating for ${duplicate}`);
      }
    }
  }
}

function validateRecords(activity, session, records, errors) {
  for (const [label, items, selector] of [
    ["exposure", records.exposures, (item) => item.exposureId],
    ["observation", records.observations, (item) => item.observationId],
    ["inference", records.inferences, (item) => item.inferenceId],
  ]) {
    for (const duplicate of duplicateValues(items, selector)) addError(errors, "LRN_DUPLICATE_ID", `duplicate ${label} ${duplicate}`);
  }

  const assignment = session.assignments.find((item) => item.learnerId === records.learnerId);
  const observationById = new Map(records.observations.map((observation) => [observation.observationId, observation]));
  for (const exposure of records.exposures) {
    if (exposure.sessionId !== session.sessionId) addError(errors, "LRN_EXPOSURE_SESSION", `${exposure.exposureId} references another session`);
    if (exposure.activityRef.activityId !== activity.activityId || exposure.activityRef.version !== activity.version || exposure.activityRef.contentHash !== activity.contentHash) {
      addError(errors, "LRN_ACTIVITY_REF", `${exposure.exposureId} has the wrong activity reference`);
    }
    const actualIds = exposure.kind === "skill" ? assignment?.actualExposureSkillIds : assignment?.actualExposureConceptIds;
    if (!actualIds?.includes(exposure.skillOrConceptId)) addError(errors, "LRN_EXPOSURE_NOT_ACTUAL", `${exposure.exposureId} was not an actual session exposure`);
  }

  for (const observation of records.observations) {
    if (observation.sessionId !== session.sessionId) addError(errors, "LRN_OBSERVATION_SESSION", `${observation.observationId} references another session`);
    const ratingSource = ["primary_rating", "secondary_rating"].includes(observation.source);
    if (ratingSource && !Number.isInteger(observation.independenceRating)) {
      addError(errors, "LRN_RATING_REQUIRED", `${observation.observationId} requires an independence rating`);
    }
    if (!ratingSource && observation.independenceRating !== null) {
      addError(errors, "LRN_RATING_FORBIDDEN", `${observation.observationId} cannot attach a rating to a free-form source`);
    }
    if (observation.provenance.aiAssisted && !observation.provenance.providerDeploymentId) {
      addError(errors, "LRN_AI_PROVENANCE", `${observation.observationId} is AI-assisted without a provider deployment id`);
    }
    if (observation.status === "corrected" && (!observation.supersedesObservationId || !observation.correctionReason)) {
      addError(errors, "LRN_CORRECTION_CHAIN", `${observation.observationId} lacks correction lineage`);
    }
    if (observation.status === "rejected" && !observation.rejectionReason) {
      addError(errors, "LRN_REJECTION_REASON", `${observation.observationId} lacks a rejection reason`);
    }
  }

  for (const inference of records.inferences) {
    const evidence = inference.evidenceLinks.map((link) => observationById.get(link.observationId));
    if (inference.state !== "not_enough_evidence" && inference.evidenceLinks.length === 0) {
      addError(errors, "LRN_INFERENCE_EVIDENCE", `${inference.inferenceId} has a state without evidence`);
    }
    for (let index = 0; index < inference.evidenceLinks.length; index += 1) {
      const link = inference.evidenceLinks[index];
      const observation = evidence[index];
      if (!observation) addError(errors, "LRN_EVIDENCE_REF", `${inference.inferenceId} references unknown observation ${link.observationId}`);
      else if (observation.skillId !== inference.skillId || observation.status === "rejected") {
        addError(errors, "LRN_EVIDENCE_MISMATCH", `${link.observationId} is not valid evidence for ${inference.skillId}`);
      }
    }
    if (inference.confidence === "strong" && evidence.filter(Boolean).length < 2) {
      addError(errors, "LRN_STRONG_EVIDENCE", `${inference.inferenceId} needs at least two observations for strong confidence`);
    }
    if (inference.state === "not_enough_evidence" && inference.confidence !== "insufficient") {
      addError(errors, "LRN_STATE_CONFIDENCE", "not_enough_evidence must use insufficient confidence");
    }
  }
}

function validateOffline(activity, session, manifest, syncEvents, errors) {
  if (session.offlineState) {
    if (session.offlineState.packId !== manifest.packId || session.offlineState.manifestContentHash !== manifest.manifestContentHash) {
      addError(errors, "OFF_MANIFEST_REF", "session offlineState must reference the exact manifest id and hash");
    }
    if (session.offlineState.baseServerRevision !== manifest.baseServerRevision) {
      addError(errors, "OFF_BASE_REVISION", "session and manifest base revisions must match");
    }
  }
  if (!isBeforeOrEqual(manifest.generatedAt, manifest.expiresAt)) addError(errors, "OFF_EXPIRY", "offline pack expiry precedes generation");
  const activityEntry = manifest.activityEntries.find((entry) => entry.activityId === activity.activityId && entry.version === activity.version);
  if (!activityEntry || activityEntry.contentHash !== activity.contentHash) addError(errors, "OFF_ACTIVITY_REF", "manifest lacks the exact activity version and hash");
  const manifestAssignment = manifest.sessionAssignments.find((item) => item.sessionId === session.sessionId);
  if (!manifestAssignment) addError(errors, "OFF_SESSION_REF", "manifest lacks the session assignment");

  for (const duplicate of duplicateValues(syncEvents, (event) => event.eventId)) addError(errors, "OFF_DUPLICATE_EVENT", `duplicate event id ${duplicate}`);
  for (const duplicate of duplicateValues(syncEvents, (event) => event.idempotencyKey)) addError(errors, "OFF_DUPLICATE_IDEMPOTENCY", `duplicate idempotency key ${duplicate}`);
  for (const event of syncEvents) {
    if (event.sessionId !== session.sessionId || event.familyId !== session.familyId) addError(errors, "OFF_EVENT_SCOPE", `${event.eventId} has the wrong family or session`);
    if (event.payload.kind !== event.eventType) addError(errors, "OFF_EVENT_KIND", `${event.eventId} payload kind does not match event type`);
    if (event.serverRevision !== null && event.serverRevision < event.baseServerRevision) addError(errors, "OFF_EVENT_REVISION", `${event.eventId} moves server revision backwards`);
  }
}

export function validateDomainBundle({ activity, session, records, manifest, syncEvents = [] }) {
  const errors = [];
  const refs = validateActivity(activity, errors);
  validateSession(activity, session, refs, errors);
  validateRecords(activity, session, records, errors);
  validateOffline(activity, session, manifest, syncEvents, errors);
  return errors;
}
