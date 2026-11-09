"""Synthetic call scripts (challenge rule: no real calls, names, numbers or accounts).

Each scam script must trigger an alert; each safe script must not. Used by the
tests, by the UI's text test mode, and as lines to act out for the demo video.
"""

SCAM = {
    "digital_arrest": [
        "Main CBI officer Vikram bol raha hoon.",
        "Aapke naam pe ek parcel mila hai jisme drugs hain, aapke khilaf warrant nikla hai.",
        "Aap digital arrest mein hain. Ye baat kisi ko mat batana, call mat kaatna.",
        "Verification ke liye apna paisa safe account mein transfer kariye.",
    ],
    "pm_kisan_kyc": [
        "Namaskar, main PM Kisan yojana daftar se bol raha hoon.",
        "Aapki agli kist ruk gayi hai kyunki KYC pending hai.",
        "Abhi ke abhi aapke phone pe ek OTP aayega, wo bata dijiye warna kist band ho jayegi.",
    ],
    "army_kirana_order": [
        "Bhaiya main army camp se bol raha hoon, pachaas kilo chawal chahiye.",
        "Payment UPI se karunga, aap ye QR code scan karo, paise aapke account mein aa jayenge.",
        "Jaldi karo, gaadi nikal rahi hai.",
    ],
    "fake_upi_refund": [
        "Sir maine galti se aapko paanch hazaar rupaye bhej diye.",
        "Please wapas bhej do, main collect request bhej raha hoon, bas UPI PIN daal do.",
    ],
    "electricity_cut": [
        "Main bijli vibhag se bol raha hoon, aapka pichhla bill update nahi hua.",
        "Aaj raat nau baje aapki bijli kat jayegi.",
        "Turant AnyDesk app download karo, main update kar deta hoon.",
    ],
    "ayushman_card": [
        "Aapka Ayushman card band ho jayega.",
        "Renewal ke liye chaar sau ninyanve rupaye ka payment kariye, link pe click karke.",
        "Aaj hi last date hai.",
    ],
    "relative_in_custody": [
        "Aunty aapka beta police station mein hai, accident ho gaya hai.",
        "Case band karne ke liye pachaas hazaar bhejiye.",
        "Ghar walon ko mat batana warna case badh jayega.",
    ],
    "bank_kyc_screenshare": [
        "Hello, SBI head office se bol rahe hain.",
        "Aapka account block ho jayega kyunki KYC expire hai.",
        "Play Store se TeamViewer QuickSupport install karo aur screen share on karo.",
    ],
    "police_kannada": [
        "ನಾನು ಪೊಲೀಸ್ ಅಧಿಕಾರಿ. ನಿಮ್ಮ ಮೇಲೆ ಕೇಸ್ ಆಗಿದೆ.",
        "ಯಾರಿಗೂ ಹೇಳಬೇಡಿ. ತಕ್ಷಣ ನಿಮ್ಮ ಒಟಿಪಿ ಹೇಳಿ.",
    ],
    "bank_telugu": [
        "నేను బ్యాంక్ నుంచి మాట్లాడుతున్నాను. మీ ఖాతా బ్లాక్ అవుతుంది.",
        "వెంటనే మీ ఓటీపీ చెప్పండి. ఎవరికీ చెప్పకండి.",
    ],
    "police_tamil": [
        "நான் போலீஸ் அதிகாரி பேசுகிறேன். உங்கள் மீது வழக்கு பதிவாகியுள்ளது, உங்களை கைது செய்வோம்.",
        "இதை யாரிடமும் சொல்லாதீர்கள். உடனே உங்கள் ஓடிபி சொல்லுங்கள்.",
    ],
    "cyber_branch_english": [
        "This is Inspector Sharma from the Mumbai cyber crime branch. A parcel in your name has drugs.",
        "There is an arrest warrant against you. Do not tell anyone about this call.",
        "Transfer your savings to the RBI safe account immediately for verification.",
    ],
    "police_marathi": [
        "मी पोलीस अधिकारी बोलतोय. तुमच्या नावावर केस दाखल झाली आहे, तुम्हाला अटक होईल.",
        "हे कोणालाही सांगू नका. लगेच तुमचा ओटीपी सांगा.",
    ],
    "bank_bengali": [
        "আমি ব্যাংক থেকে বলছি। আপনার অ্যাকাউন্ট ব্লক হয়ে যাবে।",
        "এখনই আপনার ওটিপি বলুন। কাউকে বলবেন না।",
    ],
    "police_gujarati": [
        "હું પોલીસ અધિકારી બોલું છું. તમારા પર કેસ દાખલ થયો છે, તમારી ધરપકડ થશે.",
        "આ વાત કોઈને કહેશો નહીં. તરત તમારો ઓટીપી કહો.",
    ],
    "bank_malayalam": [
        "ഞാൻ ബാങ്കിൽ നിന്നാണ് വിളിക്കുന്നത്. നിങ്ങളുടെ അക്കൗണ്ട് ബ്ലോക്ക് ആകും.",
        "ഉടനെ നിങ്ങളുടെ ഒടിപി പറയൂ. ആരോടും പറയരുത്.",
    ],
    "cbi_devanagari": [
        "मैं सीबीआई से बोल रहा हूँ, आपके खिलाफ वारंट है।",
        "किसी को मत बताना, तुरंत पैसे भेजिए।",
    ],
}

SAFE = {
    "marathi_family": ["आई, मी आज लवकर घरी येईन.", "रात्री आपण एकत्र जेवू."],
    "bengali_family": ["মা, আমি আজ সন্ধ্যায় বাড়ি ফিরব।", "রাতে একসঙ্গে খাব।"],
    "card_bill_english": [
        "Hello, this is your bank. Your credit card bill is due on the fifth.",
        "Please remember, never share your OTP with anyone.",
    ],
    "tamil_family": [
        "அம்மா, நான் இன்று சீக்கிரம் வீட்டுக்கு வருவேன்.",
        "இரவு சாப்பாடு சேர்ந்து சாப்பிடலாம்.",
    ],
    "real_bank_reminder": [
        "Namaste, main SBI branch se bol rahi hoon.",
        "Aapka home loan EMI paanch tarikh ko due hai.",
        "Yaad rakhiye, bank kabhi bhi OTP nahi maangta, OTP kisi ko na batayein.",
    ],
    "delivery_otp": [
        "Amazon delivery hai, main aapke ghar ke bahar hoon.",
        "Delivery OTP bata dijiye please.",
    ],
    "doctor_appointment": [
        "Doctor sahab ka appointment kal subah das baje hai.",
        "Thoda jaldi aaiyega, line lambi hoti hai.",
    ],
    "family_surprise": [
        "Beta bol raha hoon, aaj ghar jaldi aaunga.",
        "Mummy ko mat batana, surprise party hai.",
    ],
}
