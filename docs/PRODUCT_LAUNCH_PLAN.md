# Ruko: launch as a product (9–10 Nov 2026)

**Hard limit:** the Gnani challenge closes on **10 Nov, 11:59 PM IST**, and the post must be live before we submit. Everything below fits inside that limit, and the product stays live after it.

## 1. What Ruko is, as a product

> **Ruko is a scam-safety app for Indian families.** It guards phone calls as they happen, checks anything suspicious you receive, alerts your family the moment something goes wrong, and walks you through recovery if money is lost. It works in 6 Indian languages, and on keypad phones too.

**Who uses it**
- **Parents and elders** (the protected person): one big button, their own language, big text.
- **Their children** (the paying user): set it up, get alerted, record their voice for the warning.
- **Banks, telcos and cyber cells** (the business customer): scoring API, and anonymous scam-trend data.

**Why it can become big**
- Every protected call adds anonymous data about which scam script was used, in which language, and when. That builds a live **Scam Radar** that no single bank or telco has.
- This data is the moat and the B2B product. Truecaller won on number data; Ruko wins on *what scammers say*.

## 2. Product map (what a user can do)

| # | Feature | Real-life use | Status | Built when |
|---|---|---|---|---|
| 1 | **Call Guard**: listen on speaker, warn before the next scam step, red alert, spoken warning | Elder gets a "CBI officer" call | Built | — |
| 2 | **Keypad-phone line**: merge the call with Ruko's number; Ruko warns inside the call | Elder with a ₹1,000 phone | Built (simulator) | Real number needs your Twilio/Exotel account |
| 3 | **Family Shield**: live red screen and captions on the child's phone | Son at work sees Mummy's call turn red | Built | — |
| 4 | **Family push alerts**: notification even when the family page is closed | Son's phone buzzes in his pocket | New | Night |
| 5 | **Warning in a family member's voice** (consented clone) | Mummy hears her son say "ruko" | Built | — |
| 6 | **Check anything**: paste an SMS or WhatsApp text, a link or a UPI request, or upload a voice note; get a verdict and the scam step | "Your electricity will be cut tonight, click…" SMS | Partly built (voice note only) | Morning |
| 7 | **Report & Recover**: step-by-step after a loss. Call 1930, a ready complaint, a bank-freeze message, Chakshu (Sanchar Saathi) report, cybercrime.gov.in steps, golden-hour timer | Money already sent | Partly built (complaint) | Morning |
| 8 | **Scam Drill**: family schedules a practice scam call (Timbre voice); the elder practises saying no; score and tips | Train parents before the real call | New | Afternoon |
| 9 | **Scam Radar** (public page): live, anonymous counts of caught scams by type, language and hour, plus "top 5 scams this week" | Public awareness; press and police interest | New | Afternoon |
| 10 | **Scam library**: listen to how each scam sounds, in your language, with the red flags marked | Elders learn by ear | New, uses the existing 15 scripts | Afternoon |
| 11 | **Your language everywhere**: interface in English and Hindi (plus Kannada, Telugu, Tamil where time allows); big-text mode | Elders can't read English menus | New | Night |
| 12 | **Installable app (PWA)**: add to home screen, opens like an app, app icon | Feels like a real app, no Play Store wait | New | Night |
| 13 | **For business**: API docs page, key request form, pilot form | Bank or telco evaluation | API built; page new | Afternoon |
| 14 | **Trust pages**: privacy policy, data use, consent, delete-my-data | Needed for any real launch | New | Afternoon |

**Not doing (stated openly):**
- Native Android app: Play Store review takes days.
- Evon LLM: no hosted API, it needs a GPU.
- Blocking calls: Ruko only warns.
- Real scam recordings: the challenge rules forbid them.

## 3. Architecture changes for a real product

- **Persistent data:** Supabase (Postgres) for waitlist, Scam Radar events (anonymous: scam type, language, level, hour; no text, no audio, no numbers), drill results and push subscriptions. Voice embeddings stay in memory only, deletable. Today all of this is in memory or a local file, which Render's free plan loses on restart.
- **Web Push:** VAPID keys and the `pywebpush` library, for family alerts with the page closed.
- **i18n:** one strings file per language; UI text moves out of the HTML.
- **PWA:** `manifest.json`, a service worker for the app shell, icons.
- **Domain:** the Render URL for the challenge. A custom domain (e.g. `rukoapp.in`) later, if you buy one.

## 4. Timeline

### Tonight, 9 Nov (now to about 2 AM)
1. Commit today's work and push it to GitHub. **You** run `gh repo create` (one command).
2. Landing page rebuild: one sentence, the audible two-phone scene (you hear the scam, the son's voice says "ruko", his phone turns red), the measured proof, then features as product sections (Guard · Check · Family · Recover · Drill · Radar).
3. PWA install, plus Hindi and English interface and big-text mode.
4. Family push alerts.
5. Deploy on Render. **You** click Blueprint and paste the key, about 5 minutes.

### 10 Nov morning (8 AM to 12 PM)
6. **Check anything** (texts, links, UPI requests, voice notes).
7. **Report & Recover** flow.
8. **You** record the 60-second video. I'll prepare the exact script and on-screen steps tonight.
9. **Post on LinkedIn and X by 12 PM.** Engagement decides the shortlist, so every hour counts.

### 10 Nov afternoon (12 to 7 PM)
10. Scam Drill, Scam Library, Scam Radar.
11. For-business page, privacy and terms pages.
12. Supabase persistence, if you approve a project.

### 10 Nov evening (7 to 10 PM)
13. Full test pass: unit tests, a live eval rerun, phone-width check, dark mode.
14. Update README, `EVALUATION.md` and the submission text with the final feature list and links.
15. **Submit by 10 PM**, leaving 2 hours of buffer.

The site keeps improving after the post goes live; the link stays the same.

## 5. What only you can do

| When | What | Time |
|---|---|---|
| Tonight | Run the `gh repo create` command; deploy on Render | 10 min |
| Tonight | Say yes or no to a Supabase project (free) for real data | 1 min |
| Optional | Twilio account plus a number, for a real keypad-phone call (trial is free; may be a US number) | 20 min |
| Morning | Record the 60-second video (script provided) | 1 h |
| By 12 PM | Publish the LinkedIn and X posts; ask friends and family to share genuinely | 30 min |
| Evening | Fill and submit the form; decide "I" or "we" and the team names | 30 min |

## 6. Risks

| Risk | Plan |
|---|---|
| Too many features, some half-done | Each feature ships only when it works end to end; anything unfinished at 7 PM is hidden, not shown broken |
| Render free plan sleeps | Open the site once before recording and before submitting |
| Gnani credits run out | Warnings are cached; drills and the library use pre-made audio |
| Engagement is low because the post goes out late | Post at noon with whatever is live; the video shows the core features, which are already built |
