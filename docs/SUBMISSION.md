# Ruko: submission text

Paste each section into the matching field of the Great Indian AI Internship Challenge form. Fill in the bracketed parts yourself.

## Project title
Ruko: the phone call that answers back. A live scam-call guard for any phone, in Indian languages

## Problem
Indians lost ₹22,845 crore to cyber fraud in 2024, ₹1,935 crore of it to "digital arrest" voice calls (government replies in Parliament). These scams happen while the call is going on, in Hinglish and regional languages, from new numbers every day.

Existing protection doesn't reach the people being targeted:
- Number-based spam flags miss a fresh number.
- On-device AI scam detection runs only on a few flagship phones.
- India still has an estimated 250–350 million keypad-phone users.

After a scam, victims also lose the "golden hour" to freeze money, because they can't clearly retell the call to the 1930 helpline.

## Target users
Elders living alone, farmers, kirana shop owners and first-time digital users, who are targeted by PM-Kisan KYC, army-officer order, fake UPI refund, electricity cut-off, Ayushman card and digital-arrest calls. Also their families, who get the alert.

## What Ruko does
1. **Listens to a call on speaker** (web app, any device) and transcribes it live with Gnani Prisma.
2. **Tracks the scam's playbook.** Every phone scam runs the same four steps: pretend to be someone trusted → scare or rush → cut you off from family → ask for OTP, money or your phone. Ruko shows which step the call has reached and **warns about the next step before it comes** ("Next they will ask for an OTP. Never do it on a call"; "Real police never arrest anyone on a video call"). Scammers change numbers daily, but not this script.
3. **Scores the whole call for scam patterns**, not single keywords. Signs: claims to be an official, threat, secrecy, OTP/PIN/money request, remote-access app or link, and the "sent by mistake" refund trick. An alert needs at least two signs including a dangerous one, so genuine bank reminders and delivery OTPs don't trigger it.
4. **Full-screen red alert + spoken warning in the user's language** with Gnani Timbre: Hinglish, Hindi, Kannada, Telugu, Tamil or English. A Timbre v3.0 whispered option exists so the caller is less likely to hear it.
5. **Family Shield.** The protected person shares one link. When a call turns into a scam, the family member's phone turns red with live captions, the scam steps and what to do ("call her now: a second call breaks the scammer's hold"). Scams depend on isolation; this brings the family in.
6. **Golden-hour pack on hang-up:**
   - a 1930 / cybercrime.gov.in complaint built only from what was said, with timestamps;
   - a "Call 1930 now" button;
   - a family alert as text and voice;
   - a Caller/You timeline from Prisma Batch diarization.
   Call audio is deleted after the voices are separated.
7. **Check anything, every day:** paste or share (Android Share menu) any SMS, WhatsApp forward, link, UPI collect request or number. Ruko gives a verdict with reasons in seconds (lookalike bank domains, APK files, link shorteners, "call our officer" numbers, refund tricks), predicts the scammer's next step, and makes a one-tap WhatsApp warning for the family.
   **Community number reports and Scam Radar:** anyone can report a scam number anonymously; anyone can look a number up; a live radar shows this week's scams by type.
7. **Voice-note check:** upload a suspicious WhatsApp voice note or recording (up to 30 s).
8. **Partner API** (`POST /v1/score`): banks, UPI apps and telcos send transcript lines and get the level, flags and playbook back, e.g. to hold a large transfer while the customer is mid-scam.
9. **Phone-line mode for keypad phones:** merge the call with Ruko's number. Ruko hears the 8 kHz phone audio and speaks the warning *into the call*, plus a one-time notice to the caller.

## Gnani AI models and APIs used
- **Prisma v3.0, Realtime WebSocket:** live transcription, `codemix` format, scam `keyterms`, `topic`, at 16 kHz (speakerphone) and 8 kHz (phone line).
- **Prisma v3.0 `indic-auto`:** the default "Auto" mode detects the caller's language (`detected_language_code`), and Ruko answers in that language. Tested live with Kannada, Hindi and Telugu calls.
- **Prisma v2.5, Realtime:** selectable fallback.
- **Prisma v3.0, REST:** voice-note check.
- **Prisma v3.0, Batch with diarization:** who said what after the call.
- **Timbre v2.5:** warnings in 6 languages (voices Poorvi, Nalini, Saanvi, Suhana, Asmita, Kaveri), the family alert, and 8 kHz `pcm_mulaw` audio spoken into phone calls.
- **Timbre SSE streaming:** phone-line warnings start playing as the first chunk arrives (measured 0.7 s to first audio vs about 2.0 s for the full clip over REST). Warnings are also made in advance at call start, so the speakerphone alert plays instantly.
- **Voice cloning (`vachana-vc-v1`):** on the Family Shield screen, a family member records 5–30 s of their own voice, with an explicit consent checkbox, and can delete it any time. Warnings, including the ones spoken into a phone call, then come in that trusted voice. The voice embedding is kept in memory only.
- **Timbre v3.0:** `<whispers>` audio tag for a quiet warning, and an elder mode that uses `<slow>` on every sentence with `<pauses>` between them.

