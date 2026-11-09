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
    assert gnani.speak_lang("auto", "kn-IN") == "kn-IN" and gnani.speak_lang("auto", "bn-IN") == "hi-en"
    assert gnani.speak_lang("te-IN", "kn-IN") == "te-IN"  # a chosen language is never overridden
    assert gnani.elder_text("Ruko! Phone kaat dijiye. Call 1930.") == \
        "<slow> Ruko! <pauses> <slow> Phone kaat dijiye. <pauses> <slow> Call 1930."


def test_phone_line_feeds_family_screen():
    from backend.telephony import voice  # noqa: F401  (route exists)
    r = client.post("/twilio/voice?lang=auto&family=abcd2345ef")
    assert 'name="family" value="abcd2345ef"' in r.text and 'value="auto"' in r.text
    r = client.post("/twilio/voice?family=BAD!")
    assert 'name="family" value=""' in r.text
