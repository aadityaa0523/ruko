# Translation review sheet

**Status (10 Nov 2026):** every spoken warning has been (1) reviewed for grammar and natural phrasing by Claude (an AI, not a native speaker) and (2) checked by machine: Gnani Timbre speaks it, Gnani Prisma transcribes it back, and every word came back correctly in all 10 languages (`eval/warnings_roundtrip.json`; its similarity scores look low only because Prisma writes loanwords like "call", "bank", "OTP" in English letters). **No native speaker has signed off yet.** Each one takes about 2 minutes: read it aloud, tick the boxes, write fixes in the last column.

All warnings say the same thing: *"Stop! This call looks like a scam. Banks, police or the government never ask for an OTP or money on the phone. Hang up and call 1930."*

| Language | Warning (as spoken) | Changed in this review | Natural? | Polite enough for elders? | Reviewer, fixes |
|---|---|---|---|---|---|
| Hindi | रुकिए! यह कॉल धोखा लग रही है। बैंक, पुलिस या सरकार कभी फ़ोन पर ओ टी पी या पैसे नहीं माँगते। फ़ोन काट दीजिए, और एक नौ तीन शून्य पर कॉल कीजिए। | none | ☐ | ☐ | |
| Kannada | ನಿಲ್ಲಿ! ಇದು ವಂಚನೆಯ ಕರೆ ಅಂತ ಅನಿಸುತ್ತಿದೆ. ಬ್ಯಾಂಕ್, ಪೊಲೀಸ್ ಅಥವಾ ಸರ್ಕಾರ ಯಾವತ್ತೂ ಫೋನಿನಲ್ಲಿ ಒ ಟಿ ಪಿ ಅಥವಾ ಹಣ ಕೇಳುವುದಿಲ್ಲ. ಕರೆ ಕಟ್ ಮಾಡಿ, ಒಂದು ಒಂಬತ್ತು ಮೂರು ಸೊನ್ನೆಗೆ ಕರೆ ಮಾಡಿ. | added "ಅಂತ" (was "ವಂಚನೆ ಕರೆ ಅನಿಸುತ್ತಿದೆ"); added "ಸರ್ಕಾರ" | ☐ | ☐ | |
| Telugu | ఆగండి! ఇది మోసపు కాల్ లాగా ఉంది. బ్యాంక్, పోలీసులు లేదా ప్రభుత్వం ఎప్పుడూ ఫోన్‌లో ఓ టి పి లేదా డబ్బు అడగరు. కాల్ కట్ చేసి, ఒకటి తొమ్మిది మూడు సున్నాకి కాల్ చేయండి. | "లా" → "లాగా"; "సున్నా కి" → "సున్నాకి"; added "ప్రభుత్వం". **Check:** the voice may say "ఎప్పుడు" (when) instead of "ఎప్పుడూ" (never) | ☐ | ☐ | |
| Tamil | நிறுத்துங்கள்! இது மோசடி அழைப்பு போல் தெரிகிறது. வங்கியோ, காவல்துறையோ, அரசாங்கமோ ஒருபோதும் தொலைபேசியில் ஓ டி பி அல்லது பணம் கேட்காது. அழைப்பைத் துண்டித்து, ஒன்று ஒன்பது மூன்று பூஜ்ஜியம் என்ற எண்ணை அழையுங்கள். | "பூஜ்யம்" → "பூஜ்ஜியம்"; "எண்ணை" → "என்ற எண்ணை"; added "அரசாங்கமோ" | ☐ | ☐ | |
| Marathi | थांबा! हा कॉल फसवणुकीचा वाटतो. बँक, पोलीस किंवा सरकार कधीही फोनवर ओ टी पी किंवा पैसे मागत नाहीत. फोन कट करा, आणि एक नऊ तीन शून्य वर कॉल करा. | none | ☐ | ☐ | |
| Bengali | থামুন! এই কলটি প্রতারণা মনে হচ্ছে। ব্যাংক, পুলিশ বা সরকার কখনও ফোনে ও টি পি বা টাকা চায় না। ফোন কেটে দিন, আর এক নয় তিন শূন্যে কল করুন। | none | ☐ | ☐ | |
| Gujarati | રોકાઓ! આ કૉલ છેતરપિંડી લાગે છે. બેંક, પોલીસ કે સરકાર ક્યારેય ફોન પર ઓ ટી પી કે પૈસા માંગતી નથી. ફોન કાપી નાખો, અને એક નવ ત્રણ શૂન્ય પર કૉલ કરો. | none (Prisma heard "રોકાવો"; check which spelling is natural) | ☐ | ☐ | |
| Malayalam | നിൽക്കൂ! ഈ കോൾ തട്ടിപ്പാണെന്ന് തോന്നുന്നു. ബാങ്കോ പോലീസോ സർക്കാരോ ഒരിക്കലും ഫോണിൽ ഒ ടി പി യോ പണമോ ചോദിക്കില്ല. ഫോൺ കട്ട് ചെയ്യൂ, ഒന്ന് ഒമ്പത് മൂന്ന് പൂജ്യം എന്ന നമ്പറിൽ വിളിക്കൂ. | none | ☐ | ☐ | |

## Hindi consent form (`PILOT_KIT.md`)
Reviewed by Claude for grammar and for matching the app: the button name "इस कॉल को सुरक्षित करें" is exactly what the Hindi app shows. ☐ Native reviewer: _______

## How to get it checked fast
Send each person their row on WhatsApp with a screen recording of the sample scam call in that language (pick the language in the app, tap "Try a sample scam call") and ask: "Would your grandmother understand this immediately? Anything that sounds odd?" One reply per language is enough for the pilot.
