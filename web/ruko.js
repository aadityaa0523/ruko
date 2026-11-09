// Shared by the guard app, the family screen and the landing page.
const $ = (id) => document.getElementById(id);
const LEVEL_TEXT = { safe: "Safe", watch: "Watching", high: "Likely scam", critical: "SCAM" };
const STAGE_LABELS = ["Pretends to be someone you trust", "Scares you or rushes you", "Cuts you off from family", "Asks for OTP, money or your phone"];

function renderStages(el, playbook) {
  const stages = playbook?.stages || STAGE_LABELS.map((label) => ({ label, done: false }));
  el.innerHTML = "";
  for (const s of stages) {
    const li = document.createElement("li");
    li.textContent = s.label;
    if (s.done) li.className = "done";
    el.append(li);
  }
}

// Highlight the phrases that raised a flag (best effort: Prisma's punctuation may differ).
function addCaption(el, text, risk, prefix) {
  const li = document.createElement("li");
  if (prefix) { const b = document.createElement("b"); b.textContent = prefix + " "; li.append(b); }
  const phrases = (risk?.flags || []).map((f) => f.phrase).filter((p) => p.length > 1);
  const lower = text.toLowerCase();
  const hits = [];
  for (const p of phrases) {
    const i = lower.indexOf(p);
    if (i >= 0) hits.push([i, i + p.length]);
  }
  hits.sort((a, b) => a[0] - b[0]);
  let pos = 0;
  for (const [a, b] of hits) {
    if (a < pos) continue;
    li.append(text.slice(pos, a));
    const m = document.createElement("mark"); m.textContent = text.slice(a, b); li.append(m);
    pos = b;
  }
  li.append(text.slice(pos));
  if (risk?.new?.length) li.className = "flagged";
  el.append(li);
  li.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function setLevel(el, risk) {
  el.dataset.level = risk.level;
  el.textContent = `${LEVEL_TEXT[risk.level]} · ${risk.score}/100`;
}
