"""Check anything: an SMS, a WhatsApp forward, a link, a UPI request or a phone number.

Reuses the call playbook (risk.py) for the words, and adds message-only signals: links, lookalike domains,
APK files, UPI collect requests and phone numbers to report or look up. Rules only, so every verdict
can be explained line by line.
"""
import re
from urllib.parse import urlparse

from backend.risk import LABELS, MAX_SCORE, WEIGHTS, CallRisk

SHORTENERS = {"bit.ly", "tinyurl.com", "t.ly", "cutt.ly", "is.gd", "rb.gy", "shorturl.at", "tiny.cc", "ow.ly", "rebrand.ly", "goo.gl", "s.id"}
BRANDS = ["sbi", "hdfc", "icici", "axis", "kotak", "paytm", "phonepe", "gpay", "googlepay", "amazon", "flipkart",
          "irctc", "uidai", "aadhaar", "epfo", "incometax", "npci", "bescom", "tneb", "msedcl", "electricity", "kyc",
          "pmkisan", "ayushman", "rbi", "police", "cybercrime", "fedex", "dhl", "bluedart", "indiapost"]
# Official domains are not suspicious just because they contain a brand name.
OFFICIAL = {"sbi.co.in", "onlinesbi.sbi", "hdfcbank.com", "icicibank.com", "axisbank.com", "kotak.com", "paytm.com",
            "phonepe.com", "pay.google.com", "amazon.in", "amazon.com", "flipkart.com", "irctc.co.in", "uidai.gov.in",
            "epfindia.gov.in", "incometax.gov.in", "npci.org.in", "rbi.org.in", "cybercrime.gov.in", "pmkisan.gov.in",
            "indiapost.gov.in", "sancharsaathi.gov.in", "gov.in", "nic.in", "wa.me", "whatsapp.com", "youtube.com", "youtu.be",
            # banks, cards and insurers
            "sbicard.com", "sbilife.co.in", "sbimf.com", "bankofbaroda.in", "bankofbaroda.com", "pnbindia.in", "canarabank.com",
            "unionbankofindia.co.in", "bankofindia.co.in", "indianbank.in", "iob.in", "centralbankofindia.co.in", "idbibank.in",
            "yesbank.in", "indusind.com", "idfcfirstbank.com", "federalbank.co.in", "aubank.in", "rblbank.com", "bandhanbank.com",
            "hdfclife.com", "iciciprulife.com", "icicilombard.com", "licindia.in", "policybazaar.com", "hdfcsec.com", "icicidirect.com",
            # payments, telcos, utilities, shopping, travel
            "bhimupi.org.in", "razorpay.com", "cred.club", "mobikwik.com", "airtel.in", "jio.com", "myvi.in", "bsnl.co.in",
            "tatapower.com", "adanielectricity.com", "bescom.co.in", "tangedco.org", "mahadiscom.in", "myntra.com", "meesho.com",
            "swiggy.com", "zomato.com", "bigbasket.com", "blinkit.com", "zeptonow.com", "makemytrip.com", "redbus.in", "indianrail.gov.in",
            "bluedart.com", "delhivery.com", "dhl.com", "fedex.com",
            # government and big platforms
            "india.gov.in", "mygov.in", "digilocker.gov.in", "umang.gov.in", "passportindia.gov.in", "parivahan.gov.in",
            "google.com", "apple.com", "microsoft.com", "linkedin.com", "github.com", "instagram.com", "facebook.com", "x.com"}
RISKY_TLDS = {"xyz", "top", "click", "link", "live", "online", "site", "info", "buzz", "shop", "icu", "cfd", "sbs", "rest", "lol", "monster", "fun"}

URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"')]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|in|net|org|xyz|top|click|link|live|online|site|info|buzz|shop|icu|ly|gl|me|co|io|apk)(?:/[^\s<>\"')]*)?", re.I)
PHONE_RE = re.compile(r"(?<![\d])(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)|(?<![\d])1[48]\d{2}[\s-]?\d{3}[\s-]?\d{4}(?!\d)")
UPI_RE = re.compile(r"\b[\w.-]{2,}@(?:ok\w+|ybl|ibl|axl|paytm|upi|apl|airtel|fbl|icici|hdfcbank|sbi|kotak|axisbank|yesbank|freecharge|jio)\b", re.I)
MESSAGE_SIGNS = {
    "link_bait": [r"click (?:on )?(?:the |this )?link", r"link (?:pe|par|पर|पे) click", r"update (?:your )?kyc", r"kyc (?:update|expired|pending)",
                  r"verify (?:your )?(?:account|pan|aadhaar)", r"लिंक पर क्लिक", r"kyc अपडेट"],
    "prize": [r"(?:you have )?won", r"lottery", r"lucky draw", r"cash ?back of", r"reward points? (?:expir|redeem)", r"इनाम", r"लॉटरी", r"kbc"],
    "job": [r"part[- ]time job", r"work from home.{0,30}(?:earn|daily)", r"earn ₹?\s?\d[\d,]* (?:per|daily|a day)", r"like (?:and|&) subscribe.{0,20}earn", r"task.{0,20}(?:earn|commission)"],
    "bill": [r"electricity (?:connection|power) (?:will be )?(?:disconnected|cut)", r"bijli (?:kat|cut)", r"बिजली.{0,40}(?:कट|काट)", r"bill (?:not|un) ?paid", r"last bill",
             r"(?:connection|power supply|gas supply|subsidy).{0,30}(?:disconnect|cut off|discontinu|kaat|kat)"],
    "callback": [r"contact (?:our )?(?:officer|executive|agent|department)", r"call (?:on |us on |this number|immediately on)", r"whatsapp (?:on|us|me)", r"(?:contact|message|ping)(?: us)? on whatsapp",
                 r"इस नंबर पर (?:कॉल|संपर्क)", r"(?:call|contact) (?:karo|kijiye|करें)", r"call (?:our |the )?(?:24x7 )?(?:helpline|customer care)", r"customer care (?:on|number|no)",
                 r"(?:अधिकारी|विभाग|ऑफिसर).{0,20}संपर्क करें", r"whatsapp करें", r"\bpress [0-9]\b", r"[0-9] दबाएं"],
    "parcel": [r"(?:parcel|package|courier|consignment|पार्सल).{0,80}(?:held|seized|customs|drugs|mdma|contraband|returned|पकड़)", r"courier.{0,30}(?:held|returned|address)",
               r"delivery (?:failed|pending).{0,30}(?:update|link)", r"address (?:galat|incorrect|is wrong|update kar)"],
    # Message-only scam types (not in the call playbook)
    "loan": [r"pre-?approved (?:personal )?loan", r"\b0% interest", r"instant (?:loan|disbursal)", r"loan.{0,60}(?:contacts|photo|fraud ho|morph)",
             r"(?:contacts|कॉन्टैक्ट्स).{0,50}(?:photo|फोटो|message|bhej|भेज)", r"लोन.{0,60}(?:फोटो|कॉन्टैक्ट)"],
    "blackmail": [r"(?:video|recording|photos?|pics?).{0,60}(?:send|bhej|viral|youtube|leak|friends and family|ghar waal)", r"\bnude\b",
                  r"settle (?:the|this) matter", r"(?:वीडियो|फोटो).{0,40}(?:भेज|वायरल)"],
    "relative": [r"(?:this is )?my new number", r"phone (?:broke|is broken|kharab|toot)", r"accident ho gaya", r"(?:hospital|operation).{0,40}(?:chahiye|need|pay|bhej)",
                 r"dost bol raha", r"एक्सीडेंट", r"नया नंबर"],
    "invest": [r"guaranteed (?:returns?|profit)", r"\d+% (?:guaranteed |assured )?(?:returns?|profit)", r"\busdt\b", r"\bcrypto\b", r"trading (?:group|tips|signals)",
               r"stock tips", r"double your money", r"पैसा डबल", r"\bvip (?:group|signals)"],
    "block": [r"(?:wallet|account|sim|mobile number|number|kyc).{0,30}(?:has been |will be |is )?(?:blocked|suspended|deactivated)", r"नंबर.{0,40}बंद कर दिया जाएग"],
    "fee": [r"(?:registration|processing|delivery|release|customs|unlock|clearance) (?:fee|charge)", r"(?:रजिस्ट्रेशन )?(?:फीस|शुल्क)", r"deposit karna",
            r"\brs\.? ?\d+ pay kar", r"pay (?:rs\.?|₹) ?\d+ (?:to|for|and)"],
    "pay_request": [r"(?:gpay|phonepe|google pay|paytm|upi) kar (?:do|dijiye|dena)", r"(?:quick|urgent) payment", r"send (?:me|it) (?:once|now|asap|urgently)",
                    r"\d[\d,]* (?:turant )?chahiye", r"(?:bhar|bhej) do varna"],
}
SIGN_LABELS = {"link_bait": "Pushes you to click a link or update KYC", "prize": "Promises a prize, lottery or reward",
               "job": "Easy-money job or task offer", "bill": "Threatens to cut your electricity or service",
               "parcel": "Fake parcel, courier or customs problem", "callback": "Pushes you to call or WhatsApp a private number", "risky_link": "Suspicious link", "apk": "Asks you to install an app file (APK)",
               "upi_collect": "UPI ID or payment request", "loan": "Instant-loan offer or loan-app harassment",
               "blackmail": "Blackmail with a video or photo", "relative": "Pretends to be family or a friend in trouble",
               "invest": "Guaranteed-returns investment or crypto tips", "block": "Says your account, wallet or SIM is blocked",
               "fee": "Asks for a fee before you get something", "pay_request": "Asks you to pay or send money quickly"}
ADVICE = {
    "scam": "Don't click, pay, reply or share any OTP. Block the sender. If you already paid, call 1930 now.",
    "suspicious": "Be careful. Don't click links or pay. Check with the official app or website yourself, not through this message.",
    "safe": "No scam signs found. Still never share an OTP, PIN or password with anyone.",
}