## How it was tested
- **55 automated tests** run 11 synthetic scam scripts and 4 safe scripts, in Hinglish, Devanagari, Kannada, Telugu, Tamil and English. They also include **real Prisma transcripts**, mistakes included, from synthetic calls spoken by Timbre. Every scam alerts and no safe call does.
- **End to end against the live Gnani APIs:** speech → Prisma → risk → spoken warning, plus diarization of a two-voice call.
- **Phone-line mode** was tested with a simulator that speaks Twilio's media-stream format with real 8 kHz audio. A real carrier call has not been made yet.

## Award fit (evidence for each category)
A team can win only one award; these are the categories Ruko competes in, with proof.
- **Solo Ninja:** built end to end by one person: speech pipeline, risk engine, telephony, accounts, design, evaluation, video.
- **Noise Canceller:** measured on 8 kHz G.711 phone audio with background chatter at +5 dB SNR: 7/7 scams caught, 0/2 false alarms, median alert 0.35 s after the trigger line (36 live runs, `docs/EVALUATION.md`). Phone-line mode runs Prisma at 8 kHz and speaks Timbre μ-law back into the call.
- **Mixed Vibes:** Prisma v3.0 code-mix output (Devanagari and Latin in one sentence) is matched with mixed-script phrases ("block हो", "link पे click"); warnings are spoken in Hinglish; Auto mode detects the caller's language mid-call.
- **Main Character:** full detection and spoken warnings in Kannada, Telugu and Tamil, tested live, with a slow, paused elder voice.
- **Real Deal:** protects the groups scammers target most: farmers (PM-Kisan "installment stopped"), kirana owners (fake army orders, "sent by mistake" UPI refunds) and elders on keypad phones; ends with a ready 1930 complaint inside the golden hour.
- **Jugaad Genius:** merge a keypad-phone call with Ruko's number so the AI speaks *inside* the call; the warning comes in a family member's cloned voice (with consent); Ruko sits in Android's Share menu; it predicts the scammer's next step from a four-step playbook.
- **Demo Day Drop:** 44-second vertical video recorded from the real product (`docs/ruko-demo.mp4`).

## Business model
B2B2C, like a credit-card fraud shield:
- **Free** for the person on the call: speakerphone guard, spoken warning, 1930 pack.
- **Family Shield, ₹49/month per family:** live family alert screen and keypad-phone line mode. Children of elderly parents are the buyers.
- **Business, priced per protected call:** scoring API and in-call warnings for banks/UPI apps (fewer frauds and disputes), telcos (a value-added service for keypad-phone users) and insurers. Cyber cells get structured complaints.

The landing page (`/`) has a live pilot waitlist for families and partners.

## Honest limitations
- In speakerphone mode the user must start Ruko. The design answer is a simple habit ("unknown caller talking about money or police: open Ruko") plus family-triggered use.
- Phone-line mode still needs a telephony number (Twilio/Exotel). It has only been tested with a simulator so far.
- A careful scammer could avoid the trigger phrases. Scoring the whole call's pattern raises the bar but doesn't remove the risk.
- Ruko only warns. It never blocks or ends a call, and it isn't a replacement for 1930.

## Safety and data
- Only synthetic data was used: scripts I wrote, voices generated by Timbre or recorded with consent, and fake names and numbers.
- No call audio is stored.
- The complaint is template-based, so it never invents facts.

## Team and contributions
Solo build: product, backend, Gnani integration, risk engine, telephony, design, evaluation and video by [your name].

## Links
- Live product: https://ruko-ohn2.onrender.com (check a message: /check/, call guard: /app/, family account: /account/)
- Code: https://github.com/aadityaa0523/ruko
- Video: docs/ruko-demo.mp4 in the repo (also attached to the posts)
- Nominated posts: [LinkedIn URL] · [X URL]
