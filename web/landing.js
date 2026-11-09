// Landing page: a scripted demo call through the real scoring API, and the pilot waitlist.
renderStages($("dStages"), null);
let playing = false;

$("dPlay").onclick = async () => {
  if (playing) return;
  playing = true;
  $("dPlay").textContent = "Playing…";
  $("dCaptions").innerHTML = "";
  $("dNext").textContent = "";
  document.querySelector(".demo").classList.remove("alarm");
  try {
    const { scam } = await (await fetch("/api/scripts")).json();
    const lines = scam.digital_arrest;
    const { states } = await (await fetch("/api/analyze", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ lines }),
    })).json();
    for (let i = 0; i < lines.length; i++) {
      await new Promise((r) => setTimeout(r, 1500));
      addCaption($("dCaptions"), lines[i], states[i], "Caller:");
      setLevel($("dLevel"), states[i]);
      renderStages($("dStages"), states[i].playbook);
      $("dNext").textContent = states[i].playbook?.next || "";
      if (states[i].alert) {
        document.querySelector(".demo").classList.add("alarm");
        navigator.vibrate?.(300);
      }
    }
  } catch {
    $("dNext").textContent = "The demo server is waking up. Try again in a few seconds.";
  }
  $("dPlay").textContent = "▶ Play again";
  playing = false;
};

$("wl").onsubmit = async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  data.consent = !!data.consent;
  $("wlMsg").textContent = "Sending…";
  try {
    const r = await fetch("/api/waitlist", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    if (!r.ok) throw new Error();
    e.target.reset();
    $("wlMsg").textContent = "You're on the list. We'll reach out soon.";
  } catch {
    $("wlMsg").textContent = "Couldn't send that. Please try again.";
  }
};
