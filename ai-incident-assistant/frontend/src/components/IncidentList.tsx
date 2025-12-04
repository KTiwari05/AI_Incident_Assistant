import { useEffect, useState } from "react";
import axios from "axios";

export interface Incident {
  id: number;
  title: string;
  description?: string;
  severity: "P1" | "P2" | "P3" | string;
  status: "Open" | "Investigating" | "Resolved" | string;
  created_at: string;
}

interface IncidentListProps {
  selectedId: number | null;
  onSelect: (id: number) => void;
}

export default function IncidentList({ selectedId, onSelect }: IncidentListProps) {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);

  const fetchIncidents = async () => {
    setLoading(true);
    try {
      const res = await axios.get<Incident[]>("/api/incidents/");
      setIncidents(res.data);
    } catch (err) {
      console.error("Failed to fetch incidents", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  const handleCreateIncident = async () => {
    const title = window.prompt("Enter incident title (e.g. Nginx 502 on checkout)");
    if (!title || !title.trim()) return;

    setCreating(true);
    try {
      const res = await axios.post<Incident>("/api/incidents/", {
        title: title.trim(),
        description: "",
        severity: "P2",
        status: "Open",
      });

      const newInc = res.data;
      // Put new incident at top
      setIncidents((prev) => [newInc, ...prev]);
      onSelect(newInc.id);
    } catch (err) {
      console.error("Failed to create incident", err);
      window.alert("Failed to create incident. Check console for details.");
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="px-3 py-2 border-b border-slate-800 text-xs font-semibold uppercase tracking-wide text-slate-400 flex justify-between items-center">
        <span>Incidents</span>
        <button
          onClick={handleCreateIncident}
          disabled={creating}
          className="text-[11px] px-2 py-0.5 rounded border border-slate-700 hover:bg-slate-900 disabled:opacity-50"
        >
          {creating ? "Creating..." : "+ New"}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading && (
          <div className="px-3 py-2 text-[11px] text-slate-400">
            Loading incidents...
          </div>
        )}

        {!loading && incidents.length === 0 && (
          <div className="px-3 py-2 text-[11px] text-slate-400">
            No incidents yet. Use <span className="font-semibold">+ New</span> to create one.
          </div>
        )}

        {incidents.map((inc) => (
          <button
            key={inc.id}
            onClick={() => onSelect(inc.id)}
            className={`w-full text-left px-3 py-2 text-sm border-b border-slate-900 hover:bg-slate-800/50 ${
              selectedId === inc.id ? "bg-slate-800" : ""
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-medium truncate">{inc.title}</span>
              <span
                className={`text-[10px] px-2 py-0.5 rounded-full ${
                  inc.severity === "P1"
                    ? "bg-red-600/20 text-red-400"
                    : inc.severity === "P2"
                    ? "bg-amber-600/20 text-amber-300"
                    : "bg-emerald-600/20 text-emerald-300"
                }`}
              >
                {inc.severity}
              </span>
            </div>
            <div className="text-[11px] text-slate-400 mt-0.5">
              #{inc.id} · {inc.status}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
