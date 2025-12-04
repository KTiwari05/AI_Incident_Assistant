from abc import ABC, abstractmethod
from app.core.llm_client import LLMClient


class Agent(ABC):
    def __init__(self, llm: LLMClient):
        self.llm = llm

    @abstractmethod
    async def run(self, context: dict) -> dict:
        pass
