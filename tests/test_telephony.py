import array

from fastapi.testclient import TestClient

from backend import telephony
from backend.app import app
from backend.telephony import twilio_signature, ulaw_to_pcm16


def test_ulaw_decode_matches_g711():
    pcm = array.array("h", ulaw_to_pcm16(bytes([0xFF, 0x7F, 0x00, 0x80])))
    assert list(pcm) == [0, 0, -32124, 32124]


def test_signature_changes_with_any_param():
    url = "https://ruko.example/twilio/voice?lang=kn-IN"
    good = twilio_signature(url, {"CallSid": "CA1", "From": "+910000000000"}, "secret")
    assert good == twilio_signature(url, {"From": "+910000000000", "CallSid": "CA1"}, "secret")  # order-free
    assert good != twilio_signature(url, {"CallSid": "CA2", "From": "+910000000000"}, "secret")
    assert good != twilio_signature(url, {"CallSid": "CA1", "From": "+910000000000"}, "other")


def test_voice_webhook_returns_stream_twiml(monkeypatch):
    monkeypatch.delenv("TWILIO_AUTH_TOKEN", raising=False)
    monkeypatch.setenv("RUKO_PUBLIC_URL", "https://ruko.example")
    r = TestClient(app).post("/twilio/voice?lang=kn-IN", data={"CallSid": "CA1"})
    assert r.status_code == 200
    assert 'url="wss://ruko.example/twilio/stream"' in r.text
    assert 'name="lang" value="kn-IN"' in r.text
    assert len(telephony.TOKENS) >= 1


def test_voice_webhook_rejects_bad_signature(monkeypatch):
    monkeypatch.setenv("TWILIO_AUTH_TOKEN", "secret")
    monkeypatch.setenv("RUKO_PUBLIC_URL", "https://ruko.example")
    c = TestClient(app)
    assert c.post("/twilio/voice", data={"CallSid": "CA1"}, headers={"X-Twilio-Signature": "nope"}).status_code == 403
    sig = twilio_signature("https://ruko.example/twilio/voice", {"CallSid": "CA1"}, "secret")
    assert c.post("/twilio/voice", data={"CallSid": "CA1"}, headers={"X-Twilio-Signature": sig}).status_code == 200


def test_stream_without_valid_token_is_closed():
    c = TestClient(app)
    with c.websocket_connect("/twilio/stream") as ws:
        ws.send_json({"event": "connected"})
        ws.send_json({"event": "start", "streamSid": "MZ1", "start": {"customParameters": {"token": "forged"}}})
        msg = ws.receive()
        assert msg["type"] == "websocket.close" and msg["code"] == 1008
