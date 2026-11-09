// Check anything: message/link/number verdicts, community number reports, Scam Radar.
window.STRINGS = {
  en: {},
  hi: {
    nav_check: "जाँचें", nav_guard: "कॉल गार्ड", nav_family: "परिवार", h1: "क्या यह धोखा है?",
    sub: "कोई भी SMS, WhatsApp संदेश, लिंक, UPI अनुरोध या फ़ोन नंबर चिपकाएँ। Ruko कुछ सेकंड में बताता है, और यह भी कि ठग आगे क्या करेगा।",
    ph: "जैसे “आज रात आपकी बिजली कट जाएगी। अधिकारी को 98765 43210 पर कॉल करें”", paste: "चिपकाएँ", check: "जाँचें",
    private: "आपका चिपकाया हुआ कुछ भी सेव नहीं होता। नंबर सिर्फ़ तब सेव होता है जब आप उसे रिपोर्ट करें।", try: "आज़माएँ:",
    why: "क्यों", links: "इसमें लिंक", numbers: "इसमें फ़ोन नंबर", share: "WhatsApp पर परिवार को सावधान करें", lost: "पैसे गए? 1930 पर कॉल करें",
    lookup_h: "नंबर जाँचें या रिपोर्ट करें", number: "फ़ोन नंबर", lookup: "जाँचें", what: "उन्होंने क्या किया?", how: "कैसे संपर्क किया?",
    report: "यह नंबर रिपोर्ट करें", rep_note: "रिपोर्ट गुमनाम है। सिर्फ़ नंबर और धोखे का प्रकार सेव होता है।",
    radar_h: "स्कैम रडार · इस हफ़्ते", radar_src: "Ruko यूज़र्स की रिपोर्ट और लाइव कॉल अलर्ट से",
    v_scam: "धोखा", v_suspicious: "सावधान", v_safe: "धोखे के संकेत नहीं",
  },
};
for (const el of document.querySelectorAll("[data-i18n]")) STRINGS.en[el.dataset.i18n] ??= el.textContent;
Object.assign(STRINGS.en, { v_scam: "Scam", v_suspicious: "Be careful", v_safe: "No scam signs" });

const SAMPLES = [
  "Dear consumer, your electricity power will be disconnected tonight at 9.30 PM because your last bill was not updated. Contact our officer immediately 9876543210",
  "SBI: Your account will be blocked today. Update KYC now: http://sbi-kyc-update.xyz/login",
  "Sir maine galti se 5000 bhej diye, please wapas bhej do. Maine collect request bheji hai raju.k@ybl par approve kar do",
  "123456 is your OTP for login to SBI YONO. Do not share it with anyone. -SBI",
];
const CAT = { digital_arrest: "Fake police / CBI / digital arrest", bank_kyc: "Bank, KYC or card block", electricity: "Electricity or bill cut-off",
  parcel: "Parcel, courier or customs", refund: "“Sent money by mistake”", relative: "Relative in trouble", job: "Job, task or investment",
  prize: "Prize or lottery", loan: "Loan or recovery threats", other: "Other scams", high: "Likely-scam calls warned live", critical: "Scam calls stopped live" };
const C = window.RUKO_CONFIG;

async function rpc(fn, args) {
  const r = await fetch(`${C.supabaseUrl}/rest/v1/rpc/${fn}`, { method: "POST",
    headers: { apikey: C.supabaseKey, Authorization: `Bearer ${C.supabaseKey}`, "Content-Type": "application/json" }, body: JSON.stringify(args) });
  if (!r.ok) throw new Error(`lookup failed (${r.status})`);
  return r.json();
}
const digits = (s) => { const d = s.replace(/\D/g, ""); return d.length >= 10 && "6789".includes(d.at(-10)) ? d.slice(-10) : d; };
const pretty = (n) => n.length === 10 ? `${n.slice(0, 5)} ${n.slice(5)}` : n;

function verdictSign(v) {
  if (v === "scam") return octagonSVG("STOP");
  if (v === "suspicious") return '<svg viewBox="0 0 100 90" aria-hidden="true"><path d="M50 8 94 84H6z" fill="#fff" stroke="#141414" stroke-width="7" stroke-linejoin="round"/><rect x="45" y="34" width="10" height="28" rx="2" fill="#141414"/><circle cx="50" cy="72" r="5.5" fill="#141414"/></svg>';
  return '<svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="44" fill="#fff"/><path d="M30 52l13 13 27-29" fill="none" stroke="#1f7a45" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}

async function runCheck(text) {
  $("go").disabled = true;
  try {
    const r = await (await fetch("/api/check", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text }) })).json();
    show(r, text);
  } catch {
    $("advice").textContent = "Couldn't check right now. Please try again in a few seconds.";
    $("result").hidden = false;
  }
  $("go").disabled = false;
}

