import subprocess
import os
import time

print("[🎛️] Launching GUI...")

# Optional: activate virtualenv if one exists
venv_path = os.path.join(os.getcwd(), "venv", "Scripts", "activate.bat")
if os.path.exists(venv_path):
    print("[🔄] Activating virtual environment...")
    subprocess.call(venv_path, shell=True)

# Run FastAPI server (backend)
print("[🔌] Starting backend server on port 8000...")
subprocess.Popen(["uvicorn", "backend.server:app", "--host", "127.0.0.1", "--port", "8000"])

# Give the backend a second to start
time.sleep(2)

# Start Electron frontend if available
frontend_dir = os.path.join(os.getcwd(), "frontend")
electron_start = os.path.join(frontend_dir, "node_modules", ".bin", "electron.cmd")
main_js = os.path.join(frontend_dir, "main.js")

if os.path.exists(electron_start) and os.path.exists(main_js):
    print("[🖥️] Launching Electron GUI...")
    subprocess.Popen([electron_start, main_js], cwd=frontend_dir)
else:
    print("[⚠️] Electron GUI not found. Please run `npm install` in /frontend and make sure main.js exists.")

print("[✅] GUI system launched.")
