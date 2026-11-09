"""Phone-line mode: Ruko joins a real phone call (Twilio Media Streams, 8 kHz G.711 mu-law both ways).

Flow: the user merges a suspicious call with the Ruko number -> Twilio calls POST /twilio/voice ->
TwiML opens a bidirectional stream to /twilio/stream -> audio goes to Prisma Realtime at 8 kHz ->
on an alert, Timbre speaks *into the call* (mu-law 8 kHz): a warning for the user and a notice for the caller.
The golden-hour pack is kept in memory and shown in the web app (no screen needed on a keypad phone).
"""
import array
import asyncio
import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from datetime import datetime
from xml.sax.saxutils import quoteattr

import websockets
from fastapi import APIRouter, Request, WebSocket
from fastapi.responses import Response

from backend import family as fam
from backend import gnani
from backend.pack import build_pack
from backend.risk import CallRisk

router = APIRouter()
TOKENS: dict[str, float] = {}  # one-time stream tokens -> expiry; stops strangers burning Gnani credits
CALLS: list[dict] = []  # recent phone-line packs, newest first, memory only
FRAME = 1024  # Prisma Realtime frame: 512 samples of PCM16

# Spoken into the call. Hinglish, numbers in spoken form. Honest: Ruko prepares a report, it does not file one.
ANNOUNCE = "Suchna: is call ko Ruko suraksha sahayak sun raha hai."
CALLER_NOTICE = ("Suniye, is call ko dhokhadhadi ke roop mein pehchana gaya hai. "
                 "Iski report ek nau teen shunya cyber helpline ke liye taiyaar ki ja rahi hai.")


def _ulaw_table() -> list[int]:
    out = []
    for b in range(256):  # ITU-T G.711 mu-law decode
        u = ~b & 0xFF
        mag = (((u & 0x0F) << 3) + 0x84) << ((u >> 4) & 0x07)
        out.append(0x84 - mag if u & 0x80 else mag - 0x84)
    return out


ULAW = _ulaw_table()


def ulaw_to_pcm16(data: bytes) -> bytes:
    pcm = array.array("h", (ULAW[b] for b in data))
    if sys.byteorder == "big":
        pcm.byteswap()
    return pcm.tobytes()


def twilio_signature(url: str, params: dict, auth_token: str) -> str:
    """Twilio request signature: HMAC-SHA1 over the full URL + sorted POST params, base64."""
    data = url + "".join(k + str(params[k]) for k in sorted(params))
    return base64.b64encode(hmac.new(auth_token.encode(), data.encode(), hashlib.sha1).digest()).decode()


def public_base(request: Request) -> str:
    """URL Twilio used to reach us (behind ngrok/Render the local URL differs)."""
    if os.environ.get("RUKO_PUBLIC_URL"):
        return os.environ["RUKO_PUBLIC_URL"].rstrip("/")
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    return f"{proto}://{request.headers.get('host', request.url.netloc)}"


@router.post("/twilio/voice")
async def voice(request: Request, lang: str = "hi-en", family: str = ""):
    form = {k: v for k, v in (await request.form()).items()}
    base = public_base(request)
    auth = os.environ.get("TWILIO_AUTH_TOKEN")
    if auth:  # trust boundary: only Twilio may start a session
        url = f"{base}{request.url.path}" + (f"?{request.url.query}" if request.url.query else "")
        if not hmac.compare_digest(twilio_signature(url, form, auth), request.headers.get("x-twilio-signature", "")):
            return Response(status_code=403)
    if not gnani.valid_lang(lang):
        lang = "hi-en"
    family = family if fam.CODE.match(family) else ""
    now = time.time()
    for t, exp in list(TOKENS.items()):
        if exp < now:
            del TOKENS[t]
    token = secrets.token_urlsafe(16)
    TOKENS[token] = now + 120
    ws_url = base.replace("https://", "wss://").replace("http://", "ws://") + "/twilio/stream"
    xml = ('<?xml version="1.0" encoding="UTF-8"?><Response><Connect>'
           f'<Stream url={quoteattr(ws_url)}><Parameter name="token" value={quoteattr(token)}/>'
           f'<Parameter name="lang" value={quoteattr(lang)}/>'
           f'<Parameter name="family" value={quoteattr(family)}/></Stream></Connect></Response>')
    return Response(content=xml, media_type="application/xml")


