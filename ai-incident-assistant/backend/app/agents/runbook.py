from app.agents.base import Agent

SYSTEM_PROMPT = """
You are a Runbook Advisor for production incidents.
Use the provided RAG context (KB documents).
Extract the most relevant steps or procedures.
Keep steps short and practical.
"""

class RunbookAgent(Agent):
    async def run(self, context: dict):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"RAG Context:\n{context.get('rag_context')}"}
        ]

        output = await self.llm.chat(messages)
        return {"runbook_steps": output}
