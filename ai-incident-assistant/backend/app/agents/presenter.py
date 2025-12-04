from app.agents.base import Agent

SYSTEM_PROMPT = """
You are an experienced Site Reliability Engineer (SRE) helping a teammate in chat.

You receive:
- user query
- log analysis
- possible root causes
- relevant runbook steps
- a proposed resolution plan
- an incident timeline

Your job:
1. Respond in natural language like a senior engineer in Slack.
2. Start with a short, plain-English explanation of what's likely going on.
3. Then, only if it makes sense, include a concise numbered list of recommended actions.
4. Avoid over-formal structure, no headings like 'Root Cause', 'Timeline' unless the user asked for a report.
5. Do NOT mention 'agents', 'prompts', or internal system details.
"""

class PresenterAgent(Agent):
    async def run(self, context: dict):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
User Query:
{context.get('user_query')}

Log Analysis:
{context.get('log_analysis')}

Root Cause Hypotheses:
{context.get('root_cause')}

Runbook Suggestions:
{context.get('runbook_steps')}

Resolution Plan:
{context.get('resolution_plan')}

Timeline:
{context.get('timeline')}
"""}
        ]
        output = await self.llm.chat(messages)
        return {"final_answer": output}
