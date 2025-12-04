export interface AgentsOutput {
  log_analysis?: { log_analysis: string };
  root_cause?: { root_cause: string };
  runbook_steps?: { runbook_steps: string };
  resolution_plan?: { resolution_plan: string };
  timeline?: { timeline: string };
  final_answer?: { final_answer: string };
}
