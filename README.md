# FF14-TC-Launcher (繁中服免輸入 OTP 自訂登陸器)

專為 **《Final Fantasy XIV》繁體中文服（台港澳服）** 設計的自訂登陸器。支援自動記憶帳密、QR Code 匯入 2FA 金鑰、自動計算 OTP 並帶入憑證一鍵啟動遊戲。

---

## 特色功能

* **GUI 視窗介面**：使用 Tkinter 構建簡單直覺的操作介面。
* **QR Code 自動解析**：支援匯入 Google Authenticator 轉移條碼（`otpauth-migration://`）或官網 2FA 綁定條碼（`otpauth://`），自動提取 TOTP 金鑰。
* **DPAPI 本地安全加密**：帳號、密碼與 TOTP 金鑰皆透過 Windows DPAPI 加密儲存，金鑰不離機。
* **自動計算 OTP**：登入時依據本地金鑰即時生成當前 6 位數 OTP 驗證碼。
* **一鍵啟動**：驗證成功後自動獲取 Session Token 並啟動 `ffxiv_dx11.exe`。

---

## 初次使用與設定指南 (使用者指南)

### 步驟 1：準備 2FA QR Code 圖片
可透過以下兩種方式之一準備 QR Code 圖片：
1. **Google Authenticator 匯出條碼：** 手機開啟 App -> 點擊選單 ->「轉移帳戶/匯出帳戶」-> 選取 FF14 帳號 -> 截圖並傳送至電腦。
2. **官網重新綁定條碼：** 登入繁中服官網會員中心 -> 進行 2FA 綁定 -> 將網頁出現的 QR Code 儲存為圖片。

### 步驟 2：在登陸器中儲存設定
1. 執行 `FF14_TC_Launcher.exe`（或執行 `python src/main.py`）。
2. 輸入繁中服登入帳號（Email）與密碼。
3. 點擊 **「匯入 QR Code」**，選擇準備好的 QR Code 圖片，系統將自動解析並填入 TOTP Key。
4. 點擊 **「瀏覽...」** 指定電腦中的 `ffxiv_dx11.exe` 路徑。
5. 點擊 **「儲存設定」**，憑證將自動加密寫入本地 `credentials.bin`。

### 步驟 3：日常登入流程
1. 開啟登陸器，程式會自動讀取並解密本地憑證。
2. 點擊 **「登入並啟動遊戲」**，系統將自動計算當前 OTP、完成認證並拉起遊戲主程式。

---

## 專案目錄結構

```text
FF14-TC-Launcher/
├── src/
│   ├── main.py          # GUI 介面與主邏輯
│   ├── security.py      # DPAPI 本地憑證加密與解密模組
│   ├── totp.py          # TOTP 演算法算碼模組
│   ├── qr_parser.py     # QR Code 條碼識別與 Protobuf 解析模組
│   └── launcher.py      # HTTP 認證與遊戲主程式啟動模組
├── .github/
│   └── workflows/
│       └── release.yml  # GitHub Actions 自動構建工作流腳本
├── build.bat            # Windows 本地一鍵編譯成 EXE 批次檔
├── requirements.txt     # Python 相依套件清單
├── README.md            # 本說明文件
└── .gitignore           # Git 版本控制排除規則
```

---

## 開發與編譯說明

### 本地獨立打包成 EXE
```cmd
pip install -r requirements.txt
build.bat
```
編譯成品位於 `dist/FF14_TC_Launcher.exe`。

### GitHub Actions 自動編譯發佈
推送帶有 `v` 前綴的版本標籤即可觸發雲端自動建置：
```bash
git tag v2.0.0
git push origin v2.0.0
```
