---
name: mcp-protocol
description: |
Architect and implement the Model Context Protocol (MCP) to create a standardized interface between AI models and local/remote resources.
This skill covers the full lifecycle of MCP:from server-side tool/resource definition to client-side orchestration and transport management.
Use this when building secure data bridges, extending agent capabilities with real-time system access, or standardizing tool-calling patterns across different LLMs.
---

# Model Context Protocol (MCP)

A standardized framework for connecting AI models to external data and tools with safety and efficiency.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Architecture** | Identify if the server is Stdio-based (CLI/Local) or SSE-based (Remote/Web). |
| **Codebase** | Check `backend/mcp_server.py` for existing schemas and `mcp.json` for client configs. |
| **Security** | Determine required environment variables and data sanitization needs for tool inputs. |

## Quick Start (Python SDK)

```python
from mcp.server.fastapi import Context
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent

mcp = Server("enterprise-bridge-v1")

@mcp.tool()
async def fetch_system_metrics(category: str) -> list[TextContent]:
    """Retrieves real-time system metrics for the specified category."""
    # Logic here...
    return [TextContent(type="text", text="CPU: 20%, MEM: 45%")]

# Start via SSE or Stdio
```

## Core Concepts

### 1. Transport Layers
MCP supports multiple ways to communicate:
- **Stdio:** Best for local desktop tools (e.g., Claude Desktop integrations).
- **SSE (Server-Sent Events):** Ideal for web-based microservices and FastAPI integrations.

### 2. Tools (Dynamic Actions)
Tools are the primary way models interact with the world. They require:
- **Strict Typing:** Using Pydantic or type hints for model discovery.
- **Detailed Descriptions:** The model chooses tools based solely on these descriptions.

```python
@mcp.tool()
async def execute_task(task_id: int, ctx: Context) -> str:
    """Executes a background task by ID. Use this for asynchronous processing."""
    await ctx.report_progress(0.1, 1.0)
    # Execution logic...
    return f"Task {task_id} initiated."
```

### 3. Resources (Contextual Data)
Resources act like "files" the AI can read. They can be static or URI-templated.
- **URI Templates:** `db://{table}/{id}`
- **MIME Types:** Specify if content is `text/plain`, `application/json`, etc.

### 4. Prompts (Guided Interaction)
Standardize how models are instructed to handle specific domains.

## Advanced Patterns

### Multi-Server Aggregation
A client can connect to multiple MCP servers simultaneously, creating a unified "Knowledge Graph" for the agent.

### Binary Content Handling
MCP allows returning images or files directly to the model using `ImageContent` or `BlobContent`.

```python
@mcp.tool()
async def capture_screenshot() -> list[ImageContent]:
    """Captures a screenshot for visual debugging."""
    return [ImageContent(type="image", data="base64...", mime_type="image/png")]
```

## Best Practices

| Category | Guideline |
|----------|-----------|
| **Reliability** | Implement timeouts and retries for external API calls within tools. |
| **Security** | Use "Principle of Least Privilege". Don't give tools full shell access if not needed. |
| **Discovery** | Use semantic versioning in server names (e.g., `db-service:v2.1.0`). |
| **UX** | Provide progress updates via `ctx.report_progress` for long-running tools. |

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Generic tool names | `do_stuff()` is useless for LLM reasoning. | Use `update_inventory_count()`. |
| Huge payloads | Exceeds context windows and increases latency. | Use pagination or summaries. |
| Global mutable state | Makes the server non-thread-safe and hard to test. | Pass state through context or DB. |

## Verification Checklist
- [ ] Tool docstrings include both `What` and `When to use`.
- [ ] Inputs are validated using type hints/schemas.
- [ ] Error messages are descriptive enough for the AI to "fix" its call.
- [ ] Server starts correctly via `mcp dev` or standard python runners.