"""Ruko backend: proxies browser mic audio to Prisma Realtime, scores the call, speaks warnings via Timbre,
and on hang-up builds the golden-hour pack (evidence, complaint, family alert, diarized timeline).

Run from the ruko/ folder:  .venv/Scripts/python -m uvicorn backend.app:app --port 8870
"""
import asyncio
import base64
import json
import time
from datetime import datetime
from pathlib import Path

import websockets
from fastapi import FastAPI, File, Form, UploadFile, WebSocket
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend import gnani
from backend.pack import build_pack, pick_caller
from backend.risk import CallRisk
from backend.scripts import SAFE, SCAM
from backend.telephony import router as telephony_router

ROOT = Path(__file__).resolve().parent.parent
gnani.load_env(ROOT / ".env")

app = FastAPI(title="Ruko")
# Public demo runs on one Gnani key: cap parallel live sessions and their length.
LIVE = asyncio.Semaphore(3)
MAX_SESSION_S = 600
app.include_router(telephony_router)


@app.get("/api/health")
def health():
    return {"gnani_key": bool(gnani.api_key()), "languages": list(gnani.LANGS)}


@app.get("/api/scripts")
def scripts():
    return {"scam": SCAM, "safe": SAFE}


class Lines(BaseModel):
    lines: list[str]
    lang: str = "hi-en"


@app.post("/api/analyze")
def analyze(body: Lines):
    """Text test mode: score a call line by line without audio, and build its pack."""
    risk = CallRisk()
    states = [risk.feed(line) for line in body.lines]
    lines = [{"t": i * 4.0, "text": t, "risk": s} for i, (t, s) in enumerate(zip(body.lines, states))]
    return {"states": states, "pack": build_pack(lines, datetime.now(), body.lang)}


@app.get("/api/warning")
async def warning(lang: str = "hi-en", whisper: int = 0):
    """Speak the warning once, to check the voice."""
    if lang not in gnani.LANGS:
        return Response(status_code=400, content="unknown lang")
    try:
        audio = await gnani.tts(gnani.LANGS[lang]["warning"], lang, bool(whisper))
    except Exception as e:  # surface Gnani errors to the UI
        return Response(status_code=502, content=str(e))
    return Response(content=audio, media_type="audio/wav")


class Speak(BaseModel):
    text: str


@app.post("/api/family-voice")
async def family_voice(body: Speak):
    """Family alert read aloud in Hinglish (Timbre v2.5, Poorvi)."""
    try:
        return Response(content=await gnani.tts(body.text[:600], "hi-en"), media_type="audio/wav")
    except Exception as e:
        return Response(status_code=502, content=str(e))


@app.post("/api/clip")
async def clip(file: UploadFile = File(...), lang: str = Form("hi-en")):
    """Check a recorded call or forwarded voice note (max 30 s) with Prisma REST."""
    if lang not in gnani.LANGS:
        return JSONResponse({"error": "unknown lang"}, status_code=400)
    data = await file.read()
    if not data or len(data) > gnani.BATCH_MAX_BYTES:
        return JSONResponse({"error": "File is empty or over 10 MB"}, status_code=400)
    try:
        body = await gnani.transcribe_clip(data, file.filename or "clip.wav", lang)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=502)
    text = body.get("transcript", "")
    state = CallRisk().feed(text)
    return {"transcript": text, "language": body.get("detected_language_code"), "risk": state,
            "truncated": bool(body.get("truncated"))}


async def send_warning(ws: WebSocket, lang: str, whisper: bool, state: dict):
    text = gnani.LANGS[lang]["warning"]
    msg = {"type": "warning", "text": text, "level": state["level"], "audio": None}
    try:
        msg["audio"] = base64.b64encode(await gnani.tts(text, lang, whisper)).decode()
    except Exception as e:
        msg["error"] = str(e)
    await _safe_send(ws, msg)


async def send_diarized(ws: WebSocket, audio: bytearray, lang: str, flagged: list[str]):
    """Prisma Batch: who said what. The audio is dropped as soon as the job is sent (or fails)."""
    try:
        wav = gnani.pcm_to_wav(bytes(audio))
        audio.clear()
        segments = await gnani.diarize(wav, lang)
        caller = pick_caller(segments, flagged)
        await _safe_send(ws, {"type": "diarized", "caller": caller, "segments": [
            {"speaker": s["speaker_id"], "start": s["start_time"], "end": s["end_time"], "text": s["text"]}
            for s in segments]})
    except Exception as e:
        await _safe_send(ws, {"type": "diarized", "error": str(e)})
    finally:
        audio.clear()


