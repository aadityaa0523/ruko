// Ruko guard app. Uses helpers from /ruko.js ($, store, t, renderStages, addCaption, setLevel).
// UI text. English is the default; Hindi is a full translation of the main flow.
window.STRINGS = {
  en: {
    protect: "Protect this call", listening: "Listening…", connecting: "Connecting…", sample: "Sample call",
    hint: "Put the call on speaker and keep this device next to it, then tap. Phones can't share the microphone during a call, so use a second phone or tablet, or the keypad-phone line.",
    listening_hint: "Keep the call on speaker, close to this device.", connecting_hint: "Connecting to Gnani Prisma…",
    sample_hint: "Playing a made-up scam call…", making_report: "Making your report…", problem: "Problem: ",
    need_mic: "Ruko needs the microphone to hear the call. Allow it and tap again.",
    no_key: "Live listening is off on this server. Sample calls still work.",
    audio_deleted: "Call audio has been deleted. Only this text report stays, on this phone.",
    separating: "Separating the caller's voice from yours (Gnani Prisma Batch)…",
    over_bad: "Call over. Report within the hour.", over: "Call over.",
    pack_bad: "That was a scam. Your report is ready.", pack_ok: "Call over. No strong scam signs.",
    copied: "Copied", copy: "Copy complaint", copy_link: "Copy", select_copy: "Select the text above to copy",
    choose_file: "Choose an audio file first.", checking: "Listening with Gnani Prisma…", no_calls: "No keypad-phone calls yet.",
    cut_now: "Cut the call now. Do not share any OTP or send money.", heard: "Ruko heard: ",
    empty: "Words appear here as the call goes on. Scam phrases turn red.",
  },
  hi: {
    protect: "इस कॉल को सुरक्षित करें", listening: "सुन रहा है…", connecting: "जुड़ रहा है…", sample: "नमूना कॉल",
    hint: "कॉल स्पीकर पर रखें, यह डिवाइस उसके पास रखें, फिर दबाएँ। कॉल के दौरान फ़ोन माइक्रोफ़ोन साझा नहीं करते, इसलिए दूसरा फ़ोन या टैबलेट इस्तेमाल करें, या कीपैड-फ़ोन लाइन।",
    listening_hint: "कॉल स्पीकर पर रखें, इस फ़ोन के पास।", connecting_hint: "Gnani Prisma से जुड़ रहा है…",
    sample_hint: "एक नक़ली धोखे वाली कॉल चल रही है…", making_report: "आपकी रिपोर्ट बन रही है…", problem: "दिक़्क़त: ",
    need_mic: "कॉल सुनने के लिए Ruko को माइक्रोफ़ोन चाहिए। अनुमति दें और फिर दबाएँ।",
    no_key: "इस सर्वर पर लाइव सुनना बंद है। नमूना कॉल चलती हैं।",
    audio_deleted: "कॉल की आवाज़ मिटा दी गई है। सिर्फ़ यह लिखित रिपोर्ट इसी फ़ोन पर है।",
    separating: "कॉलर की आवाज़ आपकी आवाज़ से अलग की जा रही है…",
    over_bad: "कॉल ख़त्म। एक घंटे के अंदर रिपोर्ट करें।", over: "कॉल ख़त्म।",
    pack_bad: "यह धोखा था। आपकी रिपोर्ट तैयार है।", pack_ok: "कॉल ख़त्म। धोखे के पक्के संकेत नहीं मिले।",
    copied: "कॉपी हो गया", copy: "शिकायत कॉपी करें", copy_link: "कॉपी", select_copy: "ऊपर का टेक्स्ट चुनकर कॉपी करें",
    choose_file: "पहले एक ऑडियो फ़ाइल चुनें।", checking: "Gnani Prisma से सुन रहा है…", no_calls: "अभी कोई कीपैड-फ़ोन कॉल नहीं।",
    cut_now: "अभी कॉल काटिए। कोई OTP न बताएँ, पैसे न भेजें।", heard: "Ruko ने सुना: ",
    empty: "कॉल के दौरान शब्द यहाँ दिखेंगे। धोखे वाले शब्द लाल होंगे।",
    how_far: "धोखा कितना आगे बढ़ा", said: "कॉलर ने क्या कहा", hangup: "कॉल ख़त्म: मेरी रिपोर्ट बनाएँ",
    golden: "एक घंटे के अंदर रिपोर्ट करें। जितनी जल्दी, पैसे रुकने की उतनी उम्मीद।", call1930: "अभी 1930 पर कॉल करें",
    complaint: "शिकायत, चिपकाने के लिए तैयार", fam_msg: "परिवार के लिए संदेश", play_it: "सुनाएँ", who: "किसने क्या कहा",
    try: "एक नमूना धोखा कॉल चलाएँ", nomic: "माइक्रोफ़ोन नहीं चाहिए", try_p: "एक लिखी हुई नक़ली कॉल Ruko से चलती है ताकि आप देख सकें क्या होता है।",
    play: "चलाएँ", voice_note: "वॉइस नोट जाँचें", voice_note_p: "अजीब WhatsApp वॉइस नोट या रिकॉर्डिंग? Ruko पहले 30 सेकंड जाँचता है।", check: "जाँचें",
    keypad: "कीपैड फ़ोन की कॉल", keypad_p: "बेसिक फ़ोन पर कॉल को Ruko के नंबर से जोड़ें। Ruko कॉल के अंदर चेतावनी देता है।", refresh: "रीफ़्रेश",
    foot: "Ruko सिर्फ़ चेतावनी देता है। कॉल नहीं रोकता, आवाज़ नहीं रखता। पैसे गए? 1930 पर कॉल करें।",
    to_title: "यह धोखा है। कॉल काटिए।", to_cut: "मैंने कॉल काट दी", to_keep: "सुनते रहें",
    settings: "सेटिंग्स", speaks_in: "Ruko किस भाषा में बोले", elder: "धीरे बोले, रुक-रुककर (बुज़ुर्गों के लिए)", whisper: "चेतावनी फुसफुसाकर, ताकि कॉलर कम सुने",
    engine: "स्पीच इंजन", hear: "चेतावनी सुनें", done: "हो गया",
    fam_p: "यह लिंक अपने बेटे, बेटी या भरोसेमंद पड़ोसी को भेजें। कॉल धोखे में बदलते ही उनके फ़ोन पर दिखेगा, ताकि वे कॉल करके उसे तोड़ सकें।",
    your_name: "आपका नाम (उन्हें दिखेगा)", name_ph: "जैसे मम्मी", fam_link: "फ़ैमिली लिंक", share: "मेरी कॉल इस लिंक से साझा करें",
    wa: "WhatsApp पर भेजें", new_link: "नया लिंक बनाएँ",
  },
};
for (const el of document.querySelectorAll("[data-i18n]")) STRINGS.en[el.dataset.i18n] ??= el.textContent;
let ws = null, audioCtx = null, stream = null, speaking = false, pending = new Int16Array(0), lastPack = null, lastRisk = null;


