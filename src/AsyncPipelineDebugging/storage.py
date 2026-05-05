import json
import os
import asyncio
import aiofiles

DB_FILE = "db.json"
lock = asyncio.Lock()  # Crea un lock globale

async def save_user(user):
 async with lock:  # Usa il lock per garantire l'accesso sicuro
  if not os.path.exists(DB_FILE):
   async with aiofiles.open(DB_FILE, "w") as f:  # Usa aiofiles per la scrittura asincrona
    await f.write(json.dumps({}))

  async with aiofiles.open(DB_FILE, "r") as f:
   db = json.loads(await f.read())

  db[str(user["id"])] = user

  async with aiofiles.open(DB_FILE, "w") as f:
   await f.write(json.dumps(db))