function show(r, text) {
  $("result").hidden = false;
  $("verdict").dataset.v = r.verdict;
  $("vSign").innerHTML = verdictSign(r.verdict);
  $("vWord").textContent = t("v_" + r.verdict);
  $("vScore").textContent = `Risk ${r.score}/100`;
  $("advice").textContent = r.advice;
  const next = r.verdict !== "safe" ? r.playbook?.next : "";
  $("next").textContent = next || "";
  $("nextBox").classList.toggle("now", r.verdict === "scam");
  $("reasons").innerHTML = "";
  for (const f of r.flags) {
    const li = document.createElement("li");
    const b = document.createElement("b"); b.textContent = f.label;
    const s = document.createElement("span"); s.textContent = `“${f.phrase}”`;
    li.append(b, s); $("reasons").append(li);
  }
  if (!r.flags.length) $("reasons").innerHTML = "<li>Nothing that matches known scam patterns.</li>";
  $("linksBox").hidden = !r.links.length;
  $("links").innerHTML = "";
  for (const l of r.links) {
    const li = document.createElement("li");
    li.className = l.why.length ? "bad" : "";
    li.textContent = l.host || l.url;
    const s = document.createElement("small"); s.textContent = l.why.length ? "This link " + l.why.join("; ") + "." : "No warning signs in this address.";
    li.append(s); $("links").append(li);
  }
  $("numsBox").hidden = !r.phones.length;
  $("nums").innerHTML = "";
  for (const n of r.phones) {
    const li = document.createElement("li");
    li.innerHTML = '<b></b><span class="tag">Checking…</span><button class="btn btn-plain" type="button">Report</button>';
    li.querySelector("b").textContent = pretty(n);
    li.querySelector("button").onclick = () => { $("num").value = n; lookup(n, true); $("lookup").scrollIntoView({ behavior: "smooth" }); };
    $("nums").append(li);
    rpc("number_lookup", { p_number: n }).then(([d]) => {
      const tag = li.querySelector(".tag");
      tag.textContent = d && d.reports > 0 ? `Reported ${d.reports}× · ${CAT[d.top_category] || ""}` : "No reports yet";
      tag.classList.toggle("hot", d && d.reports > 0);
    }).catch(() => (li.querySelector(".tag").textContent = "Lookup unavailable"));
  }
  const top = r.flags[0]?.label?.toLowerCase() || "";
  const msg = r.verdict === "safe"
    ? `Ruko checked a message for me and found no scam signs. Check yours free: ${location.origin}/check/`
    : `⚠️ Scam alert from Ruko: a message going around ${top ? "(" + top + ") " : ""}is ${r.verdict === "scam" ? "a scam" : "suspicious"}. Don't click links, pay or share any OTP. Check any message free: ${location.origin}/check/`;
  $("share").href = "https://wa.me/?text=" + encodeURIComponent(msg);
  $("result").scrollIntoView({ behavior: "smooth", block: "start" });
}

$("form").onsubmit = (e) => { e.preventDefault(); const v = $("text").value.trim(); if (v) runCheck(v); };
$("paste").onclick = async () => {
  try { $("text").value = await navigator.clipboard.readText(); $("text").focus(); } catch { $("text").focus(); }
};
for (const b of document.querySelectorAll("[data-sample]")) b.onclick = () => { $("text").value = SAMPLES[+b.dataset.sample]; runCheck($("text").value); };

// ---------- number lookup and reports
async function lookup(n, openReport = false) {
  const box = $("numResult");
  box.hidden = false; box.className = "num-result"; box.textContent = "Checking…";
  try {
    const [d] = await rpc("number_lookup", { p_number: n });
    if (d && d.reports > 0) {
      box.classList.add("hot");
      box.textContent = `${pretty(n)} has been reported ${d.reports} time${d.reports > 1 ? "s" : ""}` +
        `${d.reports_7d ? ` (${d.reports_7d} this week)` : ""}, mostly for: ${CAT[d.top_category] || d.top_category}. Don't trust calls or messages from it.`;
    } else {
      box.textContent = `No reports for ${pretty(n)} yet. That doesn't mean it's safe: scammers change numbers often. If it called you with a scam, report it below.`;
    }
  } catch { box.textContent = "Lookup is unavailable right now."; }
  $("repForm").hidden = false;
  if (openReport) $("repCat").focus();
}
$("numForm").onsubmit = (e) => {
  e.preventDefault();
  const n = digits($("num").value);
  if (n.length < 6) { $("repMsg").textContent = "Type a full phone number."; $("repMsg").classList.add("err"); return; }
  $("repMsg").textContent = ""; lookup(n);
};
$("repForm").onsubmit = async (e) => {
  e.preventDefault();
  const n = digits($("num").value);
  try {
    await sbInsert("number_reports", { number: n, category: $("repCat").value, channel: $("repCh").value, language: LANG });
    $("repMsg").classList.remove("err");
    $("repMsg").textContent = `Thanks. ${pretty(n)} is now flagged for everyone who checks it.`;
    lookup(n); loadRadar();
  } catch {
    $("repMsg").classList.add("err"); $("repMsg").textContent = "Couldn't save the report. Please try again.";
  }
};

// ---------- Scam Radar
async function loadRadar() {
  const ol = $("radarList");
  try {
    const rows = await rpc("scam_radar", { p_days: 7 });
    const rep = rows.filter((r) => r.kind === "report").sort((a, b) => b.total - a.total);
    const al = rows.filter((r) => r.kind === "alert");
    const max = Math.max(1, ...rep.map((r) => r.total));
    ol.innerHTML = "";
    for (const r of [...al, ...rep]) {
      const li = document.createElement("li");
      li.innerHTML = '<span></span><span class="n"></span><span class="bar-fill"><i></i></span>';
      li.children[0].textContent = CAT[r.label] || r.label;
      li.children[1].textContent = r.total;
      li.querySelector("i").style.width = r.kind === "alert" ? "100%" : `${(r.total / max) * 100}%`;
      ol.append(li);
    }
    if (!rows.length) ol.innerHTML = '<li class="empty">No reports yet this week. If a scammer contacted you, report the number above so others are warned.</li>';
  } catch { ol.innerHTML = '<li class="empty">Scam Radar is unavailable right now.</li>'; }
}

// ---------- opened from the phone's Share menu (installed app) or a link
{
  const q = new URLSearchParams(location.search);
  const shared = [q.get("title"), q.get("text"), q.get("url")].filter(Boolean).join("\n").trim();
  if (shared) { $("text").value = shared.slice(0, 4000); runCheck($("text").value); }
  if (q.get("n")) { $("num").value = q.get("n"); lookup(digits(q.get("n"))); }
}
applyLang(LANG);
loadRadar();
