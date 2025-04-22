@echo off
setlocal ENABLEEXTENSIONS
cd /d %~dp0

set FRONTEND=black-dashboard-django-master\frontend
set PAGES=%FRONTEND%\pages
set COMPONENTS=%FRONTEND%\components

:: Create folders if missing
echo [✓] Checking if %PAGES% exists...
if not exist %PAGES% mkdir %PAGES%
echo [✓] Created folder: %PAGES%
if not exist %COMPONENTS% mkdir %COMPONENTS%
echo [✓] Created folder: %COMPONENTS%

:: Write memory.tsx
echo [✓] Writing memory.tsx...
> %PAGES%\memory.tsx echo // pages/memory.tsx
>> %PAGES%\memory.tsx echo import dynamic from 'next/dynamic';
>> %PAGES%\memory.tsx echo.
>> %PAGES%\memory.tsx echo const ChatBox = dynamic(() => import('../components/ChatBox'), { ssr: false });
>> %PAGES%\memory.tsx echo.
>> %PAGES%\memory.tsx echo export default function MemoryPanel() {
>> %PAGES%\memory.tsx echo   return (
>> %PAGES%\memory.tsx echo     <div className=\"min-h-screen bg-black text-green-400 font-mono p-6\">
>> %PAGES%\memory.tsx echo       <h1 className=\"text-3xl font-bold mb-6\">🧠 Swarm Memory ^& Chat Console</h1>
>> %PAGES%\memory.tsx echo       <div className=\"border border-green-800 p-2\">
>> %PAGES%\memory.tsx echo         <ChatBox />
>> %PAGES%\memory.tsx echo       </div>
>> %PAGES%\memory.tsx echo     </div>
>> %PAGES%\memory.tsx echo   );
>> %PAGES%\memory.tsx echo }

:: Write ChatBox.tsx
echo [✓] Writing ChatBox.tsx...
> %COMPONENTS%\ChatBox.tsx echo // components/ChatBox.tsx — Retropunk Chat Console
>> %COMPONENTS%\ChatBox.tsx echo import { useState } from 'react';
>> %COMPONENTS%\ChatBox.tsx echo.
>> %COMPONENTS%\ChatBox.tsx echo export default function ChatBox() {
>> %COMPONENTS%\ChatBox.tsx echo   const [messages, setMessages] = useState([]);
>> %COMPONENTS%\ChatBox.tsx echo   const [input, setInput] = useState("");
>> %COMPONENTS%\ChatBox.tsx echo   const [loading, setLoading] = useState(false);
>> %COMPONENTS%\ChatBox.tsx echo.
>> %COMPONENTS%\ChatBox.tsx echo   const sendMessage = async () => {
>> %COMPONENTS%\ChatBox.tsx echo     if (!input.trim()) return;
>> %COMPONENTS%\ChatBox.tsx echo     const newEntry = { user: input, ai: "" };
>> %COMPONENTS%\ChatBox.tsx echo     setMessages((prev) => [...prev, newEntry]);
>> %COMPONENTS%\ChatBox.tsx echo     setInput("");
>> %COMPONENTS%\ChatBox.tsx echo     setLoading(true);
>> %COMPONENTS%\ChatBox.tsx echo     try {
>> %COMPONENTS%\ChatBox.tsx echo       const res = await fetch("/api/chat", {
>> %COMPONENTS%\ChatBox.tsx echo         method: "POST",
>> %COMPONENTS%\ChatBox.tsx echo         headers: { "Content-Type": "application/json" },
>> %COMPONENTS%\ChatBox.tsx echo         body: JSON.stringify({ prompt: newEntry.user })
>> %COMPONENTS%\ChatBox.tsx echo       });
>> %COMPONENTS%\ChatBox.tsx echo       const data = await res.json();
>> %COMPONENTS%\ChatBox.tsx echo       setMessages((prev) => {
>> %COMPONENTS%\ChatBox.tsx echo         const updated = [...prev];
>> %COMPONENTS%\ChatBox.tsx echo         updated[updated.length - 1].ai = data.response;
>> %COMPONENTS%\ChatBox.tsx echo         return updated;
>> %COMPONENTS%\ChatBox.tsx echo       });
>> %COMPONENTS%\ChatBox.tsx echo     } catch (err) {
>> %COMPONENTS%\ChatBox.tsx echo       setMessages((prev) => {
>> %COMPONENTS%\ChatBox.tsx echo         const updated = [...prev];
>> %COMPONENTS%\ChatBox.tsx echo         updated[updated.length - 1].ai = "[Error communicating with LLM]";
>> %COMPONENTS%\ChatBox.tsx echo         return updated;
>> %COMPONENTS%\ChatBox.tsx echo       });
>> %COMPONENTS%\ChatBox.tsx echo     } finally {
>> %COMPONENTS%\ChatBox.tsx echo       setLoading(false);
>> %COMPONENTS%\ChatBox.tsx echo     }
>> %COMPONENTS%\ChatBox.tsx echo   };
>> %COMPONENTS%\ChatBox.tsx echo.
>> %COMPONENTS%\ChatBox.tsx echo   return (
>> %COMPONENTS%\ChatBox.tsx echo     <div className=\"bg-black text-green-400 font-mono h-[90vh] flex flex-col\">
>> %COMPONENTS%\ChatBox.tsx echo       <div className=\"overflow-y-auto flex-grow p-4 space-y-3\">
>> %COMPONENTS%\ChatBox.tsx echo         {messages.map((m, i) => (
>> %COMPONENTS%\ChatBox.tsx echo           <div key={i}>
>> %COMPONENTS%\ChatBox.tsx echo             <div className=\"text-green-300\">▶ YOU: {m.user}</div>
>> %COMPONENTS%\ChatBox.tsx echo             <div className=\"text-green-500\">◀ LLM: {m.ai}</div>
>> %COMPONENTS%\ChatBox.tsx echo           </div>
>> %COMPONENTS%\ChatBox.tsx echo         ))}
>> %COMPONENTS%\ChatBox.tsx echo         {loading && <div className=\"text-yellow-400 animate-pulse\">◀ LLM: ...</div>}
>> %COMPONENTS%\ChatBox.tsx echo       </div>
>> %COMPONENTS%\ChatBox.tsx echo       <div className=\"p-4 border-t border-green-700\">
>> %COMPONENTS%\ChatBox.tsx echo         <input
>> %COMPONENTS%\ChatBox.tsx echo           className=\"w-full p-2 bg-gray-900 text-green-200 border border-green-800\"
>> %COMPONENTS%\ChatBox.tsx echo           value={input}
>> %COMPONENTS%\ChatBox.tsx echo           onChange={(e) => setInput(e.target.value)}
>> %COMPONENTS%\ChatBox.tsx echo           onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
>> %COMPONENTS%\ChatBox.tsx echo           placeholder=\"Type your command...\">
>> %COMPONENTS%\ChatBox.tsx echo         </input>
>> %COMPONENTS%\ChatBox.tsx echo       </div>
>> %COMPONENTS%\ChatBox.tsx echo     </div>
>> %COMPONENTS%\ChatBox.tsx echo   );
>> %COMPONENTS%\ChatBox.tsx echo }

echo [✓] GUI memory panel and ChatBox created.
pause