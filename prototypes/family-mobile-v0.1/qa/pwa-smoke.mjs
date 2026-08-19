const artifactUrl = process.argv[2];
if (!artifactUrl) throw new Error("Usage: node pwa-smoke.mjs <http-artifact-url>");
if (!/^https?:\/\//.test(artifactUrl)) throw new Error("PWA smoke requires an HTTP(S) URL.");

const targetUrl = new URL(artifactUrl);
targetUrl.searchParams.set("reset", "1");
const expectedOfflineLabel = targetUrl.searchParams.get("lang") === "en" ? "Offline" : "Sin conexión";
const target = await fetch(`http://127.0.0.1:9222/json/new?${encodeURIComponent(targetUrl.href)}`, { method: "PUT" }).then((response) => response.json());
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
  if (message.method === "Runtime.exceptionThrown") {
    const details = message.params.exceptionDetails;
    runtimeErrors.push({
      description: details.exception?.description || details.text,
      url: details.url || "",
      executionContextId: details.executionContextId
    });
  }
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

await command("Page.enable");
await command("Runtime.enable");
await command("Network.enable");
await command("Page.navigate", { url: targetUrl.href });
await new Promise((resolve) => setTimeout(resolve, 900));
await evaluate(`navigator.serviceWorker.ready.then(() => true)`);
await command("Page.reload", { ignoreCache: false });
await new Promise((resolve) => setTimeout(resolve, 650));

await expect("Service worker controls the installed shell", `navigator.serviceWorker.controller !== null`);
await expect("Manifest exposes 192 and 512 pixel icons", `fetch(document.querySelector('link[rel="manifest"]').href).then((response) => response.json()).then((manifest) => manifest.display === 'standalone' && ['es-US','en-US'].includes(manifest.lang) && manifest.icons.some((icon) => icon.sizes === '192x192') && manifest.icons.some((icon) => icon.sizes === '512x512'))`);
await expect("App shell cache contains the bilingual core files", `caches.open('kids-founder-pilot-v3').then((cache) => cache.keys()).then((requests) => ['index.html','styles.css','i18n.js','app.js','manifest.es.webmanifest','manifest.en.webmanifest'].every((name) => requests.some((request) => request.url.endsWith(name))))`);
await evaluate(`window.dispatchEvent(new Event('offline')); true`);
await expect("Connectivity event updates the visible status", `document.body.textContent.includes(${JSON.stringify(expectedOfflineLabel)})`);
await evaluate(`window.dispatchEvent(new Event('online')); true`);

await command("Network.emulateNetworkConditions", { offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0 });
await command("Page.reload", { ignoreCache: false });
await new Promise((resolve) => setTimeout(resolve, 650));
await expect("Offline reload renders the family prototype", `document.querySelector('#app') !== null && document.body.textContent.includes('Kids Learning System')`);
await command("Network.emulateNetworkConditions", { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });

if (runtimeErrors.length) throw new Error(`Runtime exceptions: ${runtimeErrors.map((error) => `${error.description} [${error.url || `context ${error.executionContextId}`}]`).join('; ')}`);
console.log("PASS no runtime exceptions");
socket.close();
await fetch(`http://127.0.0.1:9222/json/close/${target.id}`).catch(() => {});
