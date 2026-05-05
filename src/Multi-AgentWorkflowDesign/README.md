# ReasonCritique — README

## Cos'è

**ReasonCritique** è un sistema multi-agente per Visual Studio Code che analizza un testo tecnico (documentazione, piani di implementazione, specifiche) e produce un'analisi strutturata e verificata composta da:

- **Summary** — riassunto conciso del testo
- **Themes** — temi principali identificati
- **Key Insights** — intuizioni chiave e implicazioni

---

## Architettura

Il sistema è composto da **5 agenti** (file `.agent.md`):

| File | Ruolo | Responsabilità |
|------|-------|----------------|
| `ReasonCritique.agent.md` | Orchestrator | Coordina il workflow, delega ai subagent, non genera contenuto |
| `Summarizer.agent.md` | Generatore di summary | Riceve il testo originale e produce un riassunto strutturato |
| `ThemeExtractor.agent.md` | Estrattore di temi | Identifica i macro-temi ricorrenti nel testo |
| `InsightExtractor.agent.md` | Estrattore di insights | Identifica implicazioni, conseguenze e intuizioni chiave |
| `Critic.agent.md` | Verificatore | Valida gli output contro il testo originale e produce l'output finale |

---

## Flusso di esecuzione

```
User Input (testo tecnico) → VARIABLE:ORIGINAL_TEXT
 │
 │  FASE 1 — Generazione (parallela)
 ├──→ @Summarizer        ← VARIABLE:ORIGINAL_TEXT
 ├──→ @ThemeExtractor    ← VARIABLE:ORIGINAL_TEXT
 ├──→ @InsightExtractor  ← VARIABLE:ORIGINAL_TEXT
 │
 │  FASE 2 — Verifica
 └──→ @Critic ← [ORIGINAL_TEXT + SUMMARY_OUTPUT + THEMES_OUTPUT + INSIGHTS_OUTPUT]
      │
      ├─ VERDICT:PASS  → Output finale restituito verbatim all'utente
      └─ VERDICT:REVISE → Re-dispatch agenti specifici (max 2 cicli, poi forced accept)
```

### Pattern implementati

- **Parallelismo**: i 3 agenti generativi lavorano in parallelo (sono indipendenti)
- **Conditional branching**: il Critic emette PASS o REVISE
- **Iterative verification**: fino a 2 cicli di revisione con termination condition esplicita
- **Error fallback**: se dopo 2 retry un agente non migliora, l'output viene accettato con nota
- **Explicit variable naming**: ogni dato è etichettato con prefisso `VARIABLE:`

---

## Prerequisiti

1. **Visual Studio Code** — versione aggiornata
2. **GitHub Copilot** — estensione installata e attiva
3. **GitHub Copilot Chat** — estensione installata e attiva
4. Abbonamento **GitHub Copilot** attivo (Individual, Business o Enterprise)

---

## Installazione

1. Scarica ed estrai il file ZIP
2. Nella **root** del tuo progetto/workspace, crea la seguente struttura:

```
tuo-progetto/
└── .github/
    └── agents/
        ├── ReasonCritique.agent.md
        ├── Summarizer.agent.md
        ├── ThemeExtractor.agent.md
        ├── InsightExtractor.agent.md
        └── Critic.agent.md
```

3. Apri il progetto in VS Code:

```bash
code tuo-progetto/
```

4. Se gli agenti non vengono riconosciuti, ricarica la finestra:
   - `Ctrl+Shift+P` → **Developer: Reload Window**

---

## Utilizzo

### 1. Apri la Copilot Chat

- Shortcut: `Ctrl+Shift+I` (Windows/Linux) o `Cmd+Shift+I` (Mac)
- Oppure: click sull'icona Copilot nella sidebar

### 2. Seleziona Agent Mode

Assicurati di essere in modalità **Agent** (non "Ask" o "Edit") — selezionabile dal dropdown in alto nella chat.

### 3. Invoca l'orchestrator

**Per analizzare un testo diretto:**
```
@ReasonCritique Analizza il seguente testo:

[incolla qui il testo tecnico da analizzare]
```

**Per analizzare un file nel workspace:**
```
@ReasonCritique Analizza il file docs/architecture.md
```

### 4. Output atteso

L'agente restituirà un'analisi strutturata nel formato:

```markdown
## Summary
[riassunto conciso del testo]

## Themes
[temi principali identificati con descrizione]

## Key Insights
[intuizioni chiave, implicazioni e consequences]
```

---

## Scelte di design

| Scelta | Motivazione |
|--------|-------------|
| Parallelismo in Fase 1 | Summary, temi e insights sono indipendenti → maggiore velocità |
| Critic separato | Separazione tra generazione e verifica → maggiore qualità |
| Retry con limite (max 2) | Robustezza senza rischio di loop infiniti |
| Orchestrator puro | Non produce contenuto → single responsibility principle |
| Variable naming esplicito | Tracciabilità completa del data flow tra agenti |
| Scope boundaries nei subagent | Ogni agente sa cosa È e cosa NON È nel suo dominio |

---

## Troubleshooting

| Problema | Soluzione |
|----------|-----------|
| Agenti non visibili nella chat | Verifica che i file siano in `.github/agents/` e ricarica la finestra |
| `@ReasonCritique` non riconosciuto | Assicurati di essere in Agent Mode, non Ask/Edit |
| Output incompleto | Prova con un testo più breve o riprova il comando |
| Copilot non risponde | Verifica che l'abbonamento Copilot sia attivo |
