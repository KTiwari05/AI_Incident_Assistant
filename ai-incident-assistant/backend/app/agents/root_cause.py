from app.agents.base import Agent

SYSTEM_PROMPT = """
You are an expert in Root Cause Analysis for IT infrastructure.
Given user question, logs, and findings, propose 2-4 possible root causes.
Explain them concisely.
"""

class RootCauseAgent(Agent):
    async def run(self, context: dict):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""
User Query: {context.get('user_query')}
Log Analysis: {context.get('log_analysis')}
RAG Context: {context.get('rag_context')}
"""}]

        output = await self.llm.chat(messages)
        return {"root_cause": output}
