const CACHE = "kids-system-v3";
const SHELL = ["/", "/admin", "/welcome", "/privacy", "/terms", "/safety", "/index.html", "/manifest.webmanifest", "/icon.svg"];
self.addEventListener("install", (event) => event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL))));
self.addEventListener("activate", (event) => event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))));
self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  const privatePath = ["/v1/", "/rest/", "/auth/", "/storage/", "/realtime/"].some((prefix) => url.pathname.startsWith(prefix));
  if (event.request.method !== "GET" || url.origin !== self.location.origin || privatePath) return;
  const navigation = event.request.mode === "navigate";
  const staticAsset = /\.(?:js|css|svg|png|webp|woff2?|webmanifest)$/.test(url.pathname);
  if (!navigation && !staticAsset) return;
  event.respondWith(fetch(event.request).then((response) => {
    const cacheable = response.ok && response.type === "basic" && !/no-store|private/i.test(response.headers.get("Cache-Control") || "");
    if (cacheable) caches.open(CACHE).then((cache) => cache.put(event.request, response.clone()));
    return response;
  }).catch(async () => (await caches.match(event.request)) || (navigation ? caches.match("/index.html") : Response.error())));
});
