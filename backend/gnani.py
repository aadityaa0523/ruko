"""Thin client for Gnani Vachana: Prisma STT (realtime WS) and Timbre TTS (REST)."""
import os
import re
from pathlib import Path

import httpx

STT_WS = "wss://api.vachana.ai/stt/v3/stream"
TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"

# Scam vocabulary Prisma v3.0 should recognise reliably (keyterms, max 200).
KEYTERMS = [
    "OTP", "KYC", "CBI", "RBI", "UPI", "UPI PIN", "CVV", "AnyDesk", "TeamViewer", "QuickSupport",
    "PM Kisan", "Ayushman", "digital arrest", "warrant", "FIR", "QR code", "screen share",
    "customs", "narcotics", "cyber cell", "crime branch", "safe account", "1930",
]

# UI language -> Prisma language, Timbre v2.5 language/voice, spoken warning (numbers in spoken form).
LANGS = {
    "hi-en": {"stt": "hi-IN", "tts": "hi-en", "voice": "Poorvi", "v3": "hi-IN",
              "warning": "Ruko! Yeh call dhokha lag rahi hai. Bank, police ya sarkar kabhi phone par O T P "
                         "ya paise nahi maangte. Phone kaat dijiye, aur ek nau teen shunya par call kijiye."},
    "hi-IN": {"stt": "hi-IN", "tts": "hi-IN", "voice": "Nalini", "v3": "hi-IN",
              "warning": "रुकिए! यह कॉल धोखा लग रही है। बैंक, पुलिस या सरकार कभी फ़ोन पर ओ टी पी या पैसे नहीं "
                         "माँगते। फ़ोन काट दीजिए, और एक नौ तीन शून्य पर कॉल कीजिए।"},
    "kn-IN": {"stt": "kn-IN", "tts": "kn-IN", "voice": "Saanvi", "v3": "kn-IN",
              "warning": "ನಿಲ್ಲಿ! ಇದು ವಂಚನೆ ಕರೆ ಅನಿಸುತ್ತಿದೆ. ಬ್ಯಾಂಕ್ ಅಥವಾ ಪೊಲೀಸ್ ಯಾವತ್ತೂ ಫೋನಿನಲ್ಲಿ ಒ ಟಿ ಪಿ ಅಥವಾ ಹಣ "
                         "ಕೇಳುವುದಿಲ್ಲ. ಕರೆ ಕಟ್ ಮಾಡಿ, ಒಂದು ಒಂಬತ್ತು ಮೂರು ಸೊನ್ನೆಗೆ ಕರೆ ಮಾಡಿ."},
    "te-IN": {"stt": "te-IN", "tts": "te-IN", "voice": "Suhana", "v3": "te-IN",
              "warning": "ఆగండి! ఇది మోసపు కాల్ లా ఉంది. బ్యాంక్ లేదా పోలీసులు ఎప్పుడూ ఫోన్‌లో ఓ టి పి లేదా డబ్బు "
                         "అడగరు. కాల్ కట్ చేసి, ఒకటి తొమ్మిది మూడు సున్నా కి కాల్ చేయండి."},
    "ta-IN": {"stt": "ta-IN", "tts": "ta-IN", "voice": "Asmita", "v3": "ta-IN",
              "warning": "நிறுத்துங்கள்! இது மோசடி அழைப்பு போல் தெரிகிறது. வங்கியோ காவல்துறையோ ஒருபோதும் "
                         "தொலைபேசியில் ஓ டி பி அல்லது பணம் கேட்காது. அழைப்பைத் துண்டித்து, ஒன்று ஒன்பது மூன்று "
                         "பூஜ்யம் எண்ணை அழையுங்கள்."},
    "en-IN": {"stt": "en-IN", "tts": "en-IN", "voice": "Kaveri", "v3": "en-IN",
              "warning": "Stop! This call looks like a scam. Banks, police and the government never ask for an "
                         "O T P or money on the phone. Hang up, and call one nine three zero."},
}


# "auto": Prisma identifies the language (indic-auto) and Ruko warns in the language it heard.
AUTO = "auto"
DETECTED = {"hi-IN": "hi-en", "kn-IN": "kn-IN", "te-IN": "te-IN", "ta-IN": "ta-IN", "en-IN": "en-IN"}


def valid_lang(lang: str) -> bool:
    return lang == AUTO or lang in LANGS


def speak_lang(lang: str, detected: str | None = None) -> str:
    """Concrete warning language. Auto falls back to Hinglish for languages Ruko has no warning in yet."""
    return lang if lang != AUTO else DETECTED.get(detected or "", "hi-en")


def stt_code(lang: str) -> str:
    return "indic-auto" if lang == AUTO else LANGS[lang]["stt"]


def load_env(path: Path) -> None:
    """Minimal .env loader so the key never has to be typed into code or chat."""
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"'))


def api_key() -> str:
    return os.environ.get("GNANI_API_KEY", "")


def stt_headers(lang: str, model: str, rate: int = 16000) -> dict:
    h = {"x-api-key-id": api_key(), "model": model, "x-sample-rate": str(rate)}
    if model == "prisma-v3.0":
        # One locale or indic-auto; codemix keeps the English words that callers mix in.
        h["language_code"] = stt_code(lang)
        h["format"] = "codemix"
        h["keyterms"] = ",".join(KEYTERMS)
        h["topic"] = "Phone call that may be a bank, police or government impersonation scam"
    else:
        h["language_code"] = stt_code(lang)
        h["format"] = "verbatim"
    return h


STT_REST = "https://api.vachana.ai/stt/v3"
BATCH = "https://api.vachana.ai/stt/v3/batch/jobs"
BATCH_MAX_BYTES = 10 * 1024 * 1024  # direct-upload limit per file


