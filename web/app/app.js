// Ruko guard app. Uses helpers from /ruko.js ($, renderStages, addCaption, setLevel).
let ws = null, audioCtx = null, stream = null, speaking = false, pending = new Int16Array(0), lastPack = null, lastRisk = null;

const store = {
  get(k, d) { try { return localStorage.getItem(k) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch {} },
};

// ---------- settings
const LANG_NAMES = { auto: "Auto", "hi-en": "Hinglish", "hi-IN": "हिन्दी", "kn-IN": "ಕನ್ನಡ", "te-IN": "తెలుగు", "ta-IN": "தமிழ்", "en-IN": "English" };
for (const id of ["lang", "model"]) {
  $(id).value = store.get("ruko." + id, $(id).value);
  $(id).onchange = () => { store.set("ruko." + id, $(id).value); $("langName").textContent = LANG_NAMES[$("lang").value]; };
}
for (const id of ["whisper", "elder"]) {
  $(id).checked = store.get("ruko." + id, "0") === "1";
  $(id).onchange = () => store.set("ruko." + id, $(id).checked ? "1" : "0");
}
$("langName").textContent = LANG_NAMES[$("lang").value];
$("settingsBtn").onclick = () => $("settings").showModal();
$("settingsDone").onclick = () => $("settings").close();

// ---------- Family Shield: a random code in a link; whoever has the link sees calls live
function newCode() {
  const a = crypto.getRandomValues(new Uint8Array(10));
  return Array.from(a, (b) => "abcdefghijkmnpqrstuvwxyz23456789"[b % 32]).join("");
}
let familyCode = store.get("ruko.family", "") || newCode();
store.set("ruko.family", familyCode);
const familyOn = () => store.get("ruko.familyOn", "1") === "1";
function familyLink() {
  const u = new URL("/family/", location.origin);
  u.searchParams.set("c", familyCode);
  const n = $("familyName").value.trim();
  if (n) u.searchParams.set("n", n);
  return u.href;
}
function refreshFamily() {
  $("familyLink").value = familyLink();
  $("familyWa").href = "https://wa.me/?text=" + encodeURIComponent(
    `I've turned on Ruko Family Shield. If I get a scam call, you'll see it live here: ${familyLink()}`);
  $("familyDot").style.background = familyOn() ? "" : "var(--line)";
}
$("familyName").value = store.get("ruko.name", "");
$("familyName").oninput = () => { store.set("ruko.name", $("familyName").value.trim()); refreshFamily(); };
$("familyOn").checked = familyOn();
$("familyOn").onchange = () => { store.set("ruko.familyOn", $("familyOn").checked ? "1" : "0"); refreshFamily(); };
$("familyNew").onclick = () => { familyCode = newCode(); store.set("ruko.family", familyCode); refreshFamily(); };
$("familyCopy").onclick = async () => {
  try { await navigator.clipboard.writeText(familyLink()); $("familyCopy").textContent = "Copied"; }
  catch { $("familyLink").select(); }
  setTimeout(() => ($("familyCopy").textContent = "Copy"), 2000);
};
$("familyBtn").onclick = async () => {
  refreshFamily();
  $("familyDlg").showModal();
  const v = await (await fetch(`/api/family/voice?c=${familyCode}`)).json().catch(() => ({}));
  $("familyVoice").textContent = v.has_voice
    ? `Warnings are spoken in ${v.name ? v.name + "'s" : "your family member's"} own voice.`
    : "Your family member can also record their voice on their screen, so the warning comes in a voice you trust.";
};
$("familyDone").onclick = () => $("familyDlg").close();
refreshFamily();

// Demo mode has no server-side call, so it forwards events to the family screen itself.
function toFamily(msg) {
  if (!familyOn()) return;
  fetch("/api/family/publish", { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: familyCode, msg }) }).catch(() => {});
}

// ---------- rendering
function setGuard(state, label, hint) {
  $("guard").dataset.state = state;
  if (label) $("listenLabel").innerHTML = label;
  if (hint) $("status").textContent = hint;
}

