const artifactUrl = process.argv[2];
if (!artifactUrl) throw new Error("Usage: node flow-smoke.mjs <artifact-url>");
const cleanArtifactUrl = new URL(artifactUrl);
cleanArtifactUrl.searchParams.set("reset", "1");

const target = await fetch(`http://127.0.0.1:9222/json/new?${encodeURIComponent(cleanArtifactUrl.href)}`, { method: "PUT" }).then((response) => response.json());
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

let sequence = 0;
const pending = new Map();
const runtimeErrors = [];
socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (message.method === "Runtime.exceptionThrown") runtimeErrors.push(message.params.exceptionDetails.exception?.description || message.params.exceptionDetails.text);
  if (!message.id || !pending.has(message.id)) return;
  const request = pending.get(message.id);
  pending.delete(message.id);
  if (message.error) request.reject(new Error(message.error.message));
  else request.resolve(message.result);
});

function command(method, params = {}) {
  const id = ++sequence;
  socket.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

async function evaluate(expression) {
  const result = await command("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text);
  return result.result.value;
}

async function expect(label, expression) {
  const passed = await evaluate(expression);
  if (!passed) throw new Error(`Failed: ${label}`);
  console.log(`PASS ${label}`);
}

async function click(selector) {
  const clicked = await evaluate(`(() => { const element = document.querySelector(${JSON.stringify(selector)}); if (!element) return false; element.click(); return true; })()`);
  if (!clicked) throw new Error(`Missing control: ${selector}`);
  await new Promise((resolve) => setTimeout(resolve, 40));
}

await command("Page.enable");
await command("Runtime.enable");
await command("Emulation.setDeviceMetricsOverride", { width: 360, height: 800, screenWidth: 360, screenHeight: 800, deviceScaleFactor: 1, mobile: true });
await command("Page.navigate", { url: artifactUrl });
await new Promise((resolve) => setTimeout(resolve, 500));

await expect("Page declares an installable web manifest", `document.querySelector('link[rel="manifest"]') !== null`);
await expect("Today starts with three selected participants", `document.querySelectorAll('.participant.is-selected').length === 3`);
await click('[data-target="plan"]');
await expect("Plan exposes five navigable activities", `document.querySelectorAll('.plan-card').length === 5 && [...document.querySelectorAll('.plan-card')].every((item) => item.tagName === 'BUTTON')`);
await click('[data-action="open-plan-day"][data-id="day2"]');
await expect("Every planned activity opens a complete detail", `document.querySelector('.flow-header h1')?.textContent === 'Clasificar semillas' && document.querySelectorAll('.planned-flow li').length === 6 && document.body.textContent.includes('Seguridad y detención')`);
await click('[data-action="navigate"][data-target="plan"]');
await click('[data-action="plan-view"][data-value="shopping"]');
await expect("Shopping list is grouped by store section", `document.querySelectorAll('.store-section').length === 3 && document.body.textContent.includes('Supermercado') && document.body.textContent.includes('Papelería') && document.body.textContent.includes('Casa')`);
await expect("Consumables sum and reusable tools preserve provenance", `document.body.textContent.includes('13 vasos · Vasos de papel') && document.body.textContent.includes('DÍA 1: 1 vaso + DÍA 5: 12 vasos') && [...document.querySelectorAll('.shopping-item')].some((item) => item.textContent.includes('Marcador lavable') && item.textContent.includes('REUSA'))`);
await click('[data-action="shopping-item"][data-id="paper-cups"]');
await expect("Shopping checklist updates progress", `document.querySelector('.shopping-summary h2')?.textContent.startsWith('1 de ') && document.querySelector('[data-action="shopping-item"][data-id="paper-cups"]')?.checked === true`);
await click('[data-target="today"]');
await click('[data-target="focus"]');
await expect("Educational map opens", `document.querySelector('.flow-header h1')?.textContent === 'Qué van a explorar'`);
await expect("Every child has an explained learning focus", `document.querySelectorAll('.focus-card').length === 3 && document.body.textContent.includes('Por qué este foco')`);
await expect("Age-first focus mapping starts with Sofi counting and Mateo designing", `document.querySelectorAll('.focus-card')[0]?.textContent.includes('Conteo uno a uno') && document.querySelectorAll('.focus-card')[1]?.textContent.includes('Diseñar y probar una forma')`);
await expect("Focus screen omits configuration meta-copy", `!document.body.textContent.includes('No tienes que configurar nada')`);
await expect("Normal flow has no role-swap control", `document.querySelector('[data-action="edit-role"]') === null && document.querySelector('[data-action="change-during"]') === null`);
await expect("Learning map avoids a redundant details step", `document.querySelector('[data-action="learning-details"]') === null && document.querySelector('.learning-primary')?.textContent.includes('Ingeniería')`);
await click('[data-target="prep"]');
await expect("Preparation integrates material functions", `document.querySelector('.checklist')?.textContent.includes('Mantiene los crayones reunidos') && document.querySelector('.checklist')?.textContent.includes('Amortigua la caída') && document.querySelector('.material-purpose-card') === null`);
await expect("Preparation blocks start until every item is checked", `document.querySelector('[data-action="start-session"]')?.disabled === true`);
for (const materialId of ["cup", "ruler", "marker", "towel", "surface"]) await click(`[data-action="material"][data-id="${materialId}"]`);
await expect("Preparation enables start", `document.querySelector('[data-action="start-session"]')?.disabled === false`);
await click('[data-action="start-session"]');
await expect("Session begins at Discover", `document.querySelector('.stage-button.is-current strong')?.textContent.includes('Descubrir')`);
await expect("Session names every child and gives adult script", `document.querySelectorAll('.named-action').length === 3 && document.querySelector('.say-box')?.textContent.includes('Diles')`);
await expect("Discover performs a real baseline and shows its transition", `document.querySelector('.adult-actions')?.textContent.includes('Centra el vaso vacío') && document.querySelector('.stage-brief')?.textContent.includes('resultado real') && document.querySelector('.step-checks')?.textContent.includes('resultado de referencia')`);
await expect("Stage uses one progress signal and action-first layout", `document.querySelector('.step-progress') === null && document.querySelector('.stage-visual.descubrir') !== null && document.querySelector('.facilitation-block h3')?.textContent.includes('Haz esto')`);
await click('[data-action="help"]');
await expect("Contextual help explains problem, impact, resume, and limit", `document.querySelector('#sheet')?.textContent.includes('Impacto') && document.querySelector('#sheet')?.textContent.includes('Reanuda')`);
await click('[data-action="use-support"][data-value="0"]');
await expect("Chosen support appears in the step", `document.querySelector('.applied-support') !== null`);
await click('[data-action="stage"][data-value="2"]');
await expect("Build gives every child a personal structure", `document.querySelector('.stage-brief h2')?.textContent.includes('Cada niño construye') && [...document.querySelectorAll('.named-action p')].every((item) => item.textContent.includes('propia'))`);
await click('[data-action="stage"][data-value="3"]');
await expect("Experiment gives every child a personal test", `document.querySelector('.stage-brief h2')?.textContent.includes('cada puente por separado') && document.querySelector('.turn-order')?.textContent.includes('Sofi → Mateo → Leo') && [...document.querySelectorAll('.named-action p')].every((item) => item.textContent.includes('propio'))`);
await click('[data-action="stage"][data-value="0"]');
for (let index = 0; index < 6; index += 1) await click('[data-action="next-stage"]');
await expect("Close contains three contextual ratings", `document.querySelectorAll('.rating-card').length === 3`);
await expect("Close has no visible timer or redundant receipt step", `document.querySelector('.timer') === null && document.body.textContent.includes('Guardar y terminar') && !document.body.textContent.includes('Ver lo que se guardará')`);
for (const learnerId of ["sofi", "mateo", "leo"]) await click(`[data-action="rating"][data-id="${learnerId}"][data-value="4"]`);
await expect("Three ratings enable close", `document.querySelector('[data-action="complete-close"]')?.disabled === false`);
await click('[data-action="complete-close"]');
await expect("Direct close reaches saved state", `document.body.textContent.includes('Sigan con su tarde') && !document.body.textContent.includes('El cierre tomó')`);
await expect("Operational progress is persisted locally", `(() => { const saved = JSON.parse(localStorage.getItem('kids-learning-system-founder-pilot-v1') || 'null'); return saved?.version === 1 && saved.state?.shoppingChecked?.['paper-cups'] === true && saved.state?.screen === 'saved'; })()`);
await command("Page.reload", { ignoreCache: false });
await new Promise((resolve) => setTimeout(resolve, 450));
await expect("Reload restores the saved screen", `document.body.textContent.includes('Sigan con su tarde')`);

if (runtimeErrors.length) throw new Error(`Runtime exceptions: ${runtimeErrors.join('; ')}`);
console.log("PASS no runtime exceptions");
socket.close();
await fetch(`http://127.0.0.1:9222/json/close/${target.id}`).catch(() => {});
