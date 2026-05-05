import asyncio
from ai_client import enrich_user
from storage import save_user
import aiohttp

API_URL = "https://jsonplaceholder.typicode.com/users"

async def fetch_users():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            data = await resp.json()
            return data

async def pipeline():
    users = await fetch_users()  # Aggiungi await qui
    tasks = []

    for u in users:
        tasks.append(process_user(u))

    results = await asyncio.gather(*tasks)
    print("Processed users:", len(results))

async def process_user(user):
    enriched = await enrich_user(user)  # Aggiungi await qui
    await save_user(enriched)
    return enriched

if __name__ == "__main__":
    asyncio.run(pipeline())