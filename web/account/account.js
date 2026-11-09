// Family account: Supabase Auth (email + password) and the "Your family" dashboard.
window.STRINGS = {
  en: {},
  hi: {
    sign_out: "साइन आउट", loading: "लोड हो रहा है…", auth_title_new: "अपने मम्मी-पापा को सुरक्षित करें", auth_title_login: "वापसी पर स्वागत है",
    auth_sub: "एक फ़ैमिली अकाउंट। जिन्हें आप सुरक्षित रखते हैं उन्हें जोड़ें, हर किसी को सेटअप लिंक भेजें, और देखें Ruko ने कौन-सी धोखे वाली कॉल रोकीं।",
    tab_new: "अकाउंट बनाएँ", tab_login: "लॉग इन", email: "ईमेल", password: "पासवर्ड", pw_hint: "कम से कम 8 अक्षर।",
    agree_1: "अकाउंट बनाकर आप इनसे सहमत हैं:", terms: "उपयोग की शर्तें", agree_2: "और", privacy: "गोपनीयता नीति",
    create: "अकाउंट बनाएँ", login_btn: "लॉग इन", forgot: "पासवर्ड भूल गए?",
    side_1: "आज़माना मुफ़्त। न कार्ड, न ऐप स्टोर।", side_2: "मम्मी-पापा को अकाउंट नहीं चाहिए। बस उनका लिंक खोलें।", side_3: "Ruko कॉल की आवाज़ नहीं रखता। अपना डेटा कभी भी हटाएँ।",
    your_family: "आपका परिवार", open_app: "इस फ़ोन पर Ruko खोलें", people: "जिन्हें आप सुरक्षित रखते हैं",
    add_label: "किसी को जोड़ें (आप उन्हें क्या कहते हैं)", add_ph: "जैसे मम्मी, पापा, नानी", add_btn: "जोड़ें",
    history: "Ruko ने पकड़ी धोखे वाली कॉल", history_p: "सिर्फ़ समय, व्यक्ति और धोखा कितना आगे बढ़ा। न आवाज़, न शब्द, न फ़ोन नंबर।",
    h_when: "कब", h_who: "कौन", h_level: "स्तर", h_steps: "क़दम",
    your_data: "आपका डेटा", your_data_p: "आपके जोड़े सभी लोग और उनका अलर्ट इतिहास हट जाएगा। अकाउंट बंद करने के लिए संपर्क पेज से अनुरोध भेजें।",
    wipe: "मेरे परिवार का सारा डेटा हटाएँ",
    setup: "उनका फ़ोन सेट करें", watch: "लाइव देखें", remove: "हटाएँ", no_alerts: "अभी कोई अलर्ट नहीं", last_alert: "आख़िरी अलर्ट",
    none_yet: "अभी कोई नहीं। ऊपर किसी को जोड़ें।", no_hist: "अभी कोई धोखे वाली कॉल नहीं पकड़ी गई।",
    step1: "यह लिंक उनके फ़ोन पर भेजें (WhatsApp सबसे आसान है)।", step2: "उनके फ़ोन पर लिंक खोलें और \"होम स्क्रीन पर जोड़ें\" दबाएँ।", step3: "कोई अनजान कॉल पैसे या पुलिस की बात करे, तो कॉल स्पीकर पर रखें और Ruko का बड़ा बटन दबाएँ।",
    send_wa: "WhatsApp पर भेजें", copy: "लिंक कॉपी करें", copied: "कॉपी हो गया",
    check_email: "अपना ईमेल देखें और अकाउंट की पुष्टि करें, फिर लॉग इन करें।", reset_sent: "पासवर्ड बदलने का लिंक आपके ईमेल पर भेज दिया।",
    enter_email: "पहले अपना ईमेल लिखें।", confirm_wipe: "सारे लोग और उनका अलर्ट इतिहास हमेशा के लिए हटाएँ? यह वापस नहीं होगा।",
    critical: "धोखा", high: "शायद धोखा",
  },
};
for (const el of document.querySelectorAll("[data-i18n]")) STRINGS.en[el.dataset.i18n] ??= el.textContent;
Object.assign(STRINGS.en, {
  auth_title_login: "Welcome back", login_btn: "Log in", setup: "Set up their phone", watch: "Watch live", remove: "Remove",
  no_alerts: "No alerts yet", last_alert: "Last alert", none_yet: "Nobody yet. Add someone above.", no_hist: "No scam calls caught yet.",
  step1: "Send this link to their phone (WhatsApp is easiest).", step2: "On their phone, open it and tap \"Add to Home screen\".",
  step3: "When an unknown caller talks about money or police: put the call on speaker and tap Ruko's big button.",
  send_wa: "Send on WhatsApp", copy: "Copy link", copied: "Copied",
  check_email: "Check your email to confirm your account, then log in.", reset_sent: "We've emailed you a link to reset your password.",
  enter_email: "Type your email first.", confirm_wipe: "Delete everyone you added and all their alert history? This can't be undone.",
  critical: "Scam", high: "Likely scam",
});

