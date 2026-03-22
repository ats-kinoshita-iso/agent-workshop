# Extended Filesystem MCP Server Recipe

## When to use

Add this MCP config when Claude needs access to directories **outside** the current
project root. By default Claude Code can only access the project directory; this MCP
server grants additional directory access explicitly.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/shared-docs",
        "/home/user/data"
      ]
    }
  }
}
```

## What becomes available

Once configured, Claude can:
- Read files in the specified directories
- List directory contents recursively
- Search for files by name or content
- Write files to the allowed paths (if write permission is granted)

## Allowed paths / roots configuration

The paths listed as positional arguments after the server name define the **allowed roots**.
Claude can only access files within these directories -- not the entire filesystem.

```json
"args": [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "/path/to/dir1",
  "/path/to/dir2",
  "/path/to/dir3"
]
```

Add as many paths as needed. Paths are validated at startup -- non-existent paths cause
the server to fail to start.

## Setup

1. Identify the directories you want Claude to access beyond the project root.
2. Replace the example paths with your actual directory paths.
3. Ensure the paths exist on disk.
4. Copy the snippet into your `.mcp.json` and restart Claude Code.

## Customization

| Field | What to change |
|-------|---------------|
| Path arguments | Replace example paths with your actual directories |
| Number of paths | Add or remove path arguments as needed |
| `npx` vs `bunx` | Replace `npx` with `bunx` if you prefer bun |

## Security considerations

**Recommended scope — expose only what is needed:**
- List only the specific directories Claude requires (e.g. `~/projects/myapp/data`)
  rather than broad roots like `~` or `/home/user`
- Prefer read-only subdirectories; avoid exposing parent directories that contain
  sensitive files (`.ssh/`, `.aws/`, `.gnupg/`, credential stores)
- Avoid including directories that contain secrets, API keys, or private keys
  (e.g. do NOT expose `~/.config`, `~/.ssh`, or any directory holding `.env` files)

**What to avoid:**
- Never expose system directories (`/etc`, `/var`, `C:\Windows\System32`)
- Never expose home directories at the top level — scope to project subdirectories
- Avoid exposing directories shared by multiple users or containing other users' data
- Do not grant write access unless Claude explicitly needs to create or modify files
  in that location; write permission combined with broad roots is high-risk

**Permission and operational implications:**
- The filesystem MCP server inherits the OS-level permissions of the process running
  Claude Code — it cannot exceed those permissions, but it will use them fully
- Audit the allowed paths list whenever the project scope changes
- Consider using a dedicated low-privilege user account when running Claude Code
  in automated or CI environments to limit the blast radius of any path escape
- Paths are not validated for symlink traversal — avoid including directories that
  contain symlinks pointing outside the intended scope
