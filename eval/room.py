"""Real-room speakerphone test: the call goes through the air, not through a file.

Each synthetic call is turned into narrowband phone audio (8 kHz mu-law, like a phone on speaker),
played out loud through this computer's speaker, recorded by its microphone, and the recording is
streamed in real time to Gnani Prisma exactly like the Call Guard does. Real room echo, speaker
distortion and microphone noise suppression are all in the loop.

Run from ruko/:  .venv/Scripts/python -m eval.room   (needs `pip install sounddevice numpy`, speakers on, quiet-ish room)

Needs a microphone that does NOT cancel its own speaker. On a laptop with built-in echo cancellation
(tested: Intel Smart Sound, 10 Nov 2026) the recording comes out garbled (0/7 scams caught), because the
mic removes the laptop's own playback. That is a test-setup failure, not a real-use result: play the
calls from a second device instead (the WAVs this repo can write to eval/room_calls/).
"""
import array
import asyncio
import json
import time

import numpy as np
import sounddevice as sd

from backend.risk import CallRisk
from backend.scripts import SAFE, SCAM
from eval.channels import CASES, ROOT, rms, run, speak, to_phone

RATE = 16000


def narrowband(pcm16k: bytes) -> bytes:
    """Phone-line audio (8 kHz mu-law) brought back to 16 kHz, as a phone speaker would play it."""
    a = array.array("h", to_phone(pcm16k))
    return array.array("h", (x for x in a for _ in (0, 1))).tobytes()


def through_the_air(pcm: bytes) -> bytes:
    rec = sd.playrec(np.frombuffer(pcm, dtype="int16"), samplerate=RATE, channels=1, dtype="int16", blocking=True)
    return rec.reshape(-1).tobytes()


async def main():
    results = []
    for name, lang in CASES:
        lines = SCAM.get(name) or SAFE[name]
        is_scam = name in SCAM
        audio, ends = b"", []
        for line in lines:
            audio += await speak(line, lang) + b"\0" * 16000
            ends.append(len(audio) / 32000)
        truth = CallRisk()
        states = [truth.feed(t) for t in lines]
        expect = next((i for i, s in enumerate(states) if s["alert"]), None)
        t = time.perf_counter()
        recorded = through_the_air(narrowband(audio) + b"\0" * 32000)
        level = round(rms(array.array("h", recorded)))
        r = await run(recorded, RATE, lang, ends, expect)
        r.update(script=name, lang=lang, condition="room", scam=is_scam, alert_ok=r["alerted"] == is_scam,
                 mic_rms=level, seconds=round(time.perf_counter() - t, 1))
        results.append(r)
        print(f"{name:22} alert_ok={r['alert_ok']!s:5} latency={r['latency_s']} mic_rms={level} flags={r['flags']}", flush=True)
    out = ROOT / "eval" / "room_results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = sum(r["alert_ok"] for r in results)
    print(f"correct {ok}/{len(results)}; saved {out}")


if __name__ == "__main__":
    asyncio.run(main())
