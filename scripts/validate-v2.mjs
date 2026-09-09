import fs from "node:fs";
import path from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";
import { migrateActivityV1ToV2, V2_LOCALES } from "./migrate-activity-v1-to-v2.mjs";

const readJson = (relativePath) => JSON.parse(fs.readFileSync(path.resolve(relativePath), "utf8"));
const bytes = (value) => Buffer.byteLength(JSON.stringify(value), "utf8");
const tokenEstimate = (value) => Math.ceil(bytes(value) / 4);

const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);
const blockSchema = readJson("schemas/v2/content-block.schema.json");
ajv.addSchema(blockSchema);

const compile = (schemaPath) => ajv.compile(readJson(schemaPath));
const validators = {
  core: compile("schemas/v2/activity-core.schema.json"),
  locale: compile("schemas/v2/activity-locale.schema.json"),
  idea: compile("schemas/v2/model/idea-brief.schema.json"),
  corePlan: compile("schemas/v2/model/core-plan.schema.json"),
  materialsSafety: compile("schemas/v2/model/materials-safety.schema.json"),
  stepsDraft: compile("schemas/v2/model/steps.schema.json"),
  rolesDraft: compile("schemas/v2/model/roles-adaptations.schema.json"),
  closeoutDraft: compile("schemas/v2/model/closeout.schema.json"),
  localeBatch: compile("schemas/v2/model/locale-batch.schema.json"),
  reviewFindings: compile("schemas/v2/model/review-findings.schema.json"),
  reviewSynthesis: compile("schemas/v2/model/review-synthesis.schema.json"),
  card: compile("schemas/v2/read-models/activity-card.schema.json"),
  prep: compile("schemas/v2/read-models/activity-prep.schema.json"),
  step: compile("schemas/v2/read-models/session-step.schema.json"),
  closeout: compile("schemas/v2/read-models/session-closeout.schema.json"),
};

const source = readJson("schemas/examples/activity-version.example.json");
const bundle = migrateActivityV1ToV2(source);
const failures = [];
const fail = (message) => failures.push(message);

function validate(name, validator, value) {
  if (!validator(value)) fail(`${name}: ${ajv.errorsText(validator.errors, { separator: "; " })}`);
}

validate("ActivityCoreV2", validators.core, bundle.core);
for (const locale of V2_LOCALES) validate(`ActivityLocaleV2 ${locale}`, validators.locale, bundle.locales[locale]);

for (const [name, passed] of Object.entries(bundle.report.semanticChecks)) {
  if (!passed) fail(`migration semantic check failed: ${name}`);
}

const core = bundle.core;
if (core.fit.age[0] > core.fit.age[1]) fail("fit.age is reversed");
if (core.fit.group.min > core.fit.group.max) fail("fit.group is reversed");
if (core.fit.time.min > core.fit.time.max) fail("fit.time is reversed");
if (core.fit.group.sizes.some((size) => size < core.fit.group.min || size > core.fit.group.max)) fail("fit.group.sizes escapes the declared range");

