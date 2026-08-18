import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { validateDomainBundle } from "./domain-rules.mjs";

const root = process.cwd();
const readJson = (relativePath) => JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
const clone = (value) => structuredClone(value);

const baseline = {
  activity: readJson("schemas/examples/activity-version.example.json"),
  session: readJson("schemas/examples/session.example.json"),
  records: readJson("schemas/examples/learner-records.example.json"),
  manifest: readJson("schemas/examples/offline-pack-manifest.example.json"),
  syncEvents: [
    readJson("schemas/examples/sync-event.example.json"),
    readJson("schemas/examples/sync-event-conflict.example.json"),
  ],
};

const baselineErrors = validateDomainBundle(baseline);
if (baselineErrors.length > 0) {
  process.stderr.write(`domain baseline failed (${baselineErrors.length})\n${JSON.stringify(baselineErrors, null, 2)}\n`);
  process.exit(1);
}
process.stdout.write("domain baseline ok: cross-document references and invariants\n");

const participantTemplates = [
  {
    suffix: "B",
    roleTemplateId: "ROLE-TESTER",
    primaryObjectiveSkillId: "MAT-SKL-ONE-TO-ONE-COUNTING",
    exposureSkillIds: ["MAT-SKL-ONE-TO-ONE-COUNTING"],
    stepIds: ["STEP-01", "STEP-02", "STEP-03", "STEP-04", "STEP-05", "STEP-06", "STEP-07"],
  },
  {
    suffix: "C",
    roleTemplateId: "ROLE-DESIGNER",
    primaryObjectiveSkillId: "ENG-SKL-COMPARE-REDESIGN",
    exposureSkillIds: ["ENG-SKL-COMPARE-REDESIGN"],
    stepIds: ["STEP-01", "STEP-02", "STEP-03", "STEP-04", "STEP-05", "STEP-06", "STEP-07"],
  },
];

for (let count = 1; count <= 3; count += 1) {
  const candidate = clone(baseline);
  for (const template of participantTemplates.slice(0, count - 1)) {
    const learnerId = `LEARNER-DEMO-${template.suffix}`;
    candidate.session.assignments.push({
      assignmentId: `ASN-DEMO-${template.suffix}`,
      learnerId,
      participationStatus: "participated",
      plannedRoleTemplateId: template.roleTemplateId,
      actualRoleTemplateIds: [template.roleTemplateId],
      primaryObjectiveSkillId: template.primaryObjectiveSkillId,
      plannedExposureSkillIds: template.exposureSkillIds,
      plannedExposureConceptIds: ["ENG-CON-STRUCTURAL-RIGIDITY"],
      actualExposureSkillIds: template.exposureSkillIds,
      actualExposureConceptIds: ["ENG-CON-STRUCTURAL-RIGIDITY"],
      assignmentSource: "recommendation",
      changeReason: null,
      participatedStepIds: template.stepIds,
    });
    candidate.session.closeOut.participantResults.push({
      learnerId,
      disposition: "rated",
      primaryRating: {
        skillId: template.primaryObjectiveSkillId,
        independenceRating: 3,
        contextFlags: [],
        otherContext: null,
      },
      secondaryRatings: [],
      skipReason: null,
    });
    candidate.manifest.sessionAssignments.push({
      sessionId: candidate.session.sessionId,
      activityId: candidate.activity.activityId,
      activityVersion: candidate.activity.version,
      learnerId,
      roleTemplateId: template.roleTemplateId,
      primaryObjectiveSkillId: template.primaryObjectiveSkillId,
    });
  }
  const errors = validateDomainBundle(candidate);
  if (errors.length > 0) {
    process.stderr.write(`participant fixture failed: ${count} (${JSON.stringify(errors)})\n`);
    process.exit(1);
  }
  process.stdout.write(`participant fixture ok: ${count} participant${count === 1 ? "" : "s"}\n`);
}

const negativeCases = [
  ["reversed age range", (bundle) => { bundle.activity.ageRange = { minimumYears: 10, maximumYears: 5 }; }],
  ["contradictory participant range", (bundle) => { bundle.activity.participants.minimum = 3; bundle.activity.participants.maximum = 2; }],
  ["role references missing skill", (bundle) => { bundle.activity.roleTemplates[0].eligiblePrimarySkillIds = ["MOT-SKL-MISSING"]; }],
  ["step action references missing role", (bundle) => { bundle.activity.steps[0].participantActionTemplates[0].audience = "role_templates"; bundle.activity.steps[0].participantActionTemplates[0].roleTemplateIds = ["ROLE-MISSING"]; }],
  ["step cue references missing skill", (bundle) => { bundle.activity.steps[0].observationCues[0].skillId = "ENG-SKL-MISSING"; }],
  ["broken narrative transition", (bundle) => { bundle.activity.steps[0].exitStateId = "STATE-DESIGNS-CHOSEN"; }],
  ["required participant cycle action missing", (bundle) => { bundle.activity.steps[4].cycleActions = []; }],
  ["participant cycle action hidden behind one role", (bundle) => { bundle.activity.steps[2].participantActionTemplates[0].audience = "role_templates"; bundle.activity.steps[2].participantActionTemplates[0].roleTemplateIds = ["ROLE-BUILDER"]; }],
  ["material used before its introduction", (bundle) => { bundle.activity.experienceNarrative.materialFunctions[0].introducedAtStepId = "STEP-03"; }],
  ["objective guidance has reversed age range", (bundle) => { bundle.activity.objectiveGuidance[0].startingAgeRange = { minimumYears: 8, maximumYears: 5 }; }],
  ["published without reviews or pilots", (bundle) => { bundle.activity.status = "published"; bundle.activity.editorial.reviewRecords = []; bundle.activity.editorial.pilotRecords = []; }],
  ["completed without close-out", (bundle) => { bundle.session.closeOut = null; }],
  ["duplicate learner assignment", (bundle) => { bundle.session.assignments.push(clone(bundle.session.assignments[0])); }],
  ["duplicate primary result", (bundle) => { bundle.session.closeOut.participantResults.push(clone(bundle.session.closeOut.participantResults[0])); }],
  ["nonparticipant with exposures and rating", (bundle) => { bundle.session.assignments[0].participationStatus = "did_not_participate"; }],
  ["strong inference without evidence", (bundle) => { bundle.records.inferences[0].confidence = "strong"; bundle.records.inferences[0].evidenceLinks = []; }],
  ["primary-rating observation without rating", (bundle) => { delete bundle.records.observations[0].independenceRating; }],
  ["inference references missing observation", (bundle) => { bundle.records.inferences[0].evidenceLinks[0].observationId = "OBS-MISSING"; }],
];

let failed = false;
for (const [name, mutate] of negativeCases) {
  const candidate = clone(baseline);
  mutate(candidate);
  const errors = validateDomainBundle(candidate);
  if (errors.length === 0) {
    failed = true;
    process.stderr.write(`negative fixture accepted: ${name}\n`);
  } else {
    process.stdout.write(`negative fixture rejected: ${name} (${errors[0].code})\n`);
  }
}

if (failed) process.exitCode = 1;
