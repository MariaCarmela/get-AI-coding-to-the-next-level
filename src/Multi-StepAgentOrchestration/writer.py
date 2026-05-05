import os
import json
from uuid import uuid4
from typing import override

from openai import AsyncOpenAI
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
    Message,
    Part,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils.errors import ServerError

from urls import WRITER_URL


WRITER_INSTRUCTIONS = """Role Selection
    You are the Writer Agent responsible for drafting the proposal text based on research findings.

    Role Introduction
    Your tone should be professional, persuasive, and clear. You are expected to take the research provided and create a well-structured proposal that meets the client's needs.

    Context Provision
    The input context you receive includes the research data, which contains key insights about the client. Use this information to inform your writing process.

    Task Presentation
    Your task is to draft a proposal based on the provided research. Ensure you cover all relevant points and present them in a logical order.

    Response Generation
    The output should be a polished proposal text in clear and professional language, formatted as plain text.
    """


class WriterAgent(AgentExecutor):

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.card = AgentCard(
            name="Writer",
            url=WRITER_URL,
            description="Proposal writer agent that drafts proposal text from provided research context.",
            version="1.0.0",
            capabilities=AgentCapabilities(streaming=False),
            default_input_modes=["text/plain"],
            default_output_modes=["text/plain"],
            skills=[
                AgentSkill(
                    id="draft_proposal",
                    name="Draft proposal",
                    description="Drafts proposal sections from orchestrator-provided context.",
                    tags=["proposal", "writer", "draft"],
                    examples=["Draft an executive summary for Nike from the provided research payload."],
                )
            ],
        )

    async def _invoke(self, payload: dict) -> str:
        response = await self.openai_client.responses.create(
            model="gpt-5.2",
            instructions=WRITER_INSTRUCTIONS,
            input=(
                "Draft an executive summary style proposal section using ONLY this JSON payload:\n"
                + json.dumps(payload, indent=2)
            ),
        )
        return response.output_text

    def _parse_payload(self, user_input: str) -> dict:
        try:
            data = json.loads(user_input)
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass

        return {
            "client_name": user_input.strip(),
            "research": None,
            "draft": None,
            "review": None,
            "processed": None,
        }

    @override
    async def execute(self, context: RequestContext, event_queue) -> None:
        payload = self._parse_payload(context.get_user_input())
        draft_text = await self._invoke(payload)

        message = Message(
            message_id=uuid4().hex,
            role="agent",
            parts=[Part(root=TextPart(text=draft_text))],
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

    @override
    async def cancel(self, context: RequestContext, event_queue) -> None:
        raise ServerError(error=UnsupportedOperationError())
    