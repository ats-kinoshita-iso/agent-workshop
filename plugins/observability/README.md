# observability

Observability skills for designing tracing strategies, instrumenting existing code
with structured log points, and analyzing trace logs to diagnose production issues.

## Skills

### `/trace-plan`

Design a **logging and distributed tracing strategy** for a system or agent pipeline.
Produces a span tree, structured log schema, log-level policy, and a prioritized list
of what to instrument first. Works with any language or framework.

### `/instrument-code`

Add **structured log points and trace spans** to existing code — minimally and
additively, without restructuring logic. Covers structlog, OpenTelemetry, pino, and
other popular libraries. Includes guidance on avoiding PII leakage and keeping tests green.

### `/analyze-traces`

Parse structured trace or log data and produce a **diagnostic report** covering latency
hotspots, critical path analysis, error cascades, concurrency issues, and ranked
recommendations. Works with OTLP JSON, newline-delimited JSON logs, and plain text.

## When to use

| Skill | Trigger |
|-------|---------|
| `/trace-plan` | Starting a new project or adding observability from scratch |
| `/instrument-code` | Adding log points and spans to specific existing functions |
| `/analyze-traces` | Diagnosing a production issue from captured logs or traces |

## Workflow

```
/trace-plan  -->  /instrument-code  -->  /analyze-traces
  (design)          (implement)           (diagnose)
```

## Dependencies

- **Python**: `structlog`, `opentelemetry-sdk`, `opentelemetry-exporter-otlp`
- **TypeScript**: `pino`, `@opentelemetry/sdk-node`

All dependencies are optional — skills adapt to whatever logging library the project
already uses.

## Sources

Derived from:
- `observability/` patterns (anthropic-cookbook)
- OpenTelemetry semantic conventions
