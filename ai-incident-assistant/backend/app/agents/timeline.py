from app.agents.base import Agent

SYSTEM_PROMPT = """
You are an Incident Timeline Generator.
Using all provided context, generate a simple chronological timeline.

Format:
- t0: event
- t1: event
- t2: event

Keep it short and clear.
"""

class TimelineAgent(Agent):
    async def run(self, context: dict):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
User Query: {context.get('user_query')}
Log Analysis: {context.get('log_analysis')}
Root Cause: {context.get('root_cause')}
Resolution Plan: {context.get('resolution_plan')}
"""}
        ]

        output = await self.llm.chat(messages)
        return {"timeline": output}
