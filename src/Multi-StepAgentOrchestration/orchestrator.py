import json
from dataclasses import dataclass
from typing import Any
from uuid import uuid4
import httpx
import asyncio

from a2a.client.legacy import A2AClient
from a2a.types import (
    Message,
    MessageSendParams,
    Part,
    SendMessageRequest,
    TextPart,
)
from models import ProposalPhase
from urls import PROCESSOR_URL, RESEARCHER_URL, WRITER_URL

@dataclass
class ProposalContext:
    client_name: str
    research: dict[str, Any] | None = None
    draft: dict[str, Any] | None = None
    processed: dict[str, Any] | None = None

async def make_client(url: str) -> A2AClient:
    httpx_client = httpx.AsyncClient(timeout=300)
    return A2AClient(httpx_client=httpx_client, url=url)

async def send_message(client: A2AClient, text: str) -> dict[str, Any]:
    msg = Message(
        message_id=uuid4().hex,
        role="user",
        parts=[Part(root=TextPart(text=text))],
    )
    req = SendMessageRequest(
        id=uuid4().hex,
        params=MessageSendParams(message=msg),
    )
    try:
        resp = await client.send_message(req)
        return resp.model_dump(mode="json", exclude_none=True)
    except Exception as e:
        print(f"Error sending message: {e}")
        return {}

def _build_phase_input(ctx: ProposalContext, phase: ProposalPhase) -> str:
    if phase == ProposalPhase.RESEARCHED:
        return ctx.client_name

    payload = {
        "client_name": ctx.client_name,
        "phase": phase,
        "research": ctx.research,
        "draft": ctx.draft,
        "processed": ctx.processed,
    }
    return json.dumps(payload)

PHASE_URLS: dict[ProposalPhase, str] = {
    ProposalPhase.RESEARCHED: RESEARCHER_URL,
    ProposalPhase.DRAFTED: WRITER_URL,
    ProposalPhase.PROCESSED: PROCESSOR_URL,
}

PHASE_SEQUENCE: tuple[ProposalPhase, ...] = (
    ProposalPhase.RESEARCHED,
    ProposalPhase.DRAFTED,
    ProposalPhase.PROCESSED,
)

def resolve_phase_url(phase: ProposalPhase) -> str:
    return PHASE_URLS[phase]

async def run_phase(ctx: ProposalContext, phase: ProposalPhase) -> None:
    phase_url = resolve_phase_url(phase)
    client = await make_client(phase_url)
    response = await send_message(client, _build_phase_input(ctx, phase))

    # Persist the response into the correct ProposalContext field.
    if phase == ProposalPhase.RESEARCHED:
        ctx.research = response
    elif phase == ProposalPhase.DRAFTED:
        ctx.draft = response
    elif phase == ProposalPhase.PROCESSED:
        ctx.processed = response

async def run_bid_proposal(
    client_name: str,
    phase: ProposalPhase = ProposalPhase.PROCESSED,
) -> ProposalContext:
    ctx = ProposalContext(client_name=client_name)

    # Trova l'indice della fase target
    target_index = PHASE_SEQUENCE.index(phase)

    # Esegui tutte le fasi fino e inclusa la fase target
    for i in range(target_index + 1):
        await run_phase(ctx, PHASE_SEQUENCE[i])

    return ctx

if __name__ == "__main__":
    client_name = "Rolls Royce"  # Esempio di nome cliente
    target_phase = ProposalPhase.PROCESSED  # Esempio di fase target
    asyncio.run(run_bid_proposal(client_name, target_phase))