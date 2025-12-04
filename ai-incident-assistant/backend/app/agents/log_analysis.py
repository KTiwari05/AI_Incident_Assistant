from app.agents.base import Agent

SYSTEM_PROMPT = """
You are an Infrastructure Log Analysis Expert.
Analyze logs, alerts, metrics and extract:

- anomalies
- failing components
- symptoms
- any patterns
Return output in a clear bullet-point format.
"""

class LogAnalysisAgent(Agent):
    async def run(self, context: dict):
        logs = context.get("logs", "")
        user_query = context.get("user_query", "")

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"User query: {user_query}\nLogs:\n{logs}"}
        ]

        output = await self.llm.chat(messages)
        return {"log_analysis": output}
