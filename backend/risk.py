"""Call-level scam risk.

Scores the *pattern* of a whole call (authority + threat + secrecy + payment ...),
not single keywords: each category counts once per call, and an alert needs at
least two categories including a dangerous one. Phrases cover Roman Hinglish,
Devanagari, Kannada and Telugu, because Prisma may return any of these scripts.
"""
import re
from dataclasses import dataclass, field

WEIGHTS = {"authority": 2, "threat": 3, "secrecy": 3, "urgency": 1,
           "payment": 3, "remote": 3, "refund_trick": 3}
DANGER = {"threat", "secrecy", "payment", "remote", "refund_trick"}
ALERT_AT = 6
CRITICAL_AT = 9
MAX_SCORE = 12  # for the 0-100 meter

LABELS = {
    "authority": "Claims to be an official",
    "threat": "Threat or deadline",
    "secrecy": "Asks you to keep it secret",
    "urgency": "Pressure to act now",
    "payment": "Asks for OTP / PIN / money",
    "remote": "Asks to install app or click link",
    "refund_trick": "'Sent by mistake' refund trick",
}

PHRASES = {
    "authority": [
        "cbi", "police", "cyber cell", "crime branch", "customs", "narcotics", "enforcement directorate",
        "rbi", "sbi", "bank", "bank manager", "head office", "trai", "income tax", "court", "judge",
        "army", "fauj", "military", "pm kisan", "kisan samman", "ayushman", "bijli vibhag",
        "electricity board", "ration card", "government officer", "sarkari",
        "पुलिस", "सीबीआई", "बैंक", "आर्मी", "फौज", "किसान", "आयुष्मान", "विभाग", "दफ़्तर", "दफ्तर",
        "थाने", "थाना", "सरकारी", "कस्टम", "पी एम किसान",
        "ಪೊಲೀಸ್", "ಬ್ಯಾಂಕ್", "ಸಿಬಿಐ", "పోలీస్", "బ్యాంక్", "సీబీఐ",
    ],
    "threat": [
        "arrest", "digital arrest", "warrant", "case darj", "fir", "jail", "giraftar", "giraftaar",
        "account freeze", "freeze ho", "block ho", "band ho jayega", "band ho jayegi", "band ho jaega",
        "kat jayegi", "kat jayega", "cut ho jayegi", "kist ruk", "kist band", "drugs", "money laundering",
        "illegal", "गिरफ्तार", "वारंट", "बंद हो जाएग", "band हो", "bond हो", "block हो", "ब्लॉक हो", "freeze हो",
        "कट जाएग", "किस्त रुक", "किस्त बंद", "जेल", "केस दर्ज", "ड्रग्स", "डिजिटल अरेस्ट", "ಬಂಧನ", "ಕೇಸ್", "case ಆಗಿದೆ", "block ಆಗ", "block అవ", "అరెస్ట్", "బ్లాక్",
    ],
    "secrecy": [
        "kisi ko mat batana", "kisi ko mat bataiye", "kisi ko na batayein", "kisi ko na bataye",
        "ghar walon ko mat", "family ko mat", "call mat kaatna", "phone mat kaatna", "call disconnect mat",
        "confidential", "don t tell anyone", "do not tell anyone",
        "किसी को मत बता", "किसी को न बता", "किसी को नहीं बता", "घर वालों को मत", "घरवालों को मत",
        "परिवार को मत", "मत काटना", "ಯಾರಿಗೂ ಹೇಳಬೇಡಿ", "ఎవరికీ చెప్పకండి",
    ],
    "urgency": [
        "turant", "abhi ke abhi", "jaldi", "immediately", "right now", "aaj raat", "last date",
        "last chance", "warna", "तुरंत", "अभी के अभी", "जल्दी", "वरना", "आज रात", "आज ही", "ತಕ್ಷಣ", "వెంటనే",
    ],
    "payment": [
        "otp", "o t p", "upi pin", "cvv", "card number", "pin batao", "pin bataiye", "safe account",
        "transfer kariye", "transfer karo", "transfer kar do", "paise bhejo", "paise bhejiye",
        "hazaar bhejiye", "rupaye bhejiye", "wapas bhej", "payment kariye", "payment karo", "payment kar do",
        "qr code scan", "collect request", "security deposit", "jurmana",
        "ओटीपी", "ओ टी पी", "पैसे भेज", "हज़ार भेज", "हजार भेज", "रुपये भेज", "वापस भेज", "transfer कर", "payment कर",
        "पिन बता", "सेफ अकाउंट", "स्कैन कर", "ಒಟಿಪಿ", "ಹಣ ಕಳುಹಿಸಿ", "ఓటీపీ", "డబ్బు పంపండి",
    ],
    "remote": [
        "anydesk", "any desk", "teamviewer", "team viewer", "quicksupport", "screen share",
        "screen sharing", "link pe click", "link par click", "apk", "app download karo",
        "link पे click", "link पर click", "लिंक पर क्लिक", "स्क्रीन शेयर",
    ],
    "refund_trick": ["galti se", "by mistake", "wrong transfer", "galat transfer", "galat number pe",
                     "गलती से", "ग़लती से", "गलत transfer"],
}

