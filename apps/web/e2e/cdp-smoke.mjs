const baseUrl = process.argv[2] || "http://127.0.0.1:5173";
const cdpPort = process.argv[3] || "9223";
const target = await fetch(`http://127.0.0.1:${cdpPort}/json/new?${encodeURIComponent(baseUrl)}`, { method: "PUT" }).then((response) => response.json());
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => { socket.addEventListener("open", resolve, { once: true }); socket.addEventListener("error", reject, { once: true }); });

let sequence = 0;
const pending = new Map();
const runtimeErrors = [];
socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (message.method === "Runtime.exceptionThrown") runtimeErrors.push(message.params.exceptionDetails.exception?.description || message.params.exceptionDetails.text);
  if (!message.id || !pending.has(message.id)) return;
  const request = pending.get(message.id); pending.delete(message.id);
  if (message.error) request.reject(new Error(message.error.message)); else request.resolve(message.result);
});

function command(method, params = {}) {
  const id = ++sequence; socket.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}
async function evaluate(expression) {
  const result = await command("Runtime.evaluate", { expression, returnByValue: true, awaitPromise: true });
  if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
  return result.result.value;
}
async function expect(label, expression) {
  const passed = await evaluate(expression);
  if (!passed) throw new Error(`FAIL ${label}`);
  console.log(`PASS ${label}`);
}
async function waitFor(expression, timeout = 15000) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    if (await evaluate(expression)) return;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`Timed out: ${expression}`);
}
async function click(selector) {
  const result = await evaluate(`(() => { const item = document.querySelector(${JSON.stringify(selector)}); if (!item) return false; item.click(); return true; })()`);
  if (!result) throw new Error(`Missing control ${selector}`);
}

await command("Page.enable"); await command("Runtime.enable"); await command("Network.enable");
await command("Storage.clearDataForOrigin", { origin: new URL(baseUrl).origin, storageTypes: "all" });
await command("Emulation.setDeviceMetricsOverride", { width: 430, height: 932, screenWidth: 430, screenHeight: 932, deviceScaleFactor: 1, mobile: true });
await command("Page.navigate", { url: baseUrl });
await waitFor(`document.querySelector('.family-activity-card') !== null`);
await evaluate(`localStorage.setItem('kids.locale', 'en-US')`);
await evaluate(`navigator.serviceWorker?.ready.then(() => true)`);
await command("Page.reload", { ignoreCache: false });
await waitFor(`navigator.serviceWorker?.controller !== null && document.querySelector('.family-activity-card') !== null`);
await expect("page has meaningful content", `document.body.innerText.includes('Puente de papel')`);
await expect("no Vite error overlay", `document.querySelector('.vite-error-overlay') === null`);
await expect("companion is scoped to a running activity", `document.querySelectorAll('.companion-fab').length === 0`);
await expect("no horizontal overflow", `document.documentElement.scrollWidth <= innerWidth`);
await expect("risk C activity is absent from family catalog", `!document.body.innerText.includes('Probador de conductividad')`);
await evaluate(`(() => { const button=[...document.querySelectorAll('.family-nav button')].find(item=>item.textContent.includes('Explorar')); button.click(); return true; })()`);
await waitFor(`document.querySelectorAll('.family-activity-card').length === 12`);
await expect("twelve family-eligible activities are visible", `document.querySelectorAll('.family-activity-card').length === 12`);
await click(".family-activity-card .button.primary");
await waitFor(`document.querySelector('.preparation-shell') !== null`);
await expect("companion is available during preparation", `document.querySelectorAll('.companion-fab').length === 1`);
await expect("adult can review the exact version before starting", `document.body.innerText.includes('Revisa y adapta la actividad') && document.body.innerText.includes('ACT-0001@1.0.0')`);
await click(".preparation-ready .button.primary");
await waitFor(`document.querySelector('.gate-card') !== null`);
await expect("adult friction precedes session", `document.querySelectorAll('.gate-question').length === 3`);
await evaluate(`(() => { document.querySelectorAll('.gate-question').forEach(item => item.querySelector('input').click()); return true; })()`);
await click(".gate-card .button.primary");
await waitFor(`document.querySelector('.companion-fab') !== null`);
await expect("one companion entry button during session", `document.querySelectorAll('.companion-fab').length === 1`);
await waitFor(`document.querySelectorAll('.current-block > .block').length === 1`);
await expect("one current block only", `document.querySelectorAll('.current-block > .block').length === 1`);
await expect("exact version visible", `document.body.innerText.includes('ACT-0001@1.0.0')`);
await click(".companion-fab");
await evaluate(`(() => { const item = document.querySelector('#companion-message'); const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set; setter.call(item, 'Please adapt this activity to take less time'); item.dispatchEvent(new Event('input', {bubbles:true})); return true; })()`);
await click("#companion-panel form button");
await waitFor(`document.querySelectorAll('.proposal-option').length > 0`);
await expect("approved options rendered", `document.querySelectorAll('.proposal-option').length >= 1 && document.querySelectorAll('.proposal-option').length <= 3`);
await expect("mutation still awaits adult", `document.querySelector('.proposal-actions .primary') !== null`);
await click(".proposal-actions .primary");
await waitFor(`document.body.innerText.includes('La actividad fue actualizada.')`);
await expect("confirmed adaptation rerenders guide", `document.body.innerText.includes('Una versión corta y revisada')`);

