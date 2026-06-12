@echo off
title CHLORO_SYSTEM_BOOT
echo [BOOT]: Initializing Elevated OpenClaw Gateway Engine...

:: Launch the OpenClaw background service cleanly on your port
start "" "C:\Program Files\OpenClaw\openclaw.exe" gateway --port 18789

:: Give the gateway 5 seconds to fully boot and bind to the port
timeout /t 5 /nobreak

echo [BOOT]: Launching Chloro Core Interface and Hybrid Backend...
cd /d "C:\Users\user213421\chloro"
call chloro.bat