import pytest

from backend.check import check_text, link_flags, norm_phone

SCAMS = {
    "electricity": "Dear consumer, your electricity power will be disconnected tonight at 9.30 PM because your last bill was not updated. Contact our officer immediately 9876543210",
    "kyc_link": "SBI: Your account will be blocked today. Update KYC now: http://sbi-kyc-update.xyz/login",
    "apk": "Your PM Kisan installment is pending. Download the app to update: http://pmkisan-help.in/PMKisan.apk",
    "job": "Part time job! Like and subscribe YouTube videos and earn Rs 3000 daily. Contact on WhatsApp 9123456789",
    "parcel_hi": "आपका पार्सल customs में रोका गया है, इसमें drugs मिले हैं। तुरंत इस लिंक पर क्लिक करें bit.ly/3xYz",
    "upi_refund": "Sir maine galti se 5000 bhej diye, please wapas bhej do. Maine collect request bheji hai raju.k@ybl par approve kar do",
    "loan_harass": "Loan ka paisa aaj nahi diya to tumhare sab contacts ko tumhari photo bhej denge",
    "blackmail": "Your private video is with me. Pay 10000 or it goes viral to your friends and family",
    "relative": "Hi papa this is my new number, phone broke. Need urgent payment of 18000, send it now please",
    "crypto": "Join VIP crypto group, 200% guaranteed returns in 5 days. Invest now",
    "number_block_hi": "आपका मोबाइल नंबर 2 घंटे में बंद कर दिया जाएगा। पुलिस अधिकारी से बात करने के लिए 9 दबाएं",
}
SAFE = {
    "bank_otp": "123456 is your OTP for login to SBI YONO. Do not share it with anyone. -SBI",
    "delivery": "Your Amazon order has been delivered. Track at https://www.amazon.in/orders",
    "family": "Beta, aaj shaam ko 7 baje ghar aa jana, khana saath khayenge.",
    "otp_hinglish": "Aapka OTP 482913 hai HDFC Bank login ke liye. Ye kisi ko na batayein.",
    "kyc_branch": "Dear Customer, periodic KYC update is due. Please visit your home branch with ID proof.",
    "family_money": "Mummy 500 bhej do please, sabzi leni hai",
}


@pytest.mark.parametrize("name", SCAMS)
def test_scam_messages_flagged(name):
    r = check_text(SCAMS[name])
    assert r["verdict"] in ("scam", "suspicious"), (name, r)


@pytest.mark.parametrize("name", SAFE)
def test_safe_messages_pass(name):
    assert check_text(SAFE[name])["verdict"] == "safe", (name, check_text(SAFE[name]))


def test_links_and_numbers():
    assert link_flags("https://www.sbi.co.in/web/personal-banking") == []
    assert any("official" in w for w in link_flags("http://sbi-kyc-update.xyz"))
    assert norm_phone("+91 98765 43210") == "9876543210"
    r = check_text(SCAMS["electricity"])
    assert r["phones"] == ["9876543210"]
