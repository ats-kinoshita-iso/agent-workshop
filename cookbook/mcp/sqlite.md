# SQLite MCP Server Recipe

## When to use

Add this MCP config to give Claude read/write access to a local SQLite database.
Useful for data exploration, schema inspection, query debugging, and migration work.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"]
    }
  }
}
```

## What becomes available

Once configured, Claude can:
- List all tables and their schemas
- Run SELECT queries to inspect data
- Run INSERT, UPDATE, DELETE queries
- Create and modify tables
- Export query results as JSON or CSV

## Setup

1. Install `uvx` if not already available (`uv` ships with it).
2. Ensure your SQLite database file exists at the path specified in `--db-path`.
3. Copy the `.mcp.json` snippet into your project root.
4. Restart Claude Code to load the new MCP server.

## Database path configuration

The `--db-path` argument accepts:
- Relative paths (relative to where Claude Code is launched): `./data/app.db`
- Absolute paths: `/home/user/projects/myapp/app.db`
- `:memory:` for an in-memory database (resets on restart)

## Customization

| Field | What to change |
|-------|---------------|
| `--db-path` | Point to your actual SQLite database file |
| Server name | Rename `"sqlite"` to `"db"` or your database name |
| `uvx` command | Replace with `npx @modelcontextprotocol/server-sqlite` for Node.js variant |
