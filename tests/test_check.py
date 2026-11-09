import pytest

from backend.check import check_text, link_flags, norm_phone

SCAMS = {
    "electricity": "Dear consumer, your electricity power will be disconnected tonight at 9.30 PM because your last bill was not updated. Contact our officer immediately 9876543210",
    "kyc_link": "SBI: Your account will be blocked today. Update KYC now: http://sbi-kyc-update.xyz/login",
    "apk": "Your PM Kisan installment is pending. Download the app to update: http://pmkisan-help.in/PMKisan.apk",
    "job": "Part time job! Like and subscribe YouTube videos and earn Rs 3000 daily. Contact on WhatsApp 9123456789",
    "parcel_hi": "आपका पार्सल customs में रोका गया है, इसमें drugs मिले हैं। तुरंत इस लिंक पर क्लिक करें bit.ly/3xYz",
    "upi_refund": "Sir maine galti se 5000 bhej diye, please wapas bhej do. Maine collect request bheji hai raju.k@ybl par approve kar do",
}
SAFE = {
    "bank_otp": "123456 is your OTP for login to SBI YONO. Do not share it with anyone. -SBI",
    "delivery": "Your Amazon order has been delivered. Track at https://www.amazon.in/orders",
    "family": "Beta, aaj shaam ko 7 baje ghar aa jana, khana saath khayenge.",
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