function showRisk(risk, text) {
  lastRisk = risk;
  setLevel($("level"), risk);
  renderStages($("stages"), risk.playbook);
  $("next").textContent = risk.playbook?.next || "";
  if (text !== undefined) addCaption($("captions"), text, risk);
  if (risk.level === "high" || risk.level === "critical") $("guard").dataset.state = "danger";
}

function alarm() {
  const r = lastRisk;
  $("toReason").textContent = r?.playbook?.next || "Cut the call now. Do not share any OTP or send money.";
  $("toFlags").textContent = r ? "Ruko heard: " + r.flags.map((f) => f.label).join(" · ") : "";
  $("takeover").hidden = false;
  $("takeover").classList.remove("flash"); void $("takeover").offsetWidth; $("takeover").classList.add("flash");
  navigator.vibrate?.([500, 200, 500, 200, 500]);
  $("toCut").focus();
}
$("toDismiss").onclick = () => ($("takeover").hidden = true);
$("toCut").onclick = () => { $("takeover").hidden = true; if (ws) $("hangup").click(); };

async function playWav(b64OrBlob) {
  const blob = typeof b64OrBlob === "string"
    ? new Blob([Uint8Array.from(atob(b64OrBlob), (c) => c.charCodeAt(0))], { type: "audio/wav" }) : b64OrBlob;
  const audio = new Audio(URL.createObjectURL(blob));
  speaking = true; // pause the mic so Ruko doesn't transcribe its own warning
  audio.onended = audio.onerror = () => { speaking = false; };
  await audio.play().catch(() => { speaking = false; });
}

function resetView() {
  $("captions").innerHTML = "";
  $("pack").hidden = true;
  $("takeover").hidden = true;
  showRisk({ level: "safe", score: 0, flags: [], new: [], playbook: null });
}

// ---------- live listening: mic (16 kHz PCM16, 1,024-byte frames) -> backend -> Gnani Prisma Realtime
const WORKLET = `class P extends AudioWorkletProcessor{process(i){const c=i[0][0];if(c)this.port.postMessage(c.slice(0));return true}}registerProcessor('pcm',P)`;

function sendPcm(floats) {
  const next = new Int16Array(pending.length + floats.length);
  next.set(pending);
  for (let i = 0; i < floats.length; i++) next[pending.length + i] = Math.max(-1, Math.min(1, floats[i])) * 0x7fff;
  let off = 0;
  while (next.length - off >= 512) {
    if (!speaking && ws?.readyState === WebSocket.OPEN) ws.send(next.slice(off, off + 512).buffer);
    off += 512;
  }
  pending = next.slice(off);
}

