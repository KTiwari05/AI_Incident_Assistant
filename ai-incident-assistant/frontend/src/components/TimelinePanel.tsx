interface TimelinePanelProps {
  timelineText?: string;
}

export default function TimelinePanel({ timelineText }: TimelinePanelProps) {
  const events: string[] = timelineText
    ? timelineText
        .split("\n")
        .map((l) => l.trim())
        .filter((l) => l.length > 0)
    : [
        "t0: Waiting for first incident analysis…",
      ];

  return (
    <div className="h-full flex flex-col border-b border-slate-800">
      <div className="px-3 py-2 border-b border-slate-800 text-xs font-semibold uppercase tracking-wide text-slate-400">
        Incident Timeline
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2 text-xs">
        {events.map((item, idx) => (
          <div key={idx} className="flex gap-2">
            <div className="mt-[3px] h-2 w-2 rounded-full bg-blue-500" />
            <div className="text-slate-200">{item}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
