import json
import os
import win32crypt

CONFIG_FILE = "credentials.bin"

def encrypt_string(plain_text: str) -> bytes:
    data_bytes = plain_text.encode('utf-8')
    return win32crypt.CryptProtectData(data_bytes, None, None, None, None, 0)

def decrypt_bytes(encrypted_bytes: bytes) -> str:
    _, decrypted_bytes = win32crypt.CryptUnprotectData(encrypted_bytes, None, None, None, 0)
    return decrypted_bytes.decode('utf-8')

def save_credentials(account: str, password: str, totp_secret: str, game_path: str):
    data = {
        "account": account,
        "password": password,
        "totp_secret": totp_secret,
        "game_path": game_path
    }
    json_str = json.dumps(data)
    encrypted_data = encrypt_string(json_str)
    with open(CONFIG_FILE, "wb") as f:
        f.write(encrypted_data)

def load_credentials() -> dict | None:
    if not os.path.exists(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "rb") as f:
            encrypted_data = f.read()
        json_str = decrypt_bytes(encrypted_data)
        return json.loads(json_str)
    except Exception:
        return None
