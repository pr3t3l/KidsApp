import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const root = process.cwd();
const validateExamples = process.argv.includes("--examples");
const contracts = [
  {
    name: "ActivityVersion",
    schema: "schemas/v0.1/activity-version.schema.json",
    example: "schemas/examples/activity-version.example.json",
  },
  {
    name: "ActivitySession",
    schema: "schemas/v0.1/session.schema.json",
    example: "schemas/examples/session.example.json",
  },
  {
    name: "LearnerRecords",
    schema: "schemas/v0.1/learner-records.schema.json",
    example: "schemas/examples/learner-records.example.json",
  },
  {
    name: "OfflinePackManifest",
    schema: "schemas/v0.1/offline-pack-manifest.schema.json",
    example: "schemas/examples/offline-pack-manifest.example.json",
  },
  {
    name: "SyncEvent",
    schema: "schemas/v0.1/sync-event.schema.json",
    examples: [
      "schemas/examples/sync-event.example.json",
      "schemas/examples/sync-event-conflict.example.json",
    ],
  },
];

const readJson = (relativePath) => {
  const absolutePath = path.join(root, relativePath);
  return JSON.parse(fs.readFileSync(absolutePath, "utf8"));
};

const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);

let failed = false;

for (const contract of contracts) {
  try {
    const schema = readJson(contract.schema);
    const validate = ajv.compile(schema);
    process.stdout.write(`schema ok: ${contract.name}\n`);

    if (validateExamples) {
      const examples = contract.examples ?? [contract.example];
      for (const examplePath of examples) {
        const example = readJson(examplePath);
        const valid = validate(example);
        if (!valid) {
          failed = true;
          process.stderr.write(`example failed: ${contract.name} (${examplePath})\n`);
          process.stderr.write(`${JSON.stringify(validate.errors, null, 2)}\n`);
        } else {
          process.stdout.write(`example ok: ${contract.name} (${examplePath})\n`);
        }
      }
    }
  } catch (error) {
    failed = true;
    process.stderr.write(`validation error: ${contract.name}\n${error.stack ?? error}\n`);
  }
}

if (failed) {
  process.exitCode = 1;
}
