@echo off
title Latihan Dashboard
cd /d "%~dp0"
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:5000"
python app.py
echo.
pause
