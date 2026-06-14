@echo off
title CHLORO_SYSTEM_BOOT

echo [BOOT]: Initializing Elevated OpenClaw Gateway Engine...
:: OpenClaw Gateway
start "" "%appdata%\npm\openclaw.cmd" gateway --port 18789

:: time to fully boot
timeout /t 5 /nobreak

echo Booting Chloro Core Intelligence Agent...
python "%~dp0backend\briefing.py"

echo [BOOT]: Launching Chloro Core Interface and Hybrid Backend...
cd /d "C:\Users\user213421\chloro"
call chloro.bat

pause