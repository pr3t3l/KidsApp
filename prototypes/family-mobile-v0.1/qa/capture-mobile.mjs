import { writeFile } from "node:fs/promises";

const [url, output, widthText, heightText] = process.argv.slice(2);
const width = Number(widthText);
const height = Number(heightText);

if (!url || !output || !width || !height) {
  throw new Error("Usage: node capture-mobile.mjs <url> <output> <width> <height>");
}

const target = await fetch(`http://127.0.0.1:9222/json/new?${encodeURIComponent(url)}`, { method: "PUT" }).then((response) => response.json());
const socket = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

let sequence = 0;
const pending = new Map();
socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (!message.id || !pending.has(message.id)) return;
  const { resolve, reject } = pending.get(message.id);
  pending.delete(message.id);
  if (message.error) reject(new Error(message.error.message));
  else resolve(message.result);
});

function command(method, params = {}) {
  const id = ++sequence;
  socket.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

await command("Page.enable");
await command("Emulation.setDeviceMetricsOverride", {
  width,
  height,
  screenWidth: width,
  screenHeight: height,
  deviceScaleFactor: 1,
  mobile: true,
  screenOrientation: { angle: 0, type: "portraitPrimary" }
});
await command("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
await command("Page.navigate", { url });
await new Promise((resolve) => setTimeout(resolve, 700));
const layout = await command("Runtime.evaluate", {
  expression: `JSON.stringify({
    viewport: { width: innerWidth, height: innerHeight },
    documentWidth: document.documentElement.scrollWidth,
    appWidth: document.querySelector('#app')?.getBoundingClientRect().width,
    screen: new URLSearchParams(location.search).get('screen')
  })`,
  returnByValue: true
});
const capture = await command("Page.captureScreenshot", {
  format: "png",
  fromSurface: true,
  captureBeyondViewport: false
});
await writeFile(output, Buffer.from(capture.data, "base64"));
console.log(layout.result.value);
socket.close();
