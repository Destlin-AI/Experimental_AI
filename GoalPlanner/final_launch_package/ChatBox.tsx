// components/ChatBox.tsx — Retropunk Fullscreen Chat Console

import { useState } from 'react';

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newEntry = { user: input, ai: "" };
    setMessages((prev) => [...prev, newEntry]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: newEntry.user })
      });
      const data = await res.json();
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].ai = data.response;
        return updated;
      });
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1].ai = "[Error communicating with LLM]";
        return updated;
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-black text-green-400 font-mono h-[90vh] flex flex-col">
      <div className="overflow-y-auto flex-grow p-4 space-y-3">
        {messages.map((m, i) => (
          <div key={i}>
            <div className="text-green-300">▶ YOU: {m.user}</div>
            <div className="text-green-500">◀ LLM: {m.ai}</div>
          </div>
        ))}
        {loading && <div className="text-yellow-400 animate-pulse">◀ LLM: ...</div>}
      </div>
      <div className="p-4 border-t border-green-700">
        <input
          className="w-full p-2 bg-gray-900 text-green-200 border border-green-800"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type your command..."
        />
      </div>
    </div>
  );
}