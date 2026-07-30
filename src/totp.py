import pyotp

def generate_otp(totp_secret: str) -> str:
    clean_secret = totp_secret.replace(" ", "").upper()
    totp = pyotp.TOTP(clean_secret)
    return totp.now()
