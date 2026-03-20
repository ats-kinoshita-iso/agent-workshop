---
name: agent-plan
description: >-
  Decompose a task into an orchestrator and worker architecture. Use this skill
  when asked to "plan an agent", "design a multi-agent system", "break down this
  task for agents", or any request that involves delegating work across multiple
  Claude instances or tool-calling pipelines.
---

# Agent Plan

Decompose the given task into an **orchestrator + worker** multi-agent architecture.

## Step 1: Understand the task

Read the task description and identify:
- The **end goal** (what does success look like?)
- The **inputs** available at the start
- The **outputs** required at the end
- Natural **subtask boundaries** (steps that could run independently or in sequence)

## Step 2: Design the orchestrator

The orchestrator is responsible for:
- Accepting the top-level task and breaking it into subtasks
- Dispatching subtasks to workers in the right order (sequential or parallel)
- Collecting worker results and aggregating them
- Handling worker failures (retry, fallback, or escalate)

Define the orchestrator's interface:
```
Orchestrator Input:  <describe the input schema>
Orchestrator Output: <describe the output schema>
State managed:       <list what the orchestrator tracks>
```

## Step 3: Define workers

For each subtask, define a worker with a **narrow scope**:

```
Worker: <name>
Input:  <what it receives from the orchestrator>
Output: <what it returns to the orchestrator>
Scope:  <one sentence describing exactly what it does>
Can run in parallel with: <list other workers or "none">
```

Principles for good workers:
- Each worker does exactly ONE thing well.
- Workers are stateless -- all context comes from the orchestrator.
- Workers communicate through structured outputs (JSON preferred over free text).
- Workers should not call other workers directly -- route through the orchestrator.

## Step 4: Sequence diagram

Produce a text-based sequence diagram showing the message flow:

```
User -> Orchestrator: <task>
Orchestrator -> Worker A: <subtask 1>
Worker A -> Orchestrator: <result 1>
Orchestrator -> Worker B: <subtask 2>  (can run after step 1, or in parallel)
Worker B -> Orchestrator: <result 2>
Orchestrator -> User: <final output>
```

## Step 5: Error handling plan

For each worker, define what the orchestrator should do if the worker fails:
- **Retry**: re-send the same input (for transient errors)
- **Fallback**: use an alternative worker or simplified approach
- **Escalate**: return an error to the user with context

## Step 6: Present the plan

Summarize the architecture as a concise table:

| Component | Role | Input | Output | Parallelizable |
|-----------|------|-------|--------|----------------|
| Orchestrator | ... | ... | ... | N/A |
| Worker A | ... | ... | ... | Yes/No |
| Worker B | ... | ... | ... | Yes/No |

Ask the user to confirm the decomposition before implementation begins.
