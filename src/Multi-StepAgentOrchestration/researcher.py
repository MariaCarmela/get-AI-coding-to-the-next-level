import os
from uuid import uuid4
from typing import Any

from a2a.types import AgentCapabilities, AgentCard, AgentSkill, Message, Part, TaskState, TaskStatus, TaskStatusUpdateEvent, TextPart
from a2a.server.agent_execution import AgentExecutor, RequestContext
from openai import AsyncOpenAI
from a2a.utils.errors import ServerError, UnsupportedOperationError

class ResearcherAgent(AgentExecutor):
    RESEARCHER_INSTRUCTIONS = """Role Selection
You are the Researcher Agent responsible for gathering relevant information about the client.

Role Introduction
Your tone should be professional and informative. You are expected to provide a comprehensive summary based on the client's context while adhering to the specified boundaries.

Context Provision
The input context you receive includes the client name. Use this information to research and find key facts, requirements, and risks associated with the client.

Task Presentation
Your task is to gather detailed information about the client and provide a concise, plain-text summary that can be used in the proposal.

Response Generation
The output should be a well-structured summary in plain text format that addresses the client's key aspects, such as name, location, and any relevant details discovered during your research.
"""

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.card = AgentCard(
            name="Researcher",
            url=os.environ.get("RESEARCHER_URL"),
            description="Client research agent that returns raw text.",
            version="1.0.0",
            capabilities=AgentCapabilities(streaming=False),
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            skills=[
                AgentSkill(
                    id="research_client",
                    name="Research client",
                    description="Researches a client and outputs plain text.",
                    tags=["research", "proposal", "rfp"],
                    examples=["Research NASA and summarize key facts, requirements, and risks."],
                )
            ],
        )

    async def _invoke(self, client_name: str) -> str:
        response = await self.openai_client.responses.create(
            model="gpt-5.2",
            instructions=self.RESEARCHER_INSTRUCTIONS,
            input=f"Research the client '{client_name}' and provide a concise plain-text summary.",
            tools=[{"type": "web_search"}]
        )
        return response.output_text

    async def execute(self, context: RequestContext, event_queue) -> None:
        client_name = context.get_user_input().strip()
        payload = await self._invoke(client_name)

        message = Message(
            message_id=uuid4().hex,
            role="agent",
            parts=[Part(root=TextPart(text=payload))],
        )

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                final=True,
                status=TaskStatus(
                    state=TaskState.completed,
                    message=message,
                ),
            )
        )

    async def cancel(self, context: RequestContext, event_queue) -> None:
        raise ServerError(error=UnsupportedOperationError())