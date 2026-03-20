# GitHub MCP Server Recipe

## When to use

Add this MCP config to give Claude direct access to GitHub issues, pull requests,
repositories, and code search -- without leaving your editor or switching to the browser.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## What becomes available

Once configured, Claude can:
- List and search issues and pull requests
- Read issue comments and PR reviews
- Create issues and PRs directly
- Access repository file trees and file contents
- Search code across repositories
- View commit history and diffs

## Setup

1. Create a GitHub Personal Access Token at https://github.com/settings/tokens
2. Grant scopes: `repo`, `read:org`, `read:user`
3. Set the token as an environment variable: `export GITHUB_TOKEN=ghp_...`
4. Copy the `.mcp.json` snippet into your project root.

## Customization

| Field | What to change |
|-------|---------------|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Rename env var to match your shell export |
| Token scopes | Use a fine-grained token scoped to specific repos for security |
| `npx` vs `bunx` | Replace `npx` with `bunx` if you prefer bun |
