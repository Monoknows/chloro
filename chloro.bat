@echo off
title CHLORO WORKSPACE LAUNCHER

echo [SYSTEM]: Launching Sci-Fi Graphic Core UI...
:: Start app.py and force the terminal to stay inside the frontend directory
start "" cmd /k "cd /d "%~dp0frontend" && python app.py"

echo [SYSTEM]: Booting Backend Audio Logic Pipeline...
:: Start main.py and force the terminal to stay inside the backend directory
start "" cmd /k "cd /d "%~dp0backend" && python main.py"

echo [SYSTEM]: All modules successfully initialized, Sir.
exit