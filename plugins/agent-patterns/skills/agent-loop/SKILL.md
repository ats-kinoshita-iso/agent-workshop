---
name: agent-loop
description: >-
  Design and run a self-improving evaluator/optimizer loop. Use this skill when
  asked to "set up an eval loop", "build an optimizer", "improve this output iteratively",
  or "create a generate-evaluate-improve cycle" for any agent output.
---

# Agent Loop

Design and execute a **generate -> evaluate -> improve -> repeat** loop that
iteratively refines an agent output until a quality threshold is met.

## Loop structure

```
[Generator] --> output --> [Evaluator] --> score + feedback
                                              |
                               score >= threshold? --> YES --> done
                                              |
                                             NO
                                              |
                                         [Optimizer] --> improved prompt
                                              |
                                         [Generator] --> new output
```

## Step 1: Define the goal and threshold

Before starting the loop, specify:
- **Task**: what the generator should produce
- **Quality threshold**: the minimum acceptable score (e.g., 4.0/5.0)
- **Max iterations**: upper bound to prevent infinite loops (recommended: 5)
- **Evaluation criteria**: the specific dimensions to score (use `/agent-review` criteria)

## Step 2: Set up the generator

Define the initial generation prompt:
```
System: <system prompt for the generator>
User:   <task description>
```

The generator should produce a **single, structured output** per run.
Avoid generating lists of alternatives -- the evaluator handles iteration.

## Step 3: Set up the evaluator

The evaluator scores the generator's output and produces structured feedback:

```json
{
  "score": 3.5,
  "passed": false,
  "issues": [
    "Issue description 1",
    "Issue description 2"
  ],
  "suggestions": [
    "Specific improvement 1",
    "Specific improvement 2"
  ]
}
```

The evaluator must be **deterministic** about scoring criteria -- define them
explicitly before starting the loop.

## Step 4: Set up the optimizer

The optimizer receives the current prompt and evaluator feedback, and produces
an improved prompt for the next generator run:

```
Previous prompt: <current generator prompt>
Evaluator score: <score>
Issues found:    <list of issues>
Suggestions:     <list of suggestions>

Produce an improved generator prompt that addresses these issues.
```

## Step 5: Run the loop

Execute iterations until the threshold is met or max iterations reached:

```
Iteration 1:
  Generator output: <output>
  Evaluator score:  <score> / 5.0
  Passed threshold: Yes/No
  Issues:           <issues if any>

Iteration 2 (if needed):
  Improved prompt:  <what changed>
  Generator output: <new output>
  Evaluator score:  <new score>
  Passed threshold: Yes/No

Final result: <the output that passed, or the best output if max iterations reached>
```

## Step 6: Report

After the loop completes, provide:
1. **Final output**: the best result produced
2. **Score progression**: how the score improved across iterations
3. **Key improvements**: what changes made the biggest difference
4. **Convergence status**: whether the threshold was met or the loop timed out
