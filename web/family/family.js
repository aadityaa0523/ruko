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
  ws.onopen = () => { retry = 1000; $("connText").textContent = "Live"; $("connDot").className = "dot"; };
  ws.onmessage = (e) => handle(JSON.parse(e.data));
  ws.onclose = (e) => {
    if (e.code === 1008) {
      $("connText").textContent = "This link isn't valid";
      return setState("idle", "This family link isn't valid", "Ask for a new link from the Ruko app (Family Shield → Copy).");
    }
    $("connText").textContent = "Reconnecting…";
    $("connDot").className = "dot live";
    setTimeout(connect, (retry = Math.min(retry * 2, 15000)));
  };
}

idle();
renderStages($("stages"), null);
connect();
