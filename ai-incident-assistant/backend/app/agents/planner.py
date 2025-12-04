from app.agents.base import Agent

SYSTEM_PROMPT = """
You are an Incident Resolution Planner.
Generate a step-by-step actionable plan combining:
- log analysis
- root cause findings
- runbook steps
Plan must be short, executable, and ordered.
"""

class ResolutionPlannerAgent(Agent):
    async def run(self, context: dict):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
Root Causes: {context.get('root_cause')}
Runbook Steps: {context.get('runbook_steps')}
Log Analysis: {context.get('log_analysis')}
"""}
        ]
        output = await self.llm.chat(messages)
        return {"resolution_plan": output}
