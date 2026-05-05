import asyncio
import time
import random
from decimal import Decimal

async def enrich_user(user: dict):
    await asyncio.sleep(0.2)  # Usa asyncio.sleep invece di time.sleep
    profile = {
        "id": user["id"],
        "name": user["name"],
        "summary": f"{user['name']} is a user from {user['address']['city']} with email {user['email']}",
        "score": random.random() * 100
    }
    return profile