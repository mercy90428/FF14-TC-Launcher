import tkinter as tk
from tkinter import messagebox, filedialog
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from security import save_credentials, load_credentials
from launcher import FF14TCLauncher
from qr_parser import extract_secret_from_image

class LauncherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FF14 繁中服自動登陸器")
        self.root.geometry("480x420")
        self.root.resizable(False, False)

        tk.Label(root, text="FF14 繁中服免輸入 OTP 登陸器", font=("Microsoft JhengHei", 14, "bold")).pack(pady=12)

        frame = tk.Frame(root)
        frame.pack(padx=20, pady=5, fill="x")

        # 帳號
        tk.Label(frame, text="帳號 (Email):", font=("Microsoft JhengHei", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_account = tk.Entry(frame, width=35)
        self.entry_account.grid(row=0, column=1, pady=5)

        # 密碼
        tk.Label(frame, text="密碼:", font=("Microsoft JhengHei", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_password = tk.Entry(frame, width=35, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        # TOTP Key (支援手動輸入或 QR Code 匯入)
        tk.Label(frame, text="TOTP Key:", font=("Microsoft JhengHei", 9)).grid(row=2, column=0, sticky="w", pady=5)
        totp_frame = tk.Frame(frame)
        totp_frame.grid(row=2, column=1, sticky="ew")
        self.entry_totp = tk.Entry(totp_frame, width=22, show="*")
        self.entry_totp.pack(side="left", fill="x", expand=True)
        tk.Button(totp_frame, text="匯入 QR Code", command=self.import_qrcode, bg="#E1E1E1").pack(side="right", padx=2)

        # 遊戲路徑
        tk.Label(frame, text="遊戲路徑:", font=("Microsoft JhengHei", 9)).grid(row=3, column=0, sticky="w", pady=5)
        path_frame = tk.Frame(frame)
        path_frame.grid(row=3, column=1, sticky="ew")
        self.entry_path = tk.Entry(path_frame, width=24)
        self.entry_path.pack(side="left", fill="x", expand=True)
        tk.Button(path_frame, text="瀏覽...", command=self.browse_path).pack(side="right", padx=2)

        # 動作按鈕
        self.btn_save = tk.Button(root, text="儲存設定", command=self.save_config, width=15)
        self.btn_save.pack(pady=8)

        self.btn_launch = tk.Button(root, text="登入並啟動遊戲", command=self.start_login, bg="#0078D7", fg="white", font=("Microsoft JhengHei", 11, "bold"), width=25, height=2)
        self.btn_launch.pack(pady=10)

        self.lbl_status = tk.Label(root, text="狀態: 就緒", fg="gray", font=("Microsoft JhengHei", 9))
        self.lbl_status.pack(side="bottom", pady=5)

        self.load_config()

    def import_qrcode(self):
        file_selected = filedialog.askopenfilename(
            title="選擇包含 2FA / 驗證器 QR Code 的圖片",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
        )
        if file_selected:
            try:
                secret_key = extract_secret_from_image(file_selected)
                self.entry_totp.delete(0, tk.END)
                self.entry_totp.insert(0, secret_key)
                self.lbl_status.config(text="狀態: 成功從 QR Code 解析 TOTP Key！", fg="green")
                messagebox.showinfo("成功", "已成功從 QR Code 圖片提取 TOTP 金鑰！")
            except Exception as e:
                self.lbl_status.config(text=f"狀態: QR Code 解析失敗 - {str(e)}", fg="red")
                messagebox.showerror("QR Code 解析失敗", str(e))

    def browse_path(self):
        file_selected = filedialog.askopenfilename(
            title="選擇 ffxiv_dx11.exe",
            filetypes=[("Executable Files", "ffxiv_dx11.exe"), ("All Files", "*.*")]
        )
        if file_selected:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, file_selected)

    def load_config(self):
        creds = load_credentials()
        if creds:
            self.entry_account.insert(0, creds.get("account", ""))
            self.entry_password.insert(0, creds.get("password", ""))
            self.entry_totp.insert(0, creds.get("totp_secret", ""))
            self.entry_path.insert(0, creds.get("game_path", ""))
            self.lbl_status.config(text="狀態: 已載入加密憑證", fg="green")

    def save_config(self):
        acc = self.entry_account.get().strip()
        pwd = self.entry_password.get().strip()
        totp = self.entry_totp.get().strip()
        path = self.entry_path.get().strip()

        if not all([acc, pwd, totp, path]):
            messagebox.showwarning("提示", "所有欄位皆為必填！")
            return

        save_credentials(acc, pwd, totp, path)
        self.lbl_status.config(text="狀態: 設定已加密儲存", fg="green")
        messagebox.showinfo("成功", "帳密與 TOTP Key 已使用 DPAPI 加密儲存！")

    def start_login(self):
        acc = self.entry_account.get().strip()
        pwd = self.entry_password.get().strip()
        totp = self.entry_totp.get().strip()
        path = self.entry_path.get().strip()

        if not all([acc, pwd, totp, path]):
            messagebox.showwarning("錯誤", "請完整填寫登入資訊與遊戲路徑！")
            return

        try:
            self.lbl_status.config(text="狀態: 正在計算 OTP 並驗證登入...", fg="blue")
            self.root.update()
            
            launcher = FF14TCLauncher(acc, pwd, totp, path)
            token = launcher.login()
            
            self.lbl_status.config(text="狀態: 驗證成功，正在啟動遊戲...", fg="blue")
            self.root.update()
            
            launcher.launch_game(token)
            self.root.destroy()
        except Exception as e:
            self.lbl_status.config(text=f"狀態: 錯誤 - {str(e)}", fg="red")
            messagebox.showerror("登入失敗", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()
