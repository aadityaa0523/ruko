# Ruko

Ruko listens to a phone call on speaker, warns you out loud in your own language if the call sounds like a scam, and prepares the 1930 complaint. It's built on Gnani AI's Prisma (speech to text) and Timbre (text to speech) for the Great Indian AI Internship Challenge.

## Run

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
copy .env.example .env      # then put your key from app.gnani.ai/voice in .env
.venv/Scripts/python -m uvicorn backend.app:app --port 8870
```

Open http://localhost:8870. The browser only lets a page use the microphone on localhost or over HTTPS.

## How it works

1. The browser captures mic audio (16 kHz PCM16, 1,024-byte frames) and sends it to the backend's `/ws/listen`.
2. The backend proxies the audio to **Prisma Realtime**. It holds the API key, because browsers can't set WebSocket headers. On v3.0 it uses code-mix output, Indian-language + English hints and scam keyterms.
3. Each transcript goes through `backend/risk.py`, which scores the **pattern** across the whole call: claims to be an official + threat + secrecy + payment/OTP + remote app + refund trick. An alert needs at least two categories including a dangerous one, and genuine bank safety advice is ignored.
4. On an alert, **Timbre v2.5** speaks the warning in the chosen language, or **Timbre v3.0** `<whispers>` it if that option is ticked. The mic pauses while Ruko speaks, so it doesn't transcribe itself.

## Test

```bash
.venv/Scripts/python -m pytest -q
```

There are 11 synthetic scam scripts (Hinglish, Devanagari, Kannada, Telugu) and 4 safe ones in `backend/scripts.py`. Every scam must alert and no safe call may. All data is synthetic, as the challenge rules require.

## Phone-line mode (keypad phones)

Ruko can join a real phone call. The user merges a suspicious call with the Ruko number (the phone's "add call" / conference). Twilio streams the 8 kHz μ-law call audio to `/twilio/stream`, and Prisma Realtime transcribes it at 8 kHz. On an alert, Timbre speaks into the call in phone audio format (`pcm_mulaw`, 8 kHz): first a warning to the user in their language, then a one-time notice to the caller. The report shows up under "Phone-line calls" in the web app.

Setup:
1. Make the server reachable over HTTPS (deploy it, or run `ngrok http 8870`) and set `RUKO_PUBLIC_URL` to that URL.
2. In Twilio, buy a number. Indian numbers need Twilio's regulatory documents; for a quick test, a non-Indian number works.
3. Set the number's "A call comes in" webhook to `POST https://<public-url>/twilio/voice?lang=kn-IN` (any language from the list).
4. Put the account's auth token in `TWILIO_AUTH_TOKEN`, so only Twilio-signed requests can start a session. Each stream also needs a one-time token that the webhook issues.

Without a Twilio account, you can exercise the same code with a simulator that speaks Twilio's message format. That is how this mode has been tested so far. No real phone call has been made yet.
