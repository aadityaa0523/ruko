# Publishing Ruko to the Play Store (and App Store)

Ruko is an installable web app (PWA): manifest, icons, service worker, share target and store screenshots are in place, and it runs over HTTPS at https://ruko-ohn2.onrender.com. Google supports packaging a PWA as a real Play Store app (a Trusted Web Activity), so no rewrite is needed.

## Play Store (about 1 hour of your time, plus Google's review)
1. **Developer account:** create one at https://play.google.com/console (one-time US$25; identity verification can take a few days).
2. **Package the app:** open https://www.pwabuilder.com, enter `https://ruko-ohn2.onrender.com/app/`, choose **Android → Google Play**. Package ID: e.g. `in.ruko.app`. Download the ZIP. It contains the `.aab` to upload and a signing key: back the key up; you need it for every update.
3. **Verify the domain:** the ZIP includes `assetlinks.json`. Copy it to `web/.well-known/assetlinks.json` in this repo, push, and redeploy. It must load at `https://ruko-ohn2.onrender.com/.well-known/assetlinks.json`. (Without it, the app shows a browser address bar.)
4. **Store listing:** use the screenshots in `web/store/` (1080×1920), the 512×512 icon `web/icon-512.png`, the description from `web/manifest.webmanifest`, and the privacy policy URL `https://ruko-ohn2.onrender.com/privacy/`.
5. **Data safety form:** declare microphone audio (processed by Gnani AI for transcription, not stored), email (account), phone numbers (only when the user reports one). Matches `/privacy/`.
6. **Release:** start with an internal or closed test (Google requires a closed test with testers before production for new personal accounts).

## App Store (iPhone)
Apple doesn't accept a plain web wrapper as easily. Options: PWABuilder's iOS package or Capacitor. Both need a Mac with Xcode and an Apple Developer account (US$99/year). Until then, iPhone users can use **Share → Add to Home Screen** in Safari.

## Before a real launch
- A custom domain (e.g. `ruko.app`) instead of `onrender.com`, and a paid Render instance so calls never hit a cold start.
- A native reviewer will ask why microphone access is needed: "to hear the call on speaker and warn you about scams; audio is not stored".
