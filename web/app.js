const $ = (id) => document.getElementById(id);
const LEVEL_TEXT = { safe: "Safe", watch: "Watching", high: "Likely scam", critical: "SCAM — hang up" };
let ws = null, audioCtx = null, stream = null, speaking = false, pending = new Int16Array(0);

function showRisk(risk, flaggedText) {
  $("meter").dataset.level = risk.level;
  $("meterFill").style.width = risk.score + "%";
  $("levelText").textContent = LEVEL_TEXT[risk.level];
  $("scoreText").textContent = `${risk.score} / 100`;
  $("flags").innerHTML = "";
  for (const f of risk.flags) {
    const li = document.createElement("li");
    li.innerHTML = `<b></b> `;
    li.firstChild.textContent = f.label;
    li.append(`“${f.phrase}”`);
    $("flags").append(li);
  }
  if (flaggedText !== undefined) addLine(flaggedText, risk.new.length > 0);
}

function addLine(text, flagged) {
  const li = document.createElement("li");
  li.textContent = text;
  if (flagged) li.className = "flagged";
  $("transcript").append(li);
  li.scrollIntoView({ block: "nearest" });
}

function alarm(text) {
  $("warning").hidden = false;
  $("warning").textContent = text;
  document.body.classList.remove("alarm");
  void document.body.offsetWidth;
  document.body.classList.add("alarm");
  navigator.vibrate?.([400, 200, 400]);
}

async function playWav(b64OrBlob) {
  const blob = typeof b64OrBlob === "string"
    ? new Blob([Uint8Array.from(atob(b64OrBlob), (c) => c.charCodeAt(0))], { type: "audio/wav" })
    : b64OrBlob;
  const audio = new Audio(URL.createObjectURL(blob));
  speaking = true; // stop sending mic audio so Ruko doesn't transcribe itself
  audio.onended = audio.onerror = () => { speaking = false; };
  await audio.play().catch(() => { speaking = false; });
}

function resetView() {
  $("transcript").innerHTML = "";
  $("warning").hidden = true;
  $("pack").hidden = true;
  showRisk({ level: "safe", score: 0, flags: [], new: [] });
}

