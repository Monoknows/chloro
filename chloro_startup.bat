@echo off
title CHLORO_SYSTEM_BOOT
echo [BOOT]: Initializing Elevated OpenClaw Gateway Engine...

:: OpenClaw Gateway
start "" "C:\Program Files\OpenClaw\openclaw.exe" gateway --port 18789

:: time to fully boot
timeout /t 5 /nobreak

echo [BOOT]: Launching Chloro Core Interface and Hybrid Backend...
cd /d "C:\Users\user213421\chloro"
call chloro.bat