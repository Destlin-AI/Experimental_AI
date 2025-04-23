@echo off
setlocal ENABLEEXTENSIONS

:: Root setup
echo [✓] Starting complete setup...
cd /d %~dp0

:: Create directories
mkdir frontend\pages
mkdir frontend\components
mkdir backend

echo [✓] Directories created

:: Write memory.tsx
echo import dynamic from 'next/dynamic'; > frontend\pages\memory.tsx
echo const ChatBox = dynamic(() =^> import('../components/ChatBox'), { ssr: false }); >> frontend\pages\memory.tsx
echo export default function MemoryPanel() { return ^<div^>^<ChatBox /^>^</div^>; } >> frontend\pages\memory.tsx

echo [✓] memory.tsx created

:: Write ChatBox.tsx
echo import { useState } from 'react'; > frontend\components\ChatBox.tsx
echo export default function ChatBox() { return ^<div^>ChatBox Ready^</div^>; } >> frontend\components\ChatBox.tsx

echo [✓] ChatBox.tsx created

:: Install Python dependencies (ensure they're installed before backend starts)
echo [✓] Installing Python dependencies...
pip install flask llama-cpp-python open-interpreter

echo [✓] Python dependencies installed

:: Setup Python backend
cd backend
echo from flask import Flask, jsonify, request > server.py
echo app = Flask(__name__) >> server.py
echo @app.route('/api/chat', methods=['POST']) >> server.py
echo def chat(): return jsonify({"response": "Chat ready"}) >> server.py

echo [✓] server.py created

:: Setup Node frontend
cd ..\frontend
echo { "scripts": { "dev": "next dev -p 3000" }, "dependencies": { "next": "latest", "react": "latest", "react-dom": "latest" } } > package.json
npm install

echo [✓] Node dependencies installed

:: Launch Backend and Frontend
start "" cmd /k "python ..\backend\server.py"
start "" cmd /k "interpreter"
start "" cmd /k "npm run dev"

echo [✓] Everything launched
pause