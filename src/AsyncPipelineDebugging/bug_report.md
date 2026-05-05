# Bug Report

## Bug 1: Chiamate Sincrone
- **Tipo**: Async
- **Effetto**: Il sistema si blocca durante l'enrichment degli utenti a causa dell'uso di `time.sleep(0.2)`, che interrompe il loop di eventi.
- **Fix**: Sostituito `time.sleep(0.2)` con `await asyncio.sleep(0.2)` in `ai_client.py`, permettendo al loop di eventi di gestire altre operazioni durante l'attesa.

## Bug 2: Sicurezza delle Operazioni di I/O
- **Tipo**: Async / I/O
- **Effetto**: L'accesso al file `db.json` era soggetto a condizioni di corsa, poiché le operazioni di scrittura bloccavano il loop di eventi. Questo poteva portare a stati incoerenti durante le scritture simultanee.
- **Fix**: Implementata la scrittura sicura utilizzando `asyncio.Lock()` per garantire che solo un'operazione di scrittura possa avvenire alla volta, prevenendo conflitti durante l'accesso concorrente al file.

## Bug 3: Mappatura Errata dell'API
- **Tipo**: Logic
- **Effetto**: I campi restituiti dall'API non venivano mappati correttamente, in particolare l'uso del campo `mail` anziché `email`.
- **Fix**: Corretto il campo email in `enrich_user` per utilizzare `user['email']`, garantendo la corretta rappresentazione dei dati utente.

## Bug 4: Sicurezza dei Dati
- **Tipo**: Data
- **Effetto**: La scrittura su `db.json` non era sicura in un contesto concorrente, portando a potenziali perdite di dati durante scritture simultanee.
- **Fix**: Utilizzato un lock per garantire l'accesso esclusivo alle operazioni di scrittura su `db.json`, impedendo conflitti e garantendo l'integrità dei dati.

## Bug 5: Comportamento Indeterministico
- **Tipo**: Architecture
- **Effetto**: Risultati non prevedibili a causa di condizioni di corsa quando più coroutine tentavano di scrivere nello stesso file contemporaneamente.
- **Fix**: Implementato `asyncio.Lock()` per garantire che tutte le operazioni di scrittura siano gestite in modo deterministico, evitando conflitti tra scritture concorrenti.