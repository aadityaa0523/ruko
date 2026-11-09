"""Family Shield: a family member opens /family/?c=<code> and sees the call turn red live.

The code is a random secret shared by the person being protected (like an unlisted link).
shortcut: rooms live in memory on one server, move to Redis pub/sub when running more than one instance.
"""
import re

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel

router = APIRouter()
CODE = re.compile(r"^[a-z0-9]{8,16}$")
ROOMS: dict[str, set[WebSocket]] = {}
HISTORY: dict[str, list[dict]] = {}  # current call's events, replayed to a family member who joins late
MAX_ROOMS, MAX_EVENTS = 1000, 300
TYPES = {"call_start", "transcript", "warning", "pack", "diarized", "call_end"}


async def publish(code: str | None, msg: dict):
    if not code or not CODE.match(code) or msg.get("type") not in TYPES:
        return
    msg = {k: v for k, v in msg.items() if k != "audio"}  # family gets text, not the warning audio
    if msg["type"] == "call_start":
        HISTORY[code] = []
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