async function start() {
  resetView();
  const q = new URLSearchParams({ lang: $("lang").value, model: $("model").value,
    whisper: $("whisper").checked ? 1 : 0, elder: $("elder").checked ? 1 : 0 });
  if (familyOn()) q.set("family", familyCode);
  ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/listen?${q}`);
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.type === "connected") setGuard("listening", "Listening…", "Keep the call on speaker, close to this phone.");
    else if (m.type === "transcript") showRisk(m.risk, m.text);
    else if (m.type === "warning") { alarm(); if (m.audio) playWav(m.audio); }
    else if (m.type === "pack") showPack(m);
    else if (m.type === "diarized") showTimeline(m);
    else if (m.type === "done") $("audioNote").textContent = "Call audio has been deleted. Only this text report stays, on this phone.";
    else if (m.type === "error") $("status").textContent = "Problem: " + m.message;
  };
  ws.onclose = () => stop(false);
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, channelCount: 1 } });
  } catch {
    $("status").textContent = "Ruko needs the microphone to hear the call. Allow it and tap again.";
    return stop();
  }
  audioCtx = new AudioContext({ sampleRate: 16000 });
  await audioCtx.audioWorklet.addModule(URL.createObjectURL(new Blob([WORKLET], { type: "text/javascript" })));
  const node = new AudioWorkletNode(audioCtx, "pcm");
  node.port.onmessage = (e) => sendPcm(e.data);
  audioCtx.createMediaStreamSource(stream).connect(node);
  $("hangup").hidden = false;
  setGuard("listening", "Connecting…", "Connecting to Gnani Prisma…");
}

function stop(closeWs = true) {
  if (closeWs && ws?.readyState === WebSocket.OPEN) ws.close();
  ws = null;
  stream?.getTracks().forEach((t) => t.stop());
  audioCtx?.close();
  stream = audioCtx = null;
  pending = new Int16Array(0);
  $("hangup").hidden = true;
  setGuard($("guard").dataset.state === "danger" ? "danger" : "idle", "Protect<br>this call");
}

$("listen").onclick = () => (ws ? stop() : start());
$("hangup").onclick = () => {
  if (ws?.readyState !== WebSocket.OPEN) return;
  ws.send(JSON.stringify({ type: "hangup" }));
  stream?.getTracks().forEach((t) => t.stop());
  $("hangup").hidden = true;
  $("status").textContent = "Making your report…";
};

$("testVoice").onclick = async () => {
  const fam = familyOn() ? `&family=${familyCode}` : "";
  const r = await fetch(`/api/warning?lang=${$("lang").value}&whisper=${$("whisper").checked ? 1 : 0}&elder=${$("elder").checked ? 1 : 0}${fam}`);
  if (r.ok) playWav(await r.blob());
  else $("status").textContent = "Voice problem: " + (await r.text());
};

// ---------- sample calls (synthetic scripts, text only)
const SCRIPT_NAMES = {
  digital_arrest: "“CBI officer”: digital arrest", pm_kisan_kyc: "PM-Kisan installment stopped", army_kirana_order: "Army officer's big kirana order",
  fake_upi_refund: "“Sent by mistake” UPI refund", electricity_cut: "Electricity cut tonight", ayushman_card: "Ayushman card renewal",
  relative_in_custody: "Your son is at the police station", bank_kyc_screenshare: "Bank KYC + screen share", police_kannada: "Police call (Kannada)",
  bank_telugu: "Bank call (Telugu)", police_tamil: "Police call (Tamil)",
  cyber_branch_english: "Cyber crime branch (English)", card_bill_english: "Real card bill reminder (English)",
  tamil_family: "Family call (Tamil)", cbi_devanagari: "CBI call (Hindi)", real_bank_reminder: "Real bank EMI reminder",
  delivery_otp: "Real delivery OTP", doctor_appointment: "Doctor's appointment", family_surprise: "Family surprise party",
};
(async () => {
  const { scam, safe } = await (await fetch("/api/scripts")).json();
  for (const [group, scripts] of [["Scam calls", scam], ["Normal calls (should stay safe)", safe]]) {
    const og = document.createElement("optgroup");
    og.label = group;
    for (const name of Object.keys(scripts)) og.append(new Option(SCRIPT_NAMES[name] || name.replaceAll("_", " "), JSON.stringify(scripts[name])));
    $("script").append(og);
  }
  const health = await (await fetch("/api/health")).json();
  if (!health.gnani_key) $("status").textContent = "Live listening is off on this server (no Gnani key). Sample calls still work.";
})();

$("runScript").onclick = async () => {
  resetView();
  window.scrollTo({ top: 0, behavior: "smooth" });
  const lines = JSON.parse($("script").value);
  const { states, pack } = await (await fetch("/api/analyze", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lines, lang: $("lang").value }),
  })).json();
  toFamily({ type: "call_start", demo: true });
  setGuard("listening", "Sample<br>call", "Playing a made-up scam call…");
  for (let i = 0; i < lines.length; i++) {
    await new Promise((r) => setTimeout(r, 1600));
    showRisk(states[i], lines[i]);
    toFamily({ type: "transcript", text: lines[i], risk: states[i] });
    if (states[i].alert) { alarm(); toFamily({ type: "warning", level: states[i].level }); await new Promise((r) => setTimeout(r, 2500)); $("takeover").hidden = true; }
  }
  setGuard(pack.level === "high" || pack.level === "critical" ? "danger" : "idle", "Protect<br>this call");
  showPack(pack);
  toFamily({ type: "pack", ...pack });
  showTimeline({ error: "Sample calls have no audio, so voices aren't separated." });
};

// ---------- golden-hour pack
function showPack(p) {
  lastPack = p;
  $("pack").hidden = false;
  const bad = p.level === "high" || p.level === "critical";
  $("packTitle").textContent = bad ? "That was a scam. Your report is ready." : "Call over. No strong scam signs.";
  const c = p.complaint;
  $("fields").innerHTML = "";
  for (const [k, v] of [["Category", c.category], ["Type", c.sub_category], ["When", c.incident_datetime],
    ["Caller's number", c.suspect_phone_number], ["Amount lost", c.amount_lost]]) {
    const dt = document.createElement("dt"); dt.textContent = k;
    const dd = document.createElement("dd"); dd.textContent = v;
    $("fields").append(dt, dd);
  }
  $("complaint").textContent = c.description;
  $("familyBox").hidden = !p.family_alert;
  $("family").textContent = p.family_alert || "";
  $("timeline").innerHTML = '<li class="muted">Separating the caller\'s voice from yours (Gnani Prisma Batch)…</li>';
  $("status").textContent = bad ? "Call over. Report within the hour." : "Call over.";
  $("pack").scrollIntoView({ behavior: "smooth" });
}

function showTimeline(m) {
  $("timeline").innerHTML = "";
  if (m.error || !m.segments?.length) {
    const li = document.createElement("li"); li.className = "muted";
    li.textContent = m.error || "No speech found.";
    return $("timeline").append(li);
  }
  for (const s of m.segments) {
    const li = document.createElement("li");
    const who = m.caller === null ? `Voice ${s.speaker}` : s.speaker === m.caller ? "Caller" : "You";
    if (who === "Caller") li.className = "caller";
    const b = document.createElement("b"); b.textContent = who;
    li.append(b, ` ${Math.floor(s.start / 60)}:${String(Math.floor(s.start % 60)).padStart(2, "0")}  ${s.text}`);
    $("timeline").append(li);
  }
}

$("copy").onclick = async () => {
  const c = lastPack.complaint;
  const text = `Category: ${c.category}\nType: ${c.sub_category}\nWhen: ${c.incident_datetime}\n` +
    `Caller's number: ${c.suspect_phone_number}\nAmount lost: ${c.amount_lost}\n\n${c.description}`;
  try { await navigator.clipboard.writeText(text); $("copy").textContent = "Copied"; }
  catch { $("copy").textContent = "Select the text above to copy"; }
  setTimeout(() => ($("copy").textContent = "Copy complaint"), 2500);
};

