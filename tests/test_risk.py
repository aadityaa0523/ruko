import pytest

from backend.risk import CallRisk, find_flags
from backend.scripts import SAFE, SCAM


def run(lines):
    risk = CallRisk()
    states = [risk.feed(line) for line in lines]
    return states


@pytest.mark.parametrize("name", SCAM)
def test_every_scam_script_alerts(name):
    states = run(SCAM[name])
    assert any(s["alert"] for s in states), (name, states[-1])
    assert states[-1]["level"] in ("high", "critical")


@pytest.mark.parametrize("name", SAFE)
def test_no_safe_script_alerts(name):
    states = run(SAFE[name])
    assert not any(s["alert"] for s in states), (name, states[-1])


def test_alert_fires_once_per_stage():
    states = run(SCAM["digital_arrest"])
    assert sum(s["alert"] for s in states) <= 2


def test_bank_safety_advice_is_not_a_flag():
    cats = {c for c, _ in find_flags("bank kabhi bhi OTP nahi maangta, OTP kisi ko na batayein")}
    assert not cats & {"payment", "secrecy"}


def test_ruko_own_warning_does_not_retrigger():
    from backend.gnani import LANGS
    assert not any(c in ("payment", "secrecy") for c, _ in find_flags(LANGS["hi-en"]["warning"]))


# Real Prisma v3.0 codemix transcripts (9 Nov 2026) of the synthetic scripts spoken by Timbre,
# including its recognition errors ("बाँटा", "bond", "बेली विभाग", "मेरे को").
PRISMA_SCAM = {
    "pm_kisan_kyc": ["नमस्कार, मैं PM Kisan योजना दफ़्तर से बोल रहा हूँ।",
                     "आपकी अगली किस्त रुक गई है क्योंकि KYC pending है।",
                     "अभी के अभी आपके phone पे एक OTP आएगा, वो बाँटा दीजिए वरना किस्त bond हो जाएगी।"],
    "army_kirana_order": ["भैया, मैं army camp से बोल रहा हूँ। पचास किलो चावल चाहिए।",
                          "payment UPI से करूँगा। आप ये QR code scan करो, पैसे आपके account में आ जाएंगे।",
                          "जल्दी करो, गाड़ी निकाल रही है।"],
    "fake_upi_refund": ["सर, मैंने गलती से आपको पाँच हज़ार रुपये भेज दिए।",
                        "Please वापस भेज दो। मैं collect request भेज रहा हूँ, बस UPI pin डाल दो।"],
    "electricity_cut": ["मैं बेली विभाग से बोल रहा हूँ, आपका पिछला बिल अपडेट नहीं हुआ।",
                        "आज रात नौ बजे आपकी बिजली कट जाएगी।",
                        "तुरंत AnyDesk app download करो, मैं update कर देता हूँ।"],
    "ayushman_card": ["आपका Ayushman card band हो जाएगा।",
                      "renewal के लिए चार सौ निन्यानवे रुपये का payment करिए, link पे click करके।",
                      "आज ही last date है।"],
    "relative_in_custody": ["आंटी, आपका बेटा police station में है, accident हो गया है।",
                            "case ban करने के लिए पचास हज़ार भेजिए।",
                            "कहा, मेरे को मत बताना वरना case बढ़ जाएगा।"],
    "bank_kyc_screenshare": ["Hello, SBI head office से बोल रहे हैं।",
                             "आपका account block हो जाएगा क्योंकि KYC expire है।",
                             "Play Store से TeamViewer QuickSupport install करो और screen share on करो।"],
    "digital_arrest": ["मैं CBI officer विक्रम बोल रहा हूँ।",
                       "आपके नाम पर एक parcel मिला है, जिसमें drugs हैं। आपके खिलाफ warrant निकला है।",
                       "आप digital arrest में हैं?", "ये बात किसी को मत बताना, call मत काटना।",
                       "verification के लिए अपना पैसा safe account में transfer करिए।"],
    "police_tamil": ["நான் police அதிகாரி பேசுகிறேன். உங்கள் மீது வழக்கு பதிவாகியுள்ளது, உங்களை கைது செய்வோம்.",
                     "இதை யாரிடமும் சொல்லாதீர்கள். உடனே உங்கள் OTP சொல்லுங்கள்."],
    "cyber_branch_english": ["This is Inspector Sharma from the Mumbai Cyber Crime Branch. A parcel in your name has drugs.",
                             "There is an arrest warrant against you. Do not tell anyone about this call.",
                             "Transfer your savings to the RBI safe account immediately for verification."],
}
PRISMA_SAFE = {
    "tamil_family": ["ஆமாம், நான் இன்று சீக்கிரம் வீட்டுக்கு வருவேன்.", "இரவு சாப்பாடு சேர்ந்து சாப்பிடலாம்."],
    "card_bill_english": ["Hello, this is your bank. Your credit card bill is due on the fifth.",
                          "Please remember, never share your OTP with anyone."],
    "real_bank_reminder": ["नमस्ते, मैं SBI branch से बोल रही हूँ।", "आपका home loan EMI पाँच तारीख को due है।",
                           "याद रखिए, बैंक कभी भी OTP नहीं मांगता। OTP किसी को न बताएं।"],
    "delivery_otp": ["Amazon delivery है, मैं आपके घर के बाहर हूँ।", "delivery OTP बता दीजिए, please।"],
    "doctor_appointment": ["डॉक्टर साहब का appointment कल सुबह दस बजे है।", "थोड़ा जल्दी आइएगा, line लंबी होती है।"],
    "family_surprise": ["बेटा, बोल रहा हूँ, आज घर जल्दी आऊँगा।", "मम्मी को मत बताना, surprise party है।"],
}


@pytest.mark.parametrize("name", PRISMA_SCAM)
def test_real_prisma_scam_transcripts_alert(name):
    assert any(s["alert"] for s in run(PRISMA_SCAM[name])), (name, run(PRISMA_SCAM[name])[-1])


@pytest.mark.parametrize("name", PRISMA_SAFE)
def test_real_prisma_safe_transcripts_do_not_alert(name):
    assert not any(s["alert"] for s in run(PRISMA_SAFE[name])), (name, run(PRISMA_SAFE[name])[-1])


def test_word_boundary_for_latin_phrases():
    # "fir" must not match inside "phir"
    assert find_flags("phir milte hain") == []


def test_playbook_tracks_stages_and_warns_ahead():
    s = run(PRISMA_SCAM["digital_arrest"])
    first = [st["key"] for st in s[0]["playbook"]["stages"] if st["done"]]
    assert first == ["pose"] and "OTP" in s[0]["playbook"]["next"]
    assert "police" in s[1]["playbook"]["next"].lower()  # CBI + warrant -> police myth-buster
    assert all(st["done"] for st in s[-1]["playbook"]["stages"])
    assert "Cut the call" in s[-1]["playbook"]["next"]


def test_playbook_refund_trick_and_safe_call():
    assert "send the money back" in run(["Maine galti se aapko paanch hazaar bhej diye"])[0]["playbook"]["next"]
    assert run(["kal subah dus baje appointment hai"])[0]["playbook"]["next"] is None
