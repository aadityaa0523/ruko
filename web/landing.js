// Landing: the road demo (real Timbre audio + live scoring), language switch, pilot form.
window.STRINGS = {
  en: {},
  hi: {
    nav_how: "कैसे काम करता है", nav_family: "परिवार", nav_proof: "सबूत", nav_biz: "बैंकों के लिए",
    cta: "मम्मी-पापा को सुरक्षित करें",
    h1a: "आगे धोखा है।", h1b: "Ruko पहले ही चेतावनी देता है।",
    lede: "Ruko आपके मम्मी-पापा की कॉल सुनता है, धोखे को होते हुए पहचानता है, और ठग की अगली चाल से पहले उनकी भाषा में ज़ोर से चेतावनी देता है। उसी पल आपका फ़ोन भी लाल हो जाता है।",
    play: "धोखा पकड़ते हुए सुनें", stop: "रोकें",
    f1: "कोई भी फ़ोन; कीपैड-फ़ोन लाइन जाँच में", f2: "हिंदी, हिंग्लिश, कन्नड़, तेलुगु, तमिल, अंग्रेज़ी", f3: "आज़माना मुफ़्त",
    call_label: "नमूना कॉल · कृत्रिम आवाज़ें", caller: "कॉलर", ruko: "Ruko",
    pb_h: "ठग रोज़ नंबर बदलते हैं। स्क्रिप्ट कभी नहीं बदलते।",
    pb_p: "कॉलर ID और स्पैम लिस्ट नंबर देखती हैं। Ruko सुनता है कि क्या कहा जा रहा है। हर फ़ोन धोखा इन्हीं चार संकेतों से गुज़रता है, हर भाषा में, और Ruko जानता है कि अगला संकेत क्या है।",
    s1: "भरोसेमंद होने का नाटक", s2: "डराता या जल्दी करवाता है", s3: "परिवार से अलग करता है", s4: "OTP, पैसे या फ़ोन माँगता है",
    ruko_says: "Ruko चेताता है:", s1n: "अगला क़दम OTP माँगना है।", s2n: "असली पुलिस कभी फ़ोन पर गिरफ़्तार नहीं करती।", s3n: "अभी परिवार को बताइए। उनका फ़ोन पहले ही लाल है।", s4n: "अभी कॉल काटिए और 1930 पर कॉल कीजिए।",
    fam_h: "जब मम्मी की कॉल लाल होती है, आपका फ़ोन भी लाल होता है।",
    fam_p: "धोखा इसलिए चलता है क्योंकि कॉल पर इंसान अकेला होता है। Family Shield आपको उसी पल साथ ले आता है: लाइव कैप्शन, धोखे का क़दम, और क्या करना है।",
    fam_1: "चेतावनी आपकी अपनी आवाज़ में हो सकती है। 15 सेकंड रिकॉर्ड करें; कभी भी हटाएँ।",
    fam_2: "कीपैड फ़ोन? मम्मी कॉल को Ruko के नंबर से जोड़ें, और Ruko कॉल के अंदर ही चेतावनी देता है (जाँच में)।",
    fam_3: "जब तक कॉल सुरक्षित न की जा रही हो, कुछ भी साझा नहीं होता। कॉल की आवाज़ नहीं रखी जाती।",
    ph_parent: "यह धोखा है। कॉल काटिए।", ph_cut: "मैंने कॉल काट दी", cap_parent: "मम्मी का फ़ोन, स्पीकर पर",
    ph_child: "मम्मी इस समय धोखे वाली कॉल पर हैं", ph_c1: "अभी उन्हें कॉल कीजिए।", ph_c2: "न OTP, न पैसे, न ऐप।", cap_child: "आपका फ़ोन, ऑफ़िस में",
    feat_h: "धोखे वाली कॉल के ख़िलाफ़ परिवार को जो कुछ चाहिए",
    b1: "कॉल गार्ड", b1d: "कॉल स्पीकर पर रखें, एक बार दबाएँ। लाइव कैप्शन, धोखे के क़दम, ज़ोरदार चेतावनी।",
    b2: "पहले से चेतावनी", b2d: "ठग अगला क्या माँगेगा, माँगने से पहले बता देता है।",
    b3: "उनकी भाषा", b3d: "कॉलर की भाषा पहचानकर उसी में चेतावनी देता है, ज़रूरत हो तो धीरे।",
    b4: "कीपैड फ़ोन", b4d: "कॉल को Ruko के नंबर से जोड़ें। चेतावनी कॉल के अंदर बजती है।",
    b5: "1930 रिपोर्ट", b5d: "कॉल ख़त्म होते ही: तैयार शिकायत, किसने क्या कहा, और 1930 पर कॉल का बटन।",
    b6: "वॉइस नोट", b6d: "अजीब WhatsApp वॉइस नोट आया? Ruko जाँच लेता है।",
    proof_h: "शोर वाली फ़ोन आवाज़ पर जाँचा गया, सिर्फ़ शांत कमरे में नहीं।",
    proof_p: "Gnani के स्पीच मॉडल पर 36 लाइव जाँचें: 5 भाषाओं में 7 धोखे वाली कॉल और 2 असली कॉल, स्पीकरफ़ोन और 8 kHz फ़ोन लाइन पर, पीछे टीवी जैसी आवाज़ के साथ और बिना। सभी कॉल लिखी हुई और कृत्रिम आवाज़ों में हैं।",
    proof_l: "कहाँ कमज़ोर है: पीछे शोर होने पर 14 में से 2 चेतावनियाँ लगभग 4.5 सेकंड देर से आईं। Ruko सिर्फ़ चेतावनी देता है; कॉल कभी नहीं रोकता।",
    t_cond: "स्थिति", t_caught: "पकड़े गए धोखे", t_false: "ग़लत अलार्म", t_delay: "औसत देरी",
    c1: "स्पीकरफ़ोन", c2: "फ़ोन लाइन, 8 kHz", c3: "स्पीकर + पीछे आवाज़", c4: "फ़ोन लाइन + पीछे आवाज़",
    setup_h: "दो मिनट में मम्मी-पापा के लिए सेट करें",
    st1: "उनके फ़ोन पर Ruko खोलें", st1d: "न ऐप स्टोर, न साइन-अप। होम स्क्रीन पर जोड़ें।",
    st2: "फ़ैमिली लिंक ख़ुद को भेजें", st2d: "एक टैप में WhatsApp पर। अपने फ़ोन पर खुला रखें।",
    st3: "अपनी आवाज़ रिकॉर्ड करें (वैकल्पिक)", st3d: "ताकि चेतावनी आपकी आवाज़ में सुनाई दे।",
    biz_h: "बैंकों, UPI ऐप्स और टेलीकॉम के लिए",
    biz_p: "एक API कॉल से किसी भी कॉल में धोखे के क़दम जाँचें, और ग्राहक के धोखे में फँसे होने पर बड़ा ट्रांसफ़र रोकें। टेलीकॉम कीपैड-फ़ोन लाइन को नेटवर्क सेवा की तरह दे सकते हैं।",
    wl_h: "पायलट से जुड़ें", wl_name: "आपका नाम", wl_contact: "फ़ोन या ईमेल", wl_role: "मैं जुड़ रहा/रही हूँ",
    r_family: "मम्मी-पापा की सुरक्षा के लिए", r_self: "मुझे ऐसी कॉल आती हैं", r_bank: "बैंक या फ़िनटेक", r_telco: "टेलीकॉम", r_police: "पुलिस या साइबर सेल", r_other: "अन्य",
    wl_consent: "Ruko पायलट के बारे में मुझसे संपर्क कर सकता है। और कुछ नहीं।", wl_btn: "पायलट से जुड़ें",
    wl_ok: "आप सूची में हैं। हम जल्द संपर्क करेंगे।", wl_err: "भेज नहीं पाए। फिर कोशिश करें।", wl_sending: "भेज रहे हैं…",
    foot_1: "कॉल से पैसे गए? अभी", foot_2: "पर कॉल करें, या रिपोर्ट करें",
    foot_3: "Gnani AI Great Indian AI Internship Challenge के लिए अकेले बनाया गया। आवाज़ पहचान Gnani Prisma, आवाज़ें Gnani Timbre। Ruko सिर्फ़ चेतावनी देता है; कॉल नहीं रोकता और कॉल की आवाज़ नहीं रखता।",
    empty: "▶ दबाएँ और एक नक़ली \"CBI ऑफ़िसर\" कॉल सुनें।",
  },
};
// English strings come from the HTML itself, captured once.
for (const el of document.querySelectorAll("[data-i18n]")) STRINGS.en[el.dataset.i18n] ??= el.textContent;
Object.assign(STRINGS.en, { stop: "Stop", caller: "Caller", ruko: "Ruko", empty: "Press play to hear a made-up “CBI officer” call.",
  wl_ok: "You're on the list. We'll be in touch soon.", wl_err: "Couldn't send that. Please try again.", wl_sending: "Sending…" });