// ---------- settings
const LANG_NAMES = { auto: "Auto", "hi-en": "Hinglish", "hi-IN": "हिन्दी", "kn-IN": "ಕನ್ನಡ", "te-IN": "తెలుగు", "ta-IN": "தமிழ்", "en-IN": "English", "mr-IN": "मराठी", "bn-IN": "বাংলা", "gu-IN": "ગુજરાતી", "ml-IN": "മലയാളം" };
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
{
  const q = new URLSearchParams(location.search);
  if (/^[a-z0-9]{8,16}$/.test(q.get("f") || "")) {
    store.set("ruko.family", q.get("f")); store.set("ruko.familyOn", "1");
    if (q.get("n")) store.set("ruko.name", q.get("n").slice(0, 30));
    history.replaceState(null, "", "/app/");
  }
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
  try { await navigator.clipboard.writeText(familyLink()); $("familyCopy").textContent = t("copied"); }
  catch { $("familyLink").select(); }
  setTimeout(() => ($("familyCopy").textContent = t("copy_link")), 2000);
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
  if (label) $("listenLabel").textContent = t(label);
  if (hint) $("status").textContent = t(hint);
}

function showRisk(risk, text) {
  lastRisk = risk;
  setLevel($("level"), risk);
  renderStages($("stages"), risk.playbook);
  $("next").textContent = risk.playbook?.next || "";
  $("next").parentElement.classList.toggle("now", risk.level === "critical");
  if (text !== undefined) addCaption($("captions"), text, risk);
  if (risk.level === "high" || risk.level === "critical") $("guard").dataset.state = "danger";
}

