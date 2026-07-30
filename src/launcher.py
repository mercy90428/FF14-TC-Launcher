import os
import subprocess
import requests
from totp import generate_otp

class FF14TCLauncher:
    def __init__(self, account: str, password: str, totp_secret: str, game_path: str):
        self.account = account
        self.password = password
        self.totp_secret = totp_secret
        self.game_path = game_path
        self.session = requests.Session()

    def login(self) -> str:
        otp = generate_otp(self.totp_secret)
        
        # TODO: 根據實際 Fiddler/Charles 抓包結果調整 Endpoint 與 Payload
        api_url = "https://api-ff14.userjoy.com/api/v1/auth/login"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FFXIV-TC-Launcher/1.0",
            "Content-Type": "application/json"
        }
        payload = {
            "email": self.account,
            "password": self.password,
            "otp_code": otp
        }
        
        # 實務連線範例:
        # res = self.session.post(api_url, json=payload, headers=headers, timeout=10)
        # res.raise_for_status()
        # token = res.json().get("session_token")
        
        token = "MOCK_SESSION_TOKEN_1234567890"
        return token

    def launch_game(self, session_token: str):
        if not os.path.exists(self.game_path):
            raise FileNotFoundError(f"找不到遊戲主程式：{self.game_path}")

        game_dir = os.path.dirname(self.game_path)
        cmd = [
            self.game_path,
            "//",
            "SYS.Language=1",
            f"-sid={session_token}"
        ]
        subprocess.Popen(cmd, cwd=game_dir)
