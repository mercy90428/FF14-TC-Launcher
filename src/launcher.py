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
        """向宇峻奧汀 (Userjoy) 繁中服 API 發送認證並取得 Session ID (SID)"""
        otp = generate_otp(self.totp_secret)
        
        # 宇峻奧汀繁中服登入 API 結構
        api_url = "https://api-ff14.userjoy.com/v1/auth/login"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) FFXIV-TC-Launcher/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "email": self.account,
            "password": self.password,
            "otp": otp
        }
        
        try:
            # 發送真實認證請求
            res = self.session.post(api_url, json=payload, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            
            # 解析回傳的 Session Token (SID)
            sid = data.get("sid") or data.get("data", {}).get("sid")
            if not sid:
                raise ValueError(f"登入失敗：伺服器未回傳有效 SID ({data.get('message', '未知錯誤')})")
                
            return sid
        except requests.RequestException as e:
            raise RuntimeError(f"連線至宇峻奧汀認證伺服器失敗：{e}")

    def launch_game(self, session_token: str):
        """帶入完整繁中服官方啟動旗標並拉起 ffxiv_dx11.exe"""
        if not os.path.exists(self.game_path):
            raise FileNotFoundError(f"找不到遊戲主程式：{self.game_path}")

        game_dir = os.path.dirname(self.game_path)
        
        # 繁中服 (Userjoy) 必備的完整啟動參數（修復錯誤 0 的關鍵）
        cmd = [
            self.game_path,
            "DEV.TestUser=0",
            "DEV.MaxFPSTax=0",
            "DEV.LobbyHost01=ff14lobby.userjoy.com",  # 繁中服大廳伺服器網址
            "DEV.LobbyPort01=54994",                 # 繁中服大廳 Port
            "SYS.Language=1",                        # 語系設定 (1 為繁中/預設)
            f"-sid={session_token}"                   # 驗證憑證
        ]

        # 以遊戲工作目錄啟動進程
        subprocess.Popen(cmd, cwd=game_dir)