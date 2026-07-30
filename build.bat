@echo off
chcp 65001 > NUL
echo 正在打包 FF14 繁中服自訂登陸器為 EXE...

pyinstaller --noconfirm --onefile --windowed --name "FF14_TC_Launcher" src/main.py

echo.
echo 打包完成！執行檔位於 dist/FF14_TC_Launcher.exe
pause
