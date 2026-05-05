# A2A Bid Proposal Exercise

## Problem Statement
You are building a multi-agent bid proposal pipeline.
Each agent has a single responsibility:
- **Researcher**: gather client context.
- **Writer**: draft proposal text using prior research.
- **Processor**: produce a final artifact (PDF metadata/output).

The system already has working agent servers. What is missing is robust orchestration logic that calls agents in the correct order and passes shared state across phases.

## Goal
Implement a clean multi-agent flow:
- `RESEARCHED -> DRAFTED -> PROCESSED`
- Shared state is passed by orchestrator (not by direct agent-to-agent calls)

## Task 1: Implement the Orchestrator
Implement the orchestrator in `orchestrator.py` so it:
1. Maintains a shared `ProposalContext` state object.
2. Runs phases in sequence (`RESEARCHED -> DRAFTED -> PROCESSED`) up to a target phase.
3. Sends the correct payload to each phase:
	- Research phase receives raw `client_name`.
	- Downstream phases receive serialized proposal state.
4. Stores each phase response back into context (`research`, `draft`, `processed`).

## Task 2: Add Role-Based Prompting
In both `researcher.py` and `writer.py`, write the system prompt from scratch using this exact structure:

1. **Role Selection**
2. **Role Introduction**
3. **Context Provision**
4. **Task Presentation**
5. **Response Generation**

## Implementation Guidelines
- Do **not** call one agent directly from inside another agent.
- Orchestration decisions belong in the orchestrator only.
- Keep implementation minimal and readable.
- Avoid adding new features not required by the phase flow.
- Keep all five role-based sections explicitly labeled in both prompts.
- Do not invent data outside provided inputs/context.

## Expected Behavior
Given `client_name="Rolls Royce"` and target phase `PROCESSED`:
- Researcher is called first.
- Writer is called second, with research data in payload.
- Processor is called last, with draft data in payload.
- Returned context contains non-null `research`, `draft`, and `processed`.

## Acceptance Criteria
- `run_bid_proposal(client_name, phase=...)` executes all required phases in order.
- `run_phase(...)` routes calls using the phase-to-agent mapping.
- Payload generation is phase-aware.
- Client can run once and receive full context for the target phase.
- Researcher and writer prompts include all five required role-based sections.

## Suggested Incremental Steps
1. Implement `run_phase` and response assignment.
2. Add phase sequence and run-up-to-target loop.
3. Add payload builder for phase-specific inputs.
4. Validate end-to-end with the running server + client.

## Optional Hints
- Hint 1: Use a tuple/list to define phase order once.
- Hint 2: Build payload from context, not from scratch each time.
- Hint 3: Keep the research phase input special-cased as plain text.

## Run the Project
### Start servers
`python main.py`

### Run client
`python client.py <client_name>`

### Run evaluator
`python evaluate_task.py`

## Evaluator Checks
The evaluator verifies:
- dependency installation via `pip install -r requirements.txt`,
- `OPENAI_API_KEY` environment presence,
- orchestrator sequencing/persistence,
- role-based prompt section structure and prompt quality,
- and end-to-end server/client execution.

## Submission Format

Create a zip file containing exactly these 3 files:

```
orchestrator.py
researcher.py
writer.py
```

- **`orchestrator.py`** — your completed orchestrator with phase sequencing and response persistence
- **`researcher.py`** — the researcher agent with your complete role-based system prompt (all 5 sections filled in, no TODO/placeholder text)
- **`writer.py`** — the writer agent with your complete role-based system prompt (all 5 sections filled in, no TODO/placeholder text)

Do not include other project files (`processor.py`, `main.py`, `client.py`, etc.) — only the 3 files listed above.

## Notes
- If ports are already in use, stop old processes before running `main.py`.
- Ensure `OPENAI_API_KEY` is set in your environment.


## Execution
Run the command:
```
python main.py # For the server
python client.py "Rolls Royce" #For the client