const sb = supabase.createClient(RUKO_CONFIG.supabaseUrl, RUKO_CONFIG.supabaseKey);
const STAGE_NAME = { pose: { en: "pretends", hi: "नाटक" }, fear: { en: "scares", hi: "डराना" }, isolate: { en: "isolates", hi: "अलग करना" }, ask: { en: "asks for OTP or money", hi: "OTP/पैसे माँगना" } };
let mode = new URLSearchParams(location.search).get("login") ? "login" : "new";
let families = [], alerts = [], openSetup = null;

function msg(id, text, err = false) { $(id).textContent = text; $(id).classList.toggle("err", err); }

// ---------- auth
function setMode(m) {
  mode = m;
  $("tabNew").setAttribute("aria-selected", String(m === "new"));
  $("tabLogin").setAttribute("aria-selected", String(m === "login"));
  $("authTitle").textContent = t(m === "new" ? "auth_title_new" : "auth_title_login");
  $("authBtn").textContent = t(m === "new" ? "create" : "login_btn");
  $("agree").hidden = m !== "new"; $("pwHint").hidden = m !== "new"; $("forgot").hidden = m !== "login";
  $("password").autocomplete = m === "new" ? "new-password" : "current-password";
  msg("authMsg", "");
}
$("tabNew").onclick = () => setMode("new");
$("tabLogin").onclick = () => setMode("login");

$("authForm").onsubmit = async (e) => {
  e.preventDefault();
  const email = $("email").value.trim(), password = $("password").value;
  if (!$("email").checkValidity()) return msg("authMsg", t("enter_email"), true);
  if (password.length < 8) return msg("authMsg", t("pw_hint"), true);
  $("authBtn").disabled = true;
  try {
    if (mode === "new") {
      const { data, error } = await sb.auth.signUp({ email, password, options: { emailRedirectTo: location.origin + "/account/" } });
      if (error) throw error;
      if (!data.session) msg("authMsg", t("check_email"));
    } else {
      const { error } = await sb.auth.signInWithPassword({ email, password });
      if (error) throw error;
    }
  } catch (err) {
    msg("authMsg", err.message || String(err), true);
  }
  $("authBtn").disabled = false;
};

$("forgot").onclick = async () => {
  const email = $("email").value.trim();
  if (!email) return msg("authMsg", t("enter_email"), true);
  const { error } = await sb.auth.resetPasswordForEmail(email, { redirectTo: location.origin + "/account/" });
  msg("authMsg", error ? error.message : t("reset_sent"), !!error);
};
$("signOut").onclick = () => sb.auth.signOut();

// ---------- dashboard
function newCode() {
  const a = crypto.getRandomValues(new Uint8Array(10));
  return Array.from(a, (b) => "abcdefghijkmnpqrstuvwxyz23456789"[b % 32]).join("");
}
const parentLink = (f) => `${location.origin}/app/?f=${f.code}&n=${encodeURIComponent(f.parent_name)}`;
const liveLink = (f) => `/family/?c=${f.code}&n=${encodeURIComponent(f.parent_name)}`;
const when = (iso) => new Date(iso).toLocaleString(LANG === "hi" ? "hi-IN" : "en-IN", { day: "numeric", month: "short", hour: "numeric", minute: "2-digit" });

async function load() {
  const [{ data: fam }, { data: al }] = await Promise.all([
    sb.from("families").select("id, code, parent_name, created_at").order("created_at"),
    sb.from("alerts").select("code, level, stages, source, created_at").order("created_at", { ascending: false }).limit(50),
  ]);
  families = fam || []; alerts = al || [];
  render();
}

