<!-- last-updated: 2026-03-22 -->

# MCP Server Configurations

Drop-in `.mcp.json` configurations for common integrations.

## Available Configs

| File | Server | Description |
|------|--------|-------------|
| [github.md](github.md) | `github` | GitHub MCP server — issues, PRs, repositories |
| [sqlite.md](sqlite.md) | `sqlite` | SQLite MCP server — local database access |
| [filesystem.md](filesystem.md) | `filesystem` | Extended filesystem access with scoped roots |
| [anthropic-cookbook.md](anthropic-cookbook.md) | `anthropic-cookbook` | Anthropic cookbook as an MCP resource |

## Usage

Copy the `mcpServers` block from any recipe into your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

See each recipe file for full configuration, required environment variables,
and security considerations.
