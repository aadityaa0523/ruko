"""Golden-hour pack: turns a scored call into evidence, a 1930 / cybercrime.gov.in complaint and a family alert.

Template-only (no LLM), so every sentence comes from what was actually said on the call.
"""
import re
from datetime import datetime

MONEY = re.compile(r"(₹|\brs\b|rupa?ye|rupees|hazaa?r|lakh|रुपय|रुपए|हज़ार|हजार|लाख|ರೂಪಾಯ|ಸಾವಿರ|రూపాయ|వేల)", re.I)

# What each red flag means, for the complaint (English) and the family alert (Hinglish).
ASK_EN = {"payment": "an OTP / PIN or a money transfer", "remote": "installing a remote-access app or clicking a link",
          "secrecy": "keeping the call secret from family", "threat": "threats of arrest or of blocking a service",
          "refund_trick": "returning money supposedly 'sent by mistake'"}
ASK_HI = {"payment": "OTP ya paise", "remote": "app install ya link click", "secrecy": "baat chhupane",
          "threat": "giraftari ya band karne ki dhamki", "refund_trick": "galti se bheje paise wapas"}


def build_pack(lines: list[dict], started: datetime, lang: str) -> dict:
    """lines: [{"t": seconds_from_start, "text": str, "risk": risk_state_after_this_line}]"""
    final = lines[-1]["risk"] if lines else {"level": "safe", "score": 0, "flags": []}
    flags = {f["category"]: f["phrase"] for f in final["flags"]}
    moments = [{"t": l["t"], "text": l["text"], "new": l["risk"]["new"]} for l in lines if l["risk"]["new"]]
    money = [l["text"] for l in lines if MONEY.search(l["text"])]
    asks = [c for c in ("payment", "remote", "secrecy", "threat", "refund_trick") if c in flags]
    claimed = flags.get("authority")
    if claimed and claimed.isascii() and len(claimed) <= 4:
        claimed = claimed.upper()  # cbi -> CBI
    when = started.strftime("%d %b %Y, %I:%M %p")
    duration = round(lines[-1]["t"]) if lines else 0

    desc = [f"On {when} I received a phone call that I believe was a fraud (vishing / impersonation) attempt."]
    if claimed:
        desc.append(f'The caller claimed to be from / referred to "{claimed}".')
    if asks:
        desc.append("The caller asked for or pressured me about: " + "; ".join(ASK_EN[a] for a in asks) + ".")
    if money:
        desc.append("Money mentioned on the call: " + " | ".join(f'"{m}"' for m in money[:3]) + ".")
    desc.append("Key statements made by the caller, with time from the start of the call:")
    desc += [f'  [{_mmss(m["t"])}] "{m["text"]}"' for m in moments[:8]]
    desc.append("This transcript was produced automatically by the Ruko app (speech recognition by Gnani AI Prisma) "
                "and may contain recognition errors.")

    complaint = {
        "portal": "https://cybercrime.gov.in",
        "helpline": "1930",
        "category": "Online Financial Fraud",
        "sub_category": "Fraud call / vishing (impersonation)",
        "incident_datetime": when,
        "call_duration_seconds": duration,
        "suspect_phone_number": "[enter the number that called you]",
        "amount_lost": "[enter amount if any money was lost, else 0]",
        "description": "\n".join(desc),
    }
    family = None
    if final["level"] in ("high", "critical"):
        parts = [f"Ruko alert. Aaj {started.strftime('%I:%M %p')} par aapke parivaar ke phone par ek sandigdh call aayi."]
        if claimed:
            parts.append(f"Caller ne {claimed} ka naam liya.")
        if asks:
            parts.append("Usne " + ", ".join(ASK_HI[a] for a in asks) + " ki baat ki.")
        parts.append("Ruko ne chetavni de di hai. Kripya unhe abhi call kijiye.")
        family = " ".join(parts)
    return {"level": final["level"], "score": final["score"], "flags": final["flags"], "moments": moments,
            "money_mentions": money, "complaint": complaint, "family_alert": family, "lang": lang,
            "transcript": [{"t": l["t"], "text": l["text"]} for l in lines]}


def pick_caller(segments: list[dict], flagged_texts: list[str]) -> int | None:
    """Diarized speaker who said most of the red-flag lines is the caller."""
    from backend.risk import find_flags
    score: dict[int, int] = {}
    for s in segments:
        if s.get("speaker_id", -1) >= 0 and s.get("text"):
            score[s["speaker_id"]] = score.get(s["speaker_id"], 0) + len(find_flags(s["text"]))
    return max(score, key=score.get) if score and max(score.values()) > 0 else None


def _mmss(t: float) -> str:
    return f"{int(t // 60):02d}:{int(t % 60):02d}"
