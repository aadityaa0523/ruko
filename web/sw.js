// Ruko service worker: makes the app installable and keeps the shell available on a weak network.
// Live listening always needs the network; only static files are cached.
const CACHE = "ruko-v42";
const SHELL = ["/app/", "/check/", "/check/check.js", "/check/check.css", "/app/app.css", "/app/app.js", "/ruko.css", "/ruko.js", "/tabs.js", "/fonts/fonts.css", "/icon.svg"];

self.addEventListener("install", (e) => e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", (e) => e.waitUntil(
  caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin || url.pathname.startsWith("/api/") || url.pathname.startsWith("/ws/")) return;
  // network first, cache as fallback
  e.respondWith(fetch(e.request).then((r) => {
    if (r.ok) { const copy = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, copy)); }
    return r;
  }).catch(() => caches.match(e.request)));
});

// Family Shield push alerts
self.addEventListener("push", (e) => {
  let d = {};
  try { d = e.data.json(); } catch { d = { title: "Ruko", body: e.data?.text() || "" }; }
  e.waitUntil(self.registration.showNotification(d.title || "Ruko", {
    body: d.body || "", icon: "/icon-192.png", badge: "/icon-192.png", tag: d.tag || "ruko", renotify: true,
    requireInteraction: true, vibrate: [400, 150, 400, 150, 400], data: { url: d.url || "/" },
  }));
});
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window" }).then((list) => {
    const target = e.notification.data?.url || "/";
    for (const c of list) if (c.url.includes(target) && "focus" in c) return c.focus();
    return self.clients.openWindow(target);
  }));
});
