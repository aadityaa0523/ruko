"""Does each spoken warning come out clearly? Timbre speaks it, Prisma transcribes it back, we compare.

Not a substitute for a native speaker, but it catches text the voice can't pronounce or that comes out garbled.
Run from ruko/:  .venv/Scripts/python -m eval.warnings_roundtrip   (uses Gnani credits)
"""
import asyncio
import difflib
import json
import re

from backend import gnani
from eval.channels import ROOT

gnani.load_env(ROOT / ".env")


def norm(t: str) -> str:
    return re.sub(r"[^\wऀ-ൿ]+", "", t.lower())


async def main():
    out = []
    for lang, cfg in gnani.LANGS.items():
        audio = await gnani.tts(cfg["warning"], lang)
        body = await gnani.transcribe_clip(audio, "warning.wav", lang)
        heard = body.get("transcript") or body.get("text") or json.dumps(body, ensure_ascii=False)[:400]
        sim = round(difflib.SequenceMatcher(None, norm(cfg["warning"]), norm(heard)).ratio(), 2)
        out.append({"lang": lang, "similarity": sim, "said": cfg["warning"], "heard": heard})
        print(f"{lang}: {sim}\n  said:  {cfg['warning']}\n  heard: {heard}", flush=True)
    (ROOT / "eval" / "warnings_roundtrip.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())