$("playFamily").onclick = async () => {
  const r = await fetch("/api/family-voice", { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: lastPack.family_alert }) });
  if (r.ok) playWav(await r.blob());
};

// ---------- voice-note check (Gnani Prisma REST, <= 30 s)
$("clipCheck").onclick = async () => {
  const f = $("clipFile").files[0];
  if (!f) return ($("clipResult").textContent = "Choose an audio file first.");
  $("clipResult").textContent = "Listening with Gnani Prisma…";
  const fd = new FormData();
  fd.append("file", f);
  fd.append("lang", $("lang").value);
  const d = await (await fetch("/api/clip", { method: "POST", body: fd })).json();
  if (d.error) return ($("clipResult").textContent = "Problem: " + d.error);
  const verdict = { safe: "No scam signs", watch: "Be careful", high: "Likely a scam", critical: "This is a scam" }[d.risk.level];
  $("clipResult").textContent = `${verdict} (${d.risk.score}/100). Heard: “${d.transcript}”` +
    (d.risk.playbook?.next ? " · " + d.risk.playbook.next : "") + (d.truncated ? " · Only the first 30 seconds were checked." : "");
};

// ---------- keypad-phone calls Ruko joined over the phone network
async function loadCalls() {
  const calls = await (await fetch("/api/calls")).json();
  $("calls").innerHTML = calls.length ? "" : '<li class="muted small">No keypad-phone calls yet.</li>';
  for (const p of calls) {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.type = "button"; b.className = "btn";
    b.textContent = `${p.complaint.incident_datetime} · ${LEVEL_TEXT[p.level]} (${p.score}/100)`;
    b.onclick = () => { showPack(p); showTimeline({ error: "Ruko warned inside the phone call. Voices aren't separated for these." }); };
    li.append(b);
    $("calls").append(li);
  }
}
$("refreshCalls").onclick = loadCalls;
loadCalls();
resetView();
