import asyncio
import uvicorn

from dotenv import load_dotenv
import os

load_dotenv()  # Carica le variabili dal file .env
api_key = os.getenv("OPENAI_API_KEY")  # Usa la chiave API

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore

from processor import ProcessorAgent
from researcher import ResearcherAgent
from writer import WriterAgent

def build_agent_app(agent_executor):
    handler = DefaultRequestHandler(agent_executor=agent_executor, task_store=InMemoryTaskStore())

    server = A2AStarletteApplication(
        agent_card=agent_executor.card,
        http_handler=handler,
    )
    return server.build()

AGENTS = [
    (ResearcherAgent, 8001),
    (WriterAgent, 8002),
    (ProcessorAgent, 8003),
]

async def serve(app, port: int):
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    apps_and_ports = [
        (build_agent_app(agent_cls()), port)
        for agent_cls, port in AGENTS
    ]
    await asyncio.gather(*(serve(app, port) for app, port in apps_and_ports))

if __name__ == "__main__":
    asyncio.run(main())
