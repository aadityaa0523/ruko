# Ruko: stop the scam, not just the number

**Live:** https://ruko-ohn2.onrender.com · **Code:** https://github.com/aadityaa0523/ruko · **Built on Gnani Prisma (speech recognition) + Timbre (voices, cloning)** · Built end to end by one developer

## The problem
In 2024, Indians lost **₹22,845 crore** to cyber fraud, and **₹1,935 crore** of it to fake "digital arrest" calls, across **1.2 lakh complaints** (Ministry of Home Affairs, replies in Parliament). The people targeted are **elders at home, farmers waiting for a PM-Kisan installment, and kirana owners living on UPI**, often on basic phones. The scam happens *during* the call, in Hinglish or a regional language, from a new number every day. **Scammers change numbers, but they never change the script:** pose as police → scare → isolate ("kisi ko mat batana") → ask for OTP or money.

## What Ruko does
1. **Hears the call itself** on speakerphone. Gnani Prisma transcribes it live, including **Hindi-English code-mix mid-sentence**, and auto-detects the language.
2. **Tracks the 4-step scam script** and warns **before the next step** ("next they'll ask for your OTP"). In a recorded real run, Ruko warned **0.65 s** after "kisi ko mat batana", before money was asked for.
3. **Speaks the warning in 10 Indian languages:** Hindi, Hinglish, Kannada, Telugu, Tamil, Marathi, Bengali, Gujarati, Malayalam, English. It can speak **slowly with pauses for elders**, **whisper** so the caller hears less, or use **a family member's own cloned voice**, recorded once with consent through Gnani voice cloning.
4. **Family Shield:** the daughter's phone turns red live, showing what was said and what to do now.
5. **After the call:** a ready **1930 / cybercrime.gov.in complaint**, **who said what** (Gnani batch diarization), a one-tap number report, and a ready report for DoT's **Chakshu** portal.
6. **Every day, not just the bad day:** check any SMS, WhatsApp forward, **voice note**, link, UPI request or number. Includes a community **Scam Radar**.
7. **Any phone:** on a keypad phone, merge the call with Ruko's line and the warning plays inside the call. On Android, Ruko warns before you pick up and sits in the Share menu.

## Why Ruko beats what exists
| | **Ruko** | Truecaller | Airtel | Google Pixel |
|---|---|---|---|---|
| Understands what the caller says, live | **Yes** | No (checks the number) | No (checks call patterns) | Yes |
| Warning language | **10 Indian, incl. code-mix** | n/a | n/a | English only |
| Warns of the scammer's next move | **Yes** | No | No | No |
| Family sees the scam live | **Yes, with what was said** | Can block calls remotely | No | No |
| Works on | **Any phone, incl. keypad** | Smartphones | Airtel SIMs | Pixel (<1% of India) |
| After-call complaint, Chakshu report | **Yes** | No | No | No |

## Proof (synthetic data only)
- **36/36** live calls judged correctly through Gnani Prisma (7 scams + 2 genuine calls in 5 languages), **in background noise and on 8 kHz phone-line audio**. Median alert in **0.09 s** (quiet room), **0.36 s** with background chatter.
- **Message checker:** 92% precision and 72% recall on 100 held-out messages, written blind to the rules and scored once.
- Method and limits: [docs/EVALUATION.md](EVALUATION.md). **Demo video:** real, unedited run in the middle.

## Business
Free for the person on the call. **Family Shield ₹49/month.** **Risk-scoring API for banks, UPI apps and telcos** (`/v1/score`, live): flag a customer mid-scam *before* the transfer. Next: a consented family pilot (kit ready), then a telco in-network pilot for keypad phones.
