import { useState } from "react";
import axios from "axios";
import type { ChatMode } from "../pages/Dashboard";
import type { AgentsOutput } from "../types/agents";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatPanelProps {
  mode: ChatMode;
  onAgentsOutputChange: (output: AgentsOutput | null) => void;
  selectedIncidentId: number | null;
  logsText: string;
}

export default function ChatPanel({
  mode,
  onAgentsOutputChange,
  selectedIncidentId,
  logsText,
}: ChatPanelProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim() || loading) return;

    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      if (mode === "incident") {
        const res = await axios.post("/api/chat/incident/", {
          session_id: 1,
          incident_id: selectedIncidentId, // uses the real selected incident
          message: userMsg.content,
          logs: logsText || "",
          metrics: "", // reserved for future metrics input
          model: "gpt-4o",
        });

        const answer: string = res.data.answer;
        const agents: AgentsOutput = res.data.agents_output;

        const botMsg: Message = { role: "assistant", content: answer };
        setMessages((prev) => [...prev, botMsg]);

        onAgentsOutputChange(agents);
      } else {
        const res = await axios.post("/api/chat/general/", {
          session_id: 1,
          message: userMsg.content,
          model: "gpt-4o",
        });

        const answer: string = res.data.answer;
        const botMsg: Message = { role: "assistant", content: answer };
        setMessages((prev) => [...prev, botMsg]);

        // General mode: clear agents output
        onAgentsOutputChange(null);
      }
    } catch (err) {
      console.error(err);
      const errMsg: Message = {
        role: "assistant",
        content: "Error contacting backend.",
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Chat area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`max-w-[80%] rounded-lg px-3 py-2 text-sm whitespace-pre-wrap ${
              m.role === "user"
                ? "ml-auto bg-blue-600"
                : "mr-auto bg-slate-800 border border-slate-700"
            }`}
          >
            {m.content}
          </div>
        ))}
        {loading && (
          <div className="text-xs text-slate-400 mt-2">
            {mode === "incident"
              ? "Analyzing incident with agents…"
              : "Thinking…"}
          </div>
        )}
      </div>

      {/* Input */}
      <div className="border-t border-slate-800 p-3 flex gap-2">
        <input
          className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          placeholder={
            mode === "incident"
              ? "Describe your incident or paste error details..."
              : "Ask anything (uses KB + memory)..."
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button
          onClick={send}
          disabled={loading}
          className="px-4 py-2 rounded-lg bg-blue-600 text-sm font-medium disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}