const stepIds = new Set(core.flow.steps.map((step) => step.id));
const stateIds = new Set(core.flow.states);
const materialIds = new Set(core.materials.map((material) => material.id));
const roleIds = new Set(core.flow.roles.map((role) => role.id));
const visualIds = new Set(bundle.editorial.visuals.map((visual) => visual.id));
const skillIds = new Set(core.learn.skills);
if (core.flow.steps[0].entry !== core.flow.start) fail("first step does not enter from flow.start");
if (core.flow.steps.at(-1).exit !== core.flow.end) fail("last step does not exit to flow.end");
for (let index = 1; index < core.flow.steps.length; index += 1) {
  if (core.flow.steps[index - 1].exit !== core.flow.steps[index].entry) fail(`step continuity breaks before ${core.flow.steps[index].id}`);
}
for (const step of core.flow.steps) {
  if (!stateIds.has(step.entry) || !stateIds.has(step.exit)) fail(`${step.id}: unknown narrative state`);
  if (step.materialIds.some((id) => !materialIds.has(id))) fail(`${step.id}: unknown material reference`);
  if (step.visualIds.some((id) => !visualIds.has(id))) fail(`${step.id}: unknown visual reference`);
  if (step.cues.some((cue) => !skillIds.has(cue.skill))) fail(`${step.id}: unknown cue skill`);
  for (const action of step.participantActions) if (action.roles.some((id) => !roleIds.has(id))) fail(`${step.id}: unknown action role`);
}
for (const item of core.flow.materialFunctions) {
  if (!materialIds.has(item.material) || !stepIds.has(item.firstStep)) fail(`invalid material function ${item.material}`);
}
for (const group of core.flow.groups) {
  if (!core.fit.group.sizes.includes(group.size)) fail(`group ${group.size} is not a supported size`);
  if (group.roles.length !== group.size) fail(`group ${group.size} does not have one logical slot per participant`);
  if (group.roles.some((id) => !roleIds.has(id))) fail(`group ${group.size} references an unknown role`);
}
for (const hazard of core.safety.hazards) {
  if (hazard.steps.some((id) => !stepIds.has(id))) fail(`${hazard.id}: unknown affected step`);
  for (const locale of V2_LOCALES) {
    const localized = bundle.locales[locale].safety.hazards.find((item) => item.id === hazard.id);
    if (!localized || hazard.controlIds.some((id) => !localized.controls.some((control) => control.id === id))) fail(`${hazard.id}: missing ${locale} control text`);
  }
}
for (const adaptation of core.adaptations) if (adaptation.safety !== "none" && !adaptation.adultConfirm) fail(`${adaptation.id}: safety-changing adaptation cannot be automatic`);

for (const locale of V2_LOCALES) {
  const localized = bundle.locales[locale];
  for (const step of core.flow.steps) {
    const copy = localized.flow.steps.find((item) => item.id === step.id);
    if (!copy) { fail(`${step.id}: missing ${locale} step copy`); continue; }
    if (step.participantActions.length && (!copy.purpose || !copy.participantActions.length || !copy.cues.length)) fail(`${step.id}: child participation lacks purpose/action/signal in ${locale}`);
    if (step.hasDecision !== Boolean(copy.decision)) fail(`${step.id}: decision flag differs in ${locale}`);
  }
}

const locale = bundle.locales["en-US"];
const activityCard = {
  id: core.id, version: core.version, locale: "en-US", title: locale.content.title, summary: locale.content.summary,
  age: core.fit.age, group: core.fit.group.sizes, minutes: [core.fit.time.min, core.fit.time.max], area: core.learn.primary, risk: core.safety.level,
};
const activityPrep = {
  id: core.id, version: core.version, locale: "en-US", purpose: locale.learn.goal,
  materials: core.materials.map((material) => ({ id: material.id, name: locale.materials.find((item) => item.id === material.id).name, quantity: material.quantity, unit: material.unit })),
  safety: { level: core.safety.level, supervision: locale.safety.supervision, stops: locale.safety.stops.map((item) => item.text) },
  group: { min: core.fit.group.min, max: core.fit.group.max },
};
const firstStep = core.flow.steps[0];
const firstCopy = locale.flow.steps[0];
const sessionStep = {
  sessionId: "00000000-0000-0000-0000-000000000201", activityVersion: `${core.id}@${core.version}`, stepId: firstStep.id, position: 1, total: core.flow.steps.length, canPause: true,
  blocks: [
    { id: `${firstStep.id}-purpose`, kind: "purpose", version: 1, required: true, data: { text: firstCopy.purpose } },
    { id: `${firstStep.id}-instruction`, kind: "instruction", version: 1, required: true, data: { title: firstCopy.title, text: firstCopy.instruction } },
  ],
};
const sessionCloseout = {
  sessionId: "00000000-0000-0000-0000-000000000201",
  participants: [{ learnerId: "00000000-0000-0000-0000-000000000301", alias: "Sam", skillId: locale.closeout[0].skill, question: locale.closeout[0].question, anchors: ["Not yet", "With full help", "With some help", "Mostly independently", "Independently"], canSkip: true }],
};
validate("ActivityCard", validators.card, activityCard);
validate("ActivityPrep", validators.prep, activityPrep);
validate("SessionStep", validators.step, sessionStep);
validate("SessionCloseout", validators.closeout, sessionCloseout);