await command("Network.emulateNetworkConditions", { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
await waitFor(`navigator.onLine === false`);
await expect("offline banner announces downloaded session", `document.body.innerText.includes('Sin conexión: esta sesión descargada sigue disponible.')`);
await click(".session-actions .button.primary");
await waitFor(`document.body.innerText.includes('Guardado de forma segura en este dispositivo')`);
await expect("offline progress advances locally", `document.querySelector('.session-header > span')?.textContent === '2/2'`);
await expect("encrypted queue and active session exist", `new Promise((resolve, reject) => { const request=indexedDB.open('kids-learning-private-v1'); request.onerror=()=>reject(request.error); request.onsuccess=()=>{const db=request.result;const tx=db.transaction('encrypted-records','readonly');const all=tx.objectStore('encrypted-records').getAll();all.onerror=()=>reject(all.error);all.onsuccess=()=>{const rows=all.result;resolve(rows.some(row=>row.id==='active-session'&&row.cipher instanceof ArrayBuffer)&&rows.some(row=>String(row.id).startsWith('event:'))&&rows.find(row=>row.id==='device-key')?.key?.extractable===false&&!rows.some(row=>'record' in row||'experience' in row));};};})`);
await expect("offline session is not copied to localStorage", `!Object.values(localStorage).some(value => String(value).includes('ACT-0001') || String(value).includes('sessionId'))`);

await command("Page.reload", { ignoreCache: false });
await waitFor(`document.querySelector('.session-shell') !== null`);
await expect("service worker restores the shell offline", `navigator.serviceWorker.controller !== null && document.body.innerText.includes('Versión exacta · ACT-0001@1.0.0')`);
await expect("encrypted session restores the current step", `document.querySelector('.session-header > span')?.textContent === '2/2'`);
await expect("offline reload has no error overlay", `document.querySelector('.vite-error-overlay') === null`);

await command("Network.emulateNetworkConditions", { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
await waitFor(`navigator.onLine === true`);
// CDP changes navigator.onLine but does not consistently emit the browser event.
await evaluate(`window.dispatchEvent(new Event('online'))`);
await waitFor(`!document.body.innerText.includes('cambio pendiente de sincronizar')`);
await expect("queued progress synchronizes after reconnect", `new Promise((resolve, reject) => { const request=indexedDB.open('kids-learning-private-v1'); request.onerror=()=>reject(request.error); request.onsuccess=()=>{const db=request.result;const tx=db.transaction('encrypted-records','readonly');const keys=tx.objectStore('encrypted-records').getAllKeys();keys.onerror=()=>reject(keys.error);keys.onsuccess=()=>resolve(!keys.result.some(key=>String(key).startsWith('event:')));};})`);

await command("Page.navigate", { url: `${baseUrl.replace(/\/$/, '')}/admin?lang=en-US` });
await waitFor(`document.querySelector('.admin-sidebar') !== null`);
await expect("bilingual admin workspace renders in English", `document.body.innerText.includes('Prioritized queue') && document.body.innerText.includes('ADMINISTRATIVE WORKSPACE')`);
await expect("owner navigation renders", `document.querySelectorAll('.admin-sidebar nav button').length >= 12`);
await evaluate(`(() => { const button = [...document.querySelectorAll('.admin-sidebar nav button')].find(item => item.textContent.includes('AI operations')); button.click(); return true; })()`);
await waitFor(`document.querySelectorAll('.route-table .table-row').length >= 14`);
await expect("routing matrix marks deterministic operations", `[...document.querySelectorAll('.route-table .table-row')].filter(item => item.textContent.includes('Does not use AI')).length >= 2`);
if (runtimeErrors.length) throw new Error(`Runtime exceptions: ${runtimeErrors.join("; ")}`);
console.log("PASS no runtime exceptions");
console.log("PASS end-to-end companion, offline restore, resync, and bilingual admin flow");
socket.close();
await fetch(`http://127.0.0.1:${cdpPort}/json/close/${target.id}`).catch(() => {});
