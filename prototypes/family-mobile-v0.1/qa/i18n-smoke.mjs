const artifactUrl = process.argv[2];
if (!artifactUrl) throw new Error("Usage: node i18n-smoke.mjs <artifact-url>");

const url = new URL(artifactUrl);
url.searchParams.set("lang", "en");
url.searchParams.set("reset", "1");
const target = await fetch(`http://127.0.0.1:9222/json/new?${encodeURIComponent(url.href)}`, { method: "PUT" }).then((response) => response.json());
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
  if (!await evaluate(expression)) throw new Error(`Failed: ${label}`);
  console.log(`PASS ${label}`);
}

async function act(expression) {
  await evaluate(expression);
  await new Promise((resolve) => setTimeout(resolve, 30));
}

const spanishWords = /\b(?:actividad|adulto|ahora|años|ayuda|cada|cerrar|como|compras|construir|crayones|cuando|debe|del|desde|descubrir|dispositivo|donde|el|ella|ellas|ellos|en|es|esta|estas|este|estos|explicar|familia|guardar|hasta|hoja|imaginar|la|las|listos|los|materiales|mejorar|niño|niños|observa|papel|para|pero|porque|preparación|puede|pueden|puente|seguridad|siguiente|solo|su|sus|también|todavía|un|una|uno|vaso|volver|y)\b|[áéíóúñ¿¡]/giu;
async function assertEnglish(label) {
  const snapshot = await evaluate(`(() => {
    const visible = document.body.innerText;
    const attributes = [...document.querySelectorAll('[aria-label],[title],[placeholder]')].flatMap((element) => ['aria-label','title','placeholder'].map((name) => element.getAttribute(name) || '')).join(' ');
    return visible + '\\n' + attributes;
  })()`);
  const matches = [...snapshot.matchAll(spanishWords)].map((match) => match[0]).filter((match) => match !== "ES");
  if (matches.length) throw new Error(`Spanish leak in ${label}: ${[...new Set(matches)].join(", ")}\n${snapshot}`);
  console.log(`PASS ${label} is fully English`);
}

await command("Page.enable");
await command("Runtime.enable");
await command("Network.enable");
await command("Network.clearBrowserCache");
await command("Storage.clearDataForOrigin", { origin: url.origin, storageTypes: "service_workers,cache_storage" });
await command("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, screenWidth: 390, screenHeight: 844, deviceScaleFactor: 1, mobile: true });
await command("Page.navigate", { url: url.href });
await new Promise((resolve) => setTimeout(resolve, 500));

await expect("English locale and global selector load", `document.documentElement.lang === 'en-US' && document.querySelector('[data-action="switch-language"]')?.textContent === 'ES'`);
await expect("Page metadata is localized", `document.title.includes('Family Mobile Prototype') && document.querySelector('meta[name="description"]')?.content.startsWith('Mobile prototype')`);
await expect("Install manifest follows the active language", `document.querySelector('link[rel="manifest"]')?.href.endsWith('manifest.en.webmanifest') && fetch(document.querySelector('link[rel="manifest"]').href).then((response) => response.json()).then((manifest) => manifest.lang === 'en-US' && manifest.start_url.includes('lang=en'))`);
await expect("English activity bundle has five activities and six bridge phases", `weeklyActivities.length === 5 && stages.length === 6 && weeklyActivities.every((activity) => activity.day.startsWith('DAY')) && stages[0].name === 'Discover'`);
await assertEnglish("Today");

for (const screen of ["focus", "prep", "journey", "family"]) {
  await act(`setScreen(${JSON.stringify(screen)})`);
  await assertEnglish(screen);
}

await act(`setScreen('plan'); state.planView = 'activities'; render()`);
await assertEnglish("five-day plan");
for (const day of ["day1", "day2", "day3", "day4", "day5"]) {
  await act(`state.selectedPlanDay = ${JSON.stringify(day)}; setScreen('planned-activity')`);
  await expect(`${day} contains a complete sequence`, `document.querySelectorAll('.planned-flow li').length === 6 && document.querySelector('.safety-card') !== null`);
  await assertEnglish(day);
}

await act(`setScreen('plan'); state.planView = 'shopping'; render()`);
await expect("English shopping list aggregates by three store sections", `document.querySelectorAll('.store-section').length === 3 && document.body.innerText.includes('Grocery Store') && document.body.innerText.includes('Stationery') && document.body.innerText.includes('Home')`);
await assertEnglish("shopping");

await act(`setScreen('session')`);
for (let stage = 0; stage < 6; stage += 1) {
  await act(`state.stage = ${stage}; render()`);
  await expect(`stage ${stage + 1} names every child`, `document.querySelectorAll('.named-action').length === 3`);
  await assertEnglish(`stage ${stage + 1}`);
  await act(`helpSheet()`);
  await assertEnglish(`stage ${stage + 1} help`);
  await act(`closeSheet()`);
}

await act(`setScreen('close')`);
await expect("English independence scale renders for all children", `document.querySelectorAll('.rating-card').length === 3 && document.body.innerText.includes('Independently and safely')`);
await assertEnglish("check-out");
await act(`noteSheet()`);
await assertEnglish("voice/text note sheet");
await act(`closeSheet(); learningDetailsSheet()`);
await assertEnglish("learning details sheet");
await act(`closeSheet(); pauseSheet()`);
await assertEnglish("pause sheet");
await act(`closeSheet(); installHelpSheet()`);
await assertEnglish("install instructions");
await act(`closeSheet(); state.ratings = {sofi: 4, mateo: 4, leo: 4}; setScreen('summary')`);
await assertEnglish("summary");
await act(`setScreen('saved')`);
await assertEnglish("saved confirmation");
await act(`setScreen('today'); document.querySelector('[data-action="connection-info"]').click()`);
await assertEnglish("connection sheet");
await act(`closeSheet(); showToast('Flujo opcional documentado; no se abre por defecto.')`);
await assertEnglish("toast feedback");

await act(`window.KidsI18n.setLocale('es')`);
await new Promise((resolve) => setTimeout(resolve, 400));
await expect("Language choice persists and Spanish returns", `document.documentElement.lang === 'es-US' && localStorage.getItem('kids-learning-system-locale') === 'es' && document.body.innerText.includes('Actividad sugerida')`);

if (runtimeErrors.length) throw new Error(`Runtime exceptions: ${runtimeErrors.join('; ')}`);
console.log("PASS no runtime exceptions");
socket.close();
await fetch(`http://127.0.0.1:9222/json/close/${target.id}`).catch(() => {});
