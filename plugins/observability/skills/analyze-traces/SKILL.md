---
name: analyze-traces
description: >-
  Parse and interpret trace logs from a running system to diagnose latency,
  errors, and bottlenecks. Use this skill when asked to "analyze these logs",
  "find the bottleneck", "debug this trace", or "interpret these spans".
---

# Analyze Traces

Parse structured trace logs or span data and produce a diagnostic report.

## Step 1: Load and parse the trace data

Read the trace input and identify its format:
- **OpenTelemetry OTLP JSON** — list of spans with `trace_id`, `span_id`, `parent_span_id`
- **Structured JSON logs** — newline-delimited records with `timestamp`, `level`, `event`
- **Plain text logs** — parse timestamps and log levels with regex patterns

Extract a list of spans. For each span, record:
- `span_id`, `parent_span_id`, `component` (service/function name)
- `start_time`, `end_time`, `duration_ms`
- `status` (OK / ERROR), `error_message` if present
- Key attributes relevant to the operation

## Step 2: Reconstruct the execution tree

Build a tree of spans using `parent_span_id` links. Print the tree to show call nesting:

```
[root] process_request          200ms  OK
  [1]  validate_input             5ms  OK
  [2]  fetch_context             80ms  OK
    [2a] cache_lookup              2ms  MISS
    [2b] api_fetch                78ms  OK
  [3]  call_llm                 110ms  OK
  [4]  format_response            5ms  OK
```

Identify the **critical path** — the chain of spans with no parallelism that determines total latency.

## Step 3: Identify latency hotspots

Sort spans by `duration_ms` descending. Flag any span that:
- Consumes > 20% of total trace duration
- Has duration > 2 standard deviations above the mean for its component type
- Shows significant variance across multiple trace samples

Report hotspots with:
- Component name and average duration
- Whether it is on the critical path
- Suggested investigation (e.g., "check for N+1 queries", "consider caching", "review LLM prompt length")

## Step 4: Detect errors and anomalies

Scan for spans with `status=ERROR` or log records with `level=ERROR` or `level=CRITICAL`:
- List each error with its component, timestamp, and message
- Check whether the error is isolated or cascading (did it cause parent spans to fail?)
- Identify retry storms — the same operation failing and retrying many times

## Step 5: Analyze throughput and concurrency

If multiple trace samples are provided:
- Compute **requests per second** (RPS) from trace timestamps
- Identify **concurrent span execution** — spans whose time ranges overlap
- Check for **resource contention** — components serializing when they could run in parallel

## Step 6: Generate the diagnostic report

Produce a Markdown report:

```markdown
## Trace Analysis Report

**Traces analyzed**: <count>
**Time range**: <start> to <end>
**Total duration (median)**: <Xms>

### Critical Path
<tree diagram>

### Top Latency Hotspots
| Rank | Component | Avg Duration | % of Total | On Critical Path |
|------|-----------|-------------|------------|-----------------|
| 1    | call_llm  | 110ms       | 55%        | YES             |

### Errors Detected
| Component | Count | Message (sample) |
|-----------|-------|-----------------|
| api_fetch |   3   | timeout after 5s |

### Recommendations
1. <highest impact action>
2. <second action>
3. <third action>
```

## Step 7: Suggest next instrumentation steps

Based on gaps found during analysis, list any spans or log points that are missing
and would improve future diagnosis. Use `/instrument-code` to add them.
