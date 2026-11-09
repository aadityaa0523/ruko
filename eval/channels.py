"""Speakerphone vs phone line vs noise: does Ruko still catch the scam, and how fast?

For each synthetic script, Timbre speaks it once. The same audio is then sent to Prisma Realtime under
four conditions, in real time:
  speaker   16 kHz clean (speakerphone mode)
  phone     8 kHz G.711 mu-law (phone-line mode)
  speaker+noise / phone+noise   the same with background chatter (another voice) mixed in at +5 dB SNR

Metrics per run:
  alert_ok      scam alerted / safe call stayed quiet
  flags         scam categories found in Prisma's transcript vs in the script text
  latency_s     from the end of the line that should trigger the alert to the alert (wall clock)

Run from ruko/:  .venv/Scripts/python -m eval.channels  (needs GNANI_API_KEY in .env; uses Gnani credits)
"""
import array
import asyncio
import json
import math
import sys
import time
from pathlib import Path

import httpx
import websockets

from backend import gnani
from backend.risk import CallRisk
from backend.scripts import SAFE, SCAM
from backend.telephony import ulaw_to_pcm16

ROOT = Path(__file__).resolve().parent.parent
gnani.load_env(ROOT / ".env")
CASES = [("digital_arrest", "hi-en"), ("pm_kisan_kyc", "hi-en"), ("fake_upi_refund", "hi-en"),
         ("police_kannada", "kn-IN"), ("bank_telugu", "te-IN"), ("police_tamil", "ta-IN"),
         ("cyber_branch_english", "en-IN"), ("real_bank_reminder", "hi-en"), ("delivery_otp", "hi-en")]
BABBLE = ("Aaj ka mausam saaf rahega, shaam ko halki baarish ho sakti hai. Cricket match mein India ne "
          "teen sau run banaye. Sabzi mandi mein tamatar ke daam gir gaye hain. Agle hafte school khulenge.")


async def speak(text: str, lang: str, voice: str | None = None) -> bytes:
    """Timbre v2.5 as raw 16 kHz PCM16."""
    cfg = gnani.LANGS[lang]
    body = {"text": text, "voice": voice or cfg["voice"], "model": "timbre-v2.5", "language": cfg["tts"],
            "speed": 1.0, "audio_config": {"sample_rate": 16000, "num_channels": 1, "sample_width": 2,
                                           "encoding": "linear_pcm", "container": "raw"}}
    async with httpx.AsyncClient(timeout=60) as c:
        r = await gnani._retry(lambda: c.post(gnani.TTS_URL, json=body, headers={"X-API-Key-ID": gnani.api_key()}))
    r.raise_for_status()
    return r.content


def rms(a: array.array) -> float:
    return math.sqrt(sum(x * x for x in a) / max(1, len(a))) or 1.0


def mix(speech: bytes, noise: bytes, snr_db: float) -> bytes:
    s, n = array.array("h", speech), array.array("h", noise)
    gain = rms(s) / (rms(n) * 10 ** (snr_db / 20))
    out = array.array("h", (max(-32768, min(32767, int(x + n[i % len(n)] * gain))) for i, x in enumerate(s)))
    return out.tobytes()


def to_phone(pcm16k: bytes) -> bytes:
    """16 kHz -> 8 kHz (pair averaging as a crude low-pass) -> mu-law -> back to PCM16, like a phone line."""
    a = array.array("h", pcm16k)
    down = array.array("h", ((a[i] + a[i + 1]) // 2 for i in range(0, len(a) - 1, 2)))
    return ulaw_to_pcm16(gnani.pcm16_to_ulaw(down.tobytes()))


async def run(audio: bytes, rate: int, lang: str, line_ends: list[float], expect_line: int | None) -> dict:
    """Stream in real time; return alert, flags and latency."""
    risk, flags, alert_at = CallRisk(), set(), None
    frame, step = 1024, 1024 / (rate * 2)
    done_sending = asyncio.Event()
    async with websockets.connect(gnani.STT_WS, additional_headers=gnani.stt_headers(lang, "prisma-v3.0", rate),
                                  max_size=None) as up:
        t0 = time.perf_counter()

        async def send():
            for i in range(0, len(audio), frame):
                await up.send(audio[i:i + frame].ljust(frame, b"\0"))
                await asyncio.sleep(max(0, t0 + (i // frame + 1) * step - time.perf_counter()))
            await up.send(b"\0" * frame * int(1.5 / step))  # trailing silence closes the last utterance
            await up.send(json.dumps({"type": "commit"}))
            done_sending.set()

        async def recv():
            nonlocal alert_at
            async for raw in up:
                m = json.loads(raw)
                if m.get("type") == "transcript" and m.get("text"):
                    st = risk.feed(m["text"])
                    flags.update(f["category"] for f in st["flags"])
                    if st["alert"] and alert_at is None:
                        alert_at = time.perf_counter() - t0

        rt = asyncio.create_task(recv())
        await send()
        try:
            await asyncio.wait_for(rt, timeout=6)
        except asyncio.TimeoutError:
            rt.cancel()
    latency = None
    if alert_at is not None and expect_line is not None:
        latency = round(alert_at - line_ends[expect_line], 2)
    return {"alerted": alert_at is not None, "flags": sorted(flags), "latency_s": latency}


async def main():
    noise = await speak(BABBLE, "hi-IN", voice="Deepak")
    results = []
    for name, lang in CASES:
        lines = SCAM.get(name) or SAFE[name]
        is_scam = name in SCAM
        audio, ends = b"", []
        for line in lines:
            audio += await speak(line, lang) + b"\0" * 16000  # 0.5 s gap
            ends.append(len(audio) / 32000)
        truth = CallRisk()
        states = [truth.feed(t) for t in lines]
        expect = next((i for i, s in enumerate(states) if s["alert"]), None)
        truth_flags = sorted(f["category"] for f in states[-1]["flags"])
        noisy = mix(audio, noise, 5)
        for cond, pcm, rate in [("speaker", audio, 16000), ("phone", to_phone(audio), 8000),
                                ("speaker+noise", noisy, 16000), ("phone+noise", to_phone(noisy), 8000)]:
            r = await run(pcm, rate, lang, ends, expect)
            r.update(script=name, lang=lang, condition=cond, scam=is_scam, alert_ok=r["alerted"] == is_scam,
                     truth_flags=truth_flags,
                     flag_recall=round(len(set(r["flags"]) & set(truth_flags)) / len(truth_flags), 2) if truth_flags else None)
            results.append(r)
            print(f"{name:22} {cond:14} alert_ok={r['alert_ok']!s:5} latency={r['latency_s']} "
                  f"flags={r['flags']} / {truth_flags}", flush=True)
    out = ROOT / "eval" / "channels_results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("saved", out)


if __name__ == "__main__":
    if not gnani.api_key():
        sys.exit("GNANI_API_KEY missing")
    asyncio.run(main())
