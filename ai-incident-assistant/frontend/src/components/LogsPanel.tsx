import { useState } from "react";
import axios from "axios";

interface LogsPanelProps {
  selectedIncidentId: number | null;
  logsText: string;
  onLogsTextChange: (value: string) => void;
}

export default function LogsPanel({
  selectedIncidentId,
  logsText,
  onLogsTextChange,
}: LogsPanelProps) {
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const incidentLabel = selectedIncidentId
    ? `Incident #${selectedIncidentId}`
    : "No incident selected";

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!selectedIncidentId) {
      setStatus("Select or create an incident on the left before uploading logs.");
      e.target.value = "";
      return;
    }

    const formData = new FormData();
    formData.append("incident_id", String(selectedIncidentId));
    formData.append("file", file);

    setUploading(true);
    setStatus(null);
    try {
      const res = await axios.post("/api/logs/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(
        `File ${res.data.filename} ingested into incident RAG (chunks: ${res.data.chunks_added}).`
      );
    } catch (err) {
      console.error(err);
      setStatus("Error uploading log file.");
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const handleSaveTextareaToRag = async () => {
    if (!selectedIncidentId) {
      setStatus("Select or create an incident before saving logs.");
      return;
    }
    if (!logsText.trim()) {
      setStatus("Paste some logs before saving.");
      return;
    }

    setSaving(true);
    setStatus(null);
    try {
      const res = await axios.post("/api/logs/text", {
        incident_id: selectedIncidentId,
        text: logsText,
        source: "manual_paste",
      });
      setStatus(
        `Textarea logs ingested into incident RAG (chunks: ${res.data.chunks_added}).`
      );
      // optional: don’t clear logsText, user may want to reuse/edit it
      // onLogsTextChange("");
    } catch (err) {
      console.error(err);
      setStatus("Error saving textarea logs to incident.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="border-b border-slate-800 p-3 text-xs bg-slate-950">
      <div className="flex items-center justify-between mb-1">
        <div className="flex flex-col">
          <div className="font-semibold text-[11px] uppercase tracking-wide text-slate-400">
            Incident Logs & Alerts
          </div>
          <div className="text-[10px] text-slate-500">{incidentLabel}</div>
        </div>
        {status && (
          <span className="text-[10px] text-slate-400 truncate max-w-[260px] text-right">
            {status}
          </span>
        )}
      </div>

      <div className="text-[10px] text-slate-500 mb-2">
        <span className="font-semibold">How this works:</span>{" "}
        Textarea logs are sent directly to the AI on every{" "}
        <span className="font-semibold">Incident (Agents)</span> question.  
        Use the buttons below if you also want to{" "}
        <span className="font-semibold">attach logs permanently</span> to this
        incident&apos;s RAG context.
      </div>

      <div className="flex flex-col gap-2">
        <textarea
          className="w-full h-20 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-[11px] resize-none focus:outline-none focus:ring-1 focus:ring-blue-500"
          placeholder="Paste nginx errors, stack traces, alert payloads, etc. You can keep editing this between questions."
          value={logsText}
          onChange={(e) => {
            setStatus(null);
            onLogsTextChange(e.target.value);
          }}
        />

        <div className="flex items-center justify-between gap-2">
          <button
            type="button"
            onClick={handleSaveTextareaToRag}
            disabled={saving || !selectedIncidentId}
            className="text-[11px] px-2 py-1 rounded bg-slate-800 border border-slate-700 disabled:opacity-50"
          >
            {saving ? "Saving logs to incident…" : "Save textarea logs to incident RAG"}
          </button>

          <div className="flex items-center gap-2">
            <label className="text-[11px] text-slate-400">
              Or attach .log/.txt file:
            </label>
            <input
              type="file"
              accept=".log,.txt,.out,.err"
              onChange={handleFileChange}
              disabled={uploading || !selectedIncidentId}
              className="text-[11px] file:text-[11px] file:px-2 file:py-0.5 file:bg-slate-800 file:border file:border-slate-700 file:rounded disabled:opacity-50"
            />
          </div>
        </div>

        {!selectedIncidentId && (
          <div className="text-[10px] text-amber-400">
            You haven&apos;t selected an incident yet. Create or select one on the left so
            logs, uploads, and analysis are tied to it.
          </div>
        )}
      </div>
    </div>
  );
}