let logged = new Set();
function logAlert(risk, source) {
  if (!familyOn() || !risk || logged.has(risk.level) || typeof sbInsert !== "function") return;
  logged.add(risk.level);
  const stages = (risk.playbook?.stages || []).filter((s) => s.done).map((s) => s.key);
  sbInsert("alerts", { code: familyCode, level: risk.level, stages, source }).catch(() => {});  // unknown codes are rejected; that is fine
}

function alarm() {
  const r = lastRisk;
  $("toOct").innerHTML = octagonSVG();
  $("toReason").textContent = r?.playbook?.next || t("cut_now");
  $("toFlags").textContent = r ? t("heard") + r.flags.map((f) => f.label).join(", ") : "";
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
  logged = new Set();
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
    if (m.type === "connected") setGuard("listening", "listening", "listening_hint");
    else if (m.type === "transcript") showRisk(m.risk, m.text);
    else if (m.type === "warning") { logAlert(lastRisk, "speaker"); alarm(); if (m.audio) playWav(m.audio); }
    else if (m.type === "pack") showPack(m);
    else if (m.type === "diarized") showTimeline(m);
    else if (m.type === "done") $("audioNote").textContent = t("audio_deleted");
    else if (m.type === "error") $("status").textContent = t("problem") + m.message;
  };
  ws.onclose = () => stop(false);
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, channelCount: 1 } });
  } catch {
    $("status").textContent = t("need_mic");
    return stop();
  }
  audioCtx = new AudioContext({ sampleRate: 16000 });
  await audioCtx.audioWorklet.addModule(URL.createObjectURL(new Blob([WORKLET], { type: "text/javascript" })));
  const node = new AudioWorkletNode(audioCtx, "pcm");
  node.port.onmessage = (e) => sendPcm(e.data);
  audioCtx.createMediaStreamSource(stream).connect(node);
  $("hangup").hidden = false;
  setGuard("listening", "connecting", "connecting_hint");
}

function stop(closeWs = true) {
  if (closeWs && ws?.readyState === WebSocket.OPEN) ws.close();
  ws = null;
  stream?.getTracks().forEach((t) => t.stop());
  audioCtx?.close();
  stream = audioCtx = null;
  pending = new Int16Array(0);
  $("hangup").hidden = true;
  setGuard($("guard").dataset.state === "danger" ? "danger" : "idle", "protect");
}

$("listen").onclick = () => (ws ? stop() : start());
$("hangup").onclick = () => {
  if (ws?.readyState !== WebSocket.OPEN) return;
  ws.send(JSON.stringify({ type: "hangup" }));
  stream?.getTracks().forEach((t) => t.stop());
  $("hangup").hidden = true;
  $("status").textContent = t("making_report");
};

$("testVoice").onclick = async () => {
  const fam = familyOn() ? `&family=${familyCode}` : "";
  const r = await fetch(`/api/warning?lang=${$("lang").value}&whisper=${$("whisper").checked ? 1 : 0}&elder=${$("elder").checked ? 1 : 0}${fam}`);
  if (r.ok) playWav(await r.blob());
  else $("status").textContent = t("problem") + (await r.text());
};

// ---------- sample calls (synthetic scripts, text only)
const SCRIPT_NAMES = {
  digital_arrest: "“CBI officer”: digital arrest", pm_kisan_kyc: "PM-Kisan installment stopped", army_kirana_order: "Army officer's big kirana order",
  fake_upi_refund: "“Sent by mistake” UPI refund", electricity_cut: "Electricity cut tonight", ayushman_card: "Ayushman card renewal",
  relative_in_custody: "Your son is at the police station", bank_kyc_screenshare: "Bank KYC + screen share", police_kannada: "Police call (Kannada)",
  bank_telugu: "Bank call (Telugu)", police_tamil: "Police call (Tamil)",
  cyber_branch_english: "Cyber crime branch (English)", card_bill_english: "Real card bill reminder (English)",
  tamil_family: "Family call (Tamil)", cbi_devanagari: "CBI call (Hindi)", police_marathi: "Police call (Marathi)", bank_bengali: "Bank call (Bengali)",
  police_gujarati: "Police call (Gujarati)", bank_malayalam: "Bank call (Malayalam)", marathi_family: "Family call (Marathi)", bengali_family: "Family call (Bengali)", real_bank_reminder: "Real bank EMI reminder",
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
  if (!health.gnani_key) $("status").textContent = t("no_key");
})();

