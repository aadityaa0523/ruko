"""Family Shield: a family member opens /family/?c=<code> and sees the call turn red live.

The code is a random secret shared by the person being protected (like an unlisted link).
shortcut: rooms live in memory on one server, move to Redis pub/sub when running more than one instance.
"""
import asyncio
import json
import os
import re

from fastapi import APIRouter, File, Form, UploadFile, WebSocket
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend import gnani

router = APIRouter()
CODE = re.compile(r"^[a-z0-9]{8,16}$")
ROOMS: dict[str, set[WebSocket]] = {}
HISTORY: dict[str, list[dict]] = {}  # current call's events, replayed to a family member who joins late
MAX_ROOMS, MAX_EVENTS = 1000, 300
TYPES = {"call_start", "transcript", "warning", "pack", "diarized", "call_end"}
# Family member's cloned voice for the warning, recorded by them with consent. Memory only, deletable.
# shortcut: lost on restart; persist encrypted per family if this becomes a paid feature.
VOICES: dict[str, dict] = {}
# Push subscriptions per family code (Web Push). shortcut: memory only, lost on restart; store in the database when it matters.
SUBS: dict[str, list[dict]] = {}
PUSHED: set[str] = set()  # family codes already notified during the current call
MAX_SUBS = 5


def _send_push(sub: dict, payload: dict) -> bool:
    """Returns False when the browser has dropped the subscription."""
    from pywebpush import WebPushException, webpush
    try:
        webpush(sub["subscription"], json.dumps(payload), vapid_private_key=os.environ["VAPID_PRIVATE_KEY"],
                vapid_claims={"sub": "mailto:ruko-alerts@users.noreply.github.com"}, ttl=600)
        return True
    except WebPushException as e:
        return getattr(e.response, "status_code", 0) not in (404, 410)


async def notify(code: str):
    """One push per call to every family member who asked for alerts."""
    if not SUBS.get(code) or code in PUSHED or not os.environ.get("VAPID_PRIVATE_KEY"):
        return
    PUSHED.add(code)
    last = next((e for e in reversed(HISTORY.get(code, [])) if e.get("type") == "transcript"), None)
    nxt = (last or {}).get("risk", {}).get("playbook", {}).get("next") or "Ruko has warned them out loud."
    for sub in list(SUBS[code]):
        payload = {"title": f"{sub['name']} is on a scam call right now", "body": f"{nxt} Call them now.",
                   "url": f"/family/?c={code}&n={sub['name']}", "tag": f"ruko-{code}"}
        if not await asyncio.to_thread(_send_push, sub, payload):
            SUBS[code].remove(sub)


def voice_for(code: str | None) -> dict | None:
    v = VOICES.get(code or "")
    return v["embedding"] if v else None


async def publish(code: str | None, msg: dict):
    if not code or not CODE.match(code) or msg.get("type") not in TYPES:
        return
    msg = {k: v for k, v in msg.items() if k != "audio"}  # family gets text, not the warning audio
    if msg["type"] == "call_start":
        HISTORY[code] = []
        PUSHED.discard(code)
    elif code not in HISTORY and len(HISTORY) >= MAX_ROOMS:
        return
    events = HISTORY.setdefault(code, [])
    if len(events) < MAX_EVENTS:
        events.append(msg)
    for ws in list(ROOMS.get(code, ())):
        try:
            await ws.send_json(msg)
        except Exception:
            ROOMS[code].discard(ws)
    if msg["type"] == "warning":
        asyncio.create_task(notify(code))


class Event(BaseModel):
    code: str
    msg: dict


@router.post("/api/family/publish")
async def publish_http(ev: Event):
    """Used by the guard app's demo mode (no mic), so the family screen can be shown with scripted calls."""
    if len(str(ev.msg)) > 20000:
        return {"ok": False}
    await publish(ev.code, ev.msg)
    return {"ok": True}


@router.get("/api/push/key")
def push_key():
    return {"key": os.environ.get("VAPID_PUBLIC_KEY") or None}


class PushSub(BaseModel):
    c: str
    name: str = ""
    subscription: dict


@router.post("/api/push/subscribe")
def push_subscribe(body: PushSub):
    endpoint = str(body.subscription.get("endpoint", ""))
    if not CODE.match(body.c) or not endpoint.startswith("https://") or len(json.dumps(body.subscription)) > 2000:
        return JSONResponse({"error": "invalid subscription"}, status_code=400)
    subs = [s for s in SUBS.get(body.c, []) if s["subscription"].get("endpoint") != endpoint]
    subs.append({"subscription": body.subscription, "name": (body.name.strip() or "Your family member")[:30]})
    SUBS[body.c] = subs[-MAX_SUBS:]
    return {"ok": True}


@router.post("/api/family/voice")
async def add_voice(c: str = Form(...), name: str = Form(""), consent: bool = Form(False),
                    file: UploadFile = File(...)):
    """The family member records 5-30 s of their own voice; the warning is then spoken in it."""
    if not CODE.match(c) or not consent:
        return JSONResponse({"error": "A valid family link and your consent are needed."}, status_code=400)
    data = await file.read()
    if not 16000 <= len(data) <= 5 * 1024 * 1024:
        return JSONResponse({"error": "Record between 5 and 30 seconds."}, status_code=400)
    try:
        emb = await gnani.clone_voice(data, file.filename or "voice.wav")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=502)
    if c not in VOICES and len(VOICES) >= MAX_ROOMS:
        return JSONResponse({"error": "Too many voices stored right now."}, status_code=503)
    VOICES[c] = {"embedding": emb, "name": name.strip()[:30]}
    return {"ok": True}


@router.get("/api/family/voice")
def get_voice(c: str = ""):
    v = VOICES.get(c)
    return {"has_voice": bool(v), "name": v["name"] if v else ""}


@router.delete("/api/family/voice")
def delete_voice(c: str = ""):
    return {"deleted": VOICES.pop(c, None) is not None}


@router.websocket("/ws/family")
async def family(ws: WebSocket, c: str = ""):
    await ws.accept()
    if not CODE.match(c) or (c not in ROOMS and len(ROOMS) >= MAX_ROOMS):
        await ws.close(code=1008, reason="bad family code")
        return
    ROOMS.setdefault(c, set()).add(ws)
    try:
        for msg in HISTORY.get(c, []):
            await ws.send_json(msg)
        while (await ws.receive())["type"] != "websocket.disconnect":
            pass
    finally:
        ROOMS[c].discard(ws)
        if not ROOMS[c]:
            del ROOMS[c]
