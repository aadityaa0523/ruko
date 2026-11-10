# Ruko family pilot kit

For a 4-week pilot with 20–50 families **after** the Gnani challenge (the challenge itself allows synthetic data only). Everything here assumes real people, so consent and privacy come first.

## 1. Who to recruit
- **Protected person:** 55+, uses a phone daily, gets calls from unknown numbers. Mix of smartphone and keypad-phone users; Hindi plus at least one southern language.
- **Family member:** the adult child or neighbour who will hold the Family Shield link.
- **Where to find them:** your own and classmates' families, a residents' welfare association, a senior-citizens' club, a local NGO. Never recruit through cold calls (that's how scammers work, and it destroys trust).

## 2. Consent (read aloud and give a copy)

**English**
> Ruko is a free test of a scam-call warning app. During this pilot:
> - Ruko listens only when you tap "Protect this call". It turns words into text to spot scams and warns you out loud. The sound of your calls is not saved.
> - If you share your family link, the person you choose can see live warnings during a protected call.
> - We keep only: the time of each warning, how far the scam got, and anything you choose to report. No call audio, no contacts, no bank details.
> - You can stop at any time and ask us to delete everything. Saying no will not affect anything else.
> - Ruko only warns. It can miss a scam or warn about a real call. Never share an OTP or send money because of a call. If money is lost, call 1930.
>
> I agree to take part: ______  Name: ______  Date: ______  Family member (optional): ______

**हिंदी**
> Ruko धोखे वाली कॉल की चेतावनी देने वाले ऐप का मुफ़्त परीक्षण है। इस दौरान:
> - Ruko सिर्फ़ तभी सुनता है जब आप "इस कॉल को सुरक्षित करें" दबाते हैं। यह शब्दों को टेक्स्ट में बदलकर धोखा पहचानता है और ज़ोर से चेतावनी देता है। कॉल की आवाज़ सेव नहीं होती।
> - अगर आप फ़ैमिली लिंक साझा करते हैं, तो आपका चुना हुआ व्यक्ति सुरक्षित कॉल के दौरान लाइव चेतावनी देख सकता है।
> - हम सिर्फ़ ये रखते हैं: हर चेतावनी का समय, धोखा कितना आगे बढ़ा, और जो आप ख़ुद रिपोर्ट करें। न कॉल की आवाज़, न कॉन्टैक्ट, न बैंक जानकारी।
> - आप कभी भी रुक सकते हैं और सब कुछ हटाने को कह सकते हैं। मना करने से और कुछ नहीं बदलेगा।
> - Ruko सिर्फ़ चेतावनी देता है। यह कोई धोखा चूक सकता है या असली कॉल पर चेतावनी दे सकता है। किसी कॉल की वजह से कभी OTP न बताएँ, पैसे न भेजें। पैसे गए तो 1930 पर कॉल करें।
>
> मैं भाग लेने को सहमत हूँ: ______  नाम: ______  तारीख़: ______  परिवार का सदस्य (वैकल्पिक): ______

*(Hindi reviewed by AI for grammar and to match the app's button text; still needs a native speaker's tick, see `TRANSLATION_REVIEW.md`.)*

## 3. Two-minute setup with each family
1. On the family member's phone: open `/account/`, create an account, **Add** the parent ("Mummy").
2. Tap **Set up their phone** → **Send on WhatsApp**.
3. On the parent's spare phone or tablet (or their own if it isn't the one taking calls): open the link → **Add to Home screen**. For a keypad phone: save the Ruko phone-line number instead (when live).
4. Family member: tap **Watch live** → **Alert me even when this page is closed**.
5. Practice once together: **Try a sample scam call**. Show the red screen and the family alert.
6. Agree the habit: *"Unknown caller talking about money, police or KYC → put it on speaker, tap Ruko."*

## 4. What to measure (weekly)
| Metric | Where it comes from | Target |
|---|---|---|
| Families still active in week 4 | Account dashboard (alerts or checks in the last 7 days) | ≥ 60% |
| Protected calls per family per week | Count of guard sessions (add a counter before the pilot) | ≥ 1 |
| Scam alerts and how many were real scams | Alert history plus the weekly check-in | Precision ≥ 80% |
| Genuine calls wrongly warned | Weekly check-in | ≤ 1 per family per month |
| Messages checked | `/api/check` count (add a counter) | Growing week on week |
| Numbers reported, numbers reaching 2+ reports | `number_reports` | Growing |
| Family alert seen within 1 minute | Weekly check-in | ≥ 70% |
| Money lost by pilot families | Weekly check-in | Zero |

## 5. Weekly 5-minute check-in (phone or WhatsApp)
1. Did Ruko warn you about a call this week? Was it really a scam? (yes / no / not sure)
2. Did Ruko warn about a genuine call? What was it?
3. Was a scam call missed? What did the caller say?
4. Did the family member see the alert? How fast?
5. Was anything confusing or hard to use?
6. One sentence we can quote (with permission).

## 6. Rules for the pilot team
- Never ask for OTPs, bank details or call recordings.
- Report any real loss to 1930 with the family, immediately.
- Store notes without phone numbers or full names; delete everything 30 days after the pilot unless the family asks to keep using Ruko.
- Publish results honestly, including misses and false alarms.
