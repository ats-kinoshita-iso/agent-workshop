---
name: trace-plan
description: >-
  Design a logging and tracing strategy for a system or agent pipeline. Use this
  skill when asked to "add observability", "design a logging strategy", "plan how
  to trace this system", or "what should I log in this agent".
---

# Trace Plan

Design a structured logging and distributed tracing strategy for the given system.

## Step 1: Understand the system boundaries

Read the system description and identify:
- **Entry points** — where requests or events enter the system
- **Exit points** — where responses or side effects leave the system
- **Internal components** — services, agents, tools, or functions that process data
- **External dependencies** — databases, APIs, LLMs, message queues

## Step 2: Choose a logging strategy

Select the appropriate logging approach based on system type:

| System type | Recommended strategy |
|-------------|---------------------|
| Single-process agent | Structured JSON logs to stdout/file |
| Multi-service pipeline | Distributed tracing (OpenTelemetry spans) |
| Long-running daemon | Rotating file logs + health-check endpoint |
| Serverless / ephemeral | Centralized log aggregation (CloudWatch, Datadog) |

## Step 3: Define trace boundaries

For each component identified in Step 1, define a **trace span**:

```
Span: <component name>
Parent: <parent span or "root">
Attributes to capture:
  - <key>: <description of value>
  - <key>: <description of value>
Events to record: <list of significant moments within this span>
Error conditions: <what constitutes a failed span>
```

## Step 4: Define log levels and their usage

Establish a consistent log-level policy:
- **DEBUG** — internal state changes, variable values, loop iterations (dev only)
- **INFO** — significant state transitions, request start/end, resource acquired
- **WARNING** — recoverable errors, retries, degraded mode
- **ERROR** — unrecoverable within the current operation, requires intervention
- **CRITICAL** — system-wide failures, data loss risk

## Step 5: Define structured log schema

Create a JSON schema for log entries to enable downstream filtering and aggregation:

```json
{
  "timestamp": "<ISO 8601>",
  "level": "<DEBUG|INFO|WARNING|ERROR|CRITICAL>",
  "component": "<span/service name>",
  "trace_id": "<UUID shared across a full request>",
  "span_id": "<UUID for this component's span>",
  "event": "<short machine-readable event name>",
  "message": "<human-readable description>",
  "attributes": {}
}
```

## Step 6: Identify critical paths to instrument first

Prioritize instrumentation by impact:
1. **Entry/exit of the outermost system boundary** — captures all traffic
2. **LLM API calls** — latency, token counts, model used, prompt hash
3. **Tool invocations** — tool name, inputs, outputs, duration
4. **Error paths** — every exception handler should emit a structured log

## Step 7: Output the tracing plan

Produce a Markdown document listing:
- All spans with their parent relationships (tree structure)
- Log schema with required and optional fields
- Instrumentation priority order (P1/P2/P3)
- Recommended library or framework (structlog, opentelemetry, etc.)