# Genuine safety advice (from real banks, or Ruko's own warning) is removed before matching.
SAFE_ADVICE = [
    r"otp kisi ko (na|mat|nahi) bata\w*",
    r"kabhi( bhi)?[\w ]{0,40}(otp|o t p)[\w ]{0,30}nahi maang\w*",
    r"never share (your )?otp",
    r"(otp|ओटीपी) किसी को (न|मत|नहीं) बता[\wऀ-ൿ]*",
    r"कभी( भी)?[\wऀ-ൿ ]{0,40}(otp|ओटीपी)[\wऀ-ൿ ]{0,30}नहीं मा[ंँ]?ग[\wऀ-ൿ]*",
]


def normalize(text: str) -> str:
    # Keep Latin word chars and Indic blocks (Devanagari..Malayalam, incl. combining marks), minus dandas.
    return " " + " ".join(re.sub(r"[^\wऀ-ॣ०-ൿ]+", " ", text.lower()).split()) + " "


def find_flags(text: str) -> list[tuple[str, str]]:
    norm = normalize(text)
    for pat in SAFE_ADVICE:
        norm = re.sub(pat, " ", norm)
    hits = []
    for cat, phrases in PHRASES.items():
        for p in phrases:
            # Latin phrases match whole words; Indic phrases as substrings (suffixes attach).
            if (f" {p} " if p.isascii() else p) in norm:
                hits.append((cat, p))
                break
    return hits


# Every phone scam runs the same playbook; Ruko shows where the call is and what comes next.
STAGES = [
    ("pose", "Pretends to be someone you trust", {"authority", "refund_trick"}),
    ("fear", "Scares you or rushes you", {"threat", "urgency"}),
    ("isolate", "Cuts you off from family", {"secrecy"}),
    ("ask", "Asks for OTP, money or your phone", {"payment", "remote"}),
]
NEXT = {
    "refund": "Next they will ask you to send the money back. Open your bank app yourself: the money is usually not there.",
    "police": "Real police, CBI or courts never arrest anyone on a phone or video call, and never ask for money.",
    "isolate": "Next they will tell you not to tell your family. Tell them right now.",
    "ask": "Next they will ask for an OTP, PIN, money or to install an app. Never do it on a call.",
    "final": "This is the last step of the scam. Cut the call now and call 1930.",
}
POLICE = {"cbi", "police", "cyber cell", "crime branch", "customs", "narcotics", "court", "judge",
          "पुलिस", "सीबीआई", "थाने", "थाना", "कस्टम", "ಪೊಲೀಸ್", "ಸಿಬಿಐ", "పోలీస్", "సీబీఐ"}


def playbook(flags: dict) -> dict:
    done = {k for k, _, cats in STAGES if cats & flags.keys()}
    if not done:
        nxt = None
    elif "ask" in done:
        nxt = NEXT["final"]
    elif "refund_trick" in flags:
        nxt = NEXT["refund"]
    elif flags.get("authority") in POLICE and "fear" in done:
        nxt = NEXT["police"]
    elif "fear" in done and "isolate" not in done:
        nxt = NEXT["isolate"]
    else:
        nxt = NEXT["ask"]
    return {"stages": [{"key": k, "label": l, "done": k in done} for k, l, _ in STAGES], "next": nxt}


@dataclass
class CallRisk:
    flags: dict = field(default_factory=dict)  # category -> first phrase that triggered it
    stage: int = 0  # 0 none, 1 high alert sent, 2 critical alert sent

    def feed(self, text: str) -> dict:
        new = []
        for cat, phrase in find_flags(text):
            if cat not in self.flags:
                self.flags[cat] = phrase
                new.append(cat)
        raw = sum(WEIGHTS[c] for c in self.flags)
        alertable = raw >= ALERT_AT and len(self.flags) >= 2 and bool(DANGER & self.flags.keys())
        stage = (2 if raw >= CRITICAL_AT else 1) if alertable else 0
        alert = stage > self.stage
        self.stage = max(self.stage, stage)
        level = ["safe", "watch", "high", "critical"][0 if raw == 0 else stage + 1]
        return {
            "score": min(100, round(raw / MAX_SCORE * 100)),
            "level": level,
            "alert": alert,
            "new": new,
            "flags": [{"category": c, "label": LABELS[c], "phrase": p} for c, p in self.flags.items()],
            "playbook": playbook(self.flags),
        }
