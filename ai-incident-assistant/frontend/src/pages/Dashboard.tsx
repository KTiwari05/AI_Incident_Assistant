import { useState } from "react";
import IncidentList from "../components/IncidentList";
import ChatPanel from "../components/ChatPanel";
import TimelinePanel from "../components/TimelinePanel";
import KnowledgeBasePanel from "../components/KnowledgeBasePanel";
import AnalysisPanel from "../components/AnalysisPanel";
import type { AgentsOutput } from "../types/agents";
import MetricsPanel from "../components/MetricsPanel";
import LogsPanel from "../components/LogsPanel";

export type ChatMode = "general" | "incident";

export default function Dashboard() {
  const [mode, setMode] = useState<ChatMode>("incident");
  const [agentsOutput, setAgentsOutput] = useState<AgentsOutput | null>(null);
  const [selectedIncidentId, setSelectedIncidentId] = useState<number | null>(null);
  const [logsText, setLogsText] = useState<string>("");
  return (
    <div className="h-screen flex flex-col bg-slate-950 text-slate-50">
      <header className="flex items-center justify-between px-4 py-2 border-b border-slate-800">
        <div className="font-semibold text-lg">AI Incident Assistant</div>

        <div className="flex items-center gap-2 text-xs">
          <span className="text-slate-400">Mode:</span>
          <button
            onClick={() => setMode("general")}
            className={`px-2 py-1 rounded border text-[11px] ${
              mode === "general"
                ? "bg-slate-100 text-slate-900 border-slate-300"
                : "bg-slate-900 border-slate-700 text-slate-300"
            }`}
          >
            General (RAG)
          </button>
          <button
            onClick={() => setMode("incident")}
            className={`px-2 py-1 rounded border text-[11px] ${
              mode === "incident"
                ? "bg-blue-600 text-white border-blue-500"
                : "bg-slate-900 border-slate-700 text-slate-300"
            }`}
          >
            Incident (Agents)
          </button>
        </div>
      </header>

      <main className="flex flex-1 overflow-hidden">
        <section className="w-1/4 border-r border-slate-800 overflow-y-auto">
        <IncidentList
            selectedId={selectedIncidentId}
            onSelect={setSelectedIncidentId}
        />
        </section>

        <section className="w-2/4 border-r border-slate-800 flex flex-col">
        <LogsPanel
            selectedIncidentId={selectedIncidentId}
            logsText={logsText}
            onLogsTextChange={setLogsText}
        />
        <div className="flex-1 min-h-0">
            <ChatPanel
            mode={mode}
            onAgentsOutputChange={setAgentsOutput}
            selectedIncidentId={selectedIncidentId}
            logsText={logsText}
            />
        </div>
        </section>

        <section className="w-1/4 flex flex-col overflow-hidden border-l border-slate-800/40">
        <div className="flex-1 overflow-y-auto">
            <AnalysisPanel agentsOutput={agentsOutput} />
            <TimelinePanel
            timelineText={agentsOutput?.timeline?.timeline}
            />
        </div>
        <KnowledgeBasePanel />
        <MetricsPanel />
        </section>
    </main>
    </div>
  );
}
