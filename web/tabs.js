// Native-style bottom tab bar for the app screens (pages with <body class="app-shell" data-tab="...">).
(() => {
  const tab = document.body.dataset.tab;
  if (!tab) return;
  const hi = (document.documentElement.lang || "en") === "hi";
  const TABS = [
    { id: "guard", href: "/app/", en: "Guard", hi: "गार्ड",
      icon: '<path d="M12 2.5 4.5 5.6v5.6c0 4.6 3.1 8.7 7.5 10.3 4.4-1.6 7.5-5.7 7.5-10.3V5.6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m8.6 12 2.4 2.4 4.4-4.6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' },
    { id: "check", href: "/check/", en: "Check", hi: "जाँचें",
      icon: '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' },
    { id: "family", href: "/account/", en: "Family", hi: "परिवार",
      icon: '<circle cx="8.5" cy="8" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16.5" cy="9" r="2.6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M2.8 19.5c.6-3.4 2.9-5.3 5.7-5.3s5.1 1.9 5.7 5.3M14.2 14.6c.7-.4 1.5-.6 2.3-.6 2.3 0 4.2 1.5 4.7 4.6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>' },
  ];
  const nav = document.createElement("nav");
  nav.className = "tabbar";
  nav.setAttribute("aria-label", "Ruko");
  nav.innerHTML = TABS.map((t) => `<a href="${t.href}"${t.id === tab ? ' aria-current="page"' : ""}><svg viewBox="0 0 24 24" aria-hidden="true">${t.icon}</svg><span data-tab-label="${t.id}">${hi ? t.hi : t.en}</span></a>`).join("");
  document.body.append(nav);
  document.addEventListener("langchange", () => {
    const h = document.documentElement.lang === "hi";
    for (const t of TABS) nav.querySelector(`[data-tab-label="${t.id}"]`).textContent = h ? t.hi : t.en;
  });
})();
