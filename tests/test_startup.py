from fastapi.testclient import TestClient

from backend import app as appmod
from backend.app import app

client = TestClient(app)
LINES = ["Main CBI se bol raha hoon", "aapke naam warrant hai", "kisi ko mat batana"]


def test_score_api_needs_key_and_returns_playbook():
    assert client.post("/v1/score", json={"lines": LINES}).status_code == 401
    r = client.post("/v1/score", json={"lines": LINES}, headers={"X-Ruko-Key": "demo"}).json()
    assert r["level"] in ("high", "critical") and r["playbook"]["next"]


def test_waitlist_validates_and_stores(tmp_path, monkeypatch):
    monkeypatch.setattr(appmod, "WAITLIST", tmp_path / "w.jsonl")
    lead = {"name": "Asha", "contact": "asha@example.com", "role": "family", "consent": True}
    assert client.post("/api/waitlist", json={**lead, "consent": False}).status_code == 422
    assert client.post("/api/waitlist", json={**lead, "role": "spam"}).status_code == 422
    assert client.post("/api/waitlist", json=lead).json() == {"ok": True}
    assert "Asha" in (tmp_path / "w.jsonl").read_text(encoding="utf-8")


def test_family_screen_gets_live_events_and_replay():
    code = "abcd2345ef"
    with client.websocket_connect(f"/ws/family?c={code}") as fam:
        client.post("/api/family/publish", json={"code": code, "msg": {"type": "call_start"}})
        client.post("/api/family/publish", json={"code": code, "msg": {"type": "warning", "audio": "xx", "level": "high"}})
        client.post("/api/family/publish", json={"code": code, "msg": {"type": "evil"}})
        assert fam.receive_json()["type"] == "call_start"
        w = fam.receive_json()
        assert w["type"] == "warning" and "audio" not in w
    with client.websocket_connect(f"/ws/family?c={code}") as late:  # joins late: replay
        assert [late.receive_json()["type"] for _ in range(2)] == ["call_start", "warning"]


def test_family_rejects_bad_code():
    import pytest
    from starlette.websockets import WebSocketDisconnect
    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws/family?c=BAD!") as ws:
            ws.receive_json()


def test_auto_language_and_elder_text():
    from backend import gnani
    assert gnani.stt_headers("auto", "prisma-v3.0")["language_code"] == "indic-auto"
    assert gnani.speak_lang("auto", "kn-IN") == "kn-IN" and gnani.speak_lang("auto", "pa-IN") == "hi-en" and gnani.speak_lang("auto", "bn-IN") == "bn-IN"
    assert gnani.speak_lang("te-IN", "kn-IN") == "te-IN"  # a chosen language is never overridden
    assert gnani.elder_text("Ruko! Phone kaat dijiye. Call 1930.") == \
        "<slow> Ruko! <pauses> <slow> Phone kaat dijiye. <pauses> <slow> Call 1930."


def test_phone_line_feeds_family_screen():
    from backend.telephony import voice  # noqa: F401  (route exists)
    r = client.post("/twilio/voice?lang=auto&family=abcd2345ef")
    assert 'name="family" value="abcd2345ef"' in r.text and 'value="auto"' in r.text
    r = client.post("/twilio/voice?family=BAD!")
    assert 'name="family" value=""' in r.text


def test_ulaw_encoder_round_trips():
    import array
    from backend.gnani import pcm16_to_ulaw
    from backend.telephony import ulaw_to_pcm16
    src = array.array("h", [0, 100, -100, 1000, -1000, 12000, -12000, 32767, -32768])
    back = array.array("h"); back.frombytes(ulaw_to_pcm16(pcm16_to_ulaw(src.tobytes())))
    for a, b in zip(src, back):
        assert abs(a - b) <= max(16, abs(a) * 0.07), (a, b)


def test_family_voice_needs_consent_and_can_be_deleted(monkeypatch):
    from backend import family, gnani

    async def fake_clone(data, name):
        return {"embedding": "e" * 80, "shape": [1, 768], "dtype": "torch.bfloat16"}
    monkeypatch.setattr(gnani, "clone_voice", fake_clone)
    wav = {"file": ("v.wav", b"\0" * 20000, "audio/wav")}
    c = "voicefam23"
    assert client.post("/api/family/voice", data={"c": c, "consent": "false"}, files=wav).status_code == 400
    short = {"file": ("v.wav", b"\0" * 100, "audio/wav")}
    assert client.post("/api/family/voice", data={"c": c, "consent": "true"}, files=short).status_code == 400
    ok = client.post("/api/family/voice", data={"c": c, "consent": "true", "name": "Rahul"}, files=wav)
    assert ok.json() == {"ok": True}
    assert client.get(f"/api/family/voice?c={c}").json() == {"has_voice": True, "name": "Rahul"}
    assert family.voice_for(c)["shape"] == [1, 768]
    assert client.delete(f"/api/family/voice?c={c}").json() == {"deleted": True}
    assert family.voice_for(c) is None


def test_push_subscribe_and_one_push_per_call(monkeypatch):
    from backend import family
    sent = []
    monkeypatch.setenv("VAPID_PRIVATE_KEY", "x")
    monkeypatch.setattr(family, "_send_push", lambda sub, payload: sent.append(payload) or True)
    c = "pushfam234"
    sub = {"endpoint": "https://push.example.com/abc", "keys": {"p256dh": "k", "auth": "a"}}
    assert client.post("/api/push/subscribe", json={"c": c, "name": "Mummy", "subscription": {"endpoint": "http://x"}}).status_code == 400
    assert client.post("/api/push/subscribe", json={"c": c, "name": "Mummy", "subscription": sub}).json() == {"ok": True}
    for msg in ({"type": "call_start"}, {"type": "transcript", "text": "t", "risk": {"playbook": {"next": "Next they will ask for an OTP."}}},
                {"type": "warning", "level": "high"}, {"type": "warning", "level": "critical"}):
        client.post("/api/family/publish", json={"code": c, "msg": msg})
    assert len(sent) == 1 and sent[0]["title"] == "Mummy is on a scam call right now" and "OTP" in sent[0]["body"]
