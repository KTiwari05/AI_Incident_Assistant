import time
from asyncio import to_thread
from openai import OpenAI

from app.core.config import settings
from app.core.db import async_session
from app.models.db_models import LLMCall


class LLMClient:
    def __init__(self, model: str | None = None):
        self.model = model or settings.OPENAI_MODEL
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
        )

    async def chat(self, messages, temperature: float = 0.1):
        """
        Call OpenAI chat + log basic performance metrics into llm_calls.
        """
        # simple char-length proxy for tokens
        prompt_chars = sum(len(m.get("content", "")) for m in messages)

        start = time.perf_counter()
        error_text = None
        completion_text = ""
        success = True

        def _call():
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
            return completion.choices[0].message.content

        try:
            completion_text = await to_thread(_call)
        except Exception as e:
            success = False
            error_text = str(e)
            raise
        finally:
            latency_ms = (time.perf_counter() - start) * 1000.0
            completion_chars = len(completion_text)

            # fire-and-forget style logging (but we still await since we're in async)
            async with async_session() as db:
                call = LLMCall(
                    model=self.model,
                    latency_ms=latency_ms,
                    prompt_chars=prompt_chars,
                    completion_chars=completion_chars,
                    success=success,
                    error=error_text,
                )
                db.add(call)
                await db.commit()

        return completion_text
