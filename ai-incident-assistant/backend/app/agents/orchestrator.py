from app.core.llm_client import LLMClient
from app.agents.log_analysis import LogAnalysisAgent
from app.agents.root_cause import RootCauseAgent
from app.agents.runbook import RunbookAgent
from app.agents.planner import ResolutionPlannerAgent
from app.agents.timeline import TimelineAgent
from app.agents.presenter import PresenterAgent


class Orchestrator:
    def __init__(self, model: str = "gpt-4o"):
        self.llm = LLMClient(model=model)
        self.log_agent = LogAnalysisAgent(self.llm)
        self.root_agent = RootCauseAgent(self.llm)
        self.runbook_agent = RunbookAgent(self.llm)
        self.planner_agent = ResolutionPlannerAgent(self.llm)
        self.timeline_agent = TimelineAgent(self.llm)
        self.presenter_agent = PresenterAgent(self.llm)

    async def handle(self, context: dict) -> dict:
        # 1) Log analysis
        log_out = await self.log_agent.run(context)
        context.update(log_out)

        # 2) Root cause analysis
        root_out = await self.root_agent.run(context)
        context.update(root_out)

        # 3) Runbook steps
        runbook_out = await self.runbook_agent.run(context)
        context.update(runbook_out)

        # 4) Resolution plan
        plan_out = await self.planner_agent.run(context)
        context.update(plan_out)

        # 5) Timeline
        timeline_out = await self.timeline_agent.run(context)
        context.update(timeline_out)

        # 6) Final answer for the user
        presenter_out = await self.presenter_agent.run(context)
        context.update(presenter_out)

        return {
            "log_analysis": log_out,
            "root_cause": root_out,
            "runbook_steps": runbook_out,
            "resolution_plan": plan_out,
            "timeline": timeline_out,
            "final_answer": presenter_out,
        }
