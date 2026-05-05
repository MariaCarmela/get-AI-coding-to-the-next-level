# ReasonCritique Agent — Assignment

## Objective

Design and implement a multi-agent system called **ReasonCritique** using Visual Studio Code Custom Agents. The system must produce a structured and verified analysis of a given technical text (e.g. documentation, implementation plan).

---

## Background

Visual Studio Code supports the creation of **custom AI agents** through `.agent.md` files, allowing developers to:

* Define agent behavior via system prompts
* Configure tools (e.g., `read`, `search`, `agent`)
* Compose multi-agent systems via subagents

Refer to the official documentation:
[https://code.visualstudio.com/docs/copilot/customization/custom-agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)

---

## Task Description

You must design and implement a **multi-agent system** called `ReasonCritique` that performs structured analysis of a given text.

⚠️ **Important:** The exact workflow is intentionally **not prescribed**. You are expected to design an appropriate architecture yourself.

Instead of following a fixed pipeline, you should justify your orchestration strategy through your design choices.

### Hints (Do NOT treat as requirements)

* Consider separating **generation** and **verification** responsibilities
* Think about whether different parts of the analysis could be **parallelized** (e.g., themes vs insights)
* Explore the use of an **orchestrator agent** that delegates tasks instead of performing them
* Reflect on trade-offs between:

  * Simplicity (sequential workflows)
  * Performance and robustness (parallel or modular workflows)

Your goal is to design a system that is:

* Modular
* Scalable
* Easy to reason about

---

## Requirements

### 1. Orchestrator Design

* Must define a **clear coordination strategy** between agents
* May use sequential, parallel, or hybrid workflows
* Must **not perform the core analysis itself**
* Must manage task delegation and data flow explicitly

### 2. Subagents

* Must define **at least two specialized agents**
* Agents should have **clear and distinct responsibilities**

The system must ultimately produce:

* Summary
* Themes
* Key Insights

Typical roles may include (non-mandatory):

* Generation
* Critique / Verification
* Specialized analyzers (optional)

### 3. Tool Usage

* Use only necessary tools
* Typical tools:

  * `read`
  * `search`
  * `agent`
* Avoid unnecessary tool inclusion

---

## Key Considerations

When designing your agents, consider:

* **Tool Minimization**: Include only required tools
* **Architectural Quality**:

  * Sequential pipelines are acceptable but not optimal
  * Modular and parallel designs are rewarded
* **Clear Role Separation**:

  * Orchestrator ≠ Analyst
* **Input Grounding**:

  * Always pass full original text where needed
* **Data Flow Integrity**:

  * Ensure consistency across agents
* **Failure Handling**:

  * System should tolerate imperfect intermediate outputs
* **Structured Output Enforcement**

---

## Deliverables

Create a zip file containing your `.agent.md` files. Use the `.agent.md` extension for all agent definition files.

Example submission structure:
```
ReasonCritique.agent.md      (orchestrator — required)
MyGenerator.agent.md         (subagent)
MyCritic.agent.md            (subagent)
```

- You must submit **at least 2 files** (orchestrator + at least one subagent)
- All files must use the `.agent.md` extension
- Do not include other file types

---

## Evaluation Criteria

Your implementation will be evaluated based on:

* Quality of orchestration design
* Level of modularization
* Use of parallel or advanced workflows
* Data flow integrity
* Output correctness
* Tool usage efficiency

---