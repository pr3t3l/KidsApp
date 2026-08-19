import fs from "node:fs";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const ignoredDirectories = new Set([".git", "node_modules"]);

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    if (ignoredDirectories.has(entry.name)) return [];
    const absolutePath = path.join(directory, entry.name);
    if (entry.isDirectory()) return walk(absolutePath);
    return entry.isFile() && entry.name.endsWith(".md") ? [absolutePath] : [];
  });
}

function relative(absolutePath) {
  return path.relative(root, absolutePath).replaceAll("\\", "/");
}

const markdownFiles = walk(root);
const errors = [];

const canonicalEnglishRoots = [
  "AGENTS.md",
  "README.md",
  "docs",
  "schemas/README.md",
  "prototypes/family-mobile-v0.1/README.md",
];

function isCanonicalEnglishFile(file) {
  const name = relative(file);
  return canonicalEnglishRoots.some((candidate) =>
    candidate.endsWith(".md") ? name === candidate : name.startsWith(`${candidate}/`),
  );
}

const knownTranslationRegressions = [
  ["unspaced Markdown heading", /^#{1,6}[^ #\r\n]/m],
  ["two table rows joined together", / \|\| /],
  ["table delimiter joined to its first row", /^\|[-:| ]+\|\|/m],
  ["two Markdown list items joined together", /\.- (?=\*\*|[A-Z`])/],
  ["machine-translated exposure terminology", /\b(?:exhibition|exhibitions|exhibits)\b/i],
  ["obsolete Evaluate more wording", /\b(?:Rate More|Evaluate further)\b/i],
  ["machine-translated family UI wording", /\bfamiliar (?:UI|interface|application|app|instructions)\b/i],
  ["machine-translated media wording", /\btemporary means\b/i],
  ["known residual Spanish UI copy", /\b(?:Entender la actividad|Ajustar ritmo|Necesitan terminar|todos los contextos|privado\/autenticado)\b/i],
];

for (const file of markdownFiles) {
  const contents = fs.readFileSync(file, "utf8");
  const links = contents.matchAll(/\[[^\]]*\]\(([^)]+)\)/g);

  if (isCanonicalEnglishFile(file)) {
    for (const [label, pattern] of knownTranslationRegressions) {
      if (pattern.test(contents)) errors.push(`${relative(file)}: ${label}`);
    }
  }

  for (const match of links) {
    let target = match[1].trim();
    if (target.startsWith("<") && target.endsWith(">")) {
      target = target.slice(1, -1);
    }
    if (/^(?:https?:|mailto:|#)/i.test(target)) continue;

    const targetWithoutAnchor = target.split("#", 1)[0];
    if (!targetWithoutAnchor) continue;

    let decodedTarget;
    try {
      decodedTarget = decodeURIComponent(targetWithoutAnchor);
    } catch {
      errors.push(`${relative(file)}: invalid URL encoding in link ${target}`);
      continue;
    }

    const resolved = path.resolve(path.dirname(file), decodedTarget);
    if (!fs.existsSync(resolved)) {
      errors.push(`${relative(file)}: missing local link target ${target}`);
    }
  }
}

const pilotActivities = [
  "docs/02-content/sample-activities/ACT-0001-puente-de-papel.md",
  "docs/02-content/sample-activities/ACT-0002-clasificacion-semillas.md",
  "docs/02-content/sample-activities/ACT-0003-probador-conductividad.md",
];

const requiredActivitySignals = [
  ["draft status", /\*\*Status(?: \/ Status)?:\*\* Draft/i],
  ["Spanish localization", /es-US/],
  ["English locale", /en-US/],
  ["ages 5–10", /5[–-]10/],
  ["one primary objective", /objetivo principal|primary objective/i],
  ["Discover stage", /Discover/],
  ["Explain stage", /Explain/],
  ["materials", /materiales|materials/i],
  ["safety controls", /seguridad|safety|riesgos|risks/i],
  ["observation close-out", /observaci[oó]n|observation/i],
  ["visual briefs", /briefs? visual|visual briefs?/i],
  ["editorial gates", /gates?(?: editorial(?:es)?| and plan)|editorial gates?|GATE-[0-9]{2}/i],
];

for (const activityPath of pilotActivities) {
  const absolutePath = path.join(root, activityPath);
  if (!fs.existsSync(absolutePath)) {
    errors.push(`${activityPath}: required pilot activity is missing`);
    continue;
  }

  const contents = fs.readFileSync(absolutePath, "utf8");
  for (const [label, pattern] of requiredActivitySignals) {
    if (!pattern.test(contents)) {
      errors.push(`${activityPath}: missing ${label}`);
    }
  }
}

if (errors.length > 0) {
  process.stderr.write(`documentation validation failed (${errors.length})\n`);
  for (const error of errors) process.stderr.write(`- ${error}\n`);
  process.exitCode = 1;
} else {
  process.stdout.write(`documentation ok: ${markdownFiles.length} Markdown files and 3 pilot activities\n`);
}
