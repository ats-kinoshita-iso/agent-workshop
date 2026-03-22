---
name: instrument-code
description: >-
  Add structured log points and trace spans to existing code. Use this skill
  when asked to "instrument this function", "add logging to this module",
  "add tracing to this pipeline", or "make this code observable".
---

# Instrument Code

Add structured logging and distributed tracing instrumentation to existing code.

## Step 1: Read the existing code

Read the target file(s) and identify:
- **Functions or methods** that are entry points (called from outside this module)
- **Loop boundaries** and conditional branches that affect control flow
- **External calls** — network requests, database queries, LLM API calls, subprocess runs
- **Error handlers** — try/except or equivalent blocks

## Step 2: Select the instrumentation library

Choose based on the project's existing dependencies:

| Language | Recommended library | Install command |
|----------|--------------------|-----------------|
| Python   | `structlog`        | `uv add structlog` |
| Python   | `opentelemetry-sdk`| `uv add opentelemetry-sdk opentelemetry-exporter-otlp` |
| TypeScript | `pino`           | `bun add pino` |
| TypeScript | `@opentelemetry/sdk-node` | `bun add @opentelemetry/sdk-node` |

If the project already imports a logging library, use that — do not add a second one.

## Step 3: Add span wrappers to entry points

For each external-facing function, wrap the body in a trace span:

```python
# Python (structlog + opentelemetry)
import structlog
from opentelemetry import trace

logger = structlog.get_logger(__name__)
tracer = trace.get_tracer(__name__)

def process_request(payload: dict) -> dict:
    with tracer.start_as_current_span("process_request") as span:
        span.set_attribute("payload.size", len(str(payload)))
        logger.info("process_request.start", payload_keys=list(payload.keys()))
        result = _do_work(payload)
        logger.info("process_request.end", result_keys=list(result.keys()))
        return result
```

## Step 4: Add INFO logs at significant state transitions

Insert log statements at:
- **Function entry** with key input attributes (not full payloads — avoid logging secrets)
- **Significant checkpoints** (e.g., "cache miss — fetching from API")
- **Function exit** with key output attributes (size, count, status code)

Keep log messages machine-readable: use `event="snake_case_name"` as the primary key.

## Step 5: Add WARNING/ERROR logs at exception handlers

For every except/catch block, emit a structured error log:

```python
except SomeError as exc:
    logger.error(
        "process_request.failed",
        error=str(exc),
        error_type=type(exc).__name__,
        exc_info=True,
    )
    raise
```

## Step 6: Add metrics at hot paths

For loops and repeated external calls, record timing and counts:

```python
import time

start = time.perf_counter()
result = call_llm_api(prompt)
duration_ms = (time.perf_counter() - start) * 1000
logger.info("llm_call.complete", duration_ms=round(duration_ms, 1), tokens=result.usage.total_tokens)
```

## Step 7: Verify instrumentation does not break tests

Run the test suite after adding instrumentation:
- Confirm that log output does not break assertions on stdout
- Verify span context propagates correctly across async boundaries
- Check that sensitive fields (API keys, PII) are not logged

## Step 8: Present the diff

Output the instrumented code as a unified diff, keeping changes minimal.
Avoid restructuring logic — instrumentation should be additive only.
