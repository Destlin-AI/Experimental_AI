@echo off
title 🧠 Symbolic AI System Launcher
cd /d D:\Project_AI

echo [🔧] Activating environment...
call venv\Scripts\activate.bat

echo [🧠] Starting core runtime...
start "" python Symbolic_AI_Master_Core_FULL_GUI_INTEGRATED.py

echo [🌐] Booting GUI dashboard (Black Dashboard Django)...
cd gui
start "" python manage.py runserver 127.0.0.1:8000

echo [✅] All systems live. Close window to exit launcher.
pause >nul
