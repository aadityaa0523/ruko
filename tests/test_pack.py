from datetime import datetime

from backend.pack import build_pack, pick_caller
from backend.risk import CallRisk
from backend.scripts import SAFE, SCAM


def pack_for(lines):
    risk = CallRisk()
    rows = [{"t": i * 5.0, "text": t, "risk": risk.feed(t)} for i, t in enumerate(lines)]
    return build_pack(rows, datetime(2026, 11, 9, 14, 30), "hi-en")


def test_scam_pack_has_evidence_and_complaint():
    p = pack_for(SCAM["relative_in_custody"])
    c = p["complaint"]
    assert p["level"] in ("high", "critical")
    assert c["category"] == "Online Financial Fraud" and c["helpline"] == "1930"
    assert '"police"' in c["description"]  # claimed identity is quoted from the call
    assert "pachaas hazaar" in c["description"]  # money mention kept verbatim
    assert "[00:00]" in c["description"]  # timestamped moments
    assert p["family_alert"] and "police" in p["family_alert"]


def test_complaint_only_uses_what_was_said():
    p = pack_for(SCAM["army_kirana_order"])
    assert "arrest" not in p["complaint"]["description"].lower()
    assert "[enter the number that called you]" == p["complaint"]["suspect_phone_number"]


def test_safe_call_gets_no_family_alert():
    assert pack_for(SAFE["doctor_appointment"])["family_alert"] is None


def test_empty_call_pack():
    p = build_pack([], datetime(2026, 11, 9), "hi-en")
    assert p["level"] == "safe" and p["moments"] == []


def test_pick_caller_is_speaker_with_red_flags():
    segs = [{"speaker_id": 0, "text": "Haan ji, kaun?"},
            {"speaker_id": 1, "text": "Main CBI se bol raha hoon, OTP batao"},
            {"speaker_id": 0, "text": "Kya hua?"}, {"speaker_id": -1, "text": ""}]
    assert pick_caller(segs, []) == 1
    assert pick_caller([{"speaker_id": 0, "text": "namaste"}], []) is None