function fillStatic() {
  for (const el of document.querySelectorAll("[data-sign]")) el.innerHTML = signSVG(el.dataset.sign);
  for (const el of document.querySelectorAll("[data-oct]")) el.innerHTML = octagonSVG();
  $("dStop").innerHTML = octagonSVG();
  $("dCaptions").dataset.empty = t("empty");
  if (!playing) renderStages($("dStages"), lastBook);
}
let playing = false, lastBook = null, audio = null, stopRequested = false;
document.addEventListener("langchange", fillStatic);

// ---------- the road demo: real Timbre recordings, scored live by Ruko's engine
function playClip(src) {
  return new Promise((resolve) => {
    audio = new Audio(src);
    audio.onended = audio.onerror = () => resolve();
    audio.play().catch(() => setTimeout(resolve, 2200));  // no autoplay permission: keep pacing silently
  });
}

async function runDemo() {
  playing = true; stopRequested = false;
  $("dPlay").setAttribute("aria-pressed", "true");
  $("dPlayLabel").textContent = t("stop");
  $("dCaptions").innerHTML = ""; $("dNext").textContent = "";
  $("dStop").classList.remove("lit"); document.querySelector(".road").classList.remove("alarm");
  document.querySelector(".road").classList.add("playing");
  $("dDot").classList.add("live");
  try {
    const call = await (await fetch("/demo/call.json")).json();
    const { states } = await (await fetch("/api/analyze", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lines: call.lines, lang: "hi-IN" }) })).json();
    for (let i = 0; i < call.lines.length && !stopRequested; i++) {
      addCaption($("dCaptions"), call.lines[i], states[i], t("caller"));
      await playClip(`/demo/caller-${i + 1}.mp3`);
      if (stopRequested) break;
      lastBook = states[i].playbook;
      renderStages($("dStages"), lastBook);
      setLevel($("dLevel"), states[i]);
      $("dNext").textContent = states[i].playbook?.next || "";
      if (states[i].alert && i === call.lines.length - 1) {
        $("dStop").classList.add("lit"); document.querySelector(".road").classList.add("alarm");
        navigator.vibrate?.([300, 120, 300]);
        addCaption($("dCaptions"), call.warning, null, `${t("ruko")} (son's cloned voice):`);
        await playClip("/demo/son-warning.mp3");
      }
    }
  } catch {
    $("dNext").textContent = "The demo server is waking up. Try again in a few seconds.";
  }
  audio?.pause();
  playing = false;
  $("dDot").classList.remove("live");
  $("dPlay").setAttribute("aria-pressed", "false");
  $("dPlayLabel").textContent = t("play");
}
$("dPlay").onclick = () => { if (playing) { stopRequested = true; audio?.pause(); } else runDemo(); };

// ---------- pilot form
$("wl").onsubmit = async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target));
  data.consent = !!data.consent;
  $("wlMsg").textContent = t("wl_sending");
  try {
    const r = await fetch("/api/waitlist", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    if (!r.ok) throw new Error();
    e.target.reset();
    $("wlMsg").textContent = t("wl_ok");
  } catch {
    $("wlMsg").textContent = t("wl_err");
  }
};

applyLang(LANG);
fillStatic();