@router.get("/api/calls")
def calls():
    return CALLS


@router.websocket("/twilio/stream")
async def stream(ws: WebSocket):
    await ws.accept()
    start = None
    async for raw in ws.iter_text():  # Twilio sends "connected", then "start"
        m = json.loads(raw)
        if m.get("event") == "start":
            start = m
            break
    if not start:
        return
    params = start["start"].get("customParameters", {})
    if TOKENS.pop(params.get("token", ""), 0) < time.time() or not gnani.api_key():
        await ws.close(code=1008)
        return
    sid = start["streamSid"]
    lang = params.get("lang") if gnani.valid_lang(params.get("lang", "")) else "hi-en"
    code = params.get("family") or None  # Family Shield link of the subscriber this number belongs to
    heard = {"lang": None}
    await fam.publish(code, {"type": "call_start", "source": "phone", "at": datetime.now().isoformat(timespec="seconds")})
    risk, lines, buf = CallRisk(), [], bytearray()
    started, t0 = datetime.now(), time.monotonic()
    say_lock = asyncio.Lock()

    async def say(text: str, in_lang: str):
        """Timbre mu-law 8 kHz straight into the call; one message at a time."""
        async with say_lock:
            try:
                audio = await gnani.tts(text, in_lang, telephony=True)
            except Exception as e:
                print("Timbre failed:", e)
                return
            for i in range(0, len(audio), 8000):  # 1 s per message; Twilio queues and plays in order
                await ws.send_json({"event": "media", "streamSid": sid,
                                    "media": {"payload": base64.b64encode(audio[i:i + 8000]).decode()}})
            await ws.send_json({"event": "mark", "streamSid": sid, "mark": {"name": f"said-{len(audio)}"}})

    try:
        async with websockets.connect(gnani.STT_WS, max_size=None,
                                      additional_headers=gnani.stt_headers(lang, "prisma-v3.0", rate=8000)) as up:
            asyncio.create_task(say(ANNOUNCE, "hi-en"))

            async def twilio_to_gnani():
                async for raw in ws.iter_text():
                    m = json.loads(raw)
                    ev = m.get("event")
                    if ev == "media" and m["media"].get("track", "inbound") == "inbound":
                        buf.extend(ulaw_to_pcm16(base64.b64decode(m["media"]["payload"])))
                        while len(buf) >= FRAME:
                            await up.send(bytes(buf[:FRAME]))
                            del buf[:FRAME]
                    elif ev == "stop":
                        await up.send(json.dumps({"type": "commit"}))  # flush the last utterance
                        await asyncio.sleep(1.5)
                        return

            async def gnani_to_twilio():
                async for raw in up:
                    m = json.loads(raw)
                    if m.get("type") == "transcript" and m.get("text"):
                        heard["lang"] = m.get("detected_language_code") or heard["lang"]
                        state = risk.feed(m["text"])
                        lines.append({"t": round(time.monotonic() - t0, 1), "text": m["text"], "risk": state})
                        await fam.publish(code, {"type": "transcript", "text": m["text"], "risk": state})
                        if state["alert"]:
                            spoken = gnani.speak_lang(lang, heard["lang"])
                            asyncio.create_task(say(gnani.LANGS[spoken]["warning"], spoken))
                            await fam.publish(code, {"type": "warning", "level": state["level"]})
                            if sum(l["risk"]["alert"] for l in lines) == 1:  # caller notice only once
                                asyncio.create_task(say(CALLER_NOTICE, "hi-en"))
                    elif m.get("type") == "error":
                        print("Prisma error:", m.get("message"))

            tasks = [asyncio.create_task(twilio_to_gnani()), asyncio.create_task(gnani_to_twilio())]
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for t in tasks:
                t.cancel()
    except Exception as e:
        print("Phone-line session ended with error:", e)
    finally:
        pack = build_pack(lines, started, gnani.speak_lang(lang, heard["lang"]))
        pack.update(source="phone", call_sid=start["start"].get("callSid"))
        CALLS.insert(0, pack)
        del CALLS[20:]
        await fam.publish(code, {"type": "pack", **pack})
        await fam.publish(code, {"type": "call_end"})
