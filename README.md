# FF14-TC-Launcher

FF14 繁體中文服（台港澳服）免輸入 OTP 自訂登陸器。

## 特色
* **GUI 視窗介面**：提供直覺的設定與登入畫面。
* **DPAPI 本地安全加密**：敏感憑證（帳號、密碼、TOTP 金鑰）使用 Windows DPAPI 加密儲存，金鑰不離機。
* **自動算碼**：依據 TOTP Secret Key 在登入時自動算出當前 6 位數 OTP 驗證碼。
* **一鍵啟動**：驗證成功後自動帶入 Session Token 並啟動 `ffxiv_dx11.exe`。

## 目錄結構
```
FF14-TC-Launcher/
├── src/
│   ├── main.py          # GUI 介面與進入點
│   ├── security.py      # DPAPI 加密/解密模組
│   ├── totp.py          # TOTP 生成模組
│   └── launcher.py      # HTTP 登入與遊戲啟動模組
├── .github/
│   └── workflows/
│       └── release.yml  # GitHub Actions 自動構建打包工作流
├── build.bat            # 本地 PyInstaller 打包腳本
├── requirements.txt     # 相依套件
└── .gitignore
```

## 本地開發與打包步驟

1. 安裝相依套件：
   ```cmd
   pip install -r requirements.txt
   ```
2. 執行原始碼：
   ```cmd
   python src/main.py
   ```
3. 本地打包為單一 EXE 檔：
   ```cmd
   build.bat
   ```
   打包完成後，執行檔將儲存於 `dist/FF14_TC_Launcher/`。

## GitHub Release 自動打包設定

只要建立 Tag 並 Push 至 GitHub（例如 `git tag v1.0.0 && git push origin v1.0.0`），
`.github/workflows/release.yml` 將會自動在雲端 Windows 環境編譯成 EXE 並發布到 GitHub Releases 頁面。

## 安全性警告與免責聲明
* 本專案僅供技術研究與個人自動化登入使用。
* 將 TOTP Key 與帳密存在同一台電腦會降低雙重驗證（2FA）的物理隔離安全層級。
* 請勿將生成之 `credentials.bin` 檔案上傳至任何平台。
