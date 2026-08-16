const artifactUrl = process.argv[2];
if (!artifactUrl) throw new Error("Usage: node flow-smoke.mjs <artifact-url>");

const target = await fetch(`http://127.0.0.1:9222/json/new?${encodeURIComponent(artifactUrl)}`, { method: "PUT" }).then((response) => response.json());
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
  if (message.method === "Runtime.exceptionThrown") runtimeErrors.push(message.params.exceptionDetails.text);
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

await expect("Today starts with three selected participants", `document.querySelectorAll('.participant.is-selected').length === 3`);
await click('[data-target="roles"]');
await expect("Role review opens", `document.querySelector('.flow-header h1')?.textContent === 'Plan del equipo'`);
await click('[data-action="edit-role"][data-id="sofi"]');
await click('[data-action="choose-observer"][data-id="sofi"]');
await expect("Observer mode removes the evaluated objective", `document.body.textContent.includes('No se infiere habilidad')`);
await click('[data-action="edit-role"][data-id="sofi"]');
await click('[data-action="choose-role"][data-id="sofi"][data-value="designer"]');
await expect("Role can be restored", `document.body.textContent.includes('Diseñadora y constructora')`);
await click('[data-target="prep"]');
await expect("Preparation blocks start until every item is checked", `document.querySelector('[data-action="start-session"]')?.disabled === true`);
await click('[data-action="material"][data-id="cup"]');
await click('[data-action="material"][data-id="surface"]');
await expect("Preparation enables start", `document.querySelector('[data-action="start-session"]')?.disabled === false`);
await click('[data-action="start-session"]');
await expect("Session begins at Discover", `document.querySelector('.stage-button.is-current strong')?.textContent.includes('Descubrir')`);
await click('[data-action="help"]');
await expect("Contextual help contains safe restart guidance", `document.querySelector('#sheet')?.textContent.includes('no es un error') || document.querySelector('#sheet')?.textContent.includes('separen')`);
await click('[data-action="close-sheet"]');
for (let index = 0; index < 6; index += 1) await click('[data-action="next-stage"]');
await expect("Close contains three contextual ratings", `document.querySelectorAll('.rating-card').length === 3`);
for (const learnerId of ["sofi", "mateo", "leo"]) await click(`[data-action="rating"][data-id="${learnerId}"][data-value="4"]`);
await expect("Three ratings enable close", `document.querySelector('[data-action="complete-close"]')?.disabled === false`);
await click('[data-action="complete-close"]');
await expect("Receipt explains uncertainty", `document.body.textContent.includes('Una sola sesión nunca determina')`);
await click('[data-action="save-session"]');
await expect("Session reaches saved state", `document.body.textContent.includes('Sigan con su tarde')`);

if (runtimeErrors.length) throw new Error(`Runtime exceptions: ${runtimeErrors.join('; ')}`);
console.log("PASS no runtime exceptions");
socket.close();
