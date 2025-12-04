import { useEffect, useState } from "react";
import axios from "axios";

interface LLMPerModel {
  model: string;
  count: number;
  avg_latency_ms: number | null;
}

interface LLMStats {
  total_calls: number;
  avg_latency_ms: number | null;
  total_prompt_chars: number;
  total_completion_chars: number;
  per_model: LLMPerModel[];
}

export default function MetricsPanel() {
  const [stats, setStats] = useState<LLMStats | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const res = await axios.get<LLMStats>("/api/metrics/llm/");
      setStats(res.data);
    } catch (err) {
      console.error("Failed to fetch LLM metrics", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    const id = setInterval(fetchStats, 10000); // refresh every 10s
    return () => clearInterval(id);
  }, []);

  return (
    <div className="border-t border-slate-800 px-3 py-2 text-[11px] text-slate-300">
      <div className="flex items-center justify-between mb-1">
        <span className="font-semibold uppercase tracking-wide text-slate-400">
          LLM Metrics
        </span>
        {loading && <span className="text-slate-500">refreshing…</span>}
      </div>

      {!stats && !loading && (
        <div className="text-slate-500">No data yet. Trigger some calls.</div>
      )}

      {stats && (
        <div className="space-y-1">
          <div className="flex justify-between">
            <span>Total calls</span>
            <span className="font-mono">{stats.total_calls}</span>
          </div>
          <div className="flex justify-between">
            <span>Avg latency</span>
            <span className="font-mono">
              {stats.avg_latency_ms !== null
                ? `${stats.avg_latency_ms.toFixed(1)} ms`
                : "n/a"}
            </span>
          </div>
          <div className="flex justify-between">
            <span>Prompt chars</span>
            <span className="font-mono">{stats.total_prompt_chars}</span>
          </div>
          <div className="flex justify-between mb-1">
            <span>Completion chars</span>
            <span className="font-mono">{stats.total_completion_chars}</span>
          </div>

          {stats.per_model.length > 0 && (
            <div className="mt-1">
              <div className="text-[10px] uppercase text-slate-500 mb-1">
                Per model
              </div>
              <div className="space-y-0.5">
                {stats.per_model.map((m) => (
                  <div
                    key={m.model}
                    className="flex justify-between text-[10px]"
                  >
                    <span className="truncate max-w-[90px]">{m.model}</span>
                    <span className="font-mono">
                      {m.count} calls ·{" "}
                      {m.avg_latency_ms !== null
                        ? `${m.avg_latency_ms.toFixed(1)} ms`
                        : "n/a"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