const ideaBrief = { title: locale.content.title, promise: locale.content.summary, fit: { age: core.fit.age, group: core.fit.group.sizes, minutes: core.fit.time.max, risk: core.safety.level }, area: core.learn.primary, mechanism: locale.learn.method, materials: locale.materials.map((item) => item.name), safety: locale.safety.stops.map((item) => item.text), sourceRefs: [] };
const corePlan = {
  goal: locale.learn.goal, method: locale.learn.method, skills: core.learn.skills,
  states: locale.flow.states.map((state) => ({ id: state.id, meaning: state.text })),
  steps: core.flow.steps.map((step, index) => ({ id: step.id, entry: step.entry, exit: step.exit, actor: step.actor, action: locale.flow.steps[index].instruction, purpose: locale.flow.steps[index].purpose, signal: locale.flow.steps[index].success })),
  risks: core.safety.hazards.map((hazard, index) => ({ hazard: locale.safety.hazards[index].description, control: locale.safety.hazards[index].controls.map((item) => item.text).join(" "), stop: locale.safety.stops[0].text, steps: hazard.steps })),
};
validate("IdeaBrief", validators.idea, ideaBrief);
validate("CorePlan", validators.corePlan, corePlan);

const sizeGates = [
  ["model idea schema", readJson("schemas/v2/model/idea-brief.schema.json"), 2000],
  ["model core-plan schema", readJson("schemas/v2/model/core-plan.schema.json"), 2000],
  ["model materials-safety schema", readJson("schemas/v2/model/materials-safety.schema.json"), 2000],
  ["model steps schema", readJson("schemas/v2/model/steps.schema.json"), 2000],
  ["model roles-adaptations schema", readJson("schemas/v2/model/roles-adaptations.schema.json"), 2000],
  ["model closeout schema", readJson("schemas/v2/model/closeout.schema.json"), 2000],
  ["model locale-batch schema", readJson("schemas/v2/model/locale-batch.schema.json"), 2000],
  ["model review-findings schema", readJson("schemas/v2/model/review-findings.schema.json"), 2000],
  ["model review-synthesis schema", readJson("schemas/v2/model/review-synthesis.schema.json"), 2000],
  ["idea response", ideaBrief, 2000],
  ["core-plan response", corePlan, 2000],
  ["ActivityCard", activityCard, 512],
  ["ActivityPrep", activityPrep, 3072],
  ["SessionStep", sessionStep, 2048],
];
for (const [name, value, maxTokens] of sizeGates) if (tokenEstimate(value) > maxTokens) fail(`${name}: ${tokenEstimate(value)} estimated tokens exceeds ${maxTokens}`);
if (bytes(activityCard) >= 2048) fail("ActivityCard exceeds 2 KB");
if (bytes(activityPrep) >= 12288) fail("ActivityPrep exceeds 12 KB");
if (bytes(sessionStep) >= 8192) fail("SessionStep exceeds 8 KB");
if (bytes(core) >= bytes(source)) fail("ActivityCoreV2 alone is not smaller than the V1 monolith");
for (const item of V2_LOCALES) if (bytes(bundle.locales[item]) >= bytes(source)) fail(`${item} locale payload is not smaller than the V1 monolith`);

function checkFieldNames(value, location = "root") {
  if (Array.isArray(value)) return value.forEach((item, index) => checkFieldNames(item, `${location}[${index}]`));
  if (!value || typeof value !== "object") return;
  for (const [key, child] of Object.entries(value)) {
    if (key.length > 18) fail(`${location}.${key}: field name exceeds 18 characters`);
    checkFieldNames(child, `${location}.${key}`);
  }
}
checkFieldNames(core);
for (const item of V2_LOCALES) checkFieldNames(bundle.locales[item]);

if (failures.length) {
  process.stderr.write(`${failures.join("\n")}\n`);
  process.exit(1);
}

process.stdout.write(`Activity V2 ok: core ${bytes(core)} bytes; locales ${V2_LOCALES.map((item) => `${item} ${bytes(bundle.locales[item])}`).join(", ")}; card ${bytes(activityCard)}; prep ${bytes(activityPrep)}; step ${bytes(sessionStep)}.\n`);
