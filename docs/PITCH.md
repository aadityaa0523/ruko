# Ruko: stop the scam, not just the number

**Live app:** https://ruko-ohn2.onrender.com · **Code:** https://github.com/aadityaa0523/ruko · Built on **Gnani Prisma** (speech recognition) and **Timbre** (voices)

## The problem
Indians lost **₹22,845 crore** to cyber fraud in 2024, **₹1,935 crore** of it to fake "digital arrest" calls (Ministry of Home Affairs, replies in Parliament). These scams happen *during* the call, in Hinglish and regional languages, from a fresh number each day. Caller-ID and telco filters judge the **number**, so a new SIM gets through. Google's on-device call scanning needs a Pixel (under 1% of Indian phones) and warns only in English.

## The insight
Scammers change numbers every day. **They never change the script:** pose as someone trusted → scare or rush → cut you off from family → ask for OTP or money. Ruko listens for that script.

## What Ruko does
1. **Listens to the call on speaker** and transcribes it live with Gnani Prisma, auto-detecting the language.
2. **Tracks the scam's four steps** and warns **before the next one** ("Next they'll ask for an OTP"). In our recorded live run, Ruko warned 0.97 s after "don't tell anyone", before money was asked for.
3. **Speaks the warning out loud** with Timbre in **10 Indian languages**, slowly for elders.
4. **Family Shield:** the family's phone turns red live, with what was said and what to do.
5. **After the call:** a ready 1930 / cybercrime.gov.in complaint with a timestamped transcript, a one-tap number report, and a ready report for DoT's Chakshu portal.
6. **Check anything:** paste or share any SMS, WhatsApp forward, link, UPI request or number for a verdict with reasons, plus a community Scam Radar.
7. **Beyond smartphones:** keypad phones merge the call with Ruko's phone line, and the warning plays inside the call. Ruko's Android app warns before you pick up, using community reports.

## Proof (synthetic data only, per challenge rules)
- **36/36** live calls judged correctly through Gnani Prisma: 7 scams + 2 genuine calls, on speakerphone and 8 kHz phone audio, with and without background voices. Median alert in **0.09 s**.
- **Message checker:** 92% precision, 72% recall on 100 held-out messages written blind to the rules and scored once.
- Full method and limits: [docs/EVALUATION.md](EVALUATION.md).

## Why Ruko wins
| | Ruko | Truecaller | Airtel | Google Pixel |
|---|---|---|---|---|
| Understands what the caller says | **Yes** | No (number) | No (patterns) | Yes |
| Live warning language | **10 Indian** | n/a | n/a | English |
| Family sees the scam live | **Yes** | Blocks calls remotely | No | No |
| Any phone, incl. keypad | **Yes** | Smartphones | Airtel SIMs | Pixel only |

## Business
Free for families. Revenue from a **risk-scoring API for banks, UPI apps and telcos** (`/v1/score`): flag a customer who is mid-scam before the transfer goes through. Next: a family pilot with consent (pilot kit ready), then a telco in-network pilot for keypad phones.
