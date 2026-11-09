// Family Shield screen: live view of a protected person's calls, via /ws/family?c=<code>.
const params = new URLSearchParams(location.search);
const code = params.get("c") || "";
const who = (params.get("n") || "").trim().slice(0, 30) || "Your family member";
let retry = 1000;

function setState(state, headline, sub) {
  document.body.dataset.state = state;
  $("headline").textContent = headline;
  $("sub").textContent = sub;
  $("todo").hidden = state !== "danger";
  $("famOct").hidden = state !== "danger";
  if (state === "danger" && !$("famOct").innerHTML) $("famOct").innerHTML = octagonSVG();
}

function idle() {
  setState("idle", `Watching over ${who}'s calls`, "Keep this page open. If a call turns into a scam, this screen turns red right away.");
}

function handle(m) {
  if (m.type === "call_start") {
    $("captions").innerHTML = "";
    $("packCard").hidden = true;
    $("liveCard").hidden = $("capCard").hidden = false;
    renderStages($("stages"), null);
    $("next").textContent = "";
    setState("live", `${who} is on a call`, "Ruko is listening to it now. Nothing looks wrong yet.");
  } else if (m.type === "transcript") {
    $("liveCard").hidden = $("capCard").hidden = false;
    addCaption($("captions"), m.text, m.risk);
    renderStages($("stages"), m.risk.playbook);
    $("next").textContent = m.risk.playbook?.next || "";
    $("next").parentElement.classList.toggle("now", m.risk.level === "critical");
    if (m.risk.level === "high" || m.risk.level === "critical") danger();
    else if (m.risk.level === "watch") setState("live", `${who} is on a call`, "Some warning signs. Ruko is watching closely.");
  } else if (m.type === "warning") {
    danger();
  } else if (m.type === "pack") {
    const bad = m.level === "high" || m.level === "critical";
    $("packCard").hidden = false;
    $("packText").textContent = m.family_alert || (bad ? "The call has ended. It was a scam call." : "The call has ended. No strong scam signs.");
    if (bad) setState("danger", `${who} just had a scam call`, "The call is over. Check on them now.");
    else idle();
  } else if (m.type === "call_end" && document.body.dataset.state === "live") {
    idle();
  }
}

function danger() {
  if (document.body.dataset.state !== "danger") navigator.vibrate?.([600, 200, 600, 200, 600]);
  setState("danger", `${who} is on a SCAM call right now`, "Ruko has warned them out loud. Do these now:");
}

function connect() {
  const ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/family?c=${encodeURIComponent(code)}`);
  ws.onopen = () => { retry = 1000; $("connText").textContent = "Live"; $("connDot").className = "cdot"; };
  ws.onmessage = (e) => handle(JSON.parse(e.data));
  ws.onclose = (e) => {
    if (e.code === 1008) {
      $("connText").textContent = "This link isn't valid";
      return setState("idle", "This family link isn't valid", "Ask for a new link from the Ruko app (Family Shield → Copy).");
    }
    $("connText").textContent = "Reconnecting…";
    $("connDot").className = "cdot wait";
    setTimeout(connect, (retry = Math.min(retry * 2, 15000)));
  };
}

idle();
renderStages($("stages"), null);
connect();

// ---------- "Warn in your voice": record 5-30 s as 16 kHz WAV, send with consent, Gnani makes a voice embedding
const REC = `class R extends AudioWorkletProcessor{process(i){const c=i[0][0];if(c)this.port.postMessage(c.slice(0));return true}}registerProcessor('rec',R)`;
let rec = null;

function wav16k(chunks) {
  const n = chunks.reduce((a, c) => a + c.length, 0);
  const buf = new DataView(new ArrayBuffer(44 + n * 2));
  const str = (o, s) => [...s].forEach((ch, i) => buf.setUint8(o + i, ch.charCodeAt(0)));
  str(0, "RIFF"); buf.setUint32(4, 36 + n * 2, true); str(8, "WAVEfmt "); buf.setUint32(16, 16, true);
  buf.setUint16(20, 1, true); buf.setUint16(22, 1, true); buf.setUint32(24, 16000, true); buf.setUint32(28, 32000, true);
  buf.setUint16(32, 2, true); buf.setUint16(34, 16, true); str(36, "data"); buf.setUint32(40, n * 2, true);
  let o = 44;
  for (const c of chunks) for (const s of c) { buf.setInt16(o, Math.max(-1, Math.min(1, s)) * 0x7fff, true); o += 2; }
  return new Blob([buf], { type: "audio/wav" });
}

async function voiceStatus() {
  const v = await (await fetch(`/api/family/voice?c=${encodeURIComponent(code)}`)).json();
  $("voiceDel").hidden = !v.has_voice;
  if (v.has_voice) $("voiceMsg").textContent = `Warnings will be spoken in ${v.name ? v.name + "'s" : "your"} voice.`;
}

$("voiceRec").onclick = async () => {
  if (rec) return stopRec();
  if (!$("voiceConsent").checked) return ($("voiceMsg").textContent = "Please tick the consent box first.");
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: { channelCount: 1, noiseSuppression: true } });
    const ctx = new AudioContext({ sampleRate: 16000 });
    await ctx.audioWorklet.addModule(URL.createObjectURL(new Blob([REC], { type: "text/javascript" })));
    const node = new AudioWorkletNode(ctx, "rec");
    const chunks = [];
    node.port.onmessage = (e) => chunks.push(e.data);
    ctx.createMediaStreamSource(stream).connect(node);
    rec = { stream, ctx, chunks, t0: Date.now(), timer: setTimeout(stopRec, 30000) };
    $("voiceRec").textContent = "Stop recording";
    $("voiceMsg").textContent = "Recording… read the lines above, then tap Stop.";
  } catch {
    $("voiceMsg").textContent = "Microphone permission is needed to record your voice.";
  }
};

async function stopRec() {
  const r = rec; rec = null;
  clearTimeout(r.timer);
  r.stream.getTracks().forEach((t) => t.stop());
  r.ctx.close();
  $("voiceRec").textContent = "Record again";
  if ((Date.now() - r.t0) / 1000 < 5) return ($("voiceMsg").textContent = "That was too short. Record at least 5 seconds.");
  $("voiceMsg").textContent = "Making your voice with Gnani…";
  const fd = new FormData();
  fd.append("c", code); fd.append("name", $("voiceName").value.trim()); fd.append("consent", "true");
  fd.append("file", wav16k(r.chunks), "voice.wav");
  const d = await (await fetch("/api/family/voice", { method: "POST", body: fd })).json().catch(() => ({ error: "network" }));
  $("voiceMsg").textContent = d.error ? "Couldn't make the voice: " + d.error : "Done.";
  voiceStatus();
}

$("voiceDel").onclick = async () => {
  await fetch(`/api/family/voice?c=${encodeURIComponent(code)}`, { method: "DELETE" });
  $("voiceMsg").textContent = "Your voice has been deleted. Warnings use Ruko's own voice again.";
  $("voiceDel").hidden = true;
};
voiceStatus();
