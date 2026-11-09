# Ruko on Android: what's possible, and the plan

## The hard limit
**A normal Android app cannot hear a phone call.** Since Android 10 (2019), capturing call audio needs `CAPTURE_AUDIO_OUTPUT`, a permission reserved for system apps and phone makers. Google Play also stopped allowing apps to use the Accessibility API to record calls (policy effective May 2022). Caller-ID apps, Truecaller included, cannot hear calls either; they use Android's call-screening API, which sees only the **number**.

So "Ruko listens to every call automatically" can only happen in three ways:
1. **Built into the phone** (an OEM partnership), the way Google's own scam detection works on Pixel.
2. **In the network** (a telco partnership): the call audio is analysed in the operator's network. This is also the only way to reach keypad phones at scale.
3. **Next to the call:** the speakerphone listens through the microphone of another device, or the user merges the call with Ruko's number (what Ruko does today).

## What a Play Store Ruko app can do
| Capability | Android feature | Status |
|---|---|---|
| Install from Play Store, home-screen app, share target | Trusted Web Activity wrapping the current web app (PWABuilder) | Ready to package (see `PLAY_STORE.md`) |
| Screen incoming calls by number: label "Reported 12× as fake police" before you answer | `CallScreeningService` + `ROLE_CALL_SCREENING`, fed by Ruko's community number reports | Built: `android/` (debug APK builds; not yet tested on a phone) |
| Check SMS automatically | Users can share SMS to Ruko today (the native app is also a share target). Reading the SMS inbox needs `READ_SMS`, which Play only allows for default-SMS apps, so keep it share-based | Done (share target) |
| Listen on speakerphone on a second device | Microphone (same as the web app) | Done |
| Push alerts to family | Web Push today, Firebase Cloud Messaging in a native build | Done (web push) |
| On-device speech recognition for privacy | An on-device Indic speech model; Gnani Prisma is cloud-based | Research: would trade accuracy for privacy |

## Roadmap
1. **Now:** publish the web app to Play Store as a Trusted Web Activity (zero rewrite).
2. **Built, needs device testing:** a native `CallScreeningService` app (Java, `android/`) that looks up the incoming number in Ruko's community reports and shows a warning label before the user picks up. This is the Truecaller-style "who is calling", powered by Ruko's "what they said" reports.
3. **Then:** telco pilot for the in-network keypad-phone line (the real scale path), and an OEM conversation for built-in, on-device listening.

## What to tell judges
Ruko doesn't pretend to do what Android forbids. It warns from *next to* the call today, screens numbers natively next, and its real scale path, like Google's, runs through phone makers and telcos.

## The native app (`android/`)
- **Caller warnings:** after you make Ruko your call-screening app, every incoming call from a number that isn't in your contacts is looked up in Ruko's community reports. If two or more people reported it, a warning appears while it rings: who reported it as what, and "Don't share an OTP". Unknown numbers get a quiet reminder to put the call on speaker and tap Ruko. Ruko never blocks or rejects a call.
- **Share target:** share any SMS or WhatsApp message to Ruko and it opens the checker with the text filled in.
- **Privacy:** no contacts, SMS or call-log permission. Only the incoming number is sent to the lookup.
- **Build:** `cd android && ./gradlew assembleDebug` (JDK 17+, Android SDK 36) → `app/build/outputs/apk/debug/app-debug.apk`.
- **Not done yet:** testing on a real phone (no device or emulator image was available when it was built), a release signing key, and Play Store listing review of the call-screening role.