@app.websocket("/ws/listen")
async def listen(ws: WebSocket, lang: str = "hi-en", model: str = "prisma-v3.0", whisper: int = 0):
    await ws.accept()
    if lang not in gnani.LANGS or model not in ("prisma-v3.0", "prisma-v2.5"):
        await ws.close(code=1008, reason="bad lang or model")
        return
    if not gnani.api_key():
        await ws.send_json({"type": "error", "message": "GNANI_API_KEY missing in ruko/.env"})
        await ws.close()
        return
    if LIVE.locked():
        await ws.send_json({"type": "error", "message": "Ruko is busy with other calls right now. Please try again in a minute."})
        await ws.close()
        return
    async with LIVE:
        await _listen(ws, lang, model, whisper)


async def _listen(ws: WebSocket, lang: str, model: str, whisper: int):
    risk = CallRisk()
    started, t0 = datetime.now(), time.monotonic()
    audio = bytearray()  # in memory only, for diarization after hang-up
    lines: list[dict] = []
    hung_up = asyncio.Event()
    try:
        # Browsers cannot set WS headers, so the backend holds the key and proxies audio.
        async with websockets.connect(gnani.STT_WS, additional_headers=gnani.stt_headers(lang, model),
                                      max_size=None) as up:

            async def browser_to_gnani():
                while True:
                    m = await ws.receive()
                    if m["type"] == "websocket.disconnect":
                        return
                    if m.get("bytes"):
                        if len(audio) + len(m["bytes"]) <= gnani.BATCH_MAX_BYTES:  # ~5 min kept
                            audio.extend(m["bytes"])
                        await up.send(m["bytes"])  # 1,024-byte PCM16 16 kHz frames
                    elif m.get("text"):
                        if json.loads(m["text"]).get("type") == "hangup":
                            await up.send(json.dumps({"type": "commit"}))  # flush the last utterance
                            await asyncio.sleep(1.5)
                            hung_up.set()
                            return
                        await up.send(m["text"])

            async def gnani_to_browser():
                async for raw in up:
                    m = json.loads(raw)
                    kind = m.get("type")
                    if kind == "transcript" and m.get("text"):
                        state = risk.feed(m["text"])
                        lines.append({"t": round(time.monotonic() - t0, 1), "text": m["text"], "risk": state})
                        await ws.send_json({"type": "transcript", "text": m["text"],
                                            "lang": m.get("detected_language_code"), "risk": state})
                        if state["alert"]:
                            asyncio.create_task(send_warning(ws, lang, bool(whisper), state))
                    elif kind in ("connected", "speech_start", "processing", "error"):
                        await ws.send_json(m)

            tasks = [asyncio.create_task(browser_to_gnani()), asyncio.create_task(gnani_to_browser())]
            done, pending = await asyncio.wait(tasks, timeout=MAX_SESSION_S, return_when=asyncio.FIRST_COMPLETED)
            if not done:
                await _safe_send(ws, {"type": "error", "message": "Session limit of 10 minutes reached."})
            for t in pending:
                t.cancel()
            for t in done:
                if t.exception():
                    raise t.exception()
        if hung_up.is_set():
            pack = build_pack(lines, started, lang)
            await ws.send_json({"type": "pack", **pack})
            if pack["level"] in ("high", "critical") and len(audio) > 32000:
                await send_diarized(ws, audio, lang, [m["text"] for m in pack["moments"]])
            await _safe_send(ws, {"type": "done", "audio_deleted": True})
            await ws.close()
    except websockets.InvalidStatus as e:
        await _safe_send(ws, {"type": "error", "message": f"Prisma refused connection: HTTP {e.response.status_code}"})
    except websockets.ConnectionClosed as e:
        await _safe_send(ws, {"type": "error", "message": f"Prisma closed: {e.rcvd.code if e.rcvd else ''} "
                                                         f"{e.rcvd.reason if e.rcvd else ''}"})
    except Exception as e:
        await _safe_send(ws, {"type": "error", "message": str(e)})
    finally:
        audio.clear()


async def _safe_send(ws: WebSocket, msg: dict):
    try:
        await ws.send_json(msg)
    except Exception:
        pass  # browser already gone


app.mount("/", StaticFiles(directory=ROOT / "web", html=True), name="web")