def pcm_to_wav(pcm: bytes, rate: int = 16000) -> bytes:
    import io
    import wave
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm)
    return buf.getvalue()


async def transcribe_clip(data: bytes, filename: str, lang: str) -> dict:
    """Prisma REST (<=30 s clip), e.g. a forwarded WhatsApp voice note."""
    form = {"model": "prisma-v3.0", "language_code": stt_code(lang), "format": "codemix",
            "keyterms": ",".join(KEYTERMS)}
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(STT_REST, data=form, files={"audio_file": (filename, data)},
                              headers={"X-API-Key-ID": api_key()})
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code != 200 or not body.get("success", False):
        err = body.get("error", {}).get("message") if isinstance(body.get("error"), dict) else None
        raise RuntimeError(f"Prisma {r.status_code}: {err or r.text[:300]}")
    return body


async def _retry(call, tries: int = 6):
    """Docs: retry 429/5xx with exponential backoff (some accounts allow one active request at a time)."""
    import asyncio
    for i in range(tries):
        r = await call()
        if r.status_code not in (429, 500, 503, 504) or i == tries - 1:
            return r
        await asyncio.sleep(2 ** i)


async def diarize(wav: bytes, lang: str, max_wait_s: int = 240) -> list[dict]:
    """Prisma Batch with diarization: who said what. Returns segments with speaker_id, start_time, end_time."""
    import asyncio
    import json as _json
    h = {"X-API-Key-ID": api_key()}
    config = {"model": "prisma-v3.0", "language_code": LANGS[lang]["stt"], "format": "codemix",
              "with_diarization": True, "num_speakers": 2}
    async with httpx.AsyncClient(timeout=60) as c:
        files = {"config": (None, _json.dumps(config), "application/json"), "files": ("call.wav", wav, "audio/wav")}
        r = await _retry(lambda: c.post(BATCH, headers=h, files=files))
        if r.status_code != 201:
            raise RuntimeError(f"Batch create {r.status_code}: {r.text[:300]}")
        job = r.json()["job_id"]
        r = await _retry(lambda: c.post(f"{BATCH}/{job}/start", headers=h))
        if r.status_code != 202:
            raise RuntimeError(f"Batch start {r.status_code}: {r.text[:300]}")
        for _ in range(max_wait_s // 10):
            await asyncio.sleep(10)  # docs: poll no faster than every 10 s
            status = (await _retry(lambda: c.get(f"{BATCH}/{job}", headers=h))).json().get("status")
            if status in ("COMPLETED", "PARTIAL_FAILURE", "FAILED", "START_FAILED", "CANCELLED"):
                break
        else:
            raise RuntimeError("Batch diarization timed out")
        if status not in ("COMPLETED", "PARTIAL_FAILURE"):
            raise RuntimeError(f"Batch job {status}")
        r = await _retry(lambda: c.get(f"{BATCH}/{job}/files", headers=h, params={"status": "COMPLETED"}))
        if r.status_code != 200:
            raise RuntimeError(f"Batch files {r.status_code}: {r.text[:300]}")
        files = r.json()["data"]
        if not files:
            raise RuntimeError("Batch returned no completed file")
        doc = (await c.get(files[0]["transcript_url"], follow_redirects=True)).json()
    return [s for s in doc.get("segments", []) if s.get("text")]


def elder_text(text: str) -> str:
    """Timbre v3.0 tags for elders: every sentence drawn out (<slow>), a short silence (<pauses>) between them.
    A tag lasts until the next tag, so <slow> is repeated after each pause."""
    parts = [p.strip() for p in re.split(r"(?<=[.!?।])\s+", text) if p.strip()]
    return " <pauses> ".join(f"<slow> {p}" for p in parts)


async def tts(text: str, lang: str, whisper: bool = False, telephony: bool = False, elder: bool = False) -> bytes:
    """Speak text with Timbre. v2.5 by default (named in the challenge); v3.0 for <whispers> or elder mode.
    telephony=True returns raw 8 kHz G.711 mu-law, the format phone lines carry."""
    cfg = LANGS[lang]
    if whisper:
        body = {"text": f"<whispers> {text}", "voice": "Shivani", "model": "timbre-v3.0", "language": cfg["v3"]}
    elif elder:
        body = {"text": elder_text(text), "voice": "Shivani", "model": "timbre-v3.0", "language": cfg["v3"]}
    else:
        body = {"text": text, "voice": cfg["voice"], "model": "timbre-v2.5", "language": cfg["tts"]}
    body["speed"] = 0.85  # slowest allowed, for elders (API rejects the documented "slow" string)
    if telephony:
        body["audio_config"] = {"sample_rate": 8000, "num_channels": 1, "sample_width": 1,
                                "encoding": "pcm_mulaw", "container": "raw"}
    else:
        body["audio_config"] = {"sample_rate": 24000, "num_channels": 1, "sample_width": 2,
                                "encoding": "linear_pcm", "container": "wav"}
    key = (text, lang, whisper, telephony, elder)
    if key in _TTS_CACHE:  # warnings repeat: save credits and ~1 s of delay
        return _TTS_CACHE[key]
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(TTS_URL, json=body, headers={"X-API-Key-ID": api_key()})
    if r.status_code != 200:
        raise RuntimeError(f"Timbre {r.status_code}: {r.text[:300]}")
    if len(_TTS_CACHE) >= 64:
        _TTS_CACHE.pop(next(iter(_TTS_CACHE)))
    _TTS_CACHE[key] = r.content
    return r.content


_TTS_CACHE: dict[tuple, bytes] = {}
