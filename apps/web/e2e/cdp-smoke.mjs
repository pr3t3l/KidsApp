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

await command("Page.enable"); await command("Runtime.enable");
await command("Emulation.setDeviceMetricsOverride", { width: 430, height: 932, screenWidth: 430, screenHeight: 932, deviceScaleFactor: 1, mobile: true });
await command("Page.navigate", { url: baseUrl });
await waitFor(`document.querySelector('.companion-fab') !== null`);
await expect("page has meaningful content", `document.body.innerText.includes('Paper Bridge')`);
await expect("no Vite error overlay", `document.querySelector('.vite-error-overlay') === null`);
await expect("one companion entry button", `document.querySelectorAll('.companion-fab').length === 1`);
await expect("no horizontal overflow", `document.documentElement.scrollWidth <= innerWidth`);
await click(".companion-fab");
await evaluate(`(() => { const item = document.querySelector('#companion-message'); const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set; setter.call(item, 'Please adapt this activity to take less time'); item.dispatchEvent(new Event('input', {bubbles:true})); return true; })()`);
await click("#companion-panel form button");
await waitFor(`document.querySelectorAll('.proposal-option').length > 0`);
await expect("approved options rendered", `document.querySelectorAll('.proposal-option').length >= 1 && document.querySelectorAll('.proposal-option').length <= 3`);
await expect("mutation still awaits adult", `document.body.innerText.includes('Nothing changes until you confirm')`);
await click(".proposal-actions .primary");
await waitFor(`document.body.innerText.includes('Your activity has been updated.')`);
await expect("confirmed adaptation rerenders guide", `document.body.innerText.includes('Test one change')`);
if (runtimeErrors.length) throw new Error(`Runtime exceptions: ${runtimeErrors.join("; ")}`);
console.log("PASS no runtime exceptions");
console.log("PASS end-to-end companion flow");
socket.close();
await fetch(`http://127.0.0.1:${cdpPort}/json/close/${target.id}`).catch(() => {});
