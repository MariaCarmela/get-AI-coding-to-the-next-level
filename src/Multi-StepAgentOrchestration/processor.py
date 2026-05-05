import json
from pathlib import Path
from typing import Any, override
from uuid import uuid4

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

from urls import PROCESSOR_URL


class ProcessorAgent(AgentExecutor):

	def __init__(self):
		self.card = AgentCard(
			name="Processor",
			url=PROCESSOR_URL,
			description="Converts proposal state into a PDF artifact.",
			version="1.0.0",
			capabilities=AgentCapabilities(streaming=True),
			default_input_modes=["text/plain"],
			default_output_modes=["text/plain"],
			skills=[
				AgentSkill(
					id="process_proposal",
					name="Process proposal",
					description="Builds a proposal PDF from draft/review content.",
					tags=["processor", "proposal", "pdf"],
				)
			],
		)

	def _parse_payload(self, user_input: str) -> dict[str, Any]:
		try:
			data = json.loads(user_input)
			if isinstance(data, dict):
				return data
		except json.JSONDecodeError:
			pass

		return {
			"client_name": user_input.strip(),
			"draft": None,
		}

	def _extract_text(self, field: Any) -> str:
		if isinstance(field, str):
			return field
		if not isinstance(field, dict):
			return ""

		try:
			return field["result"]["status"]["message"]["parts"][0]["text"]
		except (KeyError, IndexError, TypeError):
			return ""

	def _build_pdf(self, client_name: str, proposal_text: str, filename: str) -> str:
		from reportlab.lib.pagesizes import letter
		from reportlab.lib.styles import getSampleStyleSheet
		from reportlab.lib.units import inch
		from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

		doc = SimpleDocTemplate(
			filename,
			pagesize=letter,
			topMargin=0.75 * inch,
			bottomMargin=0.75 * inch,
			leftMargin=0.75 * inch,
			rightMargin=0.75 * inch,
		)

		styles = getSampleStyleSheet()
		story = [
			Paragraph(f"Proposal: {client_name}", styles["Heading1"]),
			Spacer(1, 0.2 * inch),
			Paragraph("Draft", styles["Heading2"]),
			Paragraph((proposal_text or "[TBD: draft missing]").replace("\n", "<br/>"), styles["BodyText"]),
		]
		doc.build(story)
		return filename

	@override
	async def execute(self, context: RequestContext, event_queue) -> None:
		payload = self._parse_payload(context.get_user_input())
		client_name = str(payload.get("client_name") or "unknown-client").strip()
		draft_text = self._extract_text(payload.get("draft"))

		safe_name = "".join(ch if ch.isalnum() else "_" for ch in client_name).strip("_") or "proposal"
		filename = str(Path.cwd() / f"{safe_name}_proposal.pdf")

		try:
			output_file = self._build_pdf(client_name, draft_text, filename)
			result = {"ok": True, "filename": output_file}
		except Exception as exc:
			result = {"ok": False, "error": str(exc)}

		message = Message(
			message_id=uuid4().hex,
			role="agent",
			parts=[Part(root=TextPart(text=json.dumps(result)))],
		)

		await event_queue.enqueue_event(
			TaskStatusUpdateEvent(
				task_id=context.task_id,
				context_id=context.context_id,
				final=True,
				status=TaskStatus(state=TaskState.completed, message=message),
			)
		)

	@override
	async def cancel(self, context: RequestContext, event_queue) -> None:
		raise ServerError(error=UnsupportedOperationError())