function render() {
  const ul = $("people");
  ul.innerHTML = "";
  if (!families.length) ul.innerHTML = `<li class="empty-people">${t("none_yet")}</li>`;
  for (const f of families) {
    const last = alerts.find((a) => a.code === f.code);
    const li = document.createElement("li");
    li.innerHTML = `<div><div class="p-name"></div><div class="p-status ${last ? "alerted" : ""}"><span class="dot"></span><span></span></div></div>
      <div class="p-actions"><button class="btn btn-primary" type="button" data-act="setup"></button><a class="btn btn-plain" data-act="watch"></a><button class="btn btn-plain" type="button" data-act="remove"></button></div>`;
    li.querySelector(".p-name").textContent = f.parent_name;
    li.querySelector(".p-status span:last-child").textContent = last ? `${t("last_alert")}: ${when(last.created_at)}` : t("no_alerts");
    li.querySelector('[data-act="setup"]').textContent = t("setup");
    const w = li.querySelector('[data-act="watch"]'); w.textContent = t("watch"); w.href = liveLink(f);
    li.querySelector('[data-act="remove"]').textContent = t("remove");
    li.querySelector('[data-act="setup"]').onclick = () => { openSetup = openSetup === f.code ? null : f.code; render(); };
    li.querySelector('[data-act="remove"]').onclick = async () => {
      if (!confirm(`${t("remove")} ${f.parent_name}?`)) return;
      await sb.from("families").delete().eq("id", f.id);
      load();
    };
    if (openSetup === f.code) {
      const box = document.createElement("div");
      box.className = "p-setup";
      const link = parentLink(f);
      const wa = `${f.parent_name}, yeh Ruko ka link hai. Isse kholo aur "Add to Home screen" karo. Koi anjaan call paise ya police ki baat kare, to call speaker par rakho aur Ruko ka bada button dabao: ${link}`;
      box.innerHTML = `<ol><li></li><li></li><li></li></ol><input readonly aria-label="Setup link"><div class="row"><a class="btn btn-primary" target="_blank" rel="noopener"></a><button class="btn btn-plain" type="button"></button></div>`;
      const steps = box.querySelectorAll("li"); steps[0].textContent = t("step1"); steps[1].textContent = t("step2"); steps[2].textContent = t("step3");
      box.querySelector("input").value = link;
      const a = box.querySelector("a"); a.textContent = t("send_wa"); a.href = "https://wa.me/?text=" + encodeURIComponent(wa);
      const c = box.querySelector("button"); c.textContent = t("copy");
      c.onclick = async () => { try { await navigator.clipboard.writeText(link); c.textContent = t("copied"); } catch { box.querySelector("input").select(); } };
      li.append(box);
    }
    ul.append(li);
  }
  const tb = $("hist");
  tb.innerHTML = "";
  if (!alerts.length) tb.innerHTML = `<tr><td class="empty" colspan="4">${t("no_hist")}</td></tr>`;
  for (const a of alerts) {
    const f = families.find((x) => x.code === a.code);
    const tr = document.createElement("tr");
    tr.innerHTML = "<td></td><td></td><td></td><td></td>";
    tr.cells[0].textContent = when(a.created_at) + (a.source === "sample" ? " · sample" : "");
    tr.cells[1].textContent = f ? f.parent_name : "—";
    tr.cells[2].textContent = t(a.level); tr.cells[2].className = "lvl-" + a.level;
    tr.cells[3].textContent = a.stages.map((s) => STAGE_NAME[s]?.[LANG] || s).join(" → ");
    tb.append(tr);
  }
}

$("addForm").onsubmit = async (e) => {
  e.preventDefault();
  const name = $("addName").value.trim();
  if (!name) return;
  const { data, error } = await sb.from("families").insert({ code: newCode(), parent_name: name }).select().single();
  if (error) return msg("addMsg", error.message, true);
  $("addName").value = ""; msg("addMsg", "");
  openSetup = data.code;
  load();
};

$("wipe").onclick = async () => {
  if (!confirm(t("confirm_wipe"))) return;
  for (const f of families) await sb.from("families").delete().eq("id", f.id);
  load();
};

// ---------- session routing
function show(session) {
  $("loading").hidden = true;
  $("authView").hidden = !!session;
  $("dashView").hidden = !session;
  $("signOut").hidden = !session;
  if (session) { $("who").textContent = session.user.email; load(); }
}
sb.auth.onAuthStateChange((_event, session) => show(session));
sb.auth.getSession().then(({ data }) => show(data.session));

document.addEventListener("langchange", () => { setMode(mode); renderStages($("authSigns"), { stages: [{ key: "pose", done: true }, { key: "fear", done: true }, { key: "isolate", done: true }, { key: "ask", done: true }] }); if (!$("dashView").hidden) render(); });
applyLang(LANG);
