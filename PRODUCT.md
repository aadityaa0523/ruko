# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
- **Primary (design leads for them): adult children, about 25–40,** often living away from their parents. They set Ruko up for a parent, share the Family Shield link, record their voice for the warning, and are the ones who would pay. Their job: "make sure my parents don't lose money to a scam call while I'm not there."
- **Protected person: a parent or elder,** often 55+, with low digital literacy, more comfortable in Hindi or a regional language, sometimes on a keypad phone. Their job during a call: get a clear, loud "stop" at the right moment. Their screen must be one big action.
- **Secondary: banks, UPI apps, telcos and cyber cells,** who would buy the scoring API and anonymous scam-trend data.

## Product Purpose
Ruko is a scam-safety app for Indian families. It listens to a phone call (on speaker, or by joining a keypad-phone call through a number), recognises the scam playbook as it unfolds, warns out loud in the elder's language before the scammer's next move, turns the family member's phone red live, and hands over a ready 1930 complaint after the call. Success: an elder hangs up before sharing an OTP or sending money, and the family knows within seconds.

## Positioning
Other guards check the caller's *number* (Truecaller, telcos) or need a flagship phone and speak Hindi/English only (Google Pixel). Ruko understands *what the caller is saying*, in 6 Indian languages, on any phone including keypad phones, and predicts the scammer's next step from the four-step playbook (pretend → scare → isolate → ask). The family is part of the defence, not a notification afterwards.

## Operating Context
- The elder is mid-call, stressed, phone on speaker; the guard screen is read in seconds.
- The adult child is at work; the family screen is glanced at on a phone, often after a push notification.
- After a loss there is a "golden hour" to call 1930 and freeze money.
- Built for the Gnani AI Great Indian AI Internship Challenge (closes 10 Nov 2026, 11:59 PM IST); the product continues after it.

## Capabilities and Constraints
- Built and verified live: speakerphone guard (Gnani Prisma Realtime), Auto language detection (6 languages: Hinglish, Hindi, Kannada, Telugu, Tamil, English), next-step warnings, spoken warning (Gnani Timbre; elder slow mode; whisper), Family Shield live screen, consented family-voice warning (Gnani voice cloning), 1930 complaint pack + diarized timeline, voice-note check, keypad-phone line via Twilio Media Streams (simulator only, no real carrier call yet), partner scoring API, pilot waitlist.
- Stack: vanilla HTML/CSS/JS served by FastAPI (`ruko/web/`), no build step. Deployed on Render free plan (sleeps when idle).
- Ruko only warns; it never blocks or ends calls. Call audio is not stored.
- Undecided: persistent storage (Supabase), custom domain, real telephony number.

## Brand Commitments
- Name: **Ruko** ("stop" in Hindi). Because another Devpost project uses the name, pair it with a descriptor where it first appears.
- Visual style (user decision, 9 Nov 2026): a polished mainstream consumer app in the class of Truecaller and similar Indian apps (white surfaces, brand blue #1f5eff, red only for scams, Manrope + Mukta). The earlier road-sign world was rejected as "not like a real product".
- Voice: plain, calm, direct, warm; short sentences; never fear-mongering; Hinglish-friendly.

## Evidence on Hand
- Measured results in `docs/EVALUATION.md`: 36 live runs, 9 synthetic calls × 4 conditions (speaker, 8 kHz phone line, both with background chatter); every scam caught, 0 false alarms; median alert delay 0.07–0.36 s, worst 4.6 s in noise; complaint pack 2.5 s after hang-up.
- 59 automated tests. Loss figures: ₹22,845 Cr cyber fraud and ₹1,935 Cr digital-arrest losses in 2024 (government replies in Parliament).
- **Solo build.** No users, testimonials, partners, press or pilots exist yet: never imply them. All test calls are synthetic (scripted, Timbre voices). Do not claim the Samarthan shortlisting.

## Product Principles
1. The elder's screen has one job: say "stop" clearly at the right moment.
2. The family is part of the defence; isolation is what scams exploit.
3. Show proof, never claims: measured numbers and honest limits.
4. Works for the phones people actually have, including keypad phones.
5. Privacy by default: no stored audio, deletable voice, nothing shared without a link the user controls.

## Accessibility & Inclusion
- Elders: large text, high contrast, big touch targets (≥48 px), plain words, English/Hindi toggle on every screen; regional-language warnings by voice.
- WCAG 2.2 AA; works at 375 px; light and dark; reduced-motion respected; the alert is never colour-only.
