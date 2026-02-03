# Quickstart: MCP Server

## Prerequisites

- Python 3.12+
- `mcp` package installed
- Local PostgreSQL (Neon) or connection string

## Installation

```bash
pip install mcp
```

## Running the Server

The MCP server runs as a standard process. You can test it using the `mcp-inspector` or by running it directly.

```bash
# Set environment variables
export NEON_DATABASE_URL="postgresql://..."

# Run the server (Stdio mode)
python backend/mcp_server.py
```

## Integrating with Claude Desktop / Agents

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "todo-backend": {
      "command": "python",
      "args": ["/absolute/path/to/project/backend/mcp_server.py"],
      "env": {
        "NEON_DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```
