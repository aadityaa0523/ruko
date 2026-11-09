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

## Pages

- `/`: landing page (problem, how it works, Family Shield, business, pricing, pilot waitlist, live demo of the scoring).
- `/app/`: the guard. One tap to protect a call, live captions, the scam-step tracker, red alert, golden-hour pack, sample calls, voice-note check.
- `/family/?c=<code>&n=<name>`: Family Shield. Turns red live when the protected person's call becomes a scam. The link is made in the app (Family Shield button).
- `/check/`: check any SMS, WhatsApp message, link, UPI request or number (`POST /api/check`, rules only, nothing stored); community number lookup and reports (Supabase `number_reports`, `number_lookup` RPC); Scam Radar (`scam_radar` RPC). Installed on Android, Ruko appears in the Share menu (Web Share Target) and opens here.
- `/account/`: family account (Supabase Auth, email + password). Add the people you protect, send each one a setup link (`/app/?f=<code>&n=<name>`), watch them live, see the alert history, delete your data.
- `/privacy/`, `/terms/`, `/licenses/`, `/contact/`: trust pages; contact and pilot forms write to Supabase `leads`.
- `POST /v1/score` (header `X-Ruko-Key`): partner API returning `level`, `score`, `flags` and `playbook` for transcript lines. Keys come from `RUKO_PARTNER_KEYS`; the key `demo` works for up to 20 lines.
- `POST/GET/DELETE /api/family/voice`: a family member's consented voice clip (5–30 s) becomes a Gnani voice embedding; warnings are then spoken in that voice. Memory only; deletable.
- `POST /api/waitlist`: pilot sign-ups, appended to `data/waitlist.jsonl` (git-ignored; local disk only).

## How it works

1. The browser captures mic audio (16 kHz PCM16, 1,024-byte frames) and sends it to the backend's `/ws/listen`.
2. The backend proxies the audio to **Prisma Realtime**. It holds the API key, because browsers can't set WebSocket headers. On v3.0 it uses code-mix output, Indian-language + English hints and scam keyterms.
3. Each transcript goes through `backend/risk.py`, which scores the **pattern** across the whole call: claims to be an official + threat + secrecy + payment/OTP + remote app + refund trick. An alert needs at least two categories including a dangerous one, and genuine bank safety advice is ignored.
3b. With the language set to **Auto**, Prisma runs with `indic-auto` and Ruko speaks the warning in the detected language (Hindi is answered in Hinglish; languages without a warning yet fall back to Hinglish).
4. `risk.py` also maps the flags to the scam's four-step playbook (pose → fear → isolate → ask) and picks a warning about the next step.
5. On an alert, **Timbre v2.5** speaks the warning in the chosen language, or **Timbre v3.0** `<whispers>` it if that option is ticked. The mic pauses while Ruko speaks, so it doesn't transcribe itself.

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
3. Set the number's "A call comes in" webhook to `POST https://<public-url>/twilio/voice?lang=auto` (or a fixed language such as `kn-IN`). Add `&family=<code>` (the code from a Family Shield link) to make the family screen turn red during phone-line calls too.
4. Put the account's auth token in `TWILIO_AUTH_TOKEN`, so only Twilio-signed requests can start a session. Each stream also needs a one-time token that the webhook issues.

Without a Twilio account, you can exercise the same code with a simulator that speaks Twilio's message format. That is how this mode has been tested so far. No real phone call has been made yet.

## Data (Supabase, Mumbai)

Tables `leads`, `families`, `alerts`, all with row-level security: anyone can submit a lead or log an alert for an existing family code; only the owner can read their families and alerts; leads are readable only from the Supabase dashboard. The browser uses the public publishable key in `web/config.js`. Alerts store time, level, steps reached and source only (no audio, words or numbers).

Auth settings to set in the Supabase dashboard: Site URL = the deployed URL; add `<url>/account/` to Redirect URLs; either turn off "Confirm email" or add your own SMTP (the built-in sender only delivers to your own team).

## Licence

© 2026 Ruko. All rights reserved. See `LICENSE` and `/licenses/`.

## Family push alerts

The family screen can buzz a family member's phone even when the page is closed (Web Push, one notification per scam call). Generate a VAPID key pair once (see `pywebpush`/`py_vapid`), then set `VAPID_PUBLIC_KEY` and `VAPID_PRIVATE_KEY` in `.env` locally and in Render. Without them the alert button stays hidden.
