import subprocess
import os
import time

print("[🎛️] Launching GUI...")

# Optional: activate virtualenv if one exists
venv_path = os.path.join(os.getcwd(), "venv", "Scripts", "activate.bat")
if os.path.exists(venv_path):
    print("[🔄] Activating virtual environment...")
    subprocess.call(venv_path, shell=True)

# ✅ Run server.py directly from backend folder
backend_path = os.path.join("C:\\real_memory_system", "backend")
print("[🔌] Starting backend server from:", backend_path)
subprocess.Popen(
    ["uvicorn", "server:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=backend_path
)

# Give backend time to boot
time.sleep(2)

# Start Electron GUI if available
frontend_dir = os.path.join("C:\\real_memory_system", "frontend")
electron_start = os.path.join(frontend_dir, "node_modules", ".bin", "electron.cmd")
main_js = os.path.join(frontend_dir, "main.js")

if os.path.exists(electron_start) and os.path.exists(main_js):
    print("[🖥️] Launching Electron GUI...")
    subprocess.Popen([electron_start, main_js], cwd=frontend_dir)
else:
    print("[⚠️] Electron GUI not found. Please run `npm install` in /frontend and make sure main.js exists.")

print("[✅] GUI system launched.")
