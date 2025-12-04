import type { AgentsOutput } from "../types/agents";

interface AnalysisPanelProps {
  agentsOutput: AgentsOutput | null;
}

export default function AnalysisPanel({ agentsOutput }: AnalysisPanelProps) {
  const logAnalysis = agentsOutput?.log_analysis?.log_analysis;
  const rootCause = agentsOutput?.root_cause?.root_cause;
  const runbook = agentsOutput?.runbook_steps?.runbook_steps;
  const plan = agentsOutput?.resolution_plan?.resolution_plan;

  const hasData = logAnalysis || rootCause || runbook || plan;

  if (!hasData) {
    return (
      <div className="border-b border-slate-800 px-3 py-2 text-xs text-slate-400">
        Run an incident query in <span className="font-semibold">Incident (Agents)</span> mode to see analysis here.
      </div>
    );
  }

  return (
    <div className="border-b border-slate-800 px-3 py-2 text-xs space-y-3">
      <div className="font-semibold text-[11px] uppercase tracking-wide text-slate-400">
        AI Incident Analysis
      </div>

      {logAnalysis && (
        <section>
          <div className="text-[11px] font-semibold text-slate-300 mb-1">
            Log Analysis
          </div>
          <pre className="whitespace-pre-wrap text-[11px] text-slate-200 bg-slate-900/60 border border-slate-800 rounded p-2">
            {logAnalysis}
          </pre>
        </section>
      )}

      {rootCause && (
        <section>
          <div className="text-[11px] font-semibold text-slate-300 mb-1">
            Root Cause Hypotheses
          </div>
          <pre className="whitespace-pre-wrap text-[11px] text-slate-200 bg-slate-900/60 border border-slate-800 rounded p-2">
            {rootCause}
          </pre>
        </section>
      )}

      {runbook && (
        <section>
          <div className="text-[11px] font-semibold text-slate-300 mb-1">
            Runbook Suggestions
          </div>
          <pre className="whitespace-pre-wrap text-[11px] text-slate-200 bg-slate-900/60 border border-slate-800 rounded p-2">
            {runbook}
          </pre>
        </section>
      )}

      {plan && (
        <section>
          <div className="text-[11px] font-semibold text-slate-300 mb-1">
            Resolution Plan
          </div>
          <pre className="whitespace-pre-wrap text-[11px] text-slate-200 bg-slate-900/60 border border-slate-800 rounded p-2">
            {plan}
          </pre>
        </section>
      )}
    </div>
  );
}
