# Ruko: measured results

All calls are synthetic: scripts we wrote, spoken by Gnani Timbre voices, sent in real time to Gnani Prisma Realtime (v3.0, code-mix). Measured on 9 Nov 2026. Reproduce with `.venv/Scripts/python -m eval.channels` (raw numbers in `eval/channels_results.json`).

## Speakerphone vs phone line vs noise

9 calls (7 scams in Hinglish, Kannada, Telugu, Tamil and English; 2 genuine calls: a bank EMI reminder and a delivery OTP), each under 4 conditions:

- **speaker:** 16 kHz clean audio, like the web app on speakerphone.
- **phone:** 8 kHz G.711 μ-law, like the phone-line mode.
- **+ noise:** another voice talking in the background (a TV or a room) at +5 dB SNR.

| Condition | Correct verdicts | Scams caught | False alarms | Median delay | Worst delay | Scam signs found |
|---|---|---|---|---|---|---|
| Speaker | 9/9 | 7/7 | 0/2 | 0.09 s | 0.19 s | 100% |
| Phone line | 9/9 | 7/7 | 0/2 | 0.07 s | 0.14 s | 100% |
| Speaker + noise | 9/9 | 7/7 | 0/2 | 0.36 s | 4.60 s | 97% |
| Phone line + noise | 9/9 | 7/7 | 0/2 | 0.35 s | 4.52 s | 94% |

**Delay** is measured from the end of the sentence that should trigger the alert to the moment Ruko raises it. **Scam signs found** compares the scam categories found in Prisma's transcript with those in the script text.

What we learned:
- **The narrow, compressed phone line did not cost accuracy.** Gnani Prisma at 8 kHz was as good as 16 kHz on these calls.
- **Background chatter is the real risk.** In 2 of 14 noisy scam runs the alert came about 4.5 s late, because the chatter kept Prisma from hearing where one sentence ended. In 2 runs one sign (secrecy) was missed, but the call was still caught. On the genuine bank call, noise produced one false "OTP" sign, but no alert, because Ruko needs two signs including a dangerous one.

## Speed of each step

| Step | Time |
|---|---|
| Phone-line warning, first audio (Timbre SSE streaming) | 0.7 s (vs about 2.0 s for the whole clip over REST) |
| Speakerphone warning | instant: it is made at call start, before any alert |
| Complaint pack after hang-up | 2.5 s |
| "Who said what" (Prisma Batch diarization) after hang-up | 15.8 s |
| Family member's voice clone from a 12 s clip | 1.4 s |

## Languages tested live

Hinglish, Hindi, Kannada, Telugu, Tamil and English. Each language had a scam call and (except Kannada and Telugu) a normal call. With the language set to **Auto**, Prisma identified each call's language and Ruko warned in that language.

## Not tested yet

- A real phone on speaker in a real room. The browser pane used for testing blocks the microphone.
- A real carrier call through Twilio or Exotel. Only a simulator speaking Twilio's protocol was used.
- Real scam recordings. The challenge allows synthetic data only.
- A native speaker reviewing the Kannada, Telugu and Tamil warning text.
