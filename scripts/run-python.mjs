import { existsSync } from "node:fs";
import { spawnSync } from "node:child_process";
import path from "node:path";

const repositoryRoot = path.resolve(import.meta.dirname, "..");
const localPython =
  process.platform === "win32"
    ? path.join(repositoryRoot, ".venv", "Scripts", "python.exe")
    : path.join(repositoryRoot, ".venv", "bin", "python");

const python = process.env.KIDS_PYTHON || (existsSync(localPython) ? localPython : "python");
const result = spawnSync(python, process.argv.slice(2), {
  cwd: repositoryRoot,
  env: process.env,
  stdio: "inherit",
});

if (result.error) {
  console.error(`Unable to start Python (${python}): ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