// ---- Live listening: mic (16 kHz PCM16, 1,024-byte frames) -> backend -> Prisma Realtime
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
  const q = new URLSearchParams({ lang: $("lang").value, model: $("model").value, whisper: $("whisper").checked ? 1 : 0 });
  ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/listen?${q}`);
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.type === "connected") $("status").textContent = "Listening… keep the call on speaker.";
    else if (m.type === "speech_start") $("status").textContent = "Hearing speech…";
    else if (m.type === "transcript") showRisk(m.risk, m.text);
    else if (m.type === "warning") { alarm(m.text); if (m.audio) playWav(m.audio); else $("status").textContent = "Warning voice failed: " + (m.error || ""); }
    else if (m.type === "pack") showPack(m);
    else if (m.type === "diarized") showTimeline(m);
    else if (m.type === "done") $("audioNote").textContent = "Call audio has been deleted. Only this text report stays, on this screen.";
    else if (m.type === "error") $("status").textContent = "Error: " + m.message;
  };
  ws.onclose = () => stop(false);
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, channelCount: 1 } });
  } catch {
    $("status").textContent = "Microphone permission is needed.";
    return stop();
  }
  audioCtx = new AudioContext({ sampleRate: 16000 });
  await audioCtx.audioWorklet.addModule(URL.createObjectURL(new Blob([WORKLET], { type: "text/javascript" })));
  const node = new AudioWorkletNode(audioCtx, "pcm");
  node.port.onmessage = (e) => sendPcm(e.data);
  audioCtx.createMediaStreamSource(stream).connect(node);
  $("hangup").hidden = false;
  $("listen").textContent = "Stop listening";
  $("listen").classList.add("on");
  $("status").textContent = "Connecting to Gnani Prisma…";
}

function stop(closeWs = true) {
  if (closeWs && ws?.readyState === WebSocket.OPEN) ws.close();
  ws = null;
  stream?.getTracks().forEach((t) => t.stop());
  audioCtx?.close();
  stream = audioCtx = null;
  pending = new Int16Array(0);
  $("hangup").hidden = true;
  $("listen").textContent = "Start listening";
  $("listen").classList.remove("on");
}

$("listen").onclick = () => (ws ? stop() : start());

// ---- Warning voice check
$("testVoice").onclick = async () => {
  const r = await fetch(`/api/warning?lang=${$("lang").value}&whisper=${$("whisper").checked ? 1 : 0}`);
  if (r.ok) playWav(await r.blob());
  else $("status").textContent = "Timbre error: " + (await r.text());
};

// ---- Text test mode (synthetic scripts, no audio)
(async () => {
  const { scam, safe } = await (await fetch("/api/scripts")).json();
  for (const [group, scripts] of [["Scam", scam], ["Safe", safe]]) {
    const og = document.createElement("optgroup");
    og.label = group;
    for (const name of Object.keys(scripts)) og.append(new Option(name.replaceAll("_", " "), JSON.stringify(scripts[name])));
    $("script").append(og);
  }
  const health = await (await fetch("/api/health")).json();
  if (!health.gnani_key) $("status").textContent = "No Gnani API key yet. Add it to ruko/.env. Text test mode still works.";
})();

$("runScript").onclick = async () => {
  resetView();
  const lines = JSON.parse($("script").value);
  const { states, pack } = await (await fetch("/api/analyze", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lines, lang: $("lang").value }),
  })).json();
  for (let i = 0; i < lines.length; i++) {
    await new Promise((r) => setTimeout(r, 900));
    showRisk(states[i], lines[i]);
    if (states[i].alert) alarm("(text test) Ruko would speak the warning now.");
  }
  showPack(pack);
  showTimeline({ error: "Text test mode has no audio, so there is no speaker separation." });
};

// ---- Hang up: stop sending audio, ask the backend for the golden-hour pack
$("hangup").onclick = () => {
  if (ws?.readyState !== WebSocket.OPEN) return;
  ws.send(JSON.stringify({ type: "hangup" }));
  stream?.getTracks().forEach((t) => t.stop());
  $("hangup").hidden = true;
  $("status").textContent = "Making your report…";
};

let lastPack = null;
function showPack(p) {
  lastPack = p;
  $("pack").hidden = false;
  const c = p.complaint;
  const rows = [["Category", c.category], ["Sub-category", c.sub_category], ["When", c.incident_datetime],
    ["Caller's number", c.suspect_phone_number], ["Amount lost", c.amount_lost]];
  $("fields").innerHTML = "";
  for (const [k, v] of rows) {
    const dt = document.createElement("dt"); dt.textContent = k;
    const dd = document.createElement("dd"); dd.textContent = v;
    $("fields").append(dt, dd);
  }
  $("complaint").textContent = c.description;
  $("familyBox").hidden = !p.family_alert;
  $("family").textContent = p.family_alert || "";
  $("timeline").innerHTML = '<li class="hint">Separating the caller\'s voice from yours (Gnani Prisma Batch)…</li>';
  $("status").textContent = p.level === "safe" || p.level === "watch" ? "Call ended. No strong scam signs found." : "Call ended. Your report is ready below.";
  $("pack").scrollIntoView({ behavior: "smooth" });
}

function showTimeline(m) {
  $("timeline").innerHTML = "";
  if (m.error || !m.segments?.length) {
    const li = document.createElement("li"); li.className = "hint";
    li.textContent = m.error ? "Could not separate voices: " + m.error : "No speech found.";
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
  const text = `Category: ${c.category}\nSub-category: ${c.sub_category}\nWhen: ${c.incident_datetime}\n` +
    `Caller's number: ${c.suspect_phone_number}\nAmount lost: ${c.amount_lost}\n\n${c.description}`;
  try { await navigator.clipboard.writeText(text); $("copy").textContent = "Copied"; }
  catch { $("copy").textContent = "Copy failed: select the text above"; }
  setTimeout(() => ($("copy").textContent = "Copy complaint"), 2500);
};

$("playFamily").onclick = async () => {
  const r = await fetch("/api/family-voice", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text: lastPack.family_alert }),
  });
  if (r.ok) playWav(await r.blob());
  else $("status").textContent = "Timbre error: " + (await r.text());
};

// ---- Clip check (Prisma REST, <= 30 s)
$("clipCheck").onclick = async () => {
  const f = $("clipFile").files[0];
  if (!f) return ($("clipResult").textContent = "Choose an audio file first.");
  $("clipResult").textContent = "Checking with Gnani Prisma…";
  const fd = new FormData();
  fd.append("file", f);
  fd.append("lang", $("lang").value);
  const d = await (await fetch("/api/clip", { method: "POST", body: fd })).json();
  if (d.error) return ($("clipResult").textContent = "Error: " + d.error);
  const verdict = { safe: "No scam signs found", watch: "Be careful", high: "Likely scam", critical: "SCAM" }[d.risk.level];
  $("clipResult").textContent = `${verdict} (${d.risk.score}/100). Heard: “${d.transcript}”` +
    (d.risk.flags.length ? " · Red flags: " + d.risk.flags.map((x) => x.label).join(", ") : "") +
    (d.truncated ? " · Only the first 30 seconds were checked." : "");
};