$("runScript").onclick = async () => {
  resetView();
  window.scrollTo({ top: 0, behavior: "smooth" });
  const lines = JSON.parse($("script").value);
  const { states, pack } = await (await fetch("/api/analyze", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lines, lang: $("lang").value }),
  })).json();
  toFamily({ type: "call_start", demo: true });
  setGuard("listening", "sample", "sample_hint");
  for (let i = 0; i < lines.length; i++) {
    await new Promise((r) => setTimeout(r, 1600));
    showRisk(states[i], lines[i]);
    toFamily({ type: "transcript", text: lines[i], risk: states[i] });
    if (states[i].alert) { logAlert(states[i], "sample"); alarm(); toFamily({ type: "warning", level: states[i].level }); await new Promise((r) => setTimeout(r, 2500)); $("takeover").hidden = true; }
  }
  setGuard(pack.level === "high" || pack.level === "critical" ? "danger" : "idle", "protect");
  showPack(pack);
  toFamily({ type: "pack", ...pack });
  showTimeline({ error: "Sample calls have no audio, so voices aren't separated." });
};

// ---------- golden-hour pack
function showPack(p) {
  lastPack = p;
  $("pack").hidden = false;
  const bad = p.level === "high" || p.level === "critical";
  $("packTitle").textContent = bad ? t("pack_bad") : t("pack_ok");
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
  $("timeline").innerHTML = `<li class="muted">${t("separating")}</li>`;
  $("status").textContent = bad ? t("over_bad") : t("over");
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
  try { await navigator.clipboard.writeText(text); $("copy").textContent = t("copied"); }
  catch { $("copy").textContent = t("select_copy"); }
  setTimeout(() => ($("copy").textContent = t("copy")), 2500);
};

$("playFamily").onclick = async () => {
  const r = await fetch("/api/family-voice", { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: lastPack.family_alert }) });
  if (r.ok) playWav(await r.blob());
};

// ---------- voice-note check (Gnani Prisma REST, <= 30 s)
$("clipCheck").onclick = async () => {
  const f = $("clipFile").files[0];
  if (!f) return ($("clipResult").textContent = t("choose_file"));
  $("clipResult").textContent = t("checking");
  const fd = new FormData();
  fd.append("file", f);
  fd.append("lang", $("lang").value);
  const d = await (await fetch("/api/clip", { method: "POST", body: fd })).json();
  if (d.error) return ($("clipResult").textContent = t("problem") + d.error);
  const verdict = { safe: "No scam signs", watch: "Be careful", high: "Likely a scam", critical: "This is a scam" }[d.risk.level];
  $("clipResult").textContent = `${verdict} (${d.risk.score}/100). Heard: “${d.transcript}”` +
    (d.risk.playbook?.next ? ". " + d.risk.playbook.next : "") + (d.truncated ? ". Only the first 30 seconds were checked." : "");
};

// ---------- keypad-phone calls Ruko joined over the phone network
async function loadCalls() {
  const calls = await (await fetch("/api/calls")).json();
  $("calls").innerHTML = calls.length ? "" : `<li class="muted small">${t("no_calls")}</li>`;
  for (const p of calls) {
    const li = document.createElement("li");
    const b = document.createElement("button");
    b.type = "button"; b.className = "btn";
    b.textContent = `${p.complaint.incident_datetime}: ${LEVEL[LANG][p.level]} (${p.score}/100)`;
    b.onclick = () => { showPack(p); showTimeline({ error: "Ruko warned inside the phone call. Voices aren't separated for these." }); };
    li.append(b);
    $("calls").append(li);
  }
}
$("refreshCalls").onclick = loadCalls;
loadCalls();
resetView();

// language switch re-renders the dynamic parts
document.addEventListener("langchange", () => {
  $("captions").dataset.empty = t("empty");
  renderStages($("stages"), lastRisk?.playbook);
  if (lastRisk) setLevel($("level"), lastRisk);
  if (!ws && $("guard").dataset.state !== "listening") setGuard($("guard").dataset.state, "protect", "hint");
});
applyLang(LANG);
// opened from the landing page's "Protect my parents": go straight to Family Shield setup
if (new URLSearchParams(location.search).get("setup") === "family") $("familyBtn").click();
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
