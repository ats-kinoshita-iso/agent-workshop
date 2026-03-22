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

## Security considerations

**Recommended scope — use the least-privileged token:**
- Prefer **fine-grained personal access tokens** (GitHub Settings → Developer settings →
  Fine-grained tokens) scoped to only the repositories Claude needs to access; classic
  PATs with `repo` scope grant read/write access to ALL your private repositories
- Grant only the permissions actually required: `Issues: Read and write`,
  `Pull requests: Read and write`, `Contents: Read-only` for most workflows — add
  `Contents: Read and write` only if Claude needs to commit or push
- Rotate the token regularly (every 90 days) and immediately if it is exposed in logs,
  environment dumps, or accidentally committed to a repository

**What to avoid:**
- Never commit the token to source control — use environment variables or a secrets
  manager (e.g. `direnv`, `1Password CLI`, `AWS Secrets Manager`)
- Avoid tokens with `admin:org` or `delete_repo` scopes unless absolutely required
- Do not use a token that belongs to a privileged service account with org-admin rights
- Avoid storing the token in `.env` files that are included in the MCP config path

**Rate-limit and permission implications:**
- GitHub's REST API enforces rate limits: 5 000 requests/hour for authenticated users
  and 15 000 for fine-grained tokens on personal accounts; heavy code-search or large
  PR-review workflows can exhaust this budget quickly
- The MCP server acts on behalf of the token owner — any issues or PRs Claude creates
  will appear under your account; use a dedicated bot account for automated workflows
- GitHub audit logs record all API actions; fine-grained tokens make it easier to
  attribute and audit Claude's actions separately from your own