def _host(url: str) -> str:
    u = url if "://" in url else "http://" + url
    return (urlparse(u).hostname or "").lower().removeprefix("www.")


def link_flags(url: str) -> list[str]:
    host = _host(url)
    if not host:
        return []
    if any(host == d or host.endswith("." + d) for d in OFFICIAL):
        return []
    why = []
    if host in SHORTENERS:
        why.append("hides the real address behind a link shortener")
    if url.lower().split("?")[0].endswith(".apk"):
        why.append("downloads an app file (APK) from outside the Play Store")
    if re.fullmatch(r"\d+\.\d+\.\d+\.\d+", host):
        why.append("is a bare number address, not a real website")
    tld = host.rsplit(".", 1)[-1]
    if tld in RISKY_TLDS:
        why.append(f"uses a .{tld} address, common in scams")
    flat = host.replace("-", "").replace(".", "")
    brand = next((b for b in BRANDS if b in flat), None)
    if brand:
        why.append(f"uses \"{brand}\" in the name but is not the official site")
    if host.count("-") >= 2 or len(host) > 30:
        why.append("has a long, made-up looking name")
    return why


def norm_phone(p: str) -> str:
    """Last 10 digits for Indian mobiles; full digits otherwise (shared with the number-report table)."""
    d = re.sub(r"\D", "", p)
    return d[-10:] if len(d) >= 10 and d[-10] in "6789" else d


def check_text(text: str) -> dict:
    text = text[:4000]
    risk = CallRisk()
    state = risk.feed("")
    for part in re.split(r"(?<=[.!?।\n])\s*", text):
        if part.strip():
            state = risk.feed(part)
    flags = [{"category": f["category"], "label": f["label"], "phrase": f["phrase"]} for f in state["flags"]]

    low = text.lower()
    phones = sorted({norm_phone(p) for p in PHONE_RE.findall(text)})
    # A genuine OTP delivery ("123456 is your OTP ... do not share") mentions an OTP but doesn't ask for one.
    otp_safe = re.search(r"do not share|don'?t share|never share|never asks?|share na kar|na batay|kisi ko na|share (?:the )?(?:delivery )?otp.{0,15}only with|"
                         r"किसी को न|किसी के साथ साझा न|कभी भी.{0,40}नहीं म", low)
    if otp_safe and re.search(r"\b(?:otp|pin|one[- ]time password)\b|ओटीपी", low):
        flags = [f for f in flags if f["category"] not in ("payment", "secrecy")]
    for key, pats in MESSAGE_SIGNS.items():
        hit = next((m.group(0) for p in pats for m in [re.search(p, low)] if m), None)
        if hit:
            flags.append({"category": key, "label": SIGN_LABELS[key], "phrase": hit})

    links = []
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip(".,;:!?")
        if "@" in url:
            continue
        why = link_flags(url)
        links.append({"url": url, "host": _host(url), "why": why})
        if why:
            flags.append({"category": "apk" if "APK" in " ".join(why) else "risky_link", "label": SIGN_LABELS["apk" if "APK" in " ".join(why) else "risky_link"], "phrase": _host(url)})
    upi = sorted(set(UPI_RE.findall(text)))
    if upi and re.search(r"collect|request|approve|scan|pay|भेज|अनुरोध|receive", low):
        flags.append({"category": "upi_collect", "label": SIGN_LABELS["upi_collect"], "phrase": upi[0]})
    if not phones:  # "call us" only matters when there's a private number to call
        flags = [f for f in flags if f["category"] != "callback"]
    # "Update your KYC" with nothing to click, call or pay is the bank's own reminder ("visit your branch").
    if not phones and not upi and not any(f["category"] in ("risky_link", "apk") for f in flags):
        flags = [f for f in flags if f["category"] != "link_bait"]

    cats = {f["category"] for f in flags}
    # block, fee and pay_request are weak alone (real bills and family ask for money); they count with another sign.
    danger = {"callback", "threat", "secrecy", "payment", "remote", "refund_trick", "risky_link", "apk", "upi_collect", "bill", "parcel", "job", "prize",
              "link_bait", "loan", "blackmail", "relative", "invest"}
    call_cats = cats & set(LABELS)
    score = round(sum(WEIGHTS[c] for c in call_cats) / MAX_SCORE * 100) + 20 * len(cats - set(LABELS))
    strong = len(cats) >= 2 and bool(cats & danger)
    verdict = "scam" if (strong and score >= 40) or {"apk", "risky_link"} & cats and len(cats) >= 2 else ("suspicious" if cats & danger or score >= 30 else "safe")
    return {
        "verdict": verdict,
        "score": min(100, score if verdict != "safe" else min(score, 25)),
        "flags": flags,
        "links": links,
        "phones": phones,
        "upi": upi,
        "playbook": state["playbook"],
        "advice": ADVICE[verdict],
    }
