import { useState } from "react";
import axios from "axios";

export default function KnowledgeBasePanel() {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const ingest = async () => {
    if (!title.trim() || !text.trim() || loading) return;
    setLoading(true);
    setStatus(null);

    try {
      const res = await axios.post("/api/rag/test/ingest", {
        title,
        text,
      });

      setStatus(
        `Ingested successfully. Chunks added: ${res.data.chunks_added ?? "?"}`
      );
      setText("");
    } catch (err) {
      console.error(err);
      setStatus("Error ingesting document.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border-t border-slate-800 p-3 text-xs">
      <div className="flex items-center justify-between mb-2">
        <div className="font-semibold text-[11px] uppercase tracking-wide text-slate-400">
          Knowledge Base
        </div>
        {status && (
          <span className="text-[10px] text-slate-400 truncate max-w-[180px]">
            {status}
          </span>
        )}
      </div>

      <div className="space-y-2">
        <input
          className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-[11px] focus:outline-none focus:ring-1 focus:ring-blue-500"
          placeholder="Document title (e.g. Nginx 502 Runbook)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          className="w-full h-24 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-[11px] resize-none focus:outline-none focus:ring-1 focus:ring-blue-500"
          placeholder="Paste your runbook, SOP, or internal doc here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          onClick={ingest}
          disabled={loading || !title.trim() || !text.trim()}
          className="w-full text-[11px] py-1.5 rounded bg-blue-600 font-medium disabled:opacity-50"
        >
          {loading ? "Ingesting..." : "Ingest into KB"}
        </button>
      </div>
    </div>
  );
}
