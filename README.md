# FF14-TC-Launcher (支援 QR Code 匯入版)

FF14 繁體中文服（台港澳服）免輸入 OTP 自訂登陸器。

## 特色
* **GUI 視窗介面**：簡單直覺的設定與登入介面。
* **QR Code 自動解析**：支援匯入 Google Authenticator 轉移/匯出 QR Code 或官網 2FA 綁定圖片，自動提取 TOTP 金鑰。
* **DPAPI 本地安全加密**：帳號、密碼與 TOTP 金鑰皆經由 Windows DPAPI 加密儲存，確保金鑰不離開本機。
* **自動算碼**：登入時依據本地金鑰即時生成當前 6 位數 OTP 驗證碼。
* **一鍵啟動**：驗證成功後自動獲取 Session Token 並啟動 `ffxiv_dx11.exe`。

## 目錄結構
```
FF14-TC-Launcher/
├── src/
│   ├── main.py          # GUI 介面與進入點
│   ├── security.py      # DPAPI 加密/解密模組
│   ├── totp.py          # TOTP 生成模組
│   ├── qr_parser.py     # QR Code 條碼與 Protobuf 解析模組
│   └── launcher.py      # HTTP 登入與遊戲啟動模組
├── .github/
│   └── workflows/
│       └── release.yml  # GitHub Actions 自動構建工作流
├── build.bat            # 本地 PyInstaller 打包腳本
├── requirements.txt     # 相依套件
└── .gitignore
```
