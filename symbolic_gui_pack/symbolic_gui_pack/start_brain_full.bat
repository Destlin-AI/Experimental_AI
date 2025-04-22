@echo off
setlocal EnableDelayedExpansion

:: ==========================
:: [🧠] Symbolic Memory System Boot
:: ==========================

echo [🔍] Checking Python environment...
where python >nul 2>nul || (
    echo [❌] Python not found! Please install Python 3.10+ and retry.
    pause
    exit /b
)

echo [🔍] Validating required packages...
python -c "import duckdb, yaml, psutil, fastapi, starlette, uvicorn" 2>nul || (
    echo [⚠️] One or more Python packages are missing or broken.
    echo [🛠] Installing packages...
    pip install duckdb pyyaml psutil fastapi==0.95.2 starlette==0.37.2 uvicorn open-interpreter==0.4.3
)

:: ==========================
:: [🚀] Launching Services
:: ==========================

echo [🚀] Starting backend API...
start "" python backend\server.py

echo [⚙️] Starting GUI layer...
start "" python gui\gui_launcher.py

echo [🤖] Launching Open Interpreter daemon...
start "" open-interpreter

echo [🧠] Symbolic system booted. Press any key to exit this launcher window.
pause
exit /b
