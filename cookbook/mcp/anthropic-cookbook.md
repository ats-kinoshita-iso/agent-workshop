# Anthropic Cookbook MCP Resource Recipe

## When to use

Add this MCP config to expose the `anthropic-cookbook` repository as an in-context
reference. This lets Claude look up patterns, examples, and notebooks from the cookbook
directly while coding, without leaving the editor.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "anthropic-cookbook": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/anthropic-cookbook"
      ]
    }
  }
}
```

## What becomes available

Once configured, Claude can reference:
- `patterns/agents/` -- Orchestrator/worker, evaluator/optimizer, agent loop examples
- `tool_use/` -- Memory management, parallel tools, structured outputs
- `tool_evaluation/` -- Evaluation harness and scoring framework
- `extended_thinking/` -- When and how to use extended thinking
- `claude_agent_sdk/` -- Agent SDK usage patterns
- `capabilities/` -- RAG, embeddings, classification examples

## Setup

1. Clone the anthropic-cookbook repository:
   ```bash
   git clone https://github.com/anthropics/anthropic-cookbook.git /path/to/anthropic-cookbook
   ```
2. Replace `/path/to/anthropic-cookbook` in the config with the actual clone path.
3. Copy the `.mcp.json` snippet into your project root.
4. Restart Claude Code to load the MCP server.

## Patterns that become available

| Directory | Key patterns |
|-----------|-------------|
| `patterns/agents/` | Orchestrator/workers, evaluator/optimizer, basic agent loop |
| `tool_use/` | Memory management, parallel tool calls, structured output |
| `tool_evaluation/` | Repeatable evaluation harness for scoring agent outputs |
| `extended_thinking/` | When to enable extended thinking; budget management |
| `claude_agent_sdk/` | SDK setup, agent lifecycle, tool registration |

## Customization

| Field | What to change |
|-------|---------------|
| Clone path | Update the path to wherever you cloned the cookbook |
| Subdirectory | Pass a subdirectory path to limit scope (e.g., `...cookbook/patterns/agents`) |
| Server name | Rename `"anthropic-cookbook"` to anything meaningful